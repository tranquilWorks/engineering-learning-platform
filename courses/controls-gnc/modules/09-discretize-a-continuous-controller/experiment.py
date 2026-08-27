from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 9
BROKEN_TEXT = 'The broken case combines coarse sampling with the less forgiving forward-error integral update.'
RECOVERY_TEXT = 'Disable the broken case and reduce the controller sample period.'

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
    Ts=.3 if broken_mode else float(parameters["sample_period_s"]); ki=float(parameters["integral_gain"]); kp=2.; t=np.arange(0,12+Ts/2,Ts); y=np.zeros_like(t); q=np.zeros_like(t); u=np.zeros_like(t); a=np.exp(-Ts)
    for k in range(len(t)-1):
        e=1-y[k]; q[k+1]=q[k]+Ts*(q[k-1] if broken_mode and k>0 else e); u[k]=kp*e+ki*q[k]; y[k+1]=a*y[k]+(1-a)*u[k]
    u[-1]=kp*(1-y[-1])+ki*q[-1]; fine=np.linspace(0,12,1201); target=1-np.exp(-2*fine)*(np.cos(2*fine)+np.sin(2*fine))
    return result(broken_mode,t,[trace("Digital PI",t,y),trace("Continuous target",fine,target,"dash")],[trace("Held command",t,u),trace("Integral state",t,q)],[("sample_rate","Controller sample rate",1/Ts,"Hz"),("final_error","Final digital error",1-y[-1],"output"),("peak_output","Peak digital output",np.max(np.abs(y)),"output")],[Ts,ki,y[-1],np.max(np.abs(y)),np.max(np.abs(u))],"Exact plant holds do not remove controller discretization: the integral rule and sample period still move closed-loop poles.")

def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
