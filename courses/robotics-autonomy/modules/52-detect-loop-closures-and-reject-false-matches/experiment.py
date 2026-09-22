from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 52
BROKEN_TEXT = (
    "Broken mode inserts the highest-scoring appearance match without geometric "
    "verification and gives its contradictory residual full quadratic influence."
)
RECOVERY_TEXT = (
    "Require both the appearance threshold and geometric residual gate, then bound "
    "the influence of any accepted closure with a robust factor."
)


def _trace(name: str, x: Any, y: Any, x_quantity: str, x_unit: str,
           y_quantity: str, y_unit: str) -> dict[str, Any]:
    return {
        "type": "scattergl", "mode": "lines+markers", "name": name,
        "x": np.asarray(x, dtype=float), "y": np.asarray(y, dtype=float),
        "meta": {"x_quantity": x_quantity, "x_unit": x_unit,
                 "y_quantity": y_quantity, "y_unit": y_unit},
    }


def _plot(title: str, x_title: str, y_title: str,
          traces: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "data": traces,
        "layout": {
            "title": {"text": title, "x": 0.02},
            "xaxis": {"title": {"text": x_title}},
            "yaxis": {"title": {"text": y_title}},
            "legend": {"orientation": "h"},
            "margin": {"l": 72, "r": 36, "t": 62, "b": 62},
            "hovermode": "closest", "uirevision": "keep-view",
        },
        "config": {"responsive": True, "displaylogo": False},
    }


def _huber_cost(normalized_residual: float, delta: float = 1.0) -> float:
    magnitude = abs(normalized_residual)
    return 0.5 * magnitude**2 if magnitude <= delta else delta * (magnitude - 0.5 * delta)


def _model(parameters: dict[str, Any], broken: bool) -> dict[str, Any]:
    score = float(parameters["descriptor_score"])
    residual_m = float(parameters["geometric_residual_m"])
    if broken:
        score, residual_m = 0.95, 1.8

    appearance_pass = score >= 0.70
    geometry_pass = residual_m <= 0.30
    inserted = appearance_pass and (geometry_pass or broken)
    normalized = residual_m / 0.30
    geometric_weight = 1.0 if broken else min(1.0, 1.0 / max(abs(normalized), 1.0))
    closure_weight = score * geometric_weight if inserted else 0.0
    robust_cost = 0.5 * normalized**2 if broken else _huber_cost(normalized)
    map_deformation = closure_weight * residual_m * (2.0 if broken else 0.20)
    signature = [closure_weight, robust_cost, map_deformation]

    candidate_index = np.arange(1.0, 5.0)
    candidate_scores = np.array([0.32, 0.56, score, 0.44])
    residual_axis = np.linspace(0.0, 2.0, 181)
    normalized_axis = residual_axis / 0.30
    influence_weight = (
        np.ones_like(residual_axis)
        if broken
        else np.minimum(1.0, 1.0 / np.maximum(normalized_axis, 1.0))
    )

    return {
        "signature": signature,
        "sample_count": len(residual_axis),
        "metrics": [
            ("closure_weight", "Inserted Closure Weight", signature[0], "1"),
            ("robust_cost", "Normalized Robust Cost", signature[1], "1"),
            ("map_deformation", "Induced Map Deformation", signature[2], "m"),
        ],
        "plots": {
            "response": _plot(
                "Appearance candidates are hypotheses, not constraints",
                "Loop-candidate index (count)",
                "Descriptor similarity (1)",
                [
                    _trace("Candidate score", candidate_index, candidate_scores, "Loop-candidate index", "count", "Descriptor similarity", "1"),
                    _trace("Appearance threshold", candidate_index, np.full(4, 0.70), "Loop-candidate index", "count", "Descriptor similarity", "1"),
                ],
            ),
            "mechanism": _plot(
                "Geometric factor influence",
                "Closure residual (m)",
                "Robust influence weight (1)",
                [
                    _trace("Applied factor weight", residual_axis, influence_weight, "Closure residual", "m", "Robust influence weight", "1"),
                    _trace("Geometric gate", residual_axis, (residual_axis <= 0.30).astype(float), "Closure residual", "m", "Robust influence weight", "1"),
                ],
            ),
        },
        "observation": (
            "Appearance proposes a revisit; independent geometry decides whether it may "
            "enter the graph, and robust weighting limits the damage of residual mismatch."
        ),
    }


def _result(model: dict[str, Any], broken: bool) -> dict[str, Any]:
    return {
        "metrics": [
            {"id": key, "label": label, "value": float(value), "unit": unit,
             "emphasis": "primary" if index == 0 else "normal"}
            for index, (key, label, value, unit) in enumerate(model["metrics"])
        ],
        "plots": model["plots"],
        "explanations": {"observation": model["observation"], "broken": BROKEN_TEXT,
                         "recovery": RECOVERY_TEXT},
        "diagnostics": {
            "item_number": ITEM_NUMBER, "broken_active": bool(broken),
            "sample_count": int(model["sample_count"]),
            "signature": [float(value) for value in model["signature"]],
            "software_only": True,
        },
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
