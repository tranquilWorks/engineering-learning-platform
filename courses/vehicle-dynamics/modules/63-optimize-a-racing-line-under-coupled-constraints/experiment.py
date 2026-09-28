from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 63
DEFAULTS = {"maximum_offset_m": 3.0, "smoothness_weight": 0.02}
RANGES = {"maximum_offset_m": (1.0, 5.0), "smoothness_weight": (0.0, 0.1)}
BROKEN_TEXT = "Broken mode selects an offset beyond the track boundary and reports an infeasible line as the fastest candidate."
RECOVERY_TEXT = "Bound lateral offset by track width, transform curvature consistently, enforce the lateral speed limit, and rank only feasible candidates."


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
        "type": "scatter",
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


def _geometry(n=256, a=180.0, b=90.0):
    theta = (np.arange(n) + 0.5) * 2 * np.pi / n
    tangent_norm = np.hypot(a * np.sin(theta), b * np.cos(theta))
    return tangent_norm * 2 * np.pi / n, a * b / tangent_norm**3


def _line(offset, ds, curvature):
    scale = 1 - offset * curvature
    shifted_ds, shifted_k = ds * scale, curvature / scale
    speed = np.sqrt(11.5 / shifted_k)
    return shifted_ds, shifted_k, speed, float(np.sum(shifted_ds / speed))


def _calc(bound, w, broken):
    ds, base = _geometry()
    candidates = np.linspace(-bound, bound, 41)
    times = np.array([_line(o, ds, base)[3] for o in candidates])
    offset = float(candidates[np.argmin(times + w * candidates**2)])
    if broken:
        offset = 1.2 * bound  # explicitly injected infeasible candidate
    distance, curvature, speed, time = _line(offset, ds, base)
    baseline = _line(0, ds, base)[3]
    signature = [
        offset,
        float(sum(distance)),
        float(max(curvature)),
        float(min(speed)),
        baseline - time,
        float(bound - abs(offset)),
        max(0.0, abs(offset) - bound),
    ]
    return signature, candidates, times, np.cumsum(distance) / sum(distance), curvature


def run(parameters: dict[str, Any]):
    p = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    sig, c, t, s, k = _calc(p["maximum_offset_m"], p["smoothness_weight"], broken)
    return {
        "metrics": [
            {"id": f"m{i}", "label": l, "value": float(v), "unit": u}
            for i, (l, v, u) in enumerate(
                zip(
                    (
                        "Selected offset",
                        "Line length",
                        "Peak curvature",
                        "Minimum speed",
                        "Travel time improvement",
                        "Boundary margin",
                        "Feasibility residual",
                    ),
                    sig,
                    ("m", "m", "1/m", "m/s", "s", "m", "m"),
                )
            )
        ],
        "plots": {
            "response": _pl(
                "Racing-line candidate time",
                "Line offset (m)",
                "Estimated time (s)",
                [_tr("Candidate", c, t, "Line offset", "m", "Estimated time", "s")],
            ),
            "mechanism": _pl(
                "Selected-line curvature",
                "Normalized distance (1)",
                "Curvature (1/m)",
                [
                    _tr(
                        "Curvature",
                        s,
                        k,
                        "Normalized distance",
                        "1",
                        "Curvature",
                        "1/m",
                    )
                ],
            ),
        },
        "explanations": {
            "observation": "A faster candidate matters only if its offset stays inside track width and its curvature respects the lateral speed envelope.",
            "broken": BROKEN_TEXT,
            "recovery": RECOVERY_TEXT,
        },
        "diagnostics": {
            "item_number": ITEM_NUMBER,
            "broken_active": broken,
            "signature": sig,
        },
    }
