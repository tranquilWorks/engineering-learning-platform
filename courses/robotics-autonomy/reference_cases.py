from __future__ import annotations

from itertools import pairwise
from typing import Any

import numpy as np

DEFAULTS: dict[str, dict[str, Any]] = {
    "P01": {
        "left_wheel_rad_s": 6.0,
        "right_wheel_rad_s": 9.0,
        "wheel_radius_m": 0.08,
        "track_width_m": 0.35,
        "duration_s": 8.0,
    },
    "P02": {
        "heading_deg": 30.0,
        "robot_x_m": 0.5,
        "robot_y_m": -0.25,
        "point_x_m": 1.2,
        "point_y_m": 0.4,
    },
    "P03": {"joint1_deg": 35.0, "joint2_deg": -45.0, "link1_m": 0.8, "link2_m": 0.6},
    "P04": {
        "target_x_m": 1.0,
        "target_y_m": 0.4,
        "link1_m": 0.8,
        "link2_m": 0.7,
        "elbow_up": False,
    },
    "P05": {"voltage_v": 12.0, "gear_ratio": 20.0, "load_torque_nm": 0.2},
    "P06": {
        "kp_v_per_rad_s": 1.5,
        "ki_v_per_rad": 4.0,
        "command_rad_s": 8.0,
        "voltage_limit_v": 12.0,
    },
    "P07": {"distance_m": 2.0, "duration_s": 4.0},
    "P08": {
        "stiffness_n_m": 200.0,
        "damping_ns_m": 20.0,
        "desired_penetration_mm": 5.0,
    },
    "P09": {
        "counts_per_rev": 1024.0,
        "speed_rpm": 120.0,
        "sample_rate_hz": 50.0,
        "duration_s": 2.0,
    },
    "P10": {
        "gyro_bias_deg_s": 0.2,
        "accel_bias_m_s2": 0.03,
        "duration_s": 30.0,
        "sample_rate_hz": 100.0,
    },
    "P11": {
        "wall_distance_m": 3.0,
        "beam_angle_deg": 20.0,
        "noise_std_m": 0.02,
        "max_range_m": 8.0,
    },
    "P12": {
        "sensor_x_m": 0.18,
        "sensor_y_m": -0.07,
        "sensor_yaw_deg": 12.0,
        "noise_mm": 2.0,
        "correspondence_count": 24.0,
    },
    "P13": {
        "wheel_radius_m": 0.08,
        "track_width_m": 0.36,
        "encoder_cpr": 2048.0,
        "duration_s": 12.0,
        "slip_percent": 2.0,
    },
    "P14": {
        "initial_heading_error_deg": 20.0,
        "gps_noise_m": 0.25,
        "process_noise": 0.02,
        "gps_interval_s": 0.5,
    },
    "P15": {
        "particle_count": 400.0,
        "motion_noise_m": 0.08,
        "sensor_noise_m": 0.4,
        "steps": 18.0,
    },
    "P16": {
        "pose_count": 8.0,
        "odometry_sigma_m": 0.05,
        "range_sigma_m": 0.1,
        "prior_weight": 1000.0,
    },
    "P17": {"grid_size": 21.0, "gap_offset": 5.0, "heuristic_weight": 1.0},
    "P18": {
        "sample_budget": 700.0,
        "step_size_m": 0.65,
        "goal_bias": 0.15,
        "obstacle_radius_m": 1.4,
    },
    "P19": {
        "robot_speed_m_s": 1.0,
        "obstacle_speed_m_s": 1.0,
        "prediction_horizon_s": 8.0,
        "safety_radius_m": 0.8,
    },
    "P20": {
        "navigate_ticks": 5.0,
        "grasp_failures": 2.0,
        "retry_limit": 3.0,
        "mission_ticks": 20.0,
    },
    "P21": {
        "target_detect_s": 2.0,
        "execute_duration_s": 4.0,
        "watchdog_s": 6.0,
        "fault_time_s": 5.0,
    },
    "P22": {
        "control_wcet_ms": 5.0,
        "perception_wcet_ms": 18.0,
        "planning_wcet_ms": 25.0,
        "horizon_ms": 100.0,
    },
    "P23": {
        "command_speed_m_s": 2.0,
        "obstacle_distance_m": 3.0,
        "reaction_time_s": 0.2,
        "deceleration_m_s2": 2.5,
    },
    "P24": {
        "plant_tau_s": 0.4,
        "io_latency_ms": 30.0,
        "fault_start_s": 2.0,
        "fault_duration_s": 1.0,
        "watchdog_ms": 120.0,
    },
}


def parameters(
    item_id: str, broken: bool, overrides: dict[str, Any] | None = None
) -> dict[str, Any]:
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
    return [
        np.degrees(q1),
        np.degrees(q2),
        tool[0],
        tool[1],
        np.linalg.norm(tool - target),
        float(reachable),
    ]


