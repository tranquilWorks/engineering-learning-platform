from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 25
BROKEN_TEXT = 'Broken mode bypasses both radial configuration projection and velocity projection. The Jacobian and its actual rank are still computed at the used configuration; the fault does not invent an extra tangent dimension.'
RECOVERY_TEXT = 'Disable broken mode, restore defaults and compare raw versus used configurations. Check both radius residual and radial velocity; repairing the position alone would leave the velocity condition unverified.'


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
    offset=float(p['constraint_offset_m']);span=float(p['joint_span_rad'])
    angles=np.linspace(-span/2,span/2,121)
    raw=(1+offset)*np.column_stack([np.cos(angles),np.sin(angles)])
    configurations=raw.copy() if broken else raw/np.linalg.norm(raw,axis=1)[:,None]
    jacobians=configurations/np.linalg.norm(configurations,axis=1)[:,None]
    requested=np.array([1.,0.])
    velocities=[];projectors=[];ranks=[]
    for row in jacobians:
        J=row[None,:]
        projection=np.eye(2)-J.T@np.linalg.solve(J@J.T,J)
        velocities.append(requested if broken else projection@requested)
        projectors.append(projection)
        ranks.append(np.linalg.matrix_rank(J,tol=1e-10))
    velocities=np.array(velocities)
    constraint=np.linalg.norm(configurations,axis=1)-1
    radial=np.sum(jacobians*velocities,axis=1)
    clearance=np.linalg.norm(configurations-np.array([1.5,0.5]),axis=1)-0.2
    signature=[np.max(abs(constraint)),2-min(ranks),np.min(clearance)]
    circle=np.column_stack([np.cos(angles),np.sin(angles)])
    return {'signature':signature,'metrics':[
        ('constraint_residual','Maximum radius constraint residual',signature[0],'m'),
        ('tangent_dimension','Measured tangent dimension',signature[1],'count'),
        ('minimum_clearance','Minimum sampled obstacle clearance',signature[2],'m')],
        'plots':{
            'response':_plot('Configuration projection','Configuration x (m)','Configuration y (m)',[
                _trace('Raw configurations',raw[:,0],raw[:,1],'Configuration x','m','Configuration y','m'),
                _trace('Used configurations',configurations[:,0],configurations[:,1],'Configuration x','m','Configuration y','m'),
                _trace('Unit-radius constraint',circle[:,0],circle[:,1],'Configuration x','m','Configuration y','m')]),
            'mechanism':_plot('Velocity tangency','Configuration angle (rad)','Radial velocity (m/s)',[
                _trace('Used candidate velocity',angles,radial,'Configuration angle','rad','Radial velocity','m/s'),
                _trace('Requested radial part',angles,jacobians@requested,'Configuration angle','rad','Radial velocity','m/s')])},
        'details':{'sample_count':len(angles),'angles':angles,'raw_configurations':raw,'configurations':configurations,
            'jacobians':jacobians,'projectors':projectors,'requested_velocity':requested,'velocities':velocities,
            'constraint_residual':constraint,'radial_velocity':radial,'clearance':clearance,'constraint_ranks':ranks},
        'observation':'The circle constraint and its Jacobian are evaluated at each sampled configuration. Projection enforces first-order tangency; the displayed arc is a configuration sweep, not an integrated velocity trajectory. Tangency alone does not certify collision avoidance.'}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
