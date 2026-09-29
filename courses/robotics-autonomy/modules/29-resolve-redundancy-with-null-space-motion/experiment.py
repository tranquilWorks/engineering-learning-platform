from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 29
BROKEN_TEXT = 'Broken mode bypasses the null projector and adds minus gain times the full posture vector to the primary command.'
RECOVERY_TEXT = 'Restore the exact projector and defaults. Check actual task velocity, secondary leakage and joint velocity together; a low total joint speed alone cannot certify task preservation.'


def _trace(
    name: str,
    x: Any,
    y: Any,
    x_quantity: str,
    x_unit: str,
    y_quantity: str,
    y_unit: str,
    *,
    mode: str = "lines",
) -> dict[str, Any]:
    # A zero-span sweep is a real point, so keep it visibly represented.
    if mode == "lines" and np.asarray(x).size and np.ptp(np.asarray(x, dtype=float)) == 0:
        mode = "lines+markers"
    return {
        "type": "scatter",
        "mode": mode,
        "name": name,
        "x": np.asarray(x, dtype=float),
        "y": np.asarray(y, dtype=float),
        "meta": {
            "x_quantity": x_quantity,
            "x_unit": x_unit,
            "y_quantity": y_quantity,
            "y_unit": y_unit,
        },
    }


def _plot(
    title: str, x_title: str, y_title: str, traces: list[dict[str, Any]]
) -> dict[str, Any]:
    return {
        "data": traces,
        "layout": {
            "title": {"text": title, "x": 0.02},
            "xaxis": {"title": {"text": x_title}},
            "yaxis": {"title": {"text": y_title}},
            "legend": {"orientation": "h"},
            "margin": {"l": 72, "r": 36, "t": 62, "b": 62},
            "hovermode": "closest",
            "uirevision": "keep-view",
        },
        "config": {"responsive": True, "displaylogo": False},
    }


def _result(model: dict[str, Any], broken: bool) -> dict[str, Any]:
    return {
        "metrics": [
            {
                "id": key,
                "label": label,
                "value": float(value),
                "unit": unit,
                "emphasis": "primary" if index == 0 else "normal",
            }
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
            **model.get("details", {}),
            "broken_active": bool(broken),
            "signature": [float(value) for value in model["signature"]],
        },
    }


def _model(p, broken):
    damping=float(p['damping']); gain=float(p['null_gain_per_s'])
    q=np.array([.3,-.7,.9]); lengths=np.array([1.,.8,.6]); angles=np.cumsum(q)
    J=np.array([[-np.sum(lengths[j:]*np.sin(angles[j:])) for j in range(3)],[np.sum(lengths[j:]*np.cos(angles[j:])) for j in range(3)]])
    desired=np.array([.1,-.06]); primary=J.T@np.linalg.solve(J@J.T+damping**2*np.eye(2),desired)
    projector=np.eye(3)-np.linalg.pinv(J)@J
    gains=np.linspace(0,gain,121); secondary=np.array([-g*(q if broken else projector@q) for g in gains])
    joint_velocity=primary+secondary; task_velocity=joint_velocity@J.T
    signature=[np.linalg.norm(task_velocity[-1]-desired),np.linalg.norm(J@secondary[-1]),np.linalg.norm(joint_velocity[-1])]
    return {'signature':signature,'metrics':[
        ('task_velocity_error','Task velocity residual',signature[0],'m/s'),('secondary_leakage','Secondary task leakage',signature[1],'m/s'),('joint_speed_norm','Joint velocity norm',signature[2],'rad/s')],
        'plots':{'response':_plot('Instantaneous joint commands','Posture gain (1/s)','Joint velocity (rad/s)',[
            _trace('Joint '+str(j+1),gains,joint_velocity[:,j],'Posture gain','1/s','Joint velocity','rad/s') for j in range(3)]),
            'mechanism':_plot('Resulting task velocity','Posture gain (1/s)','Task velocity (m/s)',[
                _trace('Actual '+axis,gains,task_velocity[:,j],'Posture gain','1/s','Task velocity','m/s') for j,axis in enumerate(['x','y'])]+[
                _trace('Desired '+axis,gains,np.full(121,desired[j]),'Posture gain','1/s','Task velocity','m/s') for j,axis in enumerate(['x','y'])])},
        'details':{'sample_count':121,'joint_position':q,'link_lengths':lengths,'jacobian':J,'projector':projector,'primary':primary,'secondary':secondary,'gains':gains,'joint_velocity':joint_velocity,'task_velocity':task_velocity,'desired':desired},
        'observation':'A damped primary inverse and an exact Moore-Penrose null projector have different roles. Normal secondary posture velocity has negligible task leakage; bypassing the projector changes the actual task velocity. This is an instantaneous calculation at one configuration, not integrated motion or a joint-limit guarantee.'}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    model = _model(parameters, broken)
    layout = model["plots"]["mechanism"]["layout"]
    layout["margin"]["b"] = 105
    layout["xaxis"]["title"]["standoff"] = 16
    layout["xaxis"]["automargin"] = True
    layout["legend"].update(entrywidth=0.5, entrywidthmode="fraction", y=-0.4)
    return _result(model, broken)
