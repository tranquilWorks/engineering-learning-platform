from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 53
BROKEN_TEXT = (
    "Broken mode publishes the causal filter as if it were a smoother and shrinks its "
    "reported covariance independently of the estimate, producing overconfident errors."
)
RECOVERY_TEXT = (
    "Restore the Rauch-Tung-Striebel backward pass, propagate its covariance with the "
    "same gain, and audit withheld absolute-position fixes that were not used in fitting."
)


def _trace(name: str, x: Any, y: Any, x_quantity: str, x_unit: str,
           y_quantity: str, y_unit: str) -> dict[str, Any]:
    return {
        "type": "scattergl", "mode": "lines", "name": name,
        "x": np.asarray(x, dtype=float), "y": np.asarray(y, dtype=float),
        "meta": {"x_quantity": x_quantity, "x_unit": x_unit,
                 "y_quantity": y_quantity, "y_unit": y_unit},
    }


def _plot(title: str, x_title: str, y_title: str,
          traces: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "data": traces,
        "layout": {
            "title": {"text": title, "x": 0.02},
            "xaxis": {"title": {"text": x_title}},
            "yaxis": {"title": {"text": y_title}},
            "legend": {"orientation": "h"},
            "margin": {"l": 72, "r": 36, "t": 62, "b": 62},
            "hovermode": "closest", "uirevision": "keep-view",
        },
        "config": {"responsive": True, "displaylogo": False},
    }


