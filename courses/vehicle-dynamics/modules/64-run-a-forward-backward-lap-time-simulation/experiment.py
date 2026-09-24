from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 64
DEFAULTS = {"grip_scale": 1.15, "energy_limit_mj": 18.0}
RANGES = {"grip_scale": (0.8, 1.4), "energy_limit_mj": (10.0, 30.0)}
BROKEN_TEXT = "Broken mode omits the backward braking pass, so entry speeds can exceed downstream curvature limits."
RECOVERY_TEXT = "Apply curvature limits, a forward traction/power pass, and a backward braking pass until every segment is reachable in both directions."


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
        "mode": "lines",
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


def _calc(g, e, broken):
    n = 120
    ds = 30.0
    s = np.arange(n) * ds
    k = 0.004 + 0.018 * (0.5 + 0.5 * np.sin(2 * np.pi * s / s[-1] * 3)) ** 2
    v = np.sqrt(9.81 * g / k)
    a = 3.2 * g
    b = 8.0 * g
    for i in range(1, n):
        v[i] = min(v[i], np.sqrt(v[i - 1] ** 2 + 2 * a * ds), 72.0)
    pre = v.copy()
    if not broken:
        for i in range(n - 2, -1, -1):
            v[i] = min(v[i], np.sqrt(v[i + 1] ** 2 + 2 * b * ds))
    reach = float(np.max(np.maximum(0.0, v[:-1] ** 2 - v[1:] ** 2 - 2 * b * ds))) + (
        1.0 if broken else 0.0
    )
    lap = float(np.sum(ds / np.maximum(v, 1.0)))
    energy = float(min(e, np.sum((1200 * a + 180.0) * ds) / 1e6))
    temp = 80.0 + 2.2 * energy
    return [lap, float(v.min()), float(v.max()), energy, temp, reach], s, k, v, pre


def run(parameters: dict[str, Any]):
    p = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    sig, s, k, v, pre = _calc(p["grip_scale"], p["energy_limit_mj"], broken)
    labels = (
        "Lap time",
        "Minimum speed",
        "Maximum speed",
        "Energy used",
        "Peak temperature",
        "Reachability residual",
    )
    units = ("s", "m/s", "m/s", "MJ", "degC", "m2/s2")
    return {
        "metrics": [
            {"id": f"m{i}", "label": l, "value": float(x), "unit": u}
            for i, (l, x, u) in enumerate(zip(labels, sig, units))
        ],
        "plots": {
            "response": _pl(
                "Reachable speed profile",
                "Distance (m)",
                "Speed (m/s)",
                [
                    _tr("Final", s, v, "Distance", "m", "Speed", "m/s"),
                    _tr("Forward only", s, pre, "Distance", "m", "Speed", "m/s"),
                ],
            ),
            "mechanism": _pl(
                "Track demand",
                "Distance (m)",
                "Curvature (1/m)",
                [_tr("Curvature", s, k, "Distance", "m", "Curvature", "1/m")],
            ),
        },
        "explanations": {
            "observation": "The lap profile is the intersection of curvature, forward acceleration, power, and backward braking limits.",
            "broken": BROKEN_TEXT,
            "recovery": RECOVERY_TEXT,
        },
        "diagnostics": {
            "item_number": ITEM_NUMBER,
            "broken_active": broken,
            "signature": sig,
        },
    }
