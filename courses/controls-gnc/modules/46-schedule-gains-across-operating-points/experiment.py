from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 46
BROKEN_TEXT = "Broken mode freezes K at its rho=0 value of 2/s. The table remains visible for comparison, but the used gain no longer adapts to the plant."
RECOVERY_TEXT = "Restore interpolation, reset spacing and compare knot values with exact gains. Inspect an off-knot value as a separate check."


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
    rho = float(p["operating_point"])
    spacing = float(p["grid_spacing"])
    knots = np.r_[np.arange(0.0, 1.0 - 1e-12, spacing), 1.0]
    values = 2 / (1 + 0.5 * knots**2)
    grid = np.unique(
        np.r_[np.linspace(0.0, 1.0, 201), knots, (knots[:-1] + knots[1:]) / 2]
    )
    exact = 2 / (1 + 0.5 * grid**2)
    gains = np.full_like(grid, 2.0) if broken else np.interp(grid, knots, values)
    selected = 2.0 if broken else np.interp(rho, knots, values)
    bandwidth = (1 + 0.5 * rho * rho) * selected
    error = max(abs(gains - exact))
    return {
        "signature": [bandwidth, abs(bandwidth - 2), error],
        "metrics": [
            ("bandwidth", "Selected closed-loop bandwidth", bandwidth, "1/s"),
            ("error", "Selected bandwidth error", abs(bandwidth - 2), "1/s"),
            ("interpolation", "Sampled maximum gain error", error, "1/s"),
        ],
        "plots": {
            "response": _plot(
                "Gain table and interpolation",
                "Operating point (1)",
                "Feedback gain (1/s)",
                [
                    _trace(
                        "Used schedule",
                        grid,
                        gains,
                        "Operating point",
                        "1",
                        "Feedback gain",
                        "1/s",
                    ),
                    _trace(
                        "Exact inverse-gain law",
                        grid,
                        exact,
                        "Operating point",
                        "1",
                        "Feedback gain",
                        "1/s",
                    ),
                    _trace(
                        "Table knots",
                        knots,
                        values,
                        "Operating point",
                        "1",
                        "Feedback gain",
                        "1/s",
                        mode="markers",
                    ),
                ],
            ),
            "mechanism": _plot(
                "Resulting closed-loop bandwidth",
                "Operating point (1)",
                "Bandwidth (1/s)",
                [
                    _trace(
                        "Scheduled bandwidth",
                        grid,
                        (1 + 0.5 * grid**2) * gains,
                        "Operating point",
                        "1",
                        "Bandwidth",
                        "1/s",
                    ),
                    _trace(
                        "Target bandwidth",
                        grid,
                        np.full_like(grid, 2.0),
                        "Operating point",
                        "1",
                        "Bandwidth",
                        "1/s",
                    ),
                ],
            ),
        },
        "details": {
            "knots": knots,
            "table": values,
            "grid": grid,
            "interpolated_gain": gains,
            "selected_gain": selected,
        },
        "observation": "Healthy interpolation is exact at table knots and generally imperfect between them. The maximum is measured on the displayed grid, not a claimed global analytic bound. Broken mode freezes gain at the rho=0 value.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
