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
                "Actual sigma-point transform",
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
                "Weighted variance contributions",
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
    return _result(_model(parameters, broken), broken)
