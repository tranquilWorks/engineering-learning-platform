from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 52
BROKEN_TEXT = "Subtract rather than add the selected process-noise variance, without changing either live parameter."
RECOVERY_TEXT = (
    "Restore the positive process-noise contribution and check the original q,T pair."
)


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
                "value": float(value) if value is not None else None,
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
    q = float(p["process_noise_density"])
    duration = float(p["propagation_interval_s"])
    time = np.linspace(0, duration, 241)
    variance = 1 + (-q if broken else q) * time
    end = float(variance[-1])
    formal = np.sqrt(np.maximum(variance, 0))
    return {
        "signature": [end, end, float(formal[-1])],
        "metrics": [
            ("propagated_variance", "Propagated scalar variance", end, "1"),
            ("minimum_covariance_eigenvalue", "Scalar covariance eigenvalue", end, "1"),
            (
                "standard_deviation",
                "Standard deviation; unavailable if P<0",
                float(formal[-1]) if end >= 0 else None,
                "1",
            ),
        ],
        "history": {
            "time": time,
            "variance": variance,
            "nominal_variance": 1 + q * time,
            "covariance_valid": bool(end >= 0),
        },
        "plots": {
            "response": _plot(
                "Covariance propagation",
                "Propagation time (s)",
                "Variance (1)",
                [
                    _trace(
                        "Applied rule",
                        time,
                        variance,
                        "Propagation time",
                        "s",
                        "Variance",
                        "1",
                    ),
                    _trace(
                        "Correct sign",
                        time,
                        1 + q * time,
                        "Propagation time",
                        "s",
                        "Variance",
                        "1",
                    ),
                ],
            ),
            "mechanism": _plot(
                "Covariance square root",
                "Propagation time (s)",
                "sqrt(max(P,0)) (1)",
                [
                    _trace(
                        "Formal root",
                        time,
                        formal,
                        "Propagation time",
                        "s",
                        "Formal square root",
                        "1",
                    ),
                    _trace(
                        "Nominal sigma",
                        time,
                        np.sqrt(1 + q * time),
                        "Propagation time",
                        "s",
                        "Standard deviation",
                        "1",
                    ),
                ],
            ),
        },
        "observation": f"P(T)=1 {'-' if broken else '+'} qT = {end:.6g}. The fault changes the noise sign at the SAME q,T. A negative covariance is invalid; clipping its square root to zero is only a plotting convention and never a valid certainty claim. This scalar zero-drift random walk does not implement a general vector process.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
