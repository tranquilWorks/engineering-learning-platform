from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 46
BROKEN_TEXT = 'Broken mode freezes the sea-level gain while evaluating the highest-gain operating point.'
RECOVERY_TEXT = 'Restore interpolation, test the grid midpoints, and keep stability claims within the scheduled envelope.'


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
    a=float(p["operating_point"]); b=float(p["grid_spacing"])
    if broken: a=1.0; b=0.5
    x=np.linspace(0.,10.,240)
    signature=[float((1+.5*a*a)*(2 if broken else 2/(1+.5*a*a))),float(abs((1+.5*a*a)*(2 if broken else 2/(1+.5*a*a))-2)),float(b*b*.125)]
    y1=np.asarray((1+.5*x*x)*(2/(1+.5*x*x)),dtype=float); y2=np.asarray(np.full_like(x,2.),dtype=float)
    z1=np.asarray(2/(1+.5*x*x),dtype=float); z2=np.asarray(np.full_like(x,2.),dtype=float)
    if y1.ndim==0: y1=np.full_like(x,float(y1))
    if y2.ndim==0: y2=np.full_like(x,float(y2))
    if z1.ndim==0: z1=np.full_like(x,float(z1))
    if z2.ndim==0: z2=np.full_like(x,float(z2))
    return {"signature":signature,"metrics":[("scheduled_bandwidth", "Scheduled Bandwidth", signature[0], "1/s"),("bandwidth_error", "Bandwidth Error", signature[1], "1/s"),("interpolation_error", "Interpolation Error", signature[2], "1")],"plots":{
      "response":_plot("Scheduled closed-loop bandwidth","Operating point (1)","Bandwidth (1/s)",[_trace("Nominal/filtered",x,y1,"Operating point","1","Bandwidth","1/s"),_trace("Reference/boundary",x,y2,"Operating point","1","Bandwidth","1/s")]),
      "mechanism":_plot("Scheduled feedback gain","Operating point (1)","Gain (1)",[_trace("Mechanism",x,z1,"Operating point","1","Gain","1"),_trace("Requirement/reference",x,z2,"Operating point","1","Gain","1")])},
      "observation":"At tabulated points the inverse-gain schedule restores the target bandwidth; interpolation error must be measured between points."}



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
