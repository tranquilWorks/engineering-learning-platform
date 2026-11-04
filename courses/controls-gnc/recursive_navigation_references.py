"""Independent formulations for new recursive and local-navigation sequences.

No production imports, retained signatures or production-generated inputs.
Scalar UKF moments use symmetric sums; EKF uses information conditioning.
Navigation uses scipy Rotation matrices, block conditioning and a separate
normal-equation pseudorange solver. References retain the declared midpoint
mechanization and second-order discrete error dynamics, not a different plant.
"""

from math import cos, sin, sqrt

import numpy as np
from scipy.spatial.transform import Rotation


def recursive(sigma, initial, alpha, method, broken):
    truth, x, p = 0.8, initial, sigma * sigma
    history = []
    for k in range(1, 81):
        u = 0.05 * cos(0.2 * k)
        truth = 0.94 * truth + 0.08 * sin(truth) + u + 0.015 * sin(0.7 * k)
        z = 0.4 * truth + 0.1 * truth**2 + 0.08 * cos(0.9 * k)

        def f(a, forcing=u):
            return 0.94 * a + 0.08 * sin(a) + forcing

        if method == "EKF":
            m = f(x)
            v = (0.94 + 0.08 * cos(x)) ** 2 * p + 0.0004
            h = 0 if broken else 0.4 + 0.2 * m
            predicted = 0.4 * m + 0.1 * m * m
            s = h * h * v + 0.01
            cross = v * h
            post = 1 / (1 / v + h * h / 0.01)
            innovation = z - predicted
            gain = post * h / 0.01
            x = m + gain * innovation
            p = post
        else:
            spread = alpha * sqrt(p)
            weights = [1 - 1 / alpha**2, 1 / (2 * alpha**2), 1 / (2 * alpha**2)]
            values = [f(x), f(x + spread), f(x - spread)]
            m = sum(w * y for w, y in zip(weights, values))
            wc = [weights[0] + 3 - alpha * alpha, weights[1], weights[2]]
            v = sum(w * (y - m) ** 2 for w, y in zip(wc, values)) + 0.0004
            # Analytic moments of the 3-point quadratic measurement transform.
            predicted = 0.4 * m + 0.1 * (m * m + v)
            cross = (0.4 + 0.2 * m) * v
            s = (0.4 + 0.2 * m) ** 2 * v + 0.02 * v * v + 0.01
            innovation = z - predicted
            gain = 0 if broken else cross / s
            x = m + gain * innovation
            p = v if broken else v - cross * cross / s
        history.append(
            [
                k,
                truth,
                z,
                m,
                v,
                predicted,
                innovation,
                s,
                gain,
                x,
                p,
                innovation**2 / s,
                (x - truth) ** 2 / p,
            ]
        )
    return np.array(history)


def cross_matrix(v):
    return np.cross(v, np.eye(3).T).T


def propagate(state, omega, force, dt):
    p, v, r, ba, bg = state
    half = Rotation.from_rotvec((omega - bg) * dt / 2).as_matrix()
    a = r @ half @ (force - ba) - np.array([0, 0, 9.80665])
    return (
        p + dt * (v + 0.5 * dt * a),
        v + dt * a,
        r @ half @ half,
        ba.copy(),
        bg.copy(),
    )


def transition(r, omega, force, dt):
    # Apply the continuous linear operator to each basis vector, then its
    # second application; independent of the production matrix assembly.
    def operator(e):
        _, dv, da, db, dg = np.split(e, 5)
        return np.r_[
            dv,
            -r @ np.cross(force, da) - r @ db,
            -np.cross(omega, da) - dg,
            np.zeros(6),
        ]

    basis = np.eye(15)
    return np.column_stack(
        [b + dt * operator(b) + dt * dt / 2 * operator(operator(b)) for b in basis]
    )


def gnss(position, t):
    satellites = np.array(
        [
            [16000, 12000, 21000],
            [-18000, 11000, 22000],
            [14000, -19000, 23000],
            [-13000, -16000, 20000],
            [2000, 3000, 26000],
            [24000, -2000, 12000],
        ],
        float,
    )
    obs = np.array(
        [
            np.linalg.norm(position - s) + 75 + 0.03 * sin(t + i)
            for i, s in enumerate(satellites)
        ]
    )
    x = np.zeros(4)
    for _ in range(9):
        norms = np.array([np.linalg.norm(x[:3] - s) for s in satellites])
        a = np.array([np.r_[(x[:3] - s) / d, 1] for s, d in zip(satellites, norms)])
        dx = np.linalg.solve(a.T @ a, a.T @ (obs - norms - x[3]))
        x += dx
        if np.linalg.norm(dx) < 1e-9:
            break
    return x


def condition(state, p, measurement, inject):
    precision = np.linalg.solve(p, np.eye(15))
    precision[:3, :3] += 4 * np.eye(3)
    post = np.linalg.solve(precision, np.eye(15))
    delta = post[:, :3] @ (4 * (measurement - state[0]))
    s = p[:3, :3] + 0.25 * np.eye(3)
    innovation = measurement - state[0]
    reset = np.eye(15)
    if inject:
        position, velocity, r, ba, bg = state
        state = (
            position + delta[:3],
            velocity + delta[3:6],
            r @ Rotation.from_rotvec(delta[6:9]).as_matrix(),
            ba + delta[9:12],
            bg + delta[12:15],
        )
        reset[6:9, 6:9] -= 0.5 * cross_matrix(delta[6:9])
    return (
        state,
        reset @ post @ reset.T,
        float(innovation @ np.linalg.solve(s, innovation)),
    )


