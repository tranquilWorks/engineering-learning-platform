from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 41
BROKEN_TEXT = 'Broken mode combines the maximum rate ratio and delay with a one-frame stale read, exceeding the declared coherent age bound.'
RECOVERY_TEXT = 'Use an explicit hold/buffer handoff, timestamp every sample, and include execution delay in the phase-margin budget.'


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
    ratio=int(20 if broken else round(float(p["rate_ratio"]))); delay=(.08 if broken else float(p["execution_delay_ms"])/1000); dt=.01; t=np.arange(0,8,dt); f=.7; desired=np.sin(2*np.pi*f*t); slow=np.arange(0,len(t),ratio); held=np.repeat(desired[slow],ratio)[:len(t)]; ticks=round(delay/dt)+(ratio if broken else 0); applied=np.concatenate([np.zeros(ticks),held[:len(t)-ticks]]) if ticks else held.copy(); age=(np.arange(len(t))%ratio)*dt+delay+(ratio*dt if broken else 0)
    hold=float(np.sqrt(np.mean((held-desired)**2))); phase=float(360*f*delay); max_age=float(np.max(age))
    return {"signature":[hold,phase,max_age],"metrics":[("hold_error","Zero-order-hold RMS error",hold,"1"),("delay_phase","Execution-delay phase lag",phase,"deg"),("data_age","Maximum data age",max_age,"s")],
      "plots":{"response":_plot("Desired and applied multirate command","Time (s)","Normalized command (1)",[_trace("Desired command",t,desired,"Time","s","Normalized command","1"),_trace("Applied command",t,applied,"Time","s","Normalized command","1")]),
      "mechanism":_plot("Timestamp-derived data age","Time (s)","Command age (s)",[_trace("Data age",t,age,"Time","s","Command age","s"),_trace("Coherent bound",t,np.full_like(t,ratio*dt+delay),"Time","s","Command age","s")])},"observation":"Rate hold and execution delay are distinct latency sources; timestamps make their combined age observable."}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
