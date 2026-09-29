from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 61
BROKEN_TEXT = 'Broken mode computes updates and shrinks covariance but discards the state correction instead of injecting it.'
RECOVERY_TEXT = 'Restore injection and reset both controls. Check actual position error and bias estimate, not only the covariance drop.'


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
    interval=float(p['gnss_interval_s']); q=float(p['bias_random_walk'])
    updates=np.arange(interval,20.+1e-9,interval)
    time=np.unique(np.round(np.r_[np.arange(0,20.0001,.1),updates],10))
    state=np.array([0.,2.,0.]); covariance=np.diag([1.,.25,.0025]); H=np.array([1.,0.,0.])
    states=[state.copy()]; covariances=[covariance.copy()]; injections=[]; update_time=[]; pre_sigma=[]; post_sigma=[]
    for t0,t in zip(time[:-1],time[1:]):
        dt=t-t0
        F=np.array([[1.,dt,-dt**2/2],[0.,1.,-dt],[0.,0.,1.]])
        Q=q*q*np.array([[dt**5/20,dt**4/8,-dt**3/6],[dt**4/8,dt**3/3,-dt**2/2],[-dt**3/6,-dt**2/2,dt]])
        acceleration=.04-state[2]
        state[:2]+=[state[1]*dt+.5*acceleration*dt**2,acceleration*dt]
        covariance=F@covariance@F.T+Q
        if np.any(abs(updates-t)<1e-8):
            pre_sigma.append(np.sqrt(covariance[0,0])); update_time.append(t)
            innovation=2*t+.3*np.sin(.7*t)-state[0]
            gain=covariance@H/(H@covariance@H+1.)
            correction=gain*innovation
            if not broken:
                state+=correction
            A=np.eye(3)-np.outer(gain,H)
            covariance=A@covariance@A.T+np.outer(gain,gain)
            injections.append(correction)
            post_sigma.append(np.sqrt(covariance[0,0]))
        states.append(state.copy()); covariances.append(covariance.copy())
    states=np.asarray(states); covariances=np.asarray(covariances)
    signature=[pre_sigma[-1],post_sigma[-1],abs(states[-1,0]-40.)]
    return {'signature':signature,'metrics':[
        ('prior_sigma','Last update prior position sigma',signature[0],'m'),('posterior_sigma','Last update posterior position sigma',signature[1],'m'),
        ('terminal_error','Terminal position error',signature[2],'m'),('bias_error','Terminal bias error',abs(states[-1,2]-.04),'m/s^2')],
        'plots':{'response':_plot('Injected navigation state','Time (s)','Position (m)',[
            _trace('Estimated position',time,states[:,0],'Time','s','Position','m'),_trace('Truth',time,2*time,'Time','s','Position','m')]),
            'mechanism':_plot('Error and formal sigma','Time (s)','Position error (m)',[
                _trace('Actual error',time,states[:,0]-2*time,'Time','s','Position error','m'),
                _trace('Formal sigma',time,np.sqrt(covariances[:,0,0]),'Time','s','Position error','m')])},
        'details':{'time':time,'states':states,'covariances':covariances,'update_time':update_time,'injections':injections,'prior_sigma':pre_sigma,'posterior_sigma':post_sigma,'reset_error_state':np.zeros(3),'reset_jacobian':np.eye(3)},
        'observation':'This additive one-axis position/velocity/bias filter propagates covariance and injects each GNSS correction. Error coordinates reset to zero with identity reset Jacobian. Withholding injection can leave optimistic covariance beside actual position drift; this is not a full attitude ESKF.'}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
