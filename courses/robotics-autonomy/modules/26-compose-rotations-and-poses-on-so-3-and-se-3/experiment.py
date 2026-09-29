from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 26
BROKEN_TEXT = 'Broken mode linearly interpolates rotation matrices instead of constructing a rotation at each fractional angle.'
RECOVERY_TEXT = 'Restore angle-based rotation, reset defaults and check orthogonality, determinant and rigid-inverse point residual together. Keep the composition-order difference; making it vanish is not the recovery objective.'


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


def rotation_z(angle):
    c,s=np.cos(angle),np.sin(angle)
    return np.array([[c,-s,0.],[s,c,0.],[0.,0.,1.]])


def pose(rotation, translation):
    result=np.eye(4);result[:3,:3]=rotation;result[:3,3]=translation
    return result


def _model(p, broken):
    angle=np.deg2rad(float(p['rotation_angle_deg']));distance=float(p['translation_m'])
    fractions=np.linspace(0,1,121)
    phi=np.pi/6
    Rx=np.array([[1.,0.,0.],[0.,np.cos(phi),-np.sin(phi)],[0.,np.sin(phi),np.cos(phi)]])
    B=pose(Rx,[0.,0.25,0.1]);point=np.array([0.3,0.2,0.4,1.])
    points_ab=[];points_ba=[];orthogonality=[];determinants=[];roundtrips=[];transforms=[]
    for fraction in fractions:
        rotation=(1-fraction)*np.eye(3)+fraction*rotation_z(angle) if broken else rotation_z(fraction*angle)
        A=pose(rotation,[0.,fraction*distance,0.]);AB=A@B;BA=B@A
        rigid_inverse=pose(AB[:3,:3].T,-AB[:3,:3].T@AB[:3,3])
        points_ab.append((AB@point)[:3]);points_ba.append((BA@point)[:3])
        orthogonality.append(np.linalg.norm(rotation.T@rotation-np.eye(3),'fro'))
        determinants.append(np.linalg.det(rotation))
        roundtrips.append(np.linalg.norm((rigid_inverse@AB@point-point)[:3]))
        transforms.append(AB)
    points_ab,points_ba=np.array(points_ab),np.array(points_ba)
    signature=[max(orthogonality),max(abs(np.array(determinants)-1)),np.linalg.norm(points_ab[-1]-points_ba[-1])]
    return {'signature':signature,'metrics':[
        ('orthogonality_error','Maximum rotation orthogonality error',signature[0],'1'),
        ('determinant_error','Maximum determinant error',signature[1],'1'),
        ('order_difference','Final composition-order point difference',signature[2],'m')],
        'plots':{
            'response':_plot('Pose composition order','World x coordinate (m)','World y coordinate (m)',[
                _trace('A after B',points_ab[:,0],points_ab[:,1],'World x coordinate','m','World y coordinate','m'),
                _trace('B after A',points_ba[:,0],points_ba[:,1],'World x coordinate','m','World y coordinate','m')]),
            'mechanism':_plot('Rotation-group checks','Composition fraction (1)','Rotation residual (1)',[
                _trace('Orthogonality error',fractions,orthogonality,'Composition fraction','1','Rotation residual','1'),
                _trace('Determinant error',fractions,np.abs(np.array(determinants)-1),'Composition fraction','1','Rotation residual','1')])},
        'details':{'sample_count':len(fractions),'fractions':fractions,'transforms':transforms,'fixed_pose':B,
            'point':point,'points_ab':points_ab,'points_ba':points_ba,'orthogonality':orthogonality,
            'determinants':determinants,'rigid_inverse_point_error':roundtrips},
        'observation':'A and B are explicitly composed homogeneous transforms applied to one 3D point; the chart shows its x/y projection. Linear interpolation of rotation matrices leaves SO(3) between valid endpoints. Composition-order difference is expected and is not itself a numerical error.'}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
