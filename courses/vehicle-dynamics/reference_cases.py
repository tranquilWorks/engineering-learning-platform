from __future__ import annotations

# Independent scalar oracle: imports no production experiment and consumes no production result.
import math


def _p01(a: float, b: float, broken: bool) -> list[float]:
    delta = math.radians(a)
    speed = b
    L = 2.57
    ratio = 13.0
    mu = 1.0
    curvature = math.tan(delta / ratio) / L
    yaw = speed * curvature
    ay = speed * yaw
    limit = mu * 9.81
    if broken:
        ay *= 1.35
    return [curvature, yaw, ay, limit, float(abs(ay) > limit)]


def _p02(a: float, b: float, broken: bool) -> list[float]:
    request = a
    speed = b
    mass = 1320.0
    mu = 1.0
    rolling = 0.015 * mass * 9.81
    drag = 0.5 * 1.225 * 0.31 * 2.0 * speed**2
    limit = mu * mass * 9.81
    applied = request if broken else min(request, limit)
    accel = (applied - rolling - drag) / mass
    return [applied, rolling, drag, accel, limit, float(request > limit)]


def _p03(a: float, b: float, broken: bool) -> list[float]:
    accel = a
    height = b
    mass = 1320.0
    g = 9.81
    L = 2.57
    front0 = 0.53 * mass * g
    transfer = mass * accel * height / L
    front = front0 - transfer
    rear = mass * g - front
    if broken:
        front -= 0.65 * mass * g
        rear = mass * g - front
    return [front, rear, transfer, front + rear, float(min(front, rear) < 0)]


def _p04(a: float, b: float, broken: bool) -> list[float]:
    fx = a
    fy = b
    capacity = 1.05 * 3600.0
    use = math.hypot(fx, fy) / capacity
    scale = 1.0 if broken or use <= 1 else 1 / use
    return [fx * scale, fy * scale, use, capacity, float(use > 1)]


def _p05(a: float, b: float, broken: bool) -> list[float]:
    kappa = a
    load = b
    mu = 1.05
    stiffness = 85000.0
    force = mu * load * math.tanh(stiffness * kappa / (mu * load))
    if broken:
        force = -force
    return [kappa, force, mu * load, stiffness, float(broken)]


def _p06(a: float, b: float, broken: bool) -> list[float]:
    alpha = math.radians(a)
    load = b
    mu = 1.05
    stiffness = 78000.0
    force = -mu * load * math.tanh(stiffness * alpha / (mu * load))
    if broken:
        force = -force
    return [alpha, force, mu * load, stiffness, float(broken)]


def _p07(a: float, b: float, broken: bool) -> list[float]:
    delta = math.radians(a)
    speed = b
    mass = 1320.0
    lf = 1.15
    lr = 1.42
    cf = 90000.0
    cr = 100000.0
    aa = -(cf + cr) / speed
    ab = (-lf * cf + lr * cr) / speed - mass * speed
    ba = -lf * cf + lr * cr
    bb = -(lf**2 * cf + lr**2 * cr)
    det = aa * bb - ab * ba
    q1 = -cf * delta
    q2 = -lf * cf * delta
    beta = (q1 * bb - ab * q2) / det
    yaw = (aa * q2 - q1 * ba) / det
    af = delta - beta - lf * yaw / speed
    ar = -beta + lr * yaw / speed
    invalid = max(abs(af), abs(ar), abs(delta)) > math.radians(8) or broken
    return [beta, yaw, af, ar, mass * speed * yaw, float(invalid)]


def _p08(a: float, b: float, broken: bool) -> list[float]:
    cf = a
    cr = b
    mass = 1320.0
    lf = 1.15
    lr = 1.42
    L = lf + lr
    speed = 25.0
    k = mass / L * (lr / cf - lf / cr)
    critical = math.sqrt(-L / k) if k < 0 else 0.0
    denominator = L + k * speed**2
    if broken and k < 0:
        speed = max(speed, critical * 1.05)
        denominator = L + k * speed**2
    return [
        k,
        math.degrees(k * 9.81),
        critical,
        speed,
        denominator,
        float(denominator <= 0),
    ]


def _p09(a: float, b: float, broken: bool) -> list[float]:
    sprung_mass = 300.0
    effective_rate = a * (b if broken else b * b)
    angular_frequency = (effective_rate / sprung_mass) ** 0.5
    static_travel = sprung_mass * 9.81 / effective_rate
    return [
        effective_rate,
        angular_frequency / (2.0 * math.pi),
        static_travel,
        a,
        b,
        float(broken),
    ]


def _p10(a: float, b: float, broken: bool) -> list[float]:
    mass = 300.0
    coefficient = -a if broken else a
    natural_rad_s = (b / mass) ** 0.5
    critical = 2.0 * (b * mass) ** 0.5
    ratio = coefficient / critical
    damped_hz = natural_rad_s * max(0.0, 1.0 - ratio * ratio) ** 0.5 / (2.0 * math.pi)
    if 0.0 < ratio < 1.0:
        overshoot = math.exp(-math.pi * ratio / (1.0 - ratio * ratio) ** 0.5)
    else:
        overshoot = 0.0 if ratio >= 1.0 else 1.0
    settling = 4.0 / (ratio * natural_rad_s) if ratio > 0.0 else 0.0
    return [
        natural_rad_s / (2.0 * math.pi),
        ratio,
        damped_hz,
        overshoot,
        settling,
        ratio * natural_rad_s,
        float(ratio <= 0.0),
    ]


