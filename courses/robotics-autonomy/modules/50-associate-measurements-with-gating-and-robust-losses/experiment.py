from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 50
BROKEN_TEXT = (
    "Broken mode skips the Mahalanobis gate and minimizes an unbounded quadratic "
    "cost, allowing one incompatible return to dominate the update."
)
RECOVERY_TEXT = (
    "Restore covariance-normalized gating before applying the Huber loss; confirm "
    "that the inlier remains accepted while the incompatible return is rejected."
)


def _trace(
    name: str,
    x: Any,
    y: Any,
    x_quantity: str,
    x_unit: str,
    y_quantity: str,
    y_unit: str,
) -> dict[str, Any]:
    return {
        "type": "scattergl",
        "mode": "lines+markers",
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


def _huber_cost(norm: float, delta: float = 1.5) -> float:
    return 0.5 * norm**2 if norm <= delta else delta * (norm - 0.5 * delta)


def _model(parameters: dict[str, Any], broken: bool) -> dict[str, Any]:
    gate_sigma = float(parameters["gate_sigma"])
    outlier_sigma = float(parameters["outlier_sigma"])
    if broken:
        gate_sigma, outlier_sigma = 0.6, 11.0

    innovations = np.array([[0.60, -0.40], [outlier_sigma, 0.35 * outlier_sigma]])
    distances = np.einsum("ij,ij->i", innovations, innovations)
    gate_squared = gate_sigma**2
    accepted = np.ones(2, dtype=bool) if broken else distances <= gate_squared
    norms = np.sqrt(distances)
    if broken:
        costs = 0.5 * distances
    else:
        costs = np.array([_huber_cost(float(value)) for value in norms])
    association_cost = float(np.sum(costs[accepted]))

    residual_axis = np.linspace(0.0, 12.0, 181)
    influence = residual_axis if broken else np.minimum(residual_axis, 1.5)
    signature = [float(accepted[0]), float(not accepted[1]), association_cost]
    candidate_index = np.array([1.0, 2.0])

    return {
        "signature": signature,
        "sample_count": len(residual_axis),
        "metrics": [
            ("accepted_inlier", "Accepted Inlier", signature[0], "1"),
            ("rejected_outlier", "Rejected Outlier", signature[1], "1"),
            ("association_cost", "Accepted Robust Cost", signature[2], "1"),
        ],
        "plots": {
            "response": _plot(
                "Covariance-normalized association gate",
                "Candidate index (count)",
                "Squared Mahalanobis distance (1)",
                [
                    _trace(
                        "Candidate distance",
                        candidate_index,
                        distances,
                        "Candidate index",
                        "count",
                        "Squared Mahalanobis distance",
                        "1",
                    ),
                    _trace(
                        "Gate threshold",
                        candidate_index,
                        np.full(2, gate_squared),
                        "Candidate index",
                        "count",
                        "Squared Mahalanobis distance",
                        "1",
                    ),
                ],
            ),
            "mechanism": _plot(
                "Influence after association",
                "Whitened residual magnitude (sigma)",
                "Loss influence (1)",
                [
                    _trace(
                        "Applied influence",
                        residual_axis,
                        influence,
                        "Whitened residual magnitude",
                        "sigma",
                        "Loss influence",
                        "1",
                    ),
                    _trace(
                        "Huber bound",
                        residual_axis,
                        np.full_like(residual_axis, 1.5),
                        "Whitened residual magnitude",
                        "sigma",
                        "Loss influence",
                        "1",
                    ),
                ],
            ),
        },
        "observation": (
            "Gating decides whether a measurement is compatible with the predicted "
            "uncertainty; robust loss only limits the influence of measurements that survive."
        ),
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
            "sample_count": int(model["sample_count"]),
            "signature": [float(value) for value in model["signature"]],
            "software_only": True,
        },
    }


def _associate(gate_sigma, outlier_sigma, broken=False):
    """One-to-one assignment with explicit unmatched observations."""
    from scipy.optimize import linear_sum_assignment

    predicted = np.array([[0.0, 0.0], [1.0, 0.4]])
    measured = np.array(
        [[0.06, -0.04], [0.97, 0.42], [0.1 * outlier_sigma, 0.035 * outlier_sigma]]
    )
    residual = (measured[:, None, :] - predicted[None, :, :]) / np.array([0.1, 0.05])
    distance = np.linalg.norm(residual, axis=2)
    loss = np.where(distance <= 1.5, 0.5 * distance**2, 1.5 * (distance - 0.75))
    unmatched = _huber_cost(gate_sigma) + 1e-9
    costs = np.full((3, 5), unmatched)
    costs[:, :2] = np.where(distance <= gate_sigma, loss, 1e6)
    if broken:
        assignment = np.argmin(distance, axis=1)
    else:
        rows, cols = linear_sum_assignment(costs)
        assignment = np.full(3, -1, dtype=int)
        assignment[rows] = np.where(cols < 2, cols, -1)
    objective = sum(
        float(costs[i, j]) if j >= 0 else unmatched for i, j in enumerate(assignment)
    )
    return {
        "assignment": assignment,
        "distances": distance,
        "costs": costs,
        "objective": objective,
        "measurements": measured,
        "predicted": predicted,
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    result = _result(_model(parameters, broken), broken)
    assignment = _associate(
        float(parameters["gate_sigma"]), float(parameters["outlier_sigma"]), broken
    )
    result["diagnostics"]["association"] = assignment
    result["tables"] = {
        "associations": {
            "columns": [
                "Observation",
                "Assigned landmark",
                "Distance to landmark 1 (sigma)",
                "Distance to landmark 2 (sigma)",
            ],
            "rows": [
                {
                    "Observation": i + 1,
                    "Assigned landmark": int(j + 1) if j >= 0 else "unmatched",
                    "Distance to landmark 1 (sigma)": float(
                        assignment["distances"][i, 0]
                    ),
                    "Distance to landmark 2 (sigma)": float(
                        assignment["distances"][i, 1]
                    ),
                }
                for i, j in enumerate(assignment["assignment"])
            ],
        }
    }
    return result
