from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 48
DEFAULTS = {"deceleration_g": 0.9, "front_brake_bias": 0.62}
RANGES = {"deceleration_g": (0.3, 1.2), "front_brake_bias": (0.45, 0.85)}
BROKEN_TEXT = "Broken mode sizes axle capacity from static load, allowing rear brake force beyond the dynamically unloaded rear axle."
RECOVERY_TEXT = "Use deceleration-dependent axle loads, cap each axle force, and recompute achieved deceleration and utilization."


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


def _plot(title: str, x_title: str, y_title: str, traces: list[dict[str, Any]]) -> dict[str, Any]:
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


def _allocation(deceleration_g: float, front_bias: float, broken: bool) -> list[float]:
    mass, gravity, a, b, height = 1450.0, 9.81, 1.20, 1.50, 0.52
    wheelbase, friction = a + b, 1.10
    transfer = mass * deceleration_g * gravity * height / wheelbase
    front_dynamic = mass * gravity * b / wheelbase + transfer
    rear_dynamic = mass * gravity * a / wheelbase - transfer
    front_used = mass * gravity * b / wheelbase if broken else front_dynamic
    rear_used = mass * gravity * a / wheelbase if broken else rear_dynamic
    requested = mass * deceleration_g * gravity
    front_force = min(front_bias * requested, friction * front_used)
    rear_force = min((1.0 - front_bias) * requested, friction * rear_used)
    front_util = front_force / (friction * front_dynamic)
    rear_util = rear_force / (friction * rear_dynamic)
    achieved = (front_force + rear_force) / (mass * gravity)
    residual = max(0.0, front_util - 1.0, rear_util - 1.0) * mass * gravity
    ideal_bias = front_dynamic / (mass * gravity)
    return [front_dynamic, ideal_bias, front_util, rear_util, achieved, residual]


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    decel, bias = p["deceleration_g"], p["front_brake_bias"]
    signature = _allocation(decel, bias, broken)
    biases = np.linspace(0.45, 0.85, 81)
    achieved = []
    front_utilization = []
    rear_utilization = []
    for value in biases:
        sample = _allocation(decel, float(value), broken)
        front_utilization.append(sample[2])
        rear_utilization.append(sample[3])
        achieved.append(sample[4])
    return {
        "signature": signature,
        "metrics": [
            ("front_load", "Dynamic front axle load", signature[0], "N"),
            ("ideal_bias", "Dynamic ideal front bias", signature[1], "1"),
            ("achieved_deceleration", "Achieved deceleration", signature[4], "g"),
            ("capacity_residual", "Axle-capacity residual", signature[5], "N"),
        ],
        "plots": {
            "response": _plot(
                "Brake-bias deceleration",
                "Front brake bias (1)",
                "Achieved deceleration (g)",
                [_trace("Achieved deceleration", biases, achieved, "Front brake bias", "1", "Achieved deceleration", "g")],
            ),
            "mechanism": _plot(
                "Axle brake utilization",
                "Front brake bias (1)",
                "Axle utilization (1)",
                [
                    _trace("Front axle", biases, front_utilization, "Front brake bias", "1", "Axle utilization", "1"),
                    _trace("Rear axle", biases, rear_utilization, "Front brake bias", "1", "Axle utilization", "1"),
                ],
            ),
        },
        "observation": "Brake bias is a dynamic load-allocation problem: rear capacity falls under deceleration even though the static axle weights have not changed.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
