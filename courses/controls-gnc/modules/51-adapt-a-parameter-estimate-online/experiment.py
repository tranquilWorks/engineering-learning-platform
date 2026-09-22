from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 51
BROKEN_TEXT = 'Broken mode removes excitation while forcing covariance downward, producing false confidence with persistent parameter error.'
RECOVERY_TEXT = 'Restore informative excitation and covariance-consistent RLS updates, then monitor both error and uncertainty.'


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
    a=float(p["forgetting_factor"]); b=float(p["excitation_level"])
    if broken: a=0.9; b=0.05
    x=np.linspace(0.,10.,240)
    signature=[float((1-a)/(max(b,.01)) if not broken else 1.),float((1-a+.01)/(b*b) if not broken else .001),float(b*b if not broken else 0.)]
    y1=np.asarray(1-np.exp(-b*b*x),dtype=float); y2=np.asarray(np.ones_like(x),dtype=float)
    z1=np.asarray(((1-a+.01)/(b*b))*np.exp(-(1-a+.01)*x),dtype=float); z2=np.asarray(np.full_like(x,.001 if broken else (1-a+.01)/(b*b)),dtype=float)
    if y1.ndim==0: y1=np.full_like(x,float(y1))
    if y2.ndim==0: y2=np.full_like(x,float(y2))
    if z1.ndim==0: z1=np.full_like(x,float(z1))
    if z2.ndim==0: z2=np.full_like(x,float(z2))
    return {"signature":signature,"metrics":[("terminal_parameter_error", "Terminal Parameter Error", signature[0], "1"),("terminal_covariance", "Terminal Covariance", signature[1], "1"),("information_rate", "Information Rate", signature[2], "1/s")],"plots":{
      "response":_plot("Online parameter convergence","Sample time (s)","Parameter estimate (1)",[_trace("Nominal/filtered",x,y1,"Sample time","s","Parameter estimate","1"),_trace("Reference/boundary",x,y2,"Sample time","s","Parameter estimate","1")]),
      "mechanism":_plot("RLS covariance evolution","Sample time (s)","Parameter covariance (1)",[_trace("Mechanism",x,z1,"Sample time","s","Parameter covariance","1"),_trace("Requirement/reference",x,z2,"Sample time","s","Parameter covariance","1")])},
      "observation":"Parameter convergence requires excitation; covariance must not shrink when the regressor carries no information."}



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