def navigation(
    duration=30.0,
    bias=0.03,
    interval=1.0,
    walk=0.01,
    dropout=0.0,
    turn_limit=12.0,
    mode="fusion",
    broken=False,
):
    count = 240 if mode == "coast" else 300
    dt = duration / count
    pt = np.array([0.0, 1.0, 0.0])
    vt = np.zeros(3)
    rt = np.eye(3)
    state = (pt.copy(), vt.copy(), rt.copy(), np.zeros(3), np.zeros(3))
    unaided = tuple(a.copy() for a in state)
    p = np.diag([1.0] * 3 + [0.25] * 3 + [0.0004] * 3 + [0.0025] * 3 + [0.000025] * 3)
    ba = np.array([bias, -bias / 2, bias / 4])
    bg = np.array([0.0004, -0.0003, 0.0006])
    points = np.array([[0, 0], [20, 0], [20, 15], [0, 15]], float)
    heading = 0
    leg = 0
    last = 0
    due = interval
    rows = []
    covariances = []
    for j in range(count):
        t = j * dt
        age = t - last
        hold = mode == "survey" and age > 3 and not broken
        if mode == "survey":
            begin, end = points[leg : leg + 2]
            length = np.linalg.norm(end - begin)
            direction = (end - begin) / length
            along = (state[0][:2] - begin) @ direction
            if along >= length - 1 and leg < 2:
                leg += 1
                begin, end = points[leg : leg + 2]
                length = np.linalg.norm(end - begin)
                direction = (end - begin) / length
                along = (state[0][:2] - begin) @ direction
            target = begin + min(max(along + 4, 0), length) * direction
            wanted = np.arctan2(target[1] - state[0][1], target[0] - state[0][0])
            yaw = np.arctan2(state[2][1, 0], state[2][0, 0])
            error = wanted - yaw
            turn = 1.5 * np.arctan2(sin(error), cos(error))
            if not broken:
                turn = min(max(turn, -np.deg2rad(turn_limit)), np.deg2rad(turn_limit))
            heading += turn * dt
            desired = (
                np.zeros(3)
                if hold
                else np.array([2 * cos(heading), 2 * sin(heading), 0])
            )
            acc = np.clip((desired - vt) / 0.35, -3, 3)
            omega = np.array([0, 0, turn])
        else:
            acc = np.array(
                [0.1 * cos(0.3 * t), 0.08 * sin(0.2 * t), 0.03 * cos(0.4 * t)]
            )
            omega = np.array([0.025 * cos(0.4 * t), 0.02 * sin(0.3 * t), 0.04])
            turn = omega[2]
            hold = False
        half = Rotation.from_rotvec(omega * dt / 2).as_matrix()
        force = (rt @ half).T @ (acc + np.array([0, 0, 9.80665]))
        rt = rt @ half @ half
        pt += dt * (vt + 0.5 * dt * acc)
        vt += dt * acc
        wm = omega + bg
        fm = force + ba
        unaided = propagate(unaided, wm, fm, dt)
        if mode == "coast":
            state = (
                *state[:3],
                ba * (0 if broken else 0.95),
                bg * (0 if broken else 0.95),
            )
        phi = transition(state[2], wm - state[4], fm - state[3], dt)
        state = propagate(state, wm, fm, dt)
        p = phi @ p @ phi.T + dt * np.diag(
            [0.0] * 3 + [0.0004] * 3 + [0.000001] * 3 + [walk * walk] * 3 + [1e-8] * 3
        )
        now = (j + 1) * dt
        nis = 0
        updated = False
        if mode != "coast" and now + 1e-9 >= due:
            due += interval
            if not 5 <= now < 5 + dropout:
                state, p, nis = condition(state, p, gnss(pt, now)[:3], not broken)
                last = now
                updated = True
        q = Rotation.from_matrix(state[2]).as_quat(scalar_first=True)
        if q[0] < 0:
            q = -q
        angle = np.arccos(np.clip((np.trace(state[2].T @ rt) - 1) / 2, -1, 1))
        lateral = (
            abs(direction[0] * (pt[1] - begin[1]) - direction[1] * (pt[0] - begin[0]))
            if mode == "survey"
            else 0
        )
        rows.append(
            [
                now,
                *pt,
                *state[0],
                *vt,
                *state[1],
                *q,
                np.linalg.norm(state[0] - pt),
                np.linalg.norm(unaided[0] - pt),
                angle,
                np.sqrt(np.trace(p[:3, :3])),
                now - last,
                float(updated),
                nis,
                float(hold),
                np.rad2deg(turn),
                lateral,
                np.linalg.norm(vt),
                *state[3],
                *state[4],
            ]
        )
        covariances.append(p.copy())
    return np.array(rows), np.array(covariances)
