"""Independent numerical references for the Controls/GNC fidelity audit.

This module never imports a learner-facing ``experiment.py``.  Each reference
uses a closed form, an affine state transition, a continuous high-accuracy
integration, a covariance update with a different algebraic form, or a second
geometric/event algorithm.  Production results are supplied only to the test
comparison layer; no function in this file accepts them as an input.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm, solve_discrete_are
from scipy.optimize import brentq
from scipy.signal import lfilter

ORIGIN = {
    "independent": True,
    "imports_production_entrypoint": False,
    "derived_from_production_output": False,
    "perturbs_production_output": False,
}

REFERENCE_METHODS: dict[int, tuple[str, str, float, float]] = {
    1: (
        "alternative_algorithm",
        "Affine semi-implicit state-transition recurrence",
        1e-10,
        1e-10,
    ),
    2: (
        "closed_form",
        "Analytic integrator/first-order response and Euler recurrence formula",
        1e-10,
        1e-10,
    ),
    3: (
        "closed_form",
        "Complex-pole exponential envelope and phase relation",
        1e-10,
        1e-10,
    ),
    4: (
        "separately_formulated_numerical",
        "High-accuracy continuous nonlinear and linear pendulum integration",
        3e-2,
        3e-2,
    ),
    5: ("closed_form", "Scalar affine closed-loop recurrence", 1e-10, 1e-10),
    6: (
        "alternative_algorithm",
        "Augmented affine PID state-transition recurrence",
        1e-9,
        1e-9,
    ),
    7: (
        "alternative_algorithm",
        "Affine plant recurrence plus root-solved frequency crossover",
        5e-1,
        7e-2,
    ),
    8: (
        "alternative_algorithm",
        "Closed-loop scalar recurrence with analytic sensitivity",
        1e-9,
        1e-9,
    ),
    9: (
        "alternative_algorithm",
        "Augmented sampled-data PI state recurrence",
        1e-10,
        1e-10,
    ),
    10: (
        "alternative_algorithm",
        "Independent sample/compute/apply event state machine",
        1e-10,
        1e-10,
    ),
    11: (
        "closed_form",
        "Continuous clipped first-order plant integration",
        1.5e-2,
        1.5e-2,
    ),
    12: (
        "separately_formulated_numerical",
        "High-accuracy continuous anti-windup state integration",
        2e-2,
        2e-2,
    ),
    13: (
        "closed_form",
        "Direct controllability matrix and finite-horizon Gramian construction",
        1e-12,
        1e-12,
    ),
    14: (
        "closed_form",
        "Direct observability matrix and least-squares reconstruction",
        1e-12,
        1e-12,
    ),
    15: (
        "closed_form",
        "Exact affine observer-error transition from a matrix exponential",
        2e-2,
        2e-2,
    ),
    16: (
        "alternative_algorithm",
        "Joseph-form covariance Kalman recurrence",
        1e-9,
        1e-9,
    ),
    17: ("alternative_algorithm", "Schur-method discrete Riccati solution", 2e-6, 2e-6),
    18: (
        "separately_formulated_numerical",
        "High-accuracy continuous feedforward/feedback integration",
        2e-2,
        2e-2,
    ),
    19: ("closed_form", "Scalar uncertain closed-loop recurrence", 1e-10, 1e-10),
    20: (
        "closed_form",
        "Two fixed-gain scalar recurrences over the declared uncertainty point",
        1e-6,
        4e-2,
    ),
    21: (
        "closed_form",
        "Analytic quintic trajectory and derivative extrema",
        1e-12,
        1e-12,
    ),
    22: (
        "alternative_algorithm",
        "Complex-plane proportional-navigation geometry recurrence",
        1e-8,
        1e-8,
    ),
    23: (
        "alternative_algorithm",
        "Independent convolution/IIR realization of actuator and sensor lags",
        1e-10,
        1e-10,
    ),
    24: (
        "alternative_algorithm",
        "Independent timestamped delivery/watchdog event scheduler",
        1e-10,
        1e-10,
    ),
}


def tolerance(item_number: int) -> dict[str, float]:
    _, _, absolute, relative = REFERENCE_METHODS[item_number]
    return {"absolute": absolute, "relative": relative}


def origin(item_number: int) -> dict[str, Any]:
    kind, formulation, _, _ = REFERENCE_METHODS[item_number]
    return {"type": kind, "formulation": formulation, **ORIGIN}


def _affine_trajectory(
    matrix: np.ndarray,
    offset: np.ndarray,
    initial: np.ndarray,
    steps: int,
) -> np.ndarray:
    states = np.empty((steps, len(initial)), dtype=float)
    states[0] = initial
    for index in range(steps - 1):
        states[index + 1] = matrix @ states[index] + offset
    return states


def _p01(parameters: Mapping[str, Any]) -> np.ndarray:
    mass = float(parameters["mass_kg"])
    damping = float(parameters["damping_ns_m"])
    stiffness = float(parameters["stiffness_n_m"])
    dt = 1.0 if parameters["broken_mode"] else 0.01
    time = np.arange(0.0, 12.0 + dt / 2, dt)
    if parameters["broken_mode"]:
        matrix = np.array(
            [[1.0, dt], [-dt * stiffness / mass, 1 - dt * damping / mass]]
        )
        offset = np.array([0.0, dt / mass])
    else:
        matrix = np.array(
            [
                [1 - dt * dt * stiffness / mass, dt * (1 - dt * damping / mass)],
                [-dt * stiffness / mass, 1 - dt * damping / mass],
            ]
        )
        offset = np.array([dt * dt / mass, dt / mass])
    state = _affine_trajectory(matrix, offset, np.zeros(2), len(time))
    position, velocity = state.T
    energy = 0.5 * mass * velocity**2 + 0.5 * stiffness * position**2
    natural_frequency = np.sqrt(stiffness / mass)
    damping_ratio = damping / (2 * np.sqrt(stiffness * mass))
    return np.array(
        [
            natural_frequency,
            damping_ratio,
            position[-1],
            np.max(np.abs(position)),
            energy[-1],
        ]
    )


def _p02(parameters: Mapping[str, Any]) -> np.ndarray:
    amplitude = float(parameters["input_amplitude"])
    tau = float(parameters["time_constant_s"])
    time = np.linspace(0, 10, 501)
    integrator = amplitude * time
    if parameters["broken_mode"]:
        dt = 3 * tau
        coarse_time = np.arange(0, 10 + dt / 2, dt)
        ratio = 1 - dt / tau
        coarse = amplitude * (1 - ratio ** np.arange(len(coarse_time)))
        first_order = np.interp(time, coarse_time, coarse)
    else:
        first_order = amplitude * (1 - np.exp(-time / tau))
    return np.array(
        [amplitude, tau, integrator[-1], first_order[-1], np.max(np.abs(first_order))]
    )


def _p03(parameters: Mapping[str, Any]) -> np.ndarray:
    real_part = float(parameters["pole_real_per_s"])
    imaginary_part = float(parameters["pole_imag_rad_s"])
    if parameters["broken_mode"]:
        real_part = abs(real_part)
    time = np.linspace(0, 12, 601)
    response = np.exp(real_part * time) * np.cos(imaginary_part * time)
    period = 2 * np.pi / imaginary_part if imaginary_part > 0 else 0.0
    return np.array(
        [real_part, imaginary_part, period, response[-1], np.max(np.abs(response))]
    )


def _p04(parameters: Mapping[str, Any]) -> np.ndarray:
    angle = np.deg2rad(
        120.0 if parameters["broken_mode"] else parameters["initial_angle_deg"]
    )
    length = float(parameters["length_m"])
    time = np.arange(0, 12.0 + 0.005, 0.01)
    omega_squared = 9.81 / length
    damping_ratio = 0.02

    def rhs(_: float, state: np.ndarray, *, nonlinear: bool) -> np.ndarray:
        theta, rate = state
        restoring = np.sin(theta) if nonlinear else theta
        acceleration = -2 * damping_ratio * np.sqrt(omega_squared) * rate
        acceleration -= omega_squared * restoring
        return np.array([rate, acceleration])

    nonlinear = solve_ivp(
        lambda t, x: rhs(t, x, nonlinear=True),
        (time[0], time[-1]),
        [angle, 0.0],
        t_eval=time,
        rtol=1e-10,
        atol=1e-12,
    ).y[0]
    linear = solve_ivp(
        lambda t, x: rhs(t, x, nonlinear=False),
        (time[0], time[-1]),
        [angle, 0.0],
        t_eval=time,
        rtol=1e-10,
        atol=1e-12,
    ).y[0]
    gap = np.max(np.abs(nonlinear - linear))
    return np.array([angle, length, gap, nonlinear[-1], linear[-1]])


def _p05(parameters: Mapping[str, Any]) -> np.ndarray:
    gain = float(parameters["proportional_gain"])
    tau = float(parameters["plant_time_constant_s"])
    sign = 1.0 if parameters["broken_mode"] else -1.0
    dt = 0.01
    steps = len(np.arange(0, 6.0 + dt / 2, dt))
    ratio = 1 + dt * (-1 + gain * sign) / tau
    offset = dt * gain / tau
    indices = np.arange(steps)
    if abs(1 - ratio) < 1e-14:
        output = offset * indices
    else:
        output = offset * (1 - ratio**indices) / (1 - ratio)
    return np.array([gain, tau, sign, output[-1], np.max(np.abs(output))])


def _p06(parameters: Mapping[str, Any]) -> np.ndarray:
    integral_gain = float(parameters["integral_gain"])
    derivative_gain = float(parameters["derivative_gain"])
    if parameters["broken_mode"]:
        derivative_gain = -derivative_gain
    proportional_gain = 4.0
    dt = 0.01
    time = np.arange(0, 20.0 + dt / 2, dt)
    matrix = np.array(
        [
            [
                1 - dt**2 * proportional_gain,
                dt * (1 - dt * (derivative_gain + 0.4)),
                dt**2 * integral_gain,
            ],
            [
                -dt * proportional_gain,
                1 - dt * (derivative_gain + 0.4),
                dt * integral_gain,
            ],
            [-dt, 0.0, 1.0],
        ]
    )
    offset = np.array(
        [dt**2 * (proportional_gain - 1), dt * (proportional_gain - 1), dt]
    )
    state = _affine_trajectory(matrix, offset, np.zeros(3), len(time))
    position, velocity, integral = state.T
    command = proportional_gain * (1 - position) + integral_gain * integral
    command -= derivative_gain * velocity
    return np.array(
        [
            integral_gain,
            derivative_gain,
            position[-1],
            np.max(position),
            np.max(np.abs(command)),
        ]
    )


def _p07(parameters: Mapping[str, Any]) -> np.ndarray:
    gain = 4.0 if parameters["broken_mode"] else float(parameters["loop_gain"])
    lag = 0.5 if parameters["broken_mode"] else float(parameters["actuator_lag_s"])
    dt = 0.005
    time = np.arange(0, 20.0 + dt / 2, dt)
    if lag > 0:
        matrix = np.array(
            [
                [1.0, dt, 0.0],
                [0.0, 1 - dt, dt],
                [-dt * gain / lag, 0.0, 1 - dt / lag],
            ]
        )
        offset = np.array([0.0, 0.0, dt * gain / lag])
    else:
        matrix = np.array([[1.0, dt, 0.0], [0.0, 1 - dt, dt], [-gain, 0.0, 0.0]])
        offset = np.array([0.0, 0.0, gain])
    output = _affine_trajectory(matrix, offset, np.zeros(3), len(time))[:, 0]

    def magnitude(omega: float) -> float:
        lag_factor = np.sqrt(1 + (lag * omega) ** 2)
        return gain / (omega * np.sqrt(1 + omega**2) * lag_factor)

    crossover = brentq(lambda omega: magnitude(omega) - 1, 1e-4, 1e4)
    phase = -90 - np.degrees(np.arctan(crossover))
    phase -= np.degrees(np.arctan(lag * crossover))
    phase_margin = 180 + phase
    return np.array([gain, lag, phase_margin, crossover, np.max(np.abs(output))])


def _p08(parameters: Mapping[str, Any]) -> np.ndarray:
    gain = float(parameters["feedback_gain"])
    frequency = float(parameters["disturbance_frequency_rad_s"])
    bias = 0.5 if parameters["broken_mode"] else 0.0
    dt = 0.005
    time = np.arange(0, 12.0 + dt / 2, dt)
    disturbance = np.where(
        time >= 1,
        np.ones_like(time) if frequency == 0 else np.sin(frequency * (time - 1)),
        0,
    )
    output = np.zeros_like(time)
    ratio = 1 - dt * (1 + gain)
    for index in range(len(time) - 1):
        active_bias = bias if time[index] >= 1 else 0.0
        output[index + 1] = ratio * output[index]
        output[index + 1] += dt * (disturbance[index] - gain * active_bias)
    command = -gain * (output + bias * (time >= 1))
    attenuation = 1 / np.sqrt((1 + gain) ** 2 + frequency**2)
    return np.array(
        [gain, frequency, bias, attenuation, output[-1], np.max(np.abs(command))]
    )


def _p09(parameters: Mapping[str, Any]) -> np.ndarray:
    sample_period = (
        0.3 if parameters["broken_mode"] else float(parameters["sample_period_s"])
    )
    integral_gain = float(parameters["integral_gain"])
    proportional_gain = 2.0
    time = np.arange(0, 12.0 + sample_period / 2, sample_period)
    output = np.zeros_like(time)
    integral = np.zeros_like(time)
    command = np.zeros_like(time)
    plant_ratio = np.exp(-sample_period)
    previous_integral = 0.0
    for index in range(len(time) - 1):
        error = 1 - output[index]
        increment = (
            previous_integral if parameters["broken_mode"] and index > 0 else error
        )
        integral[index + 1] = integral[index] + sample_period * increment
        previous_integral = integral[index]
        command[index] = proportional_gain * error + integral_gain * integral[index]
        output[index + 1] = plant_ratio * output[index]
        output[index + 1] += (1 - plant_ratio) * command[index]
    command[-1] = proportional_gain * (1 - output[-1]) + integral_gain * integral[-1]
    return np.array(
        [
            sample_period,
            integral_gain,
            output[-1],
            np.max(np.abs(output)),
            np.max(np.abs(command)),
        ]
    )


def _p10(parameters: Mapping[str, Any]) -> np.ndarray:
    sample_period = (
        0.2 if parameters["broken_mode"] else float(parameters["sample_period_s"])
    )
    fraction = 0.9 if parameters["broken_mode"] else float(parameters["delay_fraction"])
    delay = sample_period * fraction
    dt = 0.005
    time = np.arange(0, 4.0 + dt / 2, dt)
    output = np.zeros_like(time)
    command = np.zeros_like(time)
    computed = 0.0
    held = 0.0
    next_sample = 0.0
    apply_time = 0.0
    for index, instant in enumerate(time[:-1]):
        if instant + 1e-12 >= next_sample:
            held = command[index - 1] if index else 0.0
            computed = 8 * (1 - output[index])
            apply_time = instant + delay
            next_sample += sample_period
        command[index] = held if instant < apply_time else computed
        output[index + 1] = output[index] + dt * (-output[index] + command[index])
    command[-1] = command[-2]
    return np.array([sample_period, fraction, delay, output[-1], np.max(output)])


def _p11(parameters: Mapping[str, Any]) -> np.ndarray:
    reference = 1.5 if parameters["broken_mode"] else float(parameters["reference"])
    limit = 0.6 if parameters["broken_mode"] else float(parameters["actuator_limit"])
    time = np.arange(0, 6.0 + 0.005, 0.01)

    def rhs(_: float, output: np.ndarray) -> np.ndarray:
        requested = 4 * (reference - output[0])
        return np.array([-output[0] + np.clip(requested, -limit, limit)])

    output = solve_ivp(
        rhs,
        (time[0], time[-1]),
        [0.0],
        t_eval=time,
        rtol=1e-11,
        atol=1e-13,
    ).y[0]
    requested = 4 * (reference - output)
    applied = np.clip(requested, -limit, limit)
    saturated = np.mean(np.abs(requested - applied) > 1e-12)
    return np.array(
        [reference, limit, saturated, output[-1], np.max(np.abs(requested))]
    )


def _p12(parameters: Mapping[str, Any]) -> np.ndarray:
    anti_windup = float(parameters["anti_windup_gain"])
    duration = float(parameters["demand_duration_s"])
    sign = -1.0 if parameters["broken_mode"] else 1.0
    time = np.arange(0, 10.0 + 0.005, 0.01)

    def rhs(instant: float, state: np.ndarray) -> np.ndarray:
        output, integral = state
        reference = 2.0 if instant < duration else -0.5
        error = reference - output
        raw = 2 * error + integral
        command = np.clip(raw, -1, 1)
        return np.array(
            [-output + command, error + sign * anti_windup * (command - raw)]
        )

    state = solve_ivp(
        rhs,
        (time[0], time[-1]),
        [0.0, 0.0],
        t_eval=time,
        rtol=1e-10,
        atol=1e-12,
        max_step=0.005,
    ).y.T
    output, integral = state.T
    reference = np.where(time < duration, 2.0, -0.5)
    post = time >= duration
    recovery_area = np.trapezoid(np.abs(reference[post] - output[post]), time[post])
    return np.array(
        [anti_windup, duration, sign, recovery_area, np.max(np.abs(integral))]
    )


def _p13(parameters: Mapping[str, Any]) -> np.ndarray:
    input_gain = float(parameters["input_gain"])
    coupling = 0.0 if parameters["broken_mode"] else float(parameters["coupling"])
    dt = 0.05
    state = np.array([[1.0, dt * coupling], [0.0, 1.0]])
    input_matrix = np.array([[0.5 * dt**2 * input_gain], [dt * input_gain]])
    controllability = np.hstack([input_matrix, state @ input_matrix])
    rank = float(np.linalg.matrix_rank(controllability))
    gramian = np.zeros((2, 2))
    transition = np.eye(2)
    for _ in range(40):
        mapped = transition @ input_matrix
        gramian += mapped @ mapped.T
        transition = state @ transition
    eigenvalues = np.linalg.eigvalsh(gramian)
    final_position = input_gain * coupling * 0.5 * (40 * dt) ** 2
    return np.array([input_gain, coupling, rank, eigenvalues[0], final_position])


def _p14(parameters: Mapping[str, Any]) -> np.ndarray:
    sensor_gain = float(parameters["sensor_gain"])
    window = float(parameters["observation_window_s"])
    rate_only = bool(parameters["broken_mode"])
    dt = 0.05
    time = np.arange(0, window + dt / 2, dt)
    position0 = 0.8
    rate0 = 0.6
    measurement = sensor_gain * (
        np.full_like(time, rate0) if rate_only else position0 + rate0 * time
    )
    observability = (
        np.array([[0.0, sensor_gain], [0.0, sensor_gain]])
        if rate_only
        else np.array([[sensor_gain, 0.0], [sensor_gain, sensor_gain * dt]])
    )
    rank = float(np.linalg.matrix_rank(observability))
    inferred_rate = (
        0.0
        if rate_only
        else np.linalg.lstsq(
            np.column_stack([time, np.ones_like(time)]), measurement, rcond=None
        )[0][0]
        / sensor_gain
    )
    return np.array(
        [
            sensor_gain,
            window,
            float(rate_only),
            rank,
            inferred_rate,
            np.ptp(measurement),
        ]
    )


def _p15(parameters: Mapping[str, Any]) -> np.ndarray:
    speed = float(parameters["observer_speed_per_s"])
    bias = 0.15 if parameters["broken_mode"] else float(parameters["sensor_bias_m"])
    time = np.arange(0, 8.0 + 0.01, 0.02)
    initial_error = np.array([1.2, -0.5])
    matrix = np.array([[-2 * speed, 1.0], [-(speed**2), 0.0]])
    offset = np.array([-2 * speed * bias, -(speed**2) * bias])
    augmented = np.block(
        [[matrix, offset[:, None]], [np.zeros((1, 2)), np.zeros((1, 1))]]
    )
    initial = np.r_[initial_error, 1.0]
    errors = np.array([(expm(augmented * instant) @ initial)[:2] for instant in time])
    rmse = np.sqrt(np.mean(errors[:, 0] ** 2))
    return np.array([speed, bias, rmse, errors[-1, 0], errors[-1, 1]])


def _p16(parameters: Mapping[str, Any]) -> np.ndarray:
    sensor_noise = float(parameters["assumed_sensor_noise_m"])
    process_noise = float(parameters["assumed_process_noise_m_s2"])
    outlier = 4.0 if parameters["broken_mode"] else 0.0
    dt = 0.05
    time = np.arange(0, 20.0 + dt / 2, dt)
    rng = np.random.default_rng(1601)
    truth = np.column_stack(
        [0.4 * time + 0.8 * np.sin(0.25 * time), 0.4 + 0.2 * np.cos(0.25 * time)]
    )
    measurement = truth[:, 0] + rng.normal(0, 0.35, len(time))
    measurement[len(time) // 2] += outlier
    transition = np.array([[1.0, dt], [0.0, 1.0]])
    observation = np.array([[1.0, 0.0]])
    covariance_noise = process_noise**2 * np.array(
        [[dt**4 / 4, dt**3 / 2], [dt**3 / 2, dt**2]]
    )
    measurement_variance = sensor_noise**2
    estimate = np.zeros_like(truth)
    covariance = np.eye(2)
    identity = np.eye(2)
    for index in range(1, len(time)):
        predicted = transition @ estimate[index - 1]
        predicted_covariance = transition @ covariance @ transition.T + covariance_noise
        innovation = measurement[index] - (observation @ predicted).item()
        innovation_variance = (
            observation @ predicted_covariance @ observation.T
        ).item()
        innovation_variance += measurement_variance
        gain = (predicted_covariance @ observation.T / innovation_variance).ravel()
        estimate[index] = predicted + gain * innovation
        residual_map = identity - np.outer(gain, observation.ravel())
        covariance = residual_map @ predicted_covariance @ residual_map.T
        covariance += np.outer(gain, gain) * measurement_variance
    rmse = np.sqrt(np.mean((truth[:, 0] - estimate[:, 0]) ** 2))
    return np.array([sensor_noise, process_noise, outlier, rmse, estimate[-1, 1]])


def _p17(parameters: Mapping[str, Any]) -> np.ndarray:
    position_weight = float(parameters["position_weight"])
    control_weight = float(parameters["control_weight"])
    effectiveness = 0.0 if parameters["broken_mode"] else 1.0
    dt = 0.02
    state = np.array([[1.0, dt], [0.0, 1 - 0.4 * dt]])
    input_matrix = np.array([[0.5 * dt**2 * effectiveness], [dt * effectiveness]])
    state_cost = np.diag([position_weight, 1.0])
    command_cost = np.array([[control_weight]])
    if effectiveness == 0:
        gain = np.zeros((1, 2))
    else:
        riccati = solve_discrete_are(state, input_matrix, state_cost, command_cost)
        gain = np.linalg.solve(
            command_cost + input_matrix.T @ riccati @ input_matrix,
            input_matrix.T @ riccati @ state,
        )
    time = np.arange(0, 12.0 + dt / 2, dt)
    trajectory = np.zeros((len(time), 2))
    trajectory[0] = [1.0, 0.0]
    command = np.zeros(len(time))
    for index in range(len(time) - 1):
        command[index] = (-gain @ trajectory[index]).item()
        trajectory[index + 1] = (
            state @ trajectory[index] + input_matrix[:, 0] * command[index]
        )
    cost = np.trapezoid(
        position_weight * trajectory[:, 0] ** 2
        + trajectory[:, 1] ** 2
        + control_weight * command**2,
        time,
    )
    return np.array(
        [
            position_weight,
            control_weight,
            effectiveness,
            gain[0, 0],
            np.max(np.abs(command)),
            cost,
        ]
    )


def _p18(parameters: Mapping[str, Any]) -> np.ndarray:
    feedforward = float(parameters["feedforward_scale"])
    feedback = float(parameters["feedback_scale"])
    sign = -1.0 if parameters["broken_mode"] else 1.0
    time = np.arange(0, 12.0 + 0.01, 0.02)

    def demand(instant: float) -> tuple[float, float, float, float]:
        position = np.sin(0.5 * instant)
        velocity = 0.5 * np.cos(0.5 * instant)
        acceleration = -0.25 * np.sin(0.5 * instant)
        disturbance = -0.4 if instant >= 6 else 0.0
        return position, velocity, acceleration, disturbance

    def rhs(instant: float, state: np.ndarray) -> np.ndarray:
        desired_position, desired_velocity, desired_acceleration, disturbance = demand(
            instant
        )
        command = sign * feedforward * desired_acceleration
        command += feedback * (
            4 * (desired_position - state[0]) + 3 * (desired_velocity - state[1])
        )
        return np.array([state[1], command + disturbance])

    state = solve_ivp(
        rhs,
        (time[0], time[-1]),
        [0.0, 0.0],
        t_eval=time,
        rtol=1e-10,
        atol=1e-12,
        max_step=0.01,
    ).y.T
    desired_position = np.sin(0.5 * time)
    desired_velocity = 0.5 * np.cos(0.5 * time)
    desired_acceleration = -0.25 * np.sin(0.5 * time)
    command = sign * feedforward * desired_acceleration
    command += feedback * (
        4 * (desired_position - state[:, 0]) + 3 * (desired_velocity - state[:, 1])
    )
    error = desired_position - state[:, 0]
    rmse = np.sqrt(np.mean(error**2))
    return np.array([feedforward, feedback, sign, rmse, np.max(np.abs(command))])


def _scalar_closed_loop(
    gain: float, drag: float, sign: float, controller: float, steps: int
) -> np.ndarray:
    dt = 0.02
    ratio = 1 - dt * (drag + sign * gain * controller)
    offset = dt * sign * gain * controller
    indices = np.arange(steps)
    if abs(1 - ratio) < 1e-14:
        return offset * indices
    return offset * (1 - ratio**indices) / (1 - ratio)


def _p19(parameters: Mapping[str, Any]) -> np.ndarray:
    gain = float(parameters["actuator_gain_ratio"])
    drag = float(parameters["drag_ratio"])
    sign = -1.0 if parameters["broken_mode"] else 1.0
    time = np.arange(0, 10.0 + 0.01, 0.02)
    actual = _scalar_closed_loop(gain, drag, sign, 2.0, len(time))
    nominal = _scalar_closed_loop(1.0, 1.0, 1.0, 2.0, len(time))
    gap = np.max(np.abs(actual - nominal))
    return np.array([gain, drag, sign, gap, actual[-1]])


def _p20(parameters: Mapping[str, Any]) -> np.ndarray:
    gain = float(parameters["actuator_gain_ratio"])
    drag = float(parameters["drag_ratio"])
    sign = -1.0 if parameters["broken_mode"] else 1.0
    time = np.arange(0, 12.0 + 0.01, 0.02)
    nominal = _scalar_closed_loop(gain, drag, sign, 2.0, len(time))
    robust = _scalar_closed_loop(gain, drag, sign, 4.0, len(time))
    nominal_command = 2 * (1 - nominal)
    robust_command = 4 * (1 - robust)
    nominal_cost = np.trapezoid((1 - nominal) ** 2 + 0.05 * nominal_command**2, time)
    robust_cost = np.trapezoid((1 - robust) ** 2 + 0.05 * robust_command**2, time)
    return np.array([gain, drag, sign, nominal_cost, robust_cost, robust[-1]])


def _p21(parameters: Mapping[str, Any]) -> np.ndarray:
    target = (
        20.0 if parameters["broken_mode"] else float(parameters["target_position_m"])
    )
    duration = (
        4.0 if parameters["broken_mode"] else float(parameters["move_duration_s"])
    )
    normalized_time = np.linspace(0, 1, 501)
    velocity = (
        target
        / duration
        * (30 * normalized_time**2 - 60 * normalized_time**3 + 30 * normalized_time**4)
    )
    acceleration = (
        target
        / duration**2
        * (60 * normalized_time - 180 * normalized_time**2 + 120 * normalized_time**3)
    )
    peak_speed = np.max(np.abs(velocity))
    peak_acceleration = np.max(np.abs(acceleration))
    feasible = float(peak_speed <= 5 and peak_acceleration <= 2)
    return np.array([target, duration, peak_speed, peak_acceleration, feasible])


def _p22(parameters: Mapping[str, Any]) -> np.ndarray:
    navigation_constant = float(parameters["navigation_constant"])
    acceleration_limit = (
        5.0
        if parameters["broken_mode"]
        else float(parameters["maximum_acceleration_m_s2"])
    )
    dt = 0.02
    steps = int(25 / dt) + 1
    interceptor = 0.0 + 0.0j
    heading = 0.0
    speed = 300.0
    target = 5000.0 + 600.0j
    target_velocity = -60.0 + 0.0j
    ranges: list[float] = []
    accelerations: list[float] = []
    hit = False
    for _ in range(steps):
        relative = target - interceptor
        distance = abs(relative)
        ranges.append(distance)
        if distance < 5:
            hit = True
            break
        interceptor_velocity = speed * np.exp(1j * heading)
        relative_velocity = target_velocity - interceptor_velocity
        closing_speed = -np.real(np.conj(relative) * relative_velocity) / max(
            distance, 1e-9
        )
        los_rate = np.imag(np.conj(relative) * relative_velocity) / max(
            distance**2, 1e-9
        )
        acceleration = np.clip(
            navigation_constant * closing_speed * los_rate,
            -acceleration_limit,
            acceleration_limit,
        )
        accelerations.append(float(acceleration))
        heading += dt * acceleration / speed
        interceptor += dt * speed * np.exp(1j * heading)
        target += dt * target_velocity
    if len(accelerations) < len(ranges):
        accelerations.append(0.0)
    return np.array(
        [
            navigation_constant,
            acceleration_limit,
            min(ranges),
            float(hit),
            np.max(np.abs(accelerations)),
        ]
    )


def _p23(parameters: Mapping[str, Any]) -> np.ndarray:
    actuator_tau = (
        0.8
        if parameters["broken_mode"]
        else float(parameters["actuator_time_constant_s"])
    )
    sensor_tau = (
        0.6
        if parameters["broken_mode"]
        else float(parameters["sensor_time_constant_s"])
    )
    half_period = 0.1 if parameters["broken_mode"] else 2.0
    dt = 0.01
    time = np.arange(0, 8.0 + dt / 2, dt)
    command = 20 * np.where((np.floor(time / half_period) % 2) == 0, 1, -1)
    actuator_ratio = np.exp(-dt / actuator_tau)
    sensor_ratio = np.exp(-dt / sensor_tau)
    actuator = np.zeros_like(time)
    sensor = np.zeros_like(time)
    actuator[1:] = lfilter([1 - actuator_ratio], [1, -actuator_ratio], command[:-1])
    sensor[1:] = lfilter([1 - sensor_ratio], [1, -sensor_ratio], actuator[:-1])
    lag = np.sqrt(np.mean((command - sensor) ** 2))
    return np.array(
        [actuator_tau, sensor_tau, half_period, lag, actuator[-1], sensor[-1]]
    )


def _p24(parameters: Mapping[str, Any]) -> np.ndarray:
    period = (
        0.1 if parameters["broken_mode"] else float(parameters["controller_period_s"])
    )
    latency = (
        0.04 if parameters["broken_mode"] else float(parameters["one_way_latency_s"])
    )
    watchdog = 0.12 if parameters["broken_mode"] else 0.2
    drop_interval = 2 if parameters["broken_mode"] else 0
    dt = 0.01
    time = np.arange(0, 8.0 + dt / 2, dt)
    period_ticks = round(period / dt)
    latency_ticks = round(latency / dt)
    watchdog_ticks = round(watchdog / dt)
    reference = np.where(time < 4.0, 1.0, -0.5)

    position = np.zeros_like(time)
    velocity = np.zeros_like(time)
    sensor_events: list[list[tuple[float, float, int]]] = [[] for _ in range(len(time))]
    command_events: list[list[float]] = [[] for _ in range(len(time))]
    measured_position = 0.0
    measured_velocity = 0.0
    has_measurement = False
    has_command = False
    delivered_force = 0.0
    last_delivery_tick = 0
    sequence = 0
    watchdog_count = 0

    mass = 1.5
    damping = 1.2
    decay = np.exp(-damping * dt / mass)
    force_to_velocity = -np.expm1(-damping * dt / mass) / damping
    velocity_to_position = mass / damping * (1 - decay)
    force_to_position = dt / damping - mass * (1 - decay) / damping**2

    for tick in range(len(time)):
        is_controller_tick = tick % period_ticks == 0
        delivery_tick = tick + latency_ticks
        if is_controller_tick and delivery_tick < len(time):
            sensor_events[delivery_tick].append((position[tick], velocity[tick], tick))

        for measured_position, measured_velocity, _ in sensor_events[tick]:
            has_measurement = True

        if is_controller_tick and has_measurement:
            requested_force = 18 * (reference[tick] - measured_position)
            requested_force -= 8 * measured_velocity
            requested_force = float(np.clip(requested_force, -30, 30))
            sequence += 1
            dropped = drop_interval > 0 and sequence % drop_interval == 0
            if not dropped and delivery_tick < len(time):
                command_events[delivery_tick].append(requested_force)

        for delivered_force in command_events[tick]:
            has_command = True
            last_delivery_tick = tick

        timed_out = has_command and tick - last_delivery_tick >= watchdog_ticks
        watchdog_count += int(timed_out and tick < len(time) - 1)
        force = 0.0 if not has_command or timed_out else delivered_force
        if tick < len(time) - 1:
            velocity[tick + 1] = decay * velocity[tick] + force_to_velocity * force
            position[tick + 1] = (
                position[tick]
                + velocity_to_position * velocity[tick]
                + force_to_position * force
            )
    watchdog_fraction = watchdog_count / (len(time) - 1)
    return np.array(
        [
            period,
            latency,
            watchdog,
            float(drop_interval),
            position[-1],
            watchdog_fraction,
        ]
    )


REFERENCES: dict[int, Callable[[Mapping[str, Any]], np.ndarray]] = {
    1: _p01,
    2: _p02,
    3: _p03,
    4: _p04,
    5: _p05,
    6: _p06,
    7: _p07,
    8: _p08,
    9: _p09,
    10: _p10,
    11: _p11,
    12: _p12,
    13: _p13,
    14: _p14,
    15: _p15,
    16: _p16,
    17: _p17,
    18: _p18,
    19: _p19,
    20: _p20,
    21: _p21,
    22: _p22,
    23: _p23,
    24: _p24,
}


def reference_signature(item_number: int, parameters: Mapping[str, Any]) -> list[float]:
    """Return a finite independent numeric signature for one retained scenario."""

    signature = np.asarray(REFERENCES[item_number](parameters), dtype=float)
    if signature.ndim != 1 or not np.all(np.isfinite(signature)):
        raise ValueError(
            f"P{item_number:02d} produced a non-finite reference signature"
        )
    return signature.tolist()


def teaching_invariant(
    item_number: int,
    parameters: Mapping[str, Any],
    signature: list[float] | np.ndarray,
) -> tuple[str, bool]:
    """Evaluate the lesson's primary invariant from a signature only."""

    values = np.asarray(signature, dtype=float)
    broken = bool(parameters["broken_mode"])
    descriptions = {
        1: "natural frequency and damping are physical; broken integration exposes energy growth",
        2: "the integrator ramps while the stable first-order path remains bounded",
        3: "real pole sign controls decay or growth and imaginary part fixes period",
        4: "small-angle error grows at the forced large-angle failure",
        5: "negative feedback is bounded while the reversed sign is unstable",
        6: "correct derivative feedback dissipates rather than injects energy",
        7: "actuator lag reduces phase reserve",
        8: "sensitivity attenuation matches the closed-loop frequency relation",
        9: "sampled PI remains finite and exposes the chosen discretization",
        10: "delay is the declared fraction of one sample",
        11: "applied authority clips whenever requested authority exceeds its limit",
        12: "anti-windup recovery metrics remain finite and nonnegative",
        13: "zero coupling removes one controllable direction",
        14: "rate-only sensing removes one observable direction",
        15: "observer error converges to the bias-consistent equilibrium",
        16: "Kalman covariance assumptions yield a finite deterministic estimate",
        17: "zero actuator effectiveness produces zero feedback authority",
        18: "tracking and command measures remain finite under the declared sign",
        19: "the uncertainty experiment reports a finite model gap",
        20: "the lesson compares exactly two fixed gains, not robust synthesis",
        21: "feasibility follows explicit speed and acceleration limits",
        22: "PN acceleration respects the declared saturation",
        23: "positive first-order time constants create finite cascaded lag",
        24: "software event ordering produces a bounded watchdog fraction",
    }
    predicates: dict[int, Callable[[], bool]] = {
        1: lambda: (
            values[0] > 0
            and values[1] >= 0
            and (values[4] > 1 if broken else values[4] < 1)
        ),
        2: lambda: (
            abs(values[2] - 10 * values[0]) < 1e-8
            and (
                values[4] > 2 * abs(values[0])
                if broken
                else values[4] <= 1.01 * abs(values[0])
            )
        ),
        3: lambda: (
            abs(values[2] * values[1] - 2 * np.pi) < 1e-8
            and (values[4] > 1 if broken else True)
        ),
        4: lambda: values[2] > (0.1 if broken else 0.0),
        5: lambda: values[4] > (10 if broken else 0) and (broken or values[4] < 1),
        6: lambda: (values[4] > 10) if broken else (values[4] < 10),
        7: lambda: (values[2] < 0) if broken else bool(np.isfinite(values[2])),
        8: lambda: (
            abs(values[3] - 1 / np.sqrt((1 + values[0]) ** 2 + values[1] ** 2)) < 1e-10
        ),
        9: lambda: bool(np.all(np.isfinite(values)) and values[0] > 0),
        10: lambda: abs(values[2] - values[0] * values[1]) < 1e-12,
        11: lambda: 0 <= values[2] <= 1 and values[4] >= values[1],
        12: lambda: values[3] >= 0 and values[4] >= 0,
        13: lambda: values[2] == (1 if broken else 2),
        14: lambda: values[3] == (1 if broken else 2),
        15: lambda: bool(np.all(np.isfinite(values[2:]))),
        16: lambda: (
            values[0] > 0 and values[1] > 0 and bool(np.all(np.isfinite(values[3:])))
        ),
        17: lambda: abs(values[3]) < 1e-12 if broken else values[3] > 0,
        18: lambda: values[3] >= 0 and values[4] >= 0,
        19: lambda: values[3] >= 0 and bool(np.isfinite(values[4])),
        20: lambda: values[3] >= 0 and values[4] >= 0 and bool(np.isfinite(values[5])),
        21: lambda: values[4] == float(values[2] <= 5 and values[3] <= 2),
        22: lambda: values[4] <= values[1] + 1e-9 and values[2] >= 0,
        23: lambda: values[0] > 0 and values[1] > 0 and values[3] >= 0,
        24: lambda: 0 <= values[5] <= 1 and values[0] > 0 and values[1] >= 0,
    }
    return descriptions[item_number], bool(predicates[item_number]())
