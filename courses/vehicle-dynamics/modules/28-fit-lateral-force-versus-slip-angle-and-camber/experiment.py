from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 28
DEFAULTS = {"cornering_stiffness_n_rad": 70000, "camber_stiffness_n_rad": 9000}
RANGES = {"cornering_stiffness_n_rad": (30000, 130000), "camber_stiffness_n_rad": (0, 20000)}
BROKEN_TEXT = "Broken mode builds the fit matrix in degrees but reports the result per radian."
RECOVERY_TEXT = "Convert both measured angles to radians before fitting and validate on held-out radian inputs."


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
    cornering = p["cornering_stiffness_n_rad"]
    camber = p["camber_stiffness_n_rad"]
    normal_load, friction = 3500.0, 1.2
    peak = normal_load * friction
    alpha_deg = np.array([-2.0, -1.0, 0.0, 1.0, 2.0, -1.5, 1.5, 0.5, -0.5])
    gamma_deg = np.array([-1.0, 1.0, -1.0, 1.0, 0.0, 0.5, -0.5, 1.5, -1.5])
    alpha = np.deg2rad(alpha_deg)
    gamma = np.deg2rad(gamma_deg)
    force = np.clip(-(cornering * alpha + camber * gamma), -peak, peak)
    fit_alpha = alpha_deg if broken else alpha
    fit_gamma = gamma_deg if broken else gamma
    design = np.column_stack((fit_alpha, fit_gamma))
    unsaturated = np.abs(force) < 0.90 * peak
    estimate, *_ = np.linalg.lstsq(design[unsaturated], -force[unsaturated], rcond=None)
    fitted_cornering, fitted_camber = (float(value) for value in estimate)

    validation_alpha = np.deg2rad(np.array([-3.0, -1.25, 0.75, 2.5]))
    validation_gamma = np.deg2rad(np.array([0.5, -1.5, 1.0, -0.5]))
    validation_force = np.clip(
        -(cornering * validation_alpha + camber * validation_gamma), -peak, peak
    )
    prediction = np.clip(
        -(fitted_cornering * validation_alpha + fitted_camber * validation_gamma),
        -peak,
        peak,
    )
    residual = prediction - validation_force
    rmse = float(np.sqrt(np.mean(residual**2)))
    utilization = float(np.max(np.abs(force)) / peak)
    error = float(
        np.linalg.norm(estimate - np.array([cornering, camber]))
        / max(np.linalg.norm([cornering, camber]), 1.0)
    )

    alpha_plot_deg = np.linspace(-6.0, 6.0, 161)
    alpha_plot = np.deg2rad(alpha_plot_deg)
    truth = np.clip(-(cornering * alpha_plot), -peak, peak)
    fit = np.clip(-(fitted_cornering * alpha_plot), -peak, peak)
    signature = [fitted_cornering, fitted_camber, rmse, utilization, error]
    return {
        "signature": signature,
        "metrics": [
            ("cornering", "Fitted cornering stiffness", fitted_cornering, "N/rad"),
            ("camber", "Fitted camber stiffness", fitted_camber, "N/rad"),
            ("rmse", "Held-out force RMSE", rmse, "N"),
            ("unit_error", "Angle-unit parameter error", error, "1"),
        ],
        "plots": {
            "response": _plot("Lateral force at zero camber", "Slip angle (deg)", "Lateral force (N)", [
                _trace("Synthetic truth", alpha_plot_deg, truth, "Slip angle", "deg", "Lateral force", "N"),
                _trace("Fitted law", alpha_plot_deg, fit, "Slip angle", "deg", "Lateral force", "N"),
            ]),
            "mechanism": _plot("Held-out lateral-force residual", "Validation slip angle (deg)", "Force residual (N)", [
                _trace("Prediction minus truth", np.rad2deg(validation_alpha), residual, "Validation slip angle", "deg", "Force residual", "N", mode="markers"),
            ]),
        },
        "observation": "Independent alpha and camber columns separate their stiffnesses only after both angles cross the same explicit radian boundary.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
