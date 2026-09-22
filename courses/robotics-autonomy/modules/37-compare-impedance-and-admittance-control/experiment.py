from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 37
BROKEN_TEXT = 'Broken mode uses negative virtual damping, injecting energy into the contact oscillation.'
RECOVERY_TEXT = 'Restore positive damping, select architecture from actuator/sensor causality, and verify decaying stored energy.'


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
    a = float(p["environment_stiffness_n_m"])
    b = float(p["virtual_damping_n_s_m"])
    if broken:
        a, b = (2800.0, 3.0)
    x = np.linspace(0.0, 1.0, 181)
    signature = [float(value) for value in [.01*a*(1.5 if broken else 1.), 4/max(1.,(-b if broken else b)), .5*a*(.01)**2*(2 if broken else 1)]]
    y1 = np.asarray(.01*a*np.exp((b if broken else -b)*x/50)*np.sin(8*x), dtype=float)
    y2 = np.asarray(np.zeros_like(x), dtype=float)
    z1 = np.asarray(.5*a*.0001*np.exp((b if broken else -b)*x/25), dtype=float)
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
        "metrics": [("peak_contact_force", "Peak Contact Force", signature[0], "N"), ("settling_time", "Settling Time", signature[1], "s"), ("interaction_energy", "Interaction Energy", signature[2], "J")],
        "plots": {
            "response": _plot("Contact-force transient", "Time fraction (1)", "Contact force (N)", [
                _trace("Model response", x, y1, "Time fraction", "1", "Contact force", "N"),
                _trace("Reference or bound", x, y2, "Time fraction", "1", "Contact force", "N"),
            ]),
            "mechanism": _plot("Virtual interaction energy", "Time fraction (1)", "Stored energy (J)", [
                _trace("Governing mechanism", x, z1, "Time fraction", "1", "Stored energy", "J"),
                _trace("Requirement or reference", x, z2, "Time fraction", "1", "Stored energy", "J"),
            ]),
        },
        "observation": 'Impedance shapes force from motion error while admittance shapes motion from force; both require an energy and damping interpretation at contact.',
    }



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
