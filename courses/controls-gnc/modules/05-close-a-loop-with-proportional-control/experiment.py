from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 5
BROKEN_TEXT = 'The broken toggle reverses the measurement sign, producing positive feedback.'
RECOVERY_TEXT = 'Disable the broken case to restore subtraction at the summing junction.'

def layout(title: str, x: str, y: str) -> dict[str, Any]:
    return {"title": {"text": title, "x": 0.02}, "xaxis": {"title": x}, "yaxis": {"title": y}, "legend": {"orientation": "h"}, "margin": {"l": 62, "r": 20, "t": 55, "b": 55}, "hovermode": "closest", "uirevision": "keep-view"}

def trace(name: str, x: Any, y: Any, dash: str | None = None) -> dict[str, Any]:
    item = {"type": "scattergl", "mode": "lines", "name": name, "x": x, "y": y}
    if dash: item["line"] = {"dash": dash}
    return item

def result(broken_active: bool, t: np.ndarray, response: list[dict[str, Any]], mechanism: list[dict[str, Any]], metrics: list[tuple[str,str,float,str]], signature: list[float], observation: str) -> dict[str, Any]:
    return {
        "metrics": [{"id": key, "label": label, "value": float(value), "unit": unit, "emphasis": "primary" if i == 0 else "normal"} for i,(key,label,value,unit) in enumerate(metrics)],
        "plots": {
            "response": {"data": response, "layout": layout("Observable response", "Independent variable", "Response"), "config": {"responsive": True, "displaylogo": False}},
            "mechanism": {"data": mechanism, "layout": layout("Mechanism and diagnostic view", "Independent variable", "Diagnostic"), "config": {"responsive": True, "displaylogo": False}},
        },
        "explanations": {"observation": observation, "broken": BROKEN_TEXT, "recovery": RECOVERY_TEXT},
        "diagnostics": {"item_number": ITEM_NUMBER, "broken_active": bool(broken_active), "signature": [float(v) for v in signature]},
    }

def _simulate(parameters: dict[str, Any], broken_mode: bool) -> dict[str, Any]:
    kp=float(parameters["proportional_gain"]); tau=float(parameters["plant_time_constant_s"]); sign=1.0 if broken_mode else -1.0; dt=.01; t=np.arange(0,6+dt/2,dt); y=np.zeros_like(t); u=np.zeros_like(t)
    for i in range(len(t)-1): u[i]=kp*(1+sign*y[i]); y[i+1]=y[i]+dt*(-y[i]+u[i])/tau
    u[-1]=kp*(1+sign*y[-1]); stable=1+kp if sign<0 else 1-kp
    return result(broken_mode,t,[trace("Output",t,y),trace("Reference",t,np.ones_like(t),"dash")],[trace("Control effort",t,u),trace("Tracking error",t,1-y)],[("final_error","Final tracking error",1-y[-1],"output"),("closed_loop_rate","Signed loop rate",stable/tau,"1/s"),("peak_control","Peak control",np.max(np.abs(u)),"actuator")],[kp,tau,sign,y[-1],np.max(np.abs(y))],"Negative proportional feedback changes both response rate and equilibrium; the summing-junction sign is part of the plant model.")

def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
