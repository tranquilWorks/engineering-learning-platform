from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 37
BROKEN_TEXT = 'Broken mode disconnects the integral state while retaining the load, leaving the proportional servo with a visible steady bias.'
RECOVERY_TEXT = 'Reconnect integral augmentation, verify the command limit exceeds the load, and wait for the error and integrator derivative to settle.'


def _trace(name: str, x: Any, y: Any, x_quantity: str, x_unit: str,
           y_quantity: str, y_unit: str, *, mode: str = "lines") -> dict[str, Any]:
    return {
        "type": "scattergl", "mode": mode, "name": name,
        "x": np.asarray(x, dtype=float), "y": np.asarray(y, dtype=float),
        "meta": {"x_quantity": x_quantity, "x_unit": x_unit,
                 "y_quantity": y_quantity, "y_unit": y_unit},
    }


def _plot(title: str, x_title: str, y_title: str,
          traces: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "data": traces,
        "layout": {
            "title": {"text": title, "x": 0.02},
            "xaxis": {"title": {"text": x_title}},
            "yaxis": {"title": {"text": y_title}},
            "legend": {"orientation": "h"},
            "margin": {"l": 72, "r": 36, "t": 62, "b": 62},
            "hovermode": "closest", "uirevision": "keep-view",
        },
        "config": {"responsive": True, "displaylogo": False},
    }


def _result(model: dict[str, Any], broken: bool) -> dict[str, Any]:
    return {
        "metrics": [
            {"id": key, "label": label, "value": float(value), "unit": unit,
              "emphasis": "primary" if index == 0 else "normal"}
            for index, (key, label, value, unit) in enumerate(model["metrics"])
        ],
        "plots": model["plots"],
        "explanations": {
            "observation": model["observation"],
            "broken": BROKEN_TEXT,
            "recovery": RECOVERY_TEXT,
        },
        "diagnostics": {
            "item_number": ITEM_NUMBER,
            "broken_active": bool(broken),
            "signature": [float(value) for value in model["signature"]],
        },
    }

def _model(p: dict[str, Any], broken: bool) -> dict[str, Any]:
    ki=0. if broken else float(p["integral_gain_per_s"]); limit=float(p["command_limit_m_s2"]); dt=.01; t=np.arange(0,14,dt); x=np.zeros_like(t); z=0.; u=np.zeros_like(t); load=-.6
    for k in range(len(t)-1):
        e=1-x[k]; z+=dt*e; u[k]=np.clip(2*e+ki*z,-limit,limit); x[k+1]=x[k]+dt*(-x[k]+u[k]+load)
    u[-1]=u[-2]; steady=float(abs(1-np.mean(x[-100:]))); sat=float(np.mean(abs(u)>=limit-1e-9)); peak=float(np.max(abs(u)))
    return {"signature":[steady,peak,sat],"metrics":[("steady_error","Steady position error",steady,"m"),("peak_command","Peak command",peak,"m/s^2"),("saturation","Saturation fraction",sat,"1")],
      "plots":{"response":_plot("Integral-servo load rejection","Time (s)","Position (m)",[_trace("Plant position",t,x,"Time","s","Position","m"),_trace("Reference",t,np.ones_like(t),"Time","s","Position","m")]),
      "mechanism":_plot("Limited servo command","Time (s)","Command acceleration (m/s^2)",[_trace("Limited command",t,u,"Time","s","Command acceleration","m/s^2"),_trace("Positive limit",t,np.full_like(t,limit),"Time","s","Command acceleration","m/s^2")])},"observation":"Integral action removes a feasible constant-load bias, while the saturation fraction reveals the authority and transient cost."}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
