from __future__ import annotations

import math
from typing import Any

PRIMARY = "engine_torque_n_m"
SECONDARY = "gear_ratio"
PRIMARY_RANGE = (80.0, 320.0)
SECONDARY_RANGE = (0.8, 4.2)
FIELDS = [
    "engine_speed_rpm",
    "requested_wheel_force_n",
    "applied_wheel_force_n",
    "traction_limit_n",
    "wheel_power_w",
    "power_residual_w",
    "invalid",
]


def _model(a: float, b: float, broken: bool) -> list[float]:
    torque = a
    gear = b
    final_drive = 4.10
    efficiency = 1.0 if broken else 0.90
    radius = 0.315
    speed = 20.0
    mass = 1320.0
    mu = 1.0
    rpm = speed / radius * gear * final_drive * 60.0 / (2.0 * math.pi)
    requested = torque * gear * final_drive * efficiency / radius
    limit = mu * mass * 9.81
    applied = requested if broken else min(requested, limit)
    wheel_power = applied * speed
    input_power = torque * (rpm * 2.0 * math.pi / 60.0) * efficiency
    residual = wheel_power - input_power
    return [
        rpm,
        requested,
        applied,
        limit,
        wheel_power,
        residual,
        float(broken),
    ]


def _plot(name: str, x: list[float], y: list[float], x_unit: str) -> dict[str, Any]:
    return {
        "data": [
            {"type": "scatter", "mode": "lines+markers", "name": name, "x": x, "y": y}
        ],
        "layout": {
            "title": {"text": "Map Engine Torque through Gearing"},
            "xaxis": {"title": x_unit},
            "yaxis": {"title": "selected response (SI units)"},
            "uirevision": "keep-view",
        },
        "config": {"responsive": True, "displaylogo": False},
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    primary = float(parameters[PRIMARY])
    secondary = float(parameters[SECONDARY])
    broken = bool(parameters["broken_mode"])
    if (
        not math.isfinite(primary)
        or not PRIMARY_RANGE[0] <= primary <= PRIMARY_RANGE[1]
    ):
        raise ValueError(f"{PRIMARY} outside declared finite range")
    if (
        not math.isfinite(secondary)
        or not SECONDARY_RANGE[0] <= secondary <= SECONDARY_RANGE[1]
    ):
        raise ValueError(f"{SECONDARY} outside declared finite range")
    signature = _model(primary, secondary, broken)
    if len(signature) != len(FIELDS) or not all(
        math.isfinite(value) for value in signature
    ):
        raise ValueError("model produced an invalid signature")
    primary_values = [PRIMARY_RANGE[0], 250.0, PRIMARY_RANGE[1]]
    secondary_values = [SECONDARY_RANGE[0], 3.0, SECONDARY_RANGE[1]]
    primary_response = [_model(value, secondary, False)[1] for value in primary_values]
    secondary_response = [
        _model(primary, value, False)[1] for value in secondary_values
    ]
    failed = _model(primary, secondary, True)
    recovered = _model(250.0, 3.0, False)
    return {
        "metrics": [
            {
                "id": "primary",
                "label": "Engine torque",
                "value": primary,
                "unit": "N*m",
                "emphasis": "primary",
            },
            {
                "id": "secondary",
                "label": "Selected gear ratio",
                "value": secondary,
                "unit": "ratio",
            },
            {
                "id": "valid",
                "label": "Physical setup valid",
                "value": not bool(signature[-1]),
                "unit": "boolean",
            },
        ],
        "plots": {
            "response": _plot(
                "model signature",
                list(range(len(signature) - 1)),
                signature[:-1],
                "signature field index",
            ),
            "primary_sweep": _plot(PRIMARY, primary_values, primary_response, "N*m"),
            "secondary_sweep": _plot(
                SECONDARY, secondary_values, secondary_response, "ratio"
            ),
            "broken_recovery": {
                "data": [
                    {
                        "type": "bar",
                        "name": "broken",
                        "x": FIELDS[:-1],
                        "y": failed[:-1],
                    },
                    {
                        "type": "bar",
                        "name": "recovered baseline",
                        "x": FIELDS[:-1],
                        "y": recovered[:-1],
                    },
                ],
                "layout": {
                    "barmode": "group",
                    "xaxis": {"title": "physical quantity"},
                    "yaxis": {"title": "SI value"},
                },
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "Power after efficiency equals wheel force times vehicle speed when rotational acceleration is neglected.",
            "broken": "Broken mode assumes lossless gearing and applies unlimited wheel force beyond the tire-force boundary.",
            "recovery": "Restore 90% drivetrain efficiency and cap transmitted force at mu*m*g.",
        },
        "diagnostics": {
            "item_id": "P13",
            "signature": signature,
            "fields": FIELDS,
            "broken_active": broken,
            "bounded_points": 3,
        },
    }
