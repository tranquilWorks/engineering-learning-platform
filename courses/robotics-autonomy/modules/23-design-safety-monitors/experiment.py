from __future__ import annotations

from typing import Any

import numpy as np


def _layout(title: str, x: str, y: str) -> dict[str, Any]:
    return {
        "title": {"text": title, "x": 0.02},
        "xaxis": {"title": x},
        "yaxis": {"title": y},
        "legend": {"orientation": "h"},
        "margin": {"l": 65, "r": 20, "t": 55, "b": 55},
        "hovermode": "closest",
        "uirevision": "keep-view",
    }


def _trace(name: str, x: Any, y: Any) -> dict[str, Any]:
    return {"type": "scatter", "mode": "lines", "name": name, "x": x, "y": y}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    command_speed = float(parameters["command_speed_m_s"])
    obstacle_distance = float(parameters["obstacle_distance_m"])
    reaction_time = float(parameters["reaction_time_s"])
    deceleration = float(parameters["deceleration_m_s2"])
    broken = bool(parameters["broken_mode"])
    dt = 0.01
    times = np.arange(0.0, 4.0 + 0.5 * dt, dt)
    position = np.zeros(len(times))
    speed = np.zeros(len(times))
    speed[0] = command_speed
    braking = False
    interventions = 0
    threshold_history = np.zeros(len(times))
    for index in range(len(times) - 1):
        distance = obstacle_distance - position[index]
        threshold = (
            0.1
            if broken
            else speed[index] ** 2 / (2.0 * deceleration)
            + reaction_time * speed[index]
            + 0.1
        )
        threshold_history[index] = threshold
        if not braking and distance <= threshold:
            braking = True
            interventions += 1
        speed[index + 1] = (
            max(0.0, speed[index] - deceleration * dt) if braking else command_speed
        )
        position[index + 1] = (
            position[index] + 0.5 * (speed[index] + speed[index + 1]) * dt
        )
    threshold_history[-1] = (
        0.1
        if broken
        else speed[-1] ** 2 / (2.0 * deceleration) + reaction_time * speed[-1] + 0.1
    )
    separation = obstacle_distance - position
    stopped = np.flatnonzero(speed <= 1e-12)
    stop_time = times[stopped[0]] if len(stopped) else times[-1]
    collision = bool(np.any(separation <= 0.0))
    signature = [
        np.min(separation),
        stop_time,
        float(collision),
        float(interventions),
        np.max(speed),
        speed[-1],
    ]
    return {
        "metrics": [
            {
                "id": "minimum_separation",
                "label": "Minimum obstacle separation",
                "value": np.min(separation),
                "unit": "m",
                "emphasis": "primary",
            },
            {
                "id": "stop_time",
                "label": "Full-stop time",
                "value": stop_time,
                "unit": "s",
            },
            {
                "id": "collision",
                "label": "Obstacle crossed",
                "value": "yes" if collision else "no",
                "unit": None,
            },
            {
                "id": "interventions",
                "label": "Monitor interventions",
                "value": interventions,
                "unit": "events",
            },
        ],
        "plots": {
            "response": {
                "data": [
                    _trace("Speed", times, speed),
                    _trace("Separation", times, separation),
                ],
                "layout": _layout(
                    "Monitored obstacle approach",
                    "Time (s)",
                    "Speed (m/s) / separation (m)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "mechanism": {
                "data": [
                    _trace("Available separation", times, separation),
                    _trace("Required stopping envelope", times, threshold_history),
                ],
                "layout": _layout(
                    "Safety-envelope comparison", "Time (s)", "Distance (m)"
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "The monitor compares remaining separation with reaction travel, braking distance, and margin, then latches a monotonic braking response before the envelope is violated.",
            "broken": "Broken mode waits for a fixed 0.1 m threshold regardless of speed. At 2 m/s the robot requires much more distance and passes the obstacle before stopping.",
            "recovery": "Restore the speed-dependent stopping envelope and use conservative validated deceleration/reaction bounds; keep the stop latched until an explicit safe reset.",
        },
        "diagnostics": {
            "item_id": "P23",
            "reference_basis": "independent discrete stopping-envelope recurrence and kinematic limit",
            "broken_active": broken,
            "sample_count": len(times),
            "signature": [float(value) for value in signature],
        },
    }
