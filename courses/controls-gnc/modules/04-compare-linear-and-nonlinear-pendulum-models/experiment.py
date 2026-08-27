from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 4
BROKEN_TEXT = 'The broken case forces a 120 degree release while interpreting the small-angle trace as truth.'
RECOVERY_TEXT = 'Disable the broken case or reduce the release angle until the approximation error is acceptable.'

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
    angle=np.deg2rad(120.0 if broken_mode else float(parameters["initial_angle_deg"])); length=float(parameters["length_m"]); dt=.01; t=np.arange(0,12+dt/2,dt); nl=np.zeros_like(t); nv=np.zeros_like(t); li=np.zeros_like(t); lv=np.zeros_like(t); nl[0]=li[0]=angle; w2=9.81/length; z=.02
    for i in range(len(t)-1):
        nv[i+1]=nv[i]+dt*(-2*z*np.sqrt(w2)*nv[i]-w2*np.sin(nl[i])); nl[i+1]=nl[i]+dt*nv[i+1]
        lv[i+1]=lv[i]+dt*(-2*z*np.sqrt(w2)*lv[i]-w2*li[i]); li[i+1]=li[i]+dt*lv[i+1]
    gap=np.max(np.abs(nl-li));
    return result(broken_mode,t,[trace("Nonlinear sin(theta)",t,np.rad2deg(nl)),trace("Linear theta",t,np.rad2deg(li),"dash")],[trace("Model gap",t,np.rad2deg(nl-li)),trace("Phase portrait",np.rad2deg(nl),np.rad2deg(nv))],[("small_angle_gap","Maximum model gap",np.rad2deg(gap),"deg"),("linear_period","Linear period",2*np.pi/np.sqrt(w2),"s"),("release_angle","Release angle",np.rad2deg(angle),"deg")],[angle,length,gap,nl[-1],li[-1]],"The linear and nonlinear plants share their initial state; their divergence isolates the small-angle assumption.")

def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
