from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 31
DEFAULTS = {"heat_input_w": 900, "ambient_temp_c": 25}
RANGES = {"heat_input_w": (0, 2500), "ambient_temp_c": (-10, 45)}
BROKEN_TEXT = "Broken mode uses Celsius in the absolute pressure ratio."
RECOVERY_TEXT = "Convert gas temperature to Kelvin and close input heat against stored energy and rejected heat."


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
    heat_input = p["heat_input_w"]
    ambient = p["ambient_temp_c"]
    thermal_capacity, heat_transfer = 15000.0, 35.0
    duration, time_step = 600.0, 2.0
    time = np.arange(0.0, duration + time_step, time_step)
    temperature = np.empty_like(time)
    temperature[0] = ambient
    rejected = 0.0
    for index in range(1, len(time)):
        loss = heat_transfer * (temperature[index - 1] - ambient)
        rejected += loss * time_step
        temperature[index] = temperature[index - 1] + (
            heat_input - loss
        ) * time_step / thermal_capacity

    reference_pressure, reference_temp_c = 210.0, 20.0
    expected_pressure = reference_pressure * (
        (temperature + 273.15) / (reference_temp_c + 273.15)
    )
    if broken:
        pressure = reference_pressure * temperature / reference_temp_c
    else:
        pressure = expected_pressure
    grip = 1.25 * np.exp(-((temperature - 80.0) / 38.0) ** 2)
    grip *= np.maximum(0.45, 1.0 - 0.00002 * (pressure - 240.0) ** 2)
    pressure_residual = abs(pressure[-1] - expected_pressure[-1])
    balance_residual = abs(
        heat_input * duration
        - rejected
        - thermal_capacity * (temperature[-1] - ambient)
    )
    signature = [
        temperature[-1],
        pressure[-1],
        float(np.max(grip)),
        pressure_residual,
        balance_residual,
    ]
    return {
        "signature": signature,
        "metrics": [
            ("temperature", "Final tire temperature", temperature[-1], "degC"),
            ("pressure", "Final absolute pressure", pressure[-1], "kPa"),
            ("grip", "Peak modeled grip", np.max(grip), "1"),
            ("gas_law_residual", "Pressure-law residual", pressure_residual, "kPa"),
        ],
        "plots": {
            "response": _plot("Tire thermal and pressure history", "Time (s)", "Temperature (degC)", [
                _trace("Tire temperature", time, temperature, "Time", "s", "Tire temperature", "degC"),
            ]),
            "mechanism": _plot("Grip across the thermal-pressure path", "Tire temperature (degC)", "Grip coefficient (1)", [
                _trace("Temperature-pressure grip", temperature, grip, "Tire temperature", "degC", "Grip coefficient", "1"),
            ]),
        },
        "observation": "Thermal state follows an energy balance; pressure requires absolute temperature and grip peaks inside a bounded thermal-pressure window.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
