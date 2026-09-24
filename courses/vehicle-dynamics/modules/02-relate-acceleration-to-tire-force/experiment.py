from __future__ import annotations
import math
from typing import Any

PRIMARY = "tractive_force_n"
SECONDARY = "speed_mps"
PRIMARY_RANGE = (0.0, 9000.0)
SECONDARY_RANGE = (0.0, 55.0)


def _model(a: float, b: float, broken: bool) -> list[float]:
    request = a
    speed = b
    mass = 1320.0
    mu = 1.0
    rolling = 0.015 * mass * 9.81
    drag = 0.5 * 1.225 * 0.31 * 2.0 * speed**2
    limit = mu * mass * 9.81
    applied = request if broken else min(request, limit)
    accel = (applied - rolling - drag) / mass
    return [applied, rolling, drag, accel, limit, float(request > limit)]


def _plot(name: str, x: list[float], y: list[float]) -> dict[str, Any]:
    return {
        "data": [
            {"type": "scatter", "mode": "lines+markers", "name": name, "x": x, "y": y}
        ],
        "layout": {
            "title": {"text": "Relate Acceleration to Tire Force"},
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
    px = [PRIMARY_RANGE[0], 4200.0, PRIMARY_RANGE[1]]
    sx = [SECONDARY_RANGE[0], 20.0, SECONDARY_RANGE[1]]
    py = [_model(v, b, False)[1] for v in px]
    sy = [_model(a, v, False)[1] for v in sx]
    recovered = _model(4200.0, 20.0, False)
    failed = _model(a, b, True)
    return {
        "metrics": [
            {
                "id": "primary",
                "label": "tractive_force_n",
                "value": a,
                "unit": "N",
                "emphasis": "primary",
            },
            {"id": "secondary", "label": "speed_mps", "value": b, "unit": "m/s"},
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
            "observation": "Applied tire force is bounded by mu*m*g and drag grows with speed squared.",
            "broken": "Requesting force beyond the tire limit",
            "recovery": "Cap requested force at mu*m*g",
        },
        "diagnostics": {
            "item_id": "P02",
            "signature": signature,
            "broken_active": broken,
            "bounded_points": 3,
        },
    }
