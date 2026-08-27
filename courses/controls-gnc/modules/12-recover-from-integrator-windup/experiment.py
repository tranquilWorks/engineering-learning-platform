from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 12
BROKEN_TEXT = 'The broken case reverses the back-calculation sign and drives the integrator farther into windup.'
RECOVERY_TEXT = 'Disable the broken case to feed the saturation gap back with the corrective sign.'

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
    kaw=float(parameters["anti_windup_gain"]); duration=float(parameters["demand_duration_s"]); sign=-1 if broken_mode else 1; dt=.01; t=np.arange(0,10+dt/2,dt); ref=np.where(t<duration,2.,-.5); y=np.zeros_like(t); q=np.zeros_like(t); raw=np.zeros_like(t); u=np.zeros_like(t)
    for i in range(len(t)-1): raw[i]=2*(ref[i]-y[i])+q[i]; u[i]=np.clip(raw[i],-1,1); q[i+1]=q[i]+dt*((ref[i]-y[i])+sign*kaw*(u[i]-raw[i])); y[i+1]=y[i]+dt*(-y[i]+u[i])
    raw[-1]=2*(ref[-1]-y[-1])+q[-1]; u[-1]=np.clip(raw[-1],-1,1); post=t>=duration; rec=np.trapezoid(np.abs(ref[post]-y[post]),t[post])
    return result(broken_mode,t,[trace("Output",t,y),trace("Reference",t,ref,"dash")],[trace("Raw command",t,raw,"dash"),trace("Saturated command",t,u),trace("Integral state",t,q)],[("recovery_error_area","Post-demand error area",rec,"output s"),("peak_integrator","Peak integral state",np.max(np.abs(q)),"state"),("final_error","Final error",ref[-1]-y[-1],"output")],[kaw,duration,sign,rec,np.max(np.abs(q))],"Back-calculation uses the saturation gap to keep the controller's internal state consistent with applied authority.")

def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
