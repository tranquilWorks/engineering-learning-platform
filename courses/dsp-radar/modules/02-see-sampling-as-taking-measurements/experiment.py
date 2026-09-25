from __future__ import annotations

from typing import Any

import numpy as np

MAX_SAMPLES = 5000


def _layout(title: str, x_label: str, y_label: str) -> dict[str, Any]:
    return {
        "title": {"text": title, "x": 0.02, "xanchor": "left"},
        "xaxis": {"title": x_label, "showgrid": True},
        "yaxis": {"title": y_label, "showgrid": True},
        "legend": {"orientation": "h", "y": 1.14},
        "margin": {"l": 68, "r": 22, "t": 58, "b": 58},
        "uirevision": "keep-view",
    }


def _case(
    sample_rate_hz: float, clock_offset_samples: float, broken: bool
) -> dict[str, Any]:
    if not 8.0 <= sample_rate_hz <= 200.0:
        raise ValueError("sample_rate_hz must be between 8 and 200 Sa/s")
    if not 0.0 <= clock_offset_samples <= 0.95:
        raise ValueError("clock_offset_samples must be between 0 and 0.95 sample")
    frequency_hz = 7.0
    sample_rate_hz = 12.0 if broken else sample_rate_hz
    amplitude = 1.0
    phase_rad = np.pi / 5.0
    duration_s = 1.0
    count = round(sample_rate_hz * duration_s)
    if count < 2 or count > MAX_SAMPLES:
        raise ValueError("sample record is outside the bounded resource limit")
    dense_time = np.linspace(0.0, duration_s, 2000, endpoint=False)
    sample_time = (
        np.arange(count, dtype=float) + clock_offset_samples
    ) / sample_rate_hz
    dense = amplitude * np.cos(2.0 * np.pi * frequency_hz * dense_time + phase_rad)
    samples = amplitude * np.cos(2.0 * np.pi * frequency_hz * sample_time + phase_rad)
    interpolated = np.interp(
        dense_time, sample_time, samples, left=samples[0], right=samples[-1]
    )
    rmse = float(np.sqrt(np.mean((interpolated - dense) ** 2)))

    reflected_hz = abs(frequency_hz - sample_rate_hz)
    reflected_phase = -phase_rad + 2.0 * np.pi * clock_offset_samples
    reflected = amplitude * np.cos(
        2.0 * np.pi * reflected_hz * sample_time + reflected_phase
    )
    high_hz = frequency_hz + sample_rate_hz
    high_phase = phase_rad - 2.0 * np.pi * clock_offset_samples
    high = amplitude * np.cos(2.0 * np.pi * high_hz * sample_time + high_phase)
    return {
        "sample_rate_hz": sample_rate_hz,
        "clock_offset_samples": clock_offset_samples,
        "frequency_hz": frequency_hz,
        "dense_time": dense_time,
        "dense": dense,
        "sample_time": sample_time,
        "samples": samples,
        "interpolated": interpolated,
        "rmse": rmse,
        "reflected_hz": reflected_hz,
        "reflected": reflected,
        "high_hz": high_hz,
        "high": high,
        "reflected_error": float(np.max(np.abs(samples - reflected))),
        "high_error": float(np.max(np.abs(samples - high))),
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    case = _case(
        float(parameters["sample_rate_hz"]),
        float(parameters["clock_offset_samples"]),
        bool(parameters["broken_mode"]),
    )
    fs_sweep = np.array([80.0, 16.0, 12.0])
    fs_errors = [_case(value, 0.0, False)["rmse"] for value in fs_sweep]
    offset_sweep = np.array([0.0, 0.25, 0.5])
    offset_errors = [_case(80.0, value, False)["rmse"] for value in offset_sweep]
    sample_time = case["sample_time"]
    samples = case["samples"]
    broken = bool(parameters["broken_mode"])
    return {
        "metrics": [
            {
                "id": "sample_rate",
                "label": "Measurement rate",
                "value": case["sample_rate_hz"],
                "unit": "Sa/s",
                "emphasis": "primary",
            },
            {
                "id": "samples_per_cycle",
                "label": "Samples per cycle",
                "value": case["sample_rate_hz"] / case["frequency_hz"],
                "unit": "samples/cycle",
            },
            {
                "id": "interpolation_rmse",
                "label": "Linear interpolation RMSE",
                "value": case["rmse"],
                "unit": "a.u.",
            },
            {
                "id": "alias_error",
                "label": "Alias-family agreement",
                "value": case["reflected_error"],
                "unit": "a.u.",
            },
        ],
        "plots": {
            "measurements": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "dense reference",
                        "x": case["dense_time"],
                        "y": case["dense"],
                    },
                    {
                        "type": "scatter",
                        "mode": "markers",
                        "name": "measurements",
                        "x": sample_time,
                        "y": samples,
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "linear interpolation",
                        "x": case["dense_time"],
                        "y": case["interpolated"],
                        "line": {"dash": "dash"},
                    },
                ],
                "layout": _layout(
                    "A sampler records measurements, not the path between them",
                    "Time (s)",
                    "Amplitude (a.u.)",
                ),
            },
            "parameter_sweeps": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "sample-rate sweep",
                        "x": fs_sweep,
                        "y": fs_errors,
                    },
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "clock-offset sweep",
                        "x": offset_sweep,
                        "y": offset_errors,
                        "xaxis": "x2",
                        "yaxis": "y2",
                    },
                ],
                "layout": _layout(
                    "One-variable sampling sweeps",
                    "Sample rate (Sa/s); offset trace uses samples",
                    "Interpolation RMSE (a.u.)",
                ),
            },
            "alias_family": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "markers",
                        "name": "7 Hz samples",
                        "x": sample_time,
                        "y": samples,
                    },
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": f"reflected {case['reflected_hz']:.1f} Hz",
                        "x": sample_time,
                        "y": case["reflected"],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": f"high {case['high_hz']:.1f} Hz",
                        "x": sample_time,
                        "y": case["high"],
                    },
                ],
                "layout": _layout(
                    "Exact sampled alias family",
                    "Time (s)",
                    "Measured amplitude (a.u.)",
                ),
            },
        },
        "explanations": {
            "observation": "The dense sinusoid is a reference; only the marked values are measurements. Linear interpolation invents a path and its error rises as the grid thins or shifts.",
            "broken": "Broken mode forces 7 Hz below a 12 Sa/s clock. The 5 Hz reflected member and 19 Hz high member reproduce every sample exactly.",
            "recovery": "Restore 80 Sa/s. The alias-family algebra still exists, but the declared bandlimit below Nyquist selects the 7 Hz interpretation.",
        },
        "diagnostics": {
            "sample_count": len(samples),
            "broken_active": broken,
            "alias_family_hz": [
                case["reflected_hz"],
                case["frequency_hz"],
                case["high_hz"],
            ],
            "reflected_alias_error": case["reflected_error"],
            "high_alias_error": case["high_error"],
            "signature": [
                case["sample_rate_hz"],
                case["clock_offset_samples"],
                len(samples),
                case["rmse"],
                case["reflected_error"],
                case["high_error"],
            ],
        },
    }
