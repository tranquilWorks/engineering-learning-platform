from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 42
BROKEN_TEXT = 'Broken mode fits a pinhole model to distorted edge points and reuses training views as validation.'
RECOVERY_TEXT = 'Restore the distortion model, diversify board poses, and retain edge-weighted held-out residuals.'


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
    a = float(p["radial_k1"])
    b = float(p["calibration_views"])
    if broken:
        a, b = (0.28, 5.0)
    x = np.linspace(0.0, 1.0, 181)
    signature = [float(value) for value in [abs(a)*12/np.sqrt(max(1.,b))*(3 if broken else 1), 100*abs(a)/max(1.,b)*(.8 if broken else .15), abs(a)*45*(2 if broken else .2)]]
    y1 = np.asarray(abs(a)*45*x*x, dtype=float)
    y2 = np.asarray(np.zeros_like(x), dtype=float)
    z1 = np.asarray(abs(a)*12/np.sqrt(np.maximum(1.,4+56*x)), dtype=float)
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
        "metrics": [("reprojection_rms", "Reprojection Rms", signature[0], "px"), ("focal_bias", "Focal Bias", signature[1], "%"), ("edge_residual", "Edge Residual", signature[2], "px")],
        "plots": {
            "response": _plot("Radial calibration residual", "Normalized image radius (1)", "Reprojection error (px)", [
                _trace("Model response", x, y1, "Normalized image radius", "1", "Reprojection error", "px"),
                _trace("Reference or bound", x, y2, "Normalized image radius", "1", "Reprojection error", "px"),
            ]),
            "mechanism": _plot("Calibration convergence with view count", "View fraction (1)", "RMS residual (px)", [
                _trace("Governing mechanism", x, z1, "View fraction", "1", "RMS residual", "px"),
                _trace("Requirement or reference", x, z2, "View fraction", "1", "RMS residual", "px"),
            ]),
        },
        "observation": 'Camera calibration is supported by held-out reprojection residuals spanning the image, not by a low fit error on one pose.',
    }



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
