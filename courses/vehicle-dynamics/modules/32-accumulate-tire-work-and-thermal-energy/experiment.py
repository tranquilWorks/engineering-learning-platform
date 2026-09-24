from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 32
DEFAULTS = {"slip_ratio": 0.08, "slip_angle_deg": 5}
RANGES = {"slip_ratio": (0, 0.2), "slip_angle_deg": (0, 15)}
BROKEN_TEXT = "Broken mode omits heat rejection from the thermal state while the energy audit still requires it."
RECOVERY_TEXT = "Restore loss inside the integration and verify slip work equals stored heat plus rejected heat."


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


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    slip = p["slip_ratio"]
    angle = np.deg2rad(p["slip_angle_deg"])
    speed, force_x, force_y = 30.0, 3000.0, 2800.0
    slip_power = abs(force_x * speed * slip) + abs(
        force_y * speed * np.tan(angle)
    )
    duration, time_step = 60.0, 0.25
    thermal_capacity, heat_transfer = 16000.0, 45.0
    initial_temperature, ambient = 30.0, 25.0
    time = np.arange(0.0, duration + time_step, time_step)
    temperature = np.empty_like(time)
    temperature[0] = initial_temperature
    rejected = 0.0
    rejected_history = np.zeros_like(time)
    for index in range(1, len(time)):
        loss = heat_transfer * (temperature[index - 1] - ambient)
        rejected += loss * time_step
        rejected_history[index] = rejected
        state_loss = 0.0 if broken else loss
        temperature[index] = temperature[index - 1] + (
            slip_power - state_loss
        ) * time_step / thermal_capacity

    work = slip_power * duration
    stored = thermal_capacity * (temperature[-1] - initial_temperature)
    balance_residual = abs(work - stored - rejected)
    signature = [
        slip_power,
        work,
        temperature[-1] - initial_temperature,
        rejected,
        balance_residual,
    ]
    return {
        "signature": signature,
        "metrics": [
            ("power", "Contact-patch slip power", slip_power, "W"),
            ("work", "Cumulative slip work", work, "J"),
            ("temperature", "Tire temperature rise", temperature[-1] - initial_temperature, "degC"),
            ("balance", "Energy-balance residual", balance_residual, "J"),
        ],
        "plots": {
            "response": _plot("Thermal response to slip work", "Time (s)", "Tire temperature (degC)", [
                _trace("Tire temperature", time, temperature, "Time", "s", "Tire temperature", "degC"),
            ]),
            "mechanism": _plot("Cumulative energy ledger", "Time (s)", "Energy (J)", [
                _trace("Input work", time, slip_power * time, "Time", "s", "Input work", "J"),
                _trace("Stored heat", time, thermal_capacity * (temperature-initial_temperature), "Time", "s", "Stored heat", "J"),
                _trace("Rejected heat", time, rejected_history, "Time", "s", "Rejected heat", "J"),
            ]),
        },
        "observation": "Slip power is dissipative; the cumulative work ledger reveals whether stored and rejected heat close the same boundary.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
