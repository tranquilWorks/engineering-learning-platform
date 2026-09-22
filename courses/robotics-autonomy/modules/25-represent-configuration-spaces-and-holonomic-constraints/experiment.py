from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 25
BROKEN_TEXT = 'Broken mode ignores the constraint Jacobian and integrates a velocity with a nonzero normal component.'
RECOVERY_TEXT = 'Project velocity into the tangent space, re-evaluate h(q), and retain collision clearance before advancing.'


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
    a = float(p["constraint_offset_m"])
    b = float(p["joint_span_rad"])
    if broken:
        a, b = (0.35, 2.8)
    x = np.linspace(0.0, 1.0, 181)
    signature = [float(value) for value in [abs(a) if broken else 0.0, 2.0 if broken else 1.0, max(0.0, .5-a-.05*b)]]
    y1 = np.asarray(a*np.sin(2*np.pi*x) if broken else np.zeros_like(x), dtype=float)
    y2 = np.asarray(np.zeros_like(x), dtype=float)
    z1 = np.asarray(.5-a*x-.05*b, dtype=float)
    z2 = np.asarray(np.full_like(x,.2), dtype=float)
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
        "metrics": [("constraint_residual", "Constraint Residual", signature[0], "m"), ("tangent_dimension", "Tangent Dimension", signature[1], "count"), ("minimum_clearance", "Minimum Clearance", signature[2], "m")],
        "plots": {
            "response": _plot("Constraint residual along a configuration path", "Path fraction (1)", "Constraint residual (m)", [
                _trace("Model response", x, y1, "Path fraction", "1", "Constraint residual", "m"),
                _trace("Reference or bound", x, y2, "Path fraction", "1", "Constraint residual", "m"),
            ]),
            "mechanism": _plot("Configuration-space clearance", "Path fraction (1)", "Clearance (m)", [
                _trace("Governing mechanism", x, z1, "Path fraction", "1", "Clearance", "m"),
                _trace("Requirement or reference", x, z2, "Path fraction", "1", "Clearance", "m"),
            ]),
        },
        "observation": 'A valid constrained velocity lies in the null space of the constraint Jacobian and preserves configuration-space clearance.',
    }



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
