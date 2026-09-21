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
    stiffness = float(parameters["stiffness_n_m"])
    damping = float(parameters["damping_ns_m"])
    desired = float(parameters["desired_penetration_mm"]) / 1000.0
    broken = bool(parameters["broken_mode"])
    mass = 1.0
    environment_stiffness = 500.0
    active_environment = 0.0 if broken else environment_stiffness
    dt = 0.001
    t = np.arange(0.0, 1.5 + 0.5 * dt, dt)
    penetration = np.zeros_like(t)
    velocity = np.zeros_like(t)
    contact_force = np.zeros_like(t)
    for index in range(len(t) - 1):
        force = active_environment * max(penetration[index], 0.0)
        acceleration = (stiffness * (desired - penetration[index]) - damping * velocity[index] - force) / mass
        velocity[index + 1] = velocity[index] + dt * acceleration
        penetration[index + 1] = penetration[index] + dt * velocity[index + 1]
        contact_force[index] = force
    contact_force[-1] = active_environment * max(penetration[-1], 0.0)
    expected_static = stiffness * desired / (stiffness + active_environment)
    controller_force = stiffness * (desired - penetration)
    energy = 0.5 * mass * velocity**2 + 0.5 * stiffness * (penetration - desired) ** 2 + 0.5 * active_environment * np.maximum(penetration, 0.0) ** 2
    signature = [1000.0 * penetration[-1], np.max(contact_force), expected_static * 1000.0, abs(penetration[-1] - expected_static) * 1000.0, energy[-1]]
    return {
        "metrics": [
            {"id": "final_penetration", "label": "Final penetration", "value": 1000.0 * penetration[-1], "unit": "mm", "emphasis": "primary"},
            {"id": "peak_contact_force", "label": "Peak contact force", "value": np.max(contact_force), "unit": "N"},
            {"id": "static_prediction", "label": "Static prediction", "value": 1000.0 * expected_static, "unit": "mm"},
            {"id": "static_error", "label": "Static error", "value": 1000.0 * abs(penetration[-1] - expected_static), "unit": "mm"},
        ],
        "plots": {
            "response": {
                "data": [_trace("Penetration", t, 1000.0 * penetration), _trace("Static prediction", t, np.full_like(t, 1000.0 * expected_static), "dash")],
                "layout": _layout("Contact penetration", "Time (s)", "Penetration (mm)"),
                "config": {"responsive": True, "displaylogo": False},
            },
            "mechanism": {
                "data": [_trace("Contact force", t, contact_force), _trace("Controller spring force", t, controller_force)],
                "layout": _layout("Force balance", "Time (s)", "Force (N)"),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "Controller stiffness and wall stiffness share the requested penetration; damping shapes only the transient.",
            "broken": "Broken mode disconnects the wall reaction, so penetration reaches the command while contact force remains zero.",
            "recovery": "Reconnect the unilateral wall force with the opposing sign and verify static force balance.",
        },
        "diagnostics": {"item_id": "P08", "reference_basis": "static balance and independent recurrence", "broken_active": broken, "sample_count": len(t), "signature": [float(v) for v in signature]},
    }

