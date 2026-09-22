from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 33
BROKEN_TEXT = 'Broken mode keeps unit duration regardless of path length, exceeding the joint-speed limit.'
RECOVERY_TEXT = 'Increase duration from the active bound, recompute acceleration, and verify every joint rather than only the endpoint.'


def _trace(name: str, x: Any, y: Any, x_quantity: str, x_unit: str,
           y_quantity: str, y_unit: str) -> dict[str, Any]:
    return {
        "type": "scattergl", "mode": "lines", "name": name,
        "x": np.asarray(x, dtype=float), "y": np.asarray(y, dtype=float),
        "meta": {"x_quantity": x_quantity, "x_unit": x_unit,
                 "y_quantity": y_quantity, "y_unit": y_unit},
    }


def _plot(title: str, x_title: str, y_title: str,
          traces: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "data": traces,
        "layout": {
            "title": {"text": title, "x": 0.02},
            "xaxis": {"title": {"text": x_title}},
            "yaxis": {"title": {"text": y_title}},
            "legend": {"orientation": "h"},
            "margin": {"l": 72, "r": 36, "t": 62, "b": 62},
            "hovermode": "closest", "uirevision": "keep-view",
        },
        "config": {"responsive": True, "displaylogo": False},
    }


def _result(model: dict[str, Any], broken: bool) -> dict[str, Any]:
    return {
        "metrics": [
            {"id": key, "label": label, "value": float(value), "unit": unit,
              "emphasis": "primary" if index == 0 else "normal"}
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
            "sample_count": int(model["sample_count"]),
            "signature": [float(value) for value in model["signature"]],
            "software_only": True,
        },
    }

def _model(p: dict[str, Any], broken: bool) -> dict[str, Any]:
    a = float(p["path_distance_rad"])
    b = float(p["speed_limit_rad_s"])
    if broken:
        a, b = (5.5, 0.35)
    x = np.linspace(0.0, 1.0, 181)
    signature = [float(value) for value in [1.0 if broken else a/max(b,.01), 6*a/(1.0 if broken else (a/max(b,.01))**2), max(0.0,a-(b if broken else a))]]
    y1 = np.asarray(a*(3*x*x-2*x*x*x), dtype=float)
    y2 = np.asarray(a*x, dtype=float)
    z1 = np.asarray(6*a*(1-2*x), dtype=float)
    z2 = np.asarray(np.zeros_like(x), dtype=float)
    if y1.ndim == 0:
        y1 = np.full_like(x, float(y1))
    if y2.ndim == 0:
        y2 = np.full_like(x, float(y2))
    if z1.ndim == 0:
        z1 = np.full_like(x, float(z1))
    if z2.ndim == 0:
        z2 = np.full_like(x, float(z2))
    return {
        "signature": signature,
        "sample_count": len(x),
        "metrics": [("minimum_duration", "Minimum Duration", signature[0], "s"), ("peak_acceleration", "Peak Acceleration", signature[1], "rad/s^2"), ("limit_violation", "Limit Violation", signature[2], "rad/s")],
        "plots": {
            "response": _plot("Time-scaled joint path", "Normalized time (1)", "Joint displacement (rad)", [
                _trace("Model response", x, y1, "Normalized time", "1", "Joint displacement", "rad"),
                _trace("Reference or bound", x, y2, "Normalized time", "1", "Joint displacement", "rad"),
            ]),
            "mechanism": _plot("Trajectory acceleration", "Normalized time (1)", "Joint acceleration (rad/s^2)", [
                _trace("Governing mechanism", x, z1, "Normalized time", "1", "Joint acceleration", "rad/s^2"),
                _trace("Requirement or reference", x, z2, "Normalized time", "1", "Joint acceleration", "rad/s^2"),
            ]),
        },
        "observation": 'Time scaling must preserve the geometric path while enforcing joint velocity and acceleration bounds.',
    }



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
