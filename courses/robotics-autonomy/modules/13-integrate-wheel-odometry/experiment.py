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


def _trace(name: str, x: Any, y: Any) -> dict[str, Any]:
    return {"type": "scatter", "mode": "lines", "name": name, "x": x, "y": y}


def _wrap(angle: float) -> float:
    return float((angle + np.pi) % (2.0 * np.pi) - np.pi)


def _advance(
    state: np.ndarray, left: float, right: float, track: float, euler: bool
) -> np.ndarray:
    distance = 0.5 * (left + right)
    heading_delta = (right - left) / track
    x, y, heading = state
    if euler:
        return np.array(
            [
                x + distance * np.cos(heading),
                y + distance * np.sin(heading),
                heading + heading_delta,
            ]
        )
    scale = (
        1.0
        if abs(heading_delta) < 1e-12
        else 2.0 * np.sin(0.5 * heading_delta) / heading_delta
    )
    midpoint = heading + 0.5 * heading_delta
    return np.array(
        [
            x + distance * scale * np.cos(midpoint),
            y + distance * scale * np.sin(midpoint),
            heading + heading_delta,
        ]
    )


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    radius = float(parameters["wheel_radius_m"])
    track = float(parameters["track_width_m"])
    cpr = round(float(parameters["encoder_cpr"]))
    duration = float(parameters["duration_s"])
    slip = float(parameters["slip_percent"]) / 100.0
    broken = bool(parameters["broken_mode"])
    count = min(round(duration * 50.0) + 1, 1001)
    times = np.linspace(0.0, duration, count)
    dt = times[1] - times[0]
    left_rate = 5.0 + 1.2 * np.sin(0.6 * times[:-1])
    right_rate = 7.0 - 1.0 * np.sin(0.4 * times[:-1])
    edge_angle = 2.0 * np.pi / (4.0 * cpr)
    left_cumulative = np.rint(np.cumsum(left_rate * dt) / edge_angle).astype(int)
    right_cumulative = np.rint(np.cumsum(right_rate * dt) / edge_angle).astype(int)
    left_counts = np.diff(np.r_[0, left_cumulative])
    right_counts = np.diff(np.r_[0, right_cumulative])
    estimate = np.zeros((count, 3))
    truth = np.zeros((count, 3))
    path_length = 0.0
    for index in range(count - 1):
        left_est = radius * left_counts[index] * edge_angle
        right_est = radius * right_counts[index] * edge_angle
        estimate[index + 1] = _advance(
            estimate[index], left_est, right_est, track, broken
        )
        left_true = radius * left_rate[index] * dt
        right_true = radius * right_rate[index] * dt * (1.0 - slip)
        truth[index + 1] = _advance(truth[index], left_true, right_true, track, False)
        path_length += 0.5 * (abs(left_est) + abs(right_est))
    position_error = np.linalg.norm(estimate[:, :2] - truth[:, :2], axis=1)
    heading_error = np.array(
        [
            abs(_wrap(left - right))
            for left, right in zip(estimate[:, 2], truth[:, 2], strict=True)
        ]
    )
    signature = [
        estimate[-1, 0],
        estimate[-1, 1],
        np.degrees(_wrap(estimate[-1, 2])),
        path_length,
        position_error[-1],
        np.degrees(heading_error[-1]),
    ]
    return {
        "metrics": [
            {
                "id": "final_position_error",
                "label": "Final position error",
                "value": position_error[-1],
                "unit": "m",
                "emphasis": "primary",
            },
            {
                "id": "final_heading_error",
                "label": "Final heading error",
                "value": np.degrees(heading_error[-1]),
                "unit": "deg",
            },
            {
                "id": "integrated_distance",
                "label": "Integrated wheel distance",
                "value": path_length,
                "unit": "m",
            },
            {
                "id": "encoder_edge_angle",
                "label": "Encoder edge angle",
                "value": np.degrees(edge_angle),
                "unit": "deg",
            },
        ],
        "plots": {
            "response": {
                "data": [
                    _trace("Ground truth", truth[:, 0], truth[:, 1]),
                    _trace("Wheel odometry", estimate[:, 0], estimate[:, 1]),
                ],
                "layout": _layout(
                    "Integrated planar trajectory", "World x (m)", "World y (m)"
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "mechanism": {
                "data": [
                    _trace("Position error", times, position_error),
                    _trace(
                        "Heading error / 10", times, np.degrees(heading_error) / 10.0
                    ),
                ],
                "layout": _layout(
                    "Accumulated odometry disagreement",
                    "Time (s)",
                    "Error (m or 10 deg)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "Encoder quantization is bounded per sample, but systematic right-wheel slip changes curvature and accumulates pose error throughout the trajectory.",
            "broken": "Broken mode projects every increment along the old heading, a first-order approximation that cuts corners during finite rotations.",
            "recovery": "Convert count differences to wheel travel and apply the exact differential-drive twist about its midpoint; estimate slip separately rather than hiding it in integration.",
        },
        "diagnostics": {
            "item_id": "P13",
            "reference_basis": "independent SE(2) exponential integration of quantized wheel increments",
            "broken_active": broken,
            "sample_count": count,
            "signature": [float(value) for value in signature],
        },
    }
