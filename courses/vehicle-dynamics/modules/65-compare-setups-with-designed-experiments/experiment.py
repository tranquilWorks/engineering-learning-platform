from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 65
DEFAULTS = {"aero_scale": 1.0, "tire_scale": 1.0}
RANGES = {"aero_scale": (0.8, 1.2), "tire_scale": (0.85, 1.15)}
BROKEN_TEXT = "Broken mode uses only the confounded diagonal of the factorial and cannot identify the interaction."
RECOVERY_TEXT = "Restore the balanced four-corner design, fit main and interaction effects, inspect rank and residuals, then compare the predicted optimum."


def _parameters(s):
    r = {}
    for k, d in DEFAULTS.items():
        v = float(s.get(k, d))
        lo, hi = RANGES[k]
        if not np.isfinite(v) or v < lo or v > hi:
            raise ValueError(f"{k} outside declared finite range [{lo}, {hi}]")
        r[k] = v
    return r


def _tr(n, x, y, xq, xu, yq, yu):
    return {
        "type": "scattergl",
        "mode": "lines+markers",
        "name": n,
        "x": np.asarray(x),
        "y": np.asarray(y),
        "meta": {"x_quantity": xq, "x_unit": xu, "y_quantity": yq, "y_unit": yu},
    }


def _pl(t, xt, yt, d):
    return {
        "data": d,
        "layout": {
            "title": {"text": t},
            "xaxis": {"title": {"text": xt}},
            "yaxis": {"title": {"text": yt}},
        },
        "config": {"responsive": True, "displaylogo": False},
    }


def _calc(a, t, broken):
    x = np.array([[-1, -1], [-1, 1], [1, -1], [1, 1]], float)
    y = 90 - 2 * a * x[:, 0] - 3 * t * x[:, 1] - 1.2 * a * t * x[:, 0] * x[:, 1]
    if broken:
        X = np.c_[np.ones(2), x[[0, 3]]]
        yy = y[[0, 3]]
        coef = np.linalg.lstsq(X, yy, rcond=None)[0]
        pred = np.c_[np.ones(4), x] @ coef
        interaction = 0.0
        rank = float(np.linalg.matrix_rank(X))
    else:
        X = np.c_[np.ones(4), x, x[:, 0] * x[:, 1]]
        coef = np.linalg.solve(X, y)
        pred = X @ coef
        interaction = float(coef[3])
        rank = float(np.linalg.matrix_rank(X))
    res = float(np.sqrt(np.mean((pred - y) ** 2)))
    sig = [
        round(float(v), 12)
        for v in (
            -2 * coef[1],
            -2 * coef[2],
            -4 * interaction,
            res,
            y.min(),
            rank,
            abs(pred[-1] - y[-1]),
        )
    ]
    return sig, np.arange(4), y, pred


def run(parameters: dict[str, Any]):
    p = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    sig, i, y, pred = _calc(p["aero_scale"], p["tire_scale"], broken)
    labels = (
        "Aero main effect",
        "Tire main effect",
        "Interaction effect",
        "Residual RMS",
        "Best lap",
        "Design rank",
        "Held-out error",
    )
    units = ("s", "s", "s", "s", "s", "1", "s")
    return {
        "metrics": [
            {"id": f"m{j}", "label": l, "value": float(v), "unit": u}
            for j, (l, v, u) in enumerate(zip(labels, sig, units))
        ],
        "plots": {
            "response": _pl(
                "Factorial lap responses",
                "Design corner (1)",
                "Lap time (s)",
                [
                    _tr("Observed", i, y, "Design corner", "1", "Lap time", "s"),
                    _tr("Model", i, pred, "Design corner", "1", "Lap time", "s"),
                ],
            ),
            "mechanism": _pl(
                "Model residual",
                "Design corner (1)",
                "Residual (s)",
                [_tr("Residual", i, pred - y, "Design corner", "1", "Residual", "s")],
            ),
        },
        "explanations": {
            "observation": "A balanced factorial separates two main effects from their interaction and exposes lack of fit.",
            "broken": BROKEN_TEXT,
            "recovery": RECOVERY_TEXT,
        },
        "diagnostics": {
            "item_number": ITEM_NUMBER,
            "broken_active": broken,
            "signature": sig,
        },
    }
