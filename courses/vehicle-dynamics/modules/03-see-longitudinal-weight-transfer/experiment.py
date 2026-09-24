from __future__ import annotations
import math
from typing import Any

PRIMARY = "acceleration_mps2"
SECONDARY = "cg_height_m"
PRIMARY_RANGE = (-9.0, 9.0)
SECONDARY_RANGE = (0.25, 0.85)


def _model(a: float, b: float, broken: bool) -> list[float]:
    accel = a
    height = b
    mass = 1320.0
    g = 9.81
    L = 2.57
    front0 = 0.53 * mass * g
    transfer = mass * accel * height / L
    front = front0 - transfer
    rear = mass * g - front
    if broken:
        front -= 0.65 * mass * g
        rear = mass * g - front
    return [front, rear, transfer, front + rear, float(min(front, rear) < 0)]


def _plot(name: str, x: list[float], y: list[float]) -> dict[str, Any]:
    return {
        "data": [
            {"type": "scatter", "mode": "lines+markers", "name": name, "x": x, "y": y}
        ],
        "layout": {
            "title": {"text": "See Longitudinal Weight Transfer"},
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
    px = [PRIMARY_RANGE[0], 4.0, PRIMARY_RANGE[1]]
    sx = [SECONDARY_RANGE[0], 0.5, SECONDARY_RANGE[1]]
    py = [_model(v, b, False)[1] for v in px]
    sy = [_model(a, v, False)[1] for v in sx]
    recovered = _model(4.0, 0.5, False)
    failed = _model(a, b, True)
    return {
        "metrics": [
            {
                "id": "primary",
                "label": "acceleration_mps2",
                "value": a,
                "unit": "m/s^2",
                "emphasis": "primary",
            },
            {"id": "secondary", "label": "cg_height_m", "value": b, "unit": "m"},
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
            "observation": "Front plus rear axle load remains mass*g.",
            "broken": "Unloading an axle below zero",
            "recovery": "Restore acceleration so both axle loads are nonnegative",
        },
        "diagnostics": {
            "item_id": "P03",
            "signature": signature,
            "broken_active": broken,
            "bounded_points": 3,
        },
    }
