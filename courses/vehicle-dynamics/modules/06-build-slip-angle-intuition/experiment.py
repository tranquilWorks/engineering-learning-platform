from __future__ import annotations
import math
from typing import Any

PRIMARY = "slip_angle_deg"
SECONDARY = "normal_load_n"
PRIMARY_RANGE = (-14.0, 14.0)
SECONDARY_RANGE = (1000.0, 6000.0)


def _model(a: float, b: float, broken: bool) -> list[float]:
    alpha = math.radians(a)
    load = b
    mu = 1.05
    stiffness = 78000.0
    force = -mu * load * math.tanh(stiffness * alpha / (mu * load))
    if broken:
        force = -force
    return [alpha, force, mu * load, stiffness, float(broken)]


def _plot(name: str, x: list[float], y: list[float]) -> dict[str, Any]:
    return {
        "data": [
            {"type": "scatter", "mode": "lines+markers", "name": name, "x": x, "y": y}
        ],
        "layout": {
            "title": {"text": "Build Slip-Angle Intuition"},
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
    sx = [SECONDARY_RANGE[0], 3600.0, SECONDARY_RANGE[1]]
    py = [_model(v, b, False)[1] for v in px]
    sy = [_model(a, v, False)[1] for v in sx]
    recovered = _model(4.0, 3600.0, False)
    failed = _model(a, b, True)
    return {
        "metrics": [
            {
                "id": "primary",
                "label": "slip_angle_deg",
                "value": a,
                "unit": "deg",
                "emphasis": "primary",
            },
            {"id": "secondary", "label": "normal_load_n", "value": b, "unit": "N"},
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
            "observation": "Force is zero at zero slip angle and opposes positive slip angle.",
            "broken": "Reversing the force sign",
            "recovery": "Restore Fy=-Calpha*alpha near zero",
        },
        "diagnostics": {
            "item_id": "P06",
            "signature": signature,
            "broken_active": broken,
            "bounded_points": 3,
        },
    }
