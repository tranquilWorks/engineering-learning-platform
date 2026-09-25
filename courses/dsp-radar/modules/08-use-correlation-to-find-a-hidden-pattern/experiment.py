from __future__ import annotations

from typing import Any

import numpy as np

SEED = 808
MAX_SAMPLES = 1024


def _layout(title: str, x_label: str, y_label: str) -> dict[str, Any]:
    return {
        "title": {"text": title, "x": 0.02},
        "xaxis": {"title": x_label},
        "yaxis": {"title": y_label},
        "legend": {"orientation": "h", "y": 1.14},
        "margin": {"l": 68, "r": 22, "t": 58, "b": 58},
    }


def _reference() -> np.ndarray:
    chips = np.array([1, 1, -1, 1, -1, -1, 1, -1, 1, 1, 1, -1, -1], dtype=float)
    return np.repeat(chips, 2)


def _case(
    amplitude: float, noise_sigma: float, separation: int, broken: bool
) -> dict[str, Any]:
    if (
        not 0.05 <= amplitude <= 2.0
        or not 0.0 <= noise_sigma <= 2.0
        or separation < 1
        or separation > 80
    ):
        raise ValueError("correlation controls exceed the bounded range")
    count = 256
    if count > MAX_SAMPLES:
        raise ValueError("record exceeds the resource ceiling")
    reference = _reference()
    hidden_delay = 137
    if hidden_delay + separation + len(reference) > count:
        raise ValueError("targets do not fit in the bounded record")
    rng = np.random.default_rng(SEED)
    record = noise_sigma * rng.standard_normal(count)
    record[hidden_delay : hidden_delay + len(reference)] += amplitude * reference
    record[hidden_delay + separation : hidden_delay + separation + len(reference)] += (
        0.55 * amplitude * reference
    )
    correlation = np.correlate(record, reference, mode="full")
    lags = np.arange(-(len(reference) - 1), count)
    convolution = np.convolve(record, reference[::-1], mode="full")
    peak_index = int(np.argmax(correlation))
    recovered_delay = int(lags[peak_index])
    displayed_delay = peak_index if broken else recovered_delay
    alternate_error = float(np.max(np.abs(correlation - convolution)))
    return {
        "record": record,
        "reference": reference,
        "correlation": correlation,
        "lags": lags,
        "peak_index": peak_index,
        "recovered_delay": recovered_delay,
        "displayed_delay": displayed_delay,
        "index_error": peak_index - recovered_delay,
        "alternate_error": alternate_error,
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    amplitude = float(parameters["target_amplitude"])
    noise_sigma = float(parameters["noise_sigma"])
    separation = int(parameters["target_separation_samples"])
    broken = bool(parameters["broken_mode"])
    case = _case(amplitude, noise_sigma, separation, broken)
    amplitude_sweep = np.array([0.3, 0.65, 1.0])
    amplitude_peak = [
        float(np.max(_case(float(value), 0.5, 50, False)["correlation"]))
        for value in amplitude_sweep
    ]
    noise_sweep = np.array([0.2, 0.5, 1.0])
    noise_margin = []
    for value in noise_sweep:
        result = _case(0.65, float(value), 50, False)["correlation"]
        largest = np.partition(result, -2)[-2:]
        noise_margin.append(float(largest[-1] - largest[-2]))
    separation_sweep = np.array([8, 18, 40])
    valley = []
    for value in separation_sweep:
        result = _case(0.65, 0.0, int(value), False)
        first = 137 + len(result["reference"]) - 1
        second = first + int(value)
        valley.append(float(np.min(result["correlation"][first : second + 1])))
    return {
        "metrics": [
            {
                "id": "recovered_delay",
                "label": "Lag-derived delay",
                "value": case["displayed_delay"],
                "unit": "samples",
                "emphasis": "primary",
            },
            {
                "id": "peak_index",
                "label": "Raw convolution index",
                "value": case["peak_index"],
                "unit": "index",
            },
            {
                "id": "index_offset",
                "label": "Index-to-lag offset",
                "value": case["index_error"],
                "unit": "samples",
            },
            {
                "id": "alternate_error",
                "label": "Correlation/convolution error",
                "value": case["alternate_error"],
                "unit": "a.u.",
            },
        ],
        "plots": {
            "hidden_record": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "noisy record",
                        "x": np.arange(len(case["record"])),
                        "y": case["record"],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "known reference",
                        "x": np.arange(len(case["reference"])),
                        "y": case["reference"],
                    },
                ],
                "layout": _layout(
                    "An asymmetric known pattern is hidden in noise",
                    "Sample index",
                    "Amplitude (a.u.)",
                ),
            },
            "correlation": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "cross-correlation",
                        "x": case["lags"],
                        "y": case["correlation"],
                    }
                ],
                "layout": _layout(
                    "Correlation uses an explicit lag axis",
                    "Lag (samples)",
                    "Correlation (a.u.)",
                ),
            },
            "parameter_sweeps": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "target-amplitude sweep",
                        "x": amplitude_sweep,
                        "y": amplitude_peak,
                    },
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "noise sweep",
                        "x": noise_sweep,
                        "y": noise_margin,
                    },
                ],
                "layout": _layout(
                    "Two detection sweeps",
                    "Amplitude or noise standard deviation",
                    "Peak or peak margin (a.u.)",
                ),
            },
            "separation_limit": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "between-target valley",
                        "x": separation_sweep,
                        "y": valley,
                    }
                ],
                "layout": _layout(
                    "Two-target separation",
                    "Target separation (samples)",
                    "Between-peak correlation (a.u.)",
                ),
            },
        },
        "explanations": {
            "observation": "Cross-correlation slides the known asymmetric chip sequence across the record. Its peak lag estimates insertion delay; reversed-reference convolution gives the same array.",
            "broken": "Broken mode reports the array index as delay and is wrong by reference_length−1 samples.",
            "recovery": "Map the peak index through the explicit lag vector. Closely spaced targets merge when their correlation main lobes overlap.",
        },
        "diagnostics": {
            "seed": SEED,
            "record_samples": 256,
            "reference_samples": len(case["reference"]),
            "broken_active": broken,
            "true_delay_samples": 137,
            "recovered_delay_samples": case["recovered_delay"],
            "reported_delay_samples": case["displayed_delay"],
            "index_offset_samples": case["index_error"],
            "alternate_error": case["alternate_error"],
            "signature": [
                amplitude,
                noise_sigma,
                separation,
                case["recovered_delay"],
                case["displayed_delay"],
                case["alternate_error"],
            ],
        },
    }
