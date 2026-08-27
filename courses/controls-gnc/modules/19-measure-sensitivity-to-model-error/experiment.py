from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 19
BROKEN_TEXT = 'The broken case reverses actuator sign, outside the modeled positive-gain uncertainty family.'
RECOVERY_TEXT = 'Disable the broken case and validate control polarity before tuning robustness.'

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
    ga=float(parameters["actuator_gain_ratio"]); drag=float(parameters["drag_ratio"]); sign=-1 if broken_mode else 1; dt=.02; t=np.arange(0,10+dt/2,dt); nom=np.zeros_like(t); actual=np.zeros_like(t); u=np.zeros_like(t)
    for i in range(len(t)-1): u[i]=2*(1-actual[i]); nom[i+1]=nom[i]+dt*(-nom[i]+2*(1-nom[i])); actual[i+1]=actual[i]+dt*(-drag*actual[i]+sign*ga*u[i])
    gap=np.max(np.abs(actual-nom))
    return result(broken_mode,t,[trace("Nominal prediction",t,nom,"dash"),trace("Actual uncertain plant",t,actual)],[trace("Control command",t,u),trace("Prediction gap",t,actual-nom)],[("maximum_model_gap","Maximum model gap",gap,"m/s"),("final_tracking_error","Final actual error",1-actual[-1],"m/s"),("peak_control","Peak command",np.max(np.abs(u)),"command")],[ga,drag,sign,gap,actual[-1]],"Sweeping physical ratios shows which response changes are plausible model error and which indicate an invalid sign assumption.")

def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
