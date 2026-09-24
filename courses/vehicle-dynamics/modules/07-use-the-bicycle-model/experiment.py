from __future__ import annotations
import math
from typing import Any

PRIMARY = "steering_deg"
SECONDARY = "speed_mps"
PRIMARY_RANGE = (-8.0, 8.0)
SECONDARY_RANGE = (3.0, 40.0)


def _model(a: float, b: float, broken: bool) -> list[float]:
    delta = math.radians(a)
    speed = b
    mass = 1320.0
    lf = 1.15
    lr = 1.42
    cf = 90000.0
    cr = 100000.0
    aa = -(cf + cr) / speed
    ab = (-lf * cf + lr * cr) / speed - mass * speed
    ba = -lf * cf + lr * cr
    bb = -(lf**2 * cf + lr**2 * cr)
    det = aa * bb - ab * ba
    q1 = -cf * delta
    q2 = -lf * cf * delta
    beta = (q1 * bb - ab * q2) / det
    yaw = (aa * q2 - q1 * ba) / det
    af = delta - beta - lf * yaw / speed
    ar = -beta + lr * yaw / speed
    invalid = max(abs(af), abs(ar), abs(delta)) > math.radians(8) or broken
    return [beta, yaw, af, ar, mass * speed * yaw, float(invalid)]


def _plot(name: str, x: list[float], y: list[float]) -> dict[str, Any]:
    return {
        "data": [
            {"type": "scatter", "mode": "lines+markers", "name": name, "x": x, "y": y}
        ],
        "layout": {
            "title": {"text": "Use the Bicycle Model"},
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
    px = [PRIMARY_RANGE[0], 3.0, PRIMARY_RANGE[1]]
    sx = [SECONDARY_RANGE[0], 18.0, SECONDARY_RANGE[1]]
    py = [_model(v, b, False)[1] for v in px]
    sy = [_model(a, v, False)[1] for v in sx]
    recovered = _model(3.0, 18.0, False)
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
            "observation": "Axle forces balance m*V*r and yaw moments balance zero.",
            "broken": "Using the linear model at large angles",
            "recovery": "Return steer and axle slip angles to the small-angle range",
        },
        "diagnostics": {
            "item_id": "P07",
            "signature": signature,
            "broken_active": broken,
            "bounded_points": 3,
        },
    }
