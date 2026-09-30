from __future__ import annotations

# Independent scalar oracle: imports no production experiment and consumes no production result.
import math

import numpy as np
from scipy.linalg import expm


def _p01(a: float, b: float, broken: bool) -> list[float]:
    return _vehicle_reference_state(1, a, b, broken)["signature"]


def _p02(a: float, b: float, broken: bool) -> list[float]:
    return _vehicle_reference_state(2, a, b, broken)["signature"]


def _p03(a: float, b: float, broken: bool) -> list[float]:
    return _vehicle_reference_state(3, a, b, broken)["signature"]


def _p04(a: float, b: float, broken: bool) -> list[float]:
    return _vehicle_reference_state(4, a, b, broken)["signature"]


def _p05(a: float, b: float, broken: bool) -> list[float]:
    return _vehicle_reference_state(5, a, b, broken)["signature"]


def _p06(a: float, b: float, broken: bool) -> list[float]:
    return _vehicle_reference_state(6, a, b, broken)["signature"]


def _p07(a: float, b: float, broken: bool) -> list[float]:
    return _vehicle_reference_state(7, a, b, broken)["signature"]


def _p08(a: float, b: float, broken: bool) -> list[float]:
    return _vehicle_reference_state(8, a, b, broken)["signature"]


def _p09(a: float, b: float, broken: bool) -> list[float]:
    return _vehicle_reference_state(9, a, b, broken)["signature"]


def _p10(a: float, b: float, broken: bool) -> list[float]:
    return _vehicle_reference_state(10, a, b, broken)["signature"]


def _p11(a: float, b: float, broken: bool) -> list[float]:
    return _vehicle_reference_state(11, a, b, broken)["signature"]


def _p12(a: float, b: float, broken: bool) -> list[float]:
    return _vehicle_reference_state(12, a, b, broken)["signature"]


def _p13(a: float, b: float, broken: bool) -> list[float]:
    return _vehicle_driveline_reference_state(13, a, b, broken)["signature"]


def _shift_torque(engine_rpm: float) -> float:
    return max(120.0, 245.0 - 0.000006 * (engine_rpm - 5000.0) ** 2)


def _p14(a: float, b: float, broken: bool) -> list[float]:
    return _vehicle_driveline_reference_state(14, a, b, broken)["signature"]


def _p15(a: float, b: float, broken: bool) -> list[float]:
    return _vehicle_driveline_reference_state(15, a, b, broken)["signature"]


def _p16(a: float, b: float, broken: bool) -> list[float]:
    return _vehicle_driveline_reference_state(16, a, b, broken)["signature"]


def _p17(a: float, b: float, broken: bool) -> list[float]:
    raw = round(a)
    first_byte, second_byte = divmod(raw, 256)
    restored = second_byte * 256 + first_byte if broken else first_byte * 256 + second_byte
    speed_kmh = restored / 128.0
    return [
        speed_kmh,
        speed_kmh / 3.6,
        speed_kmh * 128.0 - raw,
        b,
        100.0,
        float(0x139),
        8.0,
        9.0,
        float(broken or b > 100.0),
    ]


def _p18(a: float, b: float, broken: bool) -> list[float]:
    sample_period = 0.5
    truth_acceleration = 0.4
    times = [sample_period * index for index in range(21)]
    truth_positions = [truth_acceleration * time * time / 2.0 for time in times]
    gps_positions = [
        position + 0.6 * math.sin(0.7 * time)
        for position, time in zip(truth_positions, times, strict=True)
    ]
    estimate = 0.0
    velocity = 0.0
    estimates = [estimate]
    absolute_innovations: list[float] = []
    for index in range(1, len(times)):
        sensed_acceleration = truth_acceleration + b
        prediction = (
            estimate
            + velocity * sample_period
            + sensed_acceleration * sample_period * sample_period / 2.0
        )
        velocity += sensed_acceleration * sample_period
        measurement_index = max(0, index - 2) if broken else index
        innovation = gps_positions[measurement_index] - prediction
        estimate = prediction + a * innovation
        estimates.append(estimate)
        absolute_innovations.append(abs(innovation))
    errors = [
        estimated - truth
        for estimated, truth in zip(estimates, truth_positions, strict=True)
    ]
    return [
        errors[-1],
        velocity - truth_acceleration * times[-1],
        math.sqrt(sum(error**2 for error in errors) / len(errors)),
        sum(absolute_innovations) / len(absolute_innovations),
        estimate - gps_positions[-1],
        1.0 if broken else 0.0,
        float(len(times)),
        float(broken),
    ]


