from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 46
BROKEN_TEXT = 'Broken mode estimates pose from a nearly collinear landmark set without robust rejection.'
RECOVERY_TEXT = 'Restore spatially distributed landmarks, robust residuals, and a rotation retraction before accepting pose.'


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
    a = float(p["landmark_noise_px"])
    b = float(p["visible_landmarks"])
    if broken:
        a, b = (7.5, 4.0)
    x = np.linspace(0.0, 1.0, 181)
    signature = [float(value) for value in [a/np.sqrt(max(4.,b))*(.12 if broken else .025), a/np.sqrt(max(4.,b))*(4 if broken else .7), max(0.,b*(.45 if broken else .9))]]
    y1 = np.asarray(a*(1-x)/np.sqrt(max(4.,b)), dtype=float)
    y2 = np.asarray(np.zeros_like(x), dtype=float)
    z1 = np.asarray(b*(.45 if broken else .9)*np.ones_like(x), dtype=float)
    z2 = np.asarray(np.full_like(x,b), dtype=float)
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
        "metrics": [("translation_error", "Translation Error", signature[0], "m"), ("rotation_error", "Rotation Error", signature[1], "deg"), ("inlier_count", "Inlier Count", signature[2], "count")],
        "plots": {
            "response": _plot("Object-pose translation convergence", "Iteration fraction (1)", "Translation error (m)", [
                _trace("Model response", x, y1, "Iteration fraction", "1", "Translation error", "m"),
                _trace("Reference or bound", x, y2, "Iteration fraction", "1", "Translation error", "m"),
            ]),
            "mechanism": _plot("Landmark consensus support", "Iteration fraction (1)", "Inlier count (count)", [
                _trace("Governing mechanism", x, z1, "Iteration fraction", "1", "Inlier count", "count"),
                _trace("Requirement or reference", x, z2, "Iteration fraction", "1", "Inlier count", "count"),
            ]),
        },
        "observation": 'Pose estimation must keep the solution on SE(3), use nondegenerate landmarks, and report geometric residuals plus inlier support.',
    }



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
