from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 40
DEFAULTS = {"speed_m_s": 22.0, "road_wavelength_m": 8.0}
RANGES = {"speed_m_s": (5.0, 45.0), "road_wavelength_m": (2.0, 30.0)}
BROKEN_TEXT = "Broken mode feeds cycles per second directly into an equation that requires radians per second, displacing resonance and violating base-excitation equilibrium."
RECOVERY_TEXT = "Convert road spatial cycles to hertz with speed and wavelength, then multiply by two pi before evaluating the base-excitation transfer function."


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


def _transfer(speed: float, wavelength: float, broken: bool) -> tuple[complex, float, float]:
    mass, stiffness, damping = 360.0, 32000.0, 2800.0
    frequency_hz = speed / wavelength
    declared_omega = 2.0 * np.pi * frequency_hz
    used_omega = frequency_hz if broken else declared_omega
    numerator = stiffness + 1j * damping * used_omega
    denominator = stiffness - mass * used_omega**2 + 1j * damping * used_omega
    response = numerator / denominator
    physical_numerator = stiffness + 1j * damping * declared_omega
    physical_denominator = stiffness - mass * declared_omega**2 + 1j * damping * declared_omega
    residual = abs(physical_denominator * response - physical_numerator) / abs(physical_numerator)
    return response, declared_omega, float(residual)


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    speed, wavelength = p["speed_m_s"], p["road_wavelength_m"]
    response, omega, residual = _transfer(speed, wavelength, broken)
    road_amplitude = 0.010
    natural_frequency = np.sqrt(32000.0 / 360.0) / (2.0 * np.pi)
    signature = [
        float(abs(response)),
        float(np.angle(response, deg=True)),
        float(abs(response) * road_amplitude * omega**2),
        float(speed / wavelength / natural_frequency),
        residual,
    ]
    wavelengths = np.linspace(2.0, 30.0, 141)
    magnitudes = []
    accelerations = []
    for value in wavelengths:
        sample, sample_omega, _ = _transfer(speed, value, broken)
        magnitudes.append(abs(sample))
        accelerations.append(abs(sample) * road_amplitude * sample_omega**2)
    return {
        "signature": signature,
        "metrics": [
            ("transmissibility", "Body displacement transmissibility", signature[0], "1"),
            ("phase", "Body displacement phase", signature[1], "deg"),
            ("acceleration", "Body acceleration amplitude", signature[2], "m/s^2"),
            ("equation_residual", "Base-excitation residual", residual, "1"),
        ],
        "plots": {
            "response": _plot(
                "Road-wavelength ride response",
                "Road wavelength (m)",
                "Displacement transmissibility (1)",
                [
                    _trace("Transmissibility", wavelengths, magnitudes, "Road wavelength", "m", "Displacement transmissibility", "1"),
                ],
            ),
            "mechanism": _plot(
                "Sprung-mass acceleration",
                "Road wavelength (m)",
                "Acceleration amplitude (m/s^2)",
                [
                    _trace("Body acceleration", wavelengths, accelerations, "Road wavelength", "m", "Acceleration amplitude", "m/s^2"),
                ],
            ),
        },
        "observation": "Road wavelength becomes temporal frequency through vehicle speed; resonance moves if cycles and radians are confused.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
