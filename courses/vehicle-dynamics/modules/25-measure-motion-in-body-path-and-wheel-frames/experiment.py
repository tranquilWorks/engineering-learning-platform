from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 25
DEFAULTS = {"path_heading_deg": 32, "wheel_steer_deg": 8}
RANGES = {"path_heading_deg": (-180, 180), "wheel_steer_deg": (-35, 35)}
BROKEN_TEXT = "Broken mode passes degrees directly to trigonometric functions, corrupting declared frame components."
RECOVERY_TEXT = "Convert degrees to radians exactly once, then verify expected components, norm, and inverse rotation."


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


def _rotation(angle: float) -> np.ndarray:
    return np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    heading_true = np.deg2rad(p["path_heading_deg"])
    heading_used = p["path_heading_deg"] if broken else heading_true
    steer = np.deg2rad(p["wheel_steer_deg"])
    expected_path = np.array([24.0, 1.5])
    inertial = _rotation(heading_true) @ expected_path
    path_velocity = _rotation(-heading_used) @ inertial
    body_heading = heading_true - np.deg2rad(4.0)
    body_velocity = _rotation(-body_heading) @ inertial
    wheel_velocity = _rotation(-steer) @ body_velocity
    reconstructed = _rotation(heading_used) @ path_velocity
    norm_residual = abs(np.linalg.norm(path_velocity) - np.linalg.norm(inertial))
    convention_error = np.linalg.norm(path_velocity - expected_path)
    slip_angle = np.rad2deg(np.arctan2(wheel_velocity[1], wheel_velocity[0]))

    steer_grid = np.linspace(-35.0, 35.0, 141)
    wheel_grid = np.array([
        _rotation(-np.deg2rad(value)) @ body_velocity for value in steer_grid
    ])
    heading_grid = np.linspace(-180.0, 180.0, 181)
    convention_grid = []
    for value in heading_grid:
        truth = np.deg2rad(value)
        velocity = _rotation(truth) @ expected_path
        used = value if broken else truth
        transformed = _rotation(-used) @ velocity
        convention_grid.append(np.linalg.norm(transformed - expected_path))

    signature = [
        path_velocity[0],
        path_velocity[1],
        slip_angle,
        norm_residual,
        convention_error,
    ]
    return {
        "signature": signature,
        "metrics": [
            ("path_vx", "Path longitudinal velocity", path_velocity[0], "m/s"),
            ("path_vy", "Path lateral velocity", path_velocity[1], "m/s"),
            ("wheel_alpha", "Wheel-frame slip angle", slip_angle, "deg"),
            ("frame_error", "Declared-frame convention error", convention_error, "m/s"),
        ],
        "plots": {
            "response": _plot("Wheel-frame velocity versus steer", "Wheel steer angle (deg)", "Velocity component (m/s)", [
                _trace("Wheel longitudinal", steer_grid, wheel_grid[:, 0], "Wheel steer angle", "deg", "Longitudinal velocity", "m/s"),
                _trace("Wheel lateral", steer_grid, wheel_grid[:, 1], "Wheel steer angle", "deg", "Lateral velocity", "m/s"),
            ]),
            "mechanism": _plot("Declared path-frame consistency", "Path heading (deg)", "Component error (m/s)", [
                _trace("Frame convention error", heading_grid, convention_grid, "Path heading", "deg", "Component error", "m/s"),
                _trace("Current round-trip error", [p["path_heading_deg"]], [np.linalg.norm(reconstructed-inertial)], "Path heading", "deg", "Round-trip error", "m/s", mode="markers"),
            ]),
        },
        "observation": "A proper rotation preserves norm; the expected path components independently expose an angle-unit defect that a repeated wrong inverse can hide.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
