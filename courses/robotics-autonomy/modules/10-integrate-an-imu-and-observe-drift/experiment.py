from __future__ import annotations

from typing import Any

import numpy as np


def _layout(title: str, x: str, y: str) -> dict[str, Any]:
    return {"title": {"text": title, "x": 0.02}, "xaxis": {"title": x}, "yaxis": {"title": y}, "legend": {"orientation": "h"}, "margin": {"l": 65, "r": 20, "t": 55, "b": 55}, "hovermode": "closest", "uirevision": "keep-view"}


def _trace(name: str, x: Any, y: Any) -> dict[str, Any]:
    return {"type": "scatter", "mode": "lines", "name": name, "x": x, "y": y}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    gyro_bias_deg = float(parameters["gyro_bias_deg_s"])
    accel_bias = float(parameters["accel_bias_m_s2"])
    duration = float(parameters["duration_s"])
    sample_rate = float(parameters["sample_rate_hz"])
    broken = bool(parameters["broken_mode"])
    samples = min(round(duration * sample_rate) + 1, 3001)
    t = np.linspace(0.0, duration, samples)
    dt = t[1] - t[0]
    gyro_bias = gyro_bias_deg if broken else np.radians(gyro_bias_deg)
    angle = np.zeros_like(t)
    velocity = np.zeros_like(t)
    position = np.zeros_like(t)
    for index in range(len(t) - 1):
        angle[index + 1] = angle[index] + gyro_bias * dt
        velocity[index + 1] = velocity[index] + accel_bias * dt
        position[index + 1] = position[index] + 0.5 * (velocity[index] + velocity[index + 1]) * dt
    intended_angle = np.radians(gyro_bias_deg) * duration
    intended_position = 0.5 * accel_bias * duration**2
    signature = [np.degrees(angle[-1]), velocity[-1], position[-1], abs(angle[-1] - intended_angle), abs(position[-1] - intended_position)]
    return {
        "metrics": [
            {"id": "final_angle_drift", "label": "Final angle drift", "value": np.degrees(angle[-1]), "unit": "deg", "emphasis": "primary"},
            {"id": "final_velocity_drift", "label": "Final velocity drift", "value": velocity[-1], "unit": "m/s"},
            {"id": "final_position_drift", "label": "Final position drift", "value": position[-1], "unit": "m"},
            {"id": "angle_reference_error", "label": "Angle reference error", "value": abs(angle[-1] - intended_angle), "unit": "rad"},
        ],
        "plots": {
            "response": {
                "data": [_trace("Angle drift", t, np.degrees(angle)), _trace("Velocity drift", t, velocity)],
                "layout": _layout("Integrated sensor bias", "Time (s)", "Angle (deg) / velocity (m/s)"),
                "config": {"responsive": True, "displaylogo": False},
            },
            "mechanism": {
                "data": [_trace("Position drift", t, position), _trace("Closed-form position", t, 0.5 * accel_bias * t**2)],
                "layout": _layout("Double-integrated acceleration bias", "Time (s)", "Position error (m)"),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "Constant gyro and acceleration biases create linear angle/velocity drift and quadratic position drift.",
            "broken": "Broken mode treats degrees per second as radians per second, exaggerating orientation error by 180/pi.",
            "recovery": "Convert angular-rate units before integration and compare with the closed-form bias-growth laws.",
        },
        "diagnostics": {"item_id": "P10", "reference_basis": "closed-form bias integration", "broken_active": broken, "sample_count": len(t), "signature": [float(v) for v in signature]},
    }
