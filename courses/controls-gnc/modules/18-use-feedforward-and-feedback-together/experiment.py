from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 18
BROKEN_TEXT = 'The broken case reverses feedforward sign, commanding acceleration away from the plan.'
RECOVERY_TEXT = 'Disable the broken case and verify inverse-model sign conventions.'

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
    ff=float(parameters["feedforward_scale"]); fb=float(parameters["feedback_scale"]); sign=-1 if broken_mode else 1; dt=.02; t=np.arange(0,12+dt/2,dt); xd=np.sin(.5*t); vd=.5*np.cos(.5*t); ad=-.25*np.sin(.5*t); x=np.zeros_like(t); v=np.zeros_like(t); u=np.zeros_like(t); d=np.where(t>=6,-.4,0.)
    for i in range(len(t)-1): u[i]=sign*ff*ad[i]+fb*(4*(xd[i]-x[i])+3*(vd[i]-v[i])); v[i+1]=v[i]+dt*(u[i]+d[i]); x[i+1]=x[i]+dt*v[i+1]
    err=xd-x; rms=np.sqrt(np.mean(err*err))
    return result(broken_mode,t,[trace("Desired position",t,xd,"dash"),trace("Actual position",t,x)],[trace("Feedforward term",t,sign*ff*ad),trace("Feedback correction",t,u-sign*ff*ad),trace("Disturbance",t,d)],[("tracking_rmse","Tracking RMSE",rms,"m"),("peak_control","Peak command",np.max(np.abs(u)),"m/s²"),("final_error","Final tracking error",err[-1],"m")],[ff,fb,sign,rms,np.max(np.abs(u))],"Feedforward handles modeled demand before error appears; feedback remains the channel for mismatch and disturbance.")

def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
