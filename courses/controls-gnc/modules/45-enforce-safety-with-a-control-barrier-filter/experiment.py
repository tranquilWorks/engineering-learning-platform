from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 45
BROKEN_TEXT = 'Broken mode bypasses the safety filter while commanding rapid motion toward the boundary.'
RECOVERY_TEXT = 'Restore the projection, inspect the intervention size, and keep the claim limited to the modeled relative-degree-one constraint.'


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
    a=float(p["barrier_gain_per_s"]); b=float(p["nominal_closing_speed"])
    if broken: a=2.0; b=4.0
    x=np.linspace(0.,10.,240)
    signature=[float(-b if broken else max(-b,-a*.4)),float(.4+.1*(-b if broken else max(-b,-a*.4))),float(0 if broken else abs(max(-b,-a*.4)+b))]
    y1=np.asarray(.4+(-b if broken else np.maximum(-b,-a*.4))*x,dtype=float); y2=np.asarray(.4-b*x,dtype=float)
    z1=np.asarray(np.full_like(x,-b),dtype=float); z2=np.asarray(np.full_like(x,(-b if broken else max(-b,-a*.4))),dtype=float)
    if y1.ndim==0: y1=np.full_like(x,float(y1))
    if y2.ndim==0: y2=np.full_like(x,float(y2))
    if z1.ndim==0: z1=np.full_like(x,float(z1))
    if z2.ndim==0: z2=np.full_like(x,float(z2))
    return {"signature":signature,"metrics":[("filtered_command", "Filtered Command", signature[0], "m/s"),("one_step_safety_margin", "One Step Safety Margin", signature[1], "m"),("intervention", "Intervention", signature[2], "m/s")],"plots":{
      "response":_plot("Barrier-filtered distance","Time (s)","Safety distance (m)",[_trace("Nominal/filtered",x,y1,"Time","s","Safety distance","m"),_trace("Reference/boundary",x,y2,"Time","s","Safety distance","m")]),
      "mechanism":_plot("Nominal and safe commands","Time (s)","Velocity command (m/s)",[_trace("Mechanism",x,z1,"Time","s","Velocity command","m/s"),_trace("Requirement/reference",x,z2,"Time","s","Velocity command","m/s")])},
      "observation":"The filtered command satisfies the declared barrier inequality and equals the nominal command whenever that command is already safe."}



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
