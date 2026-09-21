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
    voltage = float(parameters["voltage_v"])
    ratio = float(parameters["gear_ratio"])
    load = float(parameters["load_torque_nm"])
    broken = bool(parameters["broken_mode"])
    resistance = 1.0
    inductance = 0.02
    torque_constant = 0.05
    emf_constant = 0.0 if broken else 0.05
    motor_inertia = 0.002
    load_inertia = 0.02
    drag = 0.001
    equivalent_inertia = motor_inertia + load_inertia / ratio**2
    dt = 0.001
    t = np.arange(0.0, 2.0 + 0.5 * dt, dt)
    current = np.zeros_like(t)
    motor_speed = np.zeros_like(t)
    for index in range(len(t) - 1):
        current_dot = (voltage - resistance * current[index] - emf_constant * motor_speed[index]) / inductance
        speed_dot = (torque_constant * current[index] - drag * motor_speed[index] - load / ratio) / equivalent_inertia
        current[index + 1] = current[index] + dt * current_dot
        motor_speed[index + 1] = motor_speed[index] + dt * speed_dot
    output_speed = motor_speed / ratio
    denominator = drag + torque_constant * emf_constant / resistance
    steady_motor = (torque_constant * voltage / resistance - load / ratio) / denominator
    steady_output = steady_motor / ratio
    balance = torque_constant * current - drag * motor_speed - load / ratio
    signature = [current[-1], output_speed[-1], steady_output, abs(output_speed[-1] - steady_output), np.max(current)]
    return {
        "metrics": [
            {"id": "final_output_speed", "label": "Final output speed", "value": output_speed[-1], "unit": "rad/s", "emphasis": "primary"},
            {"id": "final_current", "label": "Final current", "value": current[-1], "unit": "A"},
            {"id": "steady_output_speed", "label": "Analytic steady speed", "value": steady_output, "unit": "rad/s"},
            {"id": "reflected_inertia", "label": "Reflected inertia", "value": equivalent_inertia, "unit": "kg m^2"},
        ],
        "plots": {
            "response": {
                "data": [_trace("Output speed", t, output_speed), _trace("Analytic steady speed", t, np.full_like(t, steady_output), "dash")],
                "layout": _layout("Geared output speed", "Time (s)", "Angular speed (rad/s)"),
                "config": {"responsive": True, "displaylogo": False},
            },
            "mechanism": {
                "data": [_trace("Armature current", t, current), _trace("Motor torque balance", t, balance)],
                "layout": _layout("Electrical and torque mechanism", "Time (s)", "Current (A) / torque (N m)"),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "Back EMF reduces current as motor speed rises; the reduction divides motor speed and reflects load to the shaft.",
            "broken": "Broken mode removes back EMF, so current and speed settle to an unphysical high state.",
            "recovery": "Restore the speed-proportional generated voltage and check both electrical and torque balances.",
        },
        "diagnostics": {"item_id": "P05", "reference_basis": "linear state solution and equilibrium", "broken_active": broken, "sample_count": len(t), "signature": [float(v) for v in signature]},
    }

