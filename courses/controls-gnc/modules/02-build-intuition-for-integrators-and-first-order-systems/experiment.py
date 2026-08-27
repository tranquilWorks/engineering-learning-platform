from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 2
BROKEN_TEXT = 'The broken case uses forward Euler with dt/tau greater than two, creating a discrete pole outside the unit circle.'
RECOVERY_TEXT = 'Disable the broken case to use the exact first-order transition.'

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
    a=float(parameters["input_amplitude"]); tau=float(parameters["time_constant_s"]); t=np.linspace(0,10,501); integ=a*t
    if broken_mode:
        dt=3*tau; tb=np.arange(0,10+dt/2,dt); y=np.zeros_like(tb)
        for i in range(len(tb)-1): y[i+1]=y[i]+dt*(a-y[i])/tau
        y=np.interp(t,tb,y)
    else: y=a*(1-np.exp(-t/tau))
    return result(broken_mode,t,[trace("Integrator",t,integ),trace("First order",t,y)],[trace("First-order error",t,a-y),trace("Input",t,np.full_like(t,a))],[("ramp_slope","Integrator slope",a,"input/s"),("time_constant","Time constant",tau,"s"),("final_first_order","Final first-order output",y[-1],"output")],[a,tau,integ[-1],y[-1],np.max(np.abs(y))],"The same step becomes an unbounded ramp through an integrator and a bounded exponential through a first-order state.")

def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
