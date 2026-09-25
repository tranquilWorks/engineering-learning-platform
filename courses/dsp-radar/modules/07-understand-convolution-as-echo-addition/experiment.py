from __future__ import annotations

from typing import Any

import numpy as np

SEED = 707
MAX_SAMPLES = 1024


def _layout(title: str, x_label: str, y_label: str) -> dict[str, Any]:
    return {
        "title": {"text": title, "x": 0.02},
        "xaxis": {"title": x_label},
        "yaxis": {"title": y_label},
        "legend": {"orientation": "h", "y": 1.14},
        "margin": {"l": 68, "r": 22, "t": 58, "b": 58},
    }


def _case(middle_delay: int, third_gain: float, broken: bool) -> dict[str, Any]:
    if middle_delay < 1 or middle_delay > 8 or not -1.0 <= third_gain <= 1.0:
        raise ValueError("echo controls exceed the bounded range")
    count = 40
    if count > MAX_SAMPLES:
        raise ValueError("record exceeds the resource ceiling")
    pulse = np.zeros(count)
    pulse[5:12] = np.array([0.2, 0.7, 1.0, 0.8, 0.45, 0.15, -0.1])
    delays = np.array([0, middle_delay, 9])
    gains = np.array([1.0, 0.6, third_gain])
    output_count = count + int(np.max(delays))
    contributions = []
    for delay, gain in zip(delays, gains, strict=True):
        path = np.zeros(output_count)
        path[int(delay) : int(delay) + count] = gain * pulse
        contributions.append(path)
    explicit = np.sum(contributions, axis=0)
    impulse = np.zeros(int(np.max(delays)) + 1)
    for delay, gain in zip(delays, gains, strict=True):
        impulse[int(delay)] += gain
    convolved = np.convolve(pulse, impulse)
    manual = np.zeros_like(explicit)
    for sample_index, sample in enumerate(pulse):
        for delay, gain in zip(delays, gains, strict=True):
            manual[sample_index + int(delay)] += sample * gain
    overwritten = np.zeros_like(explicit)
    for path in contributions:
        nonzero = path != 0.0
        overwritten[nonzero] = path[nonzero]
    displayed = overwritten if broken else explicit
    display_error = float(np.max(np.abs(displayed - explicit)))
    return {
        "pulse": pulse,
        "delays": delays,
        "gains": gains,
        "contributions": contributions,
        "explicit": explicit,
        "manual": manual,
        "convolved": convolved,
        "displayed": displayed,
        "convolution_error": float(np.max(np.abs(explicit - convolved))),
        "manual_error": float(np.max(np.abs(explicit - manual))),
        "overwrite_error": float(np.max(np.abs(explicit - overwritten))),
        "display_error": display_error,
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    middle_delay = int(parameters["middle_echo_delay_samples"])
    third_gain = float(parameters["third_echo_gain"])
    broken = bool(parameters["broken_mode"])
    case = _case(middle_delay, third_gain, broken)
    delay_sweep = np.array([3, 5, 7])
    overlap_peak = [
        float(np.max(np.abs(_case(int(value), -0.35, False)["explicit"])))
        for value in delay_sweep
    ]
    gain_sweep = np.array([-0.7, -0.35, 0.35])
    tail_value = [
        float(_case(5, float(value), False)["explicit"][18]) for value in gain_sweep
    ]
    output_index = np.arange(len(case["explicit"]))
    return {
        "metrics": [
            {
                "id": "convolution_error",
                "label": "Explicit/NumPy error",
                "value": case["convolution_error"],
                "unit": "a.u.",
            },
            {
                "id": "manual_error",
                "label": "Manual/explicit error",
                "value": case["manual_error"],
                "unit": "a.u.",
            },
            {
                "id": "overwrite_error",
                "label": "Overwrite failure",
                "value": case["overwrite_error"],
                "unit": "a.u.",
                "emphasis": "primary",
            },
        ],
        "plots": {
            "echo_paths": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": f"gain {gain:+.2f}, delay {delay}",
                        "x": output_index,
                        "y": path,
                    }
                    for path, delay, gain in zip(
                        case["contributions"],
                        case["delays"],
                        case["gains"],
                        strict=True,
                    )
                ],
                "layout": _layout(
                    "Convolution is shifted signed echo addition",
                    "Sample index",
                    "Path contribution (a.u.)",
                ),
            },
            "sum_check": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "explicit sum",
                        "x": output_index,
                        "y": case["explicit"],
                    },
                    {
                        "type": "scatter",
                        "mode": "markers",
                        "name": "NumPy convolution",
                        "x": output_index,
                        "y": case["convolved"],
                    },
                ],
                "layout": _layout(
                    "Three formulations agree",
                    "Sample index",
                    "Output amplitude (a.u.)",
                ),
            },
            "parameter_sweeps": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "middle-delay sweep",
                        "x": delay_sweep,
                        "y": overlap_peak,
                    },
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "signed-gain sweep",
                        "x": gain_sweep,
                        "y": tail_value,
                    },
                ],
                "layout": _layout(
                    "Two echo sweeps",
                    "Delay (samples) or signed gain",
                    "Overlap peak or tail amplitude",
                ),
            },
            "broken_case": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "add overlapping paths",
                        "x": output_index,
                        "y": case["explicit"],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "displayed output",
                        "x": output_index,
                        "y": case["displayed"],
                    },
                ],
                "layout": _layout(
                    "Overlap must add, not overwrite",
                    "Sample index",
                    "Output amplitude (a.u.)",
                ),
            },
        },
        "explanations": {
            "observation": "Each nonzero impulse-response tap creates a shifted, scaled, signed copy of the input. Adding those copies is convolution.",
            "broken": "Broken mode overwrites earlier path values wherever echoes overlap, discarding superposition.",
            "recovery": "Accumulate every path with +=. The manual nested sum, explicit path sum, and NumPy convolution then agree exactly.",
        },
        "diagnostics": {
            "seed": SEED,
            "broken_active": broken,
            "delays_samples": case["delays"],
            "gains": case["gains"],
            "convolution_error": case["convolution_error"],
            "manual_error": case["manual_error"],
            "overwrite_error": case["overwrite_error"],
            "signature": [
                middle_delay,
                third_gain,
                case["convolution_error"],
                case["manual_error"],
                case["overwrite_error"],
                case["display_error"],
            ],
        },
    }
