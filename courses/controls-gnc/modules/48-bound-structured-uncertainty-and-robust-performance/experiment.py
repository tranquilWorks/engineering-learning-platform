from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 48
BROKEN_TEXT = 'Broken mode applies the feedback with the wrong sign, allowing the least-stable family member to cross right half-plane.'
RECOVERY_TEXT = 'Restore the sign, recompute the worst member, and report the finite family and margin rather than general robust certification.'


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
    a=float(p["uncertainty_radius"]); b=float(p["feedback_gain"])
    if broken: a=0.9; b=0.2
    x=np.linspace(0.,10.,240)
    signature=[float((1-a)+( -b if broken else b)),float(1/max((1-a)+(-b if broken else b),.05)),float(2*a)]
    y1=np.asarray((1+x)+(-b if broken else b),dtype=float); y2=np.asarray(np.full_like(x,(1-a)+(-b if broken else b)),dtype=float)
    z1=np.asarray(1/np.maximum((1+x)+(-b if broken else b),.05),dtype=float); z2=np.asarray(np.ones_like(x),dtype=float)
    if y1.ndim==0: y1=np.full_like(x,float(y1))
    if y2.ndim==0: y2=np.full_like(x,float(y2))
    if z1.ndim==0: z1=np.full_like(x,float(z1))
    if z2.ndim==0: z2=np.full_like(x,float(z2))
    return {"signature":signature,"metrics":[("worst_stability_margin", "Worst Stability Margin", signature[0], "1/s"),("worst_sensitivity", "Worst Sensitivity", signature[1], "1"),("family_width", "Family Width", signature[2], "1/s")],"plots":{
      "response":_plot("Closed-loop margin over uncertainty","Normalized uncertainty (1)","Stability margin (1/s)",[_trace("Nominal/filtered",x,y1,"Normalized uncertainty","1","Stability margin","1/s"),_trace("Reference/boundary",x,y2,"Normalized uncertainty","1","Stability margin","1/s")]),
      "mechanism":_plot("Sensitivity proxy over uncertainty","Normalized uncertainty (1)","Sensitivity magnitude (1)",[_trace("Mechanism",x,z1,"Normalized uncertainty","1","Sensitivity magnitude","1"),_trace("Requirement/reference",x,z2,"Normalized uncertainty","1","Sensitivity magnitude","1")])},
      "observation":"A robust statement is valid only for every member of the explicitly swept uncertainty family and the stated performance metric."}



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
