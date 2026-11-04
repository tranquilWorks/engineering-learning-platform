from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 55
BROKEN_TEXT = "Broken mode omits the Gaussian covariance correction and reuses mean weights for covariance. Mean remains correct, but variance becomes (alpha²−1)*sigma⁴: zero at alpha=1 and negative for alpha<1."
RECOVERY_TEXT = "Restore the beta=2 covariance correction and reset both controls. Check both computed moments against analytic Gaussian values; do not reject a transform solely because its central mean weight is negative."


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


def _model(p, broken):
    sigma = float(p["state_standard_deviation"])
    alpha = float(p["sigma_spread"])
    points = np.array([0.0, alpha * sigma, -alpha * sigma])
    wm = np.array([1 - 1 / alpha**2, 1 / (2 * alpha**2), 1 / (2 * alpha**2)])
    wc = wm.copy()
    if not broken:
        wc[0] += 1 - alpha**2 + 2
    transformed = points**2
    mean = wm @ transformed
    contributions = wc * (transformed - mean) ** 2
    variance = sum(contributions)
    exact_mean = sigma * sigma
    exact_variance = 2 * sigma**4
    grid = np.linspace(-2 * sigma, 2 * sigma, 161)
    return {
        "signature": [abs(mean - exact_mean), abs(variance - exact_variance), min(wm)],
        "metrics": [
            ("mean_error", "Transformed mean error", abs(mean - exact_mean), "1"),
            (
                "variance_error",
                "Transformed variance error",
                abs(variance - exact_variance),
                "1",
            ),
            ("weight", "Minimum mean weight", min(wm), "1"),
            ("mean", "Computed transformed mean", mean, "1"),
            ("variance", "Computed transformed variance", variance, "1"),
            ("wc_sum", "Covariance weight sum", sum(wc), "1"),
        ],
        "plots": {
            "response": _plot(
                "Sigma-point transform",
                "Normalized state (1)",
                "Squared state (1)",
                [
                    _trace(
                        "Square transform",
                        grid,
                        grid**2,
                        "Normalized state",
                        "1",
                        "Squared state",
                        "1",
                    ),
                    _trace(
                        "Transformed sigma points",
                        points,
                        transformed,
                        "Normalized state",
                        "1",
                        "Squared state",
                        "1",
                        mode="markers",
                    ),
                ],
            ),
            "mechanism": _plot(
                "Variance contributions",
                "Sigma-point index (1)",
                "Variance contribution (1)",
                [
                    _trace(
                        "Covariance contributions",
                        np.arange(3),
                        contributions,
                        "Sigma-point index",
                        "1",
                        "Variance contribution",
                        "1",
                        mode="lines+markers",
                    )
                ],
            ),
        },
        "details": {
            "points": points,
            "mean_weights": wm,
            "covariance_weights": wc,
            "transformed": transformed,
            "mean": mean,
            "variance": variance,
            "variance_contributions": contributions,
        },
        "observation": "Mean weights sum to one; covariance weights generally do not. A negative central mean weight can be valid. The fault omits the Gaussian covariance correction. This experiment executes the unscented transform component, not a recursive UKF.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _append_recursive(
        _result(_model(parameters, broken), broken), parameters, "UKF"
    )


def _recursive_filter(sigma, initial, alpha, method, broken):
    """Bounded scalar nonlinear prediction/update; no retained-output lookup."""
    q, r = 0.0004, 0.01
    truth, estimate, covariance = 0.8, float(initial), float(sigma) ** 2
    rows = []
    for k in range(1, 81):
        forcing = 0.05 * np.cos(0.2 * k)
        truth = 0.94 * truth + 0.08 * np.sin(truth) + forcing + 0.015 * np.sin(0.7 * k)
        measurement = 0.4 * truth + 0.1 * truth**2 + 0.08 * np.cos(0.9 * k)
        if method == "EKF":
            transition = 0.94 + 0.08 * np.cos(estimate)
            prior = 0.94 * estimate + 0.08 * np.sin(estimate) + forcing
            prior_covariance = transition**2 * covariance + q
            jacobian = 0.0 if broken else 0.4 + 0.2 * prior
            predicted_measurement = 0.4 * prior + 0.1 * prior**2
            innovation_variance = jacobian**2 * prior_covariance + r
            cross_covariance = prior_covariance * jacobian
        else:
            wm = np.array([1 - 1 / alpha**2, 1 / (2 * alpha**2), 1 / (2 * alpha**2)])
            wc = wm.copy()
            wc[0] += 3 - alpha**2
            points = estimate + np.array([0, 1, -1]) * alpha * np.sqrt(covariance)
            propagated = 0.94 * points + 0.08 * np.sin(points) + forcing
            prior = float(wm @ propagated)
            prior_covariance = float(wc @ (propagated - prior) ** 2 + q)
            # Re-sigma-point after additive process noise: Q must reach the measurement.
            points = prior + np.array([0, 1, -1]) * alpha * np.sqrt(prior_covariance)
            observed = 0.4 * points + 0.1 * points**2
            predicted_measurement = float(wm @ observed)
            innovation_variance = float(
                wc @ (observed - predicted_measurement) ** 2 + r
            )
            cross_covariance = float(
                wc @ ((points - prior) * (observed - predicted_measurement))
            )
        innovation = measurement - predicted_measurement
        gain = (
            0.0
            if (method == "UKF" and broken)
            else cross_covariance / innovation_variance
        )
        estimate = prior + gain * innovation
        if method == "EKF":
            covariance = (1 - gain * jacobian) ** 2 * prior_covariance + gain**2 * r
        else:
            covariance = (
                prior_covariance
                - 2 * gain * cross_covariance
                + gain**2 * innovation_variance
            )
        if covariance <= 0 or not np.isfinite(covariance):
            raise ValueError("Recursive covariance lost positive definiteness")
        rows.append(
            [
                k,
                truth,
                measurement,
                prior,
                prior_covariance,
                predicted_measurement,
                innovation,
                innovation_variance,
                gain,
                estimate,
                covariance,
                innovation**2 / innovation_variance,
                (estimate - truth) ** 2 / covariance,
            ]
        )
    return np.asarray(rows)


