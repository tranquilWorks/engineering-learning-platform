from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 22
BROKEN_TEXT = 'The broken case limits lateral acceleration to 5 m/s², preventing intercept in the modeled engagement.'
RECOVERY_TEXT = 'Disable the broken case and restore the 80 m/s² authority used by the baseline.'

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
    N=float(parameters["navigation_constant"]); limit=5. if broken_mode else float(parameters["maximum_acceleration_m_s2"]); dt=.02; steps=int(25/dt)+1; t=np.arange(steps)*dt; p=np.array([0.,0.]); heading=0.; speed=300.; target=np.array([5000.,600.]); tv=np.array([-60.,0.]); rng=np.zeros(steps); accel=np.zeros(steps); los=np.zeros(steps); hit=False; end=steps
    for i in range(steps):
        rel=target-p; rng[i]=np.linalg.norm(rel); los[i]=np.arctan2(rel[1],rel[0]);
        if rng[i]<5: hit=True; end=i+1; break
        iv=speed*np.array([np.cos(heading),np.sin(heading)]); rv=tv-iv; closing=-np.dot(rel,rv)/max(rng[i],1e-9); rate=(rel[0]*rv[1]-rel[1]*rv[0])/max(rng[i]**2,1e-9); accel[i]=np.clip(N*closing*rate,-limit,limit); heading+=dt*accel[i]/speed; p+=dt*speed*np.array([np.cos(heading),np.sin(heading)]); target+=dt*tv
    t=t[:end]; rng=rng[:end]; accel=accel[:end]; los=los[:end]; miss=np.min(rng)
    return result(broken_mode,t,[trace("Range",t,rng),trace("LOS angle",t,np.degrees(los))],[trace("Lateral acceleration",t,accel),trace("Acceleration limit",t,np.full_like(t,limit),"dash")],[("miss_distance","Minimum range",miss,"m"),("intercept","Intercept (1=yes)",float(hit),"flag"),("peak_acceleration","Peak lateral acceleration",np.max(np.abs(accel)),"m/s²")],[N,limit,miss,float(hit),np.max(np.abs(accel))],"PN steers by cancelling line-of-sight rotation; acceleration clipping reveals whether the geometry is physically achievable.")

def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
