from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 44
BROKEN_TEXT = 'Broken mode fits all matches by least squares, allowing outliers to bias the model and pass themselves.'
RECOVERY_TEXT = 'Restore minimal-set sampling, residual gating, and a final refit on consensus inliers.'


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
    a = float(p["outlier_fraction"])
    b = float(p["ransac_threshold_px"])
    if broken:
        a, b = (0.82, 7.5)
    x = np.linspace(0.0, 1.0, 181)
    signature = [float(value) for value in [max(0.,1-a)*(.5 if broken else .95), b*(a*4 if broken else .08), min(1.,a*(1 if broken else .08*b))]]
    y1 = np.asarray(np.full_like(x,1-a), dtype=float)
    y2 = np.asarray(np.full_like(x,.5 if broken else .95*(1-a)), dtype=float)
    z1 = np.asarray(b*a*x*(4 if broken else .08), dtype=float)
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
        "metrics": [("inlier_ratio", "Inlier Ratio", signature[0], "1"), ("model_error", "Model Error", signature[1], "px"), ("false_acceptance", "False Acceptance", signature[2], "1")],
        "plots": {
            "response": _plot("Correspondence consensus", "Sample fraction (1)", "Inlier ratio (1)", [
                _trace("Model response", x, y1, "Sample fraction", "1", "Inlier ratio", "1"),
                _trace("Reference or bound", x, y2, "Sample fraction", "1", "Inlier ratio", "1"),
            ]),
            "mechanism": _plot("Robust model residual", "Sample fraction (1)", "Reprojection residual (px)", [
                _trace("Governing mechanism", x, z1, "Sample fraction", "1", "Reprojection residual", "px"),
                _trace("Requirement or reference", x, z2, "Sample fraction", "1", "Reprojection residual", "px"),
            ]),
        },
        "observation": 'Robust correspondence fitting must recover a consensus model from the declared inlier ratio and verify it on residuals not used to hypothesize the model.',
    }



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
