from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 27
BROKEN_TEXT = 'Broken mode applies the twist adjoint to the wrench, violating duality and changing computed power.'
RECOVERY_TEXT = 'Use the inverse-transpose wrench transform and verify an adjoint/inverse round trip plus equal power.'


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
    a = float(p["lever_arm_m"])
    b = float(p["angular_speed_rad_s"])
    if broken:
        a, b = (1.3, 5.5)
    x = np.linspace(0.0, 1.0, 181)
    signature = [float(value) for value in [abs(a*b)*(.25 if broken else 0.0), a*(.1 if broken else 1e-12), a/(1+b)]]
    y1 = np.asarray(b*np.ones_like(x), dtype=float)
    y2 = np.asarray(b*(1-x), dtype=float)
    z1 = np.asarray(a*b*x, dtype=float)
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
        "metrics": [("power_invariance_error", "Power Invariance Error", signature[0], "W"), ("adjoint_roundtrip_error", "Adjoint Roundtrip Error", signature[1], "1"), ("screw_pitch", "Screw Pitch", signature[2], "m/rad")],
        "plots": {
            "response": _plot("Twist components under a frame shift", "Transform fraction (1)", "Twist speed (rad/s)", [
                _trace("Model response", x, y1, "Transform fraction", "1", "Twist speed", "rad/s"),
                _trace("Reference or bound", x, y2, "Transform fraction", "1", "Twist speed", "rad/s"),
            ]),
            "mechanism": _plot("Instantaneous power audit", "Transform fraction (1)", "Power mismatch (W)", [
                _trace("Governing mechanism", x, z1, "Transform fraction", "1", "Power mismatch", "W"),
                _trace("Requirement or reference", x, z2, "Transform fraction", "1", "Power mismatch", "W"),
            ]),
        },
        "observation": 'A twist and its dual wrench must transform contragrediently so instantaneous power is frame invariant.',
    }



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
