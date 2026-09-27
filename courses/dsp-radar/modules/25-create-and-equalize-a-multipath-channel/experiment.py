from __future__ import annotations

from typing import Any

import numpy as np


def _plot(title, xlabel, ylabel, traces):
    data = []
    for name, x, y in traces:
        x, y = np.asarray(x), np.asarray(y)
        indices = np.unique(np.linspace(0, len(x) - 1, min(len(x), 512)).astype(int))
        data.append(
            {
                "type": "scatter",
                "mode": "lines",
                "name": name,
                "x": x[indices].tolist(),
                "y": y[indices].tolist(),
            }
        )
    return {
        "data": data,
        "layout": {
            "title": {"text": title},
            "xaxis": {"title": xlabel},
            "yaxis": {"title": ylabel},
            "legend": {"orientation": "h"},
        },
        "config": {"responsive": True, "displaylogo": False},
    }


def _result(signature, fields, plots, explanations, seed, broken, extra=None):
    return {
        "metrics": [
            {
                "id": fields[i][0],
                "label": fields[i][0].replace("_", " "),
                "value": float(v),
                "unit": fields[i][1],
            }
            for i, v in enumerate(signature)
        ],
        "plots": plots,
        "explanations": explanations,
        "diagnostics": {
            "signature": [float(v) for v in signature],
            "signature_fields": [f[0] for f in fields],
            "seed": seed,
            "broken_active": broken,
            **(extra or {}),
        },
    }


def _rrc(rolloff, span):
    time = np.arange(-span * 4, span * 4 + 1) / 8
    pulse = np.empty(len(time))
    for i, x in enumerate(time):
        if abs(x) < 1e-12:
            pulse[i] = 1 + rolloff * (4 / np.pi - 1)
        elif abs(abs(x) - 1 / (4 * rolloff)) < 1e-12:
            pulse[i] = (
                rolloff
                / np.sqrt(2)
                * (
                    (1 + 2 / np.pi) * np.sin(np.pi / (4 * rolloff))
                    + (1 - 2 / np.pi) * np.cos(np.pi / (4 * rolloff))
                )
            )
        else:
            pulse[i] = (
                np.sin(np.pi * x * (1 - rolloff))
                + 4 * rolloff * x * np.cos(np.pi * x * (1 + rolloff))
            ) / (np.pi * x * (1 - (4 * rolloff * x) ** 2))
    return pulse / np.sqrt(np.sum(abs(pulse) ** 2))


