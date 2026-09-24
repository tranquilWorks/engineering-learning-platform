from __future__ import annotations

import math
from typing import Any

PRIMARY = "initial_speed_m_s"
SECONDARY = "requested_brake_force_n"
PRIMARY_RANGE = (5.0, 55.0)
SECONDARY_RANGE = (1000.0, 18000.0)
FIELDS = [
    "applied_brake_force_n",
    "deceleration_m_s2",
    "stopping_distance_m",
    "stop_time_s",
    "kinetic_energy_j",
    "rotor_delta_t_c",
    "front_load_n",
    "rear_load_n",
    "invalid",
]


def _model(a: float, b: float, broken: bool) -> list[float]:
    speed = a
    request = b
    mass = 1320.0
    mu = 1.05
    gravity = 9.81
    height = 0.50
    wheelbase = 2.57
    front_static = 0.53 * mass * gravity
    limit = mu * mass * gravity
    applied = request if broken else min(request, limit)
    decel = applied / mass
    distance = speed**2 / (2.0 * decel)
    stop_time = speed / decel
    energy = 0.5 * mass * speed**2
    heat_fraction = 1.0 if broken else 0.85
    delta_t = heat_fraction * energy / (28.0 * 460.0)
    transfer = mass * decel * height / wheelbase
    front = front_static + transfer
    rear = mass * gravity - front
    return [
        applied,
        decel,
        distance,
        stop_time,
        energy,
        delta_t,
        front,
        rear,
        float(broken or rear < 0.0),
    ]


def _plot(name: str, x: list[float], y: list[float], x_unit: str) -> dict[str, Any]:
    return {
        "data": [
            {"type": "scatter", "mode": "lines+markers", "name": name, "x": x, "y": y}
        ],
        "layout": {
            "title": {"text": "Model Braking Distance and Heat"},
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
    primary_values = [PRIMARY_RANGE[0], 30.0, PRIMARY_RANGE[1]]
    secondary_values = [SECONDARY_RANGE[0], 10000.0, SECONDARY_RANGE[1]]
    primary_response = [_model(value, secondary, False)[1] for value in primary_values]
    secondary_response = [
        _model(primary, value, False)[1] for value in secondary_values
    ]
    failed = _model(primary, secondary, True)
    recovered = _model(30.0, 10000.0, False)
    return {
        "metrics": [
            {
                "id": "primary",
                "label": "Initial speed",
                "value": primary,
                "unit": "m/s",
                "emphasis": "primary",
            },
            {
                "id": "secondary",
                "label": "Requested brake force",
                "value": secondary,
                "unit": "N",
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
            "primary_sweep": _plot(PRIMARY, primary_values, primary_response, "m/s"),
            "secondary_sweep": _plot(
                SECONDARY, secondary_values, secondary_response, "N"
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
            "observation": "Stopping work equals initial kinetic energy in the constant-force model.",
            "broken": "Broken mode bypasses the tire-force cap and assigns all kinetic energy to the modeled rotors.",
            "recovery": "Restore the mu*m*g cap, the declared 85% rotor heat split, and nonnegative axle loads.",
        },
        "diagnostics": {
            "item_id": "P15",
            "signature": signature,
            "fields": FIELDS,
            "broken_active": broken,
            "bounded_points": 3,
        },
    }
