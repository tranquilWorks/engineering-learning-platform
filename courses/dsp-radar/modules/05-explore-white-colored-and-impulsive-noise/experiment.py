from __future__ import annotations

from typing import Any

import numpy as np

SEED = 505
MAX_SAMPLES = 5000


def _layout(title: str, x_label: str, y_label: str) -> dict[str, Any]:
    return {
        "title": {"text": title, "x": 0.02},
        "xaxis": {"title": x_label},
        "yaxis": {"title": y_label},
        "legend": {"orientation": "h", "y": 1.14},
        "margin": {"l": 68, "r": 22, "t": 58, "b": 58},
    }


def _normalize(record: np.ndarray, target_rms: float) -> np.ndarray:
    centered = record - np.mean(record)
    rms = float(np.sqrt(np.mean(centered**2)))
    if rms <= 1e-14:
        raise ValueError("noise record has zero centered RMS")
    return centered * target_rms / rms


def _metrics(record: np.ndarray, fs: float) -> dict[str, float]:
    rms = float(np.sqrt(np.mean(record**2)))
    crest = float(np.max(np.abs(record)) / max(rms, 1e-15))
    lag_one = float(np.corrcoef(record[:-1], record[1:])[0, 1])
    spectrum = np.abs(np.fft.rfft(record)) ** 2
    frequency = np.fft.rfftfreq(len(record), 1.0 / fs)
    low_power = float(
        np.sum(spectrum[frequency <= 200.0]) / max(np.sum(spectrum), 1e-30)
    )
    return {"rms": rms, "crest": crest, "lag_one": lag_one, "low_power": low_power}


def _case(
    alpha: float, interferer_offset_hz: float, target_rms: float, broken: bool
) -> dict[str, Any]:
    if (
        not 0.0 <= alpha <= 0.99
        or not 5.0 <= interferer_offset_hz <= 700.0
        or not 0.05 <= target_rms <= 0.6
    ):
        raise ValueError("noise controls exceed the bounded experiment range")
    fs = 4096.0
    count = 4096
    if count > MAX_SAMPLES:
        raise ValueError("noise record exceeds the resource ceiling")
    time = np.arange(count, dtype=float) / fs
    rng = np.random.default_rng(SEED)
    white_raw = rng.standard_normal(count)
    colored_raw = np.empty(count)
    colored_raw[0] = white_raw[0]
    for index in range(1, count):
        colored_raw[index] = alpha * colored_raw[index - 1] + white_raw[index]
    narrow_raw = np.sin(2.0 * np.pi * (512.0 + interferer_offset_hz) * time + 0.3)
    impulsive_raw = rng.standard_normal(count)
    mask = rng.random(count) < 0.01
    impulsive_raw[mask] += 12.0 * rng.choice(
        np.array([-1.0, 1.0]), int(np.count_nonzero(mask))
    )
    raw = {
        "white": white_raw,
        "colored": colored_raw,
        "narrowband": narrow_raw,
        "impulsive": impulsive_raw,
    }
    records = (
        raw
        if broken
        else {name: _normalize(value, target_rms) for name, value in raw.items()}
    )
    record_metrics = {name: _metrics(value, fs) for name, value in records.items()}
    tone = 0.18 * np.sin(2.0 * np.pi * 512.0 * time)
    basis = np.exp(-1j * 2.0 * np.pi * 512.0 * time)
    tone_errors = {}
    for name, noise in records.items():
        estimate = 2.0 * abs(np.vdot(basis, tone + noise)) / count
        tone_errors[name] = float(abs(estimate - 0.18))
    normalized = {name: _normalize(value, target_rms) for name, value in raw.items()}
    recovery_residual = max(
        abs(_metrics(value, fs)["rms"] - target_rms) for value in normalized.values()
    )
    return {
        "time": time,
        "records": records,
        "metrics": record_metrics,
        "tone_errors": tone_errors,
        "recovery_residual": float(recovery_residual),
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    alpha = float(parameters["colored_memory"])
    offset = float(parameters["interferer_offset_hz"])
    target_rms = float(parameters["noise_rms_v"])
    broken = bool(parameters["broken_mode"])
    case = _case(alpha, offset, target_rms, broken)
    alpha_sweep = np.array([0.0, 0.7, 0.92])
    alpha_lag = [
        _case(float(value), 100.0, 0.25, False)["metrics"]["colored"]["lag_one"]
        for value in alpha_sweep
    ]
    offset_sweep = np.array([20.0, 100.0, 300.0])
    offset_error = [
        _case(0.92, float(value), 0.25, False)["tone_errors"]["narrowband"]
        for value in offset_sweep
    ]
    metrics = case["metrics"]
    view = slice(0, 256)
    return {
        "metrics": [
            {
                "id": "white_rms",
                "label": "White RMS",
                "value": metrics["white"]["rms"],
                "unit": "V RMS",
            },
            {
                "id": "colored_lag_one",
                "label": "Colored lag-one correlation",
                "value": metrics["colored"]["lag_one"],
                "unit": "correlation",
                "emphasis": "primary",
            },
            {
                "id": "impulsive_crest",
                "label": "Impulsive crest factor",
                "value": metrics["impulsive"]["crest"],
                "unit": "ratio",
            },
            {
                "id": "narrow_tone_error",
                "label": "Tone estimate error",
                "value": case["tone_errors"]["narrowband"],
                "unit": "V",
            },
        ],
        "plots": {
            "noise_records": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": name,
                        "x": case["time"][view],
                        "y": record[view],
                    }
                    for name, record in case["records"].items()
                ],
                "layout": _layout(
                    "Equal-RMS noise can have different structure",
                    "Time (s)",
                    "Noise voltage (V)",
                ),
            },
            "noise_statistics": {
                "data": [
                    {
                        "type": "bar",
                        "name": "crest factor",
                        "x": list(metrics),
                        "y": [value["crest"] for value in metrics.values()],
                    },
                    {
                        "type": "bar",
                        "name": "low-frequency power fraction",
                        "x": list(metrics),
                        "y": [value["low_power"] for value in metrics.values()],
                    },
                ],
                "layout": _layout("Noise diagnostics", "Noise family", "Ratio"),
            },
            "parameter_sweeps": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "colored-memory sweep",
                        "x": alpha_sweep,
                        "y": alpha_lag,
                    },
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "interferer-offset sweep",
                        "x": offset_sweep,
                        "y": offset_error,
                    },
                ],
                "layout": _layout(
                    "Two one-variable noise sweeps",
                    "Memory coefficient or offset (Hz)",
                    "Correlation or tone error",
                ),
            },
        },
        "explanations": {
            "observation": "Mean-centering and RMS normalization isolate structure: color raises lag correlation and low-frequency power, impulses raise crest factor, and a nearby narrowband interferer biases tone estimation.",
            "broken": "Broken mode compares raw records with unequal RMS, so apparent differences mix noise shape with simple power differences.",
            "recovery": "Mean-center each record and scale it to the same RMS before comparing. The recovery residual reports the normalization error.",
        },
        "diagnostics": {
            "seed": SEED,
            "sample_count": 4096,
            "broken_active": broken,
            "recovery_rms_residual_v": case["recovery_residual"],
            "family_metrics": metrics,
            "tone_errors_v": case["tone_errors"],
            "signature": [
                alpha,
                offset,
                target_rms,
                metrics["white"]["rms"],
                metrics["colored"]["lag_one"],
                metrics["impulsive"]["crest"],
                case["tone_errors"]["narrowband"],
                case["recovery_residual"],
            ],
        },
    }
