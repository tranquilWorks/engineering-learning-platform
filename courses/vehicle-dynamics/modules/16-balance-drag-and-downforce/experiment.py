from __future__ import annotations

import math
from typing import Any

PRIMARY = "speed_m_s"
SECONDARY = "wing_angle_deg"
PRIMARY_RANGE = (10.0, 70.0)
SECONDARY_RANGE = (0.0, 18.0)
FIELDS = [
    "dynamic_pressure_pa",
    "drag_n",
    "downforce_n",
    "tire_capacity_n",
    "drag_power_w",
    "front_aero_share",
    "invalid",
]


def _model(a: float, b: float, broken: bool) -> list[float]:
    speed = a
    angle = b
    rho = 1.225
    mass = 1320.0
    gravity = 9.81
    mu = 1.0
    q = 0.5 * rho * speed**2
    cda = 0.65 + 0.0015 * angle**2
    cla = 0.30 + 0.045 * angle
    drag = q * cda
    downforce = q * cla
    front_share = 0.48 + 0.006 * angle
    if broken:
        drag = -drag
        front_share = 1.20
    capacity = mu * (mass * gravity + downforce)
    power = drag * speed
    return [
        q,
        drag,
        downforce,
        capacity,
        power,
        front_share,
        float(drag < 0.0 or not 0.0 <= front_share <= 1.0),
    ]


def _plot(name: str, x: list[float], y: list[float], x_unit: str) -> dict[str, Any]:
    return {
        "data": [
            {"type": "scatter", "mode": "lines+markers", "name": name, "x": x, "y": y}
        ],
        "layout": {
            "title": {"text": "Balance Drag and Downforce"},
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
    primary_values = [PRIMARY_RANGE[0], 40.0, PRIMARY_RANGE[1]]
    secondary_values = [SECONDARY_RANGE[0], 8.0, SECONDARY_RANGE[1]]
    primary_response = [_model(value, secondary, False)[1] for value in primary_values]
    secondary_response = [
        _model(primary, value, False)[1] for value in secondary_values
    ]
    failed = _model(primary, secondary, True)
    recovered = _model(40.0, 8.0, False)
    return {
        "metrics": [
            {
                "id": "primary",
                "label": "Vehicle speed",
                "value": primary,
                "unit": "m/s",
                "emphasis": "primary",
            },
            {
                "id": "secondary",
                "label": "Wing angle",
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
            "primary_sweep": _plot(PRIMARY, primary_values, primary_response, "m/s"),
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
            "observation": "At fixed coefficients, drag and downforce scale with speed squared.",
            "broken": "Broken mode reverses the drag sign and drives aero balance outside [0,1].",
            "recovery": "Restore positive CdA, downward-positive ClA, and a bounded front aero share.",
        },
        "diagnostics": {
            "item_id": "P16",
            "signature": signature,
            "fields": FIELDS,
            "broken_active": broken,
            "bounded_points": 3,
        },
    }
