from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 63
BROKEN_TEXT = 'Broken mode reverses the cross-track sign, commanding divergence from the path.'
RECOVERY_TEXT = 'Restore the frame/sign convention, select lookahead from curvature authority, and verify waypoint switching separately.'


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
    a=float(p["lookahead_distance_m"]); b=float(p["vehicle_speed_m_s"])
    if broken: a=15.0; b=8.0
    x=np.linspace(0.,10.,240)
    signature=[float(-b/a if broken else b/a),float(10*np.exp((b/a if broken else -b/a)*12)),float(np.rad2deg(np.arctan(10/a)))]
    y1=np.asarray(10*np.exp((b/a if broken else -b/a)*x),dtype=float); y2=np.asarray(np.zeros_like(x),dtype=float)
    z1=np.asarray(np.rad2deg(np.arctan((10*np.exp((b/a if broken else -b/a)*x))/a)),dtype=float); z2=np.asarray(np.zeros_like(x),dtype=float)
    if y1.ndim==0: y1=np.full_like(x,float(y1))
    if y2.ndim==0: y2=np.full_like(x,float(y2))
    if z1.ndim==0: z1=np.full_like(x,float(z1))
    if z2.ndim==0: z2=np.full_like(x,float(z2))
    return {"signature":signature,"metrics":[("cross_track_decay_rate", "Cross Track Decay Rate", signature[0], "1/s"),("terminal_cross_track_error", "Terminal Cross Track Error", signature[1], "m"),("peak_heading_command", "Peak Heading Command", signature[2], "deg")],"plots":{
      "response":_plot("LOS cross-track convergence","Time (s)","Cross-track error (m)",[_trace("Nominal/filtered",x,y1,"Time","s","Cross-track error","m"),_trace("Reference/boundary",x,y2,"Time","s","Cross-track error","m")]),
      "mechanism":_plot("LOS heading correction","Time (s)","Heading command (deg)",[_trace("Mechanism",x,z1,"Time","s","Heading command","deg"),_trace("Requirement/reference",x,z2,"Time","s","Heading command","deg")])},
      "observation":"Positive lookahead produces bounded heading commands and exponential local cross-track convergence for forward speed."}



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
