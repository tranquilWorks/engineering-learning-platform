from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 53
BROKEN_TEXT = 'Broken mode accepts the measurement regardless of a gate exceedance.'
RECOVERY_TEXT = 'Restore innovation gating, log the rejection, and diagnose the model rather than silently shrinking covariance.'


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
    a=float(p["nis_gate"]); b=float(p["outlier_sigma"])
    if broken: a=1.0; b=8.0
    x=np.linspace(0.,10.,240)
    signature=[float(b*b),float(max(b*b-a,0)),float(1. if broken else float(b*b<=a))]
    y1=np.asarray(x*x,dtype=float); y2=np.asarray(np.full_like(x,a),dtype=float)
    z1=np.asarray((x*x<=a).astype(float),dtype=float); z2=np.asarray(np.ones_like(x) if broken else (x*x<=a).astype(float),dtype=float)
    if y1.ndim==0: y1=np.full_like(x,float(y1))
    if y2.ndim==0: y2=np.full_like(x,float(y2))
    if z1.ndim==0: z1=np.full_like(x,float(z1))
    if z2.ndim==0: z2=np.full_like(x,float(z2))
    return {"signature":signature,"metrics":[("normalized_innovation_squared", "Normalized Innovation Squared", signature[0], "1"),("gate_exceedance", "Gate Exceedance", signature[1], "1"),("accepted_outlier", "Accepted Outlier", signature[2], "bool")],"plots":{
      "response":_plot("Innovation consistency statistic","Innovation magnitude (sigma)","NIS (1)",[_trace("Nominal/filtered",x,y1,"Innovation magnitude","sigma","NIS","1"),_trace("Reference/boundary",x,y2,"Innovation magnitude","sigma","NIS","1")]),
      "mechanism":_plot("Measurement gate decision","Innovation magnitude (sigma)","Accepted flag (bool)",[_trace("Mechanism",x,z1,"Innovation magnitude","sigma","Accepted flag","bool"),_trace("Requirement/reference",x,z2,"Innovation magnitude","sigma","Accepted flag","bool")])},
      "observation":"A measurement is accepted only when its NIS is inside the declared gate; NEES/NIS interpretation requires the corresponding covariance model."}



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
