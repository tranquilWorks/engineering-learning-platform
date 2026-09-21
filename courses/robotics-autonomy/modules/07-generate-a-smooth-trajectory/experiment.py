from __future__ import annotations

from typing import Any

import numpy as np


def _layout(title: str, x: str, y: str) -> dict[str, Any]:
    return {"title": {"text": title, "x": 0.02}, "xaxis": {"title": x}, "yaxis": {"title": y}, "legend": {"orientation": "h"}, "margin": {"l": 65, "r": 20, "t": 55, "b": 55}, "hovermode": "closest", "uirevision": "keep-view"}


def _trace(name: str, x: Any, y: Any) -> dict[str, Any]:
    return {"type": "scatter", "mode": "lines", "name": name, "x": x, "y": y}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    distance = float(parameters["distance_m"])
    duration = float(parameters["duration_s"])
    broken = bool(parameters["broken_mode"])
    t = np.linspace(0.0, duration, 501)
    tau = t / duration
    if broken:
        progress = 3.0 * tau**2 - 2.0 * tau**3
        d_progress = 6.0 * tau - 6.0 * tau**2
        dd_progress = 6.0 - 12.0 * tau
        ddd_progress = np.full_like(tau, -12.0)
    else:
        progress = 10.0 * tau**3 - 15.0 * tau**4 + 6.0 * tau**5
        d_progress = 30.0 * tau**2 - 60.0 * tau**3 + 30.0 * tau**4
        dd_progress = 60.0 * tau - 180.0 * tau**2 + 120.0 * tau**3
        ddd_progress = 60.0 - 360.0 * tau + 360.0 * tau**2
    position = distance * progress
    velocity = distance * d_progress / duration
    acceleration = distance * dd_progress / duration**2
    jerk = distance * ddd_progress / duration**3
    signature = [position[-1], np.max(velocity), np.max(np.abs(acceleration)), acceleration[0], acceleration[-1], np.max(np.abs(jerk))]
    return {
        "metrics": [
            {"id": "final_position", "label": "Final position", "value": position[-1], "unit": "m", "emphasis": "primary"},
            {"id": "peak_velocity", "label": "Peak velocity", "value": np.max(velocity), "unit": "m/s"},
            {"id": "peak_acceleration", "label": "Peak acceleration", "value": np.max(np.abs(acceleration)), "unit": "m/s^2"},
            {"id": "start_acceleration", "label": "Start acceleration", "value": acceleration[0], "unit": "m/s^2"},
        ],
        "plots": {
            "response": {
                "data": [_trace("Position", t, position), _trace("Velocity", t, velocity)],
                "layout": _layout("Rest-to-rest trajectory", "Time (s)", "Position (m) / velocity (m/s)"),
                "config": {"responsive": True, "displaylogo": False},
            },
            "mechanism": {
                "data": [_trace("Acceleration", t, acceleration), _trace("Jerk", t, jerk)],
                "layout": _layout("Derivative demand", "Time (s)", "Acceleration (m/s^2) / jerk (m/s^3)"),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "Normalized quintic time scaling satisfies position, velocity, and acceleration endpoint constraints.",
            "broken": "The cubic profile leaves nonzero acceleration at both endpoints, creating acceleration jumps.",
            "recovery": "Use the quintic polynomial and verify all six endpoint constraints analytically.",
        },
        "diagnostics": {"item_id": "P07", "reference_basis": "symbolic polynomial derivatives", "broken_active": broken, "sample_count": len(t), "signature": [float(v) for v in signature]},
    }

