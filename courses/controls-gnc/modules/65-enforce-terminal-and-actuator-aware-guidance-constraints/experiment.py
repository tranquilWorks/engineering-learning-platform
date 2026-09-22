from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 65
BROKEN_TEXT = 'Broken mode applies the unconstrained terminal command and reports zero miss despite violating actuator authority.'
RECOVERY_TEXT = 'Restore saturation, propagate the constrained plant, and renegotiate terminal requirements when authority is insufficient.'


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
    a=float(p["acceleration_limit_m_s2"]); b=float(p["terminal_weight"])
    if broken: a=8.0; b=20.0
    x=np.linspace(0.,10.,240)
    signature=[float(2.5*b),float(max(2.5*b-a,0)),float(0. if broken else max(2.5*b-a,0)*.4)]
    y1=np.asarray(np.minimum(2.5*b/(x+.5),a) if not broken else 2.5*b/(x+.5),dtype=float); y2=np.asarray(np.full_like(x,a),dtype=float)
    z1=np.asarray(np.maximum(2.5*b-a,0)*x/5,dtype=float); z2=np.asarray(np.zeros_like(x),dtype=float)
    if y1.ndim==0: y1=np.full_like(x,float(y1))
    if y2.ndim==0: y2=np.full_like(x,float(y2))
    if z1.ndim==0: z1=np.full_like(x,float(z1))
    if z2.ndim==0: z2=np.full_like(x,float(z2))
    return {"signature":signature,"metrics":[("required_acceleration", "Required Acceleration", signature[0], "m/s^2"),("constraint_violation", "Constraint Violation", signature[1], "m/s^2"),("terminal_error_bound", "Terminal Error Bound", signature[2], "m")],"plots":{
      "response":_plot("Terminal acceleration schedule","Time to go (s)","Acceleration command (m/s^2)",[_trace("Nominal/filtered",x,y1,"Time to go","s","Acceleration command","m/s^2"),_trace("Reference/boundary",x,y2,"Time to go","s","Acceleration command","m/s^2")]),
      "mechanism":_plot("Constrained terminal-error bound","Time to go (s)","Terminal error (m)",[_trace("Mechanism",x,z1,"Time to go","s","Terminal error","m"),_trace("Requirement/reference",x,z2,"Time to go","s","Terminal error","m")])},
      "observation":"The applied command never exceeds actuator authority; an infeasible terminal requirement must appear as residual error, not a hidden command."}



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
