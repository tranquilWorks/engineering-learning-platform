from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 21
BROKEN_TEXT = 'The broken case forces the 20 m move into 4 s, exceeding the declared speed/acceleration limits.'
RECOVERY_TEXT = 'Disable the broken case and lengthen the move until both constraints pass.'

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
    target=20. if broken_mode else float(parameters["target_position_m"]); T=4. if broken_mode else float(parameters["move_duration_s"]); t=np.linspace(0,T,501); s=t/T; x=target*(10*s**3-15*s**4+6*s**5); v=target/T*(30*s**2-60*s**3+30*s**4); a=target/T**2*(60*s-180*s**2+120*s**3); feasible=bool(np.max(np.abs(v))<=5 and np.max(np.abs(a))<=2)
    return result(broken_mode,t,[trace("Position",t,x),trace("Velocity",t,v),trace("Acceleration",t,a)],[trace("Speed limit",t,np.full_like(t,5),"dash"),trace("Acceleration limit",t,np.full_like(t,2),"dash")],[("peak_speed","Peak speed",np.max(np.abs(v)),"m/s"),("peak_acceleration","Peak acceleration",np.max(np.abs(a)),"m/s²"),("feasible","Feasible (1=yes)",float(feasible),"flag")],[target,T,np.max(np.abs(v)),np.max(np.abs(a)),float(feasible)],"The quintic guarantees smooth endpoints, but only explicit derivative checks establish actuator feasibility.")

def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
