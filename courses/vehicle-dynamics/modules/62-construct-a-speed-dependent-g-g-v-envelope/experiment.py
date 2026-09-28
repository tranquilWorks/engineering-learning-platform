from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 62
DEFAULTS = {"speed_m_s": 45.0, "friction_coefficient": 1.20}
RANGES = {"speed_m_s": (20.0, 75.0), "friction_coefficient": (0.8, 1.5)}
BROKEN_TEXT = "Broken mode commands ninety percent of independent TIRE longitudinal and lateral capacities, ignoring the power limit too simultaneously, exceeding the coupled friction boundary."
RECOVERY_TEXT = "Build speed-dependent axle load, power, drag, braking, and lateral limits, then enforce one normalized coupled acceleration boundary."


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


def _forces(v, mu, broken):
    down = 1.53125 * v * v
    drag = 0.441 * v * v
    capacity = mu * (1450 * 9.81 + down)
    power_force = capacity if v == 0 else 210000 / v
    fx = 0.9 * capacity if broken else min(0.6 * capacity, power_force)
    fy = (0.9 if broken else 0.6) * capacity
    return capacity, down, drag, power_force, fx, fy


def _state(v, mu, broken):
    capacity, down, drag, power_force, fx, fy = _forces(v, mu, broken)
    return [
        (min(capacity, power_force) - drag) / 1450,
        (capacity + drag) / 1450,
        capacity / 1450,
        down,
        drag,
        max(0.0, float(np.hypot(fx, fy) / capacity) - 1),
    ]


def run(parameters: dict[str, Any]):
    p = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    sig = _state(p["speed_m_s"], p["friction_coefficient"], broken)
    speeds = np.linspace(20, 75, 80)
    vals = np.array([_state(v, p["friction_coefficient"], broken) for v in speeds])
    ang = np.linspace(0, 2 * np.pi, 121)
    capacity, _down, drag, power_force, fx, fy = _forces(
        p["speed_m_s"], p["friction_coefficient"], broken
    )
    ax = (np.minimum(capacity * np.cos(ang), power_force) - drag) / 1450
    ay = capacity * np.sin(ang) / 1450
    demand = _tr(
        "Actual demand",
        [(fx - drag) / 1450],
        [fy / 1450],
        "Longitudinal acceleration",
        "m/s^2",
        "Lateral acceleration",
        "m/s^2",
    )
    demand["mode"] = "markers"
    return {
        "metrics": [
            {"id": f"m{i}", "label": l, "value": float(v), "unit": u}
            for i, (l, v, u) in enumerate(
                zip(
                    (
                        "Forward acceleration",
                        "Braking acceleration",
                        "Lateral capacity",
                        "Downforce",
                        "Drag",
                        "Coupled-boundary residual",
                    ),
                    sig,
                    ("m/s^2", "m/s^2", "m/s^2", "N", "N", "1"),
                )
            )
        ],
        "plots": {
            "response": _pl(
                "Speed-dependent envelope",
                "Vehicle speed (m/s)",
                "Acceleration limit (m/s^2)",
                [
                    _tr(
                        "Forward",
                        speeds,
                        vals[:, 0],
                        "Vehicle speed",
                        "m/s",
                        "Acceleration limit",
                        "m/s^2",
                    ),
                    _tr(
                        "Lateral",
                        speeds,
                        vals[:, 2],
                        "Vehicle speed",
                        "m/s",
                        "Acceleration limit",
                        "m/s^2",
                    ),
                ],
            ),
            "mechanism": _pl(
                "Coupled acceleration boundary",
                "Longitudinal acceleration (m/s^2)",
                "Lateral acceleration (m/s^2)",
                [
                    _tr(
                        "Force and power boundary",
                        ax,
                        ay,
                        "Longitudinal acceleration",
                        "m/s^2",
                        "Lateral acceleration",
                        "m/s^2",
                    ),
                    demand,
                ],
            ),
        },
        "explanations": {
            "observation": "Power and drag shape the longitudinal axis while aero load and friction shape the shared acceleration boundary.",
            "broken": BROKEN_TEXT,
            "recovery": RECOVERY_TEXT,
        },
        "diagnostics": {
            "item_number": ITEM_NUMBER,
            "broken_active": broken,
            "signature": sig,
            "demand_force_n": [fx, fy],
            "tire_capacity_n": capacity,
            "power_excess_w": max(0.0, fx * p["speed_m_s"] - 210000),
        },
    }
