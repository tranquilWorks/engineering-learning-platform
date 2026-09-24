from __future__ import annotations

import math
from typing import Any

PRIMARY = "front_roll_stiffness_n_m_rad"
SECONDARY = "rear_roll_stiffness_n_m_rad"
PRIMARY_RANGE = (10000.0, 60000.0)
SECONDARY_RANGE = (10000.0, 60000.0)
FIELDS = [
    "roll_angle_rad",
    "front_transfer_n",
    "rear_transfer_n",
    "front_share",
    "moment_residual_n_m",
    "balance_indicator",
    "invalid",
]


def _model(a: float, b: float, broken: bool) -> list[float]:
    front = a
    rear = -b if broken else b
    mass = 1320.0
    ay = 7.0
    height = 0.50
    track = 1.53
    total = front + rear
    roll_moment = mass * ay * height
    angle = roll_moment / total if abs(total) > 1e-12 else 0.0
    front_transfer = front * angle / track
    rear_transfer = rear * angle / track
    front_moment = front_transfer * track
    rear_moment = rear_transfer * track
    residual = front_moment + rear_moment - roll_moment
    share = front_moment / roll_moment
    balance = share - 0.53
    return [
        angle,
        front_transfer,
        rear_transfer,
        share,
        residual,
        balance,
        float(front <= 0.0 or rear <= 0.0 or total <= 0.0),
    ]


def _plot(name: str, x: list[float], y: list[float], x_unit: str) -> dict[str, Any]:
    return {
        "data": [
            {"type": "scatter", "mode": "lines+markers", "name": name, "x": x, "y": y}
        ],
        "layout": {
            "title": {"text": "Distribute Roll Stiffness"},
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
    primary_values = [PRIMARY_RANGE[0], 32000.0, PRIMARY_RANGE[1]]
    secondary_values = [SECONDARY_RANGE[0], 26000.0, SECONDARY_RANGE[1]]
    primary_response = [_model(value, secondary, False)[1] for value in primary_values]
    secondary_response = [
        _model(primary, value, False)[1] for value in secondary_values
    ]
    failed = _model(primary, secondary, True)
    recovered = _model(32000.0, 26000.0, False)
    return {
        "metrics": [
            {
                "id": "primary",
                "label": "Front roll stiffness",
                "value": primary,
                "unit": "N*m/rad",
                "emphasis": "primary",
            },
            {
                "id": "secondary",
                "label": "Rear roll stiffness",
                "value": secondary,
                "unit": "N*m/rad",
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
            "primary_sweep": _plot(
                PRIMARY, primary_values, primary_response, "N*m/rad"
            ),
            "secondary_sweep": _plot(
                SECONDARY, secondary_values, secondary_response, "N*m/rad"
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
            "observation": "Front and rear transfer sum to M_roll/t, so their elastic roll moments sum to the applied roll moment.",
            "broken": "Broken mode gives the rear axle negative roll stiffness and flags the nonphysical allocation.",
            "recovery": "Restore positive axle stiffnesses and verify moment conservation.",
        },
        "diagnostics": {
            "item_id": "P11",
            "signature": signature,
            "fields": FIELDS,
            "broken_active": broken,
            "bounded_points": 3,
        },
    }
