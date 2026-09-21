from __future__ import annotations

from typing import Any

import numpy as np

DEFAULTS: dict[str, dict[str, Any]] = {
    "P01": {"left_wheel_rad_s": 6.0, "right_wheel_rad_s": 9.0, "wheel_radius_m": 0.08, "track_width_m": 0.35, "duration_s": 8.0},
    "P02": {"heading_deg": 30.0, "robot_x_m": 0.5, "robot_y_m": -0.25, "point_x_m": 1.2, "point_y_m": 0.4},
    "P03": {"joint1_deg": 35.0, "joint2_deg": -45.0, "link1_m": 0.8, "link2_m": 0.6},
    "P04": {"target_x_m": 1.0, "target_y_m": 0.4, "link1_m": 0.8, "link2_m": 0.7, "elbow_up": False},
    "P05": {"voltage_v": 12.0, "gear_ratio": 20.0, "load_torque_nm": 0.2},
    "P06": {"kp_v_per_rad_s": 1.5, "ki_v_per_rad": 4.0, "command_rad_s": 8.0, "voltage_limit_v": 12.0},
    "P07": {"distance_m": 2.0, "duration_s": 4.0},
    "P08": {"stiffness_n_m": 200.0, "damping_ns_m": 20.0, "desired_penetration_mm": 5.0},
    "P09": {"counts_per_rev": 1024.0, "speed_rpm": 120.0, "sample_rate_hz": 50.0, "duration_s": 2.0},
    "P10": {"gyro_bias_deg_s": 0.2, "accel_bias_m_s2": 0.03, "duration_s": 30.0, "sample_rate_hz": 100.0},
}


def parameters(item_id: str, broken: bool, overrides: dict[str, Any] | None = None) -> dict[str, Any]:
    values = dict(DEFAULTS[item_id])
    if overrides:
        values.update(overrides)
    values["broken_mode"] = broken
    return values


def _linear_states(
    matrix: np.ndarray,
    forcing: np.ndarray,
    times: np.ndarray,
) -> np.ndarray:
    steady = -np.linalg.solve(matrix, forcing)
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    inverse = np.linalg.inv(eigenvectors)
    initial_delta = -steady
    states = np.empty((len(times), len(steady)), dtype=float)
    for index, instant in enumerate(times):
        transition = eigenvectors @ np.diag(np.exp(eigenvalues * instant)) @ inverse
        states[index] = np.real_if_close(steady + transition @ initial_delta).real
    return states


def _p01(p: dict[str, Any], broken: bool) -> list[float]:
    left = p["left_wheel_rad_s"]
    right = p["right_wheel_rad_s"]
    radius = p["wheel_radius_m"]
    track = p["track_width_m"]
    duration = p["duration_s"]
    speed = 0.5 * radius * (left + right)
    yaw = radius * (right - left) / track
    heading = yaw * duration
    if broken or abs(yaw) < 1e-12:
        x = speed * duration
        y = 0.0
    else:
        x = speed * np.sin(heading) / yaw
        y = speed * (1.0 - np.cos(heading)) / yaw
    return [speed, yaw, x, y, heading, abs(speed) * duration]


def _p02(p: dict[str, Any], broken: bool) -> list[float]:
    theta = np.radians(p["heading_deg"])
    c = np.cos(theta)
    s = np.sin(theta)
    rotation = np.array([[c, -s], [s, c]])
    origin = np.array([p["robot_x_m"], p["robot_y_m"]])
    body = np.array([p["point_x_m"], p["point_y_m"]])
    world = origin + (rotation.T if broken else rotation) @ body
    inverse = rotation.T @ (world - origin)
    error = np.linalg.norm(inverse - body)
    return [world[0], world[1], inverse[0], inverse[1], error]


def _p03(p: dict[str, Any], broken: bool) -> list[float]:
    q1 = np.radians(p["joint1_deg"])
    q2 = np.radians(p["joint2_deg"])
    link1 = p["link1_m"]
    link2 = p["link2_m"]
    elbow = link1 * np.array([np.cos(q1), np.sin(q1)])
    angle2 = q2 if broken else q1 + q2
    tool = elbow + link2 * np.array([np.cos(angle2), np.sin(angle2)])
    return [elbow[0], elbow[1], tool[0], tool[1], np.linalg.norm(tool)]


