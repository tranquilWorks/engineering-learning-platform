from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 29
DEFAULTS = {"slip_ratio": 0.12, "slip_angle_deg": 8}
RANGES = {"slip_ratio": (-0.3, 0.3), "slip_angle_deg": (-18, 18)}
BROKEN_TEXT = "Broken mode delivers two pure-slip forces without enforcing their shared friction constraint."
RECOVERY_TEXT = "Compute joint utilization and apply one common radial scale factor to both force components."


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
    normal_load, friction = 3500.0, 1.2
    capacity = normal_load * friction
    cx, cy = 80000.0, 70000.0
    pure_fx = capacity * np.tanh(cx * slip / capacity)
    pure_fy = -capacity * np.tanh(cy * angle / capacity)
    demand_utilization = float(np.hypot(pure_fx, pure_fy) / capacity)
    scale = 1.0 if broken or demand_utilization <= 1.0 else 1.0 / demand_utilization
    delivered_fx = float(scale * pure_fx)
    delivered_fy = float(scale * pure_fy)
    utilization = float(np.hypot(delivered_fx, delivered_fy) / capacity)
    violation = max(0.0, utilization - 1.0)

    slip_grid = np.linspace(-0.30, 0.30, 161)
    fx_grid = capacity * np.tanh(cx * slip_grid / capacity)
    fy_fixed = pure_fy
    demand_grid = np.hypot(fx_grid, fy_fixed) / capacity
    scale_grid = np.ones_like(demand_grid) if broken else np.minimum(1.0, 1.0 / np.maximum(demand_grid, 1e-12))
    circle_angle = np.linspace(0.0, 2.0 * np.pi, 181)
    signature = [delivered_fx, delivered_fy, utilization, scale, violation]
    return {
        "signature": signature,
        "metrics": [
            ("fx", "Delivered longitudinal force", delivered_fx, "N"),
            ("fy", "Delivered lateral force", delivered_fy, "N"),
            ("utilization", "Combined friction utilization", utilization, "1"),
            ("violation", "Constraint violation", violation, "1"),
        ],
        "plots": {
            "response": _plot("Combined-force path", "Longitudinal force (N)", "Lateral force (N)", [
                _trace("Delivered sweep", scale_grid * fx_grid, scale_grid * fy_fixed, "Longitudinal force", "N", "Lateral force", "N"),
                _trace("Friction circle", capacity * np.cos(circle_angle), capacity * np.sin(circle_angle), "Longitudinal force", "N", "Lateral force", "N"),
            ]),
            "mechanism": _plot("Demand utilization and radial scale", "Slip ratio (1)", "Utilization or scale (1)", [
                _trace("Pure-demand utilization", slip_grid, demand_grid, "Slip ratio", "1", "Demand utilization", "1"),
                _trace("Applied scale", slip_grid, scale_grid, "Slip ratio", "1", "Force scale", "1"),
            ]),
        },
        "observation": "Pure-slip demands share one contact patch; a common radial projection preserves direction while enforcing total capacity.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
