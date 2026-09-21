from __future__ import annotations

from typing import Any

import numpy as np

WHEEL_SOURCE = "pinned MATLAB model.m"


def _layout(title: str, x: str, y: str, equal: bool = False) -> dict[str, Any]:
    layout: dict[str, Any] = {
        "title": {"text": title, "x": 0.02},
        "xaxis": {"title": x},
        "yaxis": {"title": y},
        "legend": {"orientation": "h"},
        "margin": {"l": 65, "r": 20, "t": 55, "b": 55},
        "hovermode": "closest",
        "uirevision": "keep-view",
    }
    if equal:
        layout["yaxis"]["scaleanchor"] = "x"
    return layout


def _trace(name: str, x: Any, y: Any, dash: str | None = None) -> dict[str, Any]:
    trace: dict[str, Any] = {"type": "scatter", "mode": "lines", "name": name, "x": x, "y": y}
    if dash:
        trace["line"] = {"dash": dash}
    return trace


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    left = float(parameters["left_wheel_rad_s"])
    right = float(parameters["right_wheel_rad_s"])
    radius = float(parameters["wheel_radius_m"])
    track = float(parameters["track_width_m"])
    duration = float(parameters["duration_s"])
    broken = bool(parameters["broken_mode"])
    t = np.linspace(0.0, duration, 401)
    v_left = radius * left
    v_right = radius * right
    speed = 0.5 * (v_left + v_right)
    yaw_rate = (v_right - v_left) / track
    heading = yaw_rate * t
    if broken or abs(yaw_rate) < 1e-12:
        x = speed * t
        y = np.zeros_like(t)
    else:
        turn_radius = speed / yaw_rate
        x = turn_radius * np.sin(heading)
        y = turn_radius * (1.0 - np.cos(heading))
    path_length = abs(speed) * duration
    signature = [speed, yaw_rate, x[-1], y[-1], heading[-1], path_length]
    observation = (
        "Average wheel rim speed sets forward motion; their difference and track width set yaw. "
        "The path uses the exact constant-command arc."
    )
    broken_text = (
        "Decoupled translation keeps world y at zero while heading changes, violating the "
        "body-to-world velocity rotation."
    )
    recovery = "Disable broken mode so translation follows the instantaneous body heading."
    return {
        "metrics": [
            {"id": "forward_speed", "label": "Forward speed", "value": speed, "unit": "m/s", "emphasis": "primary"},
            {"id": "yaw_rate", "label": "Yaw rate", "value": yaw_rate, "unit": "rad/s"},
            {"id": "final_heading", "label": "Final heading", "value": np.degrees(heading[-1]), "unit": "deg"},
            {"id": "path_length", "label": "Path length", "value": path_length, "unit": "m"},
        ],
        "plots": {
            "response": {
                "data": [_trace("Robot center", x, y), _trace("World +x reference", [0.0, speed * duration], [0.0, 0.0], "dot")],
                "layout": _layout("Differential-drive path", "World x (m)", "World y (m)", True),
                "config": {"responsive": True, "displaylogo": False},
            },
            "mechanism": {
                "data": [_trace("Heading", t, np.degrees(heading)), _trace("Yaw-rate reference", t, np.full_like(t, np.degrees(yaw_rate)), "dash")],
                "layout": _layout("Heading accumulation", "Time (s)", "Heading (deg)"),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {"observation": observation, "broken": broken_text, "recovery": recovery},
        "diagnostics": {"item_id": "P01", "source_basis": WHEEL_SOURCE, "broken_active": broken, "sample_count": len(t), "signature": [float(v) for v in signature]},
    }
