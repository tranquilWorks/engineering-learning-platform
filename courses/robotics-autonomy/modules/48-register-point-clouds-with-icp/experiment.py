from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 48
BROKEN_TEXT = 'Broken mode accepts all nearest neighbors from a large initial offset and terminates on a small update rather than a small residual.'
RECOVERY_TEXT = 'Restore distance gating, trimming/robust loss, and independent alignment residual plus pose-change termination.'


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
    a = float(p["initial_offset_m"])
    b = float(p["outlier_fraction"])
    if broken:
        a, b = (1.4, 0.65)
    x = np.linspace(0.0, 1.0, 181)
    signature = [float(value) for value in [(.02+a*.08+b*.25)*(2 if broken else 1), (a+b)*(.7 if broken else .08), min(60.,5+25*a+30*b)*(1.4 if broken else 1)]]
    y1 = np.asarray((.02+a*.08+b*.25)*np.exp(-4*x)*(2 if broken else 1), dtype=float)
    y2 = np.asarray(np.full_like(x,.02), dtype=float)
    z1 = np.asarray((a+b)*np.exp(-3*x)*(.7 if broken else .08), dtype=float)
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
        "metrics": [("alignment_rmse", "Alignment Rmse", signature[0], "m"), ("pose_error", "Pose Error", signature[1], "m"), ("iterations", "Iterations", signature[2], "count")],
        "plots": {
            "response": _plot("ICP alignment residual", "Iteration fraction (1)", "Point residual RMSE (m)", [
                _trace("Model response", x, y1, "Iteration fraction", "1", "Point residual RMSE", "m"),
                _trace("Reference or bound", x, y2, "Iteration fraction", "1", "Point residual RMSE", "m"),
            ]),
            "mechanism": _plot("Registered pose error", "Iteration fraction (1)", "Translation error (m)", [
                _trace("Governing mechanism", x, z1, "Iteration fraction", "1", "Translation error", "m"),
                _trace("Requirement or reference", x, z2, "Iteration fraction", "1", "Translation error", "m"),
            ]),
        },
        "observation": 'ICP supports only a local registration claim: correspondences, robust weighting, and initialization jointly determine convergence.',
    }



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