def _p04(p: dict[str, Any], broken: bool) -> list[float]:
    target = np.array([p["target_x_m"], p["target_y_m"]])
    link1 = p["link1_m"]
    link2 = p["link2_m"]
    raw = (target @ target - link1**2 - link2**2) / (2.0 * link1 * link2)
    reachable = abs(raw) <= 1.0
    cosine = np.clip(raw, -1.0, 1.0)
    sine_mag = np.sqrt(max(0.0, 1.0 - cosine**2))
    sine = -sine_mag if p["elbow_up"] else sine_mag
    q2 = np.arctan2(sine, cosine)
    bearing = np.arctan2(target[1], target[0])
    correction = np.arctan2(link2 * sine, link1 + link2 * cosine)
    q1 = bearing if broken else bearing - correction
    elbow = link1 * np.array([np.cos(q1), np.sin(q1)])
    tool = elbow + link2 * np.array([np.cos(q1 + q2), np.sin(q1 + q2)])
    return [np.degrees(q1), np.degrees(q2), tool[0], tool[1], np.linalg.norm(tool - target), float(reachable)]


def _p05(p: dict[str, Any], broken: bool) -> list[float]:
    resistance = 1.0
    inductance = 0.02
    torque_constant = 0.05
    emf_constant = 0.0 if broken else 0.05
    ratio = p["gear_ratio"]
    drag = 0.001
    inertia = 0.002 + 0.02 / ratio**2
    matrix = np.array([
        [-resistance / inductance, -emf_constant / inductance],
        [torque_constant / inertia, -drag / inertia],
    ])
    forcing = np.array([p["voltage_v"] / inductance, -p["load_torque_nm"] / (ratio * inertia)])
    times = np.linspace(0.0, 2.0, 2001)
    states = _linear_states(matrix, forcing, times)
    current = states[:, 0]
    output_speed = states[:, 1] / ratio
    steady_motor = (torque_constant * p["voltage_v"] / resistance - p["load_torque_nm"] / ratio) / (
        drag + torque_constant * emf_constant / resistance
    )
    steady_output = steady_motor / ratio
    return [
        current[-1],
        output_speed[-1],
        steady_output,
        abs(output_speed[-1] - steady_output),
        np.max(current),
    ]


def _p06(p: dict[str, Any], broken: bool) -> list[float]:
    sample_time = 0.01
    count = 401
    speed = np.zeros(count)
    effort = np.zeros(count)
    memory = np.zeros(count)
    for step in range(count - 1):
        error = p["command_rad_s"] - speed[step]
        delta = error if broken else sample_time * error
        next_memory = memory[step] + delta
        unconstrained = p["kp_v_per_rad_s"] * error + p["ki_v_per_rad"] * next_memory
        command = float(np.clip(unconstrained, -p["voltage_limit_v"], p["voltage_limit_v"]))
        outward = (
            unconstrained > p["voltage_limit_v"] and error > 0.0
        ) or (
            unconstrained < -p["voltage_limit_v"] and error < 0.0
        )
        if not broken and outward:
            next_memory = memory[step]
            unconstrained = p["kp_v_per_rad_s"] * error + p["ki_v_per_rad"] * next_memory
            command = float(np.clip(unconstrained, -p["voltage_limit_v"], p["voltage_limit_v"]))
        memory[step + 1] = next_memory
        effort[step] = command
        speed[step + 1] = speed[step] + sample_time * (command - speed[step]) / 0.25
    effort[-1] = np.clip(
        p["kp_v_per_rad_s"] * (p["command_rad_s"] - speed[-1])
        + p["ki_v_per_rad"] * memory[-1],
        -p["voltage_limit_v"],
        p["voltage_limit_v"],
    )
    tail = count // 5
    tail_mae = np.mean(np.abs(p["command_rad_s"] - speed[-tail:]))
    overshoot = max(0.0, np.max(speed) - p["command_rad_s"])
    saturated = np.mean(np.abs(effort) >= p["voltage_limit_v"] - 1e-12)
    return [speed[-1], tail_mae, np.max(np.abs(effort)), memory[-1], overshoot, saturated]


