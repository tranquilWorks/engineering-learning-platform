from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 35
DEFAULTS = {"speed_m_s": 25.0, "frequency_hz": 1.0}
RANGES = {"speed_m_s": (10.0, 50.0), "frequency_hz": (0.1, 4.0)}
BROKEN_TEXT = "Broken mode inserts hertz directly where angular frequency is required, so the reported response fails the complex state equation at the declared frequency."
RECOVERY_TEXT = "Convert hertz to radians per second before solving the complex state equation and recompute magnitude, phase, and residual."


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


def _matrices(speed: float) -> tuple[np.ndarray, np.ndarray]:
    mass, inertia = 1450.0, 2400.0
    a, b, front, rear = 1.20, 1.50, 70000.0, 75000.0
    matrix = np.array(
        [
            [-(front + rear) / (mass * speed), (-a * front + b * rear) / (mass * speed**2) - 1.0],
            [(-a * front + b * rear) / inertia, -(a**2 * front + b**2 * rear) / (inertia * speed)],
        ]
    )
    return matrix, np.array((front / (mass * speed), a * front / inertia))


def _response(speed: float, frequency_hz: float, broken: bool) -> tuple[np.ndarray, float]:
    matrix, input_vector = _matrices(speed)
    declared_omega = 2.0 * np.pi * frequency_hz
    used_omega = frequency_hz if broken else declared_omega
    state = np.linalg.solve(1j * used_omega * np.eye(2) - matrix, input_vector)
    residual = np.linalg.norm(
        (1j * declared_omega * np.eye(2) - matrix).dot(state) - input_vector
    )
    return state, float(residual)


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    speed, frequency = p["speed_m_s"], p["frequency_hz"]
    state, residual = _response(speed, frequency, broken)
    matrix, input_vector = _matrices(speed)
    dc = np.linalg.solve(-matrix, input_vector)
    signature = [
        float(abs(state[1])),
        float(abs(state[0])),
        float(np.angle(state[1], deg=True)),
        float(dc[1]),
        residual,
    ]
    frequencies = np.linspace(0.0, 4.0, 161)
    yaw_gain = []
    beta_gain = []
    yaw_phase = []
    for value in frequencies:
        sample, _ = _response(speed, max(value, 1.0e-9), broken)
        yaw_gain.append(abs(sample[1]))
        beta_gain.append(abs(sample[0]))
        yaw_phase.append(np.angle(sample[1], deg=True))
    return {
        "signature": signature,
        "metrics": [
            ("yaw_gain", "Yaw-rate gain", signature[0], "1/s"),
            ("beta_gain", "Sideslip gain", signature[1], "1"),
            ("yaw_phase", "Yaw phase", signature[2], "deg"),
            ("equation_residual", "Complex-equation residual", signature[4], "1/s"),
        ],
        "plots": {
            "response": _plot(
                "Steering frequency-response magnitude",
                "Excitation frequency (Hz)",
                "Response gain (1 or 1/s)",
                [
                    _trace("Yaw-rate gain", frequencies, yaw_gain, "Excitation frequency", "Hz", "Yaw-rate gain", "1/s"),
                    _trace("Sideslip gain", frequencies, beta_gain, "Excitation frequency", "Hz", "Sideslip gain", "1"),
                ],
            ),
            "mechanism": _plot(
                "Yaw-rate phase response",
                "Excitation frequency (Hz)",
                "Yaw-rate phase (deg)",
                [
                    _trace("Yaw-rate phase", frequencies, yaw_phase, "Excitation frequency", "Hz", "Yaw-rate phase", "deg"),
                ],
            ),
        },
        "observation": "Magnitude and phase are meaningful only when the declared hertz value is converted to angular frequency in the dynamic state equation.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
