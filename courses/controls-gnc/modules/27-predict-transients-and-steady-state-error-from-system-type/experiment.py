from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 27
BROKEN_TEXT = 'Broken mode reverses damping, moving the conjugate poles into the right half-plane so transient specifications no longer describe a settling response.'
RECOVERY_TEXT = 'Restore positive damping, verify both poles are left-half-plane, and report steady error for the correct input class rather than from a finite snapshot.'


def _trace(name: str, x: Any, y: Any, x_quantity: str, x_unit: str,
           y_quantity: str, y_unit: str, *, mode: str = "lines") -> dict[str, Any]:
    return {
        "type": "scattergl", "mode": mode, "name": name,
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
            "signature": [float(value) for value in model["signature"]],
        },
    }

def _model(p: dict[str, Any], broken: bool) -> dict[str, Any]:
    zeta = -0.08 if broken else float(p["damping_ratio"])
    wn = float(p["natural_frequency_rad_s"])
    t = np.linspace(0.0, 8.0/max(wn, 0.2), 240)
    if 0.0 < zeta < 1.0:
        wd = wn*np.sqrt(1-zeta*zeta)
        phi = np.arctan2(np.sqrt(1-zeta*zeta), zeta)
        y = 1 - np.exp(-zeta*wn*t)/np.sqrt(1-zeta*zeta)*np.sin(wd*t+phi)
        overshoot = 100*np.exp(-np.pi*zeta/np.sqrt(1-zeta*zeta))
    elif zeta >= 1.0:
        roots = np.roots([1.0, 2*zeta*wn, wn*wn])
        y = np.real(1 + (roots[1]*np.exp(roots[0]*t)-roots[0]*np.exp(roots[1]*t))/(roots[0]-roots[1]))
        overshoot = 0.0
    else:
        roots = np.roots([1.0, 2*zeta*wn, wn*wn])
        y = np.real(1 + (roots[1]*np.exp(roots[0]*t)-roots[0]*np.exp(roots[1]*t))/(roots[0]-roots[1]))
        overshoot = float(100*(np.max(y)-1))
    settling = float(np.inf if zeta <= 0 else 4/(zeta*wn))
    if not np.isfinite(settling):
        settling = float(t[-1])
    ramp_error = 2*zeta/wn
    envelope = np.exp(-zeta*wn*t)
    return {
        "signature": [overshoot, settling, ramp_error],
        "metrics": [("overshoot", "Percent overshoot", overshoot, "%"),
                    ("settling", "Two-percent settling estimate", settling, "s"),
                    ("ramp_error", "Type-one ramp error", ramp_error, "s")],
        "plots": {
            "response": _plot("Second-order unit-step response", "Time (s)", "Normalized position (1)", [
                _trace("Servo response", t, y, "Time", "s", "Normalized position", "1"),
                _trace("Command", t, np.ones_like(t), "Time", "s", "Normalized position", "1")]),
            "mechanism": _plot("Pole-envelope decay", "Time (s)", "Envelope magnitude (1)", [
                _trace("Exponential envelope", t, envelope, "Time", "s", "Envelope magnitude", "1"),
                _trace("Two-percent band", t, np.full_like(t, 0.02), "Time", "s", "Envelope magnitude", "1")]),
        },
        "observation": "Transient poles and loop type answer different questions: damping/frequency shape the transient, while the origin pole determines the input class tracked without bias."
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
