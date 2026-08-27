from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 16
BROKEN_TEXT = 'The broken case injects one unvalidated 4 m position outlier.'
RECOVERY_TEXT = 'Disable the broken case; in production, gate innovations before applying the update.'

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
    rstd=float(parameters["assumed_sensor_noise_m"]); qstd=float(parameters["assumed_process_noise_m_s2"]); outlier=4. if broken_mode else 0.; dt=.05; t=np.arange(0,20+dt/2,dt); rng=np.random.default_rng(1601); truth=np.column_stack([.4*t+.8*np.sin(.25*t),.4+.2*np.cos(.25*t)]); z=truth[:,0]+rng.normal(0,.35,len(t)); z[len(t)//2]+=outlier; F=np.array([[1,dt],[0,1]]); H=np.array([[1.,0.]]); Q=qstd**2*np.array([[dt**4/4,dt**3/2],[dt**3/2,dt**2]]); R=rstd**2; est=np.zeros_like(truth); P=np.eye(2)
    for i in range(1,len(t)):
        xp=F@est[i-1]; Pp=F@P@F.T+Q; innov=z[i]-(H@xp).item(); K=(Pp@H.T/((H@Pp@H.T).item()+R)).ravel(); est[i]=xp+K*innov; P=(np.eye(2)-np.outer(K,H.ravel()))@Pp
    rmse=np.sqrt(np.mean((truth[:,0]-est[:,0])**2))
    return result(broken_mode,t,[trace("True position",t,truth[:,0]),trace("Measured position",t,z,"dot"),trace("Kalman estimate",t,est[:,0])],[trace("Position error",t,truth[:,0]-est[:,0]),trace("Velocity estimate",t,est[:,1])],[("position_rmse","Position RMSE",rmse,"m"),("maximum_innovation_proxy","Largest measurement residual",np.max(np.abs(z-est[:,0])),"m"),("final_velocity","Final velocity estimate",est[-1,1],"m/s")],[rstd,qstd,outlier,rmse,est[-1,1]],"The filter is deterministic here: a fixed noise record lets the covariance assumptions be the only swept levers.")

def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
