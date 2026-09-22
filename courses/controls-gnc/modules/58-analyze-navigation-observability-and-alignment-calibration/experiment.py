from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 58
BROKEN_TEXT = 'Broken mode removes the maneuver span, collapsing the information matrix rank.'
RECOVERY_TEXT = 'Execute a sufficiently diverse calibration maneuver and reject a covariance result from rank-deficient geometry.'


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
    a=float(p["maneuver_span_deg"]); b=float(p["measurement_noise"])
    if broken: a=0.0; b=0.05
    x=np.linspace(0.,10.,240)
    signature=[float(0. if broken else np.sin(np.deg2rad(a))**2/b**2),float(1e9 if broken or a==0 else (1+abs(np.cos(np.deg2rad(a))))/(1-abs(np.cos(np.deg2rad(a)))+1e-6)),float(b/max(abs(np.sin(np.deg2rad(a))),1e-6))]
    y1=np.asarray(np.cos(np.deg2rad(a)*(x-.5)),dtype=float); y2=np.asarray(np.ones_like(x),dtype=float)
    z1=np.asarray(np.full_like(x,0 if broken else np.sin(np.deg2rad(a))**2/b**2),dtype=float); z2=np.asarray(np.zeros_like(x),dtype=float)
    if y1.ndim==0: y1=np.full_like(x,float(y1))
    if y2.ndim==0: y2=np.full_like(x,float(y2))
    if z1.ndim==0: z1=np.full_like(x,float(z1))
    if z2.ndim==0: z2=np.full_like(x,float(z2))
    return {"signature":signature,"metrics":[("observability_determinant", "Observability Determinant", signature[0], "1"),("information_condition", "Information Condition", signature[1], "1"),("bias_standard_deviation", "Bias Standard Deviation", signature[2], "1")],"plots":{
      "response":_plot("Alignment maneuver regressors","Normalized sample (1)","Regressor amplitude (1)",[_trace("Nominal/filtered",x,y1,"Normalized sample","1","Regressor amplitude","1"),_trace("Reference/boundary",x,y2,"Normalized sample","1","Regressor amplitude","1")]),
      "mechanism":_plot("Accumulated observability information","Normalized sample (1)","Information determinant (1)",[_trace("Mechanism",x,z1,"Normalized sample","1","Information determinant","1"),_trace("Requirement/reference",x,z2,"Normalized sample","1","Information determinant","1")])},
      "observation":"Heading/bias calibration requires maneuver diversity; repeated geometry cannot separate the two parameters regardless of sample count."}



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
