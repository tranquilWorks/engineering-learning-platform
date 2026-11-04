from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 58
BROKEN_TEXT = "Remove heading diversity while retaining measurement noise, so the actual calibration regressor loses rank."
RECOVERY_TEXT = "Restore a nonzero span and examine rank, singular values and covariance availability before trusting calibration."


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
    title: str, x_title: str, y_title: str, traces: list[dict[str, Any]]
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
                "value": float(value) if value is not None else None,
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
            **model.get("history", {}),
        },
    }


def _model(p, broken):
    span = 0.0 if broken else float(p["maneuver_span_deg"])
    noise = float(p["measurement_noise"])
    psi = np.deg2rad(np.linspace(-span / 2, span / 2, 41))
    regressor = np.column_stack([np.cos(psi), np.ones(41)])
    information = regressor.T @ regressor / noise**2
    eigenvalues = np.linalg.eigvalsh(information)
    rank = int(np.linalg.matrix_rank(regressor))
    determinant = float(np.linalg.det(information)) if rank == 2 else 0.0
    reciprocal = float(eigenvalues[0] / eigenvalues[-1]) if rank == 2 else 0.0
    covariance = np.linalg.inv(information) if rank == 2 else None
    std = float(np.sqrt(covariance[1, 1])) if covariance is not None else 0.0
    accumulated = np.array(
        [
            np.linalg.det(regressor[:j].T @ regressor[:j] / noise**2)
            if np.linalg.matrix_rank(regressor[:j]) == 2
            else 0.0
            for j in range(1, 42)
        ]
    )
    result = {
        "signature": [determinant, reciprocal, std],
        "metrics": [
            (
                "observability_determinant",
                "Actual information determinant",
                determinant,
                "1",
            ),
            (
                "information_condition",
                "Reciprocal information condition; zero=singular",
                reciprocal,
                "1",
            ),
            (
                "bias_standard_deviation",
                "Bias standard deviation; zero placeholder if unavailable",
                std,
                "1",
            ),
            ("information_rank", "Regressor rank", rank, "count"),
        ],
        "history": {
            "heading_rad": psi,
            "regressor": regressor,
            "information": information,
            "eigenvalues": eigenvalues,
            "rank": rank,
            "covariance": covariance,
            "bias_uncertainty_available": rank == 2,
        },
        "plots": {
            "response": _plot(
                "Calibration regressors",
                "Sample index (step)",
                "Regressor amplitude (1)",
                [
                    _trace(
                        "cos(heading)",
                        np.arange(41),
                        regressor[:, 0],
                        "Sample index",
                        "step",
                        "Heading sensitivity",
                        "1",
                    ),
                    _trace(
                        "Bias",
                        np.arange(41),
                        regressor[:, 1],
                        "Sample index",
                        "step",
                        "Bias",
                        "1",
                    ),
                ],
            ),
            "mechanism": _plot(
                "Calibration information",
                "Sample count (count)",
                "Information determinant (1)",
                [
                    _trace(
                        "Information determinant",
                        np.arange(1, 42),
                        accumulated,
                        "Sample count",
                        "count",
                        "Information determinant",
                        "1",
                    )
                ],
            ),
        },
        "observation": f"The actual 41-by-2 regressor has rank {rank}. Reciprocal condition is {reciprocal:.5g}; zero means singular. Bias uncertainty is {'available' if rank == 2 else 'UNAVAILABLE: the numerical zero is a placeholder, not perfect calibration'}. Reducing noise scales information but cannot create geometry. This is a normalized two-parameter calibration, not full inertial alignment.",
    }
    if rank < 2:
        result["metrics"][2] = (
            result["metrics"][2][0],
            "Bias uncertainty UNAVAILABLE (singular)",
            None,
            "1",
        )
    return result


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
