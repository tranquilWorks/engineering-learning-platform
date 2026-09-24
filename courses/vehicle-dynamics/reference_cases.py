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
}


def evaluate(
    item_id: str, primary: float, secondary: float, broken: bool = False
) -> list[float]:
    return _MODELS[item_id](float(primary), float(secondary), bool(broken))
