from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 50
BROKEN_TEXT = "Broken mode removes the training input while leaving the held-out excitation active. The second regressor column is zero, b is unidentifiable, and the least-squares minimum-norm result sets it to zero."
RECOVERY_TEXT = "Restore excitation and reset controls. Confirm rank two, a positive smallest singular value and a fitted model that predicts held-out dynamics using its own previous predictions."


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
        "type": "scatter",
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
            **model.get("details", {}),
            "broken_active": bool(broken),
            "signature": [float(value) for value in model["signature"]],
        },
    }


def identification_data(amplitude, spread, broken=False, noise=0.002):
    k = np.arange(500)
    t = 0.02 * k
    u = amplitude * (
        np.sin(2 * np.pi * 0.3 * t) + 0.5 * np.sin(2 * np.pi * (0.3 + spread) * t + 0.4)
    )
    # A chronological held-out experiment resets the state and shifts input phase.
    u[300:] = amplitude * (
        np.sin(2 * np.pi * 0.7 * t[300:] + 1)
        + 0.5 * np.sin(2 * np.pi * (0.7 + spread) * t[300:] + 0.8)
    )
    if broken:
        u[:300] = 0.0
    train = np.zeros(301)
    valid = np.zeros(201)
    for j in range(300):
        train[j + 1] = 0.82 * train[j] + 0.18 * u[j] + noise * np.cos(1.7 * j)
    for j in range(200):
        valid[j + 1] = (
            0.82 * valid[j] + 0.18 * u[j + 300] + noise * np.cos(1.7 * (j + 300))
        )
    return u, train, valid


def _model(p, broken):
    u, train, valid = identification_data(
        float(p["excitation_amplitude"]), float(p["frequency_spread_hz"]), broken
    )
    X = np.column_stack([train[:-1], u[:300]])
    theta, _, rank, singular = np.linalg.lstsq(X, train[1:], rcond=None)
    prediction = np.zeros(201)
    for j in range(200):
        prediction[j + 1] = theta[0] * prediction[j] + theta[1] * u[j + 300]
    parameter_error = np.linalg.norm(theta - [0.82, 0.18])
    rmse = np.sqrt(np.mean((prediction[1:] - valid[1:]) ** 2))
    training_fit = X @ theta
    return {
        "signature": [singular[-1], parameter_error, rmse],
        "metrics": [
            ("information", "Smallest regressor singular value", singular[-1], "1"),
            ("rank", "Training regressor rank", rank, "1"),
            ("parameter", "Measured parameter error norm", parameter_error, "1"),
            ("validation", "Held-out free-run RMSE", rmse, "1"),
            ("a", "Estimated pole coefficient", theta[0], "1"),
            ("b", "Estimated input coefficient", theta[1], "1"),
        ],
        "plots": {
            "response": _plot(
                "Separate held-out validation",
                "Validation time (s)",
                "Normalized output (1)",
                [
                    _trace(
                        "Held-out truth",
                        0.02 * np.arange(201),
                        valid,
                        "Validation time",
                        "s",
                        "Normalized output",
                        "1",
                    ),
                    _trace(
                        "Free-run fitted model",
                        0.02 * np.arange(201),
                        prediction,
                        "Validation time",
                        "s",
                        "Normalized output",
                        "1",
                    ),
                ],
            ),
            "mechanism": _plot(
                "Training data and fitted response",
                "Training time (s)",
                "Normalized signal (1)",
                [
                    _trace(
                        "Training input",
                        0.02 * np.arange(300),
                        u[:300],
                        "Training time",
                        "s",
                        "Normalized signal",
                        "1",
                    ),
                    _trace(
                        "Measured next output",
                        0.02 * np.arange(300),
                        train[1:],
                        "Training time",
                        "s",
                        "Normalized signal",
                        "1",
                    ),
                    _trace(
                        "One-step fit",
                        0.02 * np.arange(300),
                        training_fit,
                        "Training time",
                        "s",
                        "Normalized signal",
                        "1",
                    ),
                ],
            ),
        },
        "details": {
            "input": u,
            "training": train,
            "validation": valid,
            "prediction": prediction,
            "theta": theta,
            "rank": int(rank),
            "singular_values": singular,
            "training_indices": [0, 299],
            "validation_indices": [300, 499],
        },
        "observation": "Least squares fits two actual ARX coefficients. Validation recursively feeds back the predicted state on a separate experiment. The fault removes training excitation: the input coefficient is unidentifiable even when the training residual looks small. Parameter error is measured against synthetic truth, not a statistical confidence bound.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
