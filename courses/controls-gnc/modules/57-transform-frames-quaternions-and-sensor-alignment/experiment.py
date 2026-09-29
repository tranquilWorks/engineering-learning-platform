from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 57
BROKEN_TEXT = 'Broken mode multiplies the composed quaternion by 1.2 and feeds it to a formula that assumes unit norm, without normalization.'
RECOVERY_TEXT = 'Disable broken mode, restore defaults, and check norm, orthogonality and actual vector error together.'


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


def quaternion_product(left, right):
    w, v = left[0], np.asarray(left[1:])
    z, u = right[0], np.asarray(right[1:])
    return np.r_[w*z-v@u, w*u+z*v+np.cross(v,u)]


def quaternion_matrix(q):
    w,x,y,z=q
    return np.array([[1-2*(y*y+z*z),2*(x*y-w*z),2*(x*z+w*y)],
                     [2*(x*y+w*z),1-2*(x*x+z*z),2*(y*z-w*x)],
                     [2*(x*z-w*y),2*(y*z+w*x),1-2*(x*x+y*y)]])


def _model(p, broken):
    yaw=np.deg2rad(float(p['yaw_angle_deg']))
    alignment=np.deg2rad(float(p['sensor_misalignment_deg']))
    sensor_to_body=np.array([np.cos(alignment/2),np.sin(alignment/2),0.,0.])
    body_vector=np.array([0.4,0.7,0.2])
    sensor_vector=quaternion_matrix(sensor_to_body).T@body_vector
    angles=np.linspace(0.,yaw,121)
    used_vectors, true_vectors, raw_vectors, norms, orthogonality, quaternions, matrices=[],[],[],[],[],[],[]
    for angle in angles:
        body_to_world=np.array([np.cos(angle/2),0.,0.,np.sin(angle/2)])
        composed=quaternion_product(body_to_world,sensor_to_body)
        used=1.2*composed if broken else composed/np.linalg.norm(composed)
        rotation=quaternion_matrix(used)
        used_vectors.append(rotation@sensor_vector)
        true_vectors.append(quaternion_matrix(body_to_world)@body_vector)
        raw_vectors.append(quaternion_matrix(body_to_world)@sensor_vector)
        norms.append(np.linalg.norm(used))
        orthogonality.append(np.linalg.norm(rotation.T@rotation-np.eye(3),'fro'))
        quaternions.append(used);matrices.append(rotation)
    used_vectors,true_vectors,raw_vectors=map(np.array,(used_vectors,true_vectors,raw_vectors))
    errors=np.linalg.norm(used_vectors-true_vectors,axis=1)
    signature=[abs(norms[-1]-1),orthogonality[-1],errors[-1]]
    return {'signature':signature,'metrics':[
        ('quaternion_norm_error','Final quaternion norm error',signature[0],'1'),
        ('dcm_orthogonality_error','Final rotation orthogonality error',signature[1],'1'),
        ('alignment_vector_error','Final compensated vector error',signature[2],'1'),
        ('uncorrected_error','Error without sensor alignment',np.linalg.norm(raw_vectors[-1]-true_vectors[-1]),'1')],
        'plots':{
            'response':_plot('World sensor vector','World x component (1)','World y component (1)',[
                _trace('Reported compensated vector',used_vectors[:,0],used_vectors[:,1],'World x component','1','World y component','1'),
                _trace('Correct world vector',true_vectors[:,0],true_vectors[:,1],'World x component','1','World y component','1'),
                _trace('Alignment omitted',raw_vectors[:,0],raw_vectors[:,1],'World x component','1','World y component','1')]),
            'mechanism':_plot('Rotation residuals','Yaw sweep (deg)','Residual norm (1)',[
                _trace('Quaternion norm error',np.rad2deg(angles),np.abs(np.array(norms)-1),'Yaw sweep','deg','Residual norm','1'),
                _trace('Orthogonality residual',np.rad2deg(angles),orthogonality,'Yaw sweep','deg','Residual norm','1'),
                _trace('Compensated vector error',np.rad2deg(angles),errors,'Yaw sweep','deg','Residual norm','1')])},
        'details':{'angles':angles,'quaternions':quaternions,'matrices':matrices,'sensor_vector':sensor_vector,
                   'body_vector':body_vector,'used_vectors':used_vectors,'true_vectors':true_vectors,'raw_vectors':raw_vectors},
        'observation':'Scalar-first active quaternions compose sensor-to-body followed by body-to-world rotation. Residuals come from the actual matrices and vectors. A scaled identity quaternion is a special case where the unit-quaternion matrix formula can look correct despite an invalid quaternion norm.'}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
