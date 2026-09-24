from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 67
DEFAULTS = {"setup_delta": 0.08, "uncertainty_fraction": 0.05}
RANGES = {"setup_delta": (0.02, 0.15), "uncertainty_fraction": (0.02, 0.1)}
BROKEN_TEXT = "Broken mode double-counts aerodynamic grip, so the coupled prediction violates its signed tire-aero ledger and four requirements fail."
RECOVERY_TEXT = "Reconcile tire, chassis, propulsion, brake, aero, track, line, lap, uncertainty, and setup ledgers once, then sign all eleven requirements."


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
        "type": "bar",
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


def _calc(d, u, broken):
    lap = 92.0 - 20 * d
    status = np.ones(11)
    residual = 0.0
    if broken:
        status[[1, 4, 7, 9]] = 0.0
        residual = 0.35 + d
    sig = [float(status.sum()), 11.0, lap, lap * u, 20 * d, residual, float(status[-1])]
    return sig, status, np.array([92.0, lap])


def run(parameters: dict[str, Any]):
    p = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    sig, status, laps = _calc(p["setup_delta"], p["uncertainty_fraction"], broken)
    labels = (
        "Requirements passed",
        "Requirements total",
        "Predicted lap",
        "Uncertainty bound",
        "Setup delta time",
        "Coupled residual",
        "Recovery verdict",
    )
    units = ("count", "count", "s", "s", "s", "1", "bool")
    return {
        "metrics": [
            {"id": f"m{i}", "label": l, "value": float(x), "unit": u}
            for i, (l, x, u) in enumerate(zip(labels, sig, units))
        ],
        "plots": {
            "response": _pl(
                "Digital-twin requirements",
                "Requirement (1)",
                "Pass (bool)",
                [
                    _tr(
                        "Status",
                        np.arange(1, 12),
                        status,
                        "Requirement",
                        "1",
                        "Pass",
                        "bool",
                    )
                ],
            ),
            "mechanism": _pl(
                "Setup prediction",
                "Setup (1)",
                "Lap time (s)",
                [_tr("Lap", np.arange(2), laps, "Setup", "1", "Lap time", "s")],
            ),
        },
        "explanations": {
            "observation": "A cumulative digital twin is credible only when every subsystem ledger, uncertainty bound, and setup prediction is traceable and signed.",
            "broken": BROKEN_TEXT,
            "recovery": RECOVERY_TEXT,
        },
        "diagnostics": {
            "item_number": ITEM_NUMBER,
            "broken_active": broken,
            "signature": sig,
        },
    }
