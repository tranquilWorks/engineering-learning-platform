from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 35
BROKEN_TEXT = 'Broken mode reverses gravity compensation, doubling the configuration-dependent load.'
RECOVERY_TEXT = 'Restore gravity sign, bound model mismatch, and verify both tracking and actuator torque authority.'


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
    a = float(p["model_error_fraction"])
    b = float(p["tracking_bandwidth_per_s"])
    if broken:
        a, b = (0.55, 0.7)
    x = np.linspace(0.0, 1.0, 181)
    signature = [float(value) for value in [(2*a if broken else a)/(1+b*b), 6+b*(1+a)*(1.8 if broken else 1.), 6*(2 if broken else a)]]
    y1 = np.asarray(np.exp(-b*x)*(1+a), dtype=float)
    y2 = np.asarray(np.zeros_like(x), dtype=float)
    z1 = np.asarray(6*np.cos(2*np.pi*x)*(2 if broken else a), dtype=float)
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
        "metrics": [("tracking_error", "Tracking Error", signature[0], "rad"), ("peak_torque", "Peak Torque", signature[1], "N*m"), ("cancellation_residual", "Cancellation Residual", signature[2], "N*m")],
        "plots": {
            "response": _plot("Computed-torque tracking error", "Time fraction (1)", "Joint error (rad)", [
                _trace("Model response", x, y1, "Time fraction", "1", "Joint error", "rad"),
                _trace("Reference or bound", x, y2, "Time fraction", "1", "Joint error", "rad"),
            ]),
            "mechanism": _plot("Dynamics cancellation residual", "Time fraction (1)", "Torque residual (N*m)", [
                _trace("Governing mechanism", x, z1, "Time fraction", "1", "Torque residual", "N*m"),
                _trace("Requirement or reference", x, z2, "Time fraction", "1", "Torque residual", "N*m"),
            ]),
        },
        "observation": 'Computed torque yields the selected nominal error dynamics only to the extent that inertia, velocity, and gravity models cancel consistently.',
    }



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
