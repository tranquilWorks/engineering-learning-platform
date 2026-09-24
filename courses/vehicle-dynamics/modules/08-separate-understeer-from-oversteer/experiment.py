from __future__ import annotations
import math
from typing import Any

PRIMARY = "front_cornering_stiffness_n_rad"
SECONDARY = "rear_cornering_stiffness_n_rad"
PRIMARY_RANGE = (45000.0, 140000.0)
SECONDARY_RANGE = (45000.0, 140000.0)


def _model(a: float, b: float, broken: bool) -> list[float]:
    cf = a
    cr = b
    mass = 1320.0
    lf = 1.15
    lr = 1.42
    L = lf + lr
    speed = 25.0
    k = mass / L * (lr / cf - lf / cr)
    critical = math.sqrt(-L / k) if k < 0 else 0.0
    denominator = L + k * speed**2
    if broken and k < 0:
        speed = max(speed, critical * 1.05)
        denominator = L + k * speed**2
    return [
        k,
        math.degrees(k * 9.81),
        critical,
        speed,
        denominator,
        float(denominator <= 0),
    ]


def _plot(name: str, x: list[float], y: list[float]) -> dict[str, Any]:
    return {
        "data": [
            {"type": "scatter", "mode": "lines+markers", "name": name, "x": x, "y": y}
        ],
        "layout": {
            "title": {"text": "Separate Understeer from Oversteer"},
            "xaxis": {"title": "controlled physical input"},
            "yaxis": {"title": "model response (SI units)"},
            "uirevision": "keep-view",
        },
        "config": {"responsive": True, "displaylogo": False},
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    a = float(parameters[PRIMARY])
    b = float(parameters[SECONDARY])
    broken = bool(parameters["broken_mode"])
    if not math.isfinite(a) or not PRIMARY_RANGE[0] <= a <= PRIMARY_RANGE[1]:
        raise ValueError(f"{PRIMARY} outside declared finite range")
    if not math.isfinite(b) or not SECONDARY_RANGE[0] <= b <= SECONDARY_RANGE[1]:
        raise ValueError(f"{SECONDARY} outside declared finite range")
    signature = _model(a, b, broken)
    if not all(math.isfinite(v) for v in signature):
        raise ValueError("non-finite model result")
    px = [PRIMARY_RANGE[0], 90000.0, PRIMARY_RANGE[1]]
    sx = [SECONDARY_RANGE[0], 100000.0, SECONDARY_RANGE[1]]
    py = [_model(v, b, False)[1] for v in px]
    sy = [_model(a, v, False)[1] for v in sx]
    recovered = _model(90000.0, 100000.0, False)
    failed = _model(a, b, True)
    return {
        "metrics": [
            {
                "id": "primary",
                "label": "front_cornering_stiffness_n_rad",
                "value": a,
                "unit": "N/rad",
                "emphasis": "primary",
            },
            {
                "id": "secondary",
                "label": "rear_cornering_stiffness_n_rad",
                "value": b,
                "unit": "N/rad",
            },
            {
                "id": "valid",
                "label": "Boundary valid",
                "value": not bool(signature[-1]),
                "unit": "boolean",
            },
        ],
        "plots": {
            "response": _plot(
                "signature", list(range(len(signature) - 1)), signature[:-1]
            ),
            "primary_sweep": _plot(PRIMARY, px, py),
            "secondary_sweep": _plot(SECONDARY, sx, sy),
            "broken_recovery": {
                "data": [
                    {
                        "type": "bar",
                        "name": "broken",
                        "x": list(range(len(failed) - 1)),
                        "y": failed[:-1],
                    },
                    {
                        "type": "bar",
                        "name": "recovered",
                        "x": list(range(len(recovered) - 1)),
                        "y": recovered[:-1],
                    },
                ],
                "layout": {
                    "barmode": "group",
                    "xaxis": {"title": "signature field"},
                    "yaxis": {"title": "SI value"},
                },
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "K>0 understeers; K=0 is neutral; K<0 has finite critical speed.",
            "broken": "Operating at or above oversteer critical speed",
            "recovery": "Increase rear stability margin or reduce speed",
        },
        "diagnostics": {
            "item_id": "P08",
            "signature": signature,
            "broken_active": broken,
            "bounded_points": 3,
        },
    }
