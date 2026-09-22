from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 47
BROKEN_TEXT = 'Broken mode marks every unreturned beam cell as free, erasing unseen obstacles.'
RECOVERY_TEXT = 'Restore maximum-range/no-return handling, clamp evidence, and audit entropy plus false-free rate.'


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
    a = float(p["hit_probability"])
    b = float(p["beam_count"])
    if broken:
        a, b = (0.52, 12.0)
    x = np.linspace(0.0, 1.0, 181)
    signature = [float(value) for value in [1/(1+np.exp(-max(0.,b/60)*(a-.5)*4)), max(.0,1-a)*np.log2(max(2.,b))/10, (.35 if broken else max(0.,.08-(a-.5)*.1))]]
    y1 = np.asarray(1/(1+np.exp(-x*b/60*(a-.5)*4)), dtype=float)
    y2 = np.asarray(np.full_like(x,.5), dtype=float)
    z1 = np.asarray((1-a)*np.exp(-b*x/180), dtype=float)
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
        "metrics": [("occupied_probability", "Occupied Probability", signature[0], "1"), ("map_entropy", "Map Entropy", signature[1], "bit"), ("false_free_rate", "False Free Rate", signature[2], "1")],
        "plots": {
            "response": _plot("Occupancy update along a sensor ray", "Ray fraction (1)", "Occupancy probability (1)", [
                _trace("Model response", x, y1, "Ray fraction", "1", "Occupancy probability", "1"),
                _trace("Reference or bound", x, y2, "Ray fraction", "1", "Occupancy probability", "1"),
            ]),
            "mechanism": _plot("Map uncertainty reduction", "Observation fraction (1)", "Cell entropy (bit)", [
                _trace("Governing mechanism", x, z1, "Observation fraction", "1", "Cell entropy", "bit"),
                _trace("Requirement or reference", x, z2, "Observation fraction", "1", "Cell entropy", "bit"),
            ]),
        },
        "observation": 'Log-odds mapping must distinguish traversed free cells from terminal occupied cells and avoid treating unobserved space as free.',
    }



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
