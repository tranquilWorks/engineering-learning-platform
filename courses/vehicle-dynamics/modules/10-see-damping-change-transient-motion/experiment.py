from __future__ import annotations

import math
from typing import Any

PRIMARY = "damping_n_s_m"
SECONDARY = "spring_rate_n_m"
PRIMARY_RANGE = (400.0, 8000.0)
SECONDARY_RANGE = (15000.0, 70000.0)
FIELDS = [
    "natural_frequency_hz",
    "damping_ratio",
    "damped_frequency_hz",
    "overshoot_ratio",
    "settling_time_s",
    "decay_rate_s_inv",
    "invalid",
]


def _model(a: float, b: float, broken: bool) -> list[float]:
    damping = -a if broken else a
    stiffness = b
    sprung = 300.0
    omega_n = math.sqrt(stiffness / sprung)
    zeta = damping / (2.0 * math.sqrt(stiffness * sprung))
    damped = omega_n * math.sqrt(max(0.0, 1.0 - zeta**2)) / (2.0 * math.pi)
    overshoot = (
        math.exp(-math.pi * zeta / math.sqrt(max(1e-12, 1.0 - zeta**2)))
        if 0.0 < zeta < 1.0
        else (0.0 if zeta >= 1.0 else 1.0)
    )
    settling = 4.0 / (zeta * omega_n) if zeta > 0.0 else 0.0
    decay = zeta * omega_n
    return [
        omega_n / (2.0 * math.pi),
        zeta,
        damped,
        overshoot,
        settling,
        decay,
        float(zeta <= 0.0),
    ]


def _plot(name: str, x: list[float], y: list[float], x_unit: str) -> dict[str, Any]:
    return {
        "data": [
            {"type": "scatter", "mode": "lines+markers", "name": name, "x": x, "y": y}
        ],
        "layout": {
            "title": {"text": "See Damping Change Transient Motion"},
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
    primary_values = [PRIMARY_RANGE[0], 3200.0, PRIMARY_RANGE[1]]
    secondary_values = [SECONDARY_RANGE[0], 35000.0, SECONDARY_RANGE[1]]
    primary_response = [_model(value, secondary, False)[1] for value in primary_values]
    secondary_response = [
        _model(primary, value, False)[1] for value in secondary_values
    ]
    failed = _model(primary, secondary, True)
    recovered = _model(3200.0, 35000.0, False)
    return {
        "metrics": [
            {
                "id": "primary",
                "label": "Damper coefficient",
                "value": primary,
                "unit": "N*s/m",
                "emphasis": "primary",
            },
            {
                "id": "secondary",
                "label": "Wheel rate",
                "value": secondary,
                "unit": "N/m",
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
            "primary_sweep": _plot(PRIMARY, primary_values, primary_response, "N*s/m"),
            "secondary_sweep": _plot(
                SECONDARY, secondary_values, secondary_response, "N/m"
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
            "observation": "Positive damping dissipates energy; negative damping makes the homogeneous response grow.",
            "broken": "Broken mode reverses the damping sign and creates an explicitly unstable response.",
            "recovery": "Restore positive damping and verify a finite positive decay rate.",
        },
        "diagnostics": {
            "item_id": "P10",
            "signature": signature,
            "fields": FIELDS,
            "broken_active": broken,
            "bounded_points": 3,
        },
    }
