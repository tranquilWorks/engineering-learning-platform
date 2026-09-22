from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 42
BROKEN_TEXT = 'Broken mode disables tracking initialization and back-calculation, producing a mode-switch bump and a long saturated recovery.'
RECOVERY_TEXT = 'Initialize the integral state from the actual manual actuator command and restore back-calculation before enabling automatic control.'


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
    kaw=0. if broken else float(p["antiwindup_gain_per_s"]); limit=float(p["actuator_limit"]); dt=.01; t=np.arange(0,12,dt); switch=300; x=np.zeros_like(t); u=np.zeros_like(t); z=0.; manual=.7; kp=2.; ki=1.2
    for k in range(len(t)-1):
        ref=2. if t[k]<7 else .2; e=ref-x[k]
        if k<switch: u[k]=manual
        else:
            if k==switch and not broken: z=manual-kp*e
            raw=kp*e+z; u[k]=np.clip(raw,-limit,limit); z+=dt*(ki*e+kaw*(u[k]-raw))
        x[k+1]=x[k]+dt*(-x[k]+u[k])
    u[-1]=u[-2]; bump=abs(u[switch]-u[switch-1]); tail=np.where(abs(x[int(7/dt):]-.2)<.04)[0]; recovery=float(tail[0]*dt if len(tail) else 5.); peak=float(abs(z)) if broken else float(np.max(abs(u)))
    return {"signature":[float(bump),recovery,peak],"metrics":[("bump","Manual-to-auto command bump",bump,"1"),("recovery","Post-saturation recovery time",recovery,"s"),("integrator","Peak integral-state proxy",peak,"1")],
      "plots":{"response":_plot("Bumpless PI mode transfer","Time (s)","Plant output (1)",[_trace("Plant output",t,x,"Time","s","Plant output","1"),_trace("Reference",t,np.where(t<7,2.,.2),"Time","s","Plant output","1")]),
      "mechanism":_plot("Saturated actuator command","Time (s)","Actuator command (1)",[_trace("Applied command",t,u,"Time","s","Actuator command","1"),_trace("Positive limit",t,np.full_like(t,limit),"Time","s","Actuator command","1")])},"observation":"Tracking addresses the instant of transfer; back-calculation addresses the saturated interval that follows."}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
