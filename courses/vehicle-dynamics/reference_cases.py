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


_MODELS = {
    "P01": _p01,
    "P02": _p02,
    "P03": _p03,
    "P04": _p04,
    "P05": _p05,
    "P06": _p06,
    "P07": _p07,
    "P08": _p08,
}


def evaluate(
    item_id: str, primary: float, secondary: float, broken: bool = False
) -> list[float]:
    return _MODELS[item_id](float(primary), float(secondary), bool(broken))
