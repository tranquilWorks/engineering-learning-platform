from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 51
DEFAULTS = {"speed_m_s": 45.0, "front_ride_height_mm": 80.0}
RANGES = {"speed_m_s": (20.0, 70.0), "front_ride_height_mm": (50.0, 120.0)}
BROKEN_TEXT = "Broken mode inserts millimetres into a ride-height law calibrated in metres, corrupting front downforce, balance, and pitch moment."
RECOVERY_TEXT = "Convert ride height to metres once, retain signed front and rear force centers, and verify the unit-sensitive coefficient against its physical-height reference."


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
) -> dict[str, Any]:
    return {
        "type": "scattergl",
        "mode": "lines",
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


def _coefficients(height_mm: float, broken: bool) -> tuple[float, float, float]:
    height = height_mm if broken else height_mm / 1000.0
    front_coefficient = 0.58 - 2.2 * (height - 0.080)
    rear_coefficient = 0.72
    drag_coefficient = 0.34 + 0.06 * (front_coefficient + rear_coefficient)
    return front_coefficient, rear_coefficient, drag_coefficient


def _forces(
    speed: float,
    height_mm: float,
    broken: bool,
) -> tuple[float, float, float]:
    front_coefficient, rear_coefficient, drag_coefficient = _coefficients(
        height_mm,
        broken,
    )
    dynamic_pressure_area = 0.5 * 1.225 * 2.0 * speed**2
    return (
        dynamic_pressure_area * front_coefficient,
        dynamic_pressure_area * rear_coefficient,
        dynamic_pressure_area * drag_coefficient,
    )


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    speed, height_mm = p["speed_m_s"], p["front_ride_height_mm"]
    front, rear, drag = _forces(speed, height_mm, broken)
    total = front + rear
    front_balance = front / total if abs(total) > 1.0e-12 else 0.0
    pitch_moment = rear * 1.50 - front * 1.20
    physical_front, _, _ = _forces(speed, height_mm, False)
    unit_residual = abs(front - physical_front)
    signature = [front, rear, drag, front_balance, pitch_moment, unit_residual]
    height_sweep = np.linspace(50.0, 120.0, 71)
    front_sweep, rear_sweep = [], []
    for value in height_sweep:
        sweep_front, sweep_rear, _ = _forces(speed, value, broken)
        front_sweep.append(sweep_front)
        rear_sweep.append(sweep_rear)
    speed_sweep = np.linspace(20.0, 70.0, 101)
    downforce_sweep, drag_sweep = [], []
    for value in speed_sweep:
        sweep_front, sweep_rear, sweep_drag = _forces(value, height_mm, broken)
        downforce_sweep.append(sweep_front + sweep_rear)
        drag_sweep.append(sweep_drag)
    return {
        "signature": signature,
        "metrics": [
            ("front_downforce", "Front downforce", front, "N"),
            ("rear_downforce", "Rear downforce", rear, "N"),
            ("drag", "Aerodynamic drag", drag, "N"),
            ("front_balance", "Front aero balance", 100.0 * front_balance, "%"),
            ("unit_residual", "Ride-height unit residual", unit_residual, "N"),
        ],
        "plots": {
            "response": _plot(
                "Ride-height aero map",
                "Front ride height (mm)",
                "Aerodynamic force (N)",
                [
                    _trace(
                        "Front downforce",
                        height_sweep,
                        front_sweep,
                        "Front ride height",
                        "mm",
                        "Aerodynamic force",
                        "N",
                    ),
                    _trace(
                        "Rear downforce",
                        height_sweep,
                        rear_sweep,
                        "Front ride height",
                        "mm",
                        "Aerodynamic force",
                        "N",
                    ),
                ],
            ),
            "mechanism": _plot(
                "Speed-squared aero scaling",
                "Vehicle speed (m/s)",
                "Aerodynamic force (N)",
                [
                    _trace(
                        "Total downforce",
                        speed_sweep,
                        downforce_sweep,
                        "Vehicle speed",
                        "m/s",
                        "Aerodynamic force",
                        "N",
                    ),
                    _trace(
                        "Drag",
                        speed_sweep,
                        drag_sweep,
                        "Vehicle speed",
                        "m/s",
                        "Aerodynamic force",
                        "N",
                    ),
                ],
            ),
        },
        "observation": "Front ride height shifts the aero center while all aerodynamic forces retain their speed-squared dependence and declared force signs.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
