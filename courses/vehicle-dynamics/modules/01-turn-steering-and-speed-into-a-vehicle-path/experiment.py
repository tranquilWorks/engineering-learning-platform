from __future__ import annotations
import math
from typing import Any

PRIMARY = "steering_deg"
SECONDARY = "speed_mps"
PRIMARY_RANGE = (-20.0, 20.0)
SECONDARY_RANGE = (1.0, 45.0)


def _model(a: float, b: float, broken: bool) -> list[float]:
    delta = math.radians(a)
    speed = b
    L = 2.57
    ratio = 13.0
    mu = 1.0
    curvature = math.tan(delta / ratio) / L
    yaw = speed * curvature
    ay = speed * yaw
    limit = mu * 9.81
    if broken:
        ay *= 1.35
    return [curvature, yaw, ay, limit, float(abs(ay) > limit)]


def _plot(name: str, x: list[float], y: list[float]) -> dict[str, Any]:
    return {
        "data": [
            {"type": "scatter", "mode": "lines+markers", "name": name, "x": x, "y": y}
        ],
        "layout": {
            "title": {"text": "Turn Steering and Speed into a Vehicle Path"},
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
    px = [PRIMARY_RANGE[0], 5.0, PRIMARY_RANGE[1]]
    sx = [SECONDARY_RANGE[0], 15.0, SECONDARY_RANGE[1]]
    py = [_model(v, b, False)[1] for v in px]
    sy = [_model(a, v, False)[1] for v in sx]
    recovered = _model(5.0, 15.0, False)
    failed = _model(a, b, True)
    return {
        "metrics": [
            {
                "id": "primary",
                "label": "steering_deg",
                "value": a,
                "unit": "deg",
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
            "observation": "Absolute lateral acceleration cannot exceed mu*g without sliding.",
            "broken": "Ignoring the friction boundary at high speed",
            "recovery": "Reduce steering or speed until |a_y| <= mu*g",
        },
        "diagnostics": {
            "item_id": "P01",
            "signature": signature,
            "broken_active": broken,
            "bounded_points": 3,
        },
    }
