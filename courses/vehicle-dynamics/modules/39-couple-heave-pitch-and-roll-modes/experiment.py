from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 39
DEFAULTS = {"front_spring_rate_n_m": 42000.0, "rear_spring_rate_n_m": 38000.0}
RANGES = {"front_spring_rate_n_m": (25000.0, 65000.0), "rear_spring_rate_n_m": (25000.0, 65000.0)}
BROKEN_TEXT = "Broken mode deletes every off-diagonal stiffness term, erasing physical heave, pitch, and roll coupling from the corner layout."
RECOVERY_TEXT = "Retain the full corner-geometry stiffness matrix and verify each mass-normalized eigenpair against the physical matrix."


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


def _matrices(front_rate: float, rear_rate: float) -> tuple[np.ndarray, np.ndarray]:
    mass_matrix = np.diag((1450.0, 2600.0, 650.0))
    corners = (
        (1.20, 0.775, front_rate * 1.04),
        (1.20, -0.775, front_rate * 0.96),
        (-1.50, 0.765, rear_rate * 0.97),
        (-1.50, -0.765, rear_rate * 1.03),
    )
    stiffness = np.zeros((3, 3))
    for x_position, y_position, rate in corners:
        vector = np.array((1.0, x_position, y_position))
        stiffness += rate * np.outer(vector, vector)
    return mass_matrix, stiffness


def _solve_modes(mass_matrix: np.ndarray, stiffness: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    inverse_sqrt = np.diag(1.0 / np.sqrt(np.diag(mass_matrix)))
    symmetric = inverse_sqrt.dot(stiffness).dot(inverse_sqrt)
    values, normalized = np.linalg.eigh(symmetric)
    modes = inverse_sqrt.dot(normalized)
    return values, modes


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    mass_matrix, physical_stiffness = _matrices(
        p["front_spring_rate_n_m"], p["rear_spring_rate_n_m"]
    )
    used_stiffness = physical_stiffness.copy()
    if broken:
        used_stiffness = np.diag(np.diag(used_stiffness))
    values, modes = _solve_modes(mass_matrix, used_stiffness)
    frequencies = np.sqrt(values) / (2.0 * np.pi)
    residuals = []
    for index, value in enumerate(values):
        vector = modes[:, index]
        residuals.append(
            np.linalg.norm(physical_stiffness.dot(vector) - value * mass_matrix.dot(vector))
            / max(np.linalg.norm(physical_stiffness.dot(vector)), 1.0)
        )
    off_diagonal = physical_stiffness - np.diag(np.diag(physical_stiffness))
    coupling = np.linalg.norm(off_diagonal) / np.linalg.norm(np.diag(np.diag(physical_stiffness)))
    signature = [
        float(frequencies[0]),
        float(frequencies[1]),
        float(frequencies[2]),
        float(coupling),
        float(max(residuals)),
    ]
    labels = np.arange(1, 4)
    participation = np.abs(modes / np.max(np.abs(modes), axis=0))
    return {
        "signature": signature,
        "metrics": [
            ("mode_1", "First natural frequency", signature[0], "Hz"),
            ("mode_2", "Second natural frequency", signature[1], "Hz"),
            ("mode_3", "Third natural frequency", signature[2], "Hz"),
            ("eigen_residual", "Maximum eigen residual", signature[4], "1"),
        ],
        "plots": {
            "response": _plot(
                "Coupled chassis natural frequencies",
                "Mode index (1)",
                "Natural frequency (Hz)",
                [
                    _trace("Natural frequency", labels, frequencies, "Mode index", "1", "Natural frequency", "Hz", mode="markers"),
                ],
            ),
            "mechanism": _plot(
                "Mass-normalized modal participation",
                "Mode index (1)",
                "Normalized participation (1)",
                [
                    _trace("Heave", labels, participation[0], "Mode index", "1", "Normalized participation", "1", mode="markers"),
                    _trace("Pitch", labels, participation[1], "Mode index", "1", "Normalized participation", "1", mode="markers"),
                    _trace("Roll", labels, participation[2], "Mode index", "1", "Normalized participation", "1", mode="markers"),
                ],
            ),
        },
        "observation": "Asymmetric corner rates produce small but traceable off-diagonal coupling; deleting it changes both modal participation and the physical eigen residual.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
