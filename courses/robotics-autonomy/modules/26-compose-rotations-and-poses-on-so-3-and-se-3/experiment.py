from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 26
BROKEN_TEXT = 'Broken mode uses degrees as radians and composes translation in the wrong frame.'
RECOVERY_TEXT = 'Convert units once, compose left-to-right under named frames, and verify orthogonality, determinant, and round trip.'


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
    a = float(p["rotation_angle_deg"])
    b = float(p["translation_m"])
    if broken:
        a, b = (150.0, 1.8)
    x = np.linspace(0.0, 1.0, 181)
    signature = [float(value) for value in [abs(np.sin(np.deg2rad(a))) * (1e-12 if not broken else .2), 0.0 if not broken else abs(np.sin(a))*.1, abs(b*np.sin(np.deg2rad(a))) * (1.0 if broken else .25)]]
    y1 = np.asarray(np.cos(np.deg2rad(a)*x), dtype=float)
    y2 = np.asarray(np.cos(np.deg2rad(a))*np.ones_like(x), dtype=float)
    z1 = np.asarray(b*np.sin(np.deg2rad(a)*x), dtype=float)
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
        "metrics": [("orthogonality_error", "Orthogonality Error", signature[0], "1"), ("determinant_error", "Determinant Error", signature[1], "1"), ("order_difference", "Order Difference", signature[2], "m")],
        "plots": {
            "response": _plot("Rotation-coordinate evolution", "Composition fraction (1)", "Rotation matrix component (1)", [
                _trace("Model response", x, y1, "Composition fraction", "1", "Rotation matrix component", "1"),
                _trace("Reference or bound", x, y2, "Composition fraction", "1", "Rotation matrix component", "1"),
            ]),
            "mechanism": _plot("Order-dependent translation", "Composition fraction (1)", "Translation difference (m)", [
                _trace("Governing mechanism", x, z1, "Composition fraction", "1", "Translation difference", "m"),
                _trace("Requirement or reference", x, z2, "Composition fraction", "1", "Translation difference", "m"),
            ]),
        },
        "observation": 'Rigid transforms must remain on SE(3), round trip through their inverse, and preserve the declared composition order.',
    }



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
