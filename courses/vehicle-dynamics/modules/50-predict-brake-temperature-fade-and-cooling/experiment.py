from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 50
DEFAULTS = {"stop_energy_kj": 450.0, "cooling_coefficient_w_k": 65.0}
RANGES = {
    "stop_energy_kj": (200.0, 700.0),
    "cooling_coefficient_w_k": (20.0, 120.0),
}
BROKEN_TEXT = "Broken mode counts convective heat rejection in the ledger but omits it from the rotor-temperature update, violating the thermal energy balance."
RECOVERY_TEXT = "Apply each stop's absorbed energy, integrate convective cooling over the interval, and close input energy against stored plus rejected heat."


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
        "mode": "lines+markers",
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


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    stop_energy = 1000.0 * p["stop_energy_kj"]
    cooling = p["cooling_coefficient_w_k"]
    absorbed_fraction, capacity = 0.75, 45000.0
    ambient, interval, step = 25.0, 45.0, 0.25
    stops, cooling_steps = 6, int(interval / step)
    temperature = ambient
    rejected = 0.0
    input_energy = 0.0
    stop_temperature = [temperature]
    post_cooling = [temperature]
    rejected_history = [0.0]
    for _ in range(stops):
        absorbed = absorbed_fraction * stop_energy
        input_energy += absorbed
        temperature += absorbed / capacity
        stop_temperature.append(temperature)
        for _ in range(cooling_steps):
            heat_loss = cooling * (temperature - ambient)
            rejected += heat_loss * step
            if not broken:
                temperature -= heat_loss * step / capacity
        post_cooling.append(temperature)
        rejected_history.append(rejected / 1000.0)
    peak_temperature = float(max(stop_temperature))
    fade_factor = float(
        np.clip(1.0 - 0.0018 * max(0.0, peak_temperature - 350.0), 0.45, 1.0)
    )
    stored = capacity * (temperature - ambient)
    residual = abs(input_energy - stored - rejected) / 1000.0
    signature = [
        peak_temperature,
        temperature,
        rejected / 1000.0,
        fade_factor,
        residual,
    ]
    stop_axis = np.arange(stops + 1, dtype=float)
    return {
        "signature": signature,
        "metrics": [
            ("peak_temperature", "Peak rotor temperature", peak_temperature, "degC"),
            ("final_temperature", "Final rotor temperature", temperature, "degC"),
            ("rejected_energy", "Rejected heat", signature[2], "kJ"),
            ("fade_factor", "Brake fade factor", fade_factor, "1"),
            ("energy_residual", "Thermal energy residual", residual, "kJ"),
        ],
        "plots": {
            "response": _plot(
                "Repeated-stop rotor temperature",
                "Stop count (1)",
                "Temperature (degC)",
                [
                    _trace(
                        "Immediately after stop",
                        stop_axis,
                        stop_temperature,
                        "Stop count",
                        "1",
                        "Rotor temperature",
                        "degC",
                    ),
                    _trace(
                        "After cooling interval",
                        stop_axis,
                        post_cooling,
                        "Stop count",
                        "1",
                        "Rotor temperature",
                        "degC",
                    ),
                ],
            ),
            "mechanism": _plot(
                "Thermal-energy ledger",
                "Stop count (1)",
                "Energy (kJ)",
                [
                    _trace(
                        "Cumulative absorbed energy",
                        stop_axis,
                        stop_axis * absorbed_fraction * stop_energy / 1000.0,
                        "Stop count",
                        "1",
                        "Energy",
                        "kJ",
                    ),
                    _trace(
                        "Cumulative rejected heat",
                        stop_axis,
                        rejected_history,
                        "Stop count",
                        "1",
                        "Energy",
                        "kJ",
                    ),
                ],
            ),
        },
        "observation": "Repeated braking raises rotor temperature until cooling offsets enough of each stop's absorbed energy; fade follows the peak, not merely the final temperature.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
