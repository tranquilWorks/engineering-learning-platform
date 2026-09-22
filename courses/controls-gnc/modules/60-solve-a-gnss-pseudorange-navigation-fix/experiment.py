from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 60
BROKEN_TEXT = 'Broken mode uses near-collinear geometry with dilution 25, making the normal equations practically singular.'
RECOVERY_TEXT = 'Restore four-or-more diverse lines of sight, solve clock and position jointly, and inspect post-fit residuals.'


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
    a=float(p["pseudorange_noise_m"]); b=float(p["geometry_dilution"])
    if broken: a=2.0; b=12.0
    x=np.linspace(0.,10.,240)
    signature=[float(a*(25 if broken else b)),float(.5*a*(25 if broken else b)),float(a/np.sqrt(4))]
    y1=np.asarray(a*(1+x*(25 if broken else b)),dtype=float); y2=np.asarray(a*x,dtype=float)
    z1=np.asarray(np.full_like(x,a/np.sqrt(4)),dtype=float); z2=np.asarray(np.zeros_like(x),dtype=float)
    if y1.ndim==0: y1=np.full_like(x,float(y1))
    if y2.ndim==0: y2=np.full_like(x,float(y2))
    if z1.ndim==0: z1=np.full_like(x,float(z1))
    if z2.ndim==0: z2=np.full_like(x,float(z2))
    return {"signature":signature,"metrics":[("position_error_bound", "Position Error Bound", signature[0], "m"),("clock_bias_error", "Clock Bias Error", signature[1], "m"),("postfit_residual_rms", "Postfit Residual Rms", signature[2], "m")],"plots":{
      "response":_plot("Pseudorange geometry error amplification","Normalized geometry coordinate (1)","Position error bound (m)",[_trace("Nominal/filtered",x,y1,"Normalized geometry coordinate","1","Position error bound","m"),_trace("Reference/boundary",x,y2,"Normalized geometry coordinate","1","Position error bound","m")]),
      "mechanism":_plot("Post-fit pseudorange residual","Satellite index (count)","Residual RMS (m)",[_trace("Mechanism",x,z1,"Satellite index","count","Residual RMS","m"),_trace("Requirement/reference",x,z2,"Satellite index","count","Residual RMS","m")])},
      "observation":"A valid fix estimates position and clock bias together; geometry dilution scales range noise into state uncertainty."}



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
