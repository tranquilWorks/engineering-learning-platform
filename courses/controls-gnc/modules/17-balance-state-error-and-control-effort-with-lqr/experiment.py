from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 17
BROKEN_TEXT = 'The broken case sets actuator effectiveness to zero, so a valid design model cannot move the plant.'
RECOVERY_TEXT = 'Disable the broken case and verify actuator authority before applying the gain.'

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
    qw=float(parameters["position_weight"]); rw=float(parameters["control_weight"]); eff=0. if broken_mode else 1.; dt=.02; A=np.array([[1,dt],[0,1-.4*dt]]); B=np.array([[.5*dt*dt*eff],[dt*eff]]); Q=np.diag([qw,1.]); R=np.array([[rw]])
    if eff==0: K=np.zeros((1,2))
    else:
        P=Q.copy()
        for _ in range(500):
            Pn=A.T@P@A-A.T@P@B@np.linalg.solve(R+B.T@P@B,B.T@P@A)+Q
            if np.max(np.abs(Pn-P))<1e-12: P=Pn; break
            P=Pn
        K=np.linalg.solve(R+B.T@P@B,B.T@P@A)
    t=np.arange(0,12+dt/2,dt); x=np.zeros((len(t),2)); x[0]=[1,0]; u=np.zeros(len(t))
    for i in range(len(t)-1): u[i]=(-K@x[i]).item(); x[i+1]=A@x[i]+B[:,0]*u[i]
    cost=np.trapezoid(qw*x[:,0]**2+x[:,1]**2+rw*u*u,t)
    return result(broken_mode,t,[trace("Position",t,x[:,0]),trace("Velocity",t,x[:,1])],[trace("Control effort",t,u),trace("State norm",t,np.linalg.norm(x,axis=1))],[("gain_position","Position gain",K[0,0],"command/m"),("peak_control","Peak command",np.max(np.abs(u)),"command"),("quadratic_cost","Realized cost",cost,"cost")],[qw,rw,eff,K[0,0],np.max(np.abs(u)),cost],"LQR does not mean aggressive by default; Q and R explicitly declare what the optimum should value.")

def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
