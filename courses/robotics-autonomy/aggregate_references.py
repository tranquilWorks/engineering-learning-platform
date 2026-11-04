"""Independent aggregate references: no production imports or result inputs."""

from __future__ import annotations

import numpy as np
from scipy.optimize import least_squares
from scipy.sparse import lil_matrix


def joint_slam(count: int, noise: float, broken: bool = False):
    """Complex-coordinate residuals with numerical derivatives and TRF/LSMR.

    Production instead uses explicit real Jacobians and Gauss-Newton line search.
    A fixed first pose removes the gauge for this reference; compare free-gauge
    production results after rigid alignment, never their arbitrary absolute frame.
    """
    angles = np.linspace(0, 2 * np.pi, count)
    truth = 3 * np.cos(angles) + 2j * np.sin(angles)
    headings = angles + np.pi / 2
    true_map = np.array([-0.8 + 0.4j, 0.9 - 0.6j, 0.1 + 1.1j])
    k = np.arange(count - 1)
    odom = (truth[1:] - truth[:-1]) * np.exp(-1j * headings[:-1]) + 0.006 * (
        np.sin(k) + 1j * np.cos(1.3 * k)
    )
    turns = np.diff(headings) + 0.0012 * np.sin(0.8 * k)
    observations = np.array(
        [
            [
                (l - truth[i]) * np.exp(-1j * headings[i])
                + 0.004 * (np.sin(0.7 * i + j) + 1j * np.cos(1.1 * i - j))
                for j, l in enumerate(true_map)
            ]
            for i in range(count)
        ]
    )
    initial_poses = np.column_stack(
        (
            truth.real + 0.12 * np.sin(1.7 * angles),
            truth.imag + 0.12 * np.cos(1.3 * angles),
            headings + 0.05 * np.sin(angles),
        )
    )
    initial_map = np.column_stack((true_map.real + 0.16, true_map.imag - 0.12))
    initial = np.r_[initial_poses.ravel(), initial_map.ravel()]
    prior = np.array([truth[0].real, truth[0].imag, headings[0]])

    def residual(x):
        poses = x[: 3 * count].reshape(-1, 3)
        z = poses[:, 0] + 1j * poses[:, 1]
        theta = poses[:, 2]
        maps = x[3 * count :].reshape(-1, 2)
        lm = maps[:, 0] + 1j * maps[:, 1]
        delta = (z[1:] - z[:-1]) * np.exp(-1j * theta[:-1]) - odom
        closing = (z[-1] - z[0]) * np.exp(-1j * theta[0]) - (noise - 0.5j * noise)
        obs = (lm[None, :] - z[:, None]) * np.exp(-1j * theta[:, None]) - observations
        return np.r_[
            (poses[0] - prior) / 0.01,
            np.column_stack(
                (delta.real / 0.03, delta.imag / 0.03, (np.diff(theta) - turns) / 0.015)
            ).ravel(),
            closing.real / max(noise, 0.02),
            closing.imag / max(noise, 0.02),
            (theta[-1] - theta[0] - 2 * np.pi) / 0.02,
            np.stack((obs.real / 0.025, obs.imag / 0.025), axis=-1).ravel(),
        ]

    pattern = lil_matrix((3 + 3 * (count - 1) + 3 + 6 * count, len(initial)))
    pattern[:3, :3] = 1
    row = 3
    for i in range(count - 1):
        pattern[row : row + 3, 3 * i : 3 * i + 6] = 1
        row += 3
    pattern[row : row + 3, :3] = 1
    pattern[row : row + 3, 3 * count - 3 : 3 * count] = 1
    row += 3
    for i in range(count):
        for j in range(3):
            pattern[row : row + 2, 3 * i : 3 * i + 3] = 1
            pattern[row : row + 2, 3 * count + 2 * j : 3 * count + 2 * j + 2] = 1
            row += 2
    solved = least_squares(
        residual,
        initial,
        jac="3-point",
        jac_sparsity=pattern.tocsr(),
        ftol=1e-12,
        xtol=1e-12,
        gtol=1e-10,
        max_nfev=100,
        tr_options={"atol": 1e-13, "btol": 1e-13},
    )
    assert solved.success, solved.message
    return {
        "poses": solved.x[: 3 * count].reshape(count, 3),
        "landmarks": solved.x[3 * count :].reshape(3, 2),
        "cost": float(solved.fun @ solved.fun),
        "free_gauge_requested": broken,
    }