def _simulate(process_noise: float, measurement_noise: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    count = 81
    dt = 0.1
    time_s = np.arange(count, dtype=float) * dt
    truth = np.zeros((count, 2), dtype=float)
    truth[0] = np.array([0.0, 0.8])
    for index in range(count - 1):
        acceleration = 0.05 * np.sin(0.55 * time_s[index])
        truth[index + 1, 0] = truth[index, 0] + dt * truth[index, 1] + 0.5 * dt**2 * acceleration
        truth[index + 1, 1] = truth[index, 1] + dt * acceleration
    deterministic_noise = measurement_noise * (
        0.72 * np.sin(1.91 * np.arange(count)) + 0.28 * np.cos(0.73 * np.arange(count))
    )
    measurements = truth[:, 0] + deterministic_noise
    return time_s, truth, measurements


def _filter_and_smooth(
    process_noise: float, measurement_noise: float, broken: bool
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    time_s, truth, measurements = _simulate(process_noise, measurement_noise)
    count = len(time_s)
    dt = time_s[1] - time_s[0]
    transition = np.array([[1.0, dt], [0.0, 1.0]])
    noise_gain = np.array([[0.5 * dt**2], [dt]])
    process_covariance = process_noise**2 * (noise_gain @ noise_gain.T) + 1.0e-10 * np.eye(2)
    measurement_matrix = np.array([[1.0, 0.0]])
    measurement_variance = max(measurement_noise, 1.0e-4) ** 2

    filtered = np.zeros((count, 2), dtype=float)
    predicted = np.zeros((count, 2), dtype=float)
    filtered_covariance = np.zeros((count, 2, 2), dtype=float)
    predicted_covariance = np.zeros((count, 2, 2), dtype=float)
    filtered[0] = np.array([measurements[0], 0.5])
    filtered_covariance[0] = np.diag([measurement_variance, 0.5])
    heldout = np.zeros(count, dtype=bool)
    heldout[::5] = True

    for index in range(1, count):
        predicted[index] = transition @ filtered[index - 1]
        predicted_covariance[index] = (
            transition @ filtered_covariance[index - 1] @ transition.T + process_covariance
        )
        if heldout[index]:
            filtered[index] = predicted[index]
            filtered_covariance[index] = predicted_covariance[index]
            continue
        innovation = measurements[index] - (measurement_matrix @ predicted[index]).item()
        innovation_variance = (
            measurement_matrix @ predicted_covariance[index] @ measurement_matrix.T
            + measurement_variance
        ).item()
        gain = predicted_covariance[index] @ measurement_matrix.T / innovation_variance
        filtered[index] = predicted[index] + gain[:, 0] * innovation
        filtered_covariance[index] = (
            np.eye(2) - gain @ measurement_matrix
        ) @ predicted_covariance[index]

    smoothed = filtered.copy()
    smoothed_covariance = filtered_covariance.copy()
    if not broken:
        for index in range(count - 2, -1, -1):
            smoothing_gain = (
                filtered_covariance[index]
                @ transition.T
                @ np.linalg.inv(predicted_covariance[index + 1])
            )
            smoothed[index] = filtered[index] + smoothing_gain @ (
                smoothed[index + 1] - predicted[index + 1]
            )
            smoothed_covariance[index] = filtered_covariance[index] + smoothing_gain @ (
                smoothed_covariance[index + 1] - predicted_covariance[index + 1]
            ) @ smoothing_gain.T
    else:
        smoothed_covariance *= 0.12

    return time_s, truth, measurements, smoothed, smoothed_covariance, heldout


def _model(parameters: dict[str, Any], broken: bool) -> dict[str, Any]:
    process_noise = float(parameters["process_noise"])
    measurement_noise = float(parameters["measurement_noise"])
    time_s, truth, measurements, estimate, covariance, heldout = _filter_and_smooth(
        process_noise, measurement_noise, broken
    )
    position_error = estimate[:, 0] - truth[:, 0]
    position_variance = np.maximum(covariance[:, 0, 0], 1.0e-12)
    normalized_squared_error = position_error**2 / position_variance
    smoothed_rmse = float(np.sqrt(np.mean(position_error**2)))
    consistency_ratio = float(np.mean(normalized_squared_error <= 3.841458820694124))
    heldout_map_error = float(
        np.sqrt(np.mean((estimate[heldout, 0] - measurements[heldout]) ** 2))
    )
    signature = [smoothed_rmse, consistency_ratio, heldout_map_error]

    return {
        "signature": signature,
        "sample_count": len(time_s),
        "metrics": [
            ("smoothed_rmse", "Smoothed Position RMSE", signature[0], "m"),
            ("consistency_ratio", "Two-Sigma Consistency Coverage", signature[1], "1"),
            ("heldout_map_error", "Held-Out Position-Fix RMSE", signature[2], "m"),
        ],
        "plots": {
            "response": _plot(
                "Filtered/smoothed trajectory against truth",
                "Elapsed time (s)",
                "Position (m)",
                [
                    _trace("Ground truth", time_s, truth[:, 0], "Elapsed time", "s", "Position", "m"),
                    _trace("Estimated trajectory", time_s, estimate[:, 0], "Elapsed time", "s", "Position", "m"),
                ],
            ),
            "mechanism": _plot(
                "Covariance consistency audit",
                "Elapsed time (s)",
                "Normalized squared error (1)",
                [
                    _trace("Position NEES", time_s, normalized_squared_error, "Elapsed time", "s", "Normalized squared error", "1"),
                    _trace("95% one-state bound", time_s, np.full_like(time_s, 3.841458820694124), "Elapsed time", "s", "Normalized squared error", "1"),
                ],
            ),
        },
        "observation": (
            "A backward smoother may improve past states with future information, but its "
            "covariance must follow the same recursion and must survive withheld-data checks."
        ),
    }


def _result(model: dict[str, Any], broken: bool) -> dict[str, Any]:
    return {
        "metrics": [
            {"id": key, "label": label, "value": float(value), "unit": unit,
             "emphasis": "primary" if index == 0 else "normal"}
            for index, (key, label, value, unit) in enumerate(model["metrics"])
        ],
        "plots": model["plots"],
        "explanations": {"observation": model["observation"], "broken": BROKEN_TEXT,
                         "recovery": RECOVERY_TEXT},
        "diagnostics": {
            "item_number": ITEM_NUMBER, "broken_active": bool(broken),
            "sample_count": int(model["sample_count"]),
            "signature": [float(value) for value in model["signature"]],
            "software_only": True,
        },
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
