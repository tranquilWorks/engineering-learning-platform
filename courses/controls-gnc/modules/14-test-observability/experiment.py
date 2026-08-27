from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 14
BROKEN_TEXT = 'The broken case measures rate only, so initial position never appears in the output.'
RECOVERY_TEXT = 'Disable the broken case to measure position and restore full observability.'

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
    g=float(parameters["sensor_gain"]); window=float(parameters["observation_window_s"]); rate_only=broken_mode; dt=.05; t=np.arange(0,window+dt/2,dt); x0=.8; v0=.6; y=g*(np.full_like(t,v0) if rate_only else x0+v0*t); O=np.array([[0,g],[0,g]]) if rate_only else np.array([[g,0],[g,g*dt]]); rank=float(np.linalg.matrix_rank(O)); fit=np.polyfit(t,y,1) if len(t)>1 else [0,y[0]]; inferred_v=0. if rate_only else fit[0]/max(g,1e-12)
    return result(broken_mode,t,[trace("Measurement history",t,y),trace("Position truth",t,x0+v0*t,"dash")],[trace("Observability singular values",[1,2],np.linalg.svd(O,compute_uv=False)),trace("Reconstructed rate",t,np.full_like(t,inferred_v))],[("rank","Observability rank",rank,"states"),("inferred_rate","Inferred initial rate",inferred_v,"m/s"),("measurement_span","Measurement span",np.ptp(y),"measurement")],[g,window,float(rate_only),rank,inferred_v,np.ptp(y)],"A measurement must vary with each state direction over time; sensor gain alone cannot create a missing direction.")

def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
