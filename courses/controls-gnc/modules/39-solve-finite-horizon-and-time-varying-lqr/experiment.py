from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 39
BROKEN_TEXT = 'Broken mode marches the terminal condition forward from the initial time, violating the boundary-value problem and producing the wrong initial gain.'
RECOVERY_TEXT = 'Restore backward integration from the actual terminal boundary and verify P(tf)=Sf before interpreting the gain schedule.'


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
    horizon=float(p["horizon_s"]); terminal=float(p["terminal_weight"]); n=500; t=np.linspace(0,horizon,n); dt=t[1]-t[0]; P=np.zeros(n); P[-1 if not broken else 0]=terminal
    if broken:
        for k in range(n-1):
            A=.25*np.sin(2*np.pi*t[k]/horizon); P[k+1]=np.clip(P[k]+dt*(-2*A*P[k]+P[k]**2-1),-50,50)
    else:
        for k in range(n-1,0,-1):
            A=.25*np.sin(2*np.pi*t[k]/horizon); P[k-1]=P[k]+dt*(2*A*P[k]-P[k]**2+1)
    P=np.clip(P,-50,50); terminal_actual=float(P[-1]); initial=float(P[0]); maximum=float(np.max(abs(P)))
    return {"signature":[initial,terminal_actual,maximum],"metrics":[("initial_gain","Initial feedback gain",initial,"1/s"),("terminal_value","Terminal Riccati value",terminal_actual,"1"),("maximum_value","Maximum Riccati magnitude",maximum,"1")],
      "plots":{"response":_plot("Finite-horizon Riccati solution","Time (s)","Riccati value (1)",[_trace("P(t)",t,P,"Time","s","Riccati value","1"),_trace("Terminal weight",t,np.full_like(t,terminal),"Time","s","Riccati value","1")]),
      "mechanism":_plot("Time-varying feedback schedule","Time (s)","Feedback gain (1/s)",[_trace("K(t)",t,P,"Time","s","Feedback gain","1/s"),_trace("Zero gain",t,np.zeros_like(t),"Time","s","Feedback gain","1/s")])},"observation":"The terminal boundary propagates backward into earlier decisions; a forward march solves a different problem."}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