def _append_recursive(result, parameters, method):
    sigma = float(
        parameters[
            "prior_standard_deviation"
            if method == "EKF"
            else "state_standard_deviation"
        ]
    )
    initial = float(parameters["linearization_state"]) if method == "EKF" else 1.0
    alpha = float(parameters["sigma_spread"]) if method == "UKF" else 0.7
    history = _recursive_filter(
        sigma, initial, alpha, method, bool(parameters["broken_mode"])
    )
    result["diagnostics"]["recursive_columns"] = [
        "step",
        "truth",
        "measurement",
        "prior_state",
        "prior_variance",
        "predicted_measurement",
        "innovation",
        "innovation_variance",
        "gain",
        "posterior_state",
        "posterior_variance",
        "nis",
        "nees",
    ]
    result["diagnostics"]["recursive_history"] = history
    result["diagnostics"]["recursive_method"] = method
    result["plots"]["recursive_state"] = _plot(
        "Recursive " + method,
        "Sample (step)",
        "State (1)",
        [
            _trace(
                "Truth", history[:, 0], history[:, 1], "Sample", "step", "State", "1"
            ),
            _trace(
                "Posterior",
                history[:, 0],
                history[:, 9],
                "Sample",
                "step",
                "State",
                "1",
            ),
        ],
    )
    result["plots"]["recursive_error"] = _plot(
        "Error and uncertainty",
        "Sample (step)",
        "State error (1)",
        [
            _trace(
                "Error",
                history[:, 0],
                history[:, 9] - history[:, 1],
                "Sample",
                "step",
                "State error",
                "1",
            ),
            _trace(
                "+2 sigma",
                history[:, 0],
                2 * np.sqrt(history[:, 10]),
                "Sample",
                "step",
                "State error",
                "1",
            ),
            _trace(
                "-2 sigma",
                history[:, 0],
                -2 * np.sqrt(history[:, 10]),
                "Sample",
                "step",
                "State error",
                "1",
            ),
        ],
    )
    result["metrics"].append(
        {
            "id": "recursive_rmse",
            "label": "Recursive state RMSE",
            "value": float(np.sqrt(np.mean((history[:, 9] - history[:, 1]) ** 2))),
            "unit": "1",
        }
    )
    result["explanations"]["observation"] += (
        " The additional 80-step sequence executes nonlinear prediction, process-noise propagation, measurement update and covariance feedback at every sample. Its deterministic disturbances illustrate NIS/NEES, not statistical coverage."
    )
    result["explanations"]["broken"] += " In the recursive sequence, the fault " + (
        "sets measurement sensitivity to zero."
        if method == "EKF"
        else "withholds every measurement correction while still predicting state and covariance."
    )
    selected = sorted({0, 1, 9, 19, 39, 59, 79})
    result.setdefault("tables", {})["integration_evidence"] = {
        "columns": [
            "Step",
            "Prior (1)",
            "Gain (1)",
            "Posterior (1)",
            "Variance (1)",
            "NIS (1)",
            "NEES (1)",
        ],
        "rows": [
            {
                "Step": int(history[k, 0]),
                "Prior (1)": float(history[k, 3]),
                "Gain (1)": float(history[k, 8]),
                "Posterior (1)": float(history[k, 9]),
                "Variance (1)": float(history[k, 10]),
                "NIS (1)": float(history[k, 11]),
                "NEES (1)": float(history[k, 12]),
            }
            for k in selected
        ],
    }
    return result
