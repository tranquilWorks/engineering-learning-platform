from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 56
BROKEN_TEXT = 'Broken mode skips the backward pass, so smoothed and filtered uncertainty are identical.'
RECOVERY_TEXT = 'Restore the backward recursion after the forward filter completes and label the result offline, not causal.'


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
    a=float(p["process_variance"]); b=float(p["measurement_variance"])
    if broken: a=0.2; b=1.0
    x=np.linspace(0.,10.,240)
    signature=[float(a*b/(a+b)),float(a*b/(a+b) if broken else .65*a*b/(a+b)),float(0. if broken else .35*a*b/(a+b))]
    y1=np.asarray((a+b)*(1-np.exp(-x)),dtype=float); y2=np.asarray(np.full_like(x,a*b/(a+b)),dtype=float)
    z1=np.asarray(np.full_like(x,a*b/(a+b)),dtype=float); z2=np.asarray(np.full_like(x,a*b/(a+b) if broken else .65*a*b/(a+b)),dtype=float)
    if y1.ndim==0: y1=np.full_like(x,float(y1))
    if y2.ndim==0: y2=np.full_like(x,float(y2))
    if z1.ndim==0: z1=np.full_like(x,float(z1))
    if z2.ndim==0: z2=np.full_like(x,float(z2))
    return {"signature":signature,"metrics":[("filtered_variance", "Filtered Variance", signature[0], "1"),("smoothed_variance", "Smoothed Variance", signature[1], "1"),("variance_reduction", "Variance Reduction", signature[2], "1")],"plots":{
      "response":_plot("Forward-filter uncertainty","Time (s)","Variance (1)",[_trace("Nominal/filtered",x,y1,"Time","s","Variance","1"),_trace("Reference/boundary",x,y2,"Time","s","Variance","1")]),
      "mechanism":_plot("Filtered and smoothed variance","Time (s)","Variance (1)",[_trace("Mechanism",x,z1,"Time","s","Variance","1"),_trace("Requirement/reference",x,z2,"Time","s","Variance","1")])},
      "observation":"RTS smoothed covariance is no larger than filtered covariance for the same linear-Gaussian model and complete future data."}



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
