from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 15
BROKEN_TEXT = 'The broken case introduces a persistent 0.15 m measurement bias.'
RECOVERY_TEXT = 'Disable the broken case and correct the sensor bias before trusting the state estimate.'

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
    speed=float(parameters["observer_speed_per_s"]); bias=.15 if broken_mode else float(parameters["sensor_bias_m"]); dt=.02; t=np.arange(0,8+dt/2,dt); x=np.zeros((len(t),2)); x[0]=[.8,-.1]; xh=np.zeros_like(x); xh[0]=[-.4,.4]; L=np.array([2*speed,speed**2])
    for i in range(len(t)-1):
        u=.4; x[i+1]=x[i]+dt*np.array([x[i,1],u]); innovation=x[i,0]+bias-xh[i,0]; xh[i+1]=xh[i]+dt*(np.array([xh[i,1],u])+L*innovation)
    err=x-xh; rms=np.sqrt(np.mean(err[:,0]**2))
    return result(broken_mode,t,[trace("True position",t,x[:,0]),trace("Estimated position",t,xh[:,0],"dash")],[trace("Position error",t,err[:,0]),trace("Rate error",t,err[:,1])],[("position_rmse","Position RMSE",rms,"m"),("final_position_error","Final position error",err[-1,0],"m"),("final_rate_error","Final rate error",err[-1,1],"m/s")],[speed,bias,rms,err[-1,0],err[-1,1]],"The innovation drives both estimated states; persistent sensor bias therefore becomes persistent state-estimate bias.")

def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