def _p19(a: float, b: float, broken: bool) -> list[float]:
    step = 0.1
    yaw_rate = b if broken else b * math.pi / 180.0
    x_position = 0.0
    y_position = 0.0
    heading = 0.0
    for _ in range(100):
        middle_heading = heading + yaw_rate * step / 2.0
        x_position += a * math.cos(middle_heading) * step
        y_position += a * math.sin(middle_heading) * step
        heading += yaw_rate * step
    curvature = yaw_rate / a
    radius = 0.0 if abs(curvature) < 1e-12 else 1.0 / abs(curvature)
    return [
        x_position,
        y_position,
        heading * 180.0 / math.pi,
        curvature,
        radius,
        a * yaw_rate,
        a * 10.0,
        float(broken),
    ]


def _p20(a: float, b: float, broken: bool) -> list[float]:
    density = 1.225
    disturbance = [0.0, 0.7, -0.4, 0.2, -0.8, 0.5, -0.1, 0.9, -0.6, 0.3, -0.2, 0.4]
    speeds = [10.0 + a * index / 11.0 for index in range(12)]
    observations = [
        180.0 + 0.5 * density * 0.64 * speed**2 + b * disturbance[index]
        for index, speed in enumerate(speeds)
    ]
    fit_indices = list(range(0, 12, 2))
    check_indices = list(range(1, 12, 2))
    regressors = [225.0 if broken else speeds[index] ** 2 for index in fit_indices]
    responses = [observations[index] for index in fit_indices]
    center_x = sum(regressors) / len(regressors)
    center_y = sum(responses) / len(responses)
    information = sum((value - center_x) ** 2 for value in regressors)
    if information <= 1e-12:
        gradient = 0.0
        offset = center_y
    else:
        gradient = sum(
            (x_value - center_x) * (y_value - center_y)
            for x_value, y_value in zip(regressors, responses, strict=True)
        ) / information
        offset = center_y - gradient * center_x
    fit_errors = [
        response - offset - gradient * regressor
        for regressor, response in zip(regressors, responses, strict=True)
    ]
    check_errors = [
        observations[index] - offset - gradient * speeds[index] ** 2
        for index in check_indices
    ]
    variance = sum(error**2 for error in fit_errors) / max(1, len(fit_errors) - 2)
    parameter_error = (
        0.0
        if information <= 1e-12
        else 2.0 * math.sqrt(variance / information) / density
    )
    return [
        offset,
        2.0 * gradient / density,
        math.sqrt(sum(error**2 for error in fit_errors) / len(fit_errors)),
        math.sqrt(sum(error**2 for error in check_errors) / len(check_errors)),
        max(regressors) - min(regressors),
        information / max(1.0, sum(value**2 for value in regressors)),
        parameter_error,
        float(broken or information <= 1e-12),
    ]


def _p21_score(offset: float, friction: float) -> tuple[float, float, float, float]:
    effective_radius = 45.0 + offset
    distance = math.pi * 45.0 / 2.0 + 0.08 * offset**2
    speed = math.sqrt(friction * 9.81 * effective_radius)
    return effective_radius, distance, speed, distance / speed + 200.0 / 45.0


def _p21(a: float, b: float, broken: bool) -> list[float]:
    candidates = [-b + 2.0 * b * index / 40.0 for index in range(41)]
    if broken:
        selected = b + 1.0
    else:
        selected = min(candidates, key=lambda offset: _p21_score(offset, a)[3])
    radius, distance, speed, elapsed = _p21_score(selected, a)
    center_elapsed = _p21_score(0.0, a)[3]
    margin = b - abs(selected)
    return [
        selected,
        radius,
        distance,
        speed,
        elapsed,
        center_elapsed - elapsed,
        margin,
        41.0,
        float(broken or margin < -1e-12),
    ]


def _p22(a: float, b: float, broken: bool) -> list[float]:
    curvatures = [
        0.0,
        0.0,
        0.012,
        0.025,
        0.045,
        0.045,
        0.020,
        0.0,
        0.0,
        0.035,
        0.050,
        0.015,
        0.0,
    ]
    spacing = 25.0
    ceilings = [
        50.0
        if curvature == 0.0
        else min(50.0, math.sqrt(a * 9.81 / curvature))
        for curvature in curvatures
    ]
    speeds = [15.0]
    for ceiling in ceilings[1:]:
        speeds.append(min(ceiling, math.sqrt(speeds[-1] ** 2 + 2.0 * b * spacing)))
    if not broken:
        speeds[-1] = min(speeds[-1], 15.0)
        for index in range(len(speeds) - 2, -1, -1):
            speeds[index] = min(
                speeds[index], math.sqrt(speeds[index + 1] ** 2 + 12.0 * spacing)
            )
    braking_residual = max(
        max(
            0.0,
            speeds[index] ** 2
            - speeds[index + 1] ** 2
            - 12.0 * spacing,
        )
        for index in range(len(speeds) - 1)
    )
    elapsed = sum(
        2.0 * spacing / (speeds[index] + speeds[index + 1])
        for index in range(len(speeds) - 1)
    )
    binding = sum(
        abs(speed - ceiling) < 1e-9
        for speed, ceiling in zip(speeds, ceilings, strict=True)
    )
    return [
        elapsed,
        max(speeds),
        speeds[8],
        braking_residual,
        float(binding),
        min(speeds),
        12.0,
        float(broken or braking_residual > 1e-9),
    ]


