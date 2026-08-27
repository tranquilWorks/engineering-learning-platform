from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 10
BROKEN_TEXT = 'The broken case uses a 0.2 s period with 90 percent computation delay.'
RECOVERY_TEXT = 'Disable the broken case and schedule computation early in the sample interval.'

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
    Ts=.2 if broken_mode else float(parameters["sample_period_s"]); frac=.9 if broken_mode else float(parameters["delay_fraction"]); delay=Ts*frac; dt=.005; t=np.arange(0,4+dt/2,dt); y=np.zeros_like(t); u=np.zeros_like(t); computed=0.; previous=0.; next_sample=0.; switch=0.
    for i in range(len(t)-1):
        if t[i]+1e-12>=next_sample: previous=u[i-1] if i else 0.; computed=8*(1-y[i]); switch=t[i]+delay; next_sample+=Ts
        u[i]=previous if t[i]<switch else computed; y[i+1]=y[i]+dt*(-y[i]+u[i])
    u[-1]=u[-2]; eq=8/9
    return result(broken_mode,t,[trace("Sampled output",t,y),trace("Continuous equilibrium",t,np.full_like(t,eq),"dash")],[trace("Applied command",t,u),trace("Equilibrium error",t,y-eq)],[("sample_rate","Sample rate",1/Ts,"Hz"),("delay","Computation delay",delay,"s"),("peak_output","Peak output",np.max(y),"output")],[Ts,frac,delay,y[-1],np.max(y)],"The plant sees old command during computation; coarse sampling and latency therefore combine rather than act independently.")

def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