def _p05(p: dict[str, Any], broken: bool) -> list[float]:
    resistance = 1.0
    inductance = 0.02
    torque_constant = 0.05
    emf_constant = 0.0 if broken else 0.05
    ratio = p["gear_ratio"]
    drag = 0.001
    inertia = 0.002 + 0.02 / ratio**2
    matrix = np.array(
        [
            [-resistance / inductance, -emf_constant / inductance],
            [torque_constant / inertia, -drag / inertia],
        ]
    )
    forcing = np.array(
        [p["voltage_v"] / inductance, -p["load_torque_nm"] / (ratio * inertia)]
    )
    times = np.linspace(0.0, 2.0, 2001)
    states = _linear_states(matrix, forcing, times)
    current = states[:, 0]
    output_speed = states[:, 1] / ratio
    steady_motor = (
        torque_constant * p["voltage_v"] / resistance - p["load_torque_nm"] / ratio
    ) / (drag + torque_constant * emf_constant / resistance)
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
        command = float(
            np.clip(unconstrained, -p["voltage_limit_v"], p["voltage_limit_v"])
        )
        outward = (unconstrained > p["voltage_limit_v"] and error > 0.0) or (
            unconstrained < -p["voltage_limit_v"] and error < 0.0
        )
        if not broken and outward:
            next_memory = memory[step]
            unconstrained = (
                p["kp_v_per_rad_s"] * error + p["ki_v_per_rad"] * next_memory
            )
            command = float(
                np.clip(unconstrained, -p["voltage_limit_v"], p["voltage_limit_v"])
            )
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
    return [
        speed[-1],
        tail_mae,
        np.max(np.abs(effort)),
        memory[-1],
        overshoot,
        saturated,
    ]


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
        acceleration = (
            distance * (60.0 * tau - 180.0 * tau**2 + 120.0 * tau**3) / duration**2
        )
        jerk = distance * (60.0 - 360.0 * tau + 360.0 * tau**2) / duration**3
    return [
        position[-1],
        np.max(velocity),
        np.max(np.abs(acceleration)),
        acceleration[0],
        acceleration[-1],
        np.max(np.abs(jerk)),
    ]


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
    return [
        float(counts[-1]),
        estimate[-1],
        np.sqrt(np.mean(error**2)),
        np.mean(speed[1:]),
        np.pi / edges,
    ]


def _p10(p: dict[str, Any], broken: bool) -> list[float]:
    duration = p["duration_s"]
    gyro_radians = p["gyro_bias_deg_s"] if broken else np.radians(p["gyro_bias_deg_s"])
    angle = gyro_radians * duration
    velocity = p["accel_bias_m_s2"] * duration
    position = 0.5 * p["accel_bias_m_s2"] * duration**2
    intended_angle = np.radians(p["gyro_bias_deg_s"]) * duration
    return [np.degrees(angle), velocity, position, abs(angle - intended_angle), 0.0]


def _standard_pattern(count: int) -> np.ndarray:
    values = np.linspace(-1.0, 1.0, count)
    values -= np.mean(values)
    return values / np.sqrt(np.mean(values**2))


def _wrap(angle: float) -> float:
    return float((angle + np.pi) % (2.0 * np.pi) - np.pi)


def _p11(p: dict[str, Any], broken: bool) -> list[float]:
    angle = np.radians(p["beam_angle_deg"])
    true_range = p["wall_distance_m"] / np.cos(angle)
    model_range = p["wall_distance_m"] if broken else true_range
    raw = true_range + p["noise_std_m"] * _standard_pattern(101)
    measured = np.clip(raw, 0.0, p["max_range_m"])
    residual = measured - model_range
    return [
        true_range,
        model_range,
        np.mean(measured),
        np.mean(residual),
        np.sqrt(np.mean(residual**2)),
        np.mean(raw >= p["max_range_m"]),
    ]


def _extrinsic_points(p: dict[str, Any]) -> tuple[np.ndarray, np.ndarray]:
    count = round(p["correspondence_count"])
    phase = np.linspace(0.0, 2.0 * np.pi, count, endpoint=False)
    radii = 0.7 + 0.2 * np.sin(3.0 * phase)
    sensor = np.column_stack((radii * np.cos(phase), radii * np.sin(phase)))
    yaw = np.radians(p["sensor_yaw_deg"])
    rotation = np.array([[np.cos(yaw), -np.sin(yaw)], [np.sin(yaw), np.cos(yaw)]])
    body = sensor @ rotation.T + np.array([p["sensor_x_m"], p["sensor_y_m"]])
    noise = p["noise_mm"] / 1000.0
    body += noise * np.column_stack((np.sin(1.7 * phase), np.cos(2.3 * phase)))
    return sensor, body