def _p23(a: float, b: float, broken: bool) -> list[float]:
    original = [28.0, 35.0, 22.0, 31.0]
    aero_response = [1.0, 0.4, 1.2, 0.6]
    tire_response = [0.8, 1.2, 0.7, 1.1]
    changed = [
        base
        * (
            1.0
            - 0.0008 * a * aero_gain
            - 0.002 * b * tire_gain
            - 0.00001 * a * b
        )
        for base, aero_gain, tire_gain in zip(
            original, aero_response, tire_response, strict=True
        )
    ]
    paired_candidate = changed[1:] + changed[:1] if broken else changed
    paired_delta = [
        candidate - baseline
        for candidate, baseline in zip(paired_candidate, original, strict=True)
    ]
    mean_delta = sum(paired_delta) / len(paired_delta)
    standard_error = math.sqrt(
        sum((delta - mean_delta) ** 2 for delta in paired_delta)
        / (len(paired_delta) - 1)
    ) / math.sqrt(len(paired_delta))
    total_delta = sum(changed) - sum(original)
    aero_effect = sum(
        -base * 0.0008 * a * gain
        for base, gain in zip(original, aero_response, strict=True)
    )
    tire_effect = sum(
        -base * 0.002 * b * gain
        for base, gain in zip(original, tire_response, strict=True)
    )
    interaction = sum(-base * 0.00001 * a * b for base in original)
    return [
        sum(original),
        sum(changed),
        total_delta,
        aero_effect,
        tire_effect,
        interaction,
        standard_error,
        -0.20 - total_delta,
        float(total_delta < -0.20 and not broken),
        float(broken),
    ]


def _p24_trajectory(
    mass: float, friction: float, broken: bool
) -> tuple[list[float], list[float], list[float], list[float], list[float]]:
    time_step = 0.2
    speed = 10.0
    heading = 0.0
    east = 0.0
    north = 0.0
    times = [0.0]
    speed_history = [speed]
    east_history = [east]
    north_history = [north]
    yaw_history = [0.0]
    for index in range(1, 61):
        time = index * time_step
        propulsion = 4000.0 + 600.0 * math.sin(0.22 * time)
        resistance = 0.5 * 1.225 * 0.65 * speed**2
        acceleration = min((propulsion - resistance) / mass, 0.35 * friction * 9.81)
        speed = max(0.0, speed + acceleration * time_step)
        steering_degrees = 12.0 * math.sin(0.35 * time)
        road_wheel_angle = (
            steering_degrees / 13.0
            if broken
            else steering_degrees * math.pi / (180.0 * 13.0)
        )
        unconstrained_yaw = speed * math.tan(road_wheel_angle) / 2.57
        yaw_bound = friction * 9.81 / max(speed, 1.0)
        yaw = max(-yaw_bound, min(yaw_bound, unconstrained_yaw))
        midpoint = heading + yaw * time_step / 2.0
        east += speed * math.cos(midpoint) * time_step
        north += speed * math.sin(midpoint) * time_step
        heading += yaw * time_step
        times.append(time)
        speed_history.append(speed)
        east_history.append(east)
        north_history.append(north)
        yaw_history.append(yaw)
    return times, speed_history, east_history, north_history, yaw_history


def _p24(a: float, b: float, broken: bool) -> list[float]:
    times, speeds, east, north, yaws = _p24_trajectory(a, b, broken)
    _, nominal_speed, nominal_east, nominal_north, nominal_yaw = _p24_trajectory(
        1320.0, 1.0, False
    )
    speed_observation = [
        value + 0.05 * math.sin(0.4 * time)
        for value, time in zip(nominal_speed, times, strict=True)
    ]
    east_observation = [
        value + 0.10 * math.sin(0.3 * time)
        for value, time in zip(nominal_east, times, strict=True)
    ]
    north_observation = [
        value + 0.10 * math.cos(0.3 * time)
        for value, time in zip(nominal_north, times, strict=True)
    ]
    yaw_observation = [
        value + 0.001 * math.sin(0.6 * time)
        for value, time in zip(nominal_yaw, times, strict=True)
    ]
    speed_error = [
        model - observed
        for model, observed in zip(speeds, speed_observation, strict=True)
    ]
    position_error = [
        math.hypot(x_model - x_observed, y_model - y_observed)
        for x_model, y_model, x_observed, y_observed in zip(
            east, north, east_observation, north_observation, strict=True
        )
    ]
    yaw_error = [
        model - observed
        for model, observed in zip(yaws, yaw_observation, strict=True)
    ]
    speed_rmse = math.sqrt(sum(value**2 for value in speed_error) / len(speed_error))
    position_rmse = math.sqrt(
        sum(value**2 for value in position_error) / len(position_error)
    )
    yaw_rmse = math.sqrt(sum(value**2 for value in yaw_error) / len(yaw_error))
    distance = sum(0.2 * value for value in speeds[1:])
    mean_speed = distance / (times[-1] - times[0])
    return [
        speed_rmse,
        position_rmse,
        yaw_rmse,
        speeds[-1],
        distance,
        2400.0 / mean_speed,
        float(sum((speed_rmse < 1.0, position_rmse < 3.0, yaw_rmse < 0.05))),
        max(abs(value) for value in yaw_error),
        float(broken),
    ]


