from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 23
BROKEN_TEXT = 'The broken case combines slow actuator/sensor dynamics with a command that reverses every 0.1 s.'
RECOVERY_TEXT = 'Disable the broken case and slow the command or increase component bandwidth.'

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
    ta=.8 if broken_mode else float(parameters["actuator_time_constant_s"]); ts=.6 if broken_mode else float(parameters["sensor_time_constant_s"]); half=.1 if broken_mode else 2.; dt=.01; t=np.arange(0,8+dt/2,dt); cmd=20*np.where((np.floor(t/half)%2)==0,1,-1); act=np.zeros_like(t); sense=np.zeros_like(t)
    for i in range(len(t)-1): act[i+1]=act[i]+(1-np.exp(-dt/ta))*(np.clip(cmd[i],-30,30)-act[i]); sense[i+1]=sense[i]+(1-np.exp(-dt/ts))*(act[i]-sense[i])
    lag=np.sqrt(np.mean((cmd-sense)**2))
    return result(broken_mode,t,[trace("Command",t,cmd,"dash"),trace("Actuator",t,act),trace("Sensor",t,sense)],[trace("Actuator error",t,cmd-act),trace("Sensor lag error",t,act-sense)],[("chain_rmse","Command-to-sensor RMSE",lag,"units"),("actuator_bandwidth","Actuator bandwidth",1/ta,"rad/s"),("sensor_bandwidth","Sensor bandwidth",1/ts,"rad/s")],[ta,ts,half,lag,act[-1],sense[-1]],"Two first-order components create two distinct lag states; plotting both prevents sensor delay from being mistaken for actuator failure.")

def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
