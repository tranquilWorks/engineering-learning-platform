from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 36
DEFAULTS = {"front_cornering_n_rad": 65000.0, "rear_cornering_n_rad": 80000.0}
RANGES = {"front_cornering_n_rad": (40000.0, 100000.0), "rear_cornering_n_rad": (40000.0, 100000.0)}
BROKEN_TEXT = "Broken mode treats axle stiffness stated per radian as though it were per degree, corrupting the understeer gradient and characteristic-speed domain."
RECOVERY_TEXT = "Use newtons per radian consistently with axle weights, then classify the gradient before computing characteristic speed."


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


def _gradient(front: float, rear: float, broken: bool) -> tuple[float, float]:
    mass, gravity, a, b = 1450.0, 9.81, 1.20, 1.50
    wheelbase = a + b
    front_weight = mass * gravity * b / wheelbase
    rear_weight = mass * gravity * a / wheelbase
    scale = np.pi / 180.0 if broken else 1.0
    gradient = front_weight / (front * scale) - rear_weight / (rear * scale)
    correct = front_weight / front - rear_weight / rear
    return gradient, correct


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    front, rear = p["front_cornering_n_rad"], p["rear_cornering_n_rad"]
    gradient, correct = _gradient(front, rear, broken)
    gravity, wheelbase, radius = 9.81, 2.70, 80.0
    characteristic = np.sqrt(gravity * wheelbase / gradient) if gradient > 1.0e-12 else 0.0
    lateral_accel = 0.70 * gravity
    steer = wheelbase / radius + gradient * lateral_accel / gravity
    residual = abs((steer - wheelbase / radius) - correct * lateral_accel / gravity)
    classification = 1.0 if gradient > 1.0e-8 else (-1.0 if gradient < -1.0e-8 else 0.0)
    signature = [
        float(np.rad2deg(gradient)),
        float(characteristic),
        float(np.rad2deg(steer)),
        classification,
        float(np.rad2deg(residual)),
    ]
    accel_g = np.linspace(0.0, 1.2, 61)
    steer_deg = np.rad2deg(wheelbase / radius + gradient * accel_g)
    neutral_deg = np.full_like(accel_g, np.rad2deg(wheelbase / radius))
    return {
        "signature": signature,
        "metrics": [
            ("gradient", "Understeer gradient", signature[0], "deg/g"),
            ("characteristic_speed", "Characteristic speed", signature[1], "m/s"),
            ("steer", "Steer at 0.7 g", signature[2], "deg"),
            ("relation_residual", "Steer-law residual", signature[4], "deg"),
        ],
        "plots": {
            "response": _plot(
                "Steer demand versus lateral acceleration",
                "Lateral acceleration (g)",
                "Road-wheel steer (deg)",
                [
                    _trace("Computed steer", accel_g, steer_deg, "Lateral acceleration", "g", "Road-wheel steer", "deg"),
                    _trace("Neutral steer", accel_g, neutral_deg, "Lateral acceleration", "g", "Road-wheel steer", "deg"),
                ],
            ),
            "mechanism": _plot(
                "Characteristic-speed domain",
                "Understeer gradient (deg/g)",
                "Characteristic speed (m/s)",
                [
                    _trace("Current setup", [signature[0]], [signature[1]], "Understeer gradient", "deg/g", "Characteristic speed", "m/s", mode="markers"),
                ],
            ),
        },
        "observation": "Characteristic speed exists for positive understeer gradient; neutral and oversteer cases require different interpretations.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
