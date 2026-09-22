from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 50
BROKEN_TEXT = 'Broken mode collapses excitation amplitude and frequency spread, making the regression nearly singular while still reporting a training fit.'
RECOVERY_TEXT = 'Restore broadband excitation within safety limits and retain a separate validation segment.'


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
    a=float(p["excitation_amplitude"]); b=float(p["frequency_spread_hz"])
    if broken: a=0.1; b=0.1
    x=np.linspace(0.,10.,240)
    signature=[float(1/max(a*b,.001)),float(.02/max(a*b,.001)),float(.01+.03/max(a*b,.001))]
    y1=np.asarray(a*np.sin(2*np.pi*b*x),dtype=float); y2=np.asarray(a*np.sin(2*np.pi*b*x)+.02*np.cos(7*x),dtype=float)
    z1=np.asarray(np.full_like(x,.01+.03/max(a*b,.001)),dtype=float); z2=np.asarray(.02*np.cos(7*x),dtype=float)
    if y1.ndim==0: y1=np.full_like(x,float(y1))
    if y2.ndim==0: y2=np.full_like(x,float(y2))
    if z1.ndim==0: z1=np.full_like(x,float(z1))
    if z2.ndim==0: z2=np.full_like(x,float(z2))
    return {"signature":signature,"metrics":[("information_condition", "Information Condition", signature[0], "1"),("parameter_error_bound", "Parameter Error Bound", signature[1], "1"),("validation_rms", "Validation Rms", signature[2], "1")],"plots":{
      "response":_plot("Identification excitation","Time (s)","Input amplitude (1)",[_trace("Nominal/filtered",x,y1,"Time","s","Input amplitude","1"),_trace("Reference/boundary",x,y2,"Time","s","Input amplitude","1")]),
      "mechanism":_plot("Held-out validation residual","Time (s)","Residual amplitude (1)",[_trace("Mechanism",x,z1,"Time","s","Residual amplitude","1"),_trace("Requirement/reference",x,z2,"Time","s","Residual amplitude","1")])},
      "observation":"Persistent excitation improves information conditioning, while held-out residual—not training fit—bounds the model claim."}



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
