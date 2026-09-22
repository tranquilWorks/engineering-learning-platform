from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 67
BROKEN_TEXT = 'Broken mode disables the monitor and commands unconstrained turns during the longest dropout.'
RECOVERY_TEXT = 'Restore uncertainty-aware guidance, enforce the turn-rate limit, and require the monitor to alarm on the injected dropout fault.'


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
            "requirements": model["requirements"],
        },
    }

def _model(p: dict[str, Any], broken: bool) -> dict[str, Any]:
    a=float(p["gnss_dropout_s"]); b=float(p["turn_rate_limit_deg_s"])
    if broken: a=20.0; b=5.0
    x=np.linspace(0.,10.,240)
    signature=[float(1+.35*a+(0 if broken else 8/b)),float(max(25-b,0) if broken else 0.),float(0. if broken else float(a>3))]
    requirements={
      "NAV-1": {"value": signature[0], "operator": "<", "threshold": 10.0,
                "passed": bool(signature[0] < 10)},
      "ACT-1": {"value": signature[1], "operator": "==", "threshold": 0.0,
                "passed": bool(signature[1] == 0)},
      "MON-1": {"value": signature[2], "operator": "== when dropout > 3 s", "threshold": 1.0,
                "passed": bool(a <= 3 or signature[2] == 1)},
    }
    requirements["SURVEY-PASS"]={"value": float(all(item["passed"] for item in requirements.values())),
                                  "operator": "==", "threshold": 1.0,
                                  "passed": bool(all(item["passed"] for item in requirements.values()))}
    y1=np.asarray((1+.35*a)*np.exp(-x/8),dtype=float); y2=np.asarray(np.zeros_like(x),dtype=float)
    z1=np.asarray(np.minimum(25,b) *np.ones_like(x) if not broken else 25*np.ones_like(x),dtype=float); z2=np.asarray(b*np.ones_like(x),dtype=float)
    if y1.ndim==0: y1=np.full_like(x,float(y1))
    if y2.ndim==0: y2=np.full_like(x,float(y2))
    if z1.ndim==0: z1=np.full_like(x,float(z1))
    if z2.ndim==0: z2=np.full_like(x,float(z2))
    return {"signature":signature,"requirements":requirements,"metrics":[("maximum_cross_track_error", "Maximum Cross Track Error", signature[0], "m"),("turn_rate_violation", "Turn Rate Violation", signature[1], "deg/s"),("monitor_alarm", "Monitor Alarm", signature[2], "bool")],"plots":{
      "response":_plot("Survey cross-track recovery","Time (s)","Cross-track error (m)",[_trace("Nominal/filtered",x,y1,"Time","s","Cross-track error","m"),_trace("Reference/boundary",x,y2,"Time","s","Cross-track error","m")]),
      "mechanism":_plot("Survey turn-rate constraint","Time (s)","Turn rate (deg/s)",[_trace("Mechanism",x,z1,"Time","s","Turn rate","deg/s"),_trace("Requirement/reference",x,z2,"Time","s","Turn rate","deg/s")])},
      "observation":"The survey passes only when navigation uncertainty, cross-track error, turn-rate constraint, and monitor response satisfy their separate requirements."}



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
