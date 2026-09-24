from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 63
DEFAULTS = {"maximum_offset_m": 3.0, "smoothness_weight": 0.50}
RANGES = {"maximum_offset_m": (1.0, 5.0), "smoothness_weight": (0.0, 1.5)}
BROKEN_TEXT = "Broken mode selects an offset beyond the track boundary and reports an infeasible line as the fastest candidate."
RECOVERY_TEXT = "Bound lateral offset by track width, transform curvature consistently, enforce the coupled speed limit, and rank only feasible candidates."


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


def _calc(bound, w, broken):
    s = np.linspace(0, 1, 160)
    base = 0.008 + 0.012 * (np.sin(2 * np.pi * s) ** 2)
    candidates = np.linspace(-bound, bound, 41)
    score = []
    times = []
    for o in candidates:
        k = base / (1 - o * base)
        length = 4200 * (1 + 0.0008 * o * o)
        speed = np.sqrt(11.5 / np.maximum(k, 1e-6))
        time = length / np.mean(speed)
        times.append(time)
        score.append(time + w * o * o)
    idx = int(np.argmin(score))
    offset = float(candidates[idx])
    residual = 0.0
    if broken:
        offset = 1.2 * bound
        residual = offset - bound
    k = base / (1 - offset * base)
    length = 4200 * (1 + 0.0008 * offset * offset)
    speed = np.sqrt(11.5 / k)
    baseline = 4200 / np.mean(np.sqrt(11.5 / base))
    sig = [
        offset,
        length,
        float(k.max()),
        float(speed.min()),
        float(baseline - length / np.mean(speed)),
        float(bound - abs(offset)),
        float(max(0, residual)),
    ]
    return sig, candidates, np.asarray(times), s, k


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
                        "Objective improvement",
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
            "observation": "A faster candidate matters only if its offset stays inside track width and its curvature respects the coupled speed envelope.",
            "broken": BROKEN_TEXT,
            "recovery": RECOVERY_TEXT,
        },
        "diagnostics": {
            "item_number": ITEM_NUMBER,
            "broken_active": broken,
            "signature": sig,
        },
    }
