from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 61
BROKEN_TEXT = 'Broken mode omits the bias state, leaving a deterministic interval-squared error after every update.'
RECOVERY_TEXT = 'Restore the bias state, inject the estimated error into the nominal solution, and reset only the error coordinates.'


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
    a=float(p["gnss_interval_s"]); b=float(p["bias_random_walk"])
    if broken: a=10.0; b=0.08
    x=np.linspace(0.,10.,240)
    signature=[float(.5*b*a*a+.5),float((.5*b*a*a+.5)*.35),float(.5*b*a*a*(3 if broken else .2))]
    y1=np.asarray(.5+b*x*x/2,dtype=float); y2=np.asarray(np.full_like(x,(.5*b*a*a+.5)*.35),dtype=float)
    z1=np.asarray(.5*b*x*x*(3 if broken else .2),dtype=float); z2=np.asarray(np.zeros_like(x),dtype=float)
    if y1.ndim==0: y1=np.full_like(x,float(y1))
    if y2.ndim==0: y2=np.full_like(x,float(y2))
    if z1.ndim==0: z1=np.full_like(x,float(z1))
    if z2.ndim==0: z2=np.full_like(x,float(z2))
    return {"signature":signature,"metrics":[("preupdate_position_sigma", "Preupdate Position Sigma", signature[0], "m"),("postupdate_position_sigma", "Postupdate Position Sigma", signature[1], "m"),("unmodeled_bias_error", "Unmodeled Bias Error", signature[2], "m")],"plots":{
      "response":_plot("ESKF position uncertainty propagation","Time since GNSS update (s)","Position sigma (m)",[_trace("Nominal/filtered",x,y1,"Time since GNSS update","s","Position sigma","m"),_trace("Reference/boundary",x,y2,"Time since GNSS update","s","Position sigma","m")]),
      "mechanism":_plot("Unmodeled accelerometer-bias error","Time since GNSS update (s)","Position error (m)",[_trace("Mechanism",x,z1,"Time since GNSS update","s","Position error","m"),_trace("Requirement/reference",x,z2,"Time since GNSS update","s","Position error","m")])},
      "observation":"GNSS updates reduce navigation-error covariance, while an explicit bias error state prevents systematic inertial drift from masquerading as white noise."}



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
