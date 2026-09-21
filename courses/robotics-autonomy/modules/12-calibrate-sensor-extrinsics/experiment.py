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


def _wrap(angle: float) -> float:
    return float((angle + np.pi) % (2.0 * np.pi) - np.pi)


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    truth_translation = np.array(
        [float(parameters["sensor_x_m"]), float(parameters["sensor_y_m"])]
    )
    truth_yaw = np.radians(float(parameters["sensor_yaw_deg"]))
    noise = float(parameters["noise_mm"]) / 1000.0
    count = round(float(parameters["correspondence_count"]))
    broken = bool(parameters["broken_mode"])
    phase = np.linspace(0.0, 2.0 * np.pi, count, endpoint=False)
    radii = 0.7 + 0.2 * np.sin(3.0 * phase)
    sensor = np.column_stack((radii * np.cos(phase), radii * np.sin(phase)))
    truth_rotation = np.array(
        [
            [np.cos(truth_yaw), -np.sin(truth_yaw)],
            [np.sin(truth_yaw), np.cos(truth_yaw)],
        ]
    )
    body = sensor @ truth_rotation.T + truth_translation
    body += noise * np.column_stack((np.sin(1.7 * phase), np.cos(2.3 * phase)))
    sensor_center = np.mean(sensor, axis=0)
    body_center = np.mean(body, axis=0)
    centered_sensor = sensor - sensor_center
    centered_body = body - body_center
    if broken:
        estimate_rotation = np.eye(2)
    else:
        covariance = centered_sensor.T @ centered_body
        left, _, right = np.linalg.svd(covariance)
        estimate_rotation = right.T @ left.T
        if np.linalg.det(estimate_rotation) < 0.0:
            right[-1, :] *= -1.0
            estimate_rotation = right.T @ left.T
    estimate_translation = body_center - estimate_rotation @ sensor_center
    fitted = sensor @ estimate_rotation.T + estimate_translation
    residual_vectors = fitted - body
    residual = np.linalg.norm(residual_vectors, axis=1)
    estimate_yaw = np.arctan2(estimate_rotation[1, 0], estimate_rotation[0, 0])
    translation_error = np.linalg.norm(estimate_translation - truth_translation)
    yaw_error = abs(_wrap(estimate_yaw - truth_yaw))
    signature = [
        estimate_translation[0],
        estimate_translation[1],
        np.degrees(estimate_yaw),
        np.sqrt(np.mean(residual**2)),
        translation_error,
        np.degrees(yaw_error),
    ]
    return {
        "metrics": [
            {
                "id": "estimated_x",
                "label": "Estimated x offset",
                "value": estimate_translation[0],
                "unit": "m",
                "emphasis": "primary",
            },
            {
                "id": "estimated_y",
                "label": "Estimated y offset",
                "value": estimate_translation[1],
                "unit": "m",
            },
            {
                "id": "estimated_yaw",
                "label": "Estimated yaw",
                "value": np.degrees(estimate_yaw),
                "unit": "deg",
            },
            {
                "id": "fit_rms",
                "label": "Fit residual RMS",
                "value": 1000.0 * np.sqrt(np.mean(residual**2)),
                "unit": "mm",
            },
        ],
        "plots": {
            "response": {
                "data": [
                    _trace("Body-frame references", body[:, 0], body[:, 1]),
                    _trace("Transformed sensor points", fitted[:, 0], fitted[:, 1]),
                ],
                "layout": _layout(
                    "Rigid correspondence alignment", "Body x (m)", "Body y (m)"
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "mechanism": {
                "data": [
                    _trace(
                        "Residual magnitude",
                        np.arange(count),
                        1000.0 * residual,
                        "lines+markers",
                    )
                ],
                "layout": _layout(
                    "Calibration residual by correspondence",
                    "Correspondence index (-)",
                    "Residual (mm)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "Centered point-cloud rotation determines yaw; the centroid difference then determines translation. Random correspondence noise sets the residual floor.",
            "broken": "Translation-only fitting cannot absorb a yaw offset, so residual direction changes across the point cloud even when the centroids align.",
            "recovery": "Estimate the proper rotation from cross-covariance, reject reflections, and solve translation only after rotation is fixed.",
        },
        "diagnostics": {
            "item_id": "P12",
            "reference_basis": "independent closed-form two-dimensional Procrustes angle and centroid solution",
            "broken_active": broken,
            "sample_count": count,
            "signature": [float(value) for value in signature],
        },
    }
