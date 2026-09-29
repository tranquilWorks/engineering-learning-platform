from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 65
BROKEN_TEXT = 'Broken mode solves the unconstrained objective and applies that command sequence without enforcing the selected actuator limit.'
RECOVERY_TEXT = 'Restore the bounded solve, reset controls and verify every applied interval satisfies the limit. Compare the residual rather than assuming it becomes zero.'


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
    from scipy.optimize import lsq_linear
    limit=float(p['acceleration_limit_m_s2']); weight=float(p['terminal_weight'])
    dt=.1; count=20
    B=np.vstack([dt**2*(count-np.arange(count)-.5),np.full(count,dt)])
    free=np.array([30.,0.]); W=np.diag([weight,.5*weight]); R=.1
    A=np.vstack([np.sqrt(W)@B,np.sqrt(R)*np.eye(count)])
    target=np.r_[-np.sqrt(W)@free,np.zeros(count)]
    u=np.linalg.lstsq(A,target,rcond=None)[0] if broken else lsq_linear(A,target,bounds=(-limit,limit),method='bvls',tol=1e-13).x
    states=[free.copy()]
    for acceleration in u:
        x,v=states[-1]
        states.append(np.array([x+dt*v+.5*dt**2*acceleration,v+dt*acceleration]))
    states=np.array(states); terminal=states[-1]; gradient=R*u+B.T@W@terminal
    projected_gradient=u-np.clip(u-gradient,-limit,limit)
    signature=[np.max(abs(u)),max(0.,np.max(abs(u))-limit),abs(terminal[0])]
    return {'signature':signature,'metrics':[
        ('peak_acceleration','Peak applied acceleration',signature[0],'m/s^2'),('actuator_violation','Actuator violation',signature[1],'m/s^2'),
        ('terminal_position_error','Terminal position residual',signature[2],'m'),('terminal_velocity_error','Terminal velocity residual',abs(terminal[1]),'m/s')],
        'plots':{'response':_plot('Executed terminal trajectory','Time (s)','Position (m)',[_trace('Position',np.arange(21)*dt,states[:,0],'Time','s','Position','m')]),
            'mechanism':_plot('Applied bounded commands','Interval start (s)','Acceleration (m/s²)',[
                _trace('Applied',np.arange(20)*dt,u,'Interval start','s','Acceleration','m/s^2',mode='lines+markers'),
                _trace('Upper limit',np.arange(20)*dt,np.full(20,limit),'Interval start','s','Acceleration','m/s^2'),
                _trace('Lower limit',np.arange(20)*dt,np.full(20,-limit),'Interval start','s','Acceleration','m/s^2')])},
        'details':{'states':states,'commands':u,'endpoint_map':B,'terminal':terminal,'gradient':gradient,'projected_gradient':projected_gradient,'objective':R*(u@u)+terminal@W@terminal,'dt':dt},
        'observation':'A twenty-interval bounded least-squares solve balances terminal position, terminal velocity and command effort. Actual applied commands propagate the double integrator. Finite terminal weights permit residual even when exact arrival is feasible; broken mode applies the unconstrained optimum.'}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
