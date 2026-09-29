from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 45
BROKEN_TEXT = "Broken mode bypasses the filter and continuously applies the selected nominal closing speed. At the default speed, clearance crosses zero within three seconds; slower closing can stay positive throughout this finite window. No control setting is secretly replaced."
RECOVERY_TEXT = "Disable broken mode and reset controls. Inspect the entire clearance history, not just its first sample, and verify a nonnegative minimum barrier residual."


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
    alpha = float(p["barrier_gain_per_s"])
    speed = float(p["nominal_closing_speed"])
    dt = 0.01
    t = np.arange(301) * dt
    h = np.zeros(len(t))
    h[0] = 0.4
    u = np.zeros(len(t))
    for j in range(len(t)):
        u[j] = -speed if broken else max(-speed, -alpha * h[j])
        if j < len(t) - 1:
            h[j + 1] = h[j] + dt * u[j]
    residual = u + alpha * h
    intervention = u + speed
    return {
        "signature": [u[0], min(h), max(intervention)],
        "metrics": [
            ("first", "First filtered command", u[0], "m/s"),
            ("margin", "Minimum safety margin", min(h), "m"),
            ("intervention", "Peak intervention", max(intervention), "m/s"),
            ("residual", "Minimum barrier residual", min(residual), "m/s"),
        ],
        "plots": {
            "response": _plot(
                "Safety margin over time",
                "Time (s)",
                "Safety margin (m)",
                [
                    _trace("Actual clearance", t, h, "Time", "s", "Safety margin", "m"),
                    _trace(
                        "Boundary",
                        t,
                        np.zeros_like(t),
                        "Time",
                        "s",
                        "Safety margin",
                        "m",
                    ),
                ],
            ),
            "mechanism": _plot(
                "State-dependent barrier filter",
                "Time (s)",
                "Velocity (m/s)",
                [
                    _trace("Applied command", t, u, "Time", "s", "Velocity", "m/s"),
                    _trace(
                        "Nominal command",
                        t,
                        -speed * np.ones_like(t),
                        "Time",
                        "s",
                        "Velocity",
                        "m/s",
                    ),
                    _trace(
                        "Barrier residual", t, residual, "Time", "s", "Velocity", "m/s"
                    ),
                ],
            ),
        },
        "details": {
            "time": t,
            "clearance": h,
            "command": u,
            "barrier_residual": residual,
            "sample_period": dt,
        },
        "observation": "The filter is recomputed every 0.01 s. With alpha*dt <= 0.08, the sampled update preserves nonnegative clearance. Bypassing the filter applies the selected closing speed; a boundary crossing can occur inside or after the three-second observation window.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
