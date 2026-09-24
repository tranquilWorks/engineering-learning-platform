from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 46
DEFAULTS = {"left_friction_mu": 0.35, "torque_bias_ratio": 4.0}
RANGES = {"left_friction_mu": (0.2, 1.2), "torque_bias_ratio": (1.0, 5.0)}
BROKEN_TEXT = "Broken mode applies the torque-bias ratio without enforcing the high-grip wheel capacity or total input demand."
RECOVERY_TEXT = "Bound each wheel by its contact capacity, the differential bias ratio, and the available driveshaft demand."


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


def _delivery(left_mu: float, bias: float, broken: bool) -> list[float]:
    wheel_load, right_mu, demand = 3200.0, 1.15, 9000.0
    left_capacity = left_mu * wheel_load
    right_capacity = right_mu * wheel_load
    open_each = min(demand / 2.0, left_capacity, right_capacity)
    open_total = 2.0 * open_each
    left_force = min(left_capacity, demand / (1.0 + bias))
    if demand > (1.0 + bias) * left_force:
        left_force = left_capacity
    right_force = bias * left_force
    if not broken:
        right_force = min(right_force, right_capacity, demand - left_force)
    lsd_total = left_force + right_force
    residual = max(
        0.0,
        left_force - left_capacity,
        right_force - right_capacity,
        lsd_total - demand,
    )
    return [open_total, lsd_total, left_force, right_force, residual]


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    left_mu, bias = p["left_friction_mu"], p["torque_bias_ratio"]
    signature = _delivery(left_mu, bias, broken)
    mu_sweep = np.linspace(0.20, 1.20, 101)
    open_force = []
    lsd_force = []
    for value in mu_sweep:
        sample = _delivery(float(value), bias, broken)
        open_force.append(sample[0])
        lsd_force.append(sample[1])
    capacities = [left_mu * 3200.0, 1.15 * 3200.0]
    wheel_forces = [signature[2], signature[3]]
    return {
        "signature": signature,
        "metrics": [
            ("open_force", "Open-differential force", signature[0], "N"),
            ("lsd_force", "Limited-slip force", signature[1], "N"),
            ("left_force", "Low-grip wheel force", signature[2], "N"),
            ("capacity_residual", "Wheel-capacity residual", signature[4], "N"),
        ],
        "plots": {
            "response": _plot(
                "Split-friction differential delivery",
                "Left-wheel friction coefficient (1)",
                "Axle traction force (N)",
                [
                    _trace("Open differential", mu_sweep, open_force, "Left-wheel friction coefficient", "1", "Axle traction force", "N"),
                    _trace("Limited slip", mu_sweep, lsd_force, "Left-wheel friction coefficient", "1", "Axle traction force", "N"),
                ],
            ),
            "mechanism": _plot(
                "Wheel force and capacity",
                "Wheel index (1)",
                "Longitudinal force (N)",
                [
                    _trace("Delivered", [1, 2], wheel_forces, "Wheel index", "1", "Longitudinal force", "N", mode="markers"),
                    _trace("Capacity", [1, 2], capacities, "Wheel index", "1", "Longitudinal force", "N", mode="markers"),
                ],
            ),
        },
        "observation": "An LSD can use more of the high-grip wheel, but neither wheel capacity nor driveshaft demand disappears when torque bias is applied.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
