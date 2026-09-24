from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 34
DEFAULTS = {"speed_m_s": 25.0, "front_cornering_n_rad": 70000.0}
RANGES = {"speed_m_s": (10.0, 50.0), "front_cornering_n_rad": (30000.0, 120000.0)}
BROKEN_TEXT = "Broken mode reverses the rear lateral-force sign inside the state model, invalidating physical force and yaw-moment balance."
RECOVERY_TEXT = "Restore the declared lateral-force signs and solve the beta/yaw-rate equilibrium from the physical state matrix."


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


def _state_model(speed: float, front: float, rear: float) -> tuple[np.ndarray, np.ndarray]:
    mass, inertia, a, b = 1450.0, 2400.0, 1.20, 1.50
    matrix = np.array(
        [
            [
                -(front + rear) / (mass * speed),
                (-a * front + b * rear) / (mass * speed**2) - 1.0,
            ],
            [
                (-a * front + b * rear) / inertia,
                -(a**2 * front + b**2 * rear) / (inertia * speed),
            ],
        ]
    )
    input_vector = np.array((front / (mass * speed), a * front / inertia))
    return matrix, input_vector


def _steady_signature(speed: float, front: float, broken: bool) -> list[float]:
    mass = 1450.0
    rear = -75000.0 if broken else 75000.0
    matrix, input_vector = _state_model(speed, front, rear)
    steer = np.deg2rad(2.0)
    state = np.linalg.solve(-matrix, input_vector * steer)
    beta, yaw_rate = state
    physical_rear = 75000.0
    force_front = front * (steer - beta - 1.20 * yaw_rate / speed)
    force_rear = physical_rear * (-beta + 1.50 * yaw_rate / speed)
    force_residual = mass * speed * yaw_rate - force_front - force_rear
    moment_residual = 1.20 * force_front - 1.50 * force_rear
    eigenvalues = np.linalg.eigvals(matrix)
    return [
        float(np.rad2deg(beta)),
        float(np.rad2deg(yaw_rate)),
        float(np.max(eigenvalues.real)),
        float(abs(force_residual)),
        float(abs(moment_residual)),
    ]


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    speed = p["speed_m_s"]
    front = p["front_cornering_n_rad"]
    signature = _steady_signature(speed, front, broken)
    steer_sweep = np.linspace(0.0, 5.0, 61)
    beta_values = []
    yaw_values = []
    rear = -75000.0 if broken else 75000.0
    matrix, input_vector = _state_model(speed, front, rear)
    for steer_deg in steer_sweep:
        state = np.linalg.solve(-matrix, input_vector * np.deg2rad(steer_deg))
        beta_values.append(np.rad2deg(state[0]))
        yaw_values.append(np.rad2deg(state[1]))
    eigenvalues = np.linalg.eigvals(matrix)
    return {
        "signature": signature,
        "metrics": [
            ("beta", "Steady sideslip", signature[0], "deg"),
            ("yaw_rate", "Steady yaw rate", signature[1], "deg/s"),
            ("pole", "Largest pole real part", signature[2], "1/s"),
            ("force_residual", "Force-balance residual", signature[3], "N"),
        ],
        "plots": {
            "response": _plot(
                "Steady bicycle response",
                "Road-wheel steer (deg)",
                "State response (deg or deg/s)",
                [
                    _trace("Sideslip", steer_sweep, beta_values, "Road-wheel steer", "deg", "Sideslip", "deg"),
                    _trace("Yaw rate", steer_sweep, yaw_values, "Road-wheel steer", "deg", "Yaw rate", "deg/s"),
                ],
            ),
            "mechanism": _plot(
                "State-matrix poles",
                "Pole real part (1/s)",
                "Pole imaginary part (rad/s)",
                [
                    _trace("Eigenvalues", eigenvalues.real, eigenvalues.imag, "Pole real part", "1/s", "Pole imaginary part", "rad/s", mode="markers"),
                ],
            ),
        },
        "observation": "A physically signed bicycle model closes lateral force and yaw moment while stable poles remain in the left half-plane.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
