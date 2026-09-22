from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 59
BROKEN_TEXT = 'Broken mode doubles the applied bias and disables the bias correction.'
RECOVERY_TEXT = 'Estimate and subtract bias, reapply gravity/frame conventions, and compare propagation to the analytic limiting case.'


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
    a=float(p["accelerometer_bias_m_s2"]); b=float(p["coast_duration_s"])
    if broken: a=0.08; b=90.0
    x=np.linspace(0.,10.,240)
    signature=[float((2 if broken else 1)*a*b),float(.5*(2 if broken else 1)*a*b*b),float(.5*(a if broken else .05*a)*b*b)]
    y1=np.asarray((2 if broken else 1)*a*x,dtype=float); y2=np.asarray(np.zeros_like(x),dtype=float)
    z1=np.asarray(.5*(2 if broken else 1)*a*x*x,dtype=float); z2=np.asarray(.5*(a if broken else .05*a)*x*x,dtype=float)
    if y1.ndim==0: y1=np.full_like(x,float(y1))
    if y2.ndim==0: y2=np.full_like(x,float(y2))
    if z1.ndim==0: z1=np.full_like(x,float(z1))
    if z2.ndim==0: z2=np.full_like(x,float(z2))
    return {"signature":signature,"metrics":[("velocity_error", "Velocity Error", signature[0], "m/s"),("position_error", "Position Error", signature[1], "m"),("corrected_position_error", "Corrected Position Error", signature[2], "m")],"plots":{
      "response":_plot("Inertial velocity error growth","Coast time (s)","Velocity error (m/s)",[_trace("Nominal/filtered",x,y1,"Coast time","s","Velocity error","m/s"),_trace("Reference/boundary",x,y2,"Coast time","s","Velocity error","m/s")]),
      "mechanism":_plot("Inertial position error growth","Coast time (s)","Position error (m)",[_trace("Mechanism",x,z1,"Coast time","s","Position error","m"),_trace("Requirement/reference",x,z2,"Coast time","s","Position error","m")])},
      "observation":"Under constant uncorrected bias, velocity error grows linearly and position error quadratically with coast time."}



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
