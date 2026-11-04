from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 63
BROKEN_TEXT = "Reverse the LOS correction sign in the executed trajectory without changing lookahead or speed."
RECOVERY_TEXT = "Restore the correcting heading sign, reset, and compare terminal cross-track position on the same straight path."


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
        "type": "scattergl",
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
            "broken_active": bool(broken),
            "signature": [float(value) for value in model["signature"]],
            **model.get("history", {}),
        },
    }


def _model(p, broken):
    from scipy.integrate import solve_ivp

    lookahead = float(p["lookahead_distance_m"])
    speed = float(p["vehicle_speed_m_s"])
    sign = 1.0 if broken else -1.0
    time = np.linspace(0, 12, 241)

    def dynamics(_, state):
        heading = sign * np.arctan2(state[1], lookahead)
        return [speed * np.cos(heading), speed * np.sin(heading)]

    h = solve_ivp(dynamics, [0, 12], [0, 10.0], t_eval=time, rtol=2e-11, atol=2e-12).y.T
    heading = sign * np.arctan2(h[:, 1], lookahead)
    return {
        "signature": [
            -sign * speed / lookahead,
            h[-1, 1],
            np.max(np.abs(np.rad2deg(heading))),
        ],
        "metrics": [
            (
                "cross_track_decay_rate",
                "Local cross-track decay rate",
                -sign * speed / lookahead,
                "1/s",
            ),
            (
                "terminal_cross_track_error",
                "Actual nonlinear terminal cross-track error",
                h[-1, 1],
                "m",
            ),
            (
                "peak_heading_command",
                "Actual peak heading command",
                np.max(abs(np.rad2deg(heading))),
                "deg",
            ),
        ],
        "history": {"time": time, "path": h, "heading_rad": heading},
        "plots": {
            "response": _plot(
                "LOS path",
                "Along-track position (m)",
                "Cross-track position (m)",
                [
                    _trace(
                        "Actual path",
                        h[:, 0],
                        h[:, 1],
                        "Along-track position",
                        "m",
                        "Cross-track position",
                        "m",
                    ),
                    _trace(
                        "Desired straight path",
                        h[:, 0],
                        np.zeros_like(time),
                        "Along-track position",
                        "m",
                        "Cross-track position",
                        "m",
                    ),
                ],
            ),
            "mechanism": _plot(
                "LOS heading",
                "Time (s)",
                "Heading correction (deg)",
                [
                    _trace(
                        "Applied LOS",
                        time,
                        np.rad2deg(heading),
                        "Time",
                        "s",
                        "Heading correction",
                        "deg",
                    ),
                    _trace(
                        "Zero correction",
                        time,
                        np.zeros_like(time),
                        "Time",
                        "s",
                        "Heading correction",
                        "deg",
                    ),
                ],
            ),
        },
        "observation": "The vehicle executes x-dot=V cos(chi), y-dot=V sin(chi), chi=-atan(y/L). Exponential convergence is only the local small-error approximation; the plotted path uses nonlinear kinematics. Fault mode reverses the heading sign at unchanged lookahead and speed. Heading tracking is instantaneous; waypoint switching, turn-rate limits and obstacles belong to the later survey capstone.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
