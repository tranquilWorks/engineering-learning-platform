from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 36
BROKEN_TEXT = "Broken mode uses Nbar=1/s² while retaining K and both propagated states. The baseline final-value position becomes 1/8 m even though both poles remain stable."
RECOVERY_TEXT = "Disable broken mode and reset both controls. Check steady tracking error returns to zero and compare the two acceleration traces again."


def _trace(
    name: str,
    x: Any,
    y: Any,
    x_quantity: str,
    x_unit: str,
    y_quantity: str,
    y_unit: str,
    *,
    mode: str = "lines",
) -> dict[str, Any]:
    return {
        "type": "scatter",
        "mode": mode,
        "name": name,
        "x": np.asarray(x, dtype=float),
        "y": np.asarray(y, dtype=float),
        "meta": {
            "x_quantity": x_quantity,
            "x_unit": x_unit,
            "y_quantity": y_quantity,
            "y_unit": y_unit,
        },
    }


def _plot(
    title: str, x_title: str, y_title: str, traces: list[dict[str, Any]]
) -> dict[str, Any]:
    return {
        "data": traces,
        "layout": {
            "title": {"text": title, "x": 0.02},
            "xaxis": {"title": {"text": x_title}},
            "yaxis": {"title": {"text": y_title}},
            "legend": {"orientation": "h"},
            "margin": {"l": 72, "r": 36, "t": 62, "b": 62},
            "hovermode": "closest",
            "uirevision": "keep-view",
        },
        "config": {"responsive": True, "displaylogo": False},
    }


def _result(model: dict[str, Any], broken: bool) -> dict[str, Any]:
    return {
        "metrics": [
            {
                "id": key,
                "label": label,
                "value": float(value),
                "unit": unit,
                "emphasis": "primary" if index == 0 else "normal",
            }
            for index, (key, label, value, unit) in enumerate(model["metrics"])
        ],
        "plots": model["plots"],
        "explanations": {
            "observation": model["observation"],
            "broken": BROKEN_TEXT,
            "recovery": RECOVERY_TEXT,
        },
        "diagnostics": {
            "item_number": ITEM_NUMBER,
            **model.get("details", {}),
            "broken_active": bool(broken),
            "signature": [float(value) for value in model["signature"]],
        },
    }


def _model(p, broken):
    from scipy.linalg import expm

    a = float(p["dominant_pole_per_s"])
    b = a * float(p["pole_ratio"])
    kp, kd = a * b, a + b
    feed = 1.0 if broken else kp
    closed = np.array([[0.0, 1.0], [-kp, -kd]])
    t = np.linspace(0.0, 8 / a, 240)
    equilibrium = np.array([feed / kp, 0.0])
    states = np.array([equilibrium - expm(closed * tt) @ equilibrium for tt in t])
    y, v = states.T
    u = feed - kp * y - kd * v
    pole_error = np.max(abs(np.sort(np.linalg.eigvals(closed)) - np.sort([-a, -b])))
    return {
        "signature": [pole_error, abs(1 - feed / kp), kp, kd],
        "metrics": [
            ("pole_error", "Pole assignment error", pole_error, "1/s"),
            ("tracking_error", "Steady tracking error", abs(1 - feed / kp), "1"),
            ("position_gain", "Position feedback gain", kp, "1/s^2"),
            ("velocity_gain", "Velocity feedback gain", kd, "1/s"),
        ],
        "plots": {
            "response": _plot(
                "Reference tracking",
                "Time (s)",
                "Position (m)",
                [
                    _trace("Position", t, y, "Time", "s", "Position", "m"),
                    _trace(
                        "Reference", t, np.ones_like(t), "Time", "s", "Position", "m"
                    ),
                ],
            ),
            "mechanism": _plot(
                "Full feedback command",
                "Time (s)",
                "Acceleration (m/s^2)",
                [
                    _trace(
                        "Applied acceleration",
                        t,
                        u,
                        "Time",
                        "s",
                        "Acceleration",
                        "m/s^2",
                    ),
                    _trace(
                        "Position term only (incomplete)",
                        t,
                        feed - kp * y,
                        "Time",
                        "s",
                        "Acceleration",
                        "m/s^2",
                    ),
                ],
            ),
        },
        "details": {
            "time": t,
            "position": y,
            "velocity": v,
            "acceleration": u,
            "gains": [kp, kd],
            "feedforward": feed,
        },
        "observation": "Acceleration includes position AND velocity feedback. The comparison omits velocity and does not drive the plotted state. Stable poles alone do not ensure unit DC tracking.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
