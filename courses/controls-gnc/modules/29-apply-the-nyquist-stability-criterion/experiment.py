from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 29
BROKEN_TEXT = "Broken mode reduces gain below the stabilizing range while ignoring the plant's one open-loop right-half-plane pole."
RECOVERY_TEXT = 'Count P before inspecting the curve, choose gain whose encirclement satisfies N=Z-P, and confirm Z from the characteristic polynomial.'


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
    gain = 1.0 if broken else float(p["loop_gain"])
    pole = float(p["unstable_pole_per_s"])
    w = np.geomspace(1e-3, 1e3, 600)
    s = 1j*w
    positive = gain*(s+1)/((s-pole)*(s+2)*(s+3))
    contour = np.concatenate([positive, positive[::-1].conjugate()])
    roots = np.roots([1.0, 5.0-pole, 6.0-5.0*pole+gain, gain-6.0*pole])
    P = 1
    Z = int(np.sum(roots.real > 1e-9))
    N = Z-P
    phase = -np.unwrap(np.angle(1+contour))
    numerical_winding = int(np.rint((phase[-1]-phase[0])/(2*np.pi)))
    return {
        "signature": [P, Z, N, numerical_winding],
        "metrics": [("open_rhp", "Open-loop RHP poles P", P, "count"),
                    ("closed_rhp", "Closed-loop RHP poles Z", Z, "count"),
                    ("winding", "Required winding N=Z-P", N, "turns")],
        "plots": {
            "response": _plot("Nyquist image of the unstable open loop", "Loop real part (1)", "Loop imaginary part (1)", [
                _trace("Nyquist contour", contour.real, contour.imag, "Loop real part", "1", "Loop imaginary part", "1"),
                _trace("Critical point -1", [-1.0], [0.0], "Loop real part", "1", "Loop imaginary part", "1", mode="markers")]),
            "mechanism": _plot("Argument accumulation around the critical point", "Contour sample (count)", "Unwrapped argument of 1+L (rad)", [
                _trace("Argument", np.arange(len(phase)), phase, "Contour sample", "count", "Unwrapped argument", "rad"),
                _trace("Expected terminal argument", np.arange(len(phase)), np.full_like(phase, phase[0]+2*np.pi*N), "Contour sample", "count", "Unwrapped argument", "rad")]),
        },
        "observation": f"Polynomial counting gives P={P}, Z={Z}, and N={N}; the sampled contour gives winding {numerical_winding}."
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
