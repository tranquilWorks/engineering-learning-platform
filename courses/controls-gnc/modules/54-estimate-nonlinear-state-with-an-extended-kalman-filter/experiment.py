from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 54
BROKEN_TEXT = "Freeze the measurement Jacobian at zero while preserving prior state, prior uncertainty and the measurement."
RECOVERY_TEXT = "Restore H=2*xhat, then compare the same prior and measurement; discuss a nonlinear alternative at a truly zero prior."


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
            **model.get("history", {}),
        },
    }


def _model(p, broken):
    sigma = float(p["prior_standard_deviation"])
    prior = float(p["linearization_state"])
    variance = sigma * sigma
    measurement = 2.25
    H = 0.0 if broken else 2 * prior
    S = H * H * variance + 1.0
    gain = variance * H / S
    innovation = measurement - prior * prior
    posterior = prior + gain * innovation
    P = (1 - gain * H) ** 2 * variance + gain * gain
    residual = posterior**2 - (prior**2 + H * (posterior - prior))
    x = np.linspace(min(-0.5, prior - 2 * sigma), max(2.5, prior + 2 * sigma), 241)
    return {
        "signature": [H, P, abs(residual)],
        "metrics": [
            ("measurement_jacobian", "Applied measurement Jacobian", H, "1"),
            ("posterior_variance", "Joseph posterior variance", P, "1"),
            (
                "linearization_residual",
                "Actual post-update linearization residual",
                abs(residual),
                "1",
            ),
            ("posterior_state", "Updated state", posterior, "1"),
            ("innovation", "Measurement innovation", innovation, "1"),
        ],
        "history": {
            "prior_state": prior,
            "prior_variance": variance,
            "measurement": measurement,
            "H": H,
            "S": S,
            "K": gain,
            "posterior_state": posterior,
            "posterior_variance": P,
            "innovation": innovation,
            "signed_linearization_residual": residual,
        },
        "plots": {
            "response": _plot(
                "Measurement and tangent",
                "State (1)",
                "Measurement (1)",
                [
                    _trace(
                        "h(x)=x squared", x, x * x, "State", "1", "Measurement", "1"
                    ),
                    _trace(
                        "Applied local model",
                        x,
                        prior * prior + H * (x - prior),
                        "State",
                        "1",
                        "Measurement",
                        "1",
                    ),
                    _trace(
                        "Observed z",
                        x,
                        np.full_like(x, measurement),
                        "State",
                        "1",
                        "Measurement",
                        "1",
                    ),
                ],
            ),
            "mechanism": _plot(
                "Prior and posterior uncertainty",
                "Estimate stage (step)",
                "Variance (1)",
                [
                    _trace(
                        "Covariance",
                        [0, 1],
                        [variance, P],
                        "Estimate stage",
                        "step",
                        "Variance",
                        "1",
                        mode="lines+markers",
                    )
                ],
            ),
        },
        "observation": f"z=2.25, innovation={innovation:.5g}, K={gain:.5g}, x+={posterior:.5g}, P+={P:.5g}. The actual nonlinear residual is {residual:.5g}, not the prior variance. Fault mode freezes H=0 at unchanged prior/noise. This single scalar update cannot resolve the global +/- ambiguity of a squared measurement.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _append_recursive(
        _result(_model(parameters, broken), broken), parameters, "EKF"
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
