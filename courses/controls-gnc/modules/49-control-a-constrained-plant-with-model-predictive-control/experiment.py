from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 49
BROKEN_TEXT = 'Broken mode applies the unconstrained move and records a limit violation.'
RECOVERY_TEXT = 'Restore the constraint projection, check feasibility before cost, and distinguish horizon approximation from plant truth.'


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
    a=float(p["prediction_horizon"]); b=float(p["input_limit"])
    if broken: a=6.0; b=0.3
    x=np.linspace(0.,10.,240)
    signature=[float(-1.5 if broken else -min(1.5,b)),float(float(abs(-1.5)>b)),float(abs(1.5+(-1.5 if broken else -min(1.5,b)))/max(a,1))]
    y1=np.asarray(1.5+(-1.5 if broken else -min(1.5,b))*x/a,dtype=float); y2=np.asarray(np.zeros_like(x),dtype=float)
    z1=np.asarray(np.full_like(x,abs(-1.5 if broken else -min(1.5,b))),dtype=float); z2=np.asarray(np.full_like(x,b),dtype=float)
    if y1.ndim==0: y1=np.full_like(x,float(y1))
    if y2.ndim==0: y2=np.full_like(x,float(y2))
    if z1.ndim==0: z1=np.full_like(x,float(z1))
    if z2.ndim==0: z2=np.full_like(x,float(z2))
    return {"signature":signature,"metrics":[("first_control_move", "First Control Move", signature[0], "1"),("constraint_activity", "Constraint Activity", signature[1], "1"),("predicted_terminal_error", "Predicted Terminal Error", signature[2], "1")],"plots":{
      "response":_plot("Predicted constrained state","Prediction step (step)","State error (1)",[_trace("Nominal/filtered",x,y1,"Prediction step","step","State error","1"),_trace("Reference/boundary",x,y2,"Prediction step","step","State error","1")]),
      "mechanism":_plot("Input constraint activity","Prediction step (step)","Control magnitude (1)",[_trace("Mechanism",x,z1,"Prediction step","step","Control magnitude","1"),_trace("Requirement/reference",x,z2,"Prediction step","step","Control magnitude","1")])},
      "observation":"The applied MPC move satisfies the declared input bound; an unconstrained optimum is not a feasible control law when it exceeds that bound."}



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
