from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 44
BROKEN_TEXT = 'Broken mode selects a sublevel outside the analytical decay region, making boundary Vdot positive.'
RECOVERY_TEXT = 'Shrink the sublevel below 1/sqrt(mu) and report it as a sufficient local certificate, not the exact global basin.'


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
    a=float(p["sublevel_radius"]); b=float(p["cubic_coefficient"])
    if broken: a=1.35; b=0.8
    x=np.linspace(0.,10.,240)
    signature=[float(1-b*a*a),float(-a*a+b*a**4),float(1/np.sqrt(b))]
    y1=np.asarray(.5*x*x,dtype=float); y2=np.asarray(.5*x*x,dtype=float)
    z1=np.asarray(-x*x+b*x**4,dtype=float); z2=np.asarray(np.zeros_like(x),dtype=float)
    if y1.ndim==0: y1=np.full_like(x,float(y1))
    if y2.ndim==0: y2=np.full_like(x,float(y2))
    if z1.ndim==0: z1=np.full_like(x,float(z1))
    if z2.ndim==0: z2=np.full_like(x,float(z2))
    return {"signature":signature,"metrics":[("minimum_decay_margin", "Minimum Decay Margin", signature[0], "1/s"),("boundary_vdot", "Boundary Vdot", signature[1], "1/s"),("roa_radius", "Roa Radius", signature[2], "1")],"plots":{
      "response":_plot("Lyapunov candidate","State x (1)","V(x) (1)",[_trace("Nominal/filtered",x,y1,"State x","1","V(x)","1"),_trace("Reference/boundary",x,y2,"State x","1","V(x)","1")]),
      "mechanism":_plot("Lyapunov derivative","State x (1)","V-dot (1/s)",[_trace("Mechanism",x,z1,"State x","1","V-dot","1/s"),_trace("Requirement/reference",x,z2,"State x","1","V-dot","1/s")])},
      "observation":"A claimed sublevel is certified only when V is positive and Vdot is strictly negative everywhere except the origin."}



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
