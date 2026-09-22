from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 64
BROKEN_TEXT = 'Broken mode reverses closing-speed sign, steering away from the intercept geometry.'
RECOVERY_TEXT = 'Restore the frame and closing convention, apply actuator limits, and compare pursuit laws under the same target maneuver.'


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
    a=float(p["navigation_constant"]); b=float(p["target_turn_rate_deg_s"])
    if broken: a=3.5; b=12.0
    x=np.linspace(0.,10.,240)
    signature=[float(( -1 if broken else 1)*a*(.2+np.deg2rad(b))*100),float(50*(1+np.deg2rad(b)*5)/max(a-2,.2)),float(-1. if broken else 1.)]
    y1=np.asarray(50/(1+max(a-2,.2)*x),dtype=float); y2=np.asarray(50/(1+x),dtype=float)
    z1=np.asarray(( -1 if broken else 1)*a*(.2+np.deg2rad(b))*100*np.exp(-x),dtype=float); z2=np.asarray(np.full_like(x,30.),dtype=float)
    if y1.ndim==0: y1=np.full_like(x,float(y1))
    if y2.ndim==0: y2=np.full_like(x,float(y2))
    if z1.ndim==0: z1=np.full_like(x,float(z1))
    if z2.ndim==0: z2=np.full_like(x,float(z2))
    return {"signature":signature,"metrics":[("pn_acceleration_demand", "Pn Acceleration Demand", signature[0], "m/s^2"),("miss_distance_proxy", "Miss Distance Proxy", signature[1], "m"),("closing_sign", "Closing Sign", signature[2], "1")],"plots":{
      "response":_plot("Pursuit-law miss-distance proxy","Time to go (s)","Predicted miss distance (m)",[_trace("Nominal/filtered",x,y1,"Time to go","s","Predicted miss distance","m"),_trace("Reference/boundary",x,y2,"Time to go","s","Predicted miss distance","m")]),
      "mechanism":_plot("PN acceleration demand","Time to go (s)","Lateral acceleration (m/s^2)",[_trace("Mechanism",x,z1,"Time to go","s","Lateral acceleration","m/s^2"),_trace("Requirement/reference",x,z2,"Time to go","s","Lateral acceleration","m/s^2")])},
      "observation":"For a closing engagement with correct LOS-rate sign, N greater than two reduces the nonmaneuvering miss proxy while increasing acceleration demand."}



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
