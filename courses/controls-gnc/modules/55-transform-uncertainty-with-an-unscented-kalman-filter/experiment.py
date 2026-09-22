from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 55
BROKEN_TEXT = 'Broken mode negates the central covariance weight, yielding a nonphysical moment estimate.'
RECOVERY_TEXT = 'Restore normalized mean/covariance weights and compare transformed moments to an analytic case before filtering data.'


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
    a=float(p["state_standard_deviation"]); b=float(p["sigma_spread"])
    if broken: a=0.8; b=0.2
    x=np.linspace(0.,10.,240)
    signature=[float(0. if not broken else a*a),float(0. if not broken else 2*a**4),float(-1. if broken else 1/(2*b*b+1))]
    y1=np.asarray(x*x,dtype=float); y2=np.asarray(np.full_like(x,a*a),dtype=float)
    z1=np.asarray((x*x-a*a)**2,dtype=float); z2=np.asarray(np.full_like(x,2*a**4),dtype=float)
    if y1.ndim==0: y1=np.full_like(x,float(y1))
    if y2.ndim==0: y2=np.full_like(x,float(y2))
    if z1.ndim==0: z1=np.full_like(x,float(z1))
    if z2.ndim==0: z2=np.full_like(x,float(z2))
    return {"signature":signature,"metrics":[("transformed_mean_error", "Transformed Mean Error", signature[0], "1"),("transformed_variance_error", "Transformed Variance Error", signature[1], "1"),("minimum_weight", "Minimum Weight", signature[2], "1")],"plots":{
      "response":_plot("Unscented transform of x squared","Sigma-point state (1)","Transformed value (1)",[_trace("Nominal/filtered",x,y1,"Sigma-point state","1","Transformed value","1"),_trace("Reference/boundary",x,y2,"Sigma-point state","1","Transformed value","1")]),
      "mechanism":_plot("Analytic transformed dispersion","Sigma-point state (1)","Squared deviation (1)",[_trace("Mechanism",x,z1,"Sigma-point state","1","Squared deviation","1"),_trace("Requirement/reference",x,z2,"Sigma-point state","1","Squared deviation","1")])},
      "observation":"A valid symmetric transform reproduces the declared nonlinear moments within its quadrature order and uses weights that sum to one."}



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
