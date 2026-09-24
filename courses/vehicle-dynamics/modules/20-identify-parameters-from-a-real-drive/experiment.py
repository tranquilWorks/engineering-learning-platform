from __future__ import annotations

import math
from typing import Any

PRIMARY = "speed_span_m_s"
SECONDARY = "force_noise_n"
PRIMARY_RANGE = (2.0, 25.0)
SECONDARY_RANGE = (0.0, 100.0)
FIELDS = [
    "rolling_resistance_n",
    "drag_area_m2",
    "training_rmse_n",
    "validation_rmse_n",
    "speed_squared_span_m2_s2",
    "excitation_ratio",
    "drag_area_standard_error_m2",
    "invalid",
]

NOISE_PATTERN = [0.0, 0.7, -0.4, 0.2, -0.8, 0.5, -0.1, 0.9, -0.6, 0.3, -0.2, 0.4]


def _identify(speed_span: float, noise_force: float, broken: bool) -> tuple[list[float], list[float], list[float], list[float]]:
    density = 1.225
    true_rolling = 180.0
    true_drag_area = 0.64
    speeds = [10.0 + speed_span * index / 11.0 for index in range(12)]
    forces = [true_rolling + 0.5 * density * true_drag_area * speed * speed + noise_force * NOISE_PATTERN[index] for index, speed in enumerate(speeds)]
    training_indices = list(range(0, 12, 2))
    validation_indices = list(range(1, 12, 2))
    training_x = [225.0 if broken else speeds[index] ** 2 for index in training_indices]
    training_y = [forces[index] for index in training_indices]
    mean_x = sum(training_x) / len(training_x)
    mean_y = sum(training_y) / len(training_y)
    denominator = sum((value - mean_x) ** 2 for value in training_x)
    if denominator <= 1e-12:
        slope = 0.0
        intercept = mean_y
    else:
        slope = sum((x_value - mean_x) * (y_value - mean_y) for x_value, y_value in zip(training_x, training_y, strict=True)) / denominator
        intercept = mean_y - slope * mean_x
    fitted_drag_area = 2.0 * slope / density
    training_residuals = [y_value - (intercept + slope * x_value) for x_value, y_value in zip(training_x, training_y, strict=True)]
    validation_residuals = [forces[index] - (intercept + slope * speeds[index] ** 2) for index in validation_indices]
    training_rmse = math.sqrt(sum(value * value for value in training_residuals) / len(training_residuals))
    validation_rmse = math.sqrt(sum(value * value for value in validation_residuals) / len(validation_residuals))
    x_span = max(training_x) - min(training_x)
    excitation = denominator / max(1.0, sum(value * value for value in training_x))
    residual_variance = sum(value * value for value in training_residuals) / max(1, len(training_residuals) - 2)
    drag_area_error = 0.0 if denominator <= 1e-12 else 2.0 * math.sqrt(residual_variance / denominator) / density
    invalid = broken or denominator <= 1e-12
    signature = [intercept, fitted_drag_area, training_rmse, validation_rmse, x_span, excitation, drag_area_error, float(invalid)]
    fitted = [intercept + slope * speed * speed for speed in speeds]
    return signature, speeds, forces, fitted


def _plot(name: str, x: list[float], y: list[float], x_title: str, y_title: str) -> dict[str, Any]:
    return {
        "data": [{"type": "scatter", "mode": "lines+markers", "name": name, "x": x, "y": y}],
        "layout": {"title": {"text": "Identify Parameters from a Real Drive (Synthetic Offline Stand-In)"}, "xaxis": {"title": x_title}, "yaxis": {"title": y_title}, "uirevision": "keep-view"},
        "config": {"responsive": True, "displaylogo": False},
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    primary = float(parameters[PRIMARY])
    secondary = float(parameters[SECONDARY])
    broken = bool(parameters["broken_mode"])
    if not math.isfinite(primary) or not PRIMARY_RANGE[0] <= primary <= PRIMARY_RANGE[1]:
        raise ValueError(f"{PRIMARY} outside declared finite range")
    if not math.isfinite(secondary) or not SECONDARY_RANGE[0] <= secondary <= SECONDARY_RANGE[1]:
        raise ValueError(f"{SECONDARY} outside declared finite range")
    signature, speeds, forces, fitted = _identify(primary, secondary, broken)
    if len(signature) != len(FIELDS) or not all(math.isfinite(value) for value in signature):
        raise ValueError("identification model produced an invalid signature")
    primary_values = [2.0, 20.0, 25.0]
    secondary_values = [0.0, 20.0, 100.0]
    failed = _identify(primary, secondary, True)[0]
    recovered = _identify(20.0, 20.0, False)[0]
    response = _plot("synthetic coastdown force", [value * value for value in speeds], forces, "speed squared (m²/s²)", "resistive force (N)")
    response["data"].append({"type": "scatter", "mode": "lines", "name": "identified model", "x": [value * value for value in speeds], "y": fitted})
    return {
        "metrics": [
            {"id": "cda", "label": "Identified drag area", "value": signature[1], "unit": "m²", "emphasis": "primary"},
            {"id": "validation", "label": "Validation RMSE", "value": signature[3], "unit": "N"},
            {"id": "valid", "label": "Excitation valid", "value": not bool(signature[-1]), "unit": "boolean"},
        ],
        "plots": {
            "response": response,
            "primary_sweep": _plot(PRIMARY, primary_values, [_identify(value, secondary, False)[0][6] for value in primary_values], "speed span (m/s)", "CdA standard error (m²)"),
            "secondary_sweep": _plot(SECONDARY, secondary_values, [_identify(primary, value, False)[0][3] for value in secondary_values], "deterministic force noise (N)", "validation RMSE (N)"),
            "broken_recovery": {
                "data": [
                    {"type": "bar", "name": "under-excited", "x": FIELDS[:-1], "y": failed[:-1]},
                    {"type": "bar", "name": "recovered baseline", "x": FIELDS[:-1], "y": recovered[:-1]},
                ],
                "layout": {"barmode": "group", "xaxis": {"title": "fit diagnostic"}, "yaxis": {"title": "reported value"}},
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "A coastdown force that is affine in speed squared separates rolling resistance from aerodynamic drag when excitation is adequate.",
            "broken": "Broken mode collapses the training regressor to one speed-squared value, making the drag slope unidentifiable.",
            "recovery": "Restore the bounded 20 m/s speed span, alternate train and validation samples, and report residuals and slope uncertainty.",
        },
        "diagnostics": {"item_id": "P20", "signature": signature, "fields": FIELDS, "broken_active": broken, "bounded_points": len(speeds), "data_provenance": "deterministic synthetic offline stand-in; not a real drive"},
    }
