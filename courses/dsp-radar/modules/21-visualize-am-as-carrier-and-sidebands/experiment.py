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


def _am(depth, frequency, multitone=False, noisy=True):
    time = np.arange(2000) / 20000
    message = (
        0.6 * np.cos(2 * np.pi * 100 * time) + 0.4 * np.cos(2 * np.pi * 350 * time)
        if multitone
        else np.cos(2 * np.pi * frequency * time)
    )
    envelope = 1 + depth * message
    carrier = np.cos(2 * np.pi * 3000 * time)
    noise = 0.005 * np.random.default_rng(1021).standard_normal(2000) if noisy else 0
    received = envelope * carrier + noise
    transform = np.fft.fft(received)
    mask = np.zeros(2000)
    mask[0] = mask[1000] = 1
    mask[1:1000] = 2
    detected = np.abs(np.fft.ifft(transform * mask))
    baseband = np.fft.ifft(
        np.fft.fft(2 * received * carrier)
        * (np.abs(np.fft.fftfreq(2000, 1 / 20000)) <= 900)
    ).real
    env_message, coh_message = (detected - 1) / depth, (baseband - 1) / depth
    amplitude = 2 * np.abs(transform[:1001]) / 2000
    amplitude[[0, -1]] /= 2
    return (
        time,
        message,
        envelope,
        received,
        detected,
        env_message,
        coh_message,
        amplitude,
    )


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    depth = float(parameters.get("modulation_depth", 0.6))
    frequency = float(parameters.get("message_frequency_hz", 200))
    broken = bool(parameters.get("broken_mode", False))
    if depth not in {0.2, 0.6, 1.0, 1.4} or frequency not in {100, 200, 400, 700}:
        raise ValueError("Choose a retained AM depth and message frequency")
    active_depth = 1.4 if broken else depth
    t, message, envelope, rf, detected, env, coherent, amplitude = _am(
        active_depth, frequency
    )
    multi = _am(depth, frequency, True)
    depth_values = [0.2, 0.6, 1.0, 1.4]
    frequency_values = [100, 200, 400, 700]
    depth_runs = [_am(d, frequency, noisy=False) for d in depth_values]
    frequency_runs = [_am(depth, f, noisy=False) for f in frequency_values]
    signature = [
        active_depth,
        frequency,
        amplitude[300],
        amplitude[int((3000 - frequency) / 10)],
        amplitude[int((3000 + frequency) / 10)],
        float(np.min(envelope)),
        float(np.sqrt(np.mean((env - message) ** 2))),
        float(np.sqrt(np.mean((coherent - message) ** 2))),
        *multi[7][[265, 290, 310, 335]],
    ]
    fields = [
        ("active_depth", "ratio"),
        ("message_frequency", "Hz"),
        ("carrier_amplitude", "V"),
        ("lower_sideband", "V"),
        ("upper_sideband", "V"),
        ("minimum_signed_envelope", "V"),
        ("envelope_rmse", "normalized amplitude"),
        ("coherent_rmse", "normalized amplitude"),
        *[(f"multitone_line_{f}", "V") for f in [2650, 2900, 3100, 3350]],
    ]
    plots = {
        "multitone_recovery": _plot(
            "Two-tone envelope and coherent recovery",
            "Time (ms)",
            "Message (normalized amplitude)",
            [
                ("truth", 1000 * multi[0][:200], multi[1][:200]),
                ("envelope", 1000 * multi[0][:200], multi[5][:200]),
                ("coherent", 1000 * multi[0][:200], multi[6][:200]),
            ],
        ),
        "rf_envelope": _plot(
            "Signed envelope and magnitude detector",
            "Time (ms)",
            "Voltage (V)",
            [
                ("received RF", 1000 * t[:200], rf[:200]),
                ("signed envelope", 1000 * t[:200], envelope[:200]),
                ("magnitude envelope", 1000 * t[:200], detected[:200]),
            ],
        ),
        "spectrum": _plot(
            "Carrier and sideband pairs",
            "RF frequency (Hz)",
            "Amplitude (V)",
            [
                ("single tone", np.arange(240, 361) * 10, amplitude[240:361]),
                ("100/350 Hz multitone", np.arange(240, 361) * 10, multi[7][240:361]),
            ],
        ),
        "recovery": _plot(
            "Envelope versus coherent recovery",
            "Time (ms)",
            "Message (normalized amplitude)",
            [
                ("truth", 1000 * t[:200], message[:200]),
                ("magnitude detector", 1000 * t[:200], env[:200]),
                ("900 Hz coherent lowpass", 1000 * t[:200], coherent[:200]),
            ],
        ),
        "depth_sweep": _plot(
            "Depth sweep: noiseless envelope folding",
            "Modulation depth (ratio)",
            "Message RMSE (normalized amplitude)",
            [
                (
                    "envelope",
                    depth_values,
                    [np.sqrt(np.mean((r[5] - r[1]) ** 2)) for r in depth_runs],
                ),
                (
                    "coherent",
                    depth_values,
                    [np.sqrt(np.mean((r[6] - r[1]) ** 2)) for r in depth_runs],
                ),
            ],
        ),
        "frequency_sweep": _plot(
            "Frequency sweep: sideband locations",
            "Message frequency (Hz)",
            "RF sideband frequency (Hz)",
            [
                ("lower", frequency_values, 3000 - np.array(frequency_values)),
                ("upper", frequency_values, 3000 + np.array(frequency_values)),
            ],
        ),
    }
    return _result(
        signature,
        fields,
        plots,
        {
            "observation": "Multiplication creates carrier ± message-frequency lines; each sideband has depth/2 times the carrier amplitude. The multitone view retains both pairs.",
            "broken": "At depth 1.4 the signed envelope crosses zero. Magnitude detection folds the negative envelope and distorts the message.",
            "recovery": "The explicit coherent mixer and 900 Hz lowpass retain envelope sign, even during overmodulation. Disable the failure to restore the selected depth.",
        },
        1021,
        broken,
        {
            "sample_count": 2000,
            "frequency_sweep_coherent_rmse": [
                float(np.sqrt(np.mean((r[6] - r[1]) ** 2))) for r in frequency_runs
            ],
        },
    )
