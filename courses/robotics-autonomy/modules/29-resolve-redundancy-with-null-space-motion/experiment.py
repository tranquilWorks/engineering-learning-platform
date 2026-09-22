from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 29
BROKEN_TEXT = 'Broken mode adds the secondary velocity directly, leaking posture motion into the end-effector task.'
RECOVERY_TEXT = 'Restore the null projector, tune damping near singularity, and verify task residual and joint-limit margin together.'


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
    a = float(p["damping"])
    b = float(p["null_gain_per_s"])
    if broken:
        a, b = (0.45, 1.8)
    x = np.linspace(0.0, 1.0, 181)
    signature = [float(value) for value in [(b*.3 if broken else a*a/(1+a)), b*(.4 if broken else a/(1+a)), max(.0,.9-.2*b-.1*a)]]
    y1 = np.asarray(np.exp(-(1+a)*x), dtype=float)
    y2 = np.asarray(np.zeros_like(x), dtype=float)
    z1 = np.asarray(.9-.2*b*x, dtype=float)
    z2 = np.asarray(np.full_like(x,.3), dtype=float)
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
        "metrics": [("task_velocity_error", "Task Velocity Error", signature[0], "m/s"), ("null_space_leakage", "Null Space Leakage", signature[1], "m/s"), ("joint_limit_margin", "Joint Limit Margin", signature[2], "rad")],
        "plots": {
            "response": _plot("Redundant task-velocity residual", "Motion fraction (1)", "Task error (m/s)", [
                _trace("Model response", x, y1, "Motion fraction", "1", "Task error", "m/s"),
                _trace("Reference or bound", x, y2, "Motion fraction", "1", "Task error", "m/s"),
            ]),
            "mechanism": _plot("Joint-limit margin", "Motion fraction (1)", "Angular margin (rad)", [
                _trace("Governing mechanism", x, z1, "Motion fraction", "1", "Angular margin", "rad"),
                _trace("Requirement or reference", x, z2, "Motion fraction", "1", "Angular margin", "rad"),
            ]),
        },
        "observation": 'Secondary motion may improve posture only through the Jacobian null space while the primary task residual remains bounded.',
    }



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
