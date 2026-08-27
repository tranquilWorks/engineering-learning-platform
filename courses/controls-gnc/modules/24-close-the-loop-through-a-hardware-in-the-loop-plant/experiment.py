from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 24
BROKEN_TEXT = 'The broken case drops every second command with a 0.1 s controller period, 0.04 s one-way latency, and 0.12 s watchdog.'
RECOVERY_TEXT = 'Disable the broken case to restore fresh commands. This is a software-only virtual protocol/plant lesson; it does not claim physical HIL execution.'

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
    period=.1 if broken_mode else float(parameters["controller_period_s"]); latency=.04 if broken_mode else float(parameters["one_way_latency_s"]); watchdog=.12 if broken_mode else .2; drop=2 if broken_mode else 0; dt=.01; t=np.arange(0,8+dt/2,dt); y=np.zeros_like(t); v=np.zeros_like(t); u=np.zeros_like(t); age=np.zeros_like(t); arrivals=[]; applied=0.; last_arrival=-1e9; seq=0; next_control=0.; watchdog_count=0
    for i in range(len(t)-1):
        if t[i]+1e-12>=next_control: seq+=1; cmd=6*(1-y[i])-4*v[i];
        else: cmd=None
        if cmd is not None:
            if not drop or seq%drop: arrivals.append((t[i]+latency,cmd))
            next_control+=period
        while arrivals and arrivals[0][0]<=t[i]+1e-12: _,applied=arrivals.pop(0); last_arrival=t[i]
        age[i]=t[i]-last_arrival if last_arrival>-1 else watchdog+1
        if age[i]>watchdog: applied=0.; watchdog_count+=1
        u[i]=applied; v[i+1]=v[i]+dt*(u[i]-.5*v[i])/1.5; y[i+1]=y[i]+dt*v[i+1]
    u[-1]=u[-2]; age[-1]=age[-2]
    return result(broken_mode,t,[trace("Virtual plant position",t,y),trace("Reference",t,np.ones_like(t),"dash")],[trace("Applied command",t,u),trace("Command age",t,age),trace("Watchdog timeout",t,np.full_like(t,watchdog),"dash")],[("final_error","Final virtual-plant error",1-y[-1],"m"),("maximum_command_age","Maximum finite command age",np.max(np.minimum(age,watchdog*2)),"s"),("watchdog_fraction","Watchdog-active samples",watchdog_count/len(t),"ratio")],[period,latency,watchdog,float(drop),y[-1],watchdog_count/len(t)],"Timestamped delivery, loss, and a fail-zero watchdog are exercised entirely in software; no physical hardware execution is claimed.")

def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
