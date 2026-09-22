from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 54
BROKEN_TEXT = 'Broken mode freezes the Jacobian at zero, so the filter ignores the nonlinear measurement.'
RECOVERY_TEXT = 'Move to an observable linearization or use an estimator that represents the nonlinear transform, then recheck innovation consistency.'


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
    a=float(p["prior_standard_deviation"]); b=float(p["linearization_state"])
    if broken: a=0.5; b=0.0
    x=np.linspace(0.,10.,240)
    signature=[float(0. if broken else 2*b),float(a*a/(1+(0 if broken else 2*b)**2*a*a)),float(a*a)]
    y1=np.asarray(x*x,dtype=float); y2=np.asarray((b+(x-b))*2*b-b*b,dtype=float)
    z1=np.asarray(np.full_like(x,a*a),dtype=float); z2=np.asarray(np.full_like(x,a*a/(1+(0 if broken else 2*b)**2*a*a)),dtype=float)
    if y1.ndim==0: y1=np.full_like(x,float(y1))
    if y2.ndim==0: y2=np.full_like(x,float(y2))
    if z1.ndim==0: z1=np.full_like(x,float(z1))
    if z2.ndim==0: z2=np.full_like(x,float(z2))
    return {"signature":signature,"metrics":[("measurement_jacobian", "Measurement Jacobian", signature[0], "1"),("posterior_variance", "Posterior Variance", signature[1], "1"),("linearization_residual", "Linearization Residual", signature[2], "1")],"plots":{
      "response":_plot("Nonlinear measurement and EKF tangent","State (1)","Measurement (1)",[_trace("Nominal/filtered",x,y1,"State","1","Measurement","1"),_trace("Reference/boundary",x,y2,"State","1","Measurement","1")]),
      "mechanism":_plot("Prior and posterior variance","Update index (step)","Variance (1)",[_trace("Mechanism",x,z1,"Update index","step","Variance","1"),_trace("Requirement/reference",x,z2,"Update index","step","Variance","1")])},
      "observation":"An EKF update uses the local Jacobian; at xhat=0 the quadratic measurement has zero first-order sensitivity despite nonzero global information."}



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
