from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 43
BROKEN_TEXT = 'Broken mode omits orientation normalization so descriptors drift under image rotation.'
RECOVERY_TEXT = 'Restore orientation-normalized patches, apply nonmaximum suppression, and report repeatability with coverage and descriptor distance.'


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
    a = float(p["detector_threshold"])
    b = float(p["image_rotation_deg"])
    if broken:
        a, b = (0.75, 170.0)
    x = np.linspace(0.0, 1.0, 181)
    signature = [float(value) for value in [max(0.,1-a)*(0.35 if broken else max(.2,1-abs(b)/360)), abs(np.sin(np.deg2rad(b)))*(1.0 if broken else .15), max(5.,320*(1-a))]]
    y1 = np.asarray(max(0.,1-a)*(1-.5*x), dtype=float)
    y2 = np.asarray(np.full_like(x,max(0.,1-a)), dtype=float)
    z1 = np.asarray(abs(np.sin(np.deg2rad(b)*x))*(1 if broken else .15), dtype=float)
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
        "metrics": [("repeatability", "Repeatability", signature[0], "1"), ("descriptor_distance", "Descriptor Distance", signature[1], "1"), ("feature_count", "Feature Count", signature[2], "count")],
        "plots": {
            "response": _plot("Feature repeatability under viewpoint change", "Viewpoint fraction (1)", "Repeatability (1)", [
                _trace("Model response", x, y1, "Viewpoint fraction", "1", "Repeatability", "1"),
                _trace("Reference or bound", x, y2, "Viewpoint fraction", "1", "Repeatability", "1"),
            ]),
            "mechanism": _plot("Descriptor change under rotation", "Viewpoint fraction (1)", "Descriptor distance (1)", [
                _trace("Governing mechanism", x, z1, "Viewpoint fraction", "1", "Descriptor distance", "1"),
                _trace("Requirement or reference", x, z2, "Viewpoint fraction", "1", "Descriptor distance", "1"),
            ]),
        },
        "observation": 'A useful feature remains localized and descriptively close under the declared viewpoint transformation while retaining spatial coverage.',
    }



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
