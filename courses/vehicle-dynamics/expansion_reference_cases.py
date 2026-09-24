"""Independent Vehicle Dynamics P25-P33 references.

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
