from __future__ import annotations

from typing import Any

import numpy as np

SEED = 1016
FS_HZ = 2048.0
COUNT = 4096


def _layout(title: str, x_label: str, y_label: str) -> dict[str, Any]:
    return {
        "title": {"text": title, "x": 0.02},
        "xaxis": {"title": x_label},
        "yaxis": {"title": y_label},
        "legend": {"orientation": "h", "y": 1.14},
        "margin": {"l": 68, "r": 22, "t": 58, "b": 58},
    }


def _analytic(values: np.ndarray) -> np.ndarray:
    if len(values) != COUNT:
        raise ValueError("analytic-signal record must contain 4096 samples")
    mask = np.zeros(COUNT)
    mask[0] = 1.0
    mask[1 : COUNT // 2] = 2.0
    mask[COUNT // 2] = 1.0
    return np.fft.ifft(np.fft.fft(values) * mask)


def _case(depth: float, deviation: float, broken: bool) -> dict[str, Any]:
    if depth not in {0.2, 0.6, 0.9}:
        raise ValueError("envelope_depth must be 0.2, 0.6, or 0.9")
    if deviation not in {0.2, 0.6, 1.2}:
        raise ValueError("phase_deviation_rad must be 0.2, 0.6, or 1.2")
    sample = np.arange(COUNT)
    time = sample / FS_HZ
    envelope = 1.0 + depth * np.cos(2.0 * np.pi * 2.0 * time)
    phase = (
        2.0 * np.pi * 240.0 * time + 0.35 + deviation * np.sin(2.0 * np.pi * 3.0 * time)
    )
    designed_frequency = 240.0 + deviation * 3.0 * np.cos(2.0 * np.pi * 3.0 * time)
    rng = np.random.default_rng(SEED)
    if broken:
        envelope = 1.0 - 0.999 * np.exp(-0.5 * ((time - 1.0) / 0.025) ** 2)
        noise = 0.010 * rng.standard_normal(COUNT)
    else:
        noise = 0.002 * rng.standard_normal(COUNT)
    observed = envelope * np.cos(phase) + noise
    analytic = _analytic(observed)
    recovered_envelope = np.abs(analytic)
    recovered_phase = np.unwrap(np.angle(analytic))
    raw_frequency = np.empty(COUNT)
    raw_frequency[0] = 240.0
    raw_frequency[1:] = np.diff(recovered_phase) * FS_HZ / (2.0 * np.pi)
    reliable = recovered_envelope >= 0.05
    reliable[1:] &= reliable[:-1]
    reliable[:128] = False
    reliable[-128:] = False
    gated_frequency = np.where(reliable, raw_frequency, 240.0)
    evaluation = np.zeros(COUNT, dtype=bool)
    evaluation[128:-128] = True
    envelope_rmse = float(
        np.sqrt(np.mean((recovered_envelope[evaluation] - envelope[evaluation]) ** 2))
    )
    frequency_rmse = float(
        np.sqrt(np.mean((raw_frequency[reliable] - designed_frequency[reliable]) ** 2))
    )
    spectrum = np.fft.fftshift(np.fft.fft(analytic)) / COUNT
    frequency = np.fft.fftshift(np.fft.fftfreq(COUNT, 1.0 / FS_HZ))
    negative = frequency < 0
    positive = frequency > 0
    suppression = float(
        10.0
        * np.log10(
            max(float(np.sum(np.abs(spectrum[positive]) ** 2)), 1e-30)
            / max(float(np.sum(np.abs(spectrum[negative]) ** 2)), 1e-30)
        )
    )
    low = recovered_envelope < 0.05
    raw_spike = (
        float(np.max(np.abs(raw_frequency[low] - designed_frequency[low])))
        if np.any(low)
        else 0.0
    )
    return {
        "time": time,
        "observed": observed,
        "envelope": envelope,
        "recovered_envelope": recovered_envelope,
        "recovered_phase": recovered_phase,
        "designed_frequency": designed_frequency,
        "raw_frequency": raw_frequency,
        "gated_frequency": gated_frequency,
        "reliable": reliable,
        "frequency": frequency,
        "spectrum": np.abs(spectrum),
        "envelope_rmse": envelope_rmse,
        "frequency_rmse": frequency_rmse,
        "suppression": suppression,
        "raw_spike": raw_spike,
        "withheld": int(np.count_nonzero(evaluation & ~reliable)),
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    depth = float(parameters["envelope_depth"])
    deviation = float(parameters["phase_deviation_rad"])
    broken = bool(parameters["broken_mode"])
    case = _case(depth, deviation, broken)
    depth_sweep = np.array([0.2, 0.6, 0.9])
    depth_rmse = [
        _case(float(value), 0.6, False)["envelope_rmse"] for value in depth_sweep
    ]
    deviation_sweep = np.array([0.2, 0.6, 1.2])
    recovered_span = []
    for value in deviation_sweep:
        item = _case(0.6, float(value), False)
        recovered_span.append(
            float(
                np.percentile(item["raw_frequency"][item["reliable"]], 95)
                - np.percentile(item["raw_frequency"][item["reliable"]], 5)
            )
        )
    display = np.arange(0, COUNT, 8)
    spectrum_display = np.arange(0, COUNT, 8)
    signature = [
        depth,
        deviation,
        case["envelope_rmse"],
        case["frequency_rmse"],
        case["suppression"],
        float(np.min(case["recovered_envelope"])),
        case["raw_spike"],
        float(case["withheld"]),
    ]
    return {
        "metrics": [
            {
                "id": "envelope_rmse",
                "label": "Envelope RMSE",
                "value": case["envelope_rmse"],
                "unit": "V",
            },
            {
                "id": "frequency_rmse",
                "label": "Reliable IF RMSE",
                "value": case["frequency_rmse"],
                "unit": "Hz",
                "emphasis": "primary",
            },
            {
                "id": "negative_suppression",
                "label": "Negative-frequency suppression",
                "value": case["suppression"],
                "unit": "dB",
            },
            {
                "id": "withheld",
                "label": "Unreliable samples withheld",
                "value": case["withheld"],
                "unit": "samples",
            },
        ],
        "plots": {
            "waveform_envelope": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "real waveform",
                        "x": case["time"][display],
                        "y": case["observed"][display],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "designed envelope",
                        "x": case["time"][display],
                        "y": case["envelope"][display],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "recovered envelope",
                        "x": case["time"][display],
                        "y": case["recovered_envelope"][display],
                    },
                ],
                "layout": _layout(
                    "Analytic envelope recovery", "Time (s)", "Amplitude (V)"
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "analytic_spectrum": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "analytic magnitude",
                        "x": case["frequency"][spectrum_display],
                        "y": case["spectrum"][spectrum_display],
                    }
                ],
                "layout": _layout(
                    "One-sided analytic spectrum",
                    "Signed frequency (Hz)",
                    "Magnitude (V)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "parameter_sweeps": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "envelope RMSE",
                        "x": depth_sweep,
                        "y": depth_rmse,
                    },
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "IF span",
                        "x": deviation_sweep,
                        "y": recovered_span,
                        "yaxis": "y2",
                    },
                ],
                "layout": _layout(
                    "Envelope-depth and phase-deviation sweeps",
                    "Control value",
                    "Envelope RMSE (V)",
                )
                | {
                    "yaxis2": {
                        "title": "IF span (Hz)",
                        "overlaying": "y",
                        "side": "right",
                    }
                },
                "config": {"responsive": True, "displaylogo": False},
            },
            "reliability_gate": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "raw instantaneous frequency",
                        "x": case["time"][display],
                        "y": case["raw_frequency"][display],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "amplitude-gated frequency",
                        "x": case["time"][display],
                        "y": case["gated_frequency"][display],
                    },
                ],
                "layout": _layout(
                    "Near-zero-envelope failure and gate",
                    "Time (s)",
                    "Instantaneous frequency (Hz)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "The explicit even-length Hilbert mask retains DC and Nyquist, doubles positive-frequency bins, and suppresses the redundant negative-frequency half.",
            "broken": "Near a zero envelope, noise controls phase and differentiation turns the phase jump into a large false instantaneous-frequency spike.",
            "recovery": "Require both adjacent analytic samples to clear the amplitude threshold before reporting the phase-difference frequency estimate.",
        },
        "diagnostics": {
            "seed": SEED,
            "signature": signature,
            "broken_active": broken,
            "hilbert_mask_dc": 1.0,
            "hilbert_mask_nyquist": 1.0,
            "hilbert_mask_positive": 2.0,
        },
    }
