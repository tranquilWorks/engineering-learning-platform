from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 33
DEFAULTS = {"observation_sigma_n": 80, "validation_fraction": 0.35}
RANGES = {"observation_sigma_n": (20, 250), "validation_fraction": (0.2, 0.6)}
BROKEN_TEXT = "Broken mode leaks validation rows into fitting and reports only one fifth of the declared uncertainty."
RECOVERY_TEXT = "Fit only training rows, retain the declared sigma, and recompute all held-out residual diagnostics."


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


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    sigma = p["observation_sigma_n"]
    validation_fraction = p["validation_fraction"]
    count = 40
    force_basis = np.linspace(500.0, 4200.0, count)
    pattern = (
        1.10 * np.sin(np.arange(count) * 1.7)
        + 0.45 * np.cos(np.arange(count) * 0.6)
    )
    observations = 0.92 * force_basis + sigma * pattern
    train_count = round(count * (1.0 - validation_fraction))
    train_count = min(max(train_count, 16), 32)
    fit_basis = force_basis if broken else force_basis[:train_count]
    fit_observations = observations if broken else observations[:train_count]
    fitted_scale = float(
        np.dot(fit_basis, fit_observations) / np.dot(fit_basis, fit_basis)
    )
    validation_basis = force_basis[train_count:]
    validation_observations = observations[train_count:]
    residual = validation_observations - fitted_scale * validation_basis
    assumed_sigma = 0.20 * sigma if broken else sigma
    normalized = residual / assumed_sigma
    bias = float(np.mean(residual))
    rmse = float(np.sqrt(np.mean(residual**2)))
    coverage = float(np.mean(np.abs(normalized) <= 1.96))
    maximum_normalized = float(np.max(np.abs(normalized)))
    signature = [fitted_scale, bias, rmse, coverage, maximum_normalized]
    indices = np.arange(train_count, count)
    return {
        "signature": signature,
        "metrics": [
            ("scale", "Fitted force scale", fitted_scale, "1"),
            ("bias", "Held-out residual bias", bias, "N"),
            ("rmse", "Held-out residual RMSE", rmse, "N"),
            ("coverage", "Prediction-interval coverage", coverage, "1"),
        ],
        "plots": {
            "response": _plot("Held-out force prediction", "Force basis (N)", "Observed force (N)", [
                _trace("Held-out observations", validation_basis, validation_observations, "Force basis", "N", "Observed force", "N", mode="markers"),
                _trace("Model prediction", validation_basis, fitted_scale * validation_basis, "Force basis", "N", "Predicted force", "N"),
            ]),
            "mechanism": _plot("Normalized validation residuals", "Validation row (1)", "Normalized residual (1)", [
                _trace("Normalized residual", indices, normalized, "Validation row", "1", "Normalized residual", "1", mode="markers"),
                _trace("Upper 95 percent bound", indices, np.full_like(indices, 1.96, dtype=float), "Validation row", "1", "Normalized residual", "1"),
                _trace("Lower 95 percent bound", indices, np.full_like(indices, -1.96, dtype=float), "Validation row", "1", "Normalized residual", "1"),
            ]),
        },
        "observation": "Held-out residuals need both a magnitude metric and a declared uncertainty scale; leakage or underreported sigma distorts coverage.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
