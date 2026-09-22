from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 41
BROKEN_TEXT = 'Broken mode uses world-frame depth without applying the camera pose and projects a point behind the camera.'
RECOVERY_TEXT = 'Transform every point into the camera frame, reject nonpositive depth, and verify projection against a ray ratio.'


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
    a = float(p["focal_length_px"])
    b = float(p["point_depth_m"])
    if broken:
        a, b = (1100.0, 0.4)
    x = np.linspace(0.0, 1.0, 181)
    signature = [float(value) for value in [a*.4/max(.1,b), a*.4/max(.1,b*b), 1.0 if broken else 0.0]]
    y1 = np.asarray(a*.4/(b+.5*x), dtype=float)
    y2 = np.asarray(np.full_like(x,a*.4/b), dtype=float)
    z1 = np.asarray(a*.4/(b+.5*x)**2, dtype=float)
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
        "metrics": [("image_radius", "Image Radius", signature[0], "px"), ("depth_sensitivity", "Depth Sensitivity", signature[1], "px/m"), ("behind_camera_count", "Behind Camera Count", signature[2], "count")],
        "plots": {
            "response": _plot("Perspective image displacement", "Ray sample fraction (1)", "Image radius (px)", [
                _trace("Model response", x, y1, "Ray sample fraction", "1", "Image radius", "px"),
                _trace("Reference or bound", x, y2, "Ray sample fraction", "1", "Image radius", "px"),
            ]),
            "mechanism": _plot("Depth sensitivity of projection", "Ray sample fraction (1)", "Pixel sensitivity (px/m)", [
                _trace("Governing mechanism", x, z1, "Ray sample fraction", "1", "Pixel sensitivity", "px/m"),
                _trace("Requirement or reference", x, z2, "Ray sample fraction", "1", "Pixel sensitivity", "px/m"),
            ]),
        },
        "observation": 'Perspective projection is defined only for positive camera-frame depth and its pixel sensitivity grows inversely with depth.',
    }



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
