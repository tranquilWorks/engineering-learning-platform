from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 52
BROKEN_TEXT = 'Broken mode assigns negative process-noise density, producing a nonphysical covariance decrement.'
RECOVERY_TEXT = 'Restore a valid PSD noise model and derive discrete covariance from the declared continuous density and interval.'


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
    a=float(p["process_noise_density"]); b=float(p["propagation_interval_s"])
    if broken: a=0.8; b=2.0
    x=np.linspace(0.,10.,240)
    signature=[float(1+( -a if broken else a)*b),float(min(1+( -a if broken else a)*b,0) if broken else 1+(a*b)),float(np.sqrt(max(1+(-a if broken else a)*b,0)))]
    y1=np.asarray(1+(-a if broken else a)*x,dtype=float); y2=np.asarray(np.ones_like(x),dtype=float)
    z1=np.asarray(np.sqrt(np.maximum(1+(-a if broken else a)*x,0)),dtype=float); z2=np.asarray(np.ones_like(x),dtype=float)
    if y1.ndim==0: y1=np.full_like(x,float(y1))
    if y2.ndim==0: y2=np.full_like(x,float(y2))
    if z1.ndim==0: z1=np.full_like(x,float(z1))
    if z2.ndim==0: z2=np.full_like(x,float(z2))
    return {"signature":signature,"metrics":[("propagated_variance", "Propagated Variance", signature[0], "1"),("minimum_covariance_eigenvalue", "Minimum Covariance Eigenvalue", signature[1], "1"),("standard_deviation", "Standard Deviation", signature[2], "1")],"plots":{
      "response":_plot("Random-walk variance growth","Propagation time (s)","Variance (1)",[_trace("Nominal/filtered",x,y1,"Propagation time","s","Variance","1"),_trace("Reference/boundary",x,y2,"Propagation time","s","Variance","1")]),
      "mechanism":_plot("Random-walk standard deviation","Propagation time (s)","Standard deviation (1)",[_trace("Mechanism",x,z1,"Propagation time","s","Standard deviation","1"),_trace("Requirement/reference",x,z2,"Propagation time","s","Standard deviation","1")])},
      "observation":"Nonnegative process noise makes covariance positive semidefinite and increases variance without changing a zero-mean state prediction."}



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
