from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 49
DEFAULTS = {"target_slip": 0.15, "brake_torque_nm": 2200.0}
RANGES = {"target_slip": (0.08, 0.25), "brake_torque_nm": (1000.0, 3500.0)}
BROKEN_TEXT = "Broken mode applies the requested brake torque without slip feedback, so the wheel locks and the tire leaves its peak-slip operating region."
RECOVERY_TEXT = "Close the loop on measured slip, release brake torque above the target band, and verify both wheel-speed dynamics and the no-lock invariant."


def _parameters(supplied: dict[str, Any]) -> dict[str, float]:
    result: dict[str, float] = {}
    for key, default in DEFAULTS.items():
        value = float(supplied.get(key, default))
        minimum, maximum = RANGES[key]
        if not np.isfinite(value) or value < minimum or value > maximum:
            raise ValueError(f"{key} outside declared finite range [{minimum}, {maximum}]")
        result[key] = value
    return result


def _trace(
    name: str,
    x: Any,
    y: Any,
    x_quantity: str,
    x_unit: str,
    y_quantity: str,
    y_unit: str,
) -> dict[str, Any]:
    return {
        "type": "scattergl",
        "mode": "lines",
        "name": name,
        "x": np.asarray(x, dtype=float),
        "y": np.asarray(y, dtype=float),
        "meta": {
            "x_quantity": x_quantity,
            "x_unit": x_unit,
            "y_quantity": y_quantity,
            "y_unit": y_unit,
        },
    }


def _plot(title: str, x_title: str, y_title: str, traces: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "data": traces,
        "layout": {
            "title": {"text": title, "x": 0.02},
            "xaxis": {"title": {"text": x_title}},
            "yaxis": {"title": {"text": y_title}},
            "legend": {"orientation": "h"},
            "margin": {"l": 72, "r": 36, "t": 62, "b": 62},
            "hovermode": "closest",
            "uirevision": "keep-view",
        },
        "config": {"responsive": True, "displaylogo": False},
    }


def _result(model: dict[str, Any], broken: bool) -> dict[str, Any]:
    return {
        "metrics": [
            {
                "id": key,
                "label": label,
                "value": float(value),
                "unit": unit,
                "emphasis": "primary" if index == 0 else "normal",
            }
            for index, (key, label, value, unit) in enumerate(model["metrics"])
        ],
        "plots": model["plots"],
        "explanations": {
            "observation": model["observation"],
            "broken": BROKEN_TEXT,
            "recovery": RECOVERY_TEXT,
        },
        "diagnostics": {
            "item_number": ITEM_NUMBER,
            "broken_active": bool(broken),
            "signature": [float(value) for value in model["signature"]],
        },
    }


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    target, requested_torque = p["target_slip"], p["brake_torque_nm"]
    mass, inertia, radius, gravity = 360.0, 1.20, 0.31, 9.81
    peak_force = 1.05 * mass * gravity
    step, samples = 0.002, 2001
    time = np.arange(samples, dtype=float) * step
    speed = np.empty(samples)
    wheel_speed = np.empty(samples)
    slip = np.empty(samples)
    brake = np.empty(samples)
    tire_force = np.empty(samples)
    speed[0], wheel_speed[0] = 30.0, 30.0 / radius
    slip[0], brake[0], tire_force[0] = 0.0, requested_torque, 0.0
    maximum_residual = 0.0
    stopping_distance = 0.0
    for index in range(1, samples):
        previous_slip = max(
            0.0,
            (speed[index - 1] - radius * wheel_speed[index - 1])
            / max(speed[index - 1], 0.5),
        )
        normalized = previous_slip / target
        force = (
            peak_force * normalized * np.exp(1.0 - normalized)
            if previous_slip > 0.0
            else 0.0
        )
        force = max(0.0, float(force))
        if broken:
            applied_torque = requested_torque
        else:
            error = target - previous_slip
            desired_slip_rate = 10.0 * error
            vehicle_acceleration = -force / mass
            applied_torque = np.clip(
                force * radius
                + inertia
                / radius
                * (
                    speed[index - 1] * desired_slip_rate
                    - (1.0 - previous_slip) * vehicle_acceleration
                ),
                0.0,
                requested_torque,
            )
        vehicle_acceleration = -force / mass
        wheel_acceleration = (force * radius - applied_torque) / inertia
        raw_wheel_speed = wheel_speed[index - 1] + step * wheel_acceleration
        wheel_speed[index] = max(0.0, raw_wheel_speed)
        speed[index] = max(0.1, speed[index - 1] + step * vehicle_acceleration)
        stopping_distance += 0.5 * step * (speed[index - 1] + speed[index])
        slip[index] = np.clip(
            (speed[index] - radius * wheel_speed[index]) / max(speed[index], 0.5),
            0.0,
            1.0,
        )
        brake[index], tire_force[index] = applied_torque, force
        actual_wheel_acceleration = (
            wheel_speed[index] - wheel_speed[index - 1]
        ) / step
        if speed[index] > 2.0:
            maximum_residual = max(
                maximum_residual,
                abs(
                    inertia * actual_wheel_acceleration
                    - (force * radius - applied_torque)
                ),
            )
    active_mask = (time >= 0.5) & (speed > 2.0)
    active = slip[active_mask]
    target_error = float(np.mean(np.abs(active - target)))
    locked = float(np.any((wheel_speed < 0.5) & (speed > 2.0)))
    signature = [
        float(np.max(slip[speed > 2.0])),
        target_error,
        float(speed[0] - speed[-1]),
        stopping_distance,
        locked,
        maximum_residual,
    ]
    return {
        "signature": signature,
        "metrics": [
            ("peak_slip", "Peak slip", signature[0], "1"),
            ("target_error", "Mean target-slip error", target_error, "1"),
            ("speed_reduction", "Speed reduction", signature[2], "m/s"),
            ("wheel_lock", "Wheel-lock flag", locked, "1"),
            ("closure", "Wheel-dynamics closure residual", maximum_residual, "N*m"),
        ],
        "plots": {
            "response": _plot(
                "ABS slip response",
                "Time (s)",
                "Slip ratio (1)",
                [
                    _trace("Wheel slip", time, slip, "Time", "s", "Slip ratio", "1"),
                    _trace(
                        "Target slip",
                        time,
                        np.full(samples, target),
                        "Time",
                        "s",
                        "Slip ratio",
                        "1",
                    ),
                ],
            ),
            "mechanism": _plot(
                "Brake-torque modulation",
                "Time (s)",
                "Torque (N*m)",
                [
                    _trace(
                        "Applied brake torque",
                        time,
                        brake,
                        "Time",
                        "s",
                        "Brake torque",
                        "N*m",
                    ),
                    _trace(
                        "Tire reaction torque",
                        time,
                        tire_force * radius,
                        "Time",
                        "s",
                        "Tire reaction torque",
                        "N*m",
                    ),
                ],
            ),
        },
        "observation": "ABS preserves useful tire force by modulating brake torque around the target slip instead of allowing sustained wheel lock.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
