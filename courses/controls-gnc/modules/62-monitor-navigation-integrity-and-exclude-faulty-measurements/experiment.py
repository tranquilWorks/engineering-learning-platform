from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 62
BROKEN_TEXT = 'Broken mode leaves the alarm computation visible but suppresses exclusion, retaining all eight rows for the final fit.'
RECOVERY_TEXT = 'Disable the fault mode, restore defaults and confirm that the selected row disappears from the refitted residual series and state error decreases.'


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
    sat=_geometry(1.)
    truth=np.array([25.,-12.,20.]); observed=_ranges(sat,truth)[0]+30.+.1*np.array([.4,-.7,.2,.8,-.5,.1,-.3,.6])
    observed[2]+=float(p['fault_magnitude_m'])
    before,pre,H,_=_fix(sat,observed)
    leverage=np.sum(H*(H@np.linalg.inv(H.T@H)),axis=1)
    standardized=pre/np.sqrt(1-leverage)
    suspect=int(np.argmax(abs(standardized))); statistic=float(np.max(abs(standardized)))
    alarm=statistic>float(p['integrity_threshold'])
    retained=np.arange(8)
    if alarm and not broken:
        retained=np.delete(retained,suspect)
    after,post,Hpost,_=_fix(sat[retained],observed[retained])
    covariance=np.linalg.inv(Hpost.T@Hpost)
    signature=[statistic,np.linalg.norm(after[:3]-truth),np.sqrt(np.mean(post**2))]
    return {'signature':signature,'metrics':[
        ('standardized_residual','Largest standardized residual',signature[0],'1'),('position_error','Retained-solution position error',signature[1],'m'),
        ('postfit_rms','Retained post-fit RMS',signature[2],'m'),('formal_horizontal_sigma','Formal horizontal sigma',np.sqrt(np.trace(covariance[:2,:2])),'m')],
        'plots':{'response':_plot('Actual fit residuals','Satellite index (1)','Residual (m)',[
            _trace('Before exclusion',np.arange(8),pre,'Satellite index','1','Residual','m',mode='lines+markers'),
            _trace('Retained and refitted',retained,post,'Satellite index','1','Residual','m',mode='lines+markers')]),
            'mechanism':_plot('Residual test','Satellite index (1)','Standardized magnitude (1)',[
                _trace('Magnitude',np.arange(8),abs(standardized),'Satellite index','1','Standardized magnitude','1'),
                _trace('Threshold',np.arange(8),np.full(8,float(p['integrity_threshold'])),'Satellite index','1','Standardized magnitude','1')])},
        'details':{'satellites':sat,'truth':truth,'observations':observed,'before_state':before,'state':after,'before_residual':pre,'post_residual':post,'retained_rows':retained,'suspect':suspect,'alarm':alarm,'leverage':leverage,'standardized_residual':standardized,'jacobian':Hpost,'covariance':covariance},
        'observation':'An alarm selects the largest leverage-standardized residual. Normal mode removes that measurement and recomputes the solution. The formal one-metre-noise covariance is not a certified protection level or a guarantee against arbitrary multiple faults.'}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
