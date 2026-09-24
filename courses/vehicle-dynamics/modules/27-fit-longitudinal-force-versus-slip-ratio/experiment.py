from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 27
DEFAULTS = {"longitudinal_stiffness_n": 80000, "peak_friction": 1.15}
RANGES = {"longitudinal_stiffness_n": (30000, 140000), "peak_friction": (0.7, 1.5)}
BROKEN_TEXT = "Broken mode fits percent slip as if it were dimensionless, corrupting stiffness and held-out prediction."
RECOVERY_TEXT = "Use dimensionless slip ratio consistently and retain both low-slip and saturated identification samples."


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
    stiffness = p["longitudinal_stiffness_n"]
    friction = p["peak_friction"]
    normal_load = 3500.0
    peak = friction * normal_load
    train_slip = np.array([-0.16, -0.10, -0.05, -0.025, 0.025, 0.05, 0.10, 0.16])
    train_force = np.clip(stiffness * train_slip, -peak, peak)
    fit_slip = train_slip * (100.0 if broken else 1.0)
    low_mask = np.abs(train_force) < 0.90 * peak
    fitted_stiffness = float(
        np.dot(fit_slip[low_mask], train_force[low_mask])
        / np.dot(fit_slip[low_mask], fit_slip[low_mask])
    )
    fitted_mu = float(np.max(np.abs(train_force)) / normal_load)

    validation_slip = np.array([-0.13, -0.07, -0.035, 0.035, 0.07, 0.13])
    validation_force = np.clip(stiffness * validation_slip, -peak, peak)
    prediction = np.clip(
        fitted_stiffness * validation_slip,
        -fitted_mu * normal_load,
        fitted_mu * normal_load,
    )
    residual = prediction - validation_force
    rmse = float(np.sqrt(np.mean(residual**2)))
    relative_error = abs(fitted_stiffness - stiffness) / stiffness

    grid = np.linspace(-0.20, 0.20, 201)
    truth = np.clip(stiffness * grid, -peak, peak)
    fitted = np.clip(fitted_stiffness * grid, -fitted_mu * normal_load, fitted_mu * normal_load)
    signature = [fitted_stiffness, fitted_mu, rmse, peak, relative_error]
    return {
        "signature": signature,
        "metrics": [
            ("stiffness", "Fitted longitudinal stiffness", fitted_stiffness, "N"),
            ("friction", "Fitted peak friction", fitted_mu, "1"),
            ("rmse", "Held-out force RMSE", rmse, "N"),
            ("parameter_error", "Stiffness relative error", relative_error, "1"),
        ],
        "plots": {
            "response": _plot("Longitudinal force law", "Slip ratio (1)", "Longitudinal force (N)", [
                _trace("Synthetic truth", grid, truth, "Slip ratio", "1", "Longitudinal force", "N"),
                _trace("Fitted law", grid, fitted, "Slip ratio", "1", "Longitudinal force", "N"),
                _trace("Training samples", train_slip, train_force, "Slip ratio", "1", "Longitudinal force", "N", mode="markers"),
            ]),
            "mechanism": _plot("Held-out residual", "Validation slip ratio (1)", "Force residual (N)", [
                _trace("Prediction minus truth", validation_slip, residual, "Validation slip ratio", "1", "Force residual", "N"),
            ]),
        },
        "observation": "The low-slip slope identifies stiffness while saturated samples identify peak friction; held-out residual exposes a unit-confused fit.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