def _p12(p: dict[str, Any], broken: bool) -> list[float]:
    sensor, body = _extrinsic_points(p)
    sensor_center = np.mean(sensor, axis=0)
    body_center = np.mean(body, axis=0)
    source = sensor - sensor_center
    target = body - body_center
    if broken:
        yaw = 0.0
    else:
        numerator = np.sum(source[:, 0] * target[:, 1] - source[:, 1] * target[:, 0])
        denominator = np.sum(source[:, 0] * target[:, 0] + source[:, 1] * target[:, 1])
        yaw = np.arctan2(numerator, denominator)
    rotation = np.array([[np.cos(yaw), -np.sin(yaw)], [np.sin(yaw), np.cos(yaw)]])
    translation = body_center - rotation @ sensor_center
    predicted = sensor @ rotation.T + translation
    residual = np.sqrt(np.mean(np.sum((predicted - body) ** 2, axis=1)))
    truth_translation = np.array([p["sensor_x_m"], p["sensor_y_m"]])
    translation_error = np.linalg.norm(translation - truth_translation)
    yaw_error = abs(_wrap(yaw - np.radians(p["sensor_yaw_deg"])))
    return [
        translation[0],
        translation[1],
        np.degrees(yaw),
        residual,
        translation_error,
        np.degrees(yaw_error),
    ]


def _se2_increment(
    state: np.ndarray, left: float, right: float, track: float, broken: bool
) -> np.ndarray:
    distance = 0.5 * (left + right)
    heading_delta = (right - left) / track
    x, y, heading = state
    if broken:
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
    middle = heading + 0.5 * heading_delta
    return np.array(
        [
            x + distance * scale * np.cos(middle),
            y + distance * scale * np.sin(middle),
            heading + heading_delta,
        ]
    )


def _p13(p: dict[str, Any], broken: bool) -> list[float]:
    count = min(round(p["duration_s"] * 50.0) + 1, 1001)
    times = np.linspace(0.0, p["duration_s"], count)
    dt = times[1] - times[0]
    left_rate = 5.0 + 1.2 * np.sin(0.6 * times[:-1])
    right_rate = 7.0 - 1.0 * np.sin(0.4 * times[:-1])
    encoder_step = 2.0 * np.pi / (4.0 * round(p["encoder_cpr"]))
    left_counts = np.rint(np.cumsum(left_rate * dt) / encoder_step).astype(int)
    right_counts = np.rint(np.cumsum(right_rate * dt) / encoder_step).astype(int)
    left_counts = np.diff(np.r_[0, left_counts])
    right_counts = np.diff(np.r_[0, right_counts])
    estimate = np.zeros(3)
    truth = np.zeros(3)
    path_length = 0.0
    slip = p["slip_percent"] / 100.0
    for index in range(count - 1):
        left_est = p["wheel_radius_m"] * left_counts[index] * encoder_step
        right_est = p["wheel_radius_m"] * right_counts[index] * encoder_step
        estimate = _se2_increment(
            estimate, left_est, right_est, p["track_width_m"], broken
        )
        left_true = p["wheel_radius_m"] * left_rate[index] * dt
        right_true = p["wheel_radius_m"] * right_rate[index] * dt * (1.0 - slip)
        truth = _se2_increment(truth, left_true, right_true, p["track_width_m"], False)
        path_length += 0.5 * (abs(left_est) + abs(right_est))
    position_error = np.linalg.norm(estimate[:2] - truth[:2])
    heading_error = abs(_wrap(estimate[2] - truth[2]))
    return [
        estimate[0],
        estimate[1],
        np.degrees(_wrap(estimate[2])),
        path_length,
        position_error,
        np.degrees(heading_error),
    ]


def _ekf_motion(
    value: np.ndarray,
    speed: float,
    yaw_rate: float,
    dt: float,
    broken: bool,
) -> np.ndarray:
    local_heading = np.radians(value[2]) if broken else value[2]
    local_middle = local_heading + 0.5 * yaw_rate * dt
    return value + np.array(
        [
            speed * dt * np.cos(local_middle),
            speed * dt * np.sin(local_middle),
            yaw_rate * dt,
        ]
    )


