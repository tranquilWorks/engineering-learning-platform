from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 6
BROKEN_TEXT = 'The broken case applies derivative action with the wrong sign, injecting velocity instead of damping it.'
RECOVERY_TEXT = 'Disable the broken case to restore derivative damping.'

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
    ki=float(parameters["integral_gain"]); kd=float(parameters["derivative_gain"]); kd= -kd if broken_mode else kd; kp=4.; dt=.01; t=np.arange(0,20+dt/2,dt); x=np.zeros_like(t); v=np.zeros_like(t); q=np.zeros_like(t); u=np.zeros_like(t)
    for i in range(len(t)-1):
        e=1-x[i]; u[i]=kp*e+ki*q[i]-kd*v[i]; a=u[i]-1-.4*v[i]; v[i+1]=v[i]+dt*a; x[i+1]=x[i]+dt*v[i+1]; q[i+1]=q[i]+dt*e
    u[-1]=kp*(1-x[-1])+ki*q[-1]-kd*v[-1]
    return result(broken_mode,t,[trace("Position",t,x),trace("Reference",t,np.ones_like(t),"dash")],[trace("P term",t,kp*(1-x)),trace("I term",t,ki*q),trace("D term",t,-kd*v)],[("final_error","Final position error",1-x[-1],"m"),("peak_control","Peak command",np.max(np.abs(u)),"N"),("overshoot","Overshoot",max(0.,np.max(x)-1),"m")],[ki,kd,x[-1],np.max(x),np.max(np.abs(u))],"P reacts now, I remembers load error, and correctly signed D removes kinetic energy.")

def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
