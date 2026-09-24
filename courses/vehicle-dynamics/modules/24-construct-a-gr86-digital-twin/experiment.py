from __future__ import annotations

import math
from typing import Any

PRIMARY = "vehicle_mass_kg"
SECONDARY = "tire_friction_coefficient"
PRIMARY_RANGE = (1150.0, 1500.0)
SECONDARY_RANGE = (0.70, 1.30)
FIELDS = [
    "speed_rmse_m_s",
    "position_rmse_m",
    "yaw_rate_rmse_rad_s",
    "final_speed_m_s",
    "path_distance_m",
    "lap_time_proxy_s",
    "requirements_passed",
    "maximum_yaw_residual_rad_s",
    "invalid",
]


def _trajectory(mass: float, friction: float, broken: bool) -> tuple[list[float], list[float], list[float], list[float], list[float]]:
    dt = 0.2
    wheelbase = 2.57
    steering_ratio = 13.0
    speed = 10.0
    heading = 0.0
    x_position = 0.0
    y_position = 0.0
    times = [0.0]
    speeds = [speed]
    xs = [x_position]
    ys = [y_position]
    yaws = [0.0]
    for index in range(1, 61):
        time = index * dt
        drive_force = 4000.0 + 600.0 * math.sin(0.22 * time)
        drag_force = 0.5 * 1.225 * 0.65 * speed * speed
        free_acceleration = (drive_force - drag_force) / mass
        acceleration = min(free_acceleration, 0.35 * friction * 9.81)
        speed = max(0.0, speed + acceleration * dt)
        steering_deg = 12.0 * math.sin(0.35 * time)
        wheel_angle = steering_deg / steering_ratio if broken else math.radians(steering_deg) / steering_ratio
        kinematic_yaw = speed * math.tan(wheel_angle) / wheelbase
        yaw_limit = friction * 9.81 / max(speed, 1.0)
        yaw_rate = max(-yaw_limit, min(yaw_limit, kinematic_yaw))
        heading_midpoint = heading + 0.5 * yaw_rate * dt
        x_position += speed * math.cos(heading_midpoint) * dt
        y_position += speed * math.sin(heading_midpoint) * dt
        heading += yaw_rate * dt
        times.append(time)
        speeds.append(speed)
        xs.append(x_position)
        ys.append(y_position)
        yaws.append(yaw_rate)
    return times, speeds, xs, ys, yaws


def _evaluate(mass: float, friction: float, broken: bool) -> tuple[list[float], list[float], list[float]]:
    times, speeds, xs, ys, yaws = _trajectory(mass, friction, broken)
    _, nominal_speeds, nominal_xs, nominal_ys, nominal_yaws = _trajectory(1320.0, 1.0, False)
    observed_speeds = [value + 0.05 * math.sin(0.4 * time) for value, time in zip(nominal_speeds, times, strict=True)]
    observed_xs = [value + 0.10 * math.sin(0.3 * time) for value, time in zip(nominal_xs, times, strict=True)]
    observed_ys = [value + 0.10 * math.cos(0.3 * time) for value, time in zip(nominal_ys, times, strict=True)]
    observed_yaws = [value + 0.001 * math.sin(0.6 * time) for value, time in zip(nominal_yaws, times, strict=True)]
    speed_errors = [model - observed for model, observed in zip(speeds, observed_speeds, strict=True)]
    position_errors = [math.hypot(x_value - observed_x, y_value - observed_y) for x_value, y_value, observed_x, observed_y in zip(xs, ys, observed_xs, observed_ys, strict=True)]
    yaw_errors = [model - observed for model, observed in zip(yaws, observed_yaws, strict=True)]
    speed_rmse = math.sqrt(sum(value * value for value in speed_errors) / len(speed_errors))
    position_rmse = math.sqrt(sum(value * value for value in position_errors) / len(position_errors))
    yaw_rmse = math.sqrt(sum(value * value for value in yaw_errors) / len(yaw_errors))
    distance = sum(0.2 * value for value in speeds[1:])
    mean_speed = distance / (times[-1] - times[0])
    lap_proxy = 2400.0 / mean_speed
    requirements_passed = float(sum((speed_rmse < 1.0, position_rmse < 3.0, yaw_rmse < 0.05)))
    signature = [speed_rmse, position_rmse, yaw_rmse, speeds[-1], distance, lap_proxy, requirements_passed, max(abs(value) for value in yaw_errors), float(broken)]
    return signature, times, speeds


def _plot(name: str, x: list[float], y: list[float], x_title: str, y_title: str) -> dict[str, Any]:
    return {
        "data": [{"type": "scatter", "mode": "lines+markers", "name": name, "x": x, "y": y}],
        "layout": {"title": {"text": "Construct a GR86 Digital Twin"}, "xaxis": {"title": x_title}, "yaxis": {"title": y_title}, "uirevision": "keep-view"},
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
    signature, times, speeds = _evaluate(primary, secondary, broken)
    if len(signature) != len(FIELDS) or not all(math.isfinite(value) for value in signature):
        raise ValueError("digital-twin model produced an invalid signature")
    primary_values = [1150.0, 1320.0, 1500.0]
    secondary_values = [0.70, 1.0, 1.30]
    failed = _evaluate(primary, secondary, True)[0]
    recovered = _evaluate(1320.0, 1.0, False)[0]
    return {
        "metrics": [
            {"id": "speed_error", "label": "Speed RMSE", "value": signature[0], "unit": "m/s", "emphasis": "primary"},
            {"id": "position_error", "label": "Position RMSE", "value": signature[1], "unit": "m"},
            {"id": "valid", "label": "Interface valid", "value": not bool(signature[-1]), "unit": "boolean"},
        ],
        "plots": {
            "response": _plot("twin speed", times, speeds, "time (s)", "speed (m/s)"),
            "primary_sweep": _plot(PRIMARY, primary_values, [_evaluate(value, secondary, False)[0][5] for value in primary_values], "vehicle mass (kg)", "lap-time proxy (s)"),
            "secondary_sweep": _plot(SECONDARY, secondary_values, [_evaluate(primary, value, False)[0][0] for value in secondary_values], "tire friction coefficient", "speed RMSE (m/s)"),
            "broken_recovery": {
                "data": [
                    {"type": "bar", "name": "steering unit defect", "x": FIELDS[:-1], "y": failed[:-1]},
                    {"type": "bar", "name": "recovered baseline", "x": FIELDS[:-1], "y": recovered[:-1]},
                ],
                "layout": {"barmode": "group", "xaxis": {"title": "integration requirement"}, "yaxis": {"title": "reported value"}},
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "The baseline twin links mass, traction-limited acceleration, steering, yaw limiting, path integration, and residual requirements.",
            "broken": "Broken mode treats steering degrees as radians at the model interface, driving yaw and position residuals outside requirements.",
            "recovery": "Convert steering to radians exactly once, retain the steering ratio and friction yaw bound, and rerun all three residual checks.",
        },
        "diagnostics": {"item_id": "P24", "signature": signature, "fields": FIELDS, "broken_active": broken, "bounded_points": len(times), "data_provenance": "deterministic synthetic telemetry; not physical GR86 validation"},
    }
