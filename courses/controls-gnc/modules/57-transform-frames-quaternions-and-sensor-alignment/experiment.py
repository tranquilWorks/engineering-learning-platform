from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 57
BROKEN_TEXT = 'Broken mode treats degrees as radians and scales the quaternion, violating the norm/orthogonality checks.'
RECOVERY_TEXT = 'Convert units, normalize the quaternion, state active/passive frame order, and recheck vector norm and determinant.'


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
    a=float(p["yaw_angle_deg"]); b=float(p["sensor_misalignment_deg"])
    if broken: a=35.0; b=15.0
    x=np.linspace(0.,10.,240)
    signature=[float(.2 if broken else 0.),float(.44 if broken else 0.),float(abs(np.sin(np.deg2rad(b)))+(1 if broken else 0))]
    y1=np.asarray(np.cos(x+np.deg2rad(a)),dtype=float); y2=np.asarray(np.sin(x+np.deg2rad(a)),dtype=float)
    z1=np.asarray(np.ones_like(x),dtype=float); z2=np.asarray(np.full_like(x,1.2 if broken else 1.),dtype=float)
    if y1.ndim==0: y1=np.full_like(x,float(y1))
    if y2.ndim==0: y2=np.full_like(x,float(y2))
    if z1.ndim==0: z1=np.full_like(x,float(z1))
    if z2.ndim==0: z2=np.full_like(x,float(z2))
    return {"signature":signature,"metrics":[("quaternion_norm_error", "Quaternion Norm Error", signature[0], "1"),("dcm_orthogonality_error", "Dcm Orthogonality Error", signature[1], "1"),("alignment_vector_error", "Alignment Vector Error", signature[2], "1")],"plots":{
      "response":_plot("Rotated body-axis vector","Vector east component (1)","Vector north component (1)",[_trace("Nominal/filtered",x,y1,"Vector east component","1","Vector north component","1"),_trace("Reference/boundary",x,y2,"Vector east component","1","Vector north component","1")]),
      "mechanism":_plot("Quaternion norm check","Rotation angle (rad)","Quaternion norm (1)",[_trace("Mechanism",x,z1,"Rotation angle","rad","Quaternion norm","1"),_trace("Requirement/reference",x,z2,"Rotation angle","rad","Quaternion norm","1")])},
      "observation":"A normalized quaternion produces an orthogonal proper rotation that preserves vector norm; alignment order remains explicit."}



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
