from __future__ import annotations

from typing import Any

import numpy as np


def _layout(title: str, x: str, y: str) -> dict[str, Any]:
    return {"title": {"text": title, "x": 0.02}, "xaxis": {"title": x}, "yaxis": {"title": y}, "legend": {"orientation": "h"}, "margin": {"l": 65, "r": 20, "t": 55, "b": 55}, "hovermode": "closest", "uirevision": "keep-view"}


def _trace(name: str, x: Any, y: Any, dash: str | None = None) -> dict[str, Any]:
    trace: dict[str, Any] = {"type": "scatter", "mode": "lines", "name": name, "x": x, "y": y}
    if dash:
        trace["line"] = {"dash": dash}
    return trace


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    lines = round(float(parameters["counts_per_rev"]))
    speed_rpm = float(parameters["speed_rpm"])
    sample_rate = float(parameters["sample_rate_hz"])
    duration = float(parameters["duration_s"])
    broken = bool(parameters["broken_mode"])
    samples = min(round(duration * sample_rate) + 1, 1001)
    t = np.linspace(0.0, duration, samples)
    true_speed = speed_rpm * 2.0 * np.pi / 60.0
    true_angle = true_speed * t
    edges_per_rev = 4 * lines
    counts = np.rint(true_angle * edges_per_rev / (2.0 * np.pi)).astype(int)
    decode_edges = lines if broken else edges_per_rev
    estimated_angle = counts * 2.0 * np.pi / decode_edges
    estimated_speed = np.empty_like(estimated_angle)
    estimated_speed[0] = 0.0
    estimated_speed[1:] = np.diff(estimated_angle) / np.diff(t)
    angle_error = estimated_angle - true_angle
    rms_error = float(np.sqrt(np.mean(angle_error**2)))
    quantization_bound = np.pi / edges_per_rev
    mean_speed = float(np.mean(estimated_speed[1:])) if len(t) > 1 else 0.0
    signature = [float(counts[-1]), estimated_angle[-1], rms_error, mean_speed, quantization_bound]
    return {
        "metrics": [
            {"id": "final_count", "label": "Final count", "value": int(counts[-1]), "unit": "count", "emphasis": "primary"},
            {"id": "angle_rms_error", "label": "Angle RMS error", "value": rms_error, "unit": "rad"},
            {"id": "mean_speed", "label": "Mean estimated speed", "value": mean_speed, "unit": "rad/s"},
            {"id": "quantization_bound", "label": "Half-count bound", "value": quantization_bound, "unit": "rad"},
        ],
        "plots": {
            "response": {
                "data": [_trace("True angle", t, true_angle), _trace("Encoder angle", t, estimated_angle, "dash")],
                "layout": _layout("Quantized shaft angle", "Time (s)", "Angle (rad)"),
                "config": {"responsive": True, "displaylogo": False},
            },
            "mechanism": {
                "data": [_trace("Estimated speed", t, estimated_speed), _trace("True speed", t, np.full_like(t, true_speed), "dash")],
                "layout": _layout("Count-difference velocity", "Time (s)", "Angular speed (rad/s)"),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "Integer quadrature counts bound angle resolution and make finite-difference speed step between discrete levels.",
            "broken": "Broken mode decodes x4 edge counts as if they were line counts, creating a fourfold scale error.",
            "recovery": "Decode with four edges per line and retain sample time in the velocity difference.",
        },
        "diagnostics": {"item_id": "P09", "reference_basis": "integer quantization equation", "broken_active": broken, "sample_count": len(t), "signature": [float(v) for v in signature]},
    }