def _ekf_reference(
    p: dict[str, Any], broken: bool
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    dt = 0.05
    times = np.arange(0.0, 12.0 + 0.5 * dt, dt)
    truth = np.zeros((len(times), 3))
    estimate = np.zeros((len(times), 3))
    estimate[0, 2] = np.radians(p["initial_heading_error_deg"])
    covariance = np.diag([0.5, 0.5, np.radians(15.0) ** 2])
    traces = np.zeros(len(times))
    traces[0] = np.trace(covariance)
    gps_steps = max(1, round(p["gps_interval_s"] / dt))
    process = p["process_noise"] * np.diag([0.2, 0.2, 0.05]) * dt
    measurement = p["gps_noise_m"] ** 2 * np.eye(2)
    identity = np.eye(3)
    for index in range(len(times) - 1):
        speed = 0.8 + 0.1 * np.sin(0.4 * times[index])
        yaw_rate = 0.12
        middle_truth = truth[index, 2] + 0.5 * yaw_rate * dt
        truth[index + 1] = truth[index] + np.array(
            [
                speed * dt * np.cos(middle_truth),
                speed * dt * np.sin(middle_truth),
                yaw_rate * dt,
            ]
        )

        previous = estimate[index].copy()
        trig_heading = np.radians(previous[2]) if broken else previous[2]
        middle = trig_heading + 0.5 * yaw_rate * dt
        predicted = previous + np.array(
            [speed * dt * np.cos(middle), speed * dt * np.sin(middle), yaw_rate * dt]
        )

        jacobian = np.empty((3, 3))
        epsilon = 1e-6
        for column in range(3):
            delta = np.zeros(3)
            delta[column] = epsilon
            jacobian[:, column] = (
                _ekf_motion(previous + delta, speed, yaw_rate, dt, broken)
                - _ekf_motion(previous - delta, speed, yaw_rate, dt, broken)
            ) / (2.0 * epsilon)
        covariance = jacobian @ covariance @ jacobian.T + process
        if (index + 1) % gps_steps == 0:
            phase = float(index + 1)
            z = truth[index + 1, :2] + p["gps_noise_m"] * np.array(
                [0.6 * np.sin(0.37 * phase), 0.6 * np.cos(0.29 * phase)]
            )
            h = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
            innovation = z - predicted[:2]
            gain = covariance @ h.T @ np.linalg.inv(h @ covariance @ h.T + measurement)
            predicted = predicted + gain @ innovation
            kh = identity - gain @ h
            covariance = kh @ covariance @ kh.T + gain @ measurement @ gain.T
        predicted[2] = _wrap(predicted[2])
        estimate[index + 1] = predicted
        traces[index + 1] = np.trace(covariance)
    return times, truth, estimate, traces


def _p14(p: dict[str, Any], broken: bool) -> list[float]:
    _, truth, estimate, traces = _ekf_reference(p, broken)
    errors = np.linalg.norm(estimate[:, :2] - truth[:, :2], axis=1)
    return [
        estimate[-1, 0],
        estimate[-1, 1],
        np.degrees(estimate[-1, 2]),
        np.sqrt(np.mean(errors**2)),
        traces[-1],
        errors[-1],
    ]


def _circular_statistics(
    values: np.ndarray, length: float, weights: np.ndarray | None = None
) -> tuple[float, float]:
    angles = 2.0 * np.pi * values / length
    if weights is None:
        weights = np.full(len(values), 1.0 / len(values))
    sine = np.sum(weights * np.sin(angles))
    cosine = np.sum(weights * np.cos(angles))
    mean = (np.arctan2(sine, cosine) % (2.0 * np.pi)) * length / (2.0 * np.pi)
    resultant = max(np.hypot(sine, cosine), 1e-15)
    std = length * np.sqrt(max(0.0, -2.0 * np.log(resultant))) / (2.0 * np.pi)
    return float(mean), float(std)


def _p15(p: dict[str, Any], broken: bool) -> list[float]:
    length = 20.0
    count = round(p["particle_count"])
    steps = round(p["steps"])
    particles = (np.arange(count) + 0.5) * length / count
    weights = np.full(count, 1.0 / count)
    truth = 18.0
    minimum_ess = float(count)
    indexes = np.arange(count, dtype=float) + 1.0
    for step in range(steps):
        truth = (truth + 0.7) % length
        pattern = np.sin(indexes * (step + 1.0) * 1.61803398875)
        pattern = (pattern - np.mean(pattern)) / np.std(pattern)
        particles = (particles + 0.7 + p["motion_noise_m"] * pattern) % length
        truth_range = min(truth, length - truth)
        measurement = truth_range + 0.35 * p["sensor_noise_m"] * np.sin(
            0.73 * (step + 1.0)
        )
        delta = np.abs(particles)
        predicted = delta if broken else np.minimum(delta, length - delta)
        likelihood = (
            np.exp(-0.5 * ((measurement - predicted) / p["sensor_noise_m"]) ** 2)
            + 1e-300
        )
        weights = likelihood / np.sum(likelihood)
        minimum_ess = min(minimum_ess, 1.0 / np.sum(weights**2))
        cumulative = np.cumsum(weights)
        locations = (np.arange(count) + 0.5) / count
        particles = particles[np.searchsorted(cumulative, locations, side="left")]
        weights.fill(1.0 / count)
    mean, std = _circular_statistics(particles, length)
    error = abs((mean - truth + 0.5 * length) % length - 0.5 * length)
    return [mean, std, truth, error, minimum_ess]


def _slam_system(
    p: dict[str, Any], broken: bool
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    poses = round(p["pose_count"])
    variables = poses + 1
    rows: list[np.ndarray] = []
    values: list[float] = []
    if not broken:
        row = np.zeros(variables)
        row[0] = p["prior_weight"]
        rows.append(row)
        values.append(0.0)
    for index in range(1, poses):
        row = np.zeros(variables)
        row[index - 1] = -1.0 / p["odometry_sigma_m"]
        row[index] = 1.0 / p["odometry_sigma_m"]
        measurement = 1.0 + 0.5 * p["odometry_sigma_m"] * np.sin(1.3 * index)
        rows.append(row)
        values.append(measurement / p["odometry_sigma_m"])
    landmark = float(poses + 2)
    for index in range(poses):
        row = np.zeros(variables)
        row[index] = -1.0 / p["range_sigma_m"]
        row[-1] = 1.0 / p["range_sigma_m"]
        measurement = (
            landmark - index + 0.5 * p["range_sigma_m"] * np.cos(0.9 * (index + 1))
        )
        rows.append(row)
        values.append(measurement / p["range_sigma_m"])
    return np.vstack(rows), np.asarray(values), np.arange(poses, dtype=float)


def _p16(p: dict[str, Any], broken: bool) -> list[float]:
    matrix, values, truth = _slam_system(p, broken)
    normal = matrix.T @ matrix
    estimate = np.linalg.pinv(normal, rcond=1e-12) @ matrix.T @ values
    residual = matrix @ estimate - values
    singular = np.linalg.svd(matrix, compute_uv=False)
    rank = np.linalg.matrix_rank(matrix, tol=1e-10)
    return [
        estimate[-2],
        estimate[-1],
        np.sqrt(np.mean((estimate[:-1] - truth) ** 2)),
        np.sqrt(np.mean(residual**2)),
        float(rank),
        singular[-1],
    ]


def _grid_neighbors(node: tuple[int, int], size: int) -> list[tuple[int, int]]:
    x, y = node
    return [
        (nx, ny)
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))
        if 0 <= nx < size and 0 <= ny < size
    ]


