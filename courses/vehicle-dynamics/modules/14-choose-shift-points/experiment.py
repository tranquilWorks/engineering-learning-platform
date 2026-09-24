from __future__ import annotations

import math
from typing import Any

PRIMARY = "current_gear_ratio"
SECONDARY = "next_gear_ratio"
PRIMARY_RANGE = (1.4, 3.7)
SECONDARY_RANGE = (0.8, 2.4)
FIELDS = [
    "shift_rpm",
    "shift_speed_m_s",
    "current_force_n",
    "next_force_n",
    "post_shift_rpm",
    "force_gap_n",
    "invalid",
]


def _model(a: float, b: float, broken: bool) -> list[float]:
    current = a
    nxt = current * 1.10 if broken else b
    final_drive = 4.10
    efficiency = 0.90
    radius = 0.315
    redline = 7400.0

    def torque(rpm: float) -> float:
        return max(120.0, 245.0 - 0.000006 * (rpm - 5000.0) ** 2)

    shift = redline
    for index in range(121):
        rpm = 2500.0 + (redline - 2500.0) * index / 120.0
        post = rpm * nxt / current
        if torque(post) * nxt >= torque(rpm) * current:
            shift = rpm
            break
    post = shift * nxt / current
    current_force = torque(shift) * current * final_drive * efficiency / radius
    next_force = torque(post) * nxt * final_drive * efficiency / radius
    speed = shift * 2.0 * math.pi / 60.0 * radius / (current * final_drive)
    return [
        shift,
        speed,
        current_force,
        next_force,
        post,
        next_force - current_force,
        float(nxt >= current),
    ]


def _plot(name: str, x: list[float], y: list[float], x_unit: str) -> dict[str, Any]:
    return {
        "data": [
            {"type": "scatter", "mode": "lines+markers", "name": name, "x": x, "y": y}
        ],
        "layout": {
            "title": {"text": "Choose Shift Points"},
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
    primary_values = [PRIMARY_RANGE[0], 2.188, PRIMARY_RANGE[1]]
    secondary_values = [SECONDARY_RANGE[0], 1.541, SECONDARY_RANGE[1]]
    primary_response = [_model(value, secondary, False)[1] for value in primary_values]
    secondary_response = [
        _model(primary, value, False)[1] for value in secondary_values
    ]
    failed = _model(primary, secondary, True)
    recovered = _model(2.188, 1.541, False)
    return {
        "metrics": [
            {
                "id": "primary",
                "label": "Current gear ratio",
                "value": primary,
                "unit": "ratio",
                "emphasis": "primary",
            },
            {
                "id": "secondary",
                "label": "Next gear ratio",
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
            "primary_sweep": _plot(PRIMARY, primary_values, primary_response, "ratio"),
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
            "observation": "At a valid force-crossover shift, adjacent-gear wheel forces are equal within grid resolution.",
            "broken": "Broken mode makes the next ratio greater than the current ratio and flags the invalid sequence.",
            "recovery": "Restore a strictly descending adjacent-gear pair and recompute the crossover below redline.",
        },
        "diagnostics": {
            "item_id": "P14",
            "signature": signature,
            "fields": FIELDS,
            "broken_active": broken,
            "bounded_points": 121,
        },
    }
