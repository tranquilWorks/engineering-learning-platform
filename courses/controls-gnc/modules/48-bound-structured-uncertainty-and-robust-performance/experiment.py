from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 48
BROKEN_TEXT = "Broken mode reverses the feedback sign, replacing a+K by a−K. At default settings the entire family is unstable even though finite-frequency magnitude values can still be computed."
RECOVERY_TEXT = "Restore negative feedback and reset both controls. Verify the minimum decay margin is positive before interpreting sensitivity as a stable closed-loop disturbance response."


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
    radius = float(p["uncertainty_radius"])
    K = float(p["feedback_gain"]) * (-1 if broken else 1)
    delta = np.linspace(-radius, radius, 81)
    a = 1 + delta
    margin = a + K
    w = np.geomspace(0.05, 100.0, 160)
    magnitude = np.sqrt(
        (a[:, None] ** 2 + w[None, :] ** 2) / (margin[:, None] ** 2 + w[None, :] ** 2)
    )
    envelope = magnitude.max(axis=0)
    peak = magnitude.max()
    model = {
        "signature": [min(margin), peak, 2 * radius],
        "metrics": [
            ("margin", "Worst stability margin", min(margin), "1/s"),
            ("sensitivity", "Sampled finite-band sensitivity peak", peak, "1"),
            ("width", "Uncertain pole-rate width", 2 * radius, "1/s"),
        ],
        "plots": {
            "response": _plot(
                "Declared uncertainty family",
                "Pole-rate perturbation (1/s)",
                "Stability margin (1/s)",
                [
                    _trace(
                        "Decay rate",
                        delta,
                        margin,
                        "Pole-rate perturbation",
                        "1/s",
                        "Stability margin",
                        "1/s",
                    ),
                    _trace(
                        "Stability boundary",
                        delta,
                        np.zeros_like(delta),
                        "Pole-rate perturbation",
                        "1/s",
                        "Stability margin",
                        "1/s",
                    ),
                ],
            ),
            "mechanism": _plot(
                "True sensitivity magnitude",
                "Angular frequency (rad/s)",
                "Sensitivity magnitude (1)",
                [
                    _trace(
                        "Sampled family envelope",
                        w,
                        envelope,
                        "Angular frequency",
                        "rad/s",
                        "Sensitivity magnitude",
                        "1",
                    ),
                    _trace(
                        "Unit sensitivity",
                        w,
                        np.ones_like(w),
                        "Angular frequency",
                        "rad/s",
                        "Sensitivity magnitude",
                        "1",
                    ),
                ],
            ),
        },
        "details": {
            "uncertainty": delta,
            "frequency": w,
            "sensitivity": magnitude,
            "stability_margin": margin,
            "family_stable": bool(min(margin) > 0),
        },
        "observation": "S(s)=(s+a)/(s+a+K) is dimensionless. The plotted peak covers sampled frequencies 0.05 to 100 rad/s and sampled uncertainty values. It is not an H-infinity stability certificate; check every family pole separately.",
    }

    model["plots"]["mechanism"]["layout"]["xaxis"]["type"] = "log"
    return model


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
