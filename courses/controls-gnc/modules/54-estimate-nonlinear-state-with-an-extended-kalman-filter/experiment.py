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
    return _result(_model(parameters, broken), broken)
