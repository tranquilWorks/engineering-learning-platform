from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 45
DEFAULTS = {"launch_torque_nm": 220.0, "driveline_inertia_kg_m2": 0.35}
RANGES = {"launch_torque_nm": (120.0, 300.0), "driveline_inertia_kg_m2": (0.1, 0.8)}
BROKEN_TEXT = "Broken mode reflects driveline inertia through the inverse gear ratio and omits wheel inertia, understating effective mass and violating launch energy."
RECOVERY_TEXT = "Reflect every rotating inertia through the squared speed ratio and retain wheel inertia at the tire radius."


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


def _launch(torque: float, driveline_inertia: float, broken: bool) -> tuple[list[float], np.ndarray, np.ndarray]:
    mass, radius, ratio, efficiency = 1450.0, 0.31, 3.60 * 4.10, 0.90
    wheel_inertia = 1.20
    physical_equivalent = 4.0 * wheel_inertia / radius**2 + driveline_inertia * (ratio / radius) ** 2
    used_equivalent = driveline_inertia / (ratio * radius) ** 2 if broken else physical_equivalent
    effective_mass = mass + used_equivalent
    tire_capacity = 1.15 * mass * 9.81 * 0.45
    drive_force = min(torque * ratio * efficiency / radius, tire_capacity)
    step, samples = 0.01, 1501
    speed = np.zeros(samples)
    distance = np.zeros(samples)
    time = np.arange(samples) * step
    target_time = time[-1]
    for index in range(1, samples):
        resistance = 180.0 + 0.38 * speed[index - 1] ** 2
        acceleration = max(0.0, (drive_force - resistance) / effective_mass)
        speed[index] = speed[index - 1] + acceleration * step
        distance[index] = distance[index - 1] + speed[index - 1] * step
        if speed[index] >= 27.78 and target_time == time[-1]:
            target_time = time[index]
    work = drive_force * distance[-1]
    resistance_work = np.trapezoid(180.0 + 0.38 * speed**2, distance)
    physical_energy = 0.5 * (mass + physical_equivalent) * speed[-1] ** 2
    energy_residual = abs(work - resistance_work - physical_energy)
    signature = [
        physical_equivalent if not broken else used_equivalent,
        (drive_force - 180.0) / effective_mass,
        target_time,
        speed[-1],
        energy_residual,
    ]
    return signature, time, speed


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    signature, time, speed = _launch(
        p["launch_torque_nm"], p["driveline_inertia_kg_m2"], broken
    )
    kinetic = 0.5 * 1450.0 * speed**2 / 1000.0
    rotating = 0.5 * signature[0] * speed**2 / 1000.0
    return {
        "signature": signature,
        "metrics": [
            ("equivalent_mass", "Reflected inertia mass", signature[0], "kg"),
            ("initial_acceleration", "Initial launch acceleration", signature[1], "m/s^2"),
            ("target_time", "Time to 100 km/h", signature[2], "s"),
            ("energy_residual", "Launch energy residual", signature[4], "J"),
        ],
        "plots": {
            "response": _plot(
                "Traction-limited launch",
                "Elapsed time (s)",
                "Vehicle speed (m/s)",
                [_trace("Vehicle speed", time, speed, "Elapsed time", "s", "Vehicle speed", "m/s")],
            ),
            "mechanism": _plot(
                "Launch kinetic-energy partition",
                "Elapsed time (s)",
                "Kinetic energy (kJ)",
                [
                    _trace("Translational", time, kinetic, "Elapsed time", "s", "Kinetic energy", "kJ"),
                    _trace("Rotating equivalent", time, rotating, "Elapsed time", "s", "Kinetic energy", "kJ"),
                ],
            ),
        },
        "observation": "Rotating inertia contributes an equivalent translational mass proportional to the square of its speed ratio, so launch work must supply both energy stores.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
