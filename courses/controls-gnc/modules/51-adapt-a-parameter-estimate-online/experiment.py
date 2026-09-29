from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 51
BROKEN_TEXT = "Broken mode sets the actual regressor to zero and uses the incorrect covariance update lambda*P. The parameter stays at zero while the reported covariance shrinks for lambda<1. The selected forgetting factor remains active."
RECOVERY_TEXT = "Restore excitation and the correct covariance recurrence, then reset the controls. Check estimate motion is accompanied by nonzero regressors and actual information accumulation."


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


def rls_history(forgetting, level, broken=False, noise=0.01):
    k = np.arange(200)
    phi = level * (np.sin(0.31 * k) + 0.4 * np.cos(0.13 * k))
    if broken:
        phi[:] = 0.0
    y = phi + noise * np.sin(0.73 * k)
    theta = [0.0]
    covariance = [10.0]
    gain = []
    for f, measurement in zip(phi, y):
        old = covariance[-1]
        g = old * f / (forgetting + f * f * old)
        theta.append(theta[-1] + g * (measurement - f * theta[-1]))
        gain.append(g)
        covariance.append(
            forgetting * old if broken else (old - g * f * old) / forgetting
        )
    return phi, y, np.array(theta), np.array(covariance), np.array(gain)


def _model(p, broken):
    forgetting = float(p["forgetting_factor"])
    phi, y, theta, cov, gain = rls_history(
        forgetting, float(p["excitation_level"]), broken
    )
    rate = sum(phi * phi) / 10.0
    t = np.arange(201) * 0.05
    model = {
        "signature": [abs(theta[-1] - 1), cov[-1], rate],
        "metrics": [
            ("error", "Final measured parameter error", abs(theta[-1] - 1), "1"),
            ("covariance", "Final RLS covariance scale", cov[-1], "1"),
            ("excitation", "Measured excitation information rate", rate, "1/s"),
        ],
        "plots": {
            "response": _plot(
                "Recursive parameter estimate",
                "Time (s)",
                "Parameter estimate (1)",
                [
                    _trace(
                        "RLS estimate", t, theta, "Time", "s", "Parameter estimate", "1"
                    ),
                    _trace(
                        "Synthetic truth",
                        t,
                        np.ones_like(t),
                        "Time",
                        "s",
                        "Parameter estimate",
                        "1",
                    ),
                ],
            ),
            "mechanism": _plot(
                "Covariance and missing excitation",
                "Time (s)",
                "Covariance scale (1)",
                [
                    _trace(
                        "Reported covariance",
                        t,
                        cov,
                        "Time",
                        "s",
                        "Covariance scale",
                        "1",
                    ),
                    _trace(
                        "Correct zero-excitation evolution",
                        t,
                        10 / forgetting ** np.arange(201),
                        "Time",
                        "s",
                        "Covariance scale",
                        "1",
                    ),
                ],
            ),
        },
        "details": {
            "time": t,
            "regressor": phi,
            "measurement": y,
            "estimate": theta,
            "covariance": cov,
            "gain": gain,
        },
        "observation": "Every estimate and covariance comes from an RLS update. Without excitation the correct covariance cannot shrink. The fault combines zero regressor with the erroneous multiplication by the forgetting factor, producing false confidence without learning.",
    }

    model["plots"]["mechanism"]["layout"]["yaxis"]["type"] = "log"
    return model


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
