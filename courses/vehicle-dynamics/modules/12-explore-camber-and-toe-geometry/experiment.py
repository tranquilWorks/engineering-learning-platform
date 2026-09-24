from __future__ import annotations

import math
from typing import Any

PRIMARY = "camber_deg"
SECONDARY = "toe_deg"
PRIMARY_RANGE = (-5.0, 2.0)
SECONDARY_RANGE = (-0.5, 0.5)
FIELDS = [
    "camber_rad",
    "toe_rad",
    "camber_thrust_n",
    "scrub_force_n",
    "scrub_power_w",
    "effective_heading_rad",
    "invalid",
]


def _model(a: float, b: float, broken: bool) -> list[float]:
    camber = math.radians(a)
    toe = math.radians(b)
    load = 3600.0
    speed = 20.0
    camber_stiffness = 60000.0
    if broken:
        camber = a
        toe = b
    thrust = -camber_stiffness * camber
    scrub = load * abs(math.tan(toe))
    power = scrub * speed
    return [camber, toe, thrust, scrub, power, toe, float(broken)]


def _plot(name: str, x: list[float], y: list[float], x_unit: str) -> dict[str, Any]:
    return {
        "data": [
            {"type": "scatter", "mode": "lines+markers", "name": name, "x": x, "y": y}
        ],
        "layout": {
            "title": {"text": "Explore Camber and Toe Geometry"},
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
    primary_values = [PRIMARY_RANGE[0], -2.0, PRIMARY_RANGE[1]]
    secondary_values = [SECONDARY_RANGE[0], 0.1, SECONDARY_RANGE[1]]
    primary_response = [_model(value, secondary, False)[1] for value in primary_values]
    secondary_response = [
        _model(primary, value, False)[1] for value in secondary_values
    ]
    failed = _model(primary, secondary, True)
    recovered = _model(-2.0, 0.1, False)
    return {
        "metrics": [
            {
                "id": "primary",
                "label": "Camber angle",
                "value": primary,
                "unit": "deg",
                "emphasis": "primary",
            },
            {
                "id": "secondary",
                "label": "Toe angle",
                "value": secondary,
                "unit": "deg",
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
            "primary_sweep": _plot(PRIMARY, primary_values, primary_response, "deg"),
            "secondary_sweep": _plot(
                SECONDARY, secondary_values, secondary_response, "deg"
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
            "observation": "Zero camber removes camber thrust and zero toe removes this model's scrub loss.",
            "broken": "Broken mode feeds degree values directly to radian trigonometric relations.",
            "recovery": "Convert both alignment angles to radians exactly once and restore the declared signs.",
        },
        "diagnostics": {
            "item_id": "P12",
            "signature": signature,
            "fields": FIELDS,
            "broken_active": broken,
            "bounded_points": 3,
        },
    }
