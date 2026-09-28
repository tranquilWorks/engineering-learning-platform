from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 64
DEFAULTS = {"grip_scale": 1.15, "energy_limit_mj": 3.0}
RANGES = {"grip_scale": (0.8, 1.4), "energy_limit_mj": (0.2, 4.0)}
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
        "type": "scatter",
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


def _solve(grip, budget_mj, broken, count=128):
    m, drag_coefficient, rolling = 1450.0, 0.441, 0.012 * 1450 * 9.81
    theta = (np.arange(count) + 0.5) * 2 * np.pi / count
    tangent = np.hypot(180 * np.sin(theta), 90 * np.cos(theta))
    ds = tangent * 2 * np.pi / count
    curvature = 180 * 90 / tangent**3
    capacity = grip * m * 9.81
    longitudinal = 0.5 * capacity
    square = np.minimum(np.sqrt(0.75) * capacity / (m * curvature), 72.0**2)

    def reach(values, braking):
        for iteration in range(512):
            old = values.copy()
            for i in range(count):
                j = (i + 1) % count
                force = min(longitudinal, 210000 / max(np.sqrt(values[i]), 1e-9))
                values[j] = min(
                    values[j],
                    max(
                        0.0,
                        values[i]
                        + 2
                        * ds[i]
                        * (force - drag_coefficient * values[i] - rolling)
                        / m,
                    ),
                )
            if braking:
                for i in reversed(range(count)):
                    j = (i + 1) % count
                    bound = (values[j] + 2 * ds[i] * (longitudinal + rolling) / m) / (
                        1 - 2 * ds[i] * drag_coefficient / m
                    )
                    values[i] = min(values[i], bound)
            if max(abs(values - old)) < 1e-10:
                return values, iteration + 1
        raise ValueError("Cyclic reachability did not converge")

    forward, _ = reach(square.copy(), False)
    square, iterations = reach(square, not broken)
    unconstrained = square.copy()

    def work(values):
        return (
            0.5 * m * (np.roll(values, -1) - values)
            + (drag_coefficient * values + rolling) * ds
        )

    floor = rolling * sum(ds)
    feasible = budget_mj * 1e6 >= floor
    if not feasible:
        square[:] = 0.0
    elif sum(np.maximum(work(square), 0)) > budget_mj * 1e6:
        low, high = 0.0, 1.0
        for _ in range(60):
            middle = (low + high) / 2
            if sum(np.maximum(work(unconstrained * middle), 0)) > budget_mj * 1e6:
                high = middle
            else:
                low = middle
        square = unconstrained * low
    wheel_work = work(square)
    force = wheel_work / ds
    speed = np.sqrt(square)
    allowed = np.minimum(longitudinal, 210000 / np.maximum(speed, 1e-9))
    residual = float(max(0.0, max(force - allowed), max(-force - longitudinal)))
    lateral = m * square * curvature
    utilization = np.hypot(force, lateral) / capacity
    lap = float(sum(ds / speed)) if feasible and min(speed) > 0 else 0.0
    signature = [
        lap,
        float(min(speed)),
        float(max(speed)),
        float(sum(np.maximum(wheel_work, 0)) / 1e6),
        float(20 + sum(np.maximum(-wheel_work, 0)) / (32 * 500)),
        residual,
    ]
    return {
        "signature": signature,
        "distance": np.cumsum(ds) - ds,
        "ds": ds,
        "curvature": curvature,
        "speed": speed,
        "forward_speed": np.sqrt(forward),
        "wheel_work_j": wheel_work,
        "segment_force_n": force,
        "utilization": utilization,
        "iterations": iterations,
        "budget_feasible": bool(feasible),
        "rolling_floor_j": float(floor),
    }


def _calc(g, e, broken):
    r = _solve(g, e, broken)
    return r["signature"], r["distance"], r["curvature"], r["speed"], r["forward_speed"]


def run(parameters: dict[str, Any]):
    p = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    details = _solve(p["grip_scale"], p["energy_limit_mj"], broken)
    sig, s, k, v, pre = (
        details[key]
        for key in ("signature", "distance", "curvature", "speed", "forward_speed")
    )
    labels = (
        "Lap time",
        "Minimum speed",
        "Maximum speed",
        "Energy used",
        "Adiabatic brake temperature",
        "Reachability force excess",
    )
    units = ("s", "m/s", "m/s", "MJ", "degC", "N")
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
            "observation": "A periodic discrete wheel-work model enforces curvature, power and braking, then reduces speed to meet the actual positive-work budget. Below the rolling-work floor, the diagnostic is infeasible and lap time 0 is a sentinel, not a completed lap.",
            "broken": BROKEN_TEXT,
            "recovery": RECOVERY_TEXT,
        },
        "diagnostics": {
            "item_number": ITEM_NUMBER,
            "broken_active": broken,
            "signature": sig,
            **{
                key: value.tolist() if isinstance(value, np.ndarray) else value
                for key, value in details.items()
            },
        },
    }
