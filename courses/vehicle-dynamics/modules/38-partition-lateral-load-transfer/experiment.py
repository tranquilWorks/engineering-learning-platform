from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 38
DEFAULTS = {"lateral_accel_g": 1.0, "front_roll_stiffness_fraction": 0.58}
RANGES = {"lateral_accel_g": (0.2, 1.5), "front_roll_stiffness_fraction": (0.3, 0.75)}
BROKEN_TEXT = "Broken mode adds full elastic roll moment without subtracting geometric transfer, double-counting the roll-center path."
RECOVERY_TEXT = "Subtract geometric roll moment before distributing the elastic remainder and verify exact roll-moment closure."


def _parameters(supplied: dict[str, Any]) -> dict[str, float]:
    result: dict[str, float] = {}
    for key, default in DEFAULTS.items():
        value = float(supplied.get(key, default))
        minimum, maximum = RANGES[key]
        if not np.isfinite(value) or value < minimum or value > maximum:
            raise ValueError(f"{key} outside declared finite range [{minimum}, {maximum}]")
        result[key] = value
    return result


def _trace(
    name: str,
    x: Any,
    y: Any,
    x_quantity: str,
    x_unit: str,
    y_quantity: str,
    y_unit: str,
    *,
    mode: str = "lines",
) -> dict[str, Any]:
    return {
        "type": "scattergl",
        "mode": mode,
        "name": name,
        "x": np.asarray(x, dtype=float),
        "y": np.asarray(y, dtype=float),
        "meta": {
            "x_quantity": x_quantity,
            "x_unit": x_unit,
            "y_quantity": y_quantity,
            "y_unit": y_unit,
        },
    }


def _plot(
    title: str,
    x_title: str,
    y_title: str,
    traces: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "data": traces,
        "layout": {
            "title": {"text": title, "x": 0.02},
            "xaxis": {"title": {"text": x_title}},
            "yaxis": {"title": {"text": y_title}},
            "legend": {"orientation": "h"},
            "margin": {"l": 72, "r": 36, "t": 62, "b": 62},
            "hovermode": "closest",
            "uirevision": "keep-view",
        },
        "config": {"responsive": True, "displaylogo": False},
    }


def _result(model: dict[str, Any], broken: bool) -> dict[str, Any]:
    return {
        "metrics": [
            {
                "id": key,
                "label": label,
                "value": float(value),
                "unit": unit,
                "emphasis": "primary" if index == 0 else "normal",
            }
            for index, (key, label, value, unit) in enumerate(model["metrics"])
        ],
        "plots": model["plots"],
        "explanations": {
            "observation": model["observation"],
            "broken": BROKEN_TEXT,
            "recovery": RECOVERY_TEXT,
        },
        "diagnostics": {
            "item_number": ITEM_NUMBER,
            "broken_active": bool(broken),
            "signature": [float(value) for value in model["signature"]],
        },
    }


def _capacity_loss(axle_load: float, transfer: float) -> float:
    exponent, reference_load, reference_mu = 0.86, 3500.0, 1.25
    left = max(1.0, axle_load / 2.0 - transfer / 2.0)
    right = axle_load / 2.0 + transfer / 2.0
    force = lambda load: reference_mu * reference_load * (load / reference_load) ** exponent
    return float(2.0 * force(axle_load / 2.0) - force(left) - force(right))


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    mass, gravity = 1450.0, 9.81
    a, b, height = 1.20, 1.50, 0.52
    front_track, rear_track = 1.55, 1.53
    front_rc, rear_rc = 0.07, 0.11
    accel = p["lateral_accel_g"] * gravity
    front_fraction = p["front_roll_stiffness_fraction"]
    front_mass = mass * b / (a + b)
    rear_mass = mass * a / (a + b)
    geometric_front_moment = front_mass * accel * front_rc
    geometric_rear_moment = rear_mass * accel * rear_rc
    total_moment = mass * accel * height
    geometric_moment = geometric_front_moment + geometric_rear_moment
    elastic_moment = total_moment if broken else total_moment - geometric_moment
    front_transfer = geometric_front_moment / front_track + front_fraction * elastic_moment / front_track
    rear_transfer = geometric_rear_moment / rear_track + (1.0 - front_fraction) * elastic_moment / rear_track
    reconstructed = front_transfer * front_track + rear_transfer * rear_track
    closure = abs(reconstructed - total_moment)
    geometric_fraction = geometric_moment / total_moment
    front_axle_load = mass * gravity * b / (a + b)
    capacity_loss = _capacity_loss(front_axle_load, front_transfer)
    signature = [front_transfer, rear_transfer, geometric_fraction, closure, capacity_loss]
    fractions = np.linspace(0.30, 0.75, 91)
    front_values = []
    rear_values = []
    for fraction in fractions:
        front_values.append(geometric_front_moment / front_track + fraction * elastic_moment / front_track)
        rear_values.append(geometric_rear_moment / rear_track + (1.0 - fraction) * elastic_moment / rear_track)
    return {
        "signature": signature,
        "metrics": [
            ("front_transfer", "Front lateral load transfer", front_transfer, "N"),
            ("rear_transfer", "Rear lateral load transfer", rear_transfer, "N"),
            ("geometric_fraction", "Geometric roll-moment fraction", geometric_fraction, "1"),
            ("closure", "Roll-moment closure residual", closure, "N*m"),
        ],
        "plots": {
            "response": _plot(
                "Load-transfer distribution",
                "Front elastic roll-stiffness fraction (1)",
                "Lateral load transfer (N)",
                [
                    _trace("Front axle", fractions, front_values, "Front elastic roll-stiffness fraction", "1", "Lateral load transfer", "N"),
                    _trace("Rear axle", fractions, rear_values, "Front elastic roll-stiffness fraction", "1", "Lateral load transfer", "N"),
                ],
            ),
            "mechanism": _plot(
                "Front tire-capacity loss",
                "Front lateral load transfer (N)",
                "Paired peak-force loss (N)",
                [
                    _trace("Load-sensitivity loss", [front_transfer], [capacity_loss], "Front lateral load transfer", "N", "Paired peak-force loss", "N", mode="markers"),
                ],
            ),
        },
        "observation": "Geometric and elastic paths must reconstruct the same total roll moment before tire-load sensitivity is applied.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
