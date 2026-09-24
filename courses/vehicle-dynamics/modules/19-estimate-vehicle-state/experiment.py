from __future__ import annotations

import math
from typing import Any

PRIMARY = "speed_m_s"
SECONDARY = "yaw_rate_deg_s"
PRIMARY_RANGE = (5.0, 45.0)
SECONDARY_RANGE = (-30.0, 30.0)
FIELDS = [
    "final_x_m",
    "final_y_m",
    "final_heading_deg",
    "curvature_1_m",
    "turn_radius_m",
    "lateral_acceleration_m_s2",
    "path_distance_m",
    "invalid",
]


def _integrate(speed: float, yaw_deg_s: float, broken: bool) -> tuple[list[float], list[float], list[float], list[float]]:
    dt = 0.1
    yaw_rad_s = yaw_deg_s if broken else math.radians(yaw_deg_s)
    x_position = 0.0
    y_position = 0.0
    heading = 0.0
    xs = [x_position]
    ys = [y_position]
    times = [0.0]
    for index in range(100):
        heading_midpoint = heading + 0.5 * yaw_rad_s * dt
        x_position += speed * math.cos(heading_midpoint) * dt
        y_position += speed * math.sin(heading_midpoint) * dt
        heading += yaw_rad_s * dt
        xs.append(x_position)
        ys.append(y_position)
        times.append((index + 1) * dt)
    curvature = yaw_rad_s / speed
    radius = 0.0 if abs(curvature) < 1e-12 else 1.0 / abs(curvature)
    signature = [
        x_position,
        y_position,
        math.degrees(heading),
        curvature,
        radius,
        speed * yaw_rad_s,
        speed * 10.0,
        float(broken),
    ]
    return signature, times, xs, ys


def _plot(name: str, x: list[float], y: list[float], x_title: str, y_title: str) -> dict[str, Any]:
    return {
        "data": [{"type": "scatter", "mode": "lines+markers", "name": name, "x": x, "y": y}],
        "layout": {"title": {"text": "Estimate Vehicle State"}, "xaxis": {"title": x_title}, "yaxis": {"title": y_title}, "uirevision": "keep-view", "yaxis_scaleanchor": "x"},
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
    signature, _, xs, ys = _integrate(primary, secondary, broken)
    if len(signature) != len(FIELDS) or not all(math.isfinite(value) for value in signature):
        raise ValueError("state estimator produced an invalid signature")
    primary_values = [5.0, 20.0, 45.0]
    secondary_values = [-30.0, 8.0, 30.0]
    failed = _integrate(primary, secondary, True)[0]
    recovered = _integrate(20.0, 8.0, False)[0]
    return {
        "metrics": [
            {"id": "heading", "label": "Final heading", "value": signature[2], "unit": "deg", "emphasis": "primary"},
            {"id": "radius", "label": "Turn radius", "value": signature[4], "unit": "m"},
            {"id": "valid", "label": "Angle interface valid", "value": not bool(signature[-1]), "unit": "boolean"},
        ],
        "plots": {
            "response": _plot("estimated path", xs, ys, "global x (m)", "global y (m)"),
            "primary_sweep": _plot(PRIMARY, primary_values, [_integrate(value, secondary, False)[0][5] for value in primary_values], "speed (m/s)", "lateral acceleration (m/s²)"),
            "secondary_sweep": _plot(SECONDARY, secondary_values, [_integrate(primary, value, False)[0][3] for value in secondary_values], "yaw rate (deg/s)", "curvature (1/m)"),
            "broken_recovery": {
                "data": [
                    {"type": "bar", "name": "degrees used as radians", "x": FIELDS[:-1], "y": failed[:-1]},
                    {"type": "bar", "name": "recovered baseline", "x": FIELDS[:-1], "y": recovered[:-1]},
                ],
                "layout": {"barmode": "group", "xaxis": {"title": "state quantity"}, "yaxis": {"title": "SI value"}},
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "For constant speed and yaw rate, curvature is yaw rate divided by speed and distance is speed times horizon.",
            "broken": "Broken mode passes degrees per second into a radian integrator, producing an unmistakably invalid path and heading.",
            "recovery": "Convert yaw rate to radians per second exactly once before midpoint integration in the global frame.",
        },
        "diagnostics": {"item_id": "P19", "signature": signature, "fields": FIELDS, "broken_active": broken, "bounded_points": len(xs)},
    }
