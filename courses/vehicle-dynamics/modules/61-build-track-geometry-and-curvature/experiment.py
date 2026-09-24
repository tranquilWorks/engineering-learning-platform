from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 61
DEFAULTS = {"major_radius_m": 60.0, "point_count": 181.0}
RANGES = {"major_radius_m": (40.0, 80.0), "point_count": (61.0, 301.0)}
BROKEN_TEXT = "Broken mode truncates the closed track before the final arc and reports geometry with a large position and heading closure error."
RECOVERY_TEXT = "Parameterize one complete closed loop, differentiate with the same parameter, preserve signed curvature, and verify position, heading, and total-curvature closure."


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


def _calc(a, n, broken):
    end = 1.8 * np.pi if broken else 2 * np.pi
    q = np.linspace(0, end, n)
    b = 0.6 * a
    x = a * np.cos(q)
    y = b * np.sin(q)
    dx = -a * np.sin(q)
    dy = b * np.cos(q)
    ddx = -a * np.cos(q)
    ddy = -b * np.sin(q)
    k = (dx * ddy - dy * ddx) / (dx * dx + dy * dy) ** 1.5
    ds = np.hypot(np.diff(x), np.diff(y))
    length = float(ds.sum())
    closure = float(np.hypot(x[-1] - x[0], y[-1] - y[0]))
    heading = np.unwrap(np.arctan2(dy, dx))
    integral = float(np.sum(0.5 * (k[:-1] + k[1:]) * ds))
    sig = [
        length,
        float(np.max(np.abs(k))),
        float(np.mean(k)),
        float(np.rad2deg(heading[-1] - heading[0])),
        closure,
        abs(integral - 2 * np.pi),
    ]
    return sig, q, x, y, k


def run(parameters: dict[str, Any]):
    p = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    sig, q, x, y, k = _calc(p["major_radius_m"], round(p["point_count"]), broken)
    return {
        "metrics": [
            {"id": f"m{i}", "label": l, "value": float(v), "unit": u}
            for i, (l, v, u) in enumerate(
                zip(
                    (
                        "Track length",
                        "Peak curvature",
                        "Mean curvature",
                        "Heading closure",
                        "Position closure",
                        "Curvature integral residual",
                    ),
                    sig,
                    ("m", "1/m", "1/m", "deg", "m", "rad"),
                )
            )
        ],
        "plots": {
            "response": _pl(
                "Closed track geometry",
                "East position (m)",
                "North position (m)",
                [_tr("Centerline", x, y, "East position", "m", "North position", "m")],
            ),
            "mechanism": _pl(
                "Signed curvature",
                "Path parameter (rad)",
                "Curvature (1/m)",
                [_tr("Curvature", q, k, "Path parameter", "rad", "Curvature", "1/m")],
            ),
        },
        "explanations": {
            "observation": "A usable track representation closes in position and heading and integrates signed curvature to one full turn.",
            "broken": BROKEN_TEXT,
            "recovery": RECOVERY_TEXT,
        },
        "diagnostics": {
            "item_number": ITEM_NUMBER,
            "broken_active": broken,
            "signature": sig,
        },
    }
