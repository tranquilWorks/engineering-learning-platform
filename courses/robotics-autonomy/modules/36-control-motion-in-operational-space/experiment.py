from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 36
BROKEN_TEXT = 'Broken mode substitutes identity inertia and an algebraic null projector near a conditioned Jacobian.'
RECOVERY_TEXT = 'Restore dynamic consistency, regularize the task inertia, and measure null-space leakage before adding posture objectives.'


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
    a = float(p["task_inertia_kg"])
    b = float(p["jacobian_condition"])
    if broken:
        a, b = (7.0, 26.0)
    x = np.linspace(0.0, 1.0, 181)
    signature = [float(value) for value in [a*(.25 if broken else .01)*b, a*(.2 if broken else .002)*b, a*(1+b/20)]]
    y1 = np.asarray(np.exp(-x*3)/(1+a), dtype=float)
    y2 = np.asarray(np.zeros_like(x), dtype=float)
    z1 = np.asarray(a*(1+b*x/20), dtype=float)
    z2 = np.asarray(np.full_like(x,a), dtype=float)
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
        "metrics": [("task_acceleration_error", "Task Acceleration Error", signature[0], "m/s^2"), ("null_torque_leakage", "Null Torque Leakage", signature[1], "N*m"), ("effective_inertia", "Effective Inertia", signature[2], "kg")],
        "plots": {
            "response": _plot("Operational-space acceleration error", "Time fraction (1)", "Acceleration error (m/s^2)", [
                _trace("Model response", x, y1, "Time fraction", "1", "Acceleration error", "m/s^2"),
                _trace("Reference or bound", x, y2, "Time fraction", "1", "Acceleration error", "m/s^2"),
            ]),
            "mechanism": _plot("Effective Cartesian inertia", "Task direction fraction (1)", "Task inertia (kg)", [
                _trace("Governing mechanism", x, z1, "Task direction fraction", "1", "Task inertia", "kg"),
                _trace("Requirement or reference", x, z2, "Task direction fraction", "1", "Task inertia", "kg"),
            ]),
        },
        "observation": 'Operational-space control must use dynamically consistent task inertia and a null torque that does not disturb the commanded task.',
    }



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
