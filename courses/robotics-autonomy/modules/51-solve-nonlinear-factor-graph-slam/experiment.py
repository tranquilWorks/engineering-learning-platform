from __future__ import annotations

from itertools import pairwise
from typing import Any

import numpy as np

ITEM_NUMBER = 51
BROKEN_TEXT = (
    "Broken mode removes the absolute prior and landmark factors, offsets the whole "
    "initial trajectory, and performs one linearization of a gauge-free relative graph."
)
RECOVERY_TEXT = (
    "Restore one explicit gauge prior, relinearize nonlinear range factors, and iterate "
    "until both weighted residual and state increment settle."
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


def _problem(
    count: int, loop_noise_m: float, broken: bool
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    phase = np.linspace(0.0, 2.0 * np.pi, count)
    truth = np.column_stack((4.0 * np.cos(phase), 2.5 * np.sin(phase)))
    edge_phase = np.linspace(0.0, 2.0 * np.pi, count - 1, endpoint=False)
    odometry = np.diff(truth, axis=0) + 0.012 * np.column_stack(
        (np.sin(edge_phase), -0.6 * np.cos(edge_phase))
    )
    estimate = np.vstack((truth[0], truth[0] + np.cumsum(odometry, axis=0)))
    estimate += 0.08 * np.column_stack((np.sin(1.7 * phase), np.cos(1.3 * phase)))
    if broken:
        estimate += np.array([0.40, -0.30])
    loop_measurement = truth[0] - truth[-1] + loop_noise_m * np.array([1.0, -0.5])
    landmarks = np.array([[-1.5, 0.8], [1.2, -0.9]])
    return truth, odometry, estimate, np.vstack((loop_measurement, landmarks))


def _linearize(
    estimate: np.ndarray,
    truth: np.ndarray,
    odometry: np.ndarray,
    loop_and_landmarks: np.ndarray,
    loop_noise_m: float,
    broken: bool,
) -> tuple[np.ndarray, np.ndarray]:
    count = len(estimate)
    residuals: list[float] = []
    jacobians: list[np.ndarray] = []

    def add(vector: np.ndarray, jacobian: np.ndarray, sigma: float) -> None:
        for row, value in zip(jacobian / sigma, vector / sigma, strict=True):
            jacobians.append(row)
            residuals.append(float(value))

    if not broken:
        prior_jacobian = np.zeros((2, 2 * count))
        prior_jacobian[:, :2] = np.eye(2)
        add(estimate[0] - truth[0], prior_jacobian, 0.02)

    for index, measurement in enumerate(odometry):
        jacobian = np.zeros((2, 2 * count))
        jacobian[:, 2 * index : 2 * index + 2] = -np.eye(2)
        jacobian[:, 2 * index + 2 : 2 * index + 4] = np.eye(2)
        add(estimate[index + 1] - estimate[index] - measurement, jacobian, 0.05)

    loop_measurement = loop_and_landmarks[0]
    loop_jacobian = np.zeros((2, 2 * count))
    loop_jacobian[:, :2] = -np.eye(2)
    loop_jacobian[:, -2:] = np.eye(2)
    add(
        estimate[-1] - estimate[0] - loop_measurement,
        loop_jacobian,
        max(loop_noise_m, 0.02),
    )

    if not broken:
        landmarks = loop_and_landmarks[1:]
        stride = max(1, count // 10)
        for pose_index in range(0, count, stride):
            for landmark_index, landmark in enumerate(landmarks):
                difference = estimate[pose_index] - landmark
                distance = max(float(np.linalg.norm(difference)), 1.0e-9)
                true_range = float(np.linalg.norm(truth[pose_index] - landmark))
                measured_range = true_range + 0.015 * np.sin(
                    0.7 * pose_index + landmark_index
                )
                jacobian = np.zeros((1, 2 * count))
                jacobian[0, 2 * pose_index : 2 * pose_index + 2] = difference / distance
                add(np.array([distance - measured_range]), jacobian, 0.04)

    return np.asarray(residuals), np.vstack(jacobians)


def _solve(
    count: int, loop_noise_m: float, broken: bool
) -> tuple[np.ndarray, np.ndarray, list[float], float]:
    truth, odometry, estimate, loop_and_landmarks = _problem(
        count, loop_noise_m, broken
    )
    history: list[float] = []
    normal_condition = 0.0
    iterations = 1 if broken else 7
    for _ in range(iterations):
        residual, jacobian = _linearize(
            estimate, truth, odometry, loop_and_landmarks, loop_noise_m, broken
        )
        history.append(float(np.sqrt(np.mean(residual**2))))
        normal = jacobian.T @ jacobian
        singular = np.linalg.svd(normal, compute_uv=False)
        if singular[-1] <= singular[0] * 1.0e-12:
            normal_condition = 1.0e12
        else:
            normal_condition = float(singular[0] / singular[-1])
        increment = np.linalg.lstsq(jacobian, -residual, rcond=1.0e-10)[0]
        estimate += increment.reshape((-1, 2))
        if float(np.linalg.norm(increment)) < 1.0e-9:
            break
    final_residual, _ = _linearize(
        estimate, truth, odometry, loop_and_landmarks, loop_noise_m, broken
    )
    history.append(float(np.sqrt(np.mean(final_residual**2))))
    return truth, estimate, history, normal_condition


def _model(parameters: dict[str, Any], broken: bool) -> dict[str, Any]:
    loop_noise_m = float(parameters["loop_noise_m"])
    pose_count = round(float(parameters["pose_count"]))
    truth, estimate, history, normal_condition = _solve(
        pose_count, loop_noise_m, broken
    )
    trajectory_rmse = float(np.sqrt(np.mean(np.sum((estimate - truth) ** 2, axis=1))))
    gauge_residual = float(np.linalg.norm(estimate[0] - truth[0]))
    signature = [trajectory_rmse, gauge_residual, normal_condition]
    iterations = np.arange(len(history), dtype=float)

    return {
        "signature": signature,
        "sample_count": max(len(truth), len(history)),
        "metrics": [
            ("trajectory_rmse", "Trajectory RMSE", signature[0], "m"),
            ("gauge_residual", "Gauge-Origin Residual", signature[1], "m"),
            ("normal_condition", "Normal-Matrix Condition", signature[2], "1"),
        ],
        "plots": {
            "response": _plot(
                "Optimized two-dimensional pose graph",
                "East position (m)",
                "North position (m)",
                [
                    _trace(
                        "Ground truth",
                        truth[:, 0],
                        truth[:, 1],
                        "East position",
                        "m",
                        "North position",
                        "m",
                    ),
                    _trace(
                        "Estimated poses",
                        estimate[:, 0],
                        estimate[:, 1],
                        "East position",
                        "m",
                        "North position",
                        "m",
                    ),
                ],
            ),
            "mechanism": _plot(
                "Gauss-Newton residual convergence",
                "Linearization iteration (count)",
                "Weighted factor residual RMS (1)",
                [
                    _trace(
                        "Residual RMS",
                        iterations,
                        history,
                        "Linearization iteration",
                        "count",
                        "Weighted factor residual RMS",
                        "1",
                    ),
                    _trace(
                        "Zero residual",
                        iterations,
                        np.zeros_like(iterations),
                        "Linearization iteration",
                        "count",
                        "Weighted factor residual RMS",
                        "1",
                    ),
                ],
            ),
        },
        "observation": (
            "Relative factors determine shape, but a gauge prior determines the global "
            "frame; nonlinear range factors must be relinearized around the updated poses."
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


def _joint_slam_problem(count, noise, broken):
    phase = np.linspace(0.0, 2 * np.pi, count)
    poses = np.column_stack((3 * np.cos(phase), 2 * np.sin(phase), phase + np.pi / 2))
    landmarks = np.array([[-0.8, 0.4], [0.9, -0.6], [0.1, 1.1]])

    def rot(a):
        return np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])

    odom = np.array(
        [np.r_[rot(p[2]).T @ (q[:2] - p[:2]), q[2] - p[2]] for p, q in pairwise(poses)]
    )
    odom += 0.006 * np.column_stack(
        (
            np.sin(np.arange(count - 1)),
            np.cos(1.3 * np.arange(count - 1)),
            0.2 * np.sin(0.8 * np.arange(count - 1)),
        )
    )
    observations = []
    for i in range(count):
        for j, l in enumerate(landmarks):
            z = rot(poses[i, 2]).T @ (l - poses[i, :2]) + 0.004 * np.array(
                [np.sin(0.7 * i + j), np.cos(1.1 * i - j)]
            )
            observations.append((i, j, z))
    initial = poses.copy()
    initial[:, :2] += 0.12 * np.column_stack((np.sin(1.7 * phase), np.cos(1.3 * phase)))
    initial[:, 2] += 0.05 * np.sin(phase)
    initial_map = landmarks + np.array([0.16, -0.12])
    if broken:
        R = rot(0.25)
        initial[:, :2] = initial[:, :2] @ R.T + [0.5, -0.3]
        initial[:, 2] += 0.25
        initial_map = initial_map @ R.T + [0.5, -0.3]
    return (
        poses,
        landmarks,
        odom,
        observations,
        np.r_[initial.ravel(), initial_map.ravel()],
    )


def _joint_slam_linearize(state, count, odom, observations, prior, noise, broken):
    from scipy.sparse import lil_matrix

    poses = state[: 3 * count].reshape(count, 3)
    landmarks = state[3 * count :].reshape(3, 2)
    total = 3 * (count - 1) + 3 + 2 * len(observations) + (0 if broken else 3)
    J = lil_matrix((total, len(state)))
    res = np.zeros(total)
    row = 0
    S = np.array([[0.0, -1.0], [1.0, 0.0]])

    def rotation(a):
        return np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])

    if not broken:
        res[:3] = (poses[0] - prior) / 0.01
        J[:3, :3] = np.eye(3) / 0.01
        row = 3
    for i, z in enumerate(odom):
        R = rotation(poses[i, 2]).T
        d = R @ (poses[i + 1, :2] - poses[i, :2])
        scale = np.array([0.03, 0.03, 0.015])
        res[row : row + 3] = (np.r_[d, poses[i + 1, 2] - poses[i, 2]] - z) / scale
        J[row : row + 2, 3 * i : 3 * i + 2] = -R / 0.03
        J[row : row + 2, 3 * i + 3 : 3 * i + 5] = R / 0.03
        J[row : row + 2, 3 * i + 2] = (-S @ d / 0.03)[:, None]
        J[row + 2, 3 * i + 2] = -1 / 0.015
        J[row + 2, 3 * i + 5] = 1 / 0.015
        row += 3
    # Closing body displacement is zero; unwrapped heading changes by 2*pi.
    R = rotation(poses[0, 2]).T
    d = R @ (poses[-1, :2] - poses[0, :2])
    sigma = max(noise, 0.02)
    res[row : row + 3] = (
        np.r_[d, poses[-1, 2] - poses[0, 2] - 2 * np.pi]
        - np.array([noise, -0.5 * noise, 0])
    ) / np.array([sigma, sigma, 0.02])
    J[row : row + 2, :2] = -R / sigma
    J[row : row + 2, 3 * count - 3 : 3 * count - 1] = R / sigma
    J[row : row + 2, 2] = (-S @ d / sigma)[:, None]
    J[row + 2, 2] = -50.0
    J[row + 2, 3 * count - 1] = 50.0
    row += 3
    for i, j, z in observations:
        R = rotation(poses[i, 2]).T
        d = R @ (landmarks[j] - poses[i, :2])
        res[row : row + 2] = (d - z) / 0.025
        J[row : row + 2, 3 * i : 3 * i + 2] = -R / 0.025
        J[row : row + 2, 3 * i + 2] = (-S @ d / 0.025)[:, None]
        J[row : row + 2, 3 * count + 2 * j : 3 * count + 2 * j + 2] = R / 0.025
        row += 2
    return res, J.tocsr()


def _joint_slam(count, noise, broken):
    from scipy.sparse.linalg import lsmr

    truth, landmarks, odom, observations, state = _joint_slam_problem(
        count, noise, broken
    )
    history = []
    for iteration in range(12):
        residual, J = _joint_slam_linearize(
            state, count, odom, observations, truth[0], noise, broken
        )
        history.append([iteration, float(residual @ residual), 0.0])
        step = lsmr(J, -residual, atol=1e-11, btol=1e-11, maxiter=4 * len(state))[0]
        scale = 1.0
        for _ in range(12):
            trial = state + scale * step
            r, _ = _joint_slam_linearize(
                trial, count, odom, observations, truth[0], noise, broken
            )
            if r @ r <= residual @ residual + 1e-12:
                break
            scale *= 0.5
        state = trial
        history[-1][2] = float(np.linalg.norm(scale * step))
        if history[-1][2] < 1e-8:
            break
    residual, J = _joint_slam_linearize(
        state, count, odom, observations, truth[0], noise, broken
    )
    return {
        "poses": state[: 3 * count].reshape(count, 3),
        "landmarks": state[3 * count :].reshape(3, 2),
        "truth": truth,
        "true_landmarks": landmarks,
        "iterations": np.asarray(history),
        "cost": float(residual @ residual),
        "jacobian": J,
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    result = _result(_model(parameters, broken), broken)
    joint = _joint_slam(
        round(float(parameters["pose_count"])),
        float(parameters["loop_noise_m"]),
        broken,
    )
    poses, landmarks = joint["poses"], joint["landmarks"]
    result["diagnostics"]["joint_slam"] = {
        k: v for k, v in joint.items() if k != "jacobian"
    }
    result["plots"]["joint_map"] = _plot(
        "Joint pose and map",
        "East position (m)",
        "North position (m)",
        [
            _trace(
                "Estimated robot", poses[:, 0], poses[:, 1], "East", "m", "North", "m"
            ),
            _trace(
                "Estimated map",
                landmarks[:, 0],
                landmarks[:, 1],
                "East",
                "m",
                "North",
                "m",
            ),
            _trace(
                "True robot",
                joint["truth"][:, 0],
                joint["truth"][:, 1],
                "East",
                "m",
                "North",
                "m",
            ),
        ],
    )
    result["plots"]["joint_map"]["data"][1]["mode"] = "markers"
    true_map = _trace(
        "True map",
        joint["true_landmarks"][:, 0],
        joint["true_landmarks"][:, 1],
        "East",
        "m",
        "North",
        "m",
    )
    true_map.update(mode="markers", marker={"symbol": "cross", "size": 9})
    result["plots"]["joint_map"]["data"].append(true_map)
    result["plots"]["joint_convergence"] = _plot(
        "Joint solve convergence",
        "Iteration (count)",
        "Weighted error (1)",
        [
            _trace(
                "Objective",
                joint["iterations"][:, 0],
                joint["iterations"][:, 1],
                "Iteration",
                "count",
                "Objective",
                "1",
            )
        ],
    )
    return result
