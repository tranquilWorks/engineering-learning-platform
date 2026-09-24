from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 62
DEFAULTS = {"speed_m_s": 45.0, "friction_coefficient": 1.20}
RANGES = {"speed_m_s": (20.0, 75.0), "friction_coefficient": (0.8, 1.5)}
BROKEN_TEXT = "Broken mode commands ninety percent of independent longitudinal and lateral limits simultaneously, exceeding the coupled friction boundary."
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


def _state(v, mu, broken):
    m = 1450.0
    g = 9.81
    down = 0.5 * 1.225 * 2.0 * 1.25 * v * v
    drag = 0.5 * 1.225 * 2.0 * 0.36 * v * v
    cap = mu * (m * g + down)
    accel = max(0.0, min(cap, 210000.0 / v) - drag) / m
    brake = (cap + drag) / m
    lat = cap / m
    util = np.hypot(0.9, 0.9) if broken else 1.0
    residual = max(0.0, util - 1.0)
    return [accel, brake, lat, down, drag, residual]


def run(parameters: dict[str, Any]):
    p = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    sig = _state(p["speed_m_s"], p["friction_coefficient"], broken)
    speeds = np.linspace(20, 75, 80)
    vals = np.array([_state(v, p["friction_coefficient"], broken) for v in speeds])
    ang = np.linspace(0, 2 * np.pi, 121)
    ax = 0.9 * sig[0] * np.cos(ang)
    ay = 0.9 * sig[2] * np.sin(ang)
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
                        "Boundary",
                        ax,
                        ay,
                        "Longitudinal acceleration",
                        "m/s^2",
                        "Lateral acceleration",
                        "m/s^2",
                    )
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
        },
    }
