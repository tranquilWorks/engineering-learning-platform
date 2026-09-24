from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 57
DEFAULTS = {"observer_gain": 0.35, "measurement_noise": 0.08}
RANGES = {"observer_gain": (0.10, 0.80), "measurement_noise": (0.02, 0.20)}
BROKEN_TEXT = "Broken mode reverses the sideslip measurement sign, so a numerically stable observer converges toward the wrong physical state."
RECOVERY_TEXT = "Predict the coupled sideslip and yaw state on the sample grid, preserve the left-positive sign convention, and apply bounded innovation feedback with a propagated uncertainty ledger."


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
    return {"type": "scattergl", "mode": "lines", "name": name, "x": np.asarray(x, dtype=float), "y": np.asarray(y, dtype=float), "meta": {"x_quantity": xq, "x_unit": xu, "y_quantity": yq, "y_unit": yu}}


def _plot(title: str, xt: str, yt: str, traces: list[dict[str, Any]]) -> dict[str, Any]:
    return {"data": traces, "layout": {"title": {"text": title, "x": 0.02}, "xaxis": {"title": {"text": xt}}, "yaxis": {"title": {"text": yt}}, "legend": {"orientation": "h"}, "margin": {"l": 72, "r": 36, "t": 62, "b": 62}, "hovermode": "closest", "uirevision": "keep-view"}, "config": {"responsive": True, "displaylogo": False}}


def _result(model: dict[str, Any], broken: bool) -> dict[str, Any]:
    return {"metrics": [{"id": key, "label": label, "value": float(value), "unit": unit, "emphasis": "primary" if index == 0 else "normal"} for index, (key, label, value, unit) in enumerate(model["metrics"])], "plots": model["plots"], "explanations": {"observation": model["observation"], "broken": BROKEN_TEXT, "recovery": RECOVERY_TEXT}, "diagnostics": {"item_number": ITEM_NUMBER, "broken_active": bool(broken), "signature": [float(value) for value in model["signature"]]}}


def _estimate(gain: float, noise: float, broken: bool) -> tuple[list[float], np.ndarray, np.ndarray, np.ndarray]:
    step, samples = 0.02, 301
    time = np.arange(samples, dtype=float) * step
    matrix = np.array(((-1.10, -0.35, 0.20), (0.80, -1.60, 0.10), (0.0, 0.0, -0.25)))
    vector = np.array((0.70, 1.30, 0.12))
    steering = 0.045 * np.sin(0.85 * time) + 0.018 * np.sin(1.90 * time)
    truth = np.zeros((samples, 3), dtype=float)
    for index in range(1, samples):
        truth[index] = truth[index - 1] + step * (matrix.dot(truth[index - 1]) + vector * steering[index - 1])
    pattern = np.column_stack((np.sin(2.7 * time) + 0.35 * np.cos(5.1 * time), np.cos(2.2 * time) - 0.25 * np.sin(4.6 * time), 0.45 * np.sin(1.4 * time)))
    measured = truth + noise * pattern
    if broken:
        measured[:, 0] *= -1.0
    estimate = np.zeros_like(truth)
    covariance = np.eye(3) * 0.25
    innovations = np.zeros_like(truth)
    used_gain = np.diag((gain, 0.75 * gain, 0.45 * gain))
    process = np.diag((2.0e-5, 4.0e-5, 1.0e-5))
    for index in range(1, samples):
        predicted = estimate[index - 1] + step * (matrix.dot(estimate[index - 1]) + vector * steering[index - 1])
        innovations[index] = measured[index] - predicted
        estimate[index] = predicted + used_gain.dot(innovations[index])
        covariance = (np.eye(3) - used_gain).dot(covariance + process)
    error = estimate - truth
    signature = [float(np.rad2deg(estimate[-1, 0])), float(np.rad2deg(estimate[-1, 1])), float(np.rad2deg(estimate[-1, 2])), float(np.rad2deg(np.sqrt(np.mean(error[:, 0] ** 2)))), float(np.rad2deg(np.sqrt(np.mean(error[:, 1] ** 2)))), float(np.trace(covariance)), float(np.sqrt(np.mean(innovations**2)))]
    return signature, time, truth, estimate


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    signature, time, truth, estimate = _estimate(p["observer_gain"], p["measurement_noise"], broken)
    return {
        "signature": signature,
        "metrics": [("sideslip", "Final estimated sideslip", signature[0], "deg"), ("yaw_rate", "Final estimated yaw rate", signature[1], "deg/s"), ("steering_bias", "Estimated steering bias state", signature[2], "deg"), ("sideslip_rmse", "Sideslip RMSE", signature[3], "deg"), ("yaw_rmse", "Yaw-rate RMSE", signature[4], "deg/s"), ("covariance_trace", "Final covariance trace", signature[5], "rad^2"), ("innovation_rms", "Innovation RMS", signature[6], "rad")],
        "plots": {"response": _plot("Observed vehicle state", "Elapsed time (s)", "Sideslip angle (deg)", [_trace("Truth", time, np.rad2deg(truth[:, 0]), "Elapsed time", "s", "Sideslip angle", "deg"), _trace("Estimate", time, np.rad2deg(estimate[:, 0]), "Elapsed time", "s", "Sideslip angle", "deg")]), "mechanism": _plot("Yaw-state estimate", "Elapsed time (s)", "Yaw rate (deg/s)", [_trace("Truth", time, np.rad2deg(truth[:, 1]), "Elapsed time", "s", "Yaw rate", "deg/s"), _trace("Estimate", time, np.rad2deg(estimate[:, 1]), "Elapsed time", "s", "Yaw rate", "deg/s")])},
        "observation": "A stable estimator is not sufficient: measurement signs, state order, update timing, and uncertainty must match the physical state definition.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
