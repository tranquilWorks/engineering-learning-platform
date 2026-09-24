from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 52
DEFAULTS = {"speed_m_s": 55.0, "stint_energy_mj": 120.0}
RANGES = {"speed_m_s": (30.0, 75.0), "stint_energy_mj": (60.0, 200.0)}
BROKEN_TEXT = "Broken mode double-counts downforce in tire capacity and omits drag from the force and energy budgets, overstating acceleration and stint length."
RECOVERY_TEXT = "Add aerodynamic load once, apply tire load sensitivity, subtract drag from tractive force, and debit drag work from every lap's stint budget."


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


def _point(
    speed: float,
    energy_mj: float,
    broken: bool,
) -> tuple[float, float, float, float, float, float]:
    mass, gravity, lap_length = 1450.0, 9.81, 4200.0
    dynamic_pressure_area = 0.5 * 1.225 * 2.0 * speed**2
    downforce = 1.30 * dynamic_pressure_area
    drag = 0.42 * dynamic_pressure_area
    used_downforce = 2.0 * downforce if broken else downforce
    reference_load = mass * gravity
    tire_capacity = 1.22 * reference_load * (
        (reference_load + used_downforce) / reference_load
    ) ** 0.86
    power_force = 210000.0 / speed
    tractive_force = min(tire_capacity, power_force)
    used_drag = 0.0 if broken else drag
    usable_acceleration = max(0.0, (tractive_force - used_drag) / mass)
    lap_energy = (3.60e6 + used_drag * lap_length) / 1.0e6
    energy_laps = energy_mj / lap_energy
    thermal_laps = 34.0 / (1.0 + 0.00012 * downforce + 0.00008 * drag)
    stint_laps = min(energy_laps, thermal_laps)
    physical_capacity = 1.22 * reference_load * (
        (reference_load + downforce) / reference_load
    ) ** 0.86
    physical_force = min(physical_capacity, power_force)
    physical_acceleration = max(0.0, (physical_force - drag) / mass)
    physical_lap_energy = (3.60e6 + drag * lap_length) / 1.0e6
    physical_stint = min(energy_mj / physical_lap_energy, thermal_laps)
    residual = abs(usable_acceleration - physical_acceleration) + abs(
        stint_laps - physical_stint
    )
    return downforce, drag, usable_acceleration, lap_energy, stint_laps, residual


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    speed, energy = p["speed_m_s"], p["stint_energy_mj"]
    signature = list(_point(speed, energy, broken))
    speed_sweep = np.linspace(30.0, 75.0, 91)
    acceleration_sweep, drag_sweep = [], []
    for value in speed_sweep:
        _, sweep_drag, acceleration, _, _, _ = _point(value, energy, broken)
        acceleration_sweep.append(acceleration)
        drag_sweep.append(sweep_drag / 1450.0)
    energy_sweep = np.linspace(60.0, 200.0, 71)
    stint_sweep = [_point(speed, value, broken)[4] for value in energy_sweep]
    lap_energy_sweep = [_point(speed, value, broken)[3] for value in energy_sweep]
    return {
        "signature": signature,
        "metrics": [
            ("downforce", "Total downforce", signature[0], "N"),
            ("drag", "Aerodynamic drag", signature[1], "N"),
            ("usable_acceleration", "Usable acceleration", signature[2], "m/s^2"),
            ("lap_energy", "Lap energy", signature[3], "MJ"),
            ("stint_laps", "Predicted stint", signature[4], "lap"),
            ("coupling_residual", "Coupling residual", signature[5], "1"),
        ],
        "plots": {
            "response": _plot(
                "Aero-load and drag coupling",
                "Vehicle speed (m/s)",
                "Acceleration (m/s^2)",
                [
                    _trace(
                        "Usable acceleration",
                        speed_sweep,
                        acceleration_sweep,
                        "Vehicle speed",
                        "m/s",
                        "Acceleration",
                        "m/s^2",
                    ),
                    _trace(
                        "Drag deceleration",
                        speed_sweep,
                        drag_sweep,
                        "Vehicle speed",
                        "m/s",
                        "Acceleration",
                        "m/s^2",
                    ),
                ],
            ),
            "mechanism": _plot(
                "Stint energy limit",
                "Available stint energy (MJ)",
                "Predicted laps (lap)",
                [
                    _trace(
                        "Stint length",
                        energy_sweep,
                        stint_sweep,
                        "Available stint energy",
                        "MJ",
                        "Predicted laps",
                        "lap",
                    ),
                    _trace(
                        "Per-lap energy",
                        energy_sweep,
                        lap_energy_sweep,
                        "Available stint energy",
                        "MJ",
                        "Per-lap energy",
                        "MJ",
                    ),
                ],
            ),
        },
        "observation": "Downforce can raise tire capacity while drag consumes both instantaneous tractive force and the finite energy budget; neither contribution may be counted twice.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
