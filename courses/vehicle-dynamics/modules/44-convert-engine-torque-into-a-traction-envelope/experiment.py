from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 44
DEFAULTS = {"engine_rpm": 5000.0, "gear_ratio": 3.2}
RANGES = {"engine_rpm": (2000.0, 7000.0), "gear_ratio": (1.0, 4.0)}
BROKEN_TEXT = "Broken mode delivers engine-limited wheel force without enforcing the driven-tire capacity boundary."
RECOVERY_TEXT = "Restore the minimum of engine-limited and tire-limited force, including final drive, efficiency, and tire radius."


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


def _torque(rpm: np.ndarray | float) -> np.ndarray:
    values = np.asarray(rpm, dtype=float)
    return 220.0 - 6.0e-6 * (values - 4500.0) ** 2


def _point(rpm: float, gear: float, broken: bool) -> list[float]:
    final_drive, efficiency, radius = 4.10, 0.92, 0.31
    torque = float(_torque(rpm))
    engine_force = torque * gear * final_drive * efficiency / radius
    tire_capacity = 1.15 * 1450.0 * 9.81 * 0.45
    delivered = engine_force if broken else min(engine_force, tire_capacity)
    physical = min(engine_force, tire_capacity)
    residual = abs(delivered - physical)
    return [torque, engine_force, tire_capacity, delivered, residual]


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    rpm, gear = p["engine_rpm"], p["gear_ratio"]
    signature = _point(rpm, gear, broken)
    rpm_sweep = np.linspace(2000.0, 7000.0, 126)
    speed = rpm_sweep * 2.0 * np.pi * 0.31 / (60.0 * gear * 4.10)
    engine_force = _torque(rpm_sweep) * gear * 4.10 * 0.92 / 0.31
    capacity = np.full_like(rpm_sweep, signature[2])
    delivered = engine_force if broken else np.minimum(engine_force, capacity)
    utilization = delivered / capacity
    return {
        "signature": signature,
        "metrics": [
            ("engine_torque", "Engine torque", signature[0], "N*m"),
            ("engine_force", "Engine-limited wheel force", signature[1], "N"),
            ("delivered_force", "Delivered traction force", signature[3], "N"),
            ("envelope_residual", "Traction-envelope residual", signature[4], "N"),
        ],
        "plots": {
            "response": _plot(
                "Wheel-force traction envelope",
                "Road speed (m/s)",
                "Longitudinal force (N)",
                [
                    _trace("Engine-limited", speed, engine_force, "Road speed", "m/s", "Longitudinal force", "N"),
                    _trace("Tire capacity", speed, capacity, "Road speed", "m/s", "Longitudinal force", "N"),
                    _trace("Delivered", speed, delivered, "Road speed", "m/s", "Longitudinal force", "N"),
                ],
            ),
            "mechanism": _plot(
                "Driven-tire utilization",
                "Engine speed (rpm)",
                "Traction utilization (1)",
                [
                    _trace("Utilization", rpm_sweep, utilization, "Engine speed", "rpm", "Traction utilization", "1"),
                ],
            ),
        },
        "observation": "Engine torque becomes road force only after gearing, efficiency, and tire radius, and delivered force cannot exceed the driven-tire boundary.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
