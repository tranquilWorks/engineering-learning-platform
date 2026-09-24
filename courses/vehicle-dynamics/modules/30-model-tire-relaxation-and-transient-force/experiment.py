from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 30
DEFAULTS = {"relaxation_length_m": 0.45, "speed_m_s": 20}
RANGES = {"relaxation_length_m": (0.1, 1.5), "speed_m_s": (2, 60)}
BROKEN_TEXT = "Broken mode treats a length in meters as a time constant in seconds and omits vehicle speed."
RECOVERY_TEXT = "Use tau equals relaxation length divided by speed and verify the 63-percent response in distance."


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
    relaxation = p["relaxation_length_m"]
    speed = p["speed_m_s"]
    steady_force = 3000.0
    time_constant = relaxation if broken else relaxation / speed
    one_length_time = relaxation / speed
    force_at_length = steady_force * (1.0 - np.exp(-one_length_time / time_constant))
    distance_to_63 = speed * time_constant
    final_time = 0.50
    final_force = steady_force * (1.0 - np.exp(-final_time / time_constant))
    final_error = steady_force - final_force
    conversion_error = abs(distance_to_63 - relaxation) / relaxation

    time = np.linspace(0.0, 0.50, 181)
    force_time = steady_force * (1.0 - np.exp(-time / time_constant))
    distance = np.linspace(0.0, max(4.0 * relaxation, speed * 0.5), 181)
    force_distance = steady_force * (1.0 - np.exp(-(distance / speed) / time_constant))
    ideal_distance = steady_force * (1.0 - np.exp(-distance / relaxation))
    signature = [force_at_length, distance_to_63, time_constant, final_error, conversion_error]
    return {
        "signature": signature,
        "metrics": [
            ("force_one_length", "Force after one relaxation length", force_at_length, "N"),
            ("distance_63", "Distance to 63 percent force", distance_to_63, "m"),
            ("time_constant", "Transient time constant", time_constant, "s"),
            ("conversion_error", "Speed-conversion relative error", conversion_error, "1"),
        ],
        "plots": {
            "response": _plot("Transient tire force in time", "Time (s)", "Longitudinal force (N)", [
                _trace("Transient force", time, force_time, "Time", "s", "Longitudinal force", "N"),
            ]),
            "mechanism": _plot("Distance-domain relaxation", "Travel distance (m)", "Longitudinal force (N)", [
                _trace("Implemented response", distance, force_distance, "Travel distance", "m", "Longitudinal force", "N"),
                _trace("Length-law invariant", distance, ideal_distance, "Travel distance", "m", "Longitudinal force", "N"),
            ]),
        },
        "observation": "Relaxation length fixes the spatial response; speed only maps that distance response into time.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
