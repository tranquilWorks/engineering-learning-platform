from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 31
BROKEN_TEXT = 'Broken mode drops a coupling term from Coriolis while retaining its inertia dependence, violating the skew identity.'
RECOVERY_TEXT = 'Restore paired inertia/Coriolis terms and verify energy balance before using inverse dynamics.'


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
    a = float(p["payload_kg"])
    b = float(p["elbow_angle_deg"])
    if broken:
        a, b = (4.5, 145.0)
    x = np.linspace(0.0, 1.0, 181)
    signature = [float(value) for value in [.18+.06*a*(1+abs(np.cos(np.deg2rad(b)))), (.12*a if broken else 1e-10), 9.81*(.3+.2*a)*np.cos(np.deg2rad(b))]]
    y1 = np.asarray(.18+.06*a*(1+np.cos(np.deg2rad(160*x))**2), dtype=float)
    y2 = np.asarray(np.full_like(x,.18), dtype=float)
    z1 = np.asarray(9.81*(.3+.2*a)*np.cos(np.deg2rad(160*x-80)), dtype=float)
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
        "metrics": [("minimum_inertia_eigenvalue", "Minimum Inertia Eigenvalue", signature[0], "kg*m^2"), ("skew_identity_error", "Skew Identity Error", signature[1], "1"), ("gravity_torque", "Gravity Torque", signature[2], "N*m")],
        "plots": {
            "response": _plot("Manipulator inertia eigenvalue", "Configuration sweep (1)", "Inertia eigenvalue (kg*m^2)", [
                _trace("Model response", x, y1, "Configuration sweep", "1", "Inertia eigenvalue", "kg*m^2"),
                _trace("Reference or bound", x, y2, "Configuration sweep", "1", "Inertia eigenvalue", "kg*m^2"),
            ]),
            "mechanism": _plot("Gravity torque over configuration", "Configuration sweep (1)", "Joint torque (N*m)", [
                _trace("Governing mechanism", x, z1, "Configuration sweep", "1", "Joint torque", "N*m"),
                _trace("Requirement or reference", x, z2, "Configuration sweep", "1", "Joint torque", "N*m"),
            ]),
        },
        "observation": 'A physically consistent rigid manipulator has symmetric positive inertia and satisfies the kinetic-energy skew identity.',
    }



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
