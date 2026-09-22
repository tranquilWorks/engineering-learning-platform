from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 34
BROKEN_TEXT = 'Broken mode collapses the eigenvector angle toward one-half degree, creating an ill-conditioned realization whose modal coefficients become enormous.'
RECOVERY_TEXT = 'Restore a separated eigenbasis or use a numerically balanced realization, then verify state propagation against the direct matrix reconstruction.'


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
    slow=float(p["slow_mode_per_s"]); angle=np.deg2rad(.5 if broken else float(p["eigenvector_angle_deg"]))
    V=np.array([[1.,np.cos(angle)],[0.,np.sin(angle)]]); lam=np.array([-slow,-4.])
    A=V@np.diag(lam)@np.linalg.inv(V); t=np.linspace(0,6,220); x0=np.array([1.,-.25]); modal=np.linalg.solve(V,x0)
    states=np.array([V@(np.exp(lam*ti)*modal) for ti in t]); direct=np.array([(np.linalg.eig(A)[1]@(np.exp(np.linalg.eigvals(A)*ti)*np.linalg.solve(np.linalg.eig(A)[1],x0))).real for ti in t])
    err=float(np.max(abs(states-direct))); cond=float(np.linalg.cond(V)); spectral=float(np.max(lam))
    return {"signature":[spectral,cond,err],"metrics":[("spectral","Spectral abscissa",spectral,"1/s"),("condition","Eigenvector condition number",cond,"1"),("reconstruction","Modal reconstruction error",err,"1")],
      "plots":{"response":_plot("State transition from two modes","Time (s)","State amplitude (1)",[_trace("State x1",t,states[:,0],"Time","s","State amplitude","1"),_trace("State x2",t,states[:,1],"Time","s","State amplitude","1")]),
      "mechanism":_plot("Individual modal decay","Time (s)","Modal amplitude (1)",[_trace("Slow mode",t,modal[0]*np.exp(lam[0]*t),"Time","s","Modal amplitude","1"),_trace("Fast mode",t,modal[1]*np.exp(lam[1]*t),"Time","s","Modal amplitude","1")])},
      "observation":"Eigenvalues set decay, but the basis condition number controls how reliably state and modal coordinates can be exchanged."}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
