from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 62
BROKEN_TEXT = 'Broken mode suppresses the alarm and retains the faulty measurement.'
RECOVERY_TEXT = 'Restore residual monitoring, exclude the identified fault, recompute the solution, and keep protection-level assumptions explicit.'


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
    a=float(p["fault_magnitude_m"]); b=float(p["integrity_threshold"])
    if broken: a=60.0; b=5.0
    x=np.linspace(0.,10.,240)
    signature=[float(a/3),float(b*2.5),float(a if broken else (.15*a if a/3>b else a))]
    y1=np.asarray(x/3,dtype=float); y2=np.asarray(np.full_like(x,b),dtype=float)
    z1=np.asarray(x,dtype=float); z2=np.asarray((.15*x if not broken else x),dtype=float)
    if y1.ndim==0: y1=np.full_like(x,float(y1))
    if y2.ndim==0: y2=np.full_like(x,float(y2))
    if z1.ndim==0: z1=np.full_like(x,float(z1))
    if z2.ndim==0: z2=np.full_like(x,float(z2))
    return {"signature":signature,"metrics":[("test_statistic", "Test Statistic", signature[0], "sigma"),("horizontal_protection_level", "Horizontal Protection Level", signature[1], "m"),("post_exclusion_residual", "Post Exclusion Residual", signature[2], "m")],"plots":{
      "response":_plot("Integrity test statistic","Fault magnitude (m)","Normalized residual (sigma)",[_trace("Nominal/filtered",x,y1,"Fault magnitude","m","Normalized residual","sigma"),_trace("Reference/boundary",x,y2,"Fault magnitude","m","Normalized residual","sigma")]),
      "mechanism":_plot("Residual after fault exclusion","Fault magnitude (m)","Post-fit residual (m)",[_trace("Mechanism",x,z1,"Fault magnitude","m","Post-fit residual","m"),_trace("Requirement/reference",x,z2,"Fault magnitude","m","Post-fit residual","m")])},
      "observation":"A declared fault above threshold raises an alarm and the excluded solution must be recomputed before reporting a reduced residual."}



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
