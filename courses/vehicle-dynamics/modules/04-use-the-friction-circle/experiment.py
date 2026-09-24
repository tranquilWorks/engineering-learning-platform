from __future__ import annotations
import math
from typing import Any

PRIMARY = "longitudinal_force_n"
SECONDARY = "lateral_force_n"
PRIMARY_RANGE = (-6500.0, 6500.0)
SECONDARY_RANGE = (-6500.0, 6500.0)


def _model(a: float, b: float, broken: bool) -> list[float]:
    fx = a
    fy = b
    capacity = 1.05 * 3600.0
    use = math.hypot(fx, fy) / capacity
    scale = 1.0 if broken or use <= 1 else 1 / use
    return [fx * scale, fy * scale, use, capacity, float(use > 1)]


def _plot(name: str, x: list[float], y: list[float]) -> dict[str, Any]:
    return {
        "data": [
            {"type": "scatter", "mode": "lines+markers", "name": name, "x": x, "y": y}
        ],
        "layout": {
            "title": {"text": "Use the Friction Circle"},
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
    px = [PRIMARY_RANGE[0], 2800.0, PRIMARY_RANGE[1]]
    sx = [SECONDARY_RANGE[0], 3500.0, SECONDARY_RANGE[1]]
    py = [_model(v, b, False)[1] for v in px]
    sy = [_model(a, v, False)[1] for v in sx]
    recovered = _model(2800.0, 3500.0, False)
    failed = _model(a, b, True)
    return {
        "metrics": [
            {
                "id": "primary",
                "label": "longitudinal_force_n",
                "value": a,
                "unit": "N",
                "emphasis": "primary",
            },
            {"id": "secondary", "label": "lateral_force_n", "value": b, "unit": "N"},
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
            "observation": "Combined-force utilization cannot exceed one.",
            "broken": "Commanding force outside the circle",
            "recovery": "Scale both components by reciprocal utilization",
        },
        "diagnostics": {
            "item_id": "P04",
            "signature": signature,
            "broken_active": broken,
            "bounded_points": 3,
        },
    }
