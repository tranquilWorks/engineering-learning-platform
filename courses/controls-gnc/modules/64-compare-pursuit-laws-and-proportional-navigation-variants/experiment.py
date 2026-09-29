from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 64
BROKEN_TEXT = 'Broken mode reverses the LOS-rate sign in PN and augmented PN while preserving both controls and the pursuit comparison.'
RECOVERY_TEXT = 'Restore the rate sign and defaults. Confirm the initial command reverses back and inspect the resulting trajectory duration and separation curve.'


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


def _trajectory(n, omega, broken, law):
    from scipy.integrate import solve_ivp
    beacon_speed = 1.0  # m/s; target lateral acceleration is speed * turn rate.
    def command(state):
        x,y,heading,bx,by,bheading=state
        relative=np.array([bx-x,by-y]); velocity=beacon_speed*np.array([np.cos(bheading),np.sin(bheading)])-3*np.array([np.cos(heading),np.sin(heading)])
        range2=relative@relative
        rate=(relative[0]*velocity[1]-relative[1]*velocity[0])/range2
        closing=-(relative@velocity)/np.sqrt(range2)
        if law=='pursuit':
            error=np.arctan2(np.sin(np.arctan2(relative[1],relative[0])-heading),np.cos(np.arctan2(relative[1],relative[0])-heading))
            return 3*1.5*error
        acceleration=n*max(closing,0.)*rate*(-1 if broken else 1)
        if law=='augmented':
            acceleration+=.5*n*beacon_speed*omega*np.cos(bheading-heading)
        return acceleration
    def derivative(t,state):
        heading=state[2]; bheading=state[5]
        return [3*np.cos(heading),3*np.sin(heading),command(state)/3,beacon_speed*np.cos(bheading),beacon_speed*np.sin(bheading),omega]
    def capture(t,state):
        return np.hypot(state[3]-state[0],state[4]-state[1])-1.
    capture.terminal=True; capture.direction=-1
    solution=solve_ivp(derivative,[0,8],[0.,0.,0.,12.,4.,.6],method='DOP853',rtol=2e-11,atol=2e-12,events=capture,dense_output=True,max_step=.1)
    if not solution.success:
        raise RuntimeError(solution.message)
    time=np.linspace(0,solution.t[-1],121); states=solution.sol(time).T
    separation=np.linalg.norm(states[:,3:5]-states[:,:2],axis=1)
    acceleration=np.array([command(state) for state in states])
    return {'time':time,'states':states,'separation':separation,'commands':acceleration,'captured':bool(len(solution.t_events[0]))}


def _model(p, broken):
    n=float(p['navigation_constant']); omega=np.deg2rad(float(p['target_turn_rate_deg_s']))
    runs={law:_trajectory(n,omega,broken,law) for law in ['pursuit','pn','augmented']}
    selected=runs['pn']; signature=[selected['commands'][0],np.min(selected['separation']),selected['time'][-1]]
    return {'signature':signature,'metrics':[
        ('initial_command','Initial PN command',signature[0],'m/s^2'),('sampled_closest','Sampled closest PN separation',signature[1],'m'),
        ('observed_duration','PN observation duration',signature[2],'s'),('peak_command','Peak sampled PN acceleration',np.max(abs(selected['commands'])),'m/s^2')],
        'plots':{'response':_plot('Moving-beacon separation','Time (s)','Separation (m)',[
            _trace(law,run['time'],run['separation'],'Time','s','Separation','m') for law,run in runs.items()]),
            'mechanism':_plot('Executed lateral commands','Time (s)','Acceleration (m/s²)',[
                _trace(law,run['time'],run['commands'],'Time','s','Acceleration','m/s^2') for law,run in runs.items()])},
        'details':{'trajectories':runs,'capture_radius_m':1.,'horizon_s':8.},
        'observation':'Civilian point-mass rendezvous compares heading pursuit, velocity-normal PN and a declared feed-forward variant. Each integration ends at one-metre capture or eight seconds. Closest separation is sampled on 121 points, not a continuous minimum or universal capture guarantee. No actuator limits are included in this comparison.'}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
