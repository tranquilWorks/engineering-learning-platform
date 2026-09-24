from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 37
DEFAULTS = {"steer_deg": 6.0, "friction_mu": 1.15}
RANGES = {"steer_deg": (1.0, 10.0), "friction_mu": (0.7, 1.5)}
BROKEN_TEXT = "Broken mode extends axle cornering stiffness linearly beyond the declared friction capacity, producing utilization above one."
RECOVERY_TEXT = "Restore bounded nonlinear axle forces, then recompute utilization, yaw moment, and the local restoring-moment slope."


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


def _forces(beta: float, steer: float, friction: float, broken: bool) -> tuple[float, float]:
    speed, a, b = 28.0, 1.20, 1.50
    mass, gravity = 1450.0, 9.81
    yaw_rate = speed * np.tan(steer) / (a + b)
    alpha_front = steer - beta - a * yaw_rate / speed
    alpha_rear = -beta + b * yaw_rate / speed
    front_linear, rear_linear = 70000.0 * alpha_front, 75000.0 * alpha_rear
    front_capacity = friction * mass * gravity * b / (a + b)
    rear_capacity = friction * mass * gravity * a / (a + b)
    if broken:
        return front_linear, rear_linear
    return (
        front_capacity * np.tanh(front_linear / front_capacity),
        rear_capacity * np.tanh(rear_linear / rear_capacity),
    )


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    steer = np.deg2rad(p["steer_deg"])
    friction = p["friction_mu"]
    mass, gravity, a, b = 1450.0, 9.81, 1.20, 1.50
    front_capacity = friction * mass * gravity * b / (a + b)
    rear_capacity = friction * mass * gravity * a / (a + b)
    beta = np.deg2rad(10.0)
    front, rear = _forces(beta, steer, friction, broken)
    front_util, rear_util = abs(front) / front_capacity, abs(rear) / rear_capacity
    yaw_moment = a * front - b * rear
    epsilon = 1.0e-5
    plus = _forces(beta + epsilon, steer, friction, broken)
    minus = _forces(beta - epsilon, steer, friction, broken)
    slope = (a * (plus[0] - minus[0]) - b * (plus[1] - minus[1])) / (2.0 * epsilon)
    stability_margin = -slope
    capacity_excess = max(0.0, front_util - 1.0, rear_util - 1.0)
    signature = [front_util, rear_util, abs(yaw_moment), stability_margin, capacity_excess]
    beta_sweep = np.deg2rad(np.linspace(-6.0, 6.0, 121))
    moments = []
    utilizations = []
    for value in beta_sweep:
        sample_front, sample_rear = _forces(value, steer, friction, broken)
        moments.append(a * sample_front - b * sample_rear)
        utilizations.append(max(abs(sample_front) / front_capacity, abs(sample_rear) / rear_capacity))
    return {
        "signature": signature,
        "metrics": [
            ("front_utilization", "Front utilization", front_util, "1"),
            ("rear_utilization", "Rear utilization", rear_util, "1"),
            ("yaw_moment", "Yaw-moment imbalance", abs(yaw_moment), "N*m"),
            ("stability_margin", "Restoring-moment slope", stability_margin, "N*m/rad"),
        ],
        "plots": {
            "response": _plot(
                "Nonlinear yaw moment",
                "Body sideslip (deg)",
                "Yaw moment (N*m)",
                [
                    _trace("Yaw moment", np.rad2deg(beta_sweep), moments, "Body sideslip", "deg", "Yaw moment", "N*m"),
                ],
            ),
            "mechanism": _plot(
                "Axle capacity utilization",
                "Body sideslip (deg)",
                "Maximum axle utilization (1)",
                [
                    _trace("Maximum utilization", np.rad2deg(beta_sweep), utilizations, "Body sideslip", "deg", "Maximum axle utilization", "1"),
                    _trace("Capacity boundary", np.rad2deg(beta_sweep), np.ones(beta_sweep.size), "Body sideslip", "deg", "Maximum axle utilization", "1"),
                ],
            ),
        },
        "observation": "A local restoring slope does not excuse a force demand above capacity; stability and saturation must be inspected together.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
