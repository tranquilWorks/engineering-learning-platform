from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 41
DEFAULTS = {"knee_velocity_m_s": 0.12, "high_speed_coefficient_n_s_m": 1800.0}
RANGES = {"knee_velocity_m_s": (0.05, 0.30), "high_speed_coefficient_n_s_m": (500.0, 3500.0)}
BROKEN_TEXT = "Broken mode treats metres per second as millimetres per second before applying the damper law, grossly overstating force and dissipated energy."
RECOVERY_TEXT = "Keep velocity in metres per second throughout the odd-symmetric digressive law and its cycle-energy integral."


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


def _force(
    velocity: np.ndarray | float,
    knee: float,
    high_coefficient: float,
) -> np.ndarray:
    values = np.asarray(velocity, dtype=float)
    low_coefficient = 7000.0
    return high_coefficient * values + (
        low_coefficient - high_coefficient
    ) * values / (1.0 + np.abs(values) / knee)


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    knee = p["knee_velocity_m_s"]
    high = p["high_speed_coefficient_n_s_m"]
    scale = 1000.0 if broken else 1.0
    evaluate = lambda velocity: _force(scale * np.asarray(velocity), knee, high)
    low_force = float(evaluate(0.05))
    high_force = float(evaluate(0.50))
    apparent_low_slope = float(evaluate(1.0e-4) / 1.0e-4)
    step = 1.0e-5
    high_slope = float((evaluate(0.50 + step) - evaluate(0.50 - step)) / (2.0 * step))
    time = np.linspace(0.0, 2.0, 1001)
    velocity = 0.35 * np.sin(np.pi * time)
    force = evaluate(velocity)
    cycle_energy = float(np.trapezoid(force * velocity, time))
    correct_force = float(_force(0.20, knee, high))
    unit_residual = abs(float(evaluate(0.20)) - correct_force)
    signature = [low_force, high_force, apparent_low_slope, cycle_energy, unit_residual]
    velocity_sweep = np.linspace(-0.70, 0.70, 281)
    force_sweep = evaluate(velocity_sweep)
    power_sweep = force_sweep * velocity_sweep
    return {
        "signature": signature,
        "metrics": [
            ("low_force", "Force at 0.05 m/s", low_force, "N"),
            ("high_force", "Force at 0.50 m/s", high_force, "N"),
            ("high_slope", "High-speed tangent slope", high_slope, "N*s/m"),
            ("cycle_energy", "Dissipated cycle energy", cycle_energy, "J"),
        ],
        "plots": {
            "response": _plot(
                "Digressive damper curve",
                "Damper velocity (m/s)",
                "Damper force (N)",
                [
                    _trace("Damper force", velocity_sweep, force_sweep, "Damper velocity", "m/s", "Damper force", "N"),
                ],
            ),
            "mechanism": _plot(
                "Instantaneous damping power",
                "Damper velocity (m/s)",
                "Dissipated power (W)",
                [
                    _trace("Damping power", velocity_sweep, power_sweep, "Damper velocity", "m/s", "Dissipated power", "W"),
                ],
            ),
        },
        "observation": "A digressive law begins near the low-speed slope, transitions continuously at the knee, and approaches the declared high-speed slope while remaining dissipative.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
