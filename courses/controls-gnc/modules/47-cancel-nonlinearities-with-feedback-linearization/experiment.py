from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 47
BROKEN_TEXT = 'Broken mode reverses the cancellation term, doubling rather than removing the nonlinear drift.'
RECOVERY_TEXT = 'Restore the cancellation sign, bound parameter mismatch, and verify the residual over the stated state interval.'


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
    a=float(p["model_mismatch"]); b=float(p["tracking_gain_per_s"])
    if broken: a=0.45; b=2.0
    x=np.linspace(0.,10.,240)
    signature=[float(2 if broken else a),float(-b+(2 if broken else a)),float(abs(2 if broken else a)/(b+1))]
    y1=np.asarray(np.exp((-b+(2 if broken else a))*x),dtype=float); y2=np.asarray(np.exp(-b*x),dtype=float)
    z1=np.asarray((2 if broken else a)*x*x,dtype=float); z2=np.asarray(np.zeros_like(x),dtype=float)
    if y1.ndim==0: y1=np.full_like(x,float(y1))
    if y2.ndim==0: y2=np.full_like(x,float(y2))
    if z1.ndim==0: z1=np.full_like(x,float(z1))
    if z2.ndim==0: z2=np.full_like(x,float(z2))
    return {"signature":signature,"metrics":[("residual_drift", "Residual Drift", signature[0], "1/s"),("closed_loop_rate", "Closed Loop Rate", signature[1], "1/s"),("terminal_error", "Terminal Error", signature[2], "1")],"plots":{
      "response":_plot("Feedback-linearized error","Time (s)","Tracking error (1)",[_trace("Nominal/filtered",x,y1,"Time","s","Tracking error","1"),_trace("Reference/boundary",x,y2,"Time","s","Tracking error","1")]),
      "mechanism":_plot("Residual nonlinear drift","State magnitude (1)","Drift rate (1/s)",[_trace("Mechanism",x,z1,"State magnitude","1","Drift rate","1/s"),_trace("Requirement/reference",x,z2,"State magnitude","1","Drift rate","1/s")])},
      "observation":"Exact cancellation leaves the selected linear error dynamics; model mismatch appears explicitly as residual nonlinear drift."}



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
