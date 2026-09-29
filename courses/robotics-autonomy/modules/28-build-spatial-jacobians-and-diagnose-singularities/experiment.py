from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 28
BROKEN_TEXT = 'Broken mode omits the elbow Jacobian column while leaving the forward kinematics unchanged. The computed Jacobian loses a joint contribution and the finite-difference residual exposes it.'
RECOVERY_TEXT = 'Restore the second column, reset controls and compare both derivative agreement and task singular values. A small singular value at a truly aligned configuration is expected and should not be repaired by adding an arbitrary floor.'


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


def _fk(q, ratio):
    return np.array([np.cos(q[0])+ratio*np.cos(q.sum()),np.sin(q[0])+ratio*np.sin(q.sum())])


def _jacobian(q, ratio):
    a,b=q; s=np.sin(a+b); c=np.cos(a+b)
    return np.array([[-np.sin(a)-ratio*s,-ratio*s],[np.cos(a)+ratio*c,ratio*c]])


def _model(p, broken):
    angle=np.deg2rad(float(p['elbow_angle_deg'])); ratio=float(p['link_ratio'])
    angles=np.linspace(0,angle,121); singular=[]; errors=[]; jacobians=[]; differences=[]
    for a in angles:
        q=np.array([.4,a]); J=_jacobian(q,ratio)
        if broken:
            J[:,1]=0.
        step=1e-5
        difference=np.column_stack([(_fk(q+step*axis,ratio)-_fk(q-step*axis,ratio))/(2*step) for axis in np.eye(2)])
        singular.append(np.linalg.svd(J,compute_uv=False)); errors.append(np.linalg.norm(J-difference)); jacobians.append(J); differences.append(difference)
    singular=np.asarray(singular); signature=[singular[-1,-1],np.prod(singular[-1]),errors[-1]]
    return {'signature':signature,'metrics':[
        ('minimum_singular_value','Minimum position singular value',signature[0],'m/rad'),('manipulability','Position manipulability',signature[1],'m^2/rad^2'),('finite_difference_error','Jacobian difference norm',signature[2],'m/rad')],
        'plots':{'response':_plot('Position-task singular values','Elbow angle (deg)','Singular value (m/rad)',[
            _trace('Largest',np.rad2deg(angles),singular[:,0],'Elbow angle','deg','Singular value','m/rad'),
            _trace('Smallest',np.rad2deg(angles),singular[:,1],'Elbow angle','deg','Singular value','m/rad')]),
            'mechanism':_plot('Kinematic derivative check','Elbow angle (deg)','Jacobian difference (m/rad)',[
                _trace('Central-difference residual',np.rad2deg(angles),errors,'Elbow angle','deg','Jacobian difference','m/rad')])},
        'details':{'sample_count':121,'angles_rad':angles,'jacobians':jacobians,'finite_differences':differences,'singular_values':singular,'fd_errors':errors,'joint_position':[.4,angle],'link_lengths_m':[1.,ratio]},
        'observation':'A two-link planar position Jacobian is differentiated from actual forward kinematics and checked by central differences. The omitted-column fault loses one joint contribution. Rank loss refers to this two-dimensional position task, not a full spatial-twist Jacobian.'}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
