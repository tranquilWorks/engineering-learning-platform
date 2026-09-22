from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 38
BROKEN_TEXT = 'Broken mode reverses observer injection, placing an estimation-error pole in the right half-plane despite a stable regulator.'
RECOVERY_TEXT = 'Restore the innovation sign, keep the observer faster but not arbitrarily ill-conditioned, and check the full augmented spectrum.'


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
    bw=float(p["regulator_bandwidth_per_s"]); ratio=float(p["observer_speed_ratio"]); A=np.array([[0.,1.],[0.,0.]]); B=np.array([[0.],[1.]]); C=np.array([[1.,0.]])
    K=np.array([[bw*bw,2*bw]]); ow=bw*ratio; L=np.array([[2*ow],[ow*ow]]); L=-L if broken else L
    reg=np.linalg.eigvals(A-B@K); obs=np.linalg.eigvals(A-L@C); aug=np.block([[A-B@K,B@K],[np.zeros((2,2)),A-L@C]]); combined=np.linalg.eigvals(aug)
    union=np.concatenate([reg,obs]); sep=float(np.max(abs(np.sort_complex(combined)-np.sort_complex(union)))); t=np.linspace(0,6/max(bw,.1),240)
    reg_env=np.exp(np.max(reg.real)*t); obs_env=np.exp(np.max(obs.real)*t)
    return {"signature":[float(np.max(reg.real)),float(np.max(obs.real)),sep],"metrics":[("regulator","Regulator spectral abscissa",np.max(reg.real),"1/s"),("observer","Observer-error spectral abscissa",np.max(obs.real),"1/s"),("separation","Separation spectrum error",sep,"1/s")],
      "plots":{"response":_plot("Regulator and observer modal envelopes","Time (s)","Normalized error envelope (1)",[_trace("Regulator envelope",t,reg_env,"Time","s","Normalized error envelope","1"),_trace("Observer envelope",t,obs_env,"Time","s","Normalized error envelope","1")]),
      "mechanism":_plot("Separated closed-loop eigenvalues","Eigenvalue real part (1/s)","Eigenvalue imaginary part (1/s)",[_trace("Regulator poles",reg.real,reg.imag,"Eigenvalue real part","1/s","Eigenvalue imaginary part","1/s",mode="markers"),_trace("Observer poles",obs.real,obs.imag,"Eigenvalue real part","1/s","Eigenvalue imaginary part","1/s",mode="markers")])},"observation":"The block-triangular augmented model exposes the separation spectrum; the innovation sign still determines observer stability."}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
