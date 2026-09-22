from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 35
BROKEN_TEXT = 'Broken mode forces a 0.6-second Euler step for a -3 per-second pole, making the discrete Euler pole cross outside the unit circle.'
RECOVERY_TEXT = 'Reduce the sample period or use a stability-preserving mapping, then place the antialias boundary before sampling.'


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
    T=.6 if broken else float(p["sample_period_s"]); f=float(p["input_frequency_hz"]); a=-3.; fs=1/T
    zoh=np.exp(a*T); tustin=(1+a*T/2)/(1-a*T/2); euler=1+a*T; alias=abs(((f+fs/2)%fs)-fs/2)
    periods=np.linspace(.005,.65,240); zoh_curve=np.exp(a*periods); euler_curve=1+a*periods
    n=np.arange(80); samples=np.sin(2*np.pi*f*n*T); alias_samples=np.sin(2*np.pi*alias*n*T)*np.sign(np.corrcoef(samples,np.sin(2*np.pi*alias*n*T))[0,1] or 1)
    return {"signature":[abs(zoh-np.exp(a*T)),abs(euler-zoh),alias],"metrics":[("zoh_error","ZOH pole error",abs(zoh-np.exp(a*T)),"1"),("euler_error","Euler versus exact pole error",abs(euler-zoh),"1"),("alias","Nyquist-folded frequency",alias,"Hz")],
      "plots":{"response":_plot("Discrete pole mappings","Sample period (s)","Discrete pole magnitude (1)",[_trace("Exact ZOH",periods,abs(zoh_curve),"Sample period","s","Discrete pole magnitude","1"),_trace("Explicit Euler",periods,abs(euler_curve),"Sample period","s","Discrete pole magnitude","1")]),
      "mechanism":_plot("Original and aliased sampled tone","Sample time (s)","Sample amplitude (1)",[_trace("Original samples",n*T,samples,"Sample time","s","Sample amplitude","1",mode="lines+markers"),_trace("Alias-equivalent samples",n*T,alias_samples,"Sample time","s","Sample amplitude","1",mode="lines+markers")])},"observation":f"At T_s={T:.3f} s the exact, Tustin, and Euler poles are {zoh:.3f}, {tustin:.3f}, and {euler:.3f}; the tone folds to {alias:.3f} Hz."}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
