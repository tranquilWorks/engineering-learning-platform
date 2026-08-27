from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 13
BROKEN_TEXT = 'The broken case removes coupling between rate and position, dropping controllability rank.'
RECOVERY_TEXT = 'Disable the broken case to restore the state-to-state path.'

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
    b=float(parameters["input_gain"]); coupling=0. if broken_mode else float(parameters["coupling"]); A=np.array([[1.,.05*coupling],[0.,1.]]); B=np.array([[.5*.05**2*b],[.05*b]]); C=np.hstack([B,A@B]); rank=float(np.linalg.matrix_rank(C)); gram=sum((np.linalg.matrix_power(A,k)@B)@(np.linalg.matrix_power(A,k)@B).T for k in range(40)); eig=np.linalg.eigvalsh(gram); t=np.arange(41)*.05; reachable=b*coupling*.5*t*t
    return result(broken_mode,t,[trace("Reachable position under unit command",t,reachable),trace("Target",t,np.ones_like(t),"dash")],[trace("Controllability singular values",[1,2],np.linalg.svd(C,compute_uv=False)),trace("Gramian eigenvalues",[1,2],eig)],[("rank","Controllability rank",rank,"states"),("minimum_gramian_eigenvalue","Minimum Gramian eigenvalue",eig[0],"energy map"),("final_reachable_position","Unit-command position",reachable[-1],"m")],[b,coupling,rank,eig[0],reachable[-1]],"Rank answers possible or impossible; Gramian eigenvalues reveal whether a possible direction is still expensive.")

def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
