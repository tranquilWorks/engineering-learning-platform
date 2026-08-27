from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 1
BROKEN_TEXT = 'The broken case uses an explicit integration step too large for the fastest mode, so numerical energy grows even though the physical system is damped.'
RECOVERY_TEXT = 'Disable the broken case to restore a time step that resolves the natural period.'

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
    m=float(parameters["mass_kg"]); c=float(parameters["damping_ns_m"]); k=float(parameters["stiffness_n_m"])
    dt=0.35 if broken_mode else 0.01; t=np.arange(0.0,12.0+dt/2,dt); x=np.zeros_like(t); v=np.zeros_like(t); force=1.0
    for i in range(len(t)-1):
        a=(force-c*v[i]-k*x[i])/m; v[i+1]=v[i]+dt*a; x[i+1]=x[i]+dt*v[i+1]
    energy=.5*m*v*v+.5*k*x*x; wn=np.sqrt(k/m); zeta=c/(2*np.sqrt(k*m))
    return result(broken_mode,t,[trace("Displacement",t,x),trace("Steady F/k",t,np.full_like(t,force/k),"dash")],[trace("Velocity",x,v),trace("Energy",t,energy)],[("natural_frequency","Natural frequency",wn,"rad/s"),("damping_ratio","Damping ratio",zeta,"ratio"),("final_displacement","Final displacement",x[-1],"m")],[wn,zeta,x[-1],np.max(np.abs(x)),energy[-1]],"Mass slows acceleration, stiffness sets equilibrium and frequency, and damping removes mechanical energy.")

def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
