from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 7
BROKEN_TEXT = 'The broken case keeps K=4 while exposing a 0.5 s actuator lag omitted by the optimistic design.'
RECOVERY_TEXT = 'Disable the broken case or lower loop gain until both margins are positive.'

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
    K=4.0 if broken_mode else float(parameters["loop_gain"]); tau=.5 if broken_mode else float(parameters["actuator_lag_s"]); dt=.005; t=np.arange(0,20+dt/2,dt); y=np.zeros_like(t); v=np.zeros_like(t); a=np.zeros_like(t)
    for i in range(len(t)-1):
        cmd=K*(1-y[i]); da=(cmd-a[i])/max(tau,dt/10) if tau>0 else 0; a[i+1]=cmd if tau==0 else a[i]+dt*da; v[i+1]=v[i]+dt*(a[i]-v[i]); y[i+1]=y[i]+dt*v[i]
    w=np.logspace(-2,2,300); mag=K/(w*np.sqrt(1+w*w)*np.sqrt(1+(tau*w)**2)); phase=-90-np.degrees(np.arctan(w))-np.degrees(np.arctan(tau*w)); idx=int(np.argmin(np.abs(20*np.log10(mag)))); pm=180+phase[idx]
    return result(broken_mode,t,[trace("Output",t,y),trace("Reference",t,np.ones_like(t),"dash")],[trace("Open-loop magnitude",w,20*np.log10(mag)),trace("Open-loop phase",w,phase)],[("phase_margin","Approx. phase margin",pm,"deg"),("crossover","Gain crossover",w[idx],"rad/s"),("peak_output","Peak output",np.max(np.abs(y)),"output")],[K,tau,pm,w[idx],np.max(np.abs(y))],"The same actuator pole that adds time-domain ringing removes phase reserve near gain crossover.")

def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
