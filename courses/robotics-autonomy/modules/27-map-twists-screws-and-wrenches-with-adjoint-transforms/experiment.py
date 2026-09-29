from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 27
BROKEN_TEXT = 'Broken mode applies the motion adjoint directly to the wrench instead of its inverse transpose. It still performs the correct twist transformation and round-trip motion check.'
RECOVERY_TEXT = 'Restore the dual wrench transformation, reset both controls and compare the two power curves. The motion round-trip residual can remain tiny in both modes, so it alone cannot diagnose the wrench fault.'


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


def _skew(v):
    x,y,z=v
    return np.array([[0.,-z,y],[z,0.,-x],[-y,x,0.]])


def _model(p, broken):
    lever=float(p['lever_arm_m']); speed=float(p['angular_speed_rad_s'])
    twist=np.array([0.,0.,speed,.2,.3,.1]); wrench=np.array([.1,.2,.3,2.,-1.,.5])
    fractions=np.linspace(0,1,121); twists=[]; wrenches=[]; power=[]; linear=[]; angular=[]; adjoints=[]
    for f in fractions:
        angle=np.pi*f/3; c,s=np.cos(angle),np.sin(angle)
        R=np.array([[c,-s,0.],[s,c,0.],[0.,0.,1.]])
        t=np.array([lever*f,.2*lever*f,0.]); A=np.block([[R,np.zeros((3,3))],[_skew(t)@R,R]])
        va=A@twist; wa=A@wrench if broken else np.linalg.solve(A.T,wrench)
        Ri=R.T; ti=-Ri@t; Ai=np.block([[Ri,np.zeros((3,3))],[_skew(ti)@Ri,Ri]])
        roundtrip=Ai@va-twist
        twists.append(va); wrenches.append(wa); power.append(wa@va); linear.append(np.linalg.norm(roundtrip[3:])); angular.append(np.linalg.norm(roundtrip[:3])); adjoints.append(A)
    twists=np.array(twists); wrenches=np.array(wrenches); power=np.array(power)
    signature=[np.max(abs(power-wrench@twist)),np.max(linear),twist[:3]@twist[3:]/(twist[:3]@twist[:3])]
    return {'signature':signature,'metrics':[
        ('power_error','Maximum power discrepancy',signature[0],'W'),('linear_roundtrip','Linear round-trip residual',signature[1],'m/s'),('screw_pitch','Screw pitch',signature[2],'m/rad')],
        'plots':{'response':_plot('Transformed linear velocity','Transform fraction (1)','Linear velocity (m/s)',[
            _trace(name,fractions,twists[:,j+3],'Transform fraction','1','Linear velocity','m/s') for j,name in enumerate(['vx','vy','vz'])]),
            'mechanism':_plot('Dual-transform power','Transform fraction (1)','Power (W)',[
                _trace('Transformed power',fractions,power,'Transform fraction','1','Power','W'),
                _trace('Original power',fractions,np.full(121,wrench@twist),'Transform fraction','1','Power','W')])},
        'details':{'sample_count':121,'fractions':fractions,'source_twist':twist,'source_wrench':wrench,'twists':twists,'wrenches':wrenches,'adjoints':adjoints,'powers':power,'angular_roundtrip_rad_s':angular,'linear_roundtrip_m_s':linear},
        'observation':'Twists use [angular; linear] order, wrenches [moment; force]. The inverse-transpose wrench map preserves their actual power pairing. Applying a motion adjoint to a wrench is the deliberate, dimensionally invalid fault. Round-trip angular and linear residuals retain separate units.'}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    model = _model(parameters, broken)
    source_power = float(model["details"]["source_twist"] @ model["details"]["source_wrench"])
    # Keep physical power readable instead of magnifying machine-roundoff wiggles.
    span = max(0.1, 1.2 * float(model["signature"][0]))
    model["plots"]["mechanism"]["layout"]["yaxis"]["range"] = [source_power - span, source_power + span]
    return _result(model, broken)
