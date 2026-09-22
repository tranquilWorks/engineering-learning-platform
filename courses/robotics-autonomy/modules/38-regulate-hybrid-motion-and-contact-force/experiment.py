from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 38
BROKEN_TEXT = 'Broken mode defines selection axes in the world frame while contact normal rotates with the surface.'
RECOVERY_TEXT = 'Express selection matrices in the contact frame, restore complementarity, and verify force error plus tangential leakage.'


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
    a = float(p["force_setpoint_n"])
    b = float(p["surface_angle_deg"])
    if broken:
        a, b = (35.0, 75.0)
    x = np.linspace(0.0, 1.0, 181)
    signature = [float(value) for value in [a*abs(np.sin(np.deg2rad(b)))*(.5 if broken else .03), abs(np.sin(np.deg2rad(b)))*(.2 if broken else .005), abs(np.sin(np.deg2rad(b)))*(.4 if broken else 0.0)]]
    y1 = np.asarray(a*(1-np.exp(-5*x)), dtype=float)
    y2 = np.asarray(a*np.ones_like(x), dtype=float)
    z1 = np.asarray(abs(np.sin(np.deg2rad(b)))*x*(.2 if broken else .005), dtype=float)
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
        "metrics": [("force_error", "Force Error", signature[0], "N"), ("motion_leakage", "Motion Leakage", signature[1], "m/s"), ("selection_orthogonality", "Selection Orthogonality", signature[2], "1")],
        "plots": {
            "response": _plot("Normal contact-force regulation", "Time fraction (1)", "Normal force (N)", [
                _trace("Model response", x, y1, "Time fraction", "1", "Normal force", "N"),
                _trace("Reference or bound", x, y2, "Time fraction", "1", "Normal force", "N"),
            ]),
            "mechanism": _plot("Tangential motion leakage", "Time fraction (1)", "Tangential velocity (m/s)", [
                _trace("Governing mechanism", x, z1, "Time fraction", "1", "Tangential velocity", "m/s"),
                _trace("Requirement or reference", x, z2, "Time fraction", "1", "Tangential velocity", "m/s"),
            ]),
        },
        "observation": 'Hybrid control must assign complementary motion and force subspaces so normal force regulation does not corrupt tangential motion.',
    }



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
