from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 56
BROKEN_TEXT = 'Broken mode skips the backward recursion and reports the forward filter as the smoother. Both controls still generate the data and filter covariance.'
RECOVERY_TEXT = 'Disable the fault and reset the two variances. Confirm the last means and variances remain equal while earlier covariance usually falls.'


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
    q = float(p['process_variance'])
    r = float(p['measurement_variance'])
    k = np.arange(41)
    truth = np.r_[0., np.cumsum(np.sqrt(q) * (0.7*np.sin(0.6*k[1:]) + 0.2*np.cos(1.1*k[1:])))]
    measurements = truth + np.sqrt(r)*(0.7*np.cos(1.4*k) + 0.2*np.sin(0.2*k))
    predicted_mean, predicted_variance, filtered_mean, filtered_variance, gains = [], [], [], [], []
    mean, variance = 0., 1.
    for index, value in enumerate(measurements):
        if index:
            variance += q
        predicted_mean.append(mean)
        predicted_variance.append(variance)
        gain = variance / (variance + r)
        mean += gain*(value-mean)
        variance = (1-gain)**2*variance + gain**2*r
        gains.append(gain)
        filtered_mean.append(mean)
        filtered_variance.append(variance)
    fm, fp = np.array(filtered_mean), np.array(filtered_variance)
    sm, sp = fm.copy(), fp.copy()
    smoother_gains = np.zeros(40)
    if not broken:
        for index in range(39,-1,-1):
            gain = fp[index]/predicted_variance[index+1]
            smoother_gains[index] = gain
            sm[index] += gain*(sm[index+1]-predicted_mean[index+1])
            sp[index] += gain**2*(sp[index+1]-predicted_variance[index+1])
    t=k*0.25
    signature = [np.mean(fp),np.mean(sp),np.mean(fp-sp)]
    return {'signature':signature,'metrics':[
        ('filtered_variance','Mean filtered variance',signature[0],'m^2'),
        ('smoothed_variance','Mean reported smoothed variance',signature[1],'m^2'),
        ('variance_reduction','Mean variance reduction',signature[2],'m^2'),
        ('trajectory_rmse','Reported trajectory RMSE',np.sqrt(np.mean((sm-truth)**2)),'m')],
        'plots':{
            'response':_plot('Executed estimates','Time (s)','Position (m)',[
                _trace('Synthetic truth',t,truth,'Time','s','Position','m'),
                _trace('Forward filter',t,fm,'Time','s','Position','m'),
                _trace('Reported smoother',t,sm,'Time','s','Position','m')]),
            'mechanism':_plot('Filter/smoother covariance','Time (s)','Position variance (m²)',[
                _trace('Filtered covariance',t,fp,'Time','s','Position variance','m^2'),
                _trace('Reported smoothed covariance',t,sp,'Time','s','Position variance','m^2')])},
        'details':{'time':t,'truth':truth,'measurements':measurements,'predicted_mean':predicted_mean,
            'predicted_variance':predicted_variance,'filtered_mean':fm,'filtered_variance':fp,
            'smoothed_mean':sm,'smoothed_variance':sp,'filter_gains':gains,'smoother_gains':smoother_gains},
        'observation':'The plotted smoother executes a backward RTS pass over all 41 retained measurements. Its last state/covariance equal the filter. Model covariance reduction does not guarantee a smaller error for every individual measurement realization.'}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