def _p11(a: float, b: float, broken: bool) -> list[float]:
    rear_rate = -b if broken else b
    applied_moment = 1320.0 * 7.0 * 0.50
    rate_sum = a + rear_rate
    roll_angle = applied_moment / rate_sum if abs(rate_sum) > 1e-12 else 0.0
    front_force_delta = a * roll_angle / 1.53
    rear_force_delta = rear_rate * roll_angle / 1.53
    front_moment = front_force_delta * 1.53
    rear_moment = rear_force_delta * 1.53
    front_fraction = front_moment / applied_moment
    return [
        roll_angle,
        front_force_delta,
        rear_force_delta,
        front_fraction,
        front_moment + rear_moment - applied_moment,
        front_fraction - 0.53,
        float(a <= 0.0 or rear_rate <= 0.0 or rate_sum <= 0.0),
    ]


def _p12(a: float, b: float, broken: bool) -> list[float]:
    gamma = a if broken else a * math.pi / 180.0
    toe = b if broken else b * math.pi / 180.0
    lateral_force = -60000.0 * gamma
    parasitic_force = 3600.0 * abs(math.sin(toe) / math.cos(toe))
    return [
        gamma,
        toe,
        lateral_force,
        parasitic_force,
        parasitic_force * 20.0,
        toe,
        float(broken),
    ]


def _p13(a: float, b: float, broken: bool) -> list[float]:
    final_ratio = 4.10
    eta = 1.0 if broken else 0.90
    tire_radius = 0.315
    velocity = 20.0
    shaft_rad_s = velocity * b * final_ratio / tire_radius
    engine_rpm = shaft_rad_s * 30.0 / math.pi
    demanded_force = a * b * final_ratio * eta / tire_radius
    available_force = 1320.0 * 9.81
    delivered_force = demanded_force if broken else min(demanded_force, available_force)
    output_power = delivered_force * velocity
    transmitted_power = a * shaft_rad_s * eta
    return [
        engine_rpm,
        demanded_force,
        delivered_force,
        available_force,
        output_power,
        output_power - transmitted_power,
        float(broken),
    ]


def _shift_torque(engine_rpm: float) -> float:
    return max(120.0, 245.0 - 0.000006 * (engine_rpm - 5000.0) ** 2)


def _p14(a: float, b: float, broken: bool) -> list[float]:
    next_ratio = a * 1.10 if broken else b
    redline = 7400.0
    chosen = redline
    for engine_rpm in [
        2500.0 + (redline - 2500.0) * step / 120.0 for step in range(121)
    ]:
        after_shift = engine_rpm * next_ratio / a
        if _shift_torque(after_shift) * next_ratio >= _shift_torque(engine_rpm) * a:
            chosen = engine_rpm
            break
    after_shift = chosen * next_ratio / a
    scale = 4.10 * 0.90 / 0.315
    before_force = _shift_torque(chosen) * a * scale
    after_force = _shift_torque(after_shift) * next_ratio * scale
    road_speed = chosen * math.pi / 30.0 * 0.315 / (a * 4.10)
    return [
        chosen,
        road_speed,
        before_force,
        after_force,
        after_shift,
        after_force - before_force,
        float(next_ratio >= a),
    ]


def _p15(a: float, b: float, broken: bool) -> list[float]:
    vehicle_mass = 1320.0
    gravity = 9.81
    force_limit = 1.05 * vehicle_mass * gravity
    brake_force = b if broken else min(b, force_limit)
    deceleration = brake_force / vehicle_mass
    distance = a * a / (2.0 * deceleration)
    duration = a / deceleration
    initial_energy = vehicle_mass * a * a / 2.0
    heat_fraction = 1.0 if broken else 0.85
    temperature_rise = heat_fraction * initial_energy / (28.0 * 460.0)
    load_shift = vehicle_mass * deceleration * 0.50 / 2.57
    front_load = 0.53 * vehicle_mass * gravity + load_shift
    rear_load = vehicle_mass * gravity - front_load
    return [
        brake_force,
        deceleration,
        distance,
        duration,
        initial_energy,
        temperature_rise,
        front_load,
        rear_load,
        float(broken or rear_load < 0.0),
    ]


def _p16(a: float, b: float, broken: bool) -> list[float]:
    pressure = 1.225 * a * a / 2.0
    drag_area = 0.65 + 0.0015 * b * b
    lift_area = 0.30 + 0.045 * b
    resistance = pressure * drag_area
    vertical_load = pressure * lift_area
    front_fraction = 0.48 + 0.006 * b
    if broken:
        resistance = -resistance
        front_fraction = 1.20
    grip = 1320.0 * 9.81 + vertical_load
    return [
        pressure,
        resistance,
        vertical_load,
        grip,
        resistance * a,
        front_fraction,
        float(resistance < 0.0 or not 0.0 <= front_fraction <= 1.0),
    ]


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