def _dijkstra_grid(
    size: int, gap_y: int, ignore_wall: bool
) -> tuple[float, list[tuple[int, int]]]:
    import heapq

    start = (1, size // 2)
    goal = (size - 2, size // 2)
    wall_x = size // 2
    frontier: list[tuple[float, tuple[int, int]]] = [(0.0, start)]
    cost = {start: 0.0}
    parent: dict[tuple[int, int], tuple[int, int]] = {}
    while frontier:
        distance, current = heapq.heappop(frontier)
        if current == goal:
            break
        if distance != cost[current]:
            continue
        for neighbor in _grid_neighbors(current, size):
            if not ignore_wall and neighbor[0] == wall_x and neighbor[1] != gap_y:
                continue
            candidate = distance + 1.0
            if candidate < cost.get(neighbor, float("inf")):
                cost[neighbor] = candidate
                parent[neighbor] = current
                heapq.heappush(frontier, (candidate, neighbor))
    path = [goal]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return cost[goal], path


def _p17(p: dict[str, Any], broken: bool) -> list[float]:
    size = round(p["grid_size"])
    center = size // 2
    gap = int(np.clip(center + round(p["gap_offset"]), 1, size - 2))
    safe_cost, _ = _dijkstra_grid(size, gap, False)
    path_cost, path = _dijkstra_grid(size, gap, broken)
    collisions = sum(node[0] == center and node[1] != gap for node in path)
    return [path_cost, safe_cost, float(collisions), float(len(path)), 1.0]


def _van_der_corput(index: int, base: int) -> float:
    value = 0.0
    factor = 1.0 / base
    while index:
        value += factor * (index % base)
        index //= base
        factor /= base
    return value


def _segment_clearance(
    start: np.ndarray, end: np.ndarray, center: np.ndarray, radius: float
) -> float:
    delta = end - start
    denominator = float(delta @ delta)
    fraction = (
        0.0
        if denominator == 0.0
        else float(np.clip((center - start) @ delta / denominator, 0.0, 1.0))
    )
    return float(np.linalg.norm(start + fraction * delta - center) - radius)


def _rrt_reference(
    p: dict[str, Any], broken: bool
) -> tuple[list[np.ndarray], list[int], list[int], bool]:
    start = np.array([0.5, 0.5])
    goal = np.array([9.5, 9.5])
    center = np.array([5.0, 5.0])
    radius = p["obstacle_radius_m"]
    nodes = [start]
    parents = [-1]
    goal_index = -1
    for iteration in range(1, round(p["sample_budget"]) + 1):
        if _van_der_corput(iteration, 5) < p["goal_bias"]:
            sample = goal
        else:
            sample = np.array(
                [
                    10.0 * _van_der_corput(iteration, 2),
                    10.0 * _van_der_corput(iteration, 3),
                ]
            )
        distances = [float(np.linalg.norm(node - sample)) for node in nodes]
        nearest_index = int(np.argmin(distances))
        direction = sample - nodes[nearest_index]
        norm = np.linalg.norm(direction)
        if norm < 1e-12:
            continue
        candidate = nodes[nearest_index] + direction / norm * min(
            p["step_size_m"], norm
        )
        clearance = (
            1.0
            if broken
            else _segment_clearance(nodes[nearest_index], candidate, center, radius)
        )
        if clearance < 0.1:
            continue
        nodes.append(candidate)
        parents.append(nearest_index)
        new_index = len(nodes) - 1
        if np.linalg.norm(candidate - goal) <= p["step_size_m"]:
            goal_clearance = (
                1.0 if broken else _segment_clearance(candidate, goal, center, radius)
            )
            if goal_clearance >= 0.1:
                nodes.append(goal.copy())
                parents.append(new_index)
                goal_index = len(nodes) - 1
                break
    path: list[int] = []
    if goal_index >= 0:
        cursor = goal_index
        while cursor >= 0:
            path.append(cursor)
            cursor = parents[cursor]
        path.reverse()
    return nodes, parents, path, goal_index >= 0


def _p18(p: dict[str, Any], broken: bool) -> list[float]:
    nodes, _, path, reached = _rrt_reference(p, broken)
    center = np.array([5.0, 5.0])
    radius = p["obstacle_radius_m"]
    length = 0.0
    collisions = 0
    minimum = 10.0
    for left, right in pairwise(path):
        length += np.linalg.norm(nodes[right] - nodes[left])
        clearance = _segment_clearance(nodes[left], nodes[right], center, radius)
        minimum = min(minimum, clearance)
        collisions += clearance < 0.0
    if not path:
        minimum = min(float(np.linalg.norm(node - center) - radius) for node in nodes)
    return [float(reached), length, float(len(nodes)), float(collisions), minimum]


def _avoidance_candidates(
    p: dict[str, Any], broken: bool
) -> tuple[float, float, float]:
    headings = np.radians(np.arange(-60.0, 61.0, 5.0))
    relative_position = np.array([5.0, -5.0])
    obstacle_velocity = np.array([0.0, 0.0 if broken else p["obstacle_speed_m_s"]])
    best: tuple[float, float, float] | None = None
    fallback: tuple[float, float, float] | None = None
    for heading in headings:
        robot_velocity = p["robot_speed_m_s"] * np.array(
            [np.cos(heading), np.sin(heading)]
        )
        relative_velocity = obstacle_velocity - robot_velocity
        speed_squared = float(relative_velocity @ relative_velocity)
        cpa_time = (
            0.0
            if speed_squared < 1e-12
            else float(
                np.clip(
                    -relative_position @ relative_velocity / speed_squared,
                    0.0,
                    p["prediction_horizon_s"],
                )
            )
        )
        separation = float(
            np.linalg.norm(relative_position + relative_velocity * cpa_time)
        )
        candidate = (
            abs(float(heading)) + 0.1 * (1.0 - np.cos(heading)),
            float(heading),
            separation,
        )
        if fallback is None or separation > fallback[2]:
            fallback = candidate
        if separation >= p["safety_radius_m"] and (
            best is None or candidate[0] < best[0]
        ):
            best = candidate
    chosen = best if best is not None else fallback
    assert chosen is not None
    return chosen[1], chosen[2], chosen[0]


def _p19(p: dict[str, Any], broken: bool) -> list[float]:
    heading, _, _ = _avoidance_candidates(p, broken)
    times = np.linspace(0.0, p["prediction_horizon_s"], 401)
    robot = (
        p["robot_speed_m_s"]
        * times[:, None]
        * np.array([np.cos(heading), np.sin(heading)])
    )
    obstacle = np.column_stack(
        (np.full_like(times, 5.0), -5.0 + p["obstacle_speed_m_s"] * times)
    )
    separation = np.linalg.norm(robot - obstacle, axis=1)
    minimum_index = int(np.argmin(separation))
    return [
        np.degrees(heading),
        separation[minimum_index],
        robot[-1, 0],
        float(separation[minimum_index] < p["safety_radius_m"]),
        times[minimum_index],
    ]


def _p20(p: dict[str, Any], broken: bool) -> list[float]:
    ticks = round(p["mission_ticks"])
    navigate_needed = round(p["navigate_ticks"])
    failures = round(p["grasp_failures"])
    retry_limit = round(p["retry_limit"])
    state = 0
    navigate_progress = 0
    attempts = 0
    deliver_progress = 0
    transitions = 0
    completion = ticks
    for tick in range(ticks):
        previous = state
        if state == 0:
            navigate_progress = 1 if broken else navigate_progress + 1
            if navigate_progress >= navigate_needed:
                state = 1
        elif state == 1:
            attempts += 1
            if attempts <= failures:
                if attempts > retry_limit:
                    state = 4
            else:
                state = 2
        elif state == 2:
            deliver_progress += 1
            if deliver_progress >= 3:
                state = 3
        if state != previous:
            transitions += 1
        if state in {3, 4}:
            completion = tick + 1
            break
    return [
        float(state),
        float(completion),
        float(attempts),
        float(transitions),
        float(state == 3),
    ]


def _mission_reference(
    p: dict[str, Any], broken: bool
) -> tuple[np.ndarray, np.ndarray]:
    dt = 0.1
    times = np.arange(0.0, 12.0 + 0.5 * dt, dt)
    states = np.zeros(len(times), dtype=int)
    state = 0
    entered = 0.0
    for index in range(1, len(times)):
        now = times[index]
        previous = state
        if not broken and now >= p["fault_time_s"] and state not in {4, 5}:
            state = 4
        elif state == 0 and now >= 0.2:
            state, entered = 1, now
        elif state == 1:
            if now >= p["target_detect_s"]:
                state, entered = 2, now
            elif now - entered >= p["watchdog_s"]:
                state, entered = 4, now
        elif state == 2 and now - entered >= 1.0:
            state, entered = 3, now
        elif state == 3 and now - entered >= p["execute_duration_s"]:
            state, entered = 5, now
        states[index] = state
        if state in {4, 5} and previous == state:
            states[index:] = state
            break
    return times, states


def _p21(p: dict[str, Any], broken: bool) -> list[float]:
    times, states = _mission_reference(p, broken)
    terminal = np.flatnonzero(np.isin(states, [4, 5]))
    terminal_time = times[terminal[0]] if len(terminal) else times[-1]
    fault_index = int(np.searchsorted(times, p["fault_time_s"], side="left"))
    unsafe_ticks = np.sum(np.isin(states[fault_index:], [1, 2, 3]))
    transitions = np.count_nonzero(np.diff(states))
    return [
        float(states[-1]),
        terminal_time,
        float(unsafe_ticks),
        float(transitions),
        float(states[-1] == 5),
    ]


def _response_time(
    wcet: float, period: float, higher: list[tuple[float, float]]
) -> float:
    response = wcet
    for _ in range(100):
        updated = wcet + sum(
            np.ceil(response / hp_period) * hp_wcet for hp_period, hp_wcet in higher
        )
        if updated == response or updated > 10_000.0:
            return float(updated)
        response = updated
    return float(response)


def _event_schedule_responses(
    tasks: list[tuple[float, float]], order: list[int], horizon: float
) -> tuple[np.ndarray, int]:
    priority = {task_index: rank for rank, task_index in enumerate(order)}
    jobs = [
        {"task": task_index, "release": release, "remaining": wcet}
        for task_index, (period, wcet) in enumerate(tasks)
        for release in np.arange(0.0, horizon, period)
    ]
    completed: list[list[float]] = [[], [], []]
    now = 0.0
    while now < horizon:
        ready = [
            job for job in jobs if job["release"] <= now and job["remaining"] > 0.0
        ]
        if not ready:
            future = [job["release"] for job in jobs if job["release"] > now]
            if not future:
                break
            now = min(min(future), horizon)
            continue
        active = min(
            ready,
            key=lambda job: (priority[int(job["task"])], job["release"]),
        )
        future_releases = [job["release"] for job in jobs if job["release"] > now]
        next_release = min(future_releases) if future_releases else horizon
        stop = min(now + active["remaining"], next_release, horizon)
        active["remaining"] -= stop - now
        now = stop
        if active["remaining"] <= 1e-12:
            task_index = int(active["task"])
            completed[task_index].append(now - active["release"])
    observed = np.array(
        [max(values) if values else horizon for values in completed], dtype=float
    )
    return observed, len(jobs)


def _p22(p: dict[str, Any], broken: bool) -> list[float]:
    tasks = [
        (20.0, p["control_wcet_ms"]),
        (50.0, p["perception_wcet_ms"]),
        (100.0, p["planning_wcet_ms"]),
    ]
    order = [2, 1, 0] if broken else [0, 1, 2]
    responses = np.zeros(3)
    for rank, task_index in enumerate(order):
        higher = [tasks[index] for index in order[:rank]]
        responses[task_index] = _response_time(
            tasks[task_index][1], tasks[task_index][0], higher
        )
    utilization = sum(wcet / period for period, wcet in tasks)
    schedulable = float(all(responses[index] <= tasks[index][0] for index in range(3)))
    observed, total_jobs = _event_schedule_responses(tasks, order, p["horizon_ms"])
    return [
        utilization,
        observed[0],
        observed[1],
        observed[2],
        schedulable,
        float(total_jobs),
    ]


def _safety_simulation(
    p: dict[str, Any], broken: bool
) -> tuple[np.ndarray, np.ndarray, np.ndarray, int]:
    dt = 0.01
    times = np.arange(0.0, 4.0 + 0.5 * dt, dt)
    position = np.zeros(len(times))
    speed = np.zeros(len(times))
    speed[0] = p["command_speed_m_s"]
    interventions = 0
    braking = False
    for index in range(len(times) - 1):
        distance = p["obstacle_distance_m"] - position[index]
        threshold = (
            0.1
            if broken
            else speed[index] ** 2 / (2.0 * p["deceleration_m_s2"])
            + p["reaction_time_s"] * speed[index]
            + 0.1
        )
        if not braking and distance <= threshold:
            braking = True
            interventions += 1
        if braking:
            speed[index + 1] = max(0.0, speed[index] - p["deceleration_m_s2"] * dt)
        else:
            speed[index + 1] = p["command_speed_m_s"]
        position[index + 1] = (
            position[index] + 0.5 * (speed[index] + speed[index + 1]) * dt
        )
    return times, position, speed, interventions


def _p23(p: dict[str, Any], broken: bool) -> list[float]:
    times, position, speed, interventions = _safety_simulation(p, broken)
    separation = p["obstacle_distance_m"] - position
    stopped = np.flatnonzero(speed <= 1e-12)
    stop_time = times[stopped[0]] if len(stopped) else times[-1]
    return [
        np.min(separation),
        stop_time,
        float(np.any(separation <= 0.0)),
        float(interventions),
        np.max(speed),
        speed[-1],
    ]


def _hil_reference(
    p: dict[str, Any], broken: bool
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    dt = 0.01
    times = np.arange(0.0, 6.0 + 0.5 * dt, dt)
    output = np.zeros(len(times))
    effort = np.zeros(len(times))
    age = np.zeros(len(times))
    delay = max(0, round(p["io_latency_ms"] / 10.0))
    queue = [0.0] * (delay + 1)
    last_measurement = 0.0
    integral = 0.0
    last_update = 0.0
    fault_end = p["fault_start_s"] + p["fault_duration_s"]
    watchdog = p["watchdog_ms"] / 1000.0
    for index in range(len(times) - 1):
        now = times[index]
        queue.append(output[index])
        delayed = queue.pop(0)
        dropout = p["fault_start_s"] <= now < fault_end
        if not dropout:
            last_measurement = delayed
            last_update = now
        age[index] = now - last_update
        safe = age[index] > watchdog and not broken
        error = 1.0 - last_measurement
        if safe:
            command = 0.0
        else:
            integral += error * dt
            command = float(np.clip(2.0 * error + integral, -2.0, 2.0))
        effort[index] = command
        output[index + 1] = (
            output[index] + dt * (-output[index] + command) / p["plant_tau_s"]
        )
    age[-1] = times[-1] - last_update
    effort[-1] = effort[-2]
    return times, output, effort, age


def _p24(p: dict[str, Any], broken: bool) -> list[float]:
    times, output, _, age = _hil_reference(p, broken)
    watchdog = p["watchdog_ms"] / 1000.0
    detections = np.flatnonzero(age > watchdog)
    detection_time = (
        times[detections[0]] if len(detections) and not broken else times[-1]
    )
    safe_duration = np.sum((age > watchdog) & (not broken)) * (times[1] - times[0])
    error = 1.0 - output
    verdict = float(len(detections) > 0 and not broken and np.all(np.isfinite(output)))
    return [
        np.max(np.abs(error)),
        np.max(output),
        detection_time,
        safe_duration,
        output[-1],
        verdict,
    ]


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
    "P11": _p11,
    "P12": _p12,
    "P13": _p13,
    "P14": _p14,
    "P15": _p15,
    "P16": _p16,
    "P17": _p17,
    "P18": _p18,
    "P19": _p19,
    "P20": _p20,
    "P21": _p21,
    "P22": _p22,
    "P23": _p23,
    "P24": _p24,
}


def expected_signature(
    item_id: str,
    broken: bool = False,
    overrides: dict[str, Any] | None = None,
) -> list[float]:
    values = parameters(item_id, broken, overrides)
    return [float(value) for value in _ORACLES[item_id](values, broken)]
