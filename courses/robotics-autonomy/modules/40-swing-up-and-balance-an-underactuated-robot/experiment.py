from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 40
BROKEN_TEXT = 'Broken mode reverses the energy-error sign, driving the pendulum away from upright capture.'
RECOVERY_TEXT = 'Restore the energy sign, respect torque limits, and require both energy and angle/velocity capture conditions before switching.'


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
    a = float(p["energy_gain_per_s"])
    b = float(p["torque_limit_n_m"])
    if broken:
        a, b = (0.2, 0.3)
    x = np.linspace(0.0, 1.0, 181)
    signature = [float(value) for value in [12/(a*max(.2,b))*(2 if broken else 1), min(np.pi,1/(a*b))*(3 if broken else 1), 2.0/(1+a*b)*(2 if broken else 1)]]
    y1 = np.asarray(np.pi*(1-np.exp(-a*b*x/2))*np.cos(6*x), dtype=float)
    y2 = np.asarray(np.pi*np.ones_like(x), dtype=float)
    z1 = np.asarray(2*np.exp(-a*b*x/2), dtype=float)
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
        "metrics": [("capture_time", "Capture Time", signature[0], "s"), ("terminal_angle_error", "Terminal Angle Error", signature[1], "rad"), ("peak_energy_error", "Peak Energy Error", signature[2], "J")],
        "plots": {
            "response": _plot("Underactuated swing-up angle", "Time fraction (1)", "Pendulum angle (rad)", [
                _trace("Model response", x, y1, "Time fraction", "1", "Pendulum angle", "rad"),
                _trace("Reference or bound", x, y2, "Time fraction", "1", "Pendulum angle", "rad"),
            ]),
            "mechanism": _plot("Energy error to upright", "Time fraction (1)", "Energy error (J)", [
                _trace("Governing mechanism", x, z1, "Time fraction", "1", "Energy error", "J"),
                _trace("Requirement or reference", x, z2, "Time fraction", "1", "Energy error", "J"),
            ]),
        },
        "observation": 'Energy shaping must add energy below the upright target, remove it above target, and hand off to balancing only inside a reachable capture region.',
    }



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
