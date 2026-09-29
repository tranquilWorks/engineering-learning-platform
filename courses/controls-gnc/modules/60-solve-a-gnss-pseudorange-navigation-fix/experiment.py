from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 60
BROKEN_TEXT = 'Broken mode omits the clock column and forces the fit to explain clock-biased measurements with three position coordinates.'
RECOVERY_TEXT = 'Restore the fourth unknown, reset both controls and verify the post-fit residual and position/clock errors recover.'


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


def _geometry(concentration):
    az = np.array([0., 47., 99., 146., 201., 249., 294., 337.])*np.pi/180/concentration
    el = np.array([18., 55., 32., 73., 24., 61., 40., 16.])*np.pi/180
    el = .6+(el-.6)/np.sqrt(concentration)
    return 2.e7*np.column_stack([np.cos(el)*np.cos(az),np.cos(el)*np.sin(az),np.sin(el)])


def _ranges(sat, position):
    radius=np.linalg.norm(sat,axis=1)
    delta=-2*sat@position+position@position
    distance=np.sqrt(radius**2+delta)
    return delta/(distance+radius), (position-sat)/distance[:,None]


def _fix(sat, observed, clock=True):
    state=np.zeros(4 if clock else 3)
    history=[]
    for _ in range(12):
        ranges,jac=_ranges(sat,state[:3])
        H=np.column_stack([jac,np.ones(len(sat))]) if clock else jac
        residual=observed-ranges-(state[3] if clock else 0.)
        step=np.linalg.lstsq(H,residual,rcond=None)[0]
        state+=step
        history.append(state.copy())
        if np.linalg.norm(step)<1e-10:
            break
    ranges,jac=_ranges(sat,state[:3])
    H=np.column_stack([jac,np.ones(len(sat))]) if clock else jac
    residual=observed-ranges-(state[3] if clock else 0.)
    return state,residual,H,np.asarray(history)
def _model(p, broken):
    sat=_geometry(float(p['geometry_dilution']))
    truth=np.array([25.,-12.,20.]); clock=30.
    noise=float(p['pseudorange_noise_m'])*np.array([.4,-.7,.2,.8,-.5,.1,-.3,.6])
    observed=_ranges(sat,truth)[0]+clock+noise
    state,residual,H,history=_fix(sat,observed,not broken)
    fullH=np.column_stack([_ranges(sat,state[:3])[1],np.ones(8)])
    covariance=np.linalg.inv(fullH.T@fullH)
    signature=[np.linalg.norm(state[:3]-truth),abs((state[3] if not broken else 0.)-clock),np.sqrt(np.mean(residual**2))]
    return {'signature':signature,'metrics':[
        ('position_error','Position error',signature[0],'m'),('clock_error','Clock-range error',signature[1],'m'),
        ('residual_rms','Post-fit RMS',signature[2],'m'),('pdop','Computed position dilution',np.sqrt(np.trace(covariance[:3,:3])),'1')],
        'plots':{'response':_plot('Position iteration','Iteration (1)','Position (m)',[
            _trace(name,np.arange(1,len(history)+1),history[:,j],'Iteration','1','Position','m') for j,name in enumerate(['x','y','z'])]),
            'mechanism':_plot('Fitted range residuals','Satellite index (1)','Residual (m)',[
                _trace('Post-fit residual',np.arange(8),residual,'Satellite index','1','Residual','m',mode='lines+markers')])},
        'details':{'satellites':sat,'truth':truth,'true_clock_m':clock,'observations':observed,'state':state,'residual':residual,'jacobian':H,'covariance':covariance,'iterations':history,'condition_number':np.linalg.cond(fullH)},
        'observation':'Eight synthetic pseudoranges determine position and clock by nonlinear least squares. Concentration changes actual lines of sight; position dilution is computed from the fitted geometry. This omits atmospheric, orbital and Earth-rotation errors.'}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
