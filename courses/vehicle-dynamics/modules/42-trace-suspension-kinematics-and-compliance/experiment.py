from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 42
DEFAULTS = {"bump_travel_mm": 25.0, "lateral_force_n": 3000.0}
RANGES = {"bump_travel_mm": (-40.0, 60.0), "lateral_force_n": (-5000.0, 5000.0)}
BROKEN_TEXT = "Broken mode converts millimetres to metres and then applies gradients declared per millimetre, hiding almost all bump camber and toe change."
RECOVERY_TEXT = "Apply kinematic gradients in degrees per millimetre, compliance gradients in degrees per newton, and motion ratio on the same declared travel coordinate."


def _parameters(supplied: dict[str, Any]) -> dict[str, float]:
    result: dict[str, float] = {}
    for key, default in DEFAULTS.items():
        value = float(supplied.get(key, default))
        minimum, maximum = RANGES[key]
        if not np.isfinite(value) or value < minimum or value > maximum:
            raise ValueError(f"{key} outside declared finite range [{minimum}, {maximum}]")
        result[key] = value
    return result


def _trace(
    name: str,
    x: Any,
    y: Any,
    x_quantity: str,
    x_unit: str,
    y_quantity: str,
    y_unit: str,
    *,
    mode: str = "lines",
) -> dict[str, Any]:
    return {
        "type": "scattergl",
        "mode": mode,
        "name": name,
        "x": np.asarray(x, dtype=float),
        "y": np.asarray(y, dtype=float),
        "meta": {
            "x_quantity": x_quantity,
            "x_unit": x_unit,
            "y_quantity": y_quantity,
            "y_unit": y_unit,
        },
    }


def _plot(
    title: str,
    x_title: str,
    y_title: str,
    traces: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "data": traces,
        "layout": {
            "title": {"text": title, "x": 0.02},
            "xaxis": {"title": {"text": x_title}},
            "yaxis": {"title": {"text": y_title}},
            "legend": {"orientation": "h"},
            "margin": {"l": 72, "r": 36, "t": 62, "b": 62},
            "hovermode": "closest",
            "uirevision": "keep-view",
        },
        "config": {"responsive": True, "displaylogo": False},
    }


def _result(model: dict[str, Any], broken: bool) -> dict[str, Any]:
    return {
        "metrics": [
            {
                "id": key,
                "label": label,
                "value": float(value),
                "unit": unit,
                "emphasis": "primary" if index == 0 else "normal",
            }
            for index, (key, label, value, unit) in enumerate(model["metrics"])
        ],
        "plots": model["plots"],
        "explanations": {
            "observation": model["observation"],
            "broken": BROKEN_TEXT,
            "recovery": RECOVERY_TEXT,
        },
        "diagnostics": {
            "item_number": ITEM_NUMBER,
            "broken_active": bool(broken),
            "signature": [float(value) for value in model["signature"]],
        },
    }


def _state(travel_mm: np.ndarray | float, force: float, broken: bool) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    travel = np.asarray(travel_mm, dtype=float)
    used_travel = travel / 1000.0 if broken else travel
    camber = -1.0 - 0.035 * used_travel - 0.00004 * force
    toe = 0.10 + 0.004 * used_travel + 0.00006 * force
    motion_ratio = 0.85 + 0.0004 * used_travel
    wheel_rate = 45000.0 * motion_ratio**2
    return camber, toe, motion_ratio, wheel_rate


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    travel, force = p["bump_travel_mm"], p["lateral_force_n"]
    camber, toe, ratio, wheel_rate = _state(travel, force, broken)
    correct = _state(travel, force, False)
    unit_residual = float(np.hypot(float(camber - correct[0]), float(toe - correct[1])))
    signature = [
        float(camber),
        float(toe),
        float(ratio),
        float(wheel_rate),
        unit_residual,
    ]
    travel_sweep = np.linspace(-40.0, 60.0, 101)
    camber_sweep, toe_sweep, _, _ = _state(travel_sweep, force, broken)
    force_sweep = np.linspace(-5000.0, 5000.0, 101)
    camber_force, toe_force, _, _ = _state(travel, force_sweep, broken)
    return {
        "signature": signature,
        "metrics": [
            ("camber", "Wheel camber", signature[0], "deg"),
            ("toe", "Wheel toe", signature[1], "deg"),
            ("motion_ratio", "Motion ratio", signature[2], "1"),
            ("wheel_rate", "Wheel rate", signature[3], "N/m"),
        ],
        "plots": {
            "response": _plot(
                "Bump kinematics",
                "Wheel travel (mm)",
                "Alignment angle (deg)",
                [
                    _trace("Camber", travel_sweep, camber_sweep, "Wheel travel", "mm", "Alignment angle", "deg"),
                    _trace("Toe", travel_sweep, toe_sweep, "Wheel travel", "mm", "Alignment angle", "deg"),
                ],
            ),
            "mechanism": _plot(
                "Lateral-force compliance",
                "Lateral tire force (N)",
                "Alignment angle (deg)",
                [
                    _trace("Camber", force_sweep, camber_force, "Lateral tire force", "N", "Alignment angle", "deg"),
                    _trace("Toe", force_sweep, toe_force, "Lateral tire force", "N", "Alignment angle", "deg"),
                ],
            ),
        },
        "observation": "Bump geometry and force compliance superpose only after their millimetre, degree, and newton conventions are made explicit.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
