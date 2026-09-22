from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 36
BROKEN_TEXT = 'Broken mode keeps the placed poles but replaces the precompensator with one, producing a steady command scale error.'
RECOVERY_TEXT = 'Retain the stabilizing gain and restore the DC precompensator, then verify both eigenvalues and final-value tracking.'


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
    p1=float(p["dominant_pole_per_s"]); p2=p1*float(p["pole_ratio"]); K=np.array([p1*p2,p1+p2]); nbar=1. if broken else K[0]
    roots=np.roots([1.,K[1],K[0]]); desired=np.array([-p1,-p2]); error=float(np.max(abs(np.sort(roots)-np.sort(desired)))); steady=nbar/K[0]; ss_error=abs(1-steady)
    t=np.linspace(0,8/p1,240); y=steady*(1+(roots[1]*np.exp(roots[0]*t)-roots[0]*np.exp(roots[1]*t))/(roots[0]-roots[1])).real
    control=nbar-K[0]*y
    return {"signature":[error,ss_error,float(np.linalg.norm(K))],"metrics":[("pole_error","Pole assignment error",error,"1/s"),("tracking_error","Steady tracking error",ss_error,"1"),("gain_norm","Feedback gain norm",np.linalg.norm(K),"1/s^2")],
      "plots":{"response":_plot("State-feedback reference tracking","Time (s)","Position (m)",[_trace("Position",t,y,"Time","s","Position","m"),_trace("Reference",t,np.ones_like(t),"Time","s","Position","m")]),
      "mechanism":_plot("State-feedback command history","Time (s)","Command acceleration (m/s^2)",[_trace("Command",t,control,"Time","s","Command acceleration","m/s^2"),_trace("Zero command",t,np.zeros_like(t),"Time","s","Command acceleration","m/s^2")])},"observation":"Pole placement fixes homogeneous dynamics; the DC precompensator fixes the forced steady response."}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
