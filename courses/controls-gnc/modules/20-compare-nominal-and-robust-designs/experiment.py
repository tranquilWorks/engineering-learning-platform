from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 20
BROKEN_TEXT = 'The broken case reverses actuator sign, violating the uncertainty set both designs assumed.'
RECOVERY_TEXT = 'Disable the broken case and restore a plant inside the certified uncertainty family.'

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
    ga=float(parameters["actuator_gain_ratio"]); drag=float(parameters["drag_ratio"]); sign=-1 if broken_mode else 1; dt=.02; t=np.arange(0,12+dt/2,dt); yn=np.zeros_like(t); yr=np.zeros_like(t); un=np.zeros_like(t); ur=np.zeros_like(t)
    for i in range(len(t)-1): un[i]=2*(1-yn[i]); ur[i]=4*(1-yr[i]); yn[i+1]=yn[i]+dt*(-drag*yn[i]+sign*ga*un[i]); yr[i+1]=yr[i]+dt*(-drag*yr[i]+sign*ga*ur[i])
    jn=np.trapezoid((1-yn)**2+.05*un**2,t); jr=np.trapezoid((1-yr)**2+.05*ur**2,t)
    return result(broken_mode,t,[trace("Nominal design K=2",t,yn),trace("Robust design K=4",t,yr)],[trace("Nominal command",t,un),trace("Robust command",t,ur)],[("nominal_cost","Nominal-design cost",jn,"cost"),("robust_cost","Robust-design cost",jr,"cost"),("robust_final_error","Robust final error",1-yr[-1],"m/s")],[ga,drag,sign,jn,jr,yr[-1]],"The robust design pays more effort to reduce response variation inside its declared gain/drag family.")

def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
