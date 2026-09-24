from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 58
DEFAULTS = {"training_fraction": 0.65, "observation_noise_n": 50.0}
RANGES = {"training_fraction": (0.50, 0.80), "observation_noise_n": (10.0, 120.0)}
BROKEN_TEXT = "Broken mode fits every timestamp and reports training error as validation error, leaking future samples into both the parameter estimate and its score."
RECOVERY_TEXT = "Split chronologically before fitting, estimate both stiffness parameters from the training rows only, and score the untouched future rows separately."


def _parameters(supplied: dict[str, Any]) -> dict[str, float]:
    result: dict[str, float] = {}
    for key, default in DEFAULTS.items():
        value = float(supplied.get(key, default))
        minimum, maximum = RANGES[key]
        if not np.isfinite(value) or value < minimum or value > maximum:
            raise ValueError(f"{key} outside declared finite range [{minimum}, {maximum}]")
        result[key] = value
    return result


def _trace(name: str, x: Any, y: Any, xq: str, xu: str, yq: str, yu: str) -> dict[str, Any]:
    return {"type": "scattergl", "mode": "lines+markers", "name": name, "x": np.asarray(x, dtype=float), "y": np.asarray(y, dtype=float), "meta": {"x_quantity": xq, "x_unit": xu, "y_quantity": yq, "y_unit": yu}}


def _plot(title: str, xt: str, yt: str, traces: list[dict[str, Any]]) -> dict[str, Any]:
    return {"data": traces, "layout": {"title": {"text": title, "x": 0.02}, "xaxis": {"title": {"text": xt}}, "yaxis": {"title": {"text": yt}}, "legend": {"orientation": "h"}, "margin": {"l": 72, "r": 36, "t": 62, "b": 62}, "hovermode": "closest", "uirevision": "keep-view"}, "config": {"responsive": True, "displaylogo": False}}


def _result(model: dict[str, Any], broken: bool) -> dict[str, Any]:
    return {"metrics": [{"id": key, "label": label, "value": float(value), "unit": unit, "emphasis": "primary" if index == 0 else "normal"} for index, (key, label, value, unit) in enumerate(model["metrics"])], "plots": model["plots"], "explanations": {"observation": model["observation"], "broken": BROKEN_TEXT, "recovery": RECOVERY_TEXT}, "diagnostics": {"item_number": ITEM_NUMBER, "broken_active": bool(broken), "signature": [float(value) for value in model["signature"]]}}


def _identify(fraction: float, noise: float, broken: bool) -> tuple[list[float], np.ndarray, np.ndarray, np.ndarray, int]:
    samples = 80
    index = np.arange(samples, dtype=float)
    front_slip = 0.032 * np.sin(0.19 * index) + 0.011 * np.cos(0.47 * index)
    rear_slip = 0.025 * np.cos(0.17 * index) - 0.009 * np.sin(0.41 * index)
    matrix = np.column_stack((front_slip, rear_slip))
    truth_parameters = np.array((80000.0, 70000.0))
    observed = matrix.dot(truth_parameters) + noise * (np.sin(1.73 * index) + 0.4 * np.cos(0.63 * index))
    train_count = round(samples * fraction)
    fit_matrix = matrix if broken else matrix[:train_count]
    fit_observed = observed if broken else observed[:train_count]
    estimate, _, _, _ = np.linalg.lstsq(fit_matrix, fit_observed, rcond=None)
    predicted = matrix.dot(estimate)
    train_rmse = float(np.sqrt(np.mean((predicted[:train_count] - observed[:train_count]) ** 2)))
    true_validation_rmse = float(np.sqrt(np.mean((predicted[train_count:] - observed[train_count:]) ** 2)))
    validation_rmse = train_rmse if broken else true_validation_rmse
    leakage = float(samples - train_count if broken else 0.0)
    signature = [float(estimate[0]), float(estimate[1]), train_rmse, validation_rmse, float(train_count), leakage]
    return signature, index, observed, predicted, train_count


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    signature, index, observed, predicted, train_count = _identify(p["training_fraction"], p["observation_noise_n"], broken)
    split = np.array((train_count - 0.5, train_count - 0.5))
    return {
        "signature": signature,
        "metrics": [("front_stiffness", "Estimated front stiffness", signature[0], "N/rad"), ("rear_stiffness", "Estimated rear stiffness", signature[1], "N/rad"), ("training_rmse", "Training RMSE", signature[2], "N"), ("validation_rmse", "Validation RMSE", signature[3], "N"), ("training_samples", "Training samples", signature[4], "sample"), ("leaked_samples", "Leaked future samples", signature[5], "sample")],
        "plots": {"response": _plot("Chronological identification split", "Sample index (1)", "Lateral force (N)", [_trace("Observed", index, observed, "Sample index", "1", "Lateral force", "N"), _trace("Predicted", index, predicted, "Sample index", "1", "Lateral force", "N")]), "mechanism": _plot("Train-validation boundary", "Sample index (1)", "Split indicator (1)", [_trace("Boundary", split, np.array((0.0, 1.0)), "Sample index", "1", "Split indicator", "1")])},
        "observation": "Parameter identification is credible only when the split precedes fitting and validation evaluates a later, untouched operating segment.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
