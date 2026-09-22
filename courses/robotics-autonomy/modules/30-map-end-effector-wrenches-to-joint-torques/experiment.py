from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 30
BROKEN_TEXT = 'Broken mode uses J F rather than J-transpose F, producing a dimensionally and energetically inconsistent torque.'
RECOVERY_TEXT = 'Restore the transpose map, carry wrench frame labels, and verify virtual power before interpreting force capability.'


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
    a = float(p["force_n"])
    b = float(p["lever_arm_m"])
    if broken:
        a, b = (28.0, 1.1)
    x = np.linspace(0.0, 1.0, 181)
    signature = [float(value) for value in [a*b*(1.4 if broken else 1.0), a*b*(.2 if broken else 0.0), 1/max(.05,b)]]
    y1 = np.asarray(a*b*x, dtype=float)
    y2 = np.asarray(a*b*np.ones_like(x), dtype=float)
    z1 = np.asarray(a*x, dtype=float)
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
        "metrics": [("joint_torque", "Joint Torque", signature[0], "N*m"), ("virtual_power_error", "Virtual Power Error", signature[1], "W"), ("mechanical_advantage", "Mechanical Advantage", signature[2], "1")],
        "plots": {
            "response": _plot("Joint torque from Cartesian force", "Load fraction (1)", "Joint torque (N*m)", [
                _trace("Model response", x, y1, "Load fraction", "1", "Joint torque", "N*m"),
                _trace("Reference or bound", x, y2, "Load fraction", "1", "Joint torque", "N*m"),
            ]),
            "mechanism": _plot("Virtual-power comparison", "Motion fraction (1)", "Power contribution (W)", [
                _trace("Governing mechanism", x, z1, "Motion fraction", "1", "Power contribution", "W"),
                _trace("Requirement or reference", x, z2, "Motion fraction", "1", "Power contribution", "W"),
            ]),
        },
        "observation": 'Jacobian transpose statics must preserve virtual power between joint and Cartesian coordinates.',
    }



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
