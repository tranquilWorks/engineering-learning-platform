from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 45
BROKEN_TEXT = 'Broken mode swaps left/right disparity sign and accepts nonrectified correspondences.'
RECOVERY_TEXT = 'Restore positive disparity convention, rectify both images, and propagate disparity uncertainty into depth.'


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
    a = float(p["baseline_m"])
    b = float(p["disparity_px"])
    if broken:
        a, b = (0.04, 1.0)
    x = np.linspace(0.0, 1.0, 181)
    signature = [float(value) for value in [520*a/max(1.,b), 520*a*.5/max(1.,b*b), 3.0 if broken else .15]]
    y1 = np.asarray(520*a/np.maximum(1.,b*(.5+x)), dtype=float)
    y2 = np.asarray(np.full_like(x,520*a/b), dtype=float)
    z1 = np.asarray(520*a*.5/np.maximum(1.,b*(.5+x))**2, dtype=float)
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
        "metrics": [("depth", "Depth", signature[0], "m"), ("depth_sigma", "Depth Sigma", signature[1], "m"), ("rectification_residual", "Rectification Residual", signature[2], "px")],
        "plots": {
            "response": _plot("Stereo depth versus disparity", "Disparity fraction (1)", "Depth (m)", [
                _trace("Model response", x, y1, "Disparity fraction", "1", "Depth", "m"),
                _trace("Reference or bound", x, y2, "Disparity fraction", "1", "Depth", "m"),
            ]),
            "mechanism": _plot("Propagated depth uncertainty", "Disparity fraction (1)", "Depth standard deviation (m)", [
                _trace("Governing mechanism", x, z1, "Disparity fraction", "1", "Depth standard deviation", "m"),
                _trace("Requirement or reference", x, z2, "Disparity fraction", "1", "Depth standard deviation", "m"),
            ]),
        },
        "observation": 'Stereo depth is inverse in disparity, so uncertainty and calibration residuals must accompany every long-range estimate.',
    }



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
