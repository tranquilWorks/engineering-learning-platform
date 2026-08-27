from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 8
BROKEN_TEXT = 'The broken case injects a 0.5-unit sensor bias with no physical disturbance.'
RECOVERY_TEXT = 'Disable the broken case and validate/calibrate the sensor bias.'

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
    K=float(parameters["feedback_gain"]); omega=float(parameters["disturbance_frequency_rad_s"]); bias=.5 if broken_mode else 0.; dt=.005; t=np.arange(0,12+dt/2,dt); y=np.zeros_like(t); d=np.where(t>=1,np.ones_like(t) if omega==0 else np.sin(omega*(t-1)),0); u=np.zeros_like(t)
    for i in range(len(t)-1): u[i]=-K*(y[i]+(bias if t[i]>=1 else 0)); y[i+1]=y[i]+dt*(-y[i]+u[i]+d[i]); u[-1]=-K*(y[-1]+bias)
    atten=1/np.sqrt((1+K)**2+omega**2)
    return result(broken_mode,t,[trace("Disturbance",t,d,"dash"),trace("True output",t,y)],[trace("Measured output",t,y+bias*(t>=1)),trace("Control effort",t,u)],[("attenuation","Theoretical disturbance gain",atten,"output/input"),("peak_output","Peak true output",np.max(np.abs(y)),"output"),("peak_control","Peak control",np.max(np.abs(u)),"actuator")],[K,omega,bias,atten,y[-1],np.max(np.abs(u))],"Feedback rejects plant disturbance through sensitivity, but a biased measurement drives a real and costly correction.")

def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