_MODELS = {
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


def evaluate(
    item_id: str, primary: float, secondary: float, broken: bool = False
) -> list[float]:
    return _MODELS[item_id](float(primary), float(secondary), bool(broken))


# Independent full-mechanism formulations for the selected quality revision.
def _vehicle_reference_state(n, a, b, fault):
    if n == 1:
        angle = a * math.pi / (180 * (1 if fault else 13))
        radius_inverse = math.sin(angle) / (2.57 * math.cos(angle))
        angular = b * radius_inverse
        lateral = b**2 * radius_inverse
        declared = math.sin(a * math.pi / 2340) / (2.57 * math.cos(a * math.pi / 2340))
        error = radius_inverse - declared
        s = [
            radius_inverse,
            angular,
            lateral,
            9.81,
            float(abs(lateral) > 9.81 or abs(error) > 1e-12),
        ]
        return dict(
            signature=s,
            road_angle_rad=angle,
            steering_relation_residual_per_m=error,
            grip_feasible=abs(lateral) <= 9.81,
            yaw_identity_residual=lateral - b * angular,
        )
    if n == 2:
        weight = 1320 * 9.81
        rolling = weight * 0.015
        aerodynamic = 1.225 * 0.31 * b * b
        tire = min(a, weight)
        actual_loads = np.array([tire, -rolling, -aerodynamic])
        acceleration = float(np.sum(actual_loads[:1] if fault else actual_loads) / 1320)
        residual = 1320 * acceleration - float(np.sum(actual_loads))
        return dict(
            signature=[
                tire,
                rolling,
                aerodynamic,
                acceleration,
                weight,
                float(abs(residual) > 1e-9),
            ],
            net_force_n=1320 * acceleration,
            force_balance_residual_n=residual,
            requested_force_n=a,
            traction_limited=a > weight,
        )
    if n == 3:
        weight = 12949.2
        demand = 1320 * a * b / 2.57
        shift = 0 if fault else demand
        # Sum of reactions and pitch moment determine the two loads independently.
        front, rear = np.linalg.solve(
            [[1, 1], [0, 2.57]], [weight, 0.47 * weight * 2.57 + shift * 2.57]
        )
        residual = (rear - 0.47 * weight) * 2.57 - 1320 * a * b
        return dict(
            signature=[
                float(front),
                float(rear),
                demand,
                float(front + rear),
                float(min(front, rear) < 0 or abs(residual) > 1e-8),
            ],
            applied_transfer_n=shift,
            pitch_balance_residual_nm=float(residual),
            weight_balance_residual_n=float(front + rear - weight),
            contact_feasible=bool(min(front, rear) >= 0),
        )
    if n == 4:
        cap = 3780.0
        length = float(np.linalg.norm([a, b]))
        applied = length if fault else min(length, cap)
        angle = math.atan2(b, a)
        fx = applied * math.cos(angle)
        fy = applied * math.sin(angle)
        if length == 0:
            fx = fy = 0.0
        scale = applied / length if length else 1.0
        return dict(
            signature=[fx, fy, length / cap, cap, float(applied > cap + 1e-9)],
            applied_utilization=applied / cap,
            scale=scale,
            direction_cross_residual=(fx / cap) * (b / cap) - (fy / cap) * (a / cap),
            requested_feasible=length <= cap,
        )
    if n in (5, 6):
        slip = a if n == 5 else a * math.pi / 180
        stiffness = 85000.0 if n == 5 else 78000.0
        capacity = b * 1.05
        # Logistic form independently evaluates the saturating constitutive law.
        z = stiffness * slip / capacity
        e = math.exp(-2 * abs(z))
        saturation = math.copysign((1 - e) / (1 + e), z)
        sign = (1 if n == 5 else -1) * (-1 if fault else 1)
        force = sign * capacity * saturation
        invalid = force * slip < -1e-10 if n == 5 else force * slip > 1e-10
        d = dict(
            signature=[slip, force, capacity, stiffness, float(invalid)],
            utilization=abs(force) / capacity,
            signed_work_indicator=force * slip,
        )
        d["initial_slope_n" if n == 5 else "initial_slope_n_per_rad"] = sign * stiffness
        return d
    if n == 7:
        steer = a * math.pi / 180
        speed = b
        mass = 1320.0
        f = 1.15
        rear_arm = 1.42
        length = f + rear_arm
        cf = 90000.0
        cr = 100000.0
        if not fault:
            # Moment balance first fixes axle force shares. Tire compatibility then fixes yaw.
            yaw = steer / (
                length / speed + mass * speed / length * (rear_arm / cf - f / cr)
            )
            front_force = mass * speed * yaw * rear_arm / length
            rear_force = mass * speed * yaw * f / length
            beta = rear_arm * yaw / speed - rear_force / cr
        else:
            # Explicit historical fault equations, independently solved by factorization.
            matrix = np.array(
                [
                    [190000 / speed, mass * speed - 38500 / speed],
                    [-38500, 1.15**2 * 90000 + 1.42**2 * 100000],
                ]
            )
            beta, yaw = np.linalg.solve(matrix, [cf * steer, cf * f * steer])
        af = steer - beta - f * yaw / speed
        ar = -beta + rear_arm * yaw / speed
        front_force = cf * af
        rear_force = cr * ar
        force_residual = front_force + rear_force - mass * speed * yaw
        moment_residual = f * front_force - rear_arm * rear_force
        small = max(abs(af), abs(ar), abs(steer), abs(beta)) <= 8 * math.pi / 180
        s = [
            float(beta),
            float(yaw),
            float(af),
            float(ar),
            float(mass * speed * yaw),
            float(not small or max(abs(force_residual), abs(moment_residual)) > 1e-6),
        ]
        return dict(
            signature=s,
            front_force_n=float(front_force),
            rear_force_n=float(rear_force),
            force_balance_residual_n=float(force_residual),
            yaw_balance_residual_nm=float(moment_residual),
            small_angle_valid=bool(small),
        )
    if n == 8:
        front_weight = 1320 * 9.81 * 1.42 / 2.57
        rear_weight = 1320 * 9.81 * 1.15 / 2.57
        coefficient = (front_weight / a - rear_weight / b) / 9.81
        available = coefficient < -1e-14
        critical = math.sqrt(2.57 / -coefficient) if available else 0.0
        physical = 2.57 + coefficient * 625.0
        used = 2.57 if fault else physical
        error = used - physical
        return dict(
            signature=[
                coefficient,
                coefficient * 9.81 * 180 / math.pi,
                critical,
                25.0,
                used,
                float(physical <= 0 or abs(error) > 1e-10),
            ],
            physical_denominator_m=physical,
            compliance_residual_m=error,
            critical_speed_available=available,
            steady_branch_stable=physical > 0,
        )
    if n == 9:
        # A unit wheel displacement produces spring displacement r and wheel force r*k*r.
        wheel_force = a * b * (1.0 if fault else b)
        compression = 2943.0 / wheel_force
        freq = math.sqrt(wheel_force / 300) / (2 * math.pi)
        error = wheel_force - a * b * b
        return dict(
            signature=[wheel_force, freq, compression, a, b, float(abs(error) > 1e-9)],
            virtual_work_stiffness_residual_n_m=error,
            static_balance_residual_n=wheel_force * compression - 2943.0,
        )
    if n == 10:
        c = -a if fault else a
        mass = 300.0
        natural = math.sqrt(b / mass)
        poles = np.linalg.eigvals([[0.0, 1.0], [-b / mass, -c / mass]])
        decay = c / (2 * mass)
        damping = decay / natural
        slow = -float(max(p.real for p in poles)) if decay > 0 else decay
        damped = float(max(abs(p.imag) for p in poles)) / (2 * math.pi)
        if abs(decay * decay - b / mass) < 1e-12:
            slow = decay
            damped = 0.0
        over = (
            math.exp(-math.pi * damping / math.sqrt(1 - damping * damping))
            if 0 < damping < 1
            else (0.0 if damping >= 1 else 1.0)
        )
        return dict(
            signature=[
                natural / (2 * math.pi),
                damping,
                damped,
                over,
                4 / slow if slow > 0 else 0.0,
                decay,
                float(decay <= 0),
            ],
            damping_n_s_m=c,
            slow_decay_rate_per_s=slow,
            stable=decay > 0,
            overshoot_available=decay > 0,
            time_scale_available=decay > 0,
        )
    if n == 11:
        moment = 4620.0
        angle = float(np.linalg.solve([[a if fault else a + b]], [moment])[0])
        mf = a * angle
        mr = b * angle
        front = mf / 1.53
        rear = mr / 1.53
        residual = mf + mr - moment
        share = mf / moment
        return dict(
            signature=[
                angle,
                front,
                rear,
                share,
                residual,
                share - 0.53,
                float(abs(residual) > 1e-8),
            ],
            front_moment_nm=mf,
            rear_moment_nm=mr,
            imposed_moment_nm=moment,
            constitutive_total_nm=(a + b) * angle,
        )
    if n == 12:
        factor = 1 if fault else math.pi / 180
        gamma = a * factor
        toe = b * factor
        thrust = -60000 * gamma
        scrub = 3600 * abs(math.sin(toe) / math.cos(toe))
        power = scrub * 20
        cg = gamma - a * math.pi / 180
        ct = toe - b * math.pi / 180
        return dict(
            signature=[
                gamma,
                toe,
                thrust,
                scrub,
                power,
                toe,
                float(max(abs(cg), abs(ct)) > 1e-12),
            ],
            camber_conversion_residual_rad=cg,
            toe_conversion_residual_rad=ct,
            power_identity_residual_w=power - 20 * scrub,
        )
    raise ValueError(n)

def _vehicle_reference_response(n, a, b, fault):
    state = lambda x, y: _vehicle_reference_state(n, x, y, fault)["signature"]
    if n == 1:
        times = np.linspace(0, 4, 81)
        yaw = state(a, b)[1]
        theta = yaw * times
        x = b * times * np.sinc(theta / np.pi)
        y = b * times * (theta / 2) * np.sinc(theta / (2 * np.pi)) ** 2
        return dict(x=x.tolist(), series=[y.tolist()], time_s=times.tolist())
    if n == 2:
        s = state(a, b)
        return dict(
            x=["Traction", "Rolling", "Drag", "Model net"],
            series=[[s[0], -s[1], -s[2], 1320 * s[3]]],
        )
    if n == 3:
        x = np.linspace(-9, 9, 61).tolist()
        vals = [state(v, b) for v in x]
        return dict(x=x, series=[[v[0] for v in vals], [v[1] for v in vals]])
    if n == 4:
        angles = np.linspace(0, 2 * np.pi, 121)
        s = state(a, b)
        return dict(
            x=(3780 * np.cos(angles)).tolist(),
            series=[(3780 * np.sin(angles)).tolist()],
            vector_x=[0.0, s[0]],
            vector_y=[0.0, s[1]],
            requested_x=[a],
            requested_y=[b],
        )
    if n in (5, 6, 7, 12):
        lo, hi, count, index = {
            5: (-0.3, 0.3, 81, 1),
            6: (-14, 14, 81, 1),
            7: (3, 40, 81, 1),
            12: (-5, 2, 61, 2),
        }[n]
        x = np.linspace(lo, hi, count).tolist()
        vals = [state(a, v)[index] if n == 7 else state(v, b)[index] for v in x]
        return dict(x=x, series=[vals])
    if n == 8:
        k = state(a, b)[0]
        used = 0 if fault else k
        x = np.linspace(5, 60, 81)
        return dict(
            x=x.tolist(),
            series=[np.rad2deg(2.57 / x**2 + used).tolist()],
            stable=(2.57 + k * x * x > 0).tolist(),
        )
    if n == 9:
        x = np.linspace(0, 0.2, 61)
        wheel = state(a, b)[0]
        return dict(x=x.tolist(), series=[(x * wheel).tolist(), [2943.0] * len(x)])
    if n == 10:
        m = 300.0
        c = -a if fault else a
        matrix = np.array([[0.0, 1.0], [-b / m, -c / m]])
        growth = max(np.linalg.eigvals([[0.0, 1.0], [-b / m, a / m]]).real)
        times = np.linspace(0, min(8.0, 3 / float(growth)), 121)
        states = np.array([expm(matrix * t) @ np.array([-0.01, 0.0]) for t in times])
        x = states[:, 0] + 0.01
        v = states[:, 1]
        acc = (b * (0.01 - x) - c * v) / m
        energy = np.einsum("ij,jk,ik->i", states, np.diag([b, m]), states) / 2
        return dict(
            x=times.tolist(),
            series=[x.tolist()],
            velocity_m_s=v.tolist(),
            acceleration_m_s2=acc.tolist(),
            energy_j=energy.tolist(),
            energy_rate_w=(-c * v * v).tolist(),
        )
    if n == 11:
        x = np.linspace(0, 12, 61)
        r = np.deg2rad(x)
        used = a if fault else a + b
        return dict(
            x=x.tolist(),
            series=[(used * r).tolist(), ((a + b) * r).tolist(), [4620.0] * len(x)],
        )
    raise ValueError(n)

def vehicle_foundations_reference(number, primary, secondary, broken=False):
    return {
        "physical": _vehicle_reference_state(
            number, float(primary), float(secondary), bool(broken)
        ),
        "response": _vehicle_reference_response(
            number, float(primary), float(secondary), bool(broken)
        ),
    }


# Independent power/work, polynomial-root and energy formulations.
# This file never imports production experiments or consumes their output.
def _driveline_fields(n, signature, **extra):
    fields = {
        13: [
            "engine_speed_rpm",
            "requested_wheel_force_n",
            "applied_wheel_force_n",
            "traction_limit_n",
            "wheel_power_w",
            "power_residual_w",
            "invalid",
        ],
        14: [
            "shift_rpm",
            "shift_speed_m_s",
            "current_force_n",
            "next_force_n",
            "post_shift_rpm",
            "force_gap_n",
            "invalid",
        ],
        15: [
            "applied_brake_force_n",
            "deceleration_m_s2",
            "stopping_distance_m",
            "stop_time_s",
            "kinetic_energy_j",
            "rotor_delta_t_c",
            "front_load_n",
            "rear_load_n",
            "invalid",
        ],
        16: [
            "dynamic_pressure_pa",
            "drag_n",
            "downforce_n",
            "tire_capacity_n",
            "drag_power_w",
            "front_aero_share",
            "invalid",
        ],
    }
    return dict(zip(fields[n], signature, strict=True), signature=signature, **extra)


def _driveline_reference_torque(rpm):
    return max(120.0, 95.0 + 0.06 * rpm - 6e-6 * rpm * rpm)


def _driveline_reference_forces(current, nxt, rpm, fault):
    ratio = nxt / current
    post = rpm * ratio
    scale = 4.1 * 0.9 / 0.315
    return [
        _driveline_reference_torque(rpm) * current * scale,
        _driveline_reference_torque(rpm if fault else post) * nxt * scale,
        post,
    ]


def _vehicle_driveline_reference_state(n, a, b, fault):
    mass, gravity = 1320.0, 9.81
    weight = mass * gravity
    if n == 13:
        # Begin with shaft work per revolution and power; invert for force/torque.
        wheel_turns_per_second = 20.0 / (2 * math.pi * 0.315)
        rpm = wheel_turns_per_second * b * 4.1 * 60
        omega = rpm * math.pi / 30
        request_power = a * omega
        eta = 1.0 if fault else 0.9
        delivered_power = min(request_power, weight * 20 / eta)
        wheel_power = eta * delivered_power
        applied = wheel_power / 20
        demanded = eta * request_power / 20
        loss = delivered_power / 10
        residual = wheel_power + loss - delivered_power
        signature = [
            rpm,
            demanded,
            applied,
            weight,
            wheel_power,
            residual,
            float(abs(residual) > 1e-8),
        ]
        return _driveline_fields(
            n,
            signature,
            engine_angular_speed_rad_s=omega,
            wheel_angular_speed_rad_s=2 * math.pi * wheel_turns_per_second,
            delivered_engine_torque_nm=delivered_power / omega,
            requested_engine_power_w=request_power,
            delivered_engine_power_w=delivered_power,
            drivetrain_loss_w=loss,
            curtailed_request_w=request_power - delivered_power,
            transmitted_efficiency=eta,
            traction_limited=float(demanded > weight),
        )
    if n == 14:
        q = b / a
        available = b < a
        # Factoring F_next-F_current gives a quadratic. Resolve it analytically,
        # independently of production's bracketed search. Only classify roots in-band.
        A = 6e-6 * (q * q + q + 1)
        B = 0.06 * (q + 1)
        candidate = (B + math.sqrt(B * B + 380 * A)) / (2 * A)
        crossover = available and not fault and candidate <= 7400
        rpm = candidate if crossover else 7400.0
        samples = [2500 + 4900 * i / 120 for i in range(121)]
        errors = []
        for r in samples:
            used = _driveline_reference_torque(r if fault else r * q)
            required = _driveline_reference_torque(r * q)
            errors.append(abs(used - required) * b * 4.1 * 0.9 / 0.315)
        error = max(errors)
        fc, fn, _ = _driveline_reference_forces(a, b, 7400.0, fault)
        if available:
            current, nxt, post = _driveline_reference_forces(a, b, rpm, fault)
            speed = (rpm / 60) / (a * 4.1) * (2 * math.pi * 0.315)
            signature = [
                rpm,
                speed,
                current,
                nxt,
                post,
                nxt - current,
                float(error > 1e-10),
            ]
        else:
            signature = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
        return _driveline_fields(
            n,
            signature,
            decision_available=float(available),
            crossover=float(crossover),
            redline_limited=float(available and not crossover),
            gear_speed_ratio=q,
            maximum_lookup_force_error_n=error,
            redline_current_force_n=fc,
            redline_next_force_n=fn,
        )
    if n == 15:
        force = min(b, 1.05 * weight)
        energy = mass * a * a / 2
        distance = energy / force
        stop = 2 * distance / a
        rotor_fraction = 1.0 if fault else 0.85
        rotor = energy * rotor_fraction
        other = energy * 0.15
        transfer = force * 0.5 / 2.57
        front = weight * 0.53 + transfer
        rear = weight * 0.47 - transfer
        signature = [
            force,
            a / stop,
            distance,
            stop,
            energy,
            rotor / 12880,
            front,
            rear,
            float(fault or rear < 0),
        ]
        return _driveline_fields(
            n,
            signature,
            traction_limit_n=1.05 * weight,
            stopping_work_j=energy,
            rotor_heat_j=rotor,
            other_heat_j=other,
            heat_residual_fraction=rotor_fraction + 0.15 - 1,
            work_residual_fraction=0.0,
            load_transfer_n=transfer,
            normal_load_residual_n=0.0,
            pitch_moment_residual_nm=0.0,
        )
    if n == 16:
        pressure = 0.6125 * a**2
        drag_area = (650 + 1.5 * b * b) / 1000
        down_area = (300 + 45 * b) / 1000
        drag = pressure * drag_area * (-1 if fault else 1)
        down = pressure * down_area
        share = 1.2 if fault else (480 + 6 * b) / 1000
        front = share * down
        rear = down - front
        fn = weight * 0.53 + front
        rn = weight * 0.47 + rear
        capacity = weight + down
        signature = [
            pressure,
            drag,
            down,
            capacity,
            drag * a,
            share,
            float(drag < 0 or share > 1 or share < 0),
        ]
        return _driveline_fields(
            n,
            signature,
            drag_area_m2=drag_area,
            downforce_area_m2=down_area,
            front_aero_n=front,
            rear_aero_n=rear,
            front_normal_n=fn,
            rear_normal_n=rn,
            aero_allocation_residual_n=0.0,
            normal_load_residual_n=0.0,
            drag_model_residual_n=drag - pressure * drag_area,
        )
    raise ValueError("Reference covers only Vehicle P13-P16")


def vehicle_driveline_reference(number, primary, secondary, broken=False):
    n, a, b, fault = number, primary, secondary, broken
    physical = _vehicle_driveline_reference_state(n, a, b, fault)
    if n == 13:
        xs = [0.8 + 3.4 * i / 60 for i in range(61)]
        states = [_vehicle_driveline_reference_state(n, a, g, fault) for g in xs]
        response = {
            "x": xs,
            "series": [
                [s[k] for s in states]
                for k in [
                    "requested_wheel_force_n",
                    "applied_wheel_force_n",
                    "traction_limit_n",
                ]
            ],
        }
    elif n == 14:
        xs = [2500 + 4900 * i / 120 for i in range(121)]
        values = [_driveline_reference_forces(a, b, r, fault) for r in xs]
        response = {
            "x": xs,
            "series": [[v[0] for v in values], [v[1] for v in values]],
            "post_shift_rpm": [v[2] for v in values],
            "next_torque_lookup_rpm": [r if fault else r * (b / a) for r in xs],
        }
    elif n == 15:
        # Parameterize by fraction of stopping time. Kinetic-energy loss supplies heat.
        u = [i / 60 for i in range(61)]
        energy = 1320 * a * a / 2
        force = min(b, 1.05 * 1320 * 9.81)
        distance = energy / force
        stop = 2 * distance / a
        velocity = [a * (1 - v) for v in u]
        remaining = [energy * (1 - v) ** 2 for v in u]
        work = [energy * (2 * v - v * v) for v in u]
        fraction = 1.0 if fault else 0.85
        response = {
            "x": [stop * v for v in u],
            "series": [velocity],
            "distance_m": [distance * (2 * v - v * v) for v in u],
            "remaining_kinetic_energy_j": remaining,
            "stopping_work_j": work,
            "braking_power_w": [force * v for v in velocity],
            "rotor_heat_j": [fraction * w for w in work],
            "other_heat_j": [0.15 * w for w in work],
            "rotor_temperature_rise_c": [fraction * w / 12880 for w in work],
        }
    else:
        xs = [10 + i for i in range(61)]
        states = [_vehicle_driveline_reference_state(n, v, b, fault) for v in xs]
        response = {
            "x": xs,
            "series": [
                [s[k] for s in states]
                for k in ["drag_n", "downforce_n", "front_aero_n", "rear_aero_n"]
            ],
        }
    return {
        "physical": physical,
        "response": response,
        "signature": physical["signature"],
    }
