from __future__ import annotations
import math
from typing import Any

PRIMARY = "slip_ratio"
SECONDARY = "normal_load_n"
PRIMARY_RANGE = (-0.3, 0.3)
SECONDARY_RANGE = (1000.0, 6000.0)


def _model(a: float, b: float, broken: bool) -> list[float]:
    kappa = a
    load = b
    mu = 1.05
    stiffness = 85000.0
    force = mu * load * math.tanh(stiffness * kappa / (mu * load))
    if broken:
        force = -force
    return [kappa, force, mu * load, stiffness, float(broken)]


def _plot(name: str, x: list[float], y: list[float]) -> dict[str, Any]:
    return {
        "data": [
            {"type": "scatter", "mode": "lines+markers", "name": name, "x": x, "y": y}
        ],
        "layout": {
            "title": {"text": "Build Slip-Ratio Intuition"},
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
    px = [PRIMARY_RANGE[0], 0.08, PRIMARY_RANGE[1]]
    sx = [SECONDARY_RANGE[0], 3600.0, SECONDARY_RANGE[1]]
    py = [_model(v, b, False)[1] for v in px]
    sy = [_model(a, v, False)[1] for v in sx]
    recovered = _model(0.08, 3600.0, False)
    failed = _model(a, b, True)
    return {
        "metrics": [
            {
                "id": "primary",
                "label": "slip_ratio",
                "value": a,
                "unit": "ratio",
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
            "observation": "Force is zero at zero slip, linear near zero, then saturates.",
            "broken": "Silently reversing the slip-ratio sign",
            "recovery": "Restore kappa=(wheel speed-ground speed)/|ground speed|",
        },
        "diagnostics": {
            "item_id": "P05",
            "signature": signature,
            "broken_active": broken,
            "bounded_points": 3,
        },
    }