def _p07(p: dict[str, Any], broken: bool) -> list[float]:
    distance = p["distance_m"]
    duration = p["duration_s"]
    tau = np.linspace(0.0, 1.0, 501)
    if broken:
        position = distance * (3.0 * tau**2 - 2.0 * tau**3)
        velocity = distance * (6.0 * tau - 6.0 * tau**2) / duration
        acceleration = distance * (6.0 - 12.0 * tau) / duration**2
        jerk = np.full_like(tau, -12.0 * distance / duration**3)
    else:
        position = distance * (10.0 * tau**3 - 15.0 * tau**4 + 6.0 * tau**5)
        velocity = distance * (30.0 * tau**2 - 60.0 * tau**3 + 30.0 * tau**4) / duration
        acceleration = distance * (60.0 * tau - 180.0 * tau**2 + 120.0 * tau**3) / duration**2
        jerk = distance * (60.0 - 360.0 * tau + 360.0 * tau**2) / duration**3
    return [position[-1], np.max(velocity), np.max(np.abs(acceleration)), acceleration[0], acceleration[-1], np.max(np.abs(jerk))]


def _p08(p: dict[str, Any], broken: bool) -> list[float]:
    stiffness = p["stiffness_n_m"]
    damping = p["damping_ns_m"]
    desired = p["desired_penetration_mm"] / 1000.0
    environment = 0.0 if broken else 500.0
    matrix = np.array([[0.0, 1.0], [-(stiffness + environment), -damping]])
    forcing = np.array([0.0, stiffness * desired])
    times = np.linspace(0.0, 1.5, 1501)
    states = _linear_states(matrix, forcing, times)
    penetration = states[:, 0]
    velocity = states[:, 1]
    contact = environment * np.maximum(penetration, 0.0)
    expected_static = stiffness * desired / (stiffness + environment)
    energy = (
        0.5 * velocity[-1] ** 2
        + 0.5 * stiffness * (penetration[-1] - desired) ** 2
        + 0.5 * environment * max(penetration[-1], 0.0) ** 2
    )
    return [
        1000.0 * penetration[-1],
        np.max(contact),
        1000.0 * expected_static,
        1000.0 * abs(penetration[-1] - expected_static),
        energy,
    ]


def _p09(p: dict[str, Any], broken: bool) -> list[float]:
    lines = round(p["counts_per_rev"])
    samples = min(round(p["duration_s"] * p["sample_rate_hz"]) + 1, 1001)
    times = np.linspace(0.0, p["duration_s"], samples)
    true_speed = p["speed_rpm"] * 2.0 * np.pi / 60.0
    true_angle = true_speed * times
    edges = 4 * lines
    counts = np.rint(true_angle * edges / (2.0 * np.pi)).astype(int)
    divisor = lines if broken else edges
    estimate = counts * 2.0 * np.pi / divisor
    speed = np.zeros_like(estimate)
    speed[1:] = np.diff(estimate) / np.diff(times)
    error = estimate - true_angle
    return [float(counts[-1]), estimate[-1], np.sqrt(np.mean(error**2)), np.mean(speed[1:]), np.pi / edges]


def _p10(p: dict[str, Any], broken: bool) -> list[float]:
    duration = p["duration_s"]
    gyro_radians = p["gyro_bias_deg_s"] if broken else np.radians(p["gyro_bias_deg_s"])
    angle = gyro_radians * duration
    velocity = p["accel_bias_m_s2"] * duration
    position = 0.5 * p["accel_bias_m_s2"] * duration**2
    intended_angle = np.radians(p["gyro_bias_deg_s"]) * duration
    return [np.degrees(angle), velocity, position, abs(angle - intended_angle), 0.0]


_ORACLES = {
    "P01": _p01,
    "P02": _p02,
    "P03": _p03,
    "P04": _p04,
    "P05": _p05,
    "P06": _p06,
    "P07": _p07,
    "P08": _p08,
    "P09": _p09,
    "P10": _p10,
}


def expected_signature(
    item_id: str,
    broken: bool = False,
    overrides: dict[str, Any] | None = None,
) -> list[float]:
    values = parameters(item_id, broken, overrides)
    return [float(value) for value in _ORACLES[item_id](values, broken)]
