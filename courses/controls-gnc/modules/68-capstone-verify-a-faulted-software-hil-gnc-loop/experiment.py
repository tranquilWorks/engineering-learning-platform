from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 68
BROKEN_TEXT = 'Broken mode holds the last command through stale/drop intervals and suppresses the watchdog, violating fail-zero behavior.'
RECOVERY_TEXT = 'Restore timestamp checks and fail-zero watchdog, rerun the deterministic fault schedule, and retain the physical-HIL gap.'


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
    a=float(p["one_way_latency_ms"]); b=float(p["packet_drop_fraction"])
    if broken: a=80.0; b=0.5
    x=np.linspace(0.,10.,240)
    deadline_miss=min(1.,max(a-30.,0.)/50.)
    watchdog_activation=0. if broken else min(1.,b+deadline_miss)
    requirements={
      "TIME-1": {"value": float(deadline_miss), "operator": "==", "threshold": 0.0,
                 "passed": bool(deadline_miss == 0)},
      "LOSS-1": {"value": float(b), "operator": "<", "threshold": .2,
                 "passed": bool(b < .2)},
      "SAFE-1": {"value": float(watchdog_activation), "operator": ">= injected fault fraction",
                 "threshold": float(b), "passed": bool(watchdog_activation >= b and not broken)},
    }
    requirements_passed=all(item["passed"] for item in requirements.values())
    signature=[float(deadline_miss),float(watchdog_activation),float(requirements_passed)]
    y1=np.asarray(a/1000+x*0+b*.1,dtype=float); y2=np.asarray(np.full_like(x,.05),dtype=float)
    z1=np.asarray(np.zeros_like(x) if broken else ((x%5)<(b*5+a/100)).astype(float),dtype=float); z2=np.asarray(np.ones_like(x),dtype=float)
    if y1.ndim==0: y1=np.full_like(x,float(y1))
    if y2.ndim==0: y2=np.full_like(x,float(y2))
    if z1.ndim==0: z1=np.full_like(x,float(z1))
    if z2.ndim==0: z2=np.full_like(x,float(z2))
    return {"signature":signature,"requirements":requirements,"metrics":[("deadline_miss_fraction", "Deadline Miss Fraction", signature[0], "1"),("watchdog_activation_fraction", "Watchdog Activation Fraction", signature[1], "1"),("requirements_passed", "Requirements Passed", signature[2], "bool")],"plots":{
      "response":_plot("Software-HIL command age","Event time (s)","Command age (s)",[_trace("Nominal/filtered",x,y1,"Event time","s","Command age","s"),_trace("Reference/boundary",x,y2,"Event time","s","Command age","s")]),
      "mechanism":_plot("Watchdog fault response","Event time (s)","Watchdog active (bool)",[_trace("Mechanism",x,z1,"Event time","s","Watchdog active","bool"),_trace("Requirement/reference",x,z2,"Event time","s","Watchdog active","bool")])},
      "observation":"A software-HIL pass requires every named timing and fault-response requirement to pass; physical I/O and real-time scheduling remain an explicit evidence gap."}



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
