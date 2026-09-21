from __future__ import annotations

from typing import Any

import numpy as np


def _layout(title: str, x: str, y: str) -> dict[str, Any]:
    return {
        "title": {"text": title, "x": 0.02},
        "xaxis": {"title": x},
        "yaxis": {"title": y},
        "legend": {"orientation": "h"},
        "margin": {"l": 65, "r": 20, "t": 55, "b": 55},
        "hovermode": "closest",
        "uirevision": "keep-view",
    }


def _trace(name: str, x: Any, y: Any, mode: str = "lines+markers") -> dict[str, Any]:
    return {"type": "scatter", "mode": mode, "name": name, "x": x, "y": y}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    poses = round(float(parameters["pose_count"]))
    odometry_sigma = float(parameters["odometry_sigma_m"])
    range_sigma = float(parameters["range_sigma_m"])
    prior_weight = float(parameters["prior_weight"])
    broken = bool(parameters["broken_mode"])
    variables = poses + 1
    rows: list[np.ndarray] = []
    values: list[float] = []
    labels: list[str] = []
    if not broken:
        row = np.zeros(variables)
        row[0] = prior_weight
        rows.append(row)
        values.append(0.0)
        labels.append("prior")
    for index in range(1, poses):
        row = np.zeros(variables)
        row[index - 1] = -1.0 / odometry_sigma
        row[index] = 1.0 / odometry_sigma
        measurement = 1.0 + 0.5 * odometry_sigma * np.sin(1.3 * index)
        rows.append(row)
        values.append(measurement / odometry_sigma)
        labels.append("odometry")
    landmark_truth = float(poses + 2)
    for index in range(poses):
        row = np.zeros(variables)
        row[index] = -1.0 / range_sigma
        row[-1] = 1.0 / range_sigma
        measurement = (
            landmark_truth - index + 0.5 * range_sigma * np.cos(0.9 * (index + 1))
        )
        rows.append(row)
        values.append(measurement / range_sigma)
        labels.append("range")
    matrix = np.vstack(rows)
    observations = np.asarray(values)
    estimate, _, rank, singular = np.linalg.lstsq(matrix, observations, rcond=1e-12)
    residual = matrix @ estimate - observations
    truth = np.arange(poses, dtype=float)
    pose_error = estimate[:-1] - truth
    pose_rmse = np.sqrt(np.mean(pose_error**2))
    residual_rms = np.sqrt(np.mean(residual**2))
    signature = [
        estimate[-2],
        estimate[-1],
        pose_rmse,
        residual_rms,
        float(rank),
        singular[-1],
    ]
    return {
        "metrics": [
            {
                "id": "pose_rmse",
                "label": "Pose RMSE",
                "value": pose_rmse,
                "unit": "m",
                "emphasis": "primary",
            },
            {
                "id": "landmark_estimate",
                "label": "Landmark estimate",
                "value": estimate[-1],
                "unit": "m",
            },
            {
                "id": "weighted_residual_rms",
                "label": "Weighted residual RMS",
                "value": residual_rms,
                "unit": "sigma",
            },
            {
                "id": "matrix_rank",
                "label": "Factor-matrix rank",
                "value": int(rank),
                "unit": "rank",
            },
        ],
        "plots": {
            "response": {
                "data": [
                    _trace("True poses", np.arange(poses), truth),
                    _trace("Estimated poses", np.arange(poses), estimate[:-1]),
                    {
                        "type": "scatter",
                        "mode": "markers",
                        "name": "Estimated landmark",
                        "x": [poses],
                        "y": [estimate[-1]],
                    },
                ],
                "layout": _layout(
                    "One-dimensional SLAM state",
                    "State index (-)",
                    "World position (m)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "mechanism": {
                "data": [
                    _trace(
                        "Whitened factor residual",
                        np.arange(len(residual)),
                        residual,
                        "lines+markers",
                    )
                ],
                "layout": _layout(
                    "Factor residual sequence",
                    "Factor index (-)",
                    "Whitened residual (sigma)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "Odometry links neighboring poses and range factors link poses to a landmark; the prior chooses the otherwise arbitrary global translation.",
            "broken": "Removing the prior leaves a one-dimensional gauge nullspace. A minimum-norm solver still draws a plausible map with low relative residual, but its absolute frame is unobservable.",
            "recovery": "Anchor one pose or add an equivalent absolute constraint, then verify full rank in addition to checking residual magnitude.",
        },
        "diagnostics": {
            "item_id": "P16",
            "reference_basis": "independent weighted-normal-equation pseudoinverse solution",
            "broken_active": broken,
            "sample_count": len(residual),
            "factor_types": labels,
            "signature": [float(value) for value in signature],
        },
    }
