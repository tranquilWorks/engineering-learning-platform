from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 11
BROKEN_TEXT = 'The broken case restricts a 1.5-unit request to 0.6 actuator units.'
RECOVERY_TEXT = 'Disable the broken case or reduce the command to fit available authority.'

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
    r=1.5 if broken_mode else float(parameters["reference"]); limit=.6 if broken_mode else float(parameters["actuator_limit"]); dt=.01; t=np.arange(0,6+dt/2,dt); y=np.zeros_like(t); req=np.zeros_like(t); applied=np.zeros_like(t)
    for i in range(len(t)-1): req[i]=4*(r-y[i]); applied[i]=np.clip(req[i],-limit,limit); y[i+1]=y[i]+dt*(-y[i]+applied[i])
    req[-1]=4*(r-y[-1]); applied[-1]=np.clip(req[-1],-limit,limit); sat=np.mean(np.abs(req-applied)>1e-12)
    return result(broken_mode,t,[trace("Limited output",t,y),trace("Reference",t,np.full_like(t,r),"dash")],[trace("Requested",t,req,"dash"),trace("Applied",t,applied)],[("saturation_fraction","Time saturated",100*sat,"%"),("final_error","Final error",r-y[-1],"output"),("peak_request","Peak requested command",np.max(np.abs(req)),"actuator")],[r,limit,sat,y[-1],np.max(np.abs(req))],"The clipping gap is a physical statement: requested control is not applied control.")

def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
