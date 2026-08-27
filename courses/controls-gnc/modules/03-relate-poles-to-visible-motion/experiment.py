from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 3
BROKEN_TEXT = 'The broken case reflects a stable pole into the right half-plane, turning decay into exponential growth.'
RECOVERY_TEXT = 'Disable the broken case and keep the real part negative.'

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
    sigma=float(parameters["pole_real_per_s"]); omega=float(parameters["pole_imag_rad_s"]); sigma=abs(sigma) if broken_mode else sigma; t=np.linspace(0,12,601); env=np.exp(sigma*t); x=env*np.cos(omega*t); period=2*np.pi/omega if omega>0 else 0.0
    return result(broken_mode,t,[trace("Response",t,x),trace("Envelope +",t,env,"dash"),trace("Envelope -",t,-env,"dash")],[trace("Phase portrait",x,np.gradient(x,t)),trace("Pole",[sigma],[omega])],[("decay_rate","Real part",sigma,"1/s"),("oscillation_rate","Imaginary part",omega,"rad/s"),("period","Oscillation period",period,"s")],[sigma,omega,period,x[-1],np.max(np.abs(x))],"The pole real part controls the envelope while its imaginary part controls rotation and visible oscillation.")

def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
