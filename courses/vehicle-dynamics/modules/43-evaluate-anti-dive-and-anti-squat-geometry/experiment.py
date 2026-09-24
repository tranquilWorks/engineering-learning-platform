from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 43
DEFAULTS = {"sideview_angle_deg": 5.0, "cg_height_m": 0.52}
RANGES = {"sideview_angle_deg": (1.0, 8.0), "cg_height_m": (0.40, 0.70)}
BROKEN_TEXT = "Broken mode sends degrees directly into the tangent function, producing nonphysical anti percentages and a failed pitch-load-transfer closure."
RECOVERY_TEXT = "Convert side-view angle to radians, bound anti percentages below lift, and partition the same pitch load transfer exactly once."


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


def _anti_fractions(angle_deg: float, height: float, broken: bool) -> tuple[float, float]:
    used_angle = angle_deg if broken else np.deg2rad(angle_deg)
    tangent = np.tan(used_angle)
    wheelbase = 2.70
    anti_dive = 0.70 * tangent * wheelbase / height
    anti_squat = tangent * wheelbase / height
    return float(anti_dive), float(anti_squat)


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    angle, height = p["sideview_angle_deg"], p["cg_height_m"]
    anti_dive, anti_squat = _anti_fractions(angle, height, broken)
    mass, gravity, wheelbase = 1450.0, 9.81, 2.70
    longitudinal_accel = 0.80 * gravity
    total_transfer = mass * longitudinal_accel * height / wheelbase
    geometric_transfer = anti_dive * total_transfer
    spring_transfer = (1.0 - anti_dive) * total_transfer
    physical_anti_dive, _ = _anti_fractions(angle, height, False)
    closure = abs(geometric_transfer - physical_anti_dive * total_transfer)
    signature = [
        100.0 * anti_dive,
        100.0 * anti_squat,
        spring_transfer,
        geometric_transfer,
        closure,
    ]
    angle_sweep = np.linspace(1.0, 8.0, 71)
    dive_values = []
    squat_values = []
    for value in angle_sweep:
        dive, squat = _anti_fractions(value, height, broken)
        dive_values.append(100.0 * dive)
        squat_values.append(100.0 * squat)
    return {
        "signature": signature,
        "metrics": [
            ("anti_dive", "Anti-dive", signature[0], "%"),
            ("anti_squat", "Anti-squat", signature[1], "%"),
            ("spring_transfer", "Spring-supported transfer", spring_transfer, "N"),
            ("closure", "Pitch-transfer closure residual", closure, "N"),
        ],
        "plots": {
            "response": _plot(
                "Side-view anti geometry",
                "Force-line angle (deg)",
                "Anti percentage (%)",
                [
                    _trace("Anti-dive", angle_sweep, dive_values, "Force-line angle", "deg", "Anti percentage", "%"),
                    _trace("Anti-squat", angle_sweep, squat_values, "Force-line angle", "deg", "Anti percentage", "%"),
                ],
            ),
            "mechanism": _plot(
                "Pitch load-transfer partition",
                "Transfer path (1)",
                "Longitudinal load transfer (N)",
                [
                    _trace("Load-transfer path", [1.0, 2.0], [geometric_transfer, spring_transfer], "Transfer path", "1", "Longitudinal load transfer", "N", mode="markers"),
                ],
            ),
        },
        "observation": "Anti geometry changes the path carrying pitch load transfer; it does not create or remove the total longitudinal load transfer.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
