from __future__ import annotations

import math
from typing import Any

PRIMARY = "spring_rate_n_m"
SECONDARY = "motion_ratio"
PRIMARY_RANGE = (15000.0, 80000.0)
SECONDARY_RANGE = (0.6, 1.1)
FIELDS = [
    "wheel_rate_n_m",
    "ride_frequency_hz",
    "static_deflection_m",
    "spring_rate_n_m",
    "motion_ratio",
    "invalid",
]


def _model(a: float, b: float, broken: bool) -> list[float]:
    spring = a
    ratio = b
    sprung = 300.0
    gravity = 9.81
    wheel_rate = spring * (ratio if broken else ratio**2)
    frequency = math.sqrt(wheel_rate / sprung) / (2.0 * math.pi)
    deflection = sprung * gravity / wheel_rate
    return [wheel_rate, frequency, deflection, spring, ratio, float(broken)]


def _plot(name: str, x: list[float], y: list[float], x_unit: str) -> dict[str, Any]:
    return {
        "data": [
            {"type": "scatter", "mode": "lines+markers", "name": name, "x": x, "y": y}
        ],
        "layout": {
            "title": {"text": "Choose Spring Rate and Ride Frequency"},
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
    primary_values = [PRIMARY_RANGE[0], 35000.0, PRIMARY_RANGE[1]]
    secondary_values = [SECONDARY_RANGE[0], 0.9, SECONDARY_RANGE[1]]
    primary_response = [_model(value, secondary, False)[1] for value in primary_values]
    secondary_response = [
        _model(primary, value, False)[1] for value in secondary_values
    ]
    failed = _model(primary, secondary, True)
    recovered = _model(35000.0, 0.9, False)
    return {
        "metrics": [
            {
                "id": "primary",
                "label": "Spring rate",
                "value": primary,
                "unit": "N/m",
                "emphasis": "primary",
            },
            {
                "id": "secondary",
                "label": "Spring-travel / wheel-travel ratio",
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
            "primary_sweep": _plot(PRIMARY, primary_values, primary_response, "N/m"),
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
            "observation": "Wheel rate follows the square of motion ratio, and static load equals wheel rate times static deflection.",
            "broken": "Broken mode incorrectly omits the squared motion-ratio transformation.",
            "recovery": "Restore k_w=k_s*i^2 and the baseline spring rate and motion ratio.",
        },
        "diagnostics": {
            "item_id": "P09",
            "signature": signature,
            "fields": FIELDS,
            "broken_active": broken,
            "bounded_points": 3,
        },
    }
