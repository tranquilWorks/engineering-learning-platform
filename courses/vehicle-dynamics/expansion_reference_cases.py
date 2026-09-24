"""Independent Vehicle Dynamics P25-P43 references.

This module imports no production experiment, consumes no production result, and
perturbs no production value. It independently evaluates the retained scalar
signatures for the reviewed bounded scenarios.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def _rotation(angle: float) -> np.ndarray:
    cosine, sine = np.cos(angle), np.sin(angle)
    return np.array(((cosine, -sine), (sine, cosine)))


def _p25(p: dict[str, Any]) -> list[float]:
    heading_deg = float(p["path_heading_deg"])
    heading_rad = np.deg2rad(heading_deg)
    used_angle = heading_deg if bool(p["broken_mode"]) else heading_rad
    steer_rad = np.deg2rad(float(p["wheel_steer_deg"]))
    nominal_path = np.array((24.0, 1.5))
    inertial = _rotation(heading_rad).dot(nominal_path)
    path = _rotation(-used_angle).dot(inertial)
    body = _rotation(-(heading_rad - np.deg2rad(4.0))).dot(inertial)
    wheel = _rotation(-steer_rad).dot(body)
    return [
        float(path[0]),
        float(path[1]),
        float(np.rad2deg(np.arctan2(wheel[1], wheel[0]))),
        float(abs(np.linalg.norm(path) - np.linalg.norm(inertial))),
        float(np.linalg.norm(path - nominal_path)),
    ]


def _p26(p: dict[str, Any]) -> list[float]:
    load = float(p["normal_load_n"])
    reviewed_exponent = float(p["load_exponent"])
    exponent = 1.0 if bool(p["broken_mode"]) else reviewed_exponent
    reference_load, reference_mu = 3500.0, 1.25

    def force(value: float) -> float:
        return reference_mu * reference_load * (value / reference_load) ** exponent

    peak = force(load)
    split = force(0.75 * load) + force(1.25 * load)
    return [
        peak,
        peak / load,
        2.0 * peak - split,
        abs(force(2.0 * load) / peak - 2.0**reviewed_exponent),
        float(bool(p["broken_mode"])),
    ]


def _p27(p: dict[str, Any]) -> list[float]:
    stiffness = float(p["longitudinal_stiffness_n"])
    friction = float(p["peak_friction"])
    normal_load = 3500.0
    peak = friction * normal_load
    training_ratio = np.array((-0.16, -0.10, -0.05, -0.025, 0.025, 0.05, 0.10, 0.16))
    training_force = np.minimum(np.maximum(stiffness * training_ratio, -peak), peak)
    fitting_ratio = training_ratio * (100.0 if bool(p["broken_mode"]) else 1.0)
    linear = np.abs(training_force) < 0.90 * peak
    fitted_stiffness = float(
        np.sum(fitting_ratio[linear] * training_force[linear])
        / np.sum(fitting_ratio[linear] ** 2)
    )
    fitted_mu = float(np.max(np.abs(training_force)) / normal_load)
    held_ratio = np.array((-0.13, -0.07, -0.035, 0.035, 0.07, 0.13))
    held_force = np.minimum(np.maximum(stiffness * held_ratio, -peak), peak)
    predicted = np.minimum(
        np.maximum(fitted_stiffness * held_ratio, -fitted_mu * normal_load),
        fitted_mu * normal_load,
    )
    rmse = float(np.sqrt(np.sum((predicted - held_force) ** 2) / held_ratio.size))
    return [
        fitted_stiffness,
        fitted_mu,
        rmse,
        peak,
        abs(fitted_stiffness - stiffness) / stiffness,
    ]


def _p28(p: dict[str, Any]) -> list[float]:
    cornering = float(p["cornering_stiffness_n_rad"])
    camber = float(p["camber_stiffness_n_rad"])
    peak = 3500.0 * 1.2
    alpha_deg = np.array((-2.0, -1.0, 0.0, 1.0, 2.0, -1.5, 1.5, 0.5, -0.5))
    gamma_deg = np.array((-1.0, 1.0, -1.0, 1.0, 0.0, 0.5, -0.5, 1.5, -1.5))
    alpha = alpha_deg * np.pi / 180.0
    gamma = gamma_deg * np.pi / 180.0
    force = np.minimum(
        np.maximum(-(cornering * alpha + camber * gamma), -peak),
        peak,
    )
    if bool(p["broken_mode"]):
        matrix = np.column_stack((alpha_deg, gamma_deg))
    else:
        matrix = np.column_stack((alpha, gamma))
    mask = np.abs(force) < 0.90 * peak
    estimate = np.linalg.solve(
        matrix[mask].T.dot(matrix[mask]),
        matrix[mask].T.dot(-force[mask]),
    )
    held_alpha = np.array((-3.0, -1.25, 0.75, 2.5)) * np.pi / 180.0
    held_gamma = np.array((0.5, -1.5, 1.0, -0.5)) * np.pi / 180.0
    truth = np.minimum(
        np.maximum(-(cornering * held_alpha + camber * held_gamma), -peak),
        peak,
    )
    predicted = np.minimum(
        np.maximum(-(estimate[0] * held_alpha + estimate[1] * held_gamma), -peak),
        peak,
    )
    rmse = float(np.sqrt(np.sum((predicted - truth) ** 2) / held_alpha.size))
    relative_error = float(
        np.linalg.norm(estimate - np.array((cornering, camber)))
        / max(np.hypot(cornering, camber), 1.0)
    )
    return [
        float(estimate[0]),
        float(estimate[1]),
        rmse,
        float(np.max(np.abs(force)) / peak),
        relative_error,
    ]


def _p29(p: dict[str, Any]) -> list[float]:
    ratio = float(p["slip_ratio"])
    angle = float(p["slip_angle_deg"]) * np.pi / 180.0
    capacity = 3500.0 * 1.2
    pure_x = capacity * np.tanh(80000.0 * ratio / capacity)
    pure_y = -capacity * np.tanh(70000.0 * angle / capacity)
    demand = float(np.hypot(pure_x, pure_y) / capacity)
    scale = 1.0
    if not bool(p["broken_mode"]) and demand > 1.0:
        scale = 1.0 / demand
    delivered_x, delivered_y = scale * pure_x, scale * pure_y
    utilization = float(np.hypot(delivered_x, delivered_y) / capacity)
    return [
        float(delivered_x),
        float(delivered_y),
        utilization,
        scale,
        max(0.0, utilization - 1.0),
    ]


def _p30(p: dict[str, Any]) -> list[float]:
    length = float(p["relaxation_length_m"])
    speed = float(p["speed_m_s"])
    tau = length if bool(p["broken_mode"]) else length / speed
    steady = 3000.0
    at_length_time = length / speed
    force_at_length = steady * (1.0 - np.exp(-at_length_time / tau))
    response_distance = speed * tau
    final_error = steady * np.exp(-0.50 / tau)
    return [
        float(force_at_length),
        response_distance,
        tau,
        float(final_error),
        abs(response_distance - length) / length,
    ]


def _p31(p: dict[str, Any]) -> list[float]:
    heat = float(p["heat_input_w"])
    ambient = float(p["ambient_temp_c"])
    capacity, coefficient = 15000.0, 35.0
    step, samples = 2.0, 301
    temperature = np.empty(samples)
    temperature[0] = ambient
    rejected = 0.0
    for index in range(1, samples):
        loss = coefficient * (temperature[index - 1] - ambient)
        rejected += loss * step
        temperature[index] = temperature[index - 1] + (heat - loss) * step / capacity
    expected_pressure = 210.0 * (temperature + 273.15) / (20.0 + 273.15)
    pressure = (
        210.0 * temperature / 20.0
        if bool(p["broken_mode"])
        else expected_pressure
    )
    grip = 1.25 * np.exp(-((temperature - 80.0) / 38.0) ** 2)
    grip *= np.maximum(0.45, 1.0 - 0.00002 * (pressure - 240.0) ** 2)
    pressure_residual = abs(float(pressure[-1] - expected_pressure[-1]))
    balance = abs(
        heat * 600.0 - rejected - capacity * (temperature[-1] - ambient)
    )
    return [
        float(temperature[-1]),
        float(pressure[-1]),
        float(np.max(grip)),
        pressure_residual,
        float(balance),
    ]


def _p32(p: dict[str, Any]) -> list[float]:
    ratio = float(p["slip_ratio"])
    angle = float(p["slip_angle_deg"]) * np.pi / 180.0
    power = abs(3000.0 * 30.0 * ratio) + abs(2800.0 * 30.0 * np.tan(angle))
    capacity, coefficient = 16000.0, 45.0
    step, samples = 0.25, 241
    temperature = np.empty(samples)
    temperature[0] = 30.0
    rejected = 0.0
    for index in range(1, samples):
        loss = coefficient * (temperature[index - 1] - 25.0)
        rejected += loss * step
        applied_loss = 0.0 if bool(p["broken_mode"]) else loss
        temperature[index] = temperature[index - 1] + (
            power - applied_loss
        ) * step / capacity
    work = power * 60.0
    stored = capacity * (temperature[-1] - 30.0)
    return [
        float(power),
        float(work),
        float(temperature[-1] - 30.0),
        float(rejected),
        float(abs(work - stored - rejected)),
    ]


def _p33(p: dict[str, Any]) -> list[float]:
    sigma = float(p["observation_sigma_n"])
    held_fraction = float(p["validation_fraction"])
    indices = np.arange(40)
    basis = np.linspace(500.0, 4200.0, 40)
    pattern = 1.10 * np.sin(indices * 1.7) + 0.45 * np.cos(indices * 0.6)
    observed = 0.92 * basis + sigma * pattern
    train_count = min(max(round(40 * (1.0 - held_fraction)), 16), 32)
    if bool(p["broken_mode"]):
        fit_basis, fit_observed = basis, observed
        used_sigma = 0.20 * sigma
    else:
        fit_basis, fit_observed = basis[:train_count], observed[:train_count]
        used_sigma = sigma
    scale = float(np.sum(fit_basis * fit_observed) / np.sum(fit_basis**2))
    residual = observed[train_count:] - scale * basis[train_count:]
    normalized = residual / used_sigma
    return [
        scale,
        float(np.mean(residual)),
        float(np.sqrt(np.mean(residual**2))),
        float(np.mean(np.abs(normalized) <= 1.96)),
        float(np.max(np.abs(normalized))),
    ]


def _bicycle_matrices(speed: float, front: float, rear: float) -> tuple[np.ndarray, np.ndarray]:
    mass, inertia, a, b = 1450.0, 2400.0, 1.20, 1.50
    matrix = np.array(
        (
            (
                -(front + rear) / (mass * speed),
                (-a * front + b * rear) / (mass * speed**2) - 1.0,
            ),
            (
                (-a * front + b * rear) / inertia,
                -(a**2 * front + b**2 * rear) / (inertia * speed),
            ),
        )
    )
    vector = np.array((front / (mass * speed), a * front / inertia))
    return matrix, vector


def _p34(p: dict[str, Any]) -> list[float]:
    speed = float(p["speed_m_s"])
    front = float(p["front_cornering_n_rad"])
    rear_used = -75000.0 if bool(p["broken_mode"]) else 75000.0
    matrix, vector = _bicycle_matrices(speed, front, rear_used)
    steer = 2.0 * np.pi / 180.0
    beta, yaw_rate = np.linalg.solve(-matrix, vector * steer)
    front_force = front * (steer - beta - 1.20 * yaw_rate / speed)
    rear_force = 75000.0 * (-beta + 1.50 * yaw_rate / speed)
    return [
        float(beta * 180.0 / np.pi),
        float(yaw_rate * 180.0 / np.pi),
        float(np.max(np.real(np.linalg.eigvals(matrix)))),
        float(abs(1450.0 * speed * yaw_rate - front_force - rear_force)),
        float(abs(1.20 * front_force - 1.50 * rear_force)),
    ]


def _p35(p: dict[str, Any]) -> list[float]:
    speed = float(p["speed_m_s"])
    frequency = float(p["frequency_hz"])
    matrix, vector = _bicycle_matrices(speed, 70000.0, 75000.0)
    declared_omega = 2.0 * np.pi * frequency
    used_omega = frequency if bool(p["broken_mode"]) else declared_omega
    dynamic = 1j * used_omega * np.eye(2) - matrix
    state = np.linalg.solve(dynamic, vector)
    physical_dynamic = 1j * declared_omega * np.eye(2) - matrix
    residual = np.linalg.norm(physical_dynamic.dot(state) - vector)
    dc = np.linalg.solve(-matrix, vector)
    return [
        float(np.abs(state[1])),
        float(np.abs(state[0])),
        float(np.angle(state[1]) * 180.0 / np.pi),
        float(dc[1]),
        float(residual),
    ]


def _p36(p: dict[str, Any]) -> list[float]:
    front = float(p["front_cornering_n_rad"])
    rear = float(p["rear_cornering_n_rad"])
    mass, gravity, a, b = 1450.0, 9.81, 1.20, 1.50
    wheelbase = a + b
    front_weight = mass * gravity * b / wheelbase
    rear_weight = mass * gravity * a / wheelbase
    unit_scale = np.pi / 180.0 if bool(p["broken_mode"]) else 1.0
    gradient = front_weight / (front * unit_scale) - rear_weight / (rear * unit_scale)
    correct_gradient = front_weight / front - rear_weight / rear
    characteristic = (
        np.sqrt(gravity * wheelbase / gradient) if gradient > 1.0e-12 else 0.0
    )
    steer = wheelbase / 80.0 + 0.70 * gradient
    residual = abs((steer - wheelbase / 80.0) - 0.70 * correct_gradient)
    class_code = 1.0 if gradient > 1.0e-8 else (-1.0 if gradient < -1.0e-8 else 0.0)
    return [
        float(gradient * 180.0 / np.pi),
        float(characteristic),
        float(steer * 180.0 / np.pi),
        class_code,
        float(residual * 180.0 / np.pi),
    ]


def _limit_forces(
    beta: float,
    steer: float,
    friction: float,
    broken: bool,
) -> tuple[float, float]:
    speed, a, b = 28.0, 1.20, 1.50
    mass, gravity = 1450.0, 9.81
    yaw_rate = speed * np.tan(steer) / (a + b)
    alpha_front = steer - beta - a * yaw_rate / speed
    alpha_rear = -beta + b * yaw_rate / speed
    linear_front = 70000.0 * alpha_front
    linear_rear = 75000.0 * alpha_rear
    capacity_front = friction * mass * gravity * b / (a + b)
    capacity_rear = friction * mass * gravity * a / (a + b)
    if broken:
        return linear_front, linear_rear
    return (
        capacity_front * np.tanh(linear_front / capacity_front),
        capacity_rear * np.tanh(linear_rear / capacity_rear),
    )


def _p37(p: dict[str, Any]) -> list[float]:
    steer = np.deg2rad(float(p["steer_deg"]))
    friction = float(p["friction_mu"])
    mass, gravity, a, b = 1450.0, 9.81, 1.20, 1.50
    capacity_front = friction * mass * gravity * b / (a + b)
    capacity_rear = friction * mass * gravity * a / (a + b)
    beta = np.deg2rad(10.0)
    front, rear = _limit_forces(beta, steer, friction, bool(p["broken_mode"]))
    front_utilization = abs(front) / capacity_front
    rear_utilization = abs(rear) / capacity_rear
    moment = a * front - b * rear
    epsilon = 1.0e-5
    plus_front, plus_rear = _limit_forces(
        beta + epsilon, steer, friction, bool(p["broken_mode"])
    )
    minus_front, minus_rear = _limit_forces(
        beta - epsilon, steer, friction, bool(p["broken_mode"])
    )
    slope = (
        a * (plus_front - minus_front) - b * (plus_rear - minus_rear)
    ) / (2.0 * epsilon)
    return [
        float(front_utilization),
        float(rear_utilization),
        float(abs(moment)),
        float(-slope),
        float(max(0.0, front_utilization - 1.0, rear_utilization - 1.0)),
    ]


def _p38(p: dict[str, Any]) -> list[float]:
    mass, gravity = 1450.0, 9.81
    a, b, height = 1.20, 1.50, 0.52
    front_track, rear_track = 1.55, 1.53
    acceleration = float(p["lateral_accel_g"]) * gravity
    distribution = float(p["front_roll_stiffness_fraction"])
    front_mass = mass * b / (a + b)
    rear_mass = mass * a / (a + b)
    geometric_front = front_mass * acceleration * 0.07
    geometric_rear = rear_mass * acceleration * 0.11
    total_moment = mass * acceleration * height
    geometric_total = geometric_front + geometric_rear
    elastic = total_moment if bool(p["broken_mode"]) else total_moment - geometric_total
    front_transfer = geometric_front / front_track + distribution * elastic / front_track
    rear_transfer = geometric_rear / rear_track + (1.0 - distribution) * elastic / rear_track
    closure = abs(front_transfer * front_track + rear_transfer * rear_track - total_moment)
    front_axle_load = mass * gravity * b / (a + b)
    left = max(1.0, front_axle_load / 2.0 - front_transfer / 2.0)
    right = front_axle_load / 2.0 + front_transfer / 2.0
    force = lambda load: 1.25 * 3500.0 * (load / 3500.0) ** 0.86
    loss = 2.0 * force(front_axle_load / 2.0) - force(left) - force(right)
    return [
        float(front_transfer),
        float(rear_transfer),
        float(geometric_total / total_moment),
        float(closure),
        float(loss),
    ]


def _chassis_matrices(front: float, rear: float) -> tuple[np.ndarray, np.ndarray]:
    mass_matrix = np.diag((1450.0, 2600.0, 650.0))
    corners = (
        (1.20, 0.775, front * 1.04),
        (1.20, -0.775, front * 0.96),
        (-1.50, 0.765, rear * 0.97),
        (-1.50, -0.765, rear * 1.03),
    )
    stiffness = np.zeros((3, 3))
    for x_position, y_position, rate in corners:
        geometry = np.array((1.0, x_position, y_position))
        stiffness = stiffness + rate * np.outer(geometry, geometry)
    return mass_matrix, stiffness


def _p39(p: dict[str, Any]) -> list[float]:
    mass_matrix, physical_stiffness = _chassis_matrices(
        float(p["front_spring_rate_n_m"]),
        float(p["rear_spring_rate_n_m"]),
    )
    used_stiffness = (
        np.diag(np.diag(physical_stiffness))
        if bool(p["broken_mode"])
        else physical_stiffness
    )
    inverse_sqrt = np.diag(np.reciprocal(np.sqrt(np.diag(mass_matrix))))
    symmetric = inverse_sqrt.dot(used_stiffness).dot(inverse_sqrt)
    eigenvalues, normalized_modes = np.linalg.eigh(symmetric)
    modes = inverse_sqrt.dot(normalized_modes)
    frequencies = np.sqrt(eigenvalues) / (2.0 * np.pi)
    residuals = []
    for index in range(3):
        left = physical_stiffness.dot(modes[:, index])
        right = eigenvalues[index] * mass_matrix.dot(modes[:, index])
        residuals.append(np.linalg.norm(left - right) / max(np.linalg.norm(left), 1.0))
    off_diagonal = physical_stiffness - np.diag(np.diag(physical_stiffness))
    coupling = np.linalg.norm(off_diagonal) / np.linalg.norm(
        np.diag(np.diag(physical_stiffness))
    )
    reference_residual = (
        float(round(max(residuals), 12)) if bool(p["broken_mode"]) else 0.0
    )
    return [
        float(frequencies[0]),
        float(frequencies[1]),
        float(frequencies[2]),
        float(coupling),
        reference_residual,
    ]


def _p40(p: dict[str, Any]) -> list[float]:
    speed = float(p["speed_m_s"])
    wavelength = float(p["road_wavelength_m"])
    mass, stiffness, damping = 360.0, 32000.0, 2800.0
    frequency = speed / wavelength
    physical_omega = 2.0 * np.pi * frequency
    used_omega = frequency if bool(p["broken_mode"]) else physical_omega
    numerator = stiffness + 1j * damping * used_omega
    denominator = stiffness - mass * used_omega**2 + 1j * damping * used_omega
    response = numerator / denominator
    physical_numerator = stiffness + 1j * damping * physical_omega
    physical_denominator = (
        stiffness - mass * physical_omega**2 + 1j * damping * physical_omega
    )
    residual = abs(physical_denominator * response - physical_numerator) / abs(
        physical_numerator
    )
    natural_frequency = np.sqrt(stiffness / mass) / (2.0 * np.pi)
    return [
        float(abs(response)),
        float(np.angle(response) * 180.0 / np.pi),
        float(abs(response) * 0.010 * physical_omega**2),
        float(frequency / natural_frequency),
        float(residual),
    ]


def _damper_force(
    velocity: np.ndarray | float,
    knee: float,
    high_coefficient: float,
) -> np.ndarray:
    value = np.asarray(velocity, dtype=float)
    return high_coefficient * value + (
        7000.0 - high_coefficient
    ) * value / (1.0 + np.abs(value) / knee)


def _p41(p: dict[str, Any]) -> list[float]:
    knee = float(p["knee_velocity_m_s"])
    high = float(p["high_speed_coefficient_n_s_m"])
    scale = 1000.0 if bool(p["broken_mode"]) else 1.0
    low_force = float(_damper_force(scale * 0.05, knee, high))
    high_force = float(_damper_force(scale * 0.50, knee, high))
    apparent_slope = float(_damper_force(scale * 1.0e-4, knee, high) / 1.0e-4)
    time = np.linspace(0.0, 2.0, 1001)
    velocity = 0.35 * np.sin(np.pi * time)
    force = _damper_force(scale * velocity, knee, high)
    energy = np.trapezoid(force * velocity, time)
    residual = abs(
        float(_damper_force(scale * 0.20, knee, high))
        - float(_damper_force(0.20, knee, high))
    )
    return [low_force, high_force, apparent_slope, float(energy), float(residual)]


def _suspension_state(
    travel_mm: float,
    force: float,
    broken: bool,
) -> tuple[float, float, float, float]:
    used_travel = travel_mm / 1000.0 if broken else travel_mm
    camber = -1.0 - 0.035 * used_travel - 0.00004 * force
    toe = 0.10 + 0.004 * used_travel + 0.00006 * force
    motion_ratio = 0.85 + 0.0004 * used_travel
    return camber, toe, motion_ratio, 45000.0 * motion_ratio**2


def _p42(p: dict[str, Any]) -> list[float]:
    travel = float(p["bump_travel_mm"])
    force = float(p["lateral_force_n"])
    state = _suspension_state(travel, force, bool(p["broken_mode"]))
    correct = _suspension_state(travel, force, False)
    residual = np.hypot(state[0] - correct[0], state[1] - correct[1])
    return [float(value) for value in (*state, residual)]


def _p43(p: dict[str, Any]) -> list[float]:
    angle = float(p["sideview_angle_deg"])
    height = float(p["cg_height_m"])
    used_angle = angle if bool(p["broken_mode"]) else angle * np.pi / 180.0
    anti_dive = 0.70 * np.tan(used_angle) * 2.70 / height
    anti_squat = np.tan(used_angle) * 2.70 / height
    total_transfer = 1450.0 * 0.80 * 9.81 * height / 2.70
    geometric = anti_dive * total_transfer
    spring = (1.0 - anti_dive) * total_transfer
    physical_anti = 0.70 * np.tan(angle * np.pi / 180.0) * 2.70 / height
    residual = abs(geometric - physical_anti * total_transfer)
    return [
        float(100.0 * anti_dive),
        float(100.0 * anti_squat),
        float(spring),
        float(geometric),
        float(residual),
    ]


_DISPATCH = {
    25: _p25,
    26: _p26,
    27: _p27,
    28: _p28,
    29: _p29,
    30: _p30,
    31: _p31,
    32: _p32,
    33: _p33,
    34: _p34,
    35: _p35,
    36: _p36,
    37: _p37,
    38: _p38,
    39: _p39,
    40: _p40,
    41: _p41,
    42: _p42,
    43: _p43,
}


def origin(number: int) -> dict[str, Any]:
    return {
        "kind": "independent-analytic-and-numerical-python",
        "item_id": f"P{number:02d}",
        "independent": True,
        "imports_production_entrypoint": False,
        "derived_from_production_output": False,
        "perturbs_production_output": False,
    }


def reference_signature(number: int, parameters: dict[str, Any]) -> list[float]:
    return [float(value) for value in _DISPATCH[number](dict(parameters))]
