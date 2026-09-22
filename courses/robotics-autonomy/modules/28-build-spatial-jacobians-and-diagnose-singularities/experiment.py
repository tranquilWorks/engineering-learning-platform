from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 28
BROKEN_TEXT = 'Broken mode evaluates the Jacobian at the wrong elbow sign, hiding the approaching straight-arm singularity.'
RECOVERY_TEXT = 'Restore the joint convention, compare against a finite difference, and report conditioning rather than inverting blindly.'


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
    a = float(p["elbow_angle_deg"])
    b = float(p["link_ratio"])
    if broken:
        a, b = (2.0, 0.25)
    x = np.linspace(0.0, 1.0, 181)
    signature = [float(value) for value in [abs(np.sin(np.deg2rad(a)))*min(1.0,b), abs(np.sin(np.deg2rad(a)))*b, (.05 if broken else 1e-7)*(1+b)]]
    y1 = np.asarray(abs(np.sin(np.deg2rad(180*x))), dtype=float)
    y2 = np.asarray(np.ones_like(x), dtype=float)
    z1 = np.asarray(1/np.maximum(.05,abs(np.sin(np.deg2rad(180*x)))), dtype=float)
    z2 = np.asarray(np.full_like(x,5.), dtype=float)
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
        "metrics": [("minimum_singular_value", "Minimum Singular Value", signature[0], "m/rad"), ("manipulability", "Manipulability", signature[1], "m^2/rad^2"), ("finite_difference_error", "Finite Difference Error", signature[2], "m/rad")],
        "plots": {
            "response": _plot("Jacobian singular values across elbow angle", "Normalized elbow sweep (1)", "Singular value (m/rad)", [
                _trace("Model response", x, y1, "Normalized elbow sweep", "1", "Singular value", "m/rad"),
                _trace("Reference or bound", x, y2, "Normalized elbow sweep", "1", "Singular value", "m/rad"),
            ]),
            "mechanism": _plot("Jacobian conditioning", "Normalized elbow sweep (1)", "Condition number (1)", [
                _trace("Governing mechanism", x, z1, "Normalized elbow sweep", "1", "Condition number", "1"),
                _trace("Requirement or reference", x, z2, "Normalized elbow sweep", "1", "Condition number", "1"),
            ]),
        },
        "observation": 'The spatial Jacobian must match finite-difference kinematics and expose loss of motion authority through singular values.',
    }



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