def _equalize(echo, regularization, deep=False):
    rng = np.random.default_rng(1025)
    bits = (rng.random((2, 480)) >= 0.5).astype(int)
    symbols = ((2 * bits[0] - 1) + 1j * (2 * bits[1] - 1)) / np.sqrt(2)
    pulse = _rrc(0.25, 8)
    impulses = np.zeros(3840, complex)
    impulses[::8] = symbols
    tx = np.convolve(impulses, pulse)
    h = (
        np.array([1, -0.999], complex)
        if deep
        else np.array([1, echo * np.exp(0.45j), 0.2 * np.exp(-0.8j)])
    )
    channel = np.zeros((len(h) - 1) * 8 + 1, complex)
    channel[::8] = h
    propagated = np.convolve(tx, channel)
    # A fixed 3920-sample bank keeps echo/regularization sweeps on identical noise.
    noise = (rng.standard_normal(3920) + 1j * rng.standard_normal(3920)) / np.sqrt(2)
    rx = propagated + 10 ** (-18 / 20) * noise[: len(propagated)]
    matched = np.convolve(rx, pulse[::-1].conj())
    samples = matched[64 + np.arange(480 + len(h) - 1) * 8]
    matrix = np.zeros((len(h) + 30, 31), complex)
    for column in range(31):
        matrix[column : column + len(h), column] = h
    target = np.zeros(len(h) + 30)
    target[0] = 1
    zf = np.linalg.solve(matrix[:31], target[:31])
    regular = np.linalg.solve(
        matrix.conj().T @ matrix + regularization * np.eye(31), matrix.conj().T @ target
    )
    output = [
        samples[:480],
        np.convolve(samples, zf)[:480],
        np.convolve(samples, regular)[:480],
    ]
    evm = [
        float(100 * np.sqrt(np.mean(abs(v[40:-40] - symbols[40:-40]) ** 2)))
        for v in output
    ]
    ser = [
        float(
            np.mean(
                np.any(
                    np.array([v.real >= 0, v.imag >= 0])[:, 40:-40] != bits[:, 40:-40],
                    axis=0,
                )
            )
        )
        for v in output
    ]
    gain = [float(10 * np.log10(np.sum(abs(w) ** 2))) for w in [zf, regular]]
    residual = float(100 * np.linalg.norm(matrix @ regular - target))
    response = np.fft.fftshift(np.fft.fft(h, 2048))
    combined = np.convolve(np.convolve(pulse, channel), pulse[::-1].conj())[::8]
    return (
        h,
        samples,
        output,
        evm,
        ser,
        gain,
        residual,
        response,
        combined,
        regular,
        zf,
        matched,
    )


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    echo = float(parameters.get("echo_gain", 0.45))
    regularization = float(parameters.get("regularization", 10 ** (-18 / 10)))
    broken = bool(parameters.get("broken_mode", False))
    if echo not in {0, 0.25, 0.45, 0.5, 0.75} or regularization not in {
        0.001,
        0.01,
        0.03,
        0.1,
        10 ** (-18 / 10),
    }:
        raise ValueError("Choose a retained echo gain and regularization")
    active = _equalize(echo, regularization, broken)
    deep = _equalize(echo, 0.01, True)
    (
        h,
        _samples,
        outputs,
        evm,
        ser,
        gains,
        residual,
        response,
        combined,
        regular,
        zf,
        matched,
    ) = active
    signature = [
        *evm,
        *ser,
        *gains,
        residual,
        20 * np.log10(max(float(min(abs(response))), 1e-12)),
        deep[3][1],
        deep[3][2],
        deep[5][0],
        deep[5][1],
        deep[6],
    ]
    fields = [
        (name, unit)
        for name, unit in [
            ("unequalized_evm", "percent"),
            ("zf_evm", "percent"),
            ("regularized_evm", "percent"),
            ("unequalized_ser", "ratio"),
            ("zf_ser", "ratio"),
            ("regularized_ser", "ratio"),
            ("zf_noise_gain", "dB"),
            ("regularized_noise_gain", "dB"),
            ("residual_impulse_error", "percent"),
            ("minimum_channel_response", "dB"),
            ("deep_null_zf_evm", "percent"),
            ("deep_null_recovery_evm", "percent"),
            ("deep_null_zf_gain", "dB"),
            ("deep_null_recovery_gain", "dB"),
            ("deep_null_residual", "percent"),
        ]
    ]
    echoes, lambdas = [0, 0.25, 0.5, 0.75], [0.001, 0.01, 0.03, 0.1]
    echo_runs = [_equalize(e, 10 ** (-18 / 10)) for e in echoes]
    regular_runs = [_equalize(echo, l, True) for l in lambdas]
    plots = {
        "equalizer_taps": _plot(
            "Finite inverse tap magnitudes",
            "Tap index (integer)",
            "Magnitude (gain)",
            [
                ("ZF", np.arange(31), abs(zf)),
                ("regularized", np.arange(31), abs(regular)),
            ],
        ),
        "eye": _plot(
            "Matched-channel eye before equalization",
            "Offset (symbol periods)",
            "In-phase (normalized amplitude)",
            [
                (
                    f"symbol {k}",
                    np.arange(-8, 9) / 8,
                    matched.real[64 + k * 8 - 8 : 64 + k * 8 + 9],
                )
                for k in range(40, 72)
            ],
        ),
        "paths": _plot(
            "Delayed complex path coefficients",
            "Delay (symbols)",
            "Complex gain component (ratio)",
            [
                ("real", np.arange(len(h)), h.real),
                ("imaginary", np.arange(len(h)), h.imag),
            ],
        ),
        "symbol_response": _plot(
            "Pulse/channel/matched-filter sampled response",
            "Delay (symbols)",
            "Response component (ratio)",
            [
                ("real", np.arange(len(combined)) - 8, combined.real),
                ("imaginary", np.arange(len(combined)) - 8, combined.imag),
            ],
        ),
        "channel_spectrum": _plot(
            "Destructive interference produces a notch",
            "Frequency (cycles/symbol)",
            "Channel magnitude (dB)",
            [
                (
                    "active channel",
                    np.arange(-1024, 1024) / 2048,
                    20 * np.log10(np.maximum(abs(response), 1e-12)),
                )
            ],
        ),
        "constellation": _plot(
            "Equalizer symbol decisions",
            "In-phase (normalized amplitude)",
            "Quadrature (normalized amplitude)",
            [
                (name, v.real[40:-40], v.imag[40:-40])
                for name, v in zip(
                    ["unequalized", "ZF", "regularized"], outputs, strict=True
                )
            ],
        ),
        "echo_sweep": _plot(
            "Echo strength with fixed pulse and noise",
            "One-symbol echo gain (ratio)",
            "EVM (percent)",
            [
                ("unequalized", echoes, [r[3][0] for r in echo_runs]),
                ("regularized", echoes, [r[3][2] for r in echo_runs]),
            ],
        ),
        "regularization_sweep": _plot(
            "Deep-null regularization tradeoff",
            "Regularization (ratio)",
            "Error (percent)",
            [
                ("symbol EVM", lambdas, [r[3][2] for r in regular_runs]),
                ("impulse distortion", lambdas, [r[6] for r in regular_runs]),
            ],
        ),
        "noise_gain": _plot(
            "Deep-null inverse noise gain",
            "Regularization (ratio)",
            "Noise gain (dB)",
            [
                ("regularized", lambdas, [r[5][1] for r in regular_runs]),
                ("ZF", lambdas, [deep[5][0]] * 4),
            ],
        ),
    }
    for trace in plots["constellation"]["data"]:
        trace["mode"] = "markers"
    return _result(
        signature,
        fields,
        plots,
        {
            "observation": "Delayed pulse-shaped paths smear neighboring QPSK symbols. A 31-tap causal inverse cancels the leading response; regularization also penalizes tap energy.",
            "broken": "The [1,-0.999] path has a -60 dB DC null. Finite ZF inversion boosts noise and leaves a tail: its symbol EVM and noise gain reveal the cost.",
            "recovery": "The deep-null comparison uses lambda=0.01, nearest the 18 dB noise variance in the source grid. Regularization reduces noise enhancement but retains reported residual distortion; it does not perfectly recover lost information.",
        },
        1025,
        broken,
        {
            "symbol_count": 480,
            "equalizer_taps": 31,
            "noise_bank_samples": 3920,
            "deep_null_recovery_lambda": 0.01,
        },
    )
