from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 66
DEFAULTS = {"validation_fraction": 0.3, "fault_severity": 1.0}
RANGES = {"validation_fraction": (0.2, 0.4), "fault_severity": (0.5, 2.0)}
BROKEN_TEXT = "Broken mode leaks validation data into calibration and leaves timing and injected-fault recovery requirements unsigned."
RECOVERY_TEXT = "Replay deterministically, align and calibrate first, preserve a held-out split, trace every requirement, inject a fault, and sign the recovery evidence."


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


def _calc(v, f, broken):
    status = np.ones(9)
    residual = 0.08 + 0.04 * f + 0.02 * (0.3 - v) ** 2
    trace = 0.0
    if broken:
        status[[1, 2, 5, 7]] = 0.0
        residual += 0.45 * f
        trace = 4.0
    sig = [
        float(status.sum()),
        9.0,
        residual,
        float(status.mean()),
        float(1 + (f > 1.4)),
        trace,
        float(status[-1]),
    ]
    return sig, status


def run(parameters: dict[str, Any]):
    p = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    sig, status = _calc(p["validation_fraction"], p["fault_severity"], broken)
    labels = (
        "Requirements passed",
        "Requirements total",
        "Held-out residual",
        "Trace coverage",
        "Fault count",
        "Trace residual",
        "Recovery verdict",
    )
    units = ("count", "count", "1", "fraction", "count", "count", "bool")
    return {
        "metrics": [
            {"id": f"m{i}", "label": l, "value": float(x), "unit": u}
            for i, (l, x, u) in enumerate(zip(labels, sig, units))
        ],
        "plots": {
            "response": _pl(
                "Signed telemetry requirements",
                "Requirement (1)",
                "Pass (bool)",
                [
                    _tr(
                        "Status",
                        np.arange(1, 10),
                        status,
                        "Requirement",
                        "1",
                        "Pass",
                        "bool",
                    )
                ],
            ),
            "mechanism": _pl(
                "Requirement residual",
                "Requirement (1)",
                "Residual (1)",
                [
                    _tr(
                        "Residual",
                        np.arange(1, 10),
                        1 - status,
                        "Requirement",
                        "1",
                        "Residual",
                        "1",
                    )
                ],
            ),
        },
        "explanations": {
            "observation": "The capstone passes only when replay, timing, calibration, state, identification, uncertainty, fault, and recovery evidence are all signed.",
            "broken": BROKEN_TEXT,
            "recovery": RECOVERY_TEXT,
        },
        "diagnostics": {
            "item_number": ITEM_NUMBER,
            "broken_active": broken,
            "signature": sig,
        },
    }
