from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 43
BROKEN_TEXT = 'Broken mode makes damping negative, so the energy derivative becomes positive and the phase spiral expands.'
RECOVERY_TEXT = 'Restore positive dissipation and verify both local eigenvalues and global energy decrease.'


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
    a=float(p["damping_per_s"]); b=float(p["initial_energy"])
    if broken: a=-0.18; b=1.8
    x=np.linspace(0.,10.,240)
    signature=[float(-a*b),float(np.sqrt(b)*np.exp(-a*8)),float(-a/2)]
    y1=np.asarray(np.sqrt(2*b)*np.exp(-a*x)*np.cos(x),dtype=float); y2=np.asarray(-np.sqrt(2*b)*np.exp(-a*x)*np.sin(x),dtype=float)
    z1=np.asarray(b*np.exp(-2*a*x),dtype=float); z2=np.asarray(-a*b*np.exp(-2*a*x),dtype=float)
    if y1.ndim==0: y1=np.full_like(x,float(y1))
    if y2.ndim==0: y2=np.full_like(x,float(y2))
    if z1.ndim==0: z1=np.full_like(x,float(z1))
    if z2.ndim==0: z2=np.full_like(x,float(z2))
    return {"signature":signature,"metrics":[("energy_decay_rate", "Energy Decay Rate", signature[0], "W"),("terminal_radius", "Terminal Radius", signature[1], "1"),("local_decay_rate", "Local Decay Rate", signature[2], "1/s")],"plots":{
      "response":_plot("Phase-plane trajectory","Position (m)","Velocity (m/s)",[_trace("Nominal/filtered",x,y1,"Position","m","Velocity","m/s"),_trace("Reference/boundary",x,y2,"Position","m","Velocity","m/s")]),
      "mechanism":_plot("Energy dissipation","Time (s)","Energy rate (W)",[_trace("Mechanism",x,z1,"Time","s","Energy rate","W"),_trace("Requirement/reference",x,z2,"Time","s","Energy rate","W")])},
      "observation":"Positive damping makes energy nonincreasing even when a local linearization does not describe the full basin."}



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