def manipulation(noise_cm, yaw_error_deg=0.8, friction=0.5, broken=False):
    """Independent point-Jacobian dynamics, adaptive DOP853 and discrete guards.

    No production imports. Mass and gravity are assembled from Cartesian point
    Jacobians, rather than the expanded two-link matrix in the experiment.
    """
    from scipy.integrate import solve_ivp

    def endpoint(q):
        return 0.75 * np.exp(1j * q[0]) + 0.55 * np.exp(1j * sum(q))

    def inverse(z):
        elbow = -np.arccos((abs(z) ** 2 - 0.75**2 - 0.55**2) / (0.825))
        return np.array(
            [np.angle(z) - np.angle(0.75 + 0.55 * np.exp(1j * elbow)), elbow]
        )

    actual = 0.28 + 0.12j + (0.72 + 0.18j) * np.exp(1j * np.deg2rad(25))
    sensor = 0.72 + 0.18j + noise_cm * (0.006 - 0.0035j)
    estimated = (
        sensor
        if broken
        else 0.28 + 0.12j + sensor * np.exp(1j * np.deg2rad(25 + yaw_error_deg))
    )
    drop = 0.5 + 0.55j
    obj = actual
    offset = 0j
    y = np.array([0.2, -1.2, 0.0, 0.0])
    goal = y[:2].copy()
    phase = 0
    entered = 0.0
    force = 0.0
    held = False
    events = []
    rows = []
    failure = ""
    success = False

    def rhs(t, y):
        q, v = y[:2], y[2:]
        a = 0.75 * np.exp(1j * q[0])
        b = 0.55 * np.exp(1j * sum(q))
        J1 = np.array([1j * a, 0j])
        J2 = np.array([1j * (a + b), 1j * b])
        m2 = 0.7 + (0.45 if held else 0.0)
        mass = np.real(np.outer(J1.conj(), J1) + m2 * np.outer(J2.conj(), J2))
        bias1 = -a * v[0] ** 2
        bias2 = bias1 - b * sum(v) ** 2
        bias = np.real(J1.conj() * bias1 + m2 * J2.conj() * bias2)
        gravity = 9.81 * (J1.imag + m2 * J2.imag)
        torque = np.clip(
            mass @ (36 * (goal - q) - 12 * v) + bias + gravity + 0.025 * v, -25, 25
        )
        return np.r_[v, np.linalg.solve(mass, torque - bias - gravity - 0.025 * v)]

    for tick in range(2401):
        t = tick / 100
        tip = endpoint(y[:2])
        prior = phase
        settled = np.linalg.norm(y[:2] - goal) < 0.005 and np.linalg.norm(y[2:]) < 0.015
        if phase == 0:
            phase = 1
        elif phase == 1:
            if not 0.2 <= abs(estimated) <= 1.3:
                failure = "unreachable estimated pickup"
                phase = 9
            else:
                goal = inverse(estimated)
                phase = 2
        elif phase == 2 and settled:
            phase = 3
        elif phase == 3:
            force = min(10, force + 0.3)
            if force >= 10:
                phase = 4
        elif phase == 4:
            if abs(tip - actual) > 0.055:
                failure = "gripper missed object"
                phase = 9
            elif 2 * friction * force < 0.45 * 9.81:
                failure = "insufficient vertical grasp support"
                phase = 9
            elif abs(estimated + 0.12j) > 1.3:
                failure = "unreachable lift"
                phase = 9
            else:
                held = True
                offset = actual - tip
                goal = inverse(estimated + 0.12j)
                phase = 5
        elif phase == 5 and settled:
            goal = inverse(drop - offset)
            phase = 6
        elif phase == 6 and settled:
            phase = 7
        elif phase == 7:
            held = False
            force = max(0, force - 0.3)
            if force <= 0:
                goal = inverse(drop + 0.15j)
                phase = 8
        elif phase == 8 and settled:
            phase = 10
            success = abs(obj - drop) < 0.02
            if not success:
                failure = "placement outside tolerance"
        if phase not in (9, 10) and t - entered > 5:
            failure = "phase timeout"
            phase = 9
        if phase != prior:
            events.append(
                [t, prior, phase, abs(tip - actual), 2 * friction * force - 0.45 * 9.81]
            )
            entered = t
        if tick % 5 == 0 or phase in (9, 10):
            rows.append(
                [
                    t,
                    phase,
                    *y,
                    tip.real,
                    tip.imag,
                    obj.real,
                    obj.imag,
                    force,
                    float(held),
                    abs(obj - drop),
                ]
            )
        if phase in (9, 10):
            break
        y = solve_ivp(rhs, (t, t + 0.01), y, method="DOP853", rtol=2e-10, atol=2e-12).y[
            :, -1
        ]
        if held:
            obj = endpoint(y[:2]) + offset
    return {
        "history": np.asarray(rows),
        "events": np.asarray(events),
        "success": bool(success),
        "failure": failure,
        "placement_error_m": abs(obj - drop),
    }
