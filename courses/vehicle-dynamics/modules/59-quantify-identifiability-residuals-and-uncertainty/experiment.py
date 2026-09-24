from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 59
DEFAULTS = {"excitation_level": 0.70, "noise_sigma_n": 80.0}
RANGES = {"excitation_level": (0.20, 1.00), "noise_sigma_n": (20.0, 150.0)}
BROKEN_TEXT = "Broken mode forms an unscaled normal-equation inverse and understates observation noise by a factor of ten, producing unjustifiably narrow intervals."
RECOVERY_TEXT = "Inspect singular values before interpreting parameters, fit with an SVD-based least-squares solve, retain residual correlation, and propagate the declared force-noise variance."


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


def _analyze(excitation: float, sigma: float, broken: bool) -> tuple[list[float], np.ndarray, np.ndarray, np.ndarray]:
    samples = 60
    index = np.arange(samples, dtype=float)
    first = excitation * (0.030 * np.sin(0.25 * index) + 0.008 * np.cos(0.53 * index))
    second = excitation * (0.028 * np.sin(0.25 * index + 0.16) + 0.004 * np.cos(0.91 * index))
    matrix = np.column_stack((first, second))
    truth = np.array((78000.0, 68000.0))
    observed = matrix.dot(truth) + sigma * (0.75 * np.sin(1.31 * index) + 0.35 * np.cos(0.29 * index))
    estimate, _, _, singular = np.linalg.lstsq(matrix, observed, rcond=None)
    residual = observed - matrix.dot(estimate)
    residual_rms = float(np.sqrt(np.mean(residual**2)))
    lag_correlation = float(np.corrcoef(residual[:-1], residual[1:])[0, 1])
    used_sigma = 0.10 * sigma if broken else sigma
    covariance = used_sigma**2 * (np.linalg.inv(matrix.T.dot(matrix)) if broken else np.linalg.pinv(matrix.T.dot(matrix)))
    standard = np.sqrt(np.diag(covariance))
    coverage = float(np.mean(np.abs(estimate - truth) <= 1.96 * standard))
    physical_covariance = sigma**2 * np.linalg.pinv(matrix.T.dot(matrix))
    covariance_residual = float(np.linalg.norm(covariance - physical_covariance))
    signature = [float(singular[0] / singular[-1]), float(singular[-1]), residual_rms, lag_correlation, float(np.mean(standard)), coverage, covariance_residual]
    return signature, singular, residual, standard


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    signature, singular, residual, standard = _analyze(p["excitation_level"], p["noise_sigma_n"], broken)
    return {
        "signature": signature,
        "metrics": [("condition", "Design condition number", signature[0], "1"), ("minimum_singular", "Minimum singular value", signature[1], "rad"), ("residual_rms", "Residual RMS", signature[2], "N"), ("lag_correlation", "Residual lag-one correlation", signature[3], "1"), ("standard_uncertainty", "Mean parameter standard uncertainty", signature[4], "N/rad"), ("coverage", "Nominal interval coverage", signature[5], "fraction"), ("covariance_residual", "Covariance ledger residual", signature[6], "(N/rad)^2")],
        "plots": {"response": _plot("Residual audit", "Sample index (1)", "Force residual (N)", [_trace("Residual", np.arange(residual.size), residual, "Sample index", "1", "Force residual", "N")]), "mechanism": _plot("Identifiability and uncertainty", "Parameter index (1)", "Scaled diagnostic (1)", [_trace("Singular value", np.arange(singular.size), singular / singular[0], "Parameter index", "1", "Scaled diagnostic", "1"), _trace("Standard uncertainty", np.arange(standard.size), standard / np.max(standard), "Parameter index", "1", "Scaled diagnostic", "1")])},
        "observation": "Small residuals do not guarantee identifiable parameters; excitation, singular values, residual structure, and covariance scale must be audited together.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
