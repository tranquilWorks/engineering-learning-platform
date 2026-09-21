from __future__ import annotations

from typing import Any

import numpy as np


def _layout(title: str, x: str, y: str) -> dict[str, Any]:
    return {
        "title": {"text": title, "x": 0.02},
        "xaxis": {"title": x},
        "yaxis": {"title": y},
        "legend": {"orientation": "h"},
        "margin": {"l": 65, "r": 20, "t": 55, "b": 55},
        "hovermode": "closest",
        "uirevision": "keep-view",
    }


def _trace(name: str, x: Any, y: Any, mode: str = "lines") -> dict[str, Any]:
    return {"type": "scatter", "mode": mode, "name": name, "x": x, "y": y}


def _standard_pattern(count: int) -> np.ndarray:
    values = np.linspace(-1.0, 1.0, count)
    values -= np.mean(values)
    return values / np.sqrt(np.mean(values**2))


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    wall = float(parameters["wall_distance_m"])
    angle_deg = float(parameters["beam_angle_deg"])
    noise_std = float(parameters["noise_std_m"])
    maximum = float(parameters["max_range_m"])
    broken = bool(parameters["broken_mode"])
    angle = np.radians(angle_deg)
    true_range = wall / np.cos(angle)
    model_range = wall if broken else true_range
    noise = noise_std * _standard_pattern(101)
    raw = true_range + noise
    measured = np.clip(raw, 0.0, maximum)
    residual = measured - model_range
    angles = np.linspace(-60.0, 60.0, 121)
    geometric = wall / np.cos(np.radians(angles))
    modeled = np.full_like(angles, wall) if broken else geometric
    signature = [
        true_range,
        model_range,
        np.mean(measured),
        np.mean(residual),
        np.sqrt(np.mean(residual**2)),
        np.mean(raw >= maximum),
    ]
    return {
        "metrics": [
            {
                "id": "true_slant_range",
                "label": "True slant range",
                "value": true_range,
                "unit": "m",
                "emphasis": "primary",
            },
            {
                "id": "model_range",
                "label": "Model prediction",
                "value": model_range,
                "unit": "m",
            },
            {
                "id": "residual_bias",
                "label": "Mean residual",
                "value": np.mean(residual),
                "unit": "m",
            },
            {
                "id": "residual_rms",
                "label": "Residual RMS",
                "value": np.sqrt(np.mean(residual**2)),
                "unit": "m",
            },
        ],
        "plots": {
            "response": {
                "data": [
                    _trace("Measured range", np.arange(len(measured)), measured),
                    _trace(
                        "Model prediction",
                        [0, len(measured) - 1],
                        [model_range, model_range],
                    ),
                ],
                "layout": _layout(
                    "Deterministic range samples", "Sample index (-)", "Range (m)"
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "mechanism": {
                "data": [
                    _trace("Ray-plane geometry", angles, geometric),
                    _trace("Active model", angles, modeled),
                    _trace("Maximum range", [-60, 60], [maximum, maximum]),
                ],
                "layout": _layout(
                    "Angle-dependent wall intersection",
                    "Beam angle (deg)",
                    "Predicted range (m)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "The ray travels farther than the perpendicular wall distance by the secant of the beam angle; bounded noise spreads samples around that geometric range.",
            "broken": "Broken mode substitutes perpendicular distance for slant range, so an angle-dependent model error appears as a biased residual.",
            "recovery": "Intersect the ray with the wall using d/cos(theta), then apply noise and saturation as separate sensor effects.",
        },
        "diagnostics": {
            "item_id": "P11",
            "reference_basis": "closed-form ray-plane intersection with a normalized deterministic noise sequence",
            "broken_active": broken,
            "sample_count": len(measured),
            "signature": [float(value) for value in signature],
        },
    }
