"""Independent Vehicle Dynamics P25-P67 references.

This module imports no production experiment, consumes no production result, and
perturbs no production value. It independently evaluates the retained scalar
signatures for the reviewed bounded scenarios.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
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


def _p44(p: dict[str, Any]) -> list[float]:
    rpm = float(p["engine_rpm"])
    gear = float(p["gear_ratio"])
    torque = 220.0 - 6.0e-6 * (rpm - 4500.0) ** 2
    engine_force = torque * gear * 4.10 * 0.92 / 0.31
    tire_capacity = 1.15 * 1450.0 * 9.81 * 0.45
    physical_delivery = min(engine_force, tire_capacity)
    delivered = engine_force if bool(p["broken_mode"]) else physical_delivery
    return [
        float(torque),
        float(engine_force),
        float(tire_capacity),
        float(delivered),
        float(abs(delivered - physical_delivery)),
    ]


def _p45(p: dict[str, Any]) -> list[float]:
    torque = float(p["launch_torque_nm"])
    driveline_inertia = float(p["driveline_inertia_kg_m2"])
    broken = bool(p["broken_mode"])
    mass, radius, ratio, efficiency = 1450.0, 0.31, 3.60 * 4.10, 0.90
    wheel_inertia = 1.20
    physical_equivalent = (
        4.0 * wheel_inertia / radius**2
        + driveline_inertia * (ratio / radius) ** 2
    )
    used_equivalent = (
        driveline_inertia / (ratio * radius) ** 2
        if broken
        else physical_equivalent
    )
    effective_mass = mass + used_equivalent
    tire_capacity = 1.15 * mass * 9.81 * 0.45
    drive_force = min(torque * ratio * efficiency / radius, tire_capacity)
    step, samples = 0.01, 1501
    speed = np.zeros(samples)
    distance = np.zeros(samples)
    time = np.arange(samples) * step
    target_time = time[-1]
    for index in range(1, samples):
        resistance = 180.0 + 0.38 * speed[index - 1] ** 2
        acceleration = max(0.0, (drive_force - resistance) / effective_mass)
        speed[index] = speed[index - 1] + acceleration * step
        distance[index] = distance[index - 1] + speed[index - 1] * step
        if speed[index] >= 27.78 and target_time == time[-1]:
            target_time = time[index]
    work = drive_force * distance[-1]
    resistance_work = np.trapezoid(180.0 + 0.38 * speed**2, distance)
    physical_energy = 0.5 * (mass + physical_equivalent) * speed[-1] ** 2
    return [
        float(physical_equivalent if not broken else used_equivalent),
        float((drive_force - 180.0) / effective_mass),
        float(target_time),
        float(speed[-1]),
        float(abs(work - resistance_work - physical_energy)),
    ]


def _p46(p: dict[str, Any]) -> list[float]:
    left_mu = float(p["left_friction_mu"])
    bias = float(p["torque_bias_ratio"])
    wheel_load, right_mu, demand = 3200.0, 1.15, 9000.0
    left_capacity = left_mu * wheel_load
    right_capacity = right_mu * wheel_load
    open_each = min(demand / 2.0, left_capacity, right_capacity)
    open_total = 2.0 * open_each
    left_force = min(left_capacity, demand / (1.0 + bias))
    if demand > (1.0 + bias) * left_force:
        left_force = left_capacity
    right_force = bias * left_force
    if not bool(p["broken_mode"]):
        right_force = min(right_force, right_capacity, demand - left_force)
    total = left_force + right_force
    residual = max(
        0.0,
        left_force - left_capacity,
        right_force - right_capacity,
        total - demand,
    )
    return [
        float(open_total),
        float(total),
        float(left_force),
        float(right_force),
        float(residual),
    ]


_REFERENCE_GEARS = np.array((3.60, 2.20, 1.50, 1.15))


def _reference_gear_state(
    speed: float,
    final_drive: float,
    broken: bool,
) -> tuple[int, float, float]:
    rpm_values = (
        speed / 0.31 * _REFERENCE_GEARS * final_drive * 60.0 / (2.0 * np.pi)
    )
    if broken:
        rpm = rpm_values[0]
        limited_rpm = min(rpm, 7000.0)
        torque = max(120.0, 220.0 - 6.0e-6 * (limited_rpm - 4500.0) ** 2)
        return (
            0,
            float(rpm),
            float(torque * _REFERENCE_GEARS[0] * final_drive * 0.92 / 0.31),
        )
    candidates = np.full(4, -np.inf)
    for index, rpm in enumerate(rpm_values):
        if 1500.0 <= rpm <= 7000.0:
            torque = 220.0 - 6.0e-6 * (float(rpm) - 4500.0) ** 2
            candidates[index] = (
                torque * _REFERENCE_GEARS[index] * final_drive * 0.92 / 0.31
            )
    if not np.any(np.isfinite(candidates)):
        selected = int(np.argmin(np.abs(rpm_values - 4250.0)))
        return selected, float(rpm_values[selected]), 0.0
    selected = int(np.argmax(candidates))
    return selected, float(rpm_values[selected]), float(candidates[selected])


def _p47(p: dict[str, Any]) -> list[float]:
    final_drive = float(p["final_drive_ratio"])
    delay = float(p["shift_delay_s"])
    broken = bool(p["broken_mode"])
    step, samples = 0.01, 4001
    time = np.arange(samples) * step
    speed = np.zeros(samples)
    speed[0] = 5.0
    selected, _, _ = _reference_gear_state(speed[0], final_drive, broken)
    interruption = 0.0
    shift_speeds: list[float] = []
    peak_acceleration = 0.0
    max_redline_excess = 0.0
    finish_time = time[-1]
    for index in range(1, samples):
        desired, rpm, force = _reference_gear_state(
            speed[index - 1], final_drive, broken
        )
        max_redline_excess = max(max_redline_excess, rpm - 7000.0)
        if not broken and desired != selected and interruption <= 0.0:
            selected = desired
            interruption = delay
            shift_speeds.append(speed[index - 1])
        if interruption > 0.0:
            force = 0.0
            interruption = max(0.0, interruption - step)
        resistance = 180.0 + 0.38 * speed[index - 1] ** 2
        acceleration = max(0.0, (force - resistance) / 1450.0)
        peak_acceleration = max(peak_acceleration, acceleration)
        speed[index] = speed[index - 1] + acceleration * step
        if speed[index] >= 27.78 and finish_time == time[-1]:
            finish_time = time[index]
    first_shift = shift_speeds[0] * 3.6 if shift_speeds else 0.0
    second_shift = shift_speeds[1] * 3.6 if len(shift_speeds) > 1 else 0.0
    return [
        float(finish_time),
        float(first_shift),
        float(second_shift),
        float(peak_acceleration),
        float(max(0.0, max_redline_excess)),
    ]


def _p48(p: dict[str, Any]) -> list[float]:
    deceleration = float(p["deceleration_g"])
    front_bias = float(p["front_brake_bias"])
    mass, gravity, a, b, height = 1450.0, 9.81, 1.20, 1.50, 0.52
    wheelbase, friction = a + b, 1.10
    transfer = mass * deceleration * gravity * height / wheelbase
    front_dynamic = mass * gravity * b / wheelbase + transfer
    rear_dynamic = mass * gravity * a / wheelbase - transfer
    if bool(p["broken_mode"]):
        front_used = mass * gravity * b / wheelbase
        rear_used = mass * gravity * a / wheelbase
    else:
        front_used, rear_used = front_dynamic, rear_dynamic
    requested = mass * deceleration * gravity
    front_force = min(front_bias * requested, friction * front_used)
    rear_force = min((1.0 - front_bias) * requested, friction * rear_used)
    front_utilization = front_force / (friction * front_dynamic)
    rear_utilization = rear_force / (friction * rear_dynamic)
    achieved = (front_force + rear_force) / (mass * gravity)
    residual = max(0.0, front_utilization - 1.0, rear_utilization - 1.0)
    residual *= mass * gravity
    return [
        float(front_dynamic),
        float(front_dynamic / (mass * gravity)),
        float(front_utilization),
        float(rear_utilization),
        float(achieved),
        float(residual),
    ]


def _p49(p: dict[str, Any]) -> list[float]:
    target = float(p["target_slip"])
    requested_torque = float(p["brake_torque_nm"])
    broken = bool(p["broken_mode"])
    mass, inertia, radius, gravity = 360.0, 1.20, 0.31, 9.81
    peak_force = 1.05 * mass * gravity
    step, samples = 0.002, 2001
    time = np.arange(samples, dtype=float) * step
    speed = np.empty(samples)
    wheel_speed = np.empty(samples)
    slip = np.empty(samples)
    speed[0], wheel_speed[0], slip[0] = 30.0, 30.0 / radius, 0.0
    stopping_distance = 0.0
    maximum_residual = 0.0
    for index in range(1, samples):
        prior_slip = max(
            0.0,
            (speed[index - 1] - radius * wheel_speed[index - 1])
            / max(speed[index - 1], 0.5),
        )
        normalized_slip = prior_slip / target
        tire_force = (
            peak_force * normalized_slip * np.exp(1.0 - normalized_slip)
            if prior_slip > 0.0
            else 0.0
        )
        tire_force = max(0.0, float(tire_force))
        vehicle_acceleration = -tire_force / mass
        if broken:
            brake_torque = requested_torque
        else:
            requested_rate = 10.0 * (target - prior_slip)
            brake_torque = np.clip(
                tire_force * radius
                + inertia
                / radius
                * (
                    speed[index - 1] * requested_rate
                    - (1.0 - prior_slip) * vehicle_acceleration
                ),
                0.0,
                requested_torque,
            )
        wheel_acceleration = (tire_force * radius - brake_torque) / inertia
        unconstrained_wheel_speed = (
            wheel_speed[index - 1] + step * wheel_acceleration
        )
        wheel_speed[index] = max(0.0, unconstrained_wheel_speed)
        speed[index] = max(0.1, speed[index - 1] + step * vehicle_acceleration)
        stopping_distance += 0.5 * step * (speed[index - 1] + speed[index])
        slip[index] = np.clip(
            (speed[index] - radius * wheel_speed[index]) / max(speed[index], 0.5),
            0.0,
            1.0,
        )
        actual_wheel_acceleration = (
            wheel_speed[index] - wheel_speed[index - 1]
        ) / step
        if speed[index] > 2.0:
            maximum_residual = max(
                maximum_residual,
                abs(
                    inertia * actual_wheel_acceleration
                    - (tire_force * radius - brake_torque)
                ),
            )
    active = (time >= 0.5) & (speed > 2.0)
    lock = np.any((wheel_speed < 0.5) & (speed > 2.0))
    return [
        float(np.max(slip[speed > 2.0])),
        float(np.mean(np.abs(slip[active] - target))),
        float(speed[0] - speed[-1]),
        float(stopping_distance),
        float(lock),
        float(maximum_residual),
    ]


def _p50(p: dict[str, Any]) -> list[float]:
    stop_energy = 1000.0 * float(p["stop_energy_kj"])
    cooling = float(p["cooling_coefficient_w_k"])
    broken = bool(p["broken_mode"])
    absorbed_fraction, capacity = 0.75, 45000.0
    ambient, interval, step = 25.0, 45.0, 0.25
    stops, cooling_steps = 6, int(interval / step)
    temperature = ambient
    rejected = 0.0
    input_energy = 0.0
    peak_temperature = temperature
    for _ in range(stops):
        absorbed = absorbed_fraction * stop_energy
        input_energy += absorbed
        temperature += absorbed / capacity
        peak_temperature = max(peak_temperature, temperature)
        for _ in range(cooling_steps):
            heat_loss = cooling * (temperature - ambient)
            rejected += heat_loss * step
            if not broken:
                temperature -= heat_loss * step / capacity
    fade_factor = np.clip(
        1.0 - 0.0018 * max(0.0, peak_temperature - 350.0),
        0.45,
        1.0,
    )
    stored = capacity * (temperature - ambient)
    return [
        float(peak_temperature),
        float(temperature),
        float(rejected / 1000.0),
        float(fade_factor),
        float(abs(input_energy - stored - rejected) / 1000.0),
    ]


def _reference_aero_forces(
    speed: float,
    height_mm: float,
    broken: bool,
) -> tuple[float, float, float]:
    height = height_mm if broken else height_mm / 1000.0
    front_coefficient = 0.58 - 2.2 * (height - 0.080)
    rear_coefficient = 0.72
    drag_coefficient = 0.34 + 0.06 * (front_coefficient + rear_coefficient)
    pressure_area = 0.5 * 1.225 * 2.0 * speed**2
    return (
        pressure_area * front_coefficient,
        pressure_area * rear_coefficient,
        pressure_area * drag_coefficient,
    )


def _p51(p: dict[str, Any]) -> list[float]:
    speed = float(p["speed_m_s"])
    height_mm = float(p["front_ride_height_mm"])
    front, rear, drag = _reference_aero_forces(
        speed,
        height_mm,
        bool(p["broken_mode"]),
    )
    total = front + rear
    balance = front / total if abs(total) > 1.0e-12 else 0.0
    pitch_moment = rear * 1.50 - front * 1.20
    physical_front = _reference_aero_forces(speed, height_mm, False)[0]
    return [
        float(front),
        float(rear),
        float(drag),
        float(balance),
        float(pitch_moment),
        float(abs(front - physical_front)),
    ]


def _p52(p: dict[str, Any]) -> list[float]:
    speed = float(p["speed_m_s"])
    energy_mj = float(p["stint_energy_mj"])
    broken = bool(p["broken_mode"])
    mass, gravity, lap_length = 1450.0, 9.81, 4200.0
    pressure_area = 0.5 * 1.225 * 2.0 * speed**2
    downforce = 1.30 * pressure_area
    drag = 0.42 * pressure_area
    used_downforce = 2.0 * downforce if broken else downforce
    reference_load = mass * gravity
    tire_capacity = 1.22 * reference_load * (
        (reference_load + used_downforce) / reference_load
    ) ** 0.86
    power_force = 210000.0 / speed
    tractive_force = min(tire_capacity, power_force)
    used_drag = 0.0 if broken else drag
    usable_acceleration = max(0.0, (tractive_force - used_drag) / mass)
    lap_energy = (3.60e6 + used_drag * lap_length) / 1.0e6
    thermal_laps = 34.0 / (1.0 + 0.00012 * downforce + 0.00008 * drag)
    stint_laps = min(energy_mj / lap_energy, thermal_laps)
    physical_capacity = 1.22 * reference_load * (
        (reference_load + downforce) / reference_load
    ) ** 0.86
    physical_force = min(physical_capacity, power_force)
    physical_acceleration = max(0.0, (physical_force - drag) / mass)
    physical_lap_energy = (3.60e6 + drag * lap_length) / 1.0e6
    physical_stint = min(energy_mj / physical_lap_energy, thermal_laps)
    residual = abs(usable_acceleration - physical_acceleration) + abs(
        stint_laps - physical_stint
    )
    return [
        float(downforce),
        float(drag),
        float(usable_acceleration),
        float(lap_energy),
        float(stint_laps),
        float(residual),
    ]


def _encode_u16(value: float) -> tuple[int, int]:
    integer = round(value)
    return integer, ((integer & 255) << 8) + (integer >> 8)


def _p53(p: dict[str, Any]) -> list[float]:
    limit = round(float(p["record_limit"]))
    scale = float(p["engine_scale_rpm_count"])
    broken = bool(p["broken_mode"])
    engine_decoded: list[float] = []
    engine_expected: list[float] = []
    wheel_decoded: list[float] = []
    wheel_expected: list[float] = []
    sequence = 0
    for tick in range(101):
        time = 0.02 * tick
        for identifier, divisor in (
            (0x118, 2),
            (0x139, 1),
            (0x241, 2),
            (0x2D2, 3),
            (0x390, 5),
            (0x710, 2),
        ):
            if tick % divisor:
                continue
            if sequence >= limit:
                residuals = np.concatenate(
                    (
                        np.asarray(engine_decoded) - engine_expected,
                        np.asarray(wheel_decoded) - wheel_expected,
                    )
                )
                return [
                    float(limit),
                    float(engine_decoded[-1]),
                    float(np.mean(wheel_decoded)),
                    0.0,
                    1.0,
                    float(np.sqrt(np.mean(residuals**2))),
                ]
            if identifier == 0x118:
                rpm = 2600.0 + 900.0 * time if time <= 1.15 else 3635.0 - 700.0 * (time - 1.15)
                big, little = _encode_u16(4.0 * np.clip(rpm, 0.0, 16000.0))
                raw = little if broken else big
                engine_decoded.append(raw * scale)
                engine_expected.append(big / 4.0)
            elif identifier == 0x139:
                center = 36.0 + 15.0 * time if time <= 1.2 else 54.0 - 10.0 * (time - 1.2)
                turn = np.sin(np.pi * time / 2.0)
                slip = 0.7 if time < 1.0 else 0.0
                speeds = (
                    center - 0.35 * turn,
                    center + 0.35 * turn,
                    center - 0.45 * turn + slip,
                    center + 0.45 * turn + slip,
                )
                encoded = [_encode_u16(128.0 * np.clip(value, 0.0, 511.99)) for value in speeds]
                wheel_decoded.append(float(np.mean([(little if broken else big) / 128.0 for big, little in encoded])))
                wheel_expected.append(float(np.mean([big / 128.0 for big, _ in encoded])))
            sequence += 1
    raise AssertionError("record limit exceeds independent fixture schedule")


def _p54(p: dict[str, Any]) -> list[float]:
    offset = float(p["clock_offset_ms"]) / 1000.0
    period = round(float(p["drop_period"]))
    reference_time = np.arange(101, dtype=float) * 0.02
    truth = np.sin(2.0 * np.pi * 0.7 * reference_time) + 0.2 * np.cos(2.0 * np.pi * 1.3 * reference_time)
    source_time = reference_time + offset
    keep = np.ones(reference_time.size, dtype=bool)
    keep[period::period] = False
    observed_time = source_time[keep]
    aligned_time = observed_time if bool(p["broken_mode"]) else observed_time - offset
    reconstructed = np.interp(reference_time, aligned_time, truth[keep])
    recovered_offset = 0.0 if bool(p["broken_mode"]) else offset
    return [
        1000.0 * recovered_offset,
        float(np.count_nonzero(~keep)),
        float(reference_time.size),
        1000.0 * float(np.max(np.diff(aligned_time))),
        float(np.sqrt(np.mean((reconstructed - truth) ** 2))),
        1000.0 * abs(recovered_offset - offset),
    ]


def _p55(p: dict[str, Any]) -> list[float]:
    bias = float(p["yaw_bias_deg_s"])
    mounting = float(p["mounting_yaw_deg"])
    broken = bool(p["broken_mode"])
    truth = np.array((1.20, 4.50))
    sensor_bias = np.array((0.15, -0.10))
    sensor_scale = np.array((1.04, 0.97))
    measured = sensor_scale * _rotation(-np.deg2rad(mounting)).dot(truth) + sensor_bias
    used_angle = mounting if broken else np.deg2rad(mounting)
    used_vector = measured if broken else (measured - sensor_bias) / sensor_scale
    body = _rotation(used_angle).dot(used_vector)
    yaw = 12.0 + bias if broken else 12.0
    return [
        float(body[0]),
        float(body[1]),
        yaw,
        float(abs(np.linalg.norm(body) - np.linalg.norm(used_vector))),
        float(np.linalg.norm(body - truth) + abs(yaw - 12.0)),
    ]


def _p56(p: dict[str, Any]) -> list[float]:
    initial = float(p["initial_heading_deg"])
    blend = float(p["gps_blend"])
    broken = bool(p["broken_mode"])
    step, samples = 0.05, 241
    time = np.arange(samples, dtype=float) * step
    speed = 15.0 + 2.0 * np.sin(0.35 * time)
    yaw_deg_s = 8.0 * np.sin(0.28 * time) + 1.5
    truth_x, truth_y, truth_heading = np.zeros(samples), np.zeros(samples), np.zeros(samples)
    truth_heading[0] = np.deg2rad(initial)
    for index in range(1, samples):
        truth_heading[index] = truth_heading[index - 1] + np.deg2rad(yaw_deg_s[index - 1]) * step
        truth_x[index] = truth_x[index - 1] + speed[index - 1] * np.cos(truth_heading[index - 1]) * step
        truth_y[index] = truth_y[index - 1] + speed[index - 1] * np.sin(truth_heading[index - 1]) * step
    gps_x = truth_x + 0.40 * np.sin(0.9 * time)
    gps_y = truth_y + 0.35 * np.cos(0.7 * time)
    x, y, heading = np.zeros(samples), np.zeros(samples), np.zeros(samples)
    heading[0] = initial if broken else np.deg2rad(initial)
    for index in range(1, samples):
        yaw = yaw_deg_s[index - 1] if broken else np.deg2rad(yaw_deg_s[index - 1])
        heading[index] = heading[index - 1] + yaw * step
        x_predict = x[index - 1] + speed[index - 1] * np.cos(heading[index - 1]) * step
        y_predict = y[index - 1] + speed[index - 1] * np.sin(heading[index - 1]) * step
        x[index] = x_predict + blend * (gps_x[index] - x_predict) * step
        y[index] = y_predict + blend * (gps_y[index] - y_predict) * step
    return [
        float(x[-1]),
        float(y[-1]),
        float(heading[-1] if broken else np.rad2deg(heading[-1])),
        float(np.sum(speed[:-1]) * step),
        float(np.hypot(x[-1] - truth_x[-1], y[-1] - truth_y[-1])),
        float(np.sqrt(np.mean((x - truth_x) ** 2 + (y - truth_y) ** 2))),
    ]


def _p57(p: dict[str, Any]) -> list[float]:
    gain = float(p["observer_gain"])
    noise = float(p["measurement_noise"])
    step, samples = 0.02, 301
    time = np.arange(samples, dtype=float) * step
    matrix = np.array(((-1.10, -0.35, 0.20), (0.80, -1.60, 0.10), (0.0, 0.0, -0.25)))
    vector = np.array((0.70, 1.30, 0.12))
    steering = 0.045 * np.sin(0.85 * time) + 0.018 * np.sin(1.90 * time)
    truth = np.zeros((samples, 3), dtype=float)
    for index in range(1, samples):
        truth[index] = truth[index - 1] + step * (matrix.dot(truth[index - 1]) + vector * steering[index - 1])
    pattern = np.column_stack((np.sin(2.7 * time) + 0.35 * np.cos(5.1 * time), np.cos(2.2 * time) - 0.25 * np.sin(4.6 * time), 0.45 * np.sin(1.4 * time)))
    measured = truth + noise * pattern
    if bool(p["broken_mode"]):
        measured[:, 0] *= -1.0
    estimate, innovation = np.zeros_like(truth), np.zeros_like(truth)
    covariance = np.eye(3) * 0.25
    used_gain = np.diag((gain, 0.75 * gain, 0.45 * gain))
    for index in range(1, samples):
        predicted = estimate[index - 1] + step * (matrix.dot(estimate[index - 1]) + vector * steering[index - 1])
        innovation[index] = measured[index] - predicted
        estimate[index] = predicted + used_gain.dot(innovation[index])
        covariance = (np.eye(3) - used_gain).dot(covariance + np.diag((2.0e-5, 4.0e-5, 1.0e-5)))
    error = estimate - truth
    return [
        float(np.rad2deg(estimate[-1, 0])),
        float(np.rad2deg(estimate[-1, 1])),
        float(np.rad2deg(estimate[-1, 2])),
        float(np.rad2deg(np.sqrt(np.mean(error[:, 0] ** 2)))),
        float(np.rad2deg(np.sqrt(np.mean(error[:, 1] ** 2)))),
        float(np.trace(covariance)),
        float(np.sqrt(np.mean(innovation**2))),
    ]


def _p58(p: dict[str, Any]) -> list[float]:
    fraction, noise = float(p["training_fraction"]), float(p["observation_noise_n"])
    index = np.arange(80, dtype=float)
    matrix = np.column_stack((0.032 * np.sin(0.19 * index) + 0.011 * np.cos(0.47 * index), 0.025 * np.cos(0.17 * index) - 0.009 * np.sin(0.41 * index)))
    observed = matrix.dot(np.array((80000.0, 70000.0))) + noise * (np.sin(1.73 * index) + 0.4 * np.cos(0.63 * index))
    train_count = round(80 * fraction)
    fit_matrix = matrix if bool(p["broken_mode"]) else matrix[:train_count]
    fit_observed = observed if bool(p["broken_mode"]) else observed[:train_count]
    estimate = np.linalg.lstsq(fit_matrix, fit_observed, rcond=None)[0]
    predicted = matrix.dot(estimate)
    train_rmse = float(np.sqrt(np.mean((predicted[:train_count] - observed[:train_count]) ** 2)))
    validation_rmse = train_rmse if bool(p["broken_mode"]) else float(np.sqrt(np.mean((predicted[train_count:] - observed[train_count:]) ** 2)))
    return [float(estimate[0]), float(estimate[1]), train_rmse, validation_rmse, float(train_count), float(80 - train_count if bool(p["broken_mode"]) else 0)]


def _p59(p: dict[str, Any]) -> list[float]:
    excitation, sigma = float(p["excitation_level"]), float(p["noise_sigma_n"])
    index = np.arange(60, dtype=float)
    matrix = np.column_stack((excitation * (0.030 * np.sin(0.25 * index) + 0.008 * np.cos(0.53 * index)), excitation * (0.028 * np.sin(0.25 * index + 0.16) + 0.004 * np.cos(0.91 * index))))
    truth = np.array((78000.0, 68000.0))
    observed = matrix.dot(truth) + sigma * (0.75 * np.sin(1.31 * index) + 0.35 * np.cos(0.29 * index))
    estimate, _, _, singular = np.linalg.lstsq(matrix, observed, rcond=None)
    residual = observed - matrix.dot(estimate)
    used_sigma = 0.10 * sigma if bool(p["broken_mode"]) else sigma
    covariance = used_sigma**2 * (np.linalg.inv(matrix.T.dot(matrix)) if bool(p["broken_mode"]) else np.linalg.pinv(matrix.T.dot(matrix)))
    standard = np.sqrt(np.diag(covariance))
    physical_covariance = sigma**2 * np.linalg.pinv(matrix.T.dot(matrix))
    return [float(singular[0] / singular[-1]), float(singular[-1]), float(np.sqrt(np.mean(residual**2))), float(np.corrcoef(residual[:-1], residual[1:])[0, 1]), float(np.mean(standard)), float(np.mean(np.abs(estimate - truth) <= 1.96 * standard)), float(np.linalg.norm(covariance - physical_covariance))]


def _p60(p: dict[str, Any]) -> list[float]:
    limit = round(float(p["inspection_limit"]))
    window = round(float(p["reorder_window"]))
    missing = int(limit > 37) + int(limit > 89)
    duplicates = int(limit > 52)
    inversion = int(limit > 72)
    malformed = int(limit > 89)
    corrupted_count = limit - int(limit > 37) + duplicates
    recovered = limit - missing - int(inversion and window < 1)
    if bool(p["broken_mode"]):
        residual = 2 + 1 + 1 + 1 + abs(corrupted_count - (limit - 2)) + 1
        return [0.0, 0.0, 0.0, 0.0, float(corrupted_count), 0.0, float(residual)]
    return [float(missing), float(duplicates), float(inversion), float(malformed), float(recovered), 1.0, 0.0]


def _p61(p: dict[str, Any]) -> list[float]:
    a = float(p["major_radius_m"])
    b = 0.6 * a
    n = round(float(p["point_count"]))
    theta = np.linspace(0, (1.8 if p["broken_mode"] else 2) * np.pi, n)
    curvature = a * b / (a * a * np.sin(theta) ** 2 + b * b * np.cos(theta) ** 2) ** 1.5
    # Chord length via half-angle ellipse identity, not differenced xy arrays.
    mid = (theta[1:] + theta[:-1]) / 2
    ds = (
        2
        * np.sin(np.diff(theta) / 2)
        * np.sqrt(a * a * np.sin(mid) ** 2 + b * b * np.cos(mid) ** 2)
    )
    angle = np.unwrap(np.angle(-a * np.sin(theta) + 1j * b * np.cos(theta)))
    closure = abs(a * (np.cos(theta[-1]) - 1) + 1j * b * np.sin(theta[-1]))
    total = sum(
        float(ds[i]) * (curvature[i] + curvature[i + 1]) / 2 for i in range(n - 1)
    )
    return [
        float(sum(ds)),
        float(max(curvature)),
        float(sum(curvature) / n),
        float((angle[-1] - angle[0]) * 180 / np.pi),
        float(closure),
        float(abs(total - 2 * np.pi)),
    ]


def _p62(p: dict[str, Any]) -> list[float]:
    speed = float(p["speed_m_s"])
    friction = float(p["friction_coefficient"])
    down = 0.5 * 1.225 * 2 * 1.25 * speed**2
    drag = 0.5 * 1.225 * 2 * 0.36 * speed**2
    normal = 1450 * 9.81 + down
    limit = friction * normal
    available = limit if speed == 0 else min(limit, 210000 / speed)
    lateral = (0.9 if p["broken_mode"] else 0.6) * limit
    longitudinal = 0.9 * limit if p["broken_mode"] else min(0.6 * limit, available)
    residual = max(0.0, np.sqrt(longitudinal**2 + lateral**2) / limit - 1)
    return [
        (available - drag) / 1450,
        (limit + drag) / 1450,
        limit / 1450,
        down,
        drag,
        float(residual),
    ]


def _p63(p: dict[str, Any]) -> list[float]:
    bound = float(p["maximum_offset_m"])
    penalty = float(p["smoothness_weight"])
    measures = []
    for index in range(256):
        angle = (index + 0.5) * 2 * np.pi / 256
        tangent = (180**2 * np.sin(angle) ** 2 + 90**2 * np.cos(angle) ** 2) ** 0.5
        measures.append((tangent * 2 * np.pi / 256, 16200 / tangent**3))

    def evaluate(offset):
        lengths = [ds * (1 - offset * k) for ds, k in measures]
        curves = [k / (1 - offset * k) for _, k in measures]
        velocities = [(11.5 / k) ** 0.5 for k in curves]
        time = sum(length / v for length, v in zip(lengths, velocities))
        return time, sum(lengths), max(curves), min(velocities)

    candidates = [-bound + index * (2 * bound / 40) for index in range(41)]
    chosen = min(
        candidates, key=lambda value: evaluate(value)[0] + penalty * value * value
    )
    if p["broken_mode"]:
        chosen = 1.2 * bound
    time, length, peak, minimum = evaluate(chosen)
    return [
        chosen,
        float(length),
        float(peak),
        float(minimum),
        float(evaluate(0)[0] - time),
        bound - abs(chosen),
        max(0.0, abs(chosen) - bound),
    ]


def _p64(p: dict[str, Any]) -> list[float]:
    # Simultaneous Jacobi reachability, independently of production in-place passes.
    grip = float(p["grip_scale"])
    budget = float(p["energy_limit_mj"]) * 1e6
    angle = (np.arange(128) + 0.5) * 2 * np.pi / 128
    tangent = np.sqrt(180**2 * np.sin(angle) ** 2 + 90**2 * np.cos(angle) ** 2)
    distance = tangent * 2 * np.pi / 128
    curvature = 16200 / tangent**3
    reserve = 0.5 * grip * 1450 * 9.81
    rolling = 0.012 * 1450 * 9.81
    square = np.minimum(np.sqrt(3) * reserve / (1450 * curvature), 5184.0)
    for _ in range(1024):
        drive = np.minimum(reserve, 210000 / np.maximum(np.sqrt(square), 1e-9))
        downstream = square + 2 * distance * (drive - 0.441 * square - rolling) / 1450
        candidate = np.minimum(square, np.roll(np.maximum(0, downstream), 1))
        if not p["broken_mode"]:
            upstream = (
                np.roll(square, -1) + 2 * distance * (reserve + rolling) / 1450
            ) / (1 - 2 * distance * 0.441 / 1450)
            candidate = np.minimum(candidate, upstream)
        if np.max(abs(candidate - square)) < 1e-11:
            square = candidate
            break
        square = candidate
    else:
        raise ValueError("Independent cyclic solver failed convergence")
    # E(beta) is piecewise linear. Solve on its active positive-work segments.
    coefficient = (
        0.5 * 1450 * (np.roll(square, -1) - square) + 0.441 * square * distance
    )
    constant = rolling * distance
    feasible = budget >= sum(constant)
    if not feasible:
        beta = 0.0
    elif sum(np.maximum(coefficient + constant, 0)) <= budget:
        beta = 1.0
    else:
        breakpoints = sorted(
            {
                0.0,
                1.0,
                *[
                    float(-b / a)
                    for a, b in zip(coefficient, constant)
                    if a < 0 and 0 < -b / a < 1
                ],
            }
        )
        beta = None
        for interval in range(len(breakpoints)-1):
            left, right = breakpoints[interval:interval+2]
            active = coefficient * ((left + right) / 2) + constant > 0
            slope = sum(coefficient[active])
            intercept = sum(constant[active])
            if slope > 0:
                root = (budget - intercept) / slope
                if left - 1e-12 <= root <= right + 1e-12:
                    beta = float(np.clip(root, 0, 1))
                    break
        if beta is None:
            raise ValueError("No energy-budget root")
    square *= beta
    speed = np.sqrt(square)
    work = (
        0.5 * 1450 * (np.roll(square, -1) - square)
        + (0.441 * square + rolling) * distance
    )
    force = work / distance
    excess = max(
        0.0,
        float(max(force - np.minimum(reserve, 210000 / np.maximum(speed, 1e-9)))),
        float(max(-force - reserve)),
    )
    time = float(sum(distance / speed)) if feasible and min(speed) > 0 else 0.0
    return [
        time,
        float(min(speed)),
        float(max(speed)),
        float(sum(np.maximum(work, 0)) / 1e6),
        float(20 + sum(np.maximum(-work, 0)) / 16000),
        excess,
    ]


def _p65(p: dict[str, Any]) -> list[float]:
    a = float(p["aero_scale"])
    t = float(p["tire_scale"])
    points = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    def response(x, y):
        return 90 - 2 * a * x - 3 * t * y - 1.2 * a * t * x * y

    observed = [response(x, y) for x, y in points]
    if p["broken_mode"]:
        intercept = (observed[0] + observed[3]) / 2
        c1 = c2 = (observed[3] - observed[0]) / 4
        interaction = 0.0
        rank = 2
    else:
        intercept = sum(observed) / 4
        c1 = sum(x * z for (x, _), z in zip(points, observed)) / 4
        c2 = sum(y * z for (_, y), z in zip(points, observed)) / 4
        interaction = sum(x * y * z for (x, y), z in zip(points, observed)) / 4
        rank = 4

    def error(x, y):
        return intercept + c1 * x + c2 * y + interaction * x * y - response(x, y)

    rms = (sum(error(x, y) ** 2 for x, y in points) / 4) ** 0.5
    unused = [(-0.5, 0.25), (0.25, -0.5), (0.5, 0.5)]
    held = (sum(error(x, y) ** 2 for x, y in unused) / len(unused)) ** 0.5
    return [
        round(float(v), 12)
        for v in [-2 * c1, -2 * c2, -4 * interaction, rms, min(observed), rank, held]
    ]


def _p66(p: dict[str, Any]) -> list[float]:
    # Raw bytes shared as inputs only. Manual decoding, two-point transforms,
    # scalar trajectory and explicit 2x2 least squares are independent oracles.
    folder = Path(__file__).resolve().parent / "fixtures"
    metadata = json.loads((folder / "manifest.json").read_text())
    can = [
        json.loads(row)
        for row in (folder / "gr86-can-replay-v1.jsonl").read_text().splitlines()
    ]
    ble = [
        json.loads(row)
        for row in (folder / "racechrono-ble-replay-v1.jsonl").read_text().splitlines()
    ]
    hash_errors = sum(
        hashlib.sha256((folder / e["path"]).read_bytes()).hexdigest() != e["sha256"]
        for e in metadata["files"][:2]
    )
    canonical = {
        r["sequence"]: (
            r["source_time_us"],
            int(r["can_id"], 16),
            r["data_hex"].upper(),
        )
        for r in can
    }

    def parts(row):
        text = row["payload_hex"]
        octets = [int(text[i : i + 2], 16) for i in range(0, len(text), 2)]
        return sum(octets[i] * 256**i for i in range(4)), octets[4:]

    def defects(records):
        count = 0
        seen = set()
        for r in records:
            clock, identifier, payload = canonical[r["sequence"]]
            decoded, data = parts(r)
            count += int(
                r["sequence"] in seen
                or clock != r["source_time_us"]
                or identifier != decoded
                or "".join(f"{b:02X}" for b in data) != payload
            )
            seen.add(r["sequence"])
        return count

    provenance = (
        hash_errors
        + defects(ble)
        + int(metadata["measured_vehicle_data"] is not False)
        + int(metadata["provenance_class"] != "synthetic_protocol_fixture")
    )
    faulty = [dict(r) for r in ble]
    wheel_indices = [i for i, r in enumerate(can) if int(r["can_id"], 16) == 313]
    severity = float(p["fault_severity"])
    broken = p["broken_mode"]
    for i in [wheel_indices[10]] + ([wheel_indices[50]] if severity > 1.4 else []):
        text = faulty[i]["payload_hex"]
        faulty[i]["payload_hex"] = (
            text[:8] + f"{int(text[8:10], 16) ^ 4:02X}" + text[10:]
        )
    faulty.insert(wheel_indices[20], dict(faulty[wheel_indices[20]]))
    faults = defects(faulty)
    records = (
        faulty
        if broken
        else [
            {
                "sequence": key,
                "source_time_us": value[0],
                "payload_hex": "".join(
                    f"{(value[1] >> (8 * i)) & 255:02X}" for i in range(4)
                )
                + value[2],
            }
            for key, value in sorted(canonical.items())
        ]
    )
    unresolved = defects(records)

    def decode(rows):
        speeds = {}
        rates = {}
        for r in rows:
            identifier, data = parts(r)
            time = r["source_time_us"] / 1e6
            if identifier == 313:
                speeds[time] = sum(
                    256 * data[i] + data[i + 1] for i in (0, 2, 4, 6)
                ) / (4 * 128 * 3.6)
            if identifier == 722:
                rates[time] = ((256 * data[0] + data[1]) - 32768) * np.pi / 18000
        return (
            sorted(speeds),
            [speeds[t] for t in sorted(speeds)],
            sorted(rates),
            [rates[t] for t in sorted(rates)],
        )

    t, v0, yt, y0 = decode(ble)
    tx, vx, ty, vy = decode(records)
    gain = 1 + 0.0008 * severity
    offset = 0.02 * severity
    first = offset
    last = 2 * gain + offset
    fitted_gain = (last - first) / 2

    def correct_time(values):
        observed = np.asarray(values) * gain + offset
        return observed if broken else (observed - first) / fitted_gain

    clock_residual = max(abs(correct_time([0, 1, 2]) - np.array([0, 1, 2])))
    sensor_gain = 1 + 0.02 * severity
    bias = 0.2 * severity
    low = bias
    high = 30 * sensor_gain + bias

    def correct_speed(values):
        raw = np.asarray(values) * sensor_gain + bias
        return raw if broken else 30 * (raw - low) / (high - low)

    calibration_residual = abs(float(correct_speed([15])[0]) - 15)
    yaw_bias = np.pi / 360 * severity
    calibrated_yaw = np.asarray(vy) + yaw_bias
    if not broken:
        calibrated_yaw -= yaw_bias  # measured zero-rate calibration
    v = np.interp(t, correct_time(tx), correct_speed(vx))
    y = np.interp(t, correct_time(ty), calibrated_yaw)
    true_yaw = np.interp(t, yt, y0)

    def endpoint(vel, rate):
        east = north = heading = 0.0
        for i in range(len(t) - 1):
            dt = t[i + 1] - t[i]
            east += vel[i] * dt * np.cos(heading)
            north += vel[i] * dt * np.sin(heading)
            heading += rate[i] * dt
        return complex(east, north)

    trajectory_error = abs(endpoint(v, y) - endpoint(v0, true_yaw))
    a = [0.0] + [(v[i] - v[i - 1]) / (t[i] - t[i - 1]) for i in range(1, len(t))]
    a0 = [0.0] + [(v0[i] - v0[i - 1]) / (t[i] - t[i - 1]) for i in range(1, len(t))]
    force = [
        1450 * a0[i] + 0.45 * v0[i] ** 2 + 2 * np.sin(0.9 * i) for i in range(len(t))
    ]
    split = int((1 - float(p["validation_fraction"])) * len(t))
    aa = ab = bb = af = bf = 0.0
    for i in range(1, split):
        x, z = a[i], v[i] ** 2
        aa += x * x
        ab += x * z
        bb += z * z
        af += x * force[i]
        bf += z * force[i]
    determinant = aa * bb - ab * ab
    mass = (af * bb - bf * ab) / determinant
    drag = (bf * aa - af * ab) / determinant
    held = (
        sum(
            (mass * a[i] + drag * v[i] ** 2 - force[i]) ** 2
            for i in range(split, len(t))
        )
        / (len(t) - split)
    ) ** 0.5
    information = 1 - abs(ab / (aa * bb) ** 0.5)
    rms = (sum((v[i] - v0[i]) ** 2 for i in range(len(t))) / len(t)) ** 0.5
    recovery = max(abs(v[i] - v0[i]) for i in range(len(t)))
    checks = [
        provenance == 0,
        clock_residual <= 1.1e-9,
        calibration_residual <= 1.1e-9,
        trajectory_error <= 0.05 + 1e-10,
        rms <= 0.01 + 1e-10,
        held <= 20 + 1e-10,
        information >= 0.001 - 1e-10,
        unresolved == 0,
        recovery <= 0.01 + 1e-10,
    ]
    passed = sum(checks)
    return [
        float(passed),
        9.0,
        float(held),
        passed / 9,
        float(faults),
        float(9 - passed),
        float(checks[-1]),
    ]


def _reference_twin(setup, factor, broken):
    # Scalar force balances and Gauss-Seidel passes; no production helpers/data.
    weight = 1450 * 9.81
    reference_load = weight / 4
    calibration_slip = [0.005, 0.01, 0.02, 0.03, 0.12, 0.16]
    calibration_force = [
        min(70000 * x, 1.15 * reference_load) for x in calibration_slip
    ]
    slope = sum(
        x * y for x, y in zip(calibration_slip[:4], calibration_force[:4])
    ) / sum(x * x for x in calibration_slip[:4])
    mu = sum(calibration_force[4:]) / (2 * reference_load)
    fit_error = max(
        abs(min(slope * x, mu * reference_load) - min(70000 * x, 1.15 * reference_load))
        for x in [0.04, 0.07]
    )
    mu *= factor * (1 + 0.3 * setup)
    c = 0.6125 * 0.72 * (1 + setup)
    roll = 0.012 * weight
    ratios = [3.63, 2.19, 1.54, 1.21, 1, 0.77]

    def engine(square):
        speed = square**0.5
        forces = []
        for gear in ratios:
            total = gear * 4.1
            rpm = speed * total * 30 / (np.pi * 0.31)
            if 2000 <= rpm <= 7400:
                torque = float(
                    np.interp(
                        rpm,
                        [2000, 3000, 4000, 5000, 6000, 7000, 7400],
                        [170, 205, 225, 230, 225, 200, 180],
                    )
                )
                forces.append(torque * total * 0.9 / 0.31)
        return max(forces, default=0.0)

    def contact(square, curve, extra):
        aero = 1.53125 * (1 + 2 * setup) * square
        front_total = 0.53 * weight + 0.5 * aero * (1 + int(extra))
        rear_total = 0.47 * weight + 0.5 * aero * (1 + int(extra))
        moved = 1450 * square * curve * 0.5 / 1.52
        fraction = 0.55 + 0.1 * setup
        wheel = [
            front_total / 2 + moved * fraction,
            front_total / 2 - moved * fraction,
            rear_total / 2 + moved * (1 - fraction),
            rear_total / 2 - moved * (1 - fraction),
        ]
        grip = (
            mu
            * reference_load
            * sum((max(0, fz) / reference_load) ** 0.9 for fz in wheel)
        )
        return grip, wheel, aero

    candidates = []
    for offset in np.linspace(-1.5, 1.5, 9):
        curves = []
        lengths = []
        squares = []
        for index in range(96):
            angle = (index + 0.5) * np.pi / 48
            norm = (180**2 * np.sin(angle) ** 2 + 110**2 * np.cos(angle) ** 2) ** 0.5
            curve = 19800 / norm**3
            scale = 1 - offset * curve
            curves.append(curve / scale)
            lengths.append(norm * np.pi / 48 * scale)
            lo, hi = 25.0, 4900.0
            for _ in range(44):
                trial = (lo + hi) / 2
                grip, wheel, _ = contact(trial, curves[-1], broken)
                if 1450 * trial * curves[-1] <= 0.8 * grip and min(wheel) >= 200:
                    lo = trial
                else:
                    hi = trial
            squares.append(lo)
        for iteration in range(1024):
            old = list(squares)
            for i in range(96):
                j = (i + 1) % 96
                grip, _, _ = contact(squares[i], curves[i], broken)
                traction = min(0.6 * grip, engine(squares[i]))
                allowance = (
                    squares[i]
                    + 2 * lengths[i] * (traction - c * squares[i] - roll) / 1450
                )
                squares[j] = min(squares[j], allowance)
            for i in reversed(range(96)):
                j = (i + 1) % 96
                grip, _, _ = contact(squares[i], curves[i], broken)
                braking = min(0.6 * grip, 7500 * (1 + setup))
                allowance = (squares[j] + 2 * lengths[i] * (braking + roll) / 1450) / (
                    1 - 2 * lengths[i] * c / 1450
                )
                squares[i] = min(squares[i], allowance)
            if max(abs(a - b) for a, b in zip(old, squares)) < 1e-10:
                break
        else:
            raise ValueError("Independent twin reachability did not converge")
        time = sum(d / w**0.5 for d, w in zip(lengths, squares))
        utilization = []
        loads = []
        propulsion = []
        reach = []
        heat = 0.0
        ledger = []
        for i in range(96):
            next_w = squares[(i + 1) % 96]
            w = squares[i]
            ds = lengths[i]
            k = curves[i]
            force = 1450 * (next_w - w) / (2 * ds) + c * w + roll
            used, used_wheel, aero = contact(w, k, broken)
            physical, wheel, _ = contact(w, k, False)
            utilization.append((force**2 + (1450 * w * k) ** 2) ** 0.5 / physical)
            loads.extend(wheel)
            propulsion.append(force - engine(w))
            reach.extend(
                [
                    force - min(0.6 * used, engine(w)),
                    -force - min(0.6 * used, 7500 * (1 + setup)),
                ]
            )
            heat += max(0, -force * ds)
            ledger.append(abs(sum(used_wheel) - weight - aero) / (weight + aero))
        candidates.append(
            {
                "time": float(time),
                "offset": float(offset),
                "fit": float(fit_error),
                "util": float(max(utilization)),
                "load": float(min(loads)),
                "propulsion": float(max(0, max(propulsion))),
                "temperature": 20 + heat / 16000,
                "ledger": float(max(ledger)),
                "geometry": float(
                    abs(sum(d * k for d, k in zip(lengths, curves)) - 2 * np.pi)
                ),
                "reach": float(max(0, max(reach))),
            }
        )
    return min(candidates, key=lambda row: row["time"])


def _p67(p: dict[str, Any]) -> list[float]:
    setup = float(p["setup_delta"])
    uncertainty = float(p["uncertainty_fraction"])
    broken = p["broken_mode"]
    current = _reference_twin(setup, 1, broken)
    base = _reference_twin(0, 1, False)
    endpoints = [
        _reference_twin(setup, 1 - uncertainty, broken)["time"],
        _reference_twin(setup, 1 + uncertainty, broken)["time"],
    ]
    clean = _reference_twin(setup, 1, False)
    replay = _reference_twin(setup, 1, False)
    recovery = abs(clean["time"] - replay["time"])
    coverage = max(
        0, min(endpoints) - current["time"], current["time"] - max(endpoints)
    )
    checks = [
        current["fit"] <= 1.01e-8,
        current["util"] <= 1.000001 + 1e-10,
        current["load"] >= 200 - 1e-10,
        current["propulsion"] <= 1e-5 + 1e-10,
        current["temperature"] <= 450 + 1e-10,
        current["ledger"] <= 2e-10,
        current["geometry"] <= 1e-6 + 1e-10,
        abs(current["offset"]) <= 1.5 + 1e-10,
        current["reach"] <= 1e-5 + 1e-10,
        coverage <= 1.01e-8,
        recovery <= 2e-10,
    ]
    return [
        float(sum(checks)),
        11.0,
        current["time"],
        max(endpoints) - min(endpoints),
        base["time"] - current["time"],
        current["ledger"],
        float(checks[-1]),
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
    44: _p44,
    45: _p45,
    46: _p46,
    47: _p47,
    48: _p48,
    49: _p49,
    50: _p50,
    51: _p51,
    52: _p52,
    53: _p53,
    54: _p54,
    55: _p55,
    56: _p56,
    57: _p57,
    58: _p58,
    59: _p59,
    60: _p60,
    61: _p61,
    62: _p62,
    63: _p63,
    64: _p64,
    65: _p65,
    66: _p66,
    67: _p67,
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
