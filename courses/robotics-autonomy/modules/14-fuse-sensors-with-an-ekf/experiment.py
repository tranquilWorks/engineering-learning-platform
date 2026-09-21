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


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    initial_error = np.radians(float(parameters["initial_heading_error_deg"]))
    gps_noise = float(parameters["gps_noise_m"])
    process_scale = float(parameters["process_noise"])
    gps_interval = float(parameters["gps_interval_s"])
    broken = bool(parameters["broken_mode"])
    dt = 0.05
    times = np.arange(0.0, 12.0 + 0.5 * dt, dt)
    truth = np.zeros((len(times), 3))
    estimate = np.zeros((len(times), 3))
    estimate[0, 2] = initial_error
    covariance = np.diag([0.5, 0.5, np.radians(15.0) ** 2])
    covariance_trace = np.zeros(len(times))
    covariance_trace[0] = np.trace(covariance)
    position_sigma = np.zeros(len(times))
    position_sigma[0] = np.sqrt(covariance[0, 0] + covariance[1, 1])
    gps_steps = max(1, round(gps_interval / dt))
    process = process_scale * np.diag([0.2, 0.2, 0.05]) * dt
    measurement = gps_noise**2 * np.eye(2)
    identity = np.eye(3)
    gps_x: list[float] = []
    gps_y: list[float] = []
    for index in range(len(times) - 1):
        speed = 0.8 + 0.1 * np.sin(0.4 * times[index])
        yaw_rate = 0.12
        truth_middle = truth[index, 2] + 0.5 * yaw_rate * dt
        truth[index + 1] = truth[index] + np.array(
            [
                speed * dt * np.cos(truth_middle),
                speed * dt * np.sin(truth_middle),
                yaw_rate * dt,
            ]
        )
        heading_factor = np.pi / 180.0 if broken else 1.0
        trig_heading = estimate[index, 2] * heading_factor
        middle = trig_heading + 0.5 * yaw_rate * dt
        predicted = estimate[index] + np.array(
            [speed * dt * np.cos(middle), speed * dt * np.sin(middle), yaw_rate * dt]
        )
        jacobian = np.eye(3)
        jacobian[0, 2] = -speed * dt * np.sin(middle) * heading_factor
        jacobian[1, 2] = speed * dt * np.cos(middle) * heading_factor
        covariance = jacobian @ covariance @ jacobian.T + process
        if (index + 1) % gps_steps == 0:
            phase = float(index + 1)
            observation = truth[index + 1, :2] + gps_noise * np.array(
                [0.6 * np.sin(0.37 * phase), 0.6 * np.cos(0.29 * phase)]
            )
            gps_x.append(float(observation[0]))
            gps_y.append(float(observation[1]))
            h = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
            innovation = observation - predicted[:2]
            gain = np.linalg.solve(h @ covariance @ h.T + measurement, h @ covariance).T
            predicted = predicted + gain @ innovation
            kh = identity - gain @ h
            covariance = kh @ covariance @ kh.T + gain @ measurement @ gain.T
        predicted[2] = _wrap(predicted[2])
        estimate[index + 1] = predicted
        covariance_trace[index + 1] = np.trace(covariance)
        position_sigma[index + 1] = np.sqrt(covariance[0, 0] + covariance[1, 1])
    position_error = np.linalg.norm(estimate[:, :2] - truth[:, :2], axis=1)
    rms_error = np.sqrt(np.mean(position_error**2))
    signature = [
        estimate[-1, 0],
        estimate[-1, 1],
        np.degrees(estimate[-1, 2]),
        rms_error,
        covariance_trace[-1],
        position_error[-1],
    ]
    return {
        "metrics": [
            {
                "id": "rms_position_error",
                "label": "RMS position error",
                "value": rms_error,
                "unit": "m",
                "emphasis": "primary",
            },
            {
                "id": "final_position_error",
                "label": "Final position error",
                "value": position_error[-1],
                "unit": "m",
            },
            {
                "id": "final_heading",
                "label": "Estimated final heading",
                "value": np.degrees(estimate[-1, 2]),
                "unit": "deg",
            },
            {
                "id": "covariance_trace",
                "label": "Final covariance trace",
                "value": covariance_trace[-1],
                "unit": "mixed",
            },
        ],
        "plots": {
            "response": {
                "data": [
                    _trace("Ground truth", truth[:, 0], truth[:, 1]),
                    _trace("EKF estimate", estimate[:, 0], estimate[:, 1]),
                    {
                        "type": "scatter",
                        "mode": "markers",
                        "name": "GPS updates",
                        "x": gps_x,
                        "y": gps_y,
                    },
                ],
                "layout": _layout(
                    "Nonlinear planar state estimate", "World x (m)", "World y (m)"
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "mechanism": {
                "data": [
                    _trace("Position error", times, position_error),
                    _trace("Position 1-sigma scale", times, position_sigma),
                ],
                "layout": _layout(
                    "Estimation error and reported uncertainty",
                    "Time (s)",
                    "Distance (m)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "The nonlinear prediction transports pose between GPS updates; each measurement update reduces position covariance and corrects accumulated error.",
            "broken": "Broken mode interprets a radian state as degrees inside sine and cosine, so the state and Jacobian describe the wrong motion even though GPS repeatedly pulls position toward truth.",
            "recovery": "Use one angular unit throughout the motion function and linearize exactly that function; retain the Joseph covariance update to preserve symmetry and positive semidefiniteness.",
        },
        "diagnostics": {
            "item_id": "P14",
            "reference_basis": "independent EKF recurrence with finite-difference motion Jacobian",
            "broken_active": broken,
            "sample_count": len(times),
            "signature": [float(value) for value in signature],
        },
    }
