from __future__ import annotations

from typing import Any

import numpy as np


def _layout(title: str, x: str, y: str) -> dict[str, Any]:
    return {"title": {"text": title, "x": 0.02}, "xaxis": {"title": x}, "yaxis": {"title": y}, "legend": {"orientation": "h"}, "margin": {"l": 65, "r": 20, "t": 55, "b": 55}, "hovermode": "closest", "uirevision": "keep-view"}


def _trace(name: str, x: Any, y: Any, dash: str | None = None) -> dict[str, Any]:
    trace: dict[str, Any] = {"type": "scatter", "mode": "lines", "name": name, "x": x, "y": y}
    if dash:
        trace["line"] = {"dash": dash}
    return trace


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    kp = float(parameters["kp_v_per_rad_s"])
    ki = float(parameters["ki_v_per_rad"])
    command = float(parameters["command_rad_s"])
    limit = float(parameters["voltage_limit_v"])
    broken = bool(parameters["broken_mode"])
    dt = 0.01
    plant_tau = 0.25
    plant_gain = 1.0
    t = np.arange(0.0, 4.0 + 0.5 * dt, dt)
    speed = np.zeros_like(t)
    voltage = np.zeros_like(t)
    integral = np.zeros_like(t)
    for index in range(len(t) - 1):
        error = command - speed[index]
        increment = error if broken else dt * error
        candidate_integral = integral[index] + increment
        raw = kp * error + ki * candidate_integral
        saturated = float(np.clip(raw, -limit, limit))
        pushes_outward = (raw > limit and error > 0.0) or (raw < -limit and error < 0.0)
        if not broken and pushes_outward:
            candidate_integral = integral[index]
            raw = kp * error + ki * candidate_integral
            saturated = float(np.clip(raw, -limit, limit))
        integral[index + 1] = candidate_integral
        voltage[index] = saturated
        speed[index + 1] = speed[index] + dt * (plant_gain * saturated - speed[index]) / plant_tau
    voltage[-1] = float(np.clip(kp * (command - speed[-1]) + ki * integral[-1], -limit, limit))
    error = command - speed
    tail = max(1, len(t) // 5)
    tail_mae = float(np.mean(np.abs(error[-tail:])))
    overshoot = float(max(0.0, np.max(speed) - command))
    saturation_fraction = float(np.mean(np.abs(voltage) >= limit - 1e-12))
    signature = [speed[-1], tail_mae, np.max(np.abs(voltage)), integral[-1], overshoot, saturation_fraction]
    return {
        "metrics": [
            {"id": "final_speed", "label": "Final speed", "value": speed[-1], "unit": "rad/s", "emphasis": "primary"},
            {"id": "tail_error", "label": "Tail mean error", "value": tail_mae, "unit": "rad/s"},
            {"id": "overshoot", "label": "Overshoot", "value": overshoot, "unit": "rad/s"},
            {"id": "saturation_fraction", "label": "Time saturated", "value": 100.0 * saturation_fraction, "unit": "%"},
        ],
        "plots": {
            "response": {
                "data": [_trace("Wheel speed", t, speed), _trace("Command", t, np.full_like(t, command), "dash")],
                "layout": _layout("Closed-loop wheel speed", "Time (s)", "Angular speed (rad/s)"),
                "config": {"responsive": True, "displaylogo": False},
            },
            "mechanism": {
                "data": [_trace("Voltage command", t, voltage), _trace("Integral state", t, integral)],
                "layout": _layout("Controller effort and memory", "Time (s)", "Voltage (V) / integral error (rad)"),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "PI action closes the speed loop while voltage saturation and conditional integration bound actuator effort.",
            "broken": "Broken mode omits sample time from integral accumulation, multiplying effective integral action by 100.",
            "recovery": "Scale each error sample by 10 ms and freeze integration when it would deepen saturation.",
        },
        "diagnostics": {"item_id": "P06", "reference_basis": "independent discrete recurrence", "broken_active": broken, "sample_count": len(t), "signature": [float(v) for v in signature]},
    }

