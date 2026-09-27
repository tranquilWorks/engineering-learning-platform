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


def _pulse_chain(rolloff, span, offset=0):
    rng = np.random.default_rng(1024)
    bits = (rng.random((2, 320)) >= 0.5).astype(int)
    symbols = ((2 * bits[0] - 1) + 1j * (2 * bits[1] - 1)) / np.sqrt(2)
    impulses = np.zeros(2560, complex)
    impulses[::8] = symbols
    pulse = _rrc(rolloff, span)
    rectangular = np.ones(8) / np.sqrt(8)
    bank = (rng.standard_normal(2625) + 1j * rng.standard_normal(2625)) / np.sqrt(2)
    tx = np.convolve(impulses, pulse)
    rx = tx + 10 ** (-14 / 20) * bank[: len(tx)]
    matched = np.convolve(rx, pulse[::-1].conj())
    indices = len(pulse) - 1 + np.arange(320) * 8
    samples = matched[indices + offset]
    clean = np.convolve(tx, pulse[::-1].conj())[indices]
    raw = rx[(len(pulse) - 1) // 2 + np.arange(320) * 8] / pulse[len(pulse) // 2]
    rect_tx = np.convolve(impulses, rectangular)
    rect_rx = rect_tx + 10 ** (-14 / 20) * bank[: len(rect_tx)]
    rect_samples = np.convolve(rect_rx, rectangular[::-1])[7 + np.arange(320) * 8]
    valid = slice(span, 320 - span)
    evm = lambda v: float(100 * np.sqrt(np.mean(abs(v[valid] - symbols[valid]) ** 2)))
    ser = float(
        np.mean(
            np.any(np.array([samples.real >= 0, samples.imag >= 0]) != bits, axis=0)
        )
    )
    return (
        pulse,
        symbols,
        tx,
        matched,
        samples,
        [evm(rect_samples), evm(raw), evm(samples), evm(clean), ser],
    )


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    rolloff = float(parameters.get("rolloff", 0.25))
    span = int(parameters.get("span_symbols", 8))
    broken = bool(parameters.get("broken_mode", False))
    if rolloff not in {0.1, 0.25, 0.5, 1.0} or span not in {2, 4, 6, 8}:
        raise ValueError("Choose a retained RRC rolloff and finite span")
    pulse, _symbols, tx, matched, samples, metrics = _pulse_chain(
        rolloff, span, 4 if broken else 0
    )
    recovery = _pulse_chain(rolloff, span)
    signature = [
        float(np.sum(pulse**2)),
        len(pulse) - 1,
        *metrics,
        recovery[5][2],
        float(np.max(abs(pulse - pulse[::-1]))),
    ]
    fields = [
        ("pulse_energy", "normalized energy"),
        ("total_group_delay", "samples"),
        ("rectangular_evm", "percent"),
        ("raw_evm", "percent"),
        ("matched_evm", "percent"),
        ("finite_span_isi_evm", "percent"),
        ("symbol_error_rate", "ratio"),
        ("aligned_recovery_evm", "percent"),
        ("pulse_symmetry_error", "normalized amplitude"),
    ]
    alpha_values, span_values = [0.1, 0.25, 0.5, 1.0], [2, 4, 6, 8]
    rr = [_pulse_chain(a, span)[5] for a in alpha_values]
    sr = [_pulse_chain(rolloff, s)[5] for s in span_values]
    freq = np.fft.fftshift(np.fft.fftfreq(4096, 1 / 8))
    rect = np.ones(8) / np.sqrt(8)
    plots = {
        "pulses": _plot(
            "Finite unit-energy pulses",
            "Time (symbol periods)",
            "Pulse amplitude (normalized)",
            [
                ("RRC", (np.arange(len(pulse)) - len(pulse) // 2) / 8, pulse),
                ("rectangular", np.arange(8) / 8, rect),
            ],
        ),
        "waveform": _plot(
            "Transmit convolution and received matched output",
            "Time (symbol periods)",
            "In-phase (normalized amplitude)",
            [
                ("transmitted", np.arange(160) / 8, tx.real[:160]),
                (
                    "matched, delay removed",
                    np.arange(160) / 8,
                    matched.real[len(pulse) - 1 : len(pulse) + 159],
                ),
            ],
        ),
        "spectrum": _plot(
            "Pulse spectral containment",
            "Frequency (cycles/symbol)",
            "Relative power (dB)",
            [
                (
                    "RRC",
                    freq,
                    20
                    * np.log10(
                        np.maximum(
                            abs(np.fft.fftshift(np.fft.fft(pulse, 4096))) / np.sqrt(8),
                            1e-8,
                        )
                    ),
                ),
                (
                    "rectangular",
                    freq,
                    20
                    * np.log10(
                        np.maximum(
                            abs(np.fft.fftshift(np.fft.fft(rect, 4096))) / np.sqrt(8),
                            1e-8,
                        )
                    ),
                ),
            ],
        ),
        "eye": _plot(
            "Forty matched-filter eye traces",
            "Offset (symbol periods)",
            "In-phase (normalized amplitude)",
            [
                (
                    f"symbol {k}",
                    np.arange(-8, 9) / 8,
                    matched.real[
                        len(pulse) - 1 + k * 8 - 8 : len(pulse) - 1 + k * 8 + 9
                    ],
                )
                for k in range(span + 1, span + 41)
            ],
        ),
        "decisions": _plot(
            "Timing controls the sampled constellation",
            "In-phase (normalized amplitude)",
            "Quadrature (normalized amplitude)",
            [
                ("active samples", samples.real, samples.imag),
                ("aligned", recovery[4].real, recovery[4].imag),
            ],
        ),
        "rolloff_sweep": _plot(
            "Rolloff at fixed span",
            "Rolloff (ratio)",
            "EVM (percent)",
            [
                ("matched", alpha_values, [m[2] for m in rr]),
                ("noiseless ISI", alpha_values, [m[3] for m in rr]),
            ],
        ),
        "span_sweep": _plot(
            "Span at fixed rolloff",
            "Finite span (symbols)",
            "EVM (percent)",
            [
                ("matched", span_values, [m[2] for m in sr]),
                ("noiseless ISI", span_values, [m[3] for m in sr]),
            ],
        ),
    }
    for trace in plots["decisions"]["data"]:
        trace["mode"] = "markers"
    return _result(
        signature,
        fields,
        plots,
        {
            "observation": "The explicit RRC singularity limits produce a finite unit-energy pulse. The conjugate reversed receiver filter peaks after the total transmit/receive delay; finite truncation leaves measurable ISI.",
            "broken": "Sampling four samples late is a half-symbol timing error. Even a correct matched filter cannot open the constellation at the wrong sampling instant.",
            "recovery": "Align samples at len(pulse)-1 plus multiples of eight. Compare aligned noisy EVM, noiseless residual ISI, and the rectangular reference.",
        },
        1024,
        broken,
        {
            "symbol_count": 320,
            "samples_per_symbol": 8,
            "timing_offset_samples": 4 if broken else 0,
        },
    )
