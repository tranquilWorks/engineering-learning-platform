from __future__ import annotations

import math
from typing import Any

PRIMARY = "friction_coefficient"
SECONDARY = "acceleration_limit_m_s2"
PRIMARY_RANGE = (0.70, 1.40)
SECONDARY_RANGE = (1.0, 6.0)
FIELDS = [
    "lap_time_s",
    "peak_speed_m_s",
    "corner_entry_speed_m_s",
    "maximum_braking_violation_m2_s2",
    "active_grip_limits",
    "minimum_speed_m_s",
    "segments",
    "invalid",
]

CURVATURES = [0.0, 0.0, 0.012, 0.025, 0.045, 0.045, 0.020, 0.0, 0.0, 0.035, 0.050, 0.015, 0.0]


def _simulate(friction: float, acceleration: float, broken: bool) -> tuple[list[float], list[float], list[float], list[float]]:
    distance_step = 25.0
    brake_limit = 6.0
    limits = [50.0 if curvature == 0.0 else min(50.0, math.sqrt(friction * 9.81 / curvature)) for curvature in CURVATURES]
    speeds = [15.0]
    for index in range(1, len(limits)):
        reachable = math.sqrt(speeds[-1] ** 2 + 2.0 * acceleration * distance_step)
        speeds.append(min(limits[index], reachable))
    if not broken:
        speeds[-1] = min(speeds[-1], 15.0)
        for index in range(len(speeds) - 2, -1, -1):
            brake_reachable = math.sqrt(speeds[index + 1] ** 2 + 2.0 * brake_limit * distance_step)
            speeds[index] = min(speeds[index], brake_reachable)
    violation = max(max(0.0, speeds[index] ** 2 - speeds[index + 1] ** 2 - 2.0 * brake_limit * distance_step) for index in range(len(speeds) - 1))
    segment_times = [2.0 * distance_step / (speeds[index] + speeds[index + 1]) for index in range(len(speeds) - 1)]
    lap_time = sum(segment_times)
    active_limits = sum(abs(speed - limit) < 1e-9 for speed, limit in zip(speeds, limits, strict=True))
    invalid = broken or violation > 1e-9
    signature = [lap_time, max(speeds), speeds[8], violation, float(active_limits), min(speeds), float(len(CURVATURES) - 1), float(invalid)]
    distances = [distance_step * index for index in range(len(speeds))]
    return signature, distances, speeds, limits


def _plot(name: str, x: list[float], y: list[float], x_title: str, y_title: str) -> dict[str, Any]:
    return {
        "data": [{"type": "scatter", "mode": "lines+markers", "name": name, "x": x, "y": y}],
        "layout": {"title": {"text": "Build a Lap-Time Simulator"}, "xaxis": {"title": x_title}, "yaxis": {"title": y_title}, "uirevision": "keep-view"},
        "config": {"responsive": True, "displaylogo": False},
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    primary = float(parameters[PRIMARY])
    secondary = float(parameters[SECONDARY])
    broken = bool(parameters["broken_mode"])
    if not math.isfinite(primary) or not PRIMARY_RANGE[0] <= primary <= PRIMARY_RANGE[1]:
        raise ValueError(f"{PRIMARY} outside declared finite range")
    if not math.isfinite(secondary) or not SECONDARY_RANGE[0] <= secondary <= SECONDARY_RANGE[1]:
        raise ValueError(f"{SECONDARY} outside declared finite range")
    signature, distances, speeds, limits = _simulate(primary, secondary, broken)
    if len(signature) != len(FIELDS) or not all(math.isfinite(value) for value in signature):
        raise ValueError("lap simulation produced an invalid signature")
    primary_values = [0.70, 1.05, 1.40]
    secondary_values = [1.0, 3.5, 6.0]
    failed = _simulate(primary, secondary, True)[0]
    recovered = _simulate(1.05, 3.5, False)[0]
    response = _plot("constrained speed", distances, speeds, "distance (m)", "speed (m/s)")
    response["data"].append({"type": "scatter", "mode": "lines", "name": "curvature speed limit", "x": distances, "y": limits})
    return {
        "metrics": [
            {"id": "lap", "label": "Lap time", "value": signature[0], "unit": "s", "emphasis": "primary"},
            {"id": "entry", "label": "Corner-entry speed", "value": signature[2], "unit": "m/s"},
            {"id": "valid", "label": "Braking constraints valid", "value": not bool(signature[-1]), "unit": "boolean"},
        ],
        "plots": {
            "response": response,
            "primary_sweep": _plot(PRIMARY, primary_values, [_simulate(value, secondary, False)[0][0] for value in primary_values], "friction coefficient", "lap time (s)"),
            "secondary_sweep": _plot(SECONDARY, secondary_values, [_simulate(primary, value, False)[0][0] for value in secondary_values], "acceleration limit (m/s²)", "lap time (s)"),
            "broken_recovery": {
                "data": [
                    {"type": "bar", "name": "forward pass only", "x": FIELDS[:-1], "y": failed[:-1]},
                    {"type": "bar", "name": "forward/backward", "x": FIELDS[:-1], "y": recovered[:-1]},
                ],
                "layout": {"barmode": "group", "xaxis": {"title": "simulation diagnostic"}, "yaxis": {"title": "reported value"}},
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "The forward pass enforces acceleration and local grip; the backward pass propagates future braking needs upstream.",
            "broken": "Broken mode omits the backward pass, so a later slow corner creates a positive corner-entry braking violation.",
            "recovery": "Restore the six m/s² backward braking pass before integrating time over the 12 bounded segments.",
        },
        "diagnostics": {"item_id": "P22", "signature": signature, "fields": FIELDS, "broken_active": broken, "bounded_points": len(speeds)},
    }
