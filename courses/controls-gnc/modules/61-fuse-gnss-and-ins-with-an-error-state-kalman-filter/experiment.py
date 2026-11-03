from __future__ import annotations

import itertools
from typing import Any

import numpy as np

ITEM_NUMBER = 61
BROKEN_TEXT = "Broken mode computes updates and shrinks covariance but discards the state correction instead of injecting it."
RECOVERY_TEXT = "Restore injection and reset both controls. Check actual position error and bias estimate, not only the covariance drop."


def _trace(
    name: str,
    x: Any,
    y: Any,
    x_quantity: str,
    x_unit: str,
    y_quantity: str,
    y_unit: str,
    *,
    mode: str = "lines",
) -> dict[str, Any]:
    return {
        "type": "scatter",
        "mode": mode,
        "name": name,
        "x": np.asarray(x, dtype=float),
        "y": np.asarray(y, dtype=float),
        "meta": {
            "x_quantity": x_quantity,
            "x_unit": x_unit,
            "y_quantity": y_quantity,
            "y_unit": y_unit,
        },
    }


def _plot(
    title: str, x_title: str, y_title: str, traces: list[dict[str, Any]]
) -> dict[str, Any]:
    return {
        "data": traces,
        "layout": {
            "title": {"text": title, "x": 0.02},
            "xaxis": {"title": {"text": x_title}},
            "yaxis": {"title": {"text": y_title}},
            "legend": {"orientation": "h"},
            "margin": {"l": 72, "r": 36, "t": 62, "b": 62},
            "hovermode": "closest",
            "uirevision": "keep-view",
        },
        "config": {"responsive": True, "displaylogo": False},
    }


def _result(model: dict[str, Any], broken: bool) -> dict[str, Any]:
    return {
        "metrics": [
            {
                "id": key,
                "label": label,
                "value": float(value),
                "unit": unit,
                "emphasis": "primary" if index == 0 else "normal",
            }
            for index, (key, label, value, unit) in enumerate(model["metrics"])
        ],
        "plots": model["plots"],
        "explanations": {
            "observation": model["observation"],
            "broken": BROKEN_TEXT,
            "recovery": RECOVERY_TEXT,
        },
        "diagnostics": {
            "item_number": ITEM_NUMBER,
            **model.get("details", {}),
            "broken_active": bool(broken),
            "signature": [float(value) for value in model["signature"]],
        },
    }


def _model(p, broken):
    interval = float(p["gnss_interval_s"])
    q = float(p["bias_random_walk"])
    updates = np.arange(interval, 20.0 + 1e-9, interval)
    time = np.unique(np.round(np.r_[np.arange(0, 20.0001, 0.1), updates], 10))
    state = np.array([0.0, 2.0, 0.0])
    covariance = np.diag([1.0, 0.25, 0.0025])
    H = np.array([1.0, 0.0, 0.0])
    states = [state.copy()]
    covariances = [covariance.copy()]
    injections = []
    update_time = []
    pre_sigma = []
    post_sigma = []
    for t0, t in itertools.pairwise(time):
        dt = t - t0
        F = np.array([[1.0, dt, -(dt**2) / 2], [0.0, 1.0, -dt], [0.0, 0.0, 1.0]])
        Q = (
            q
            * q
            * np.array(
                [
                    [dt**5 / 20, dt**4 / 8, -(dt**3) / 6],
                    [dt**4 / 8, dt**3 / 3, -(dt**2) / 2],
                    [-(dt**3) / 6, -(dt**2) / 2, dt],
                ]
            )
        )
        acceleration = 0.04 - state[2]
        state[:2] += [state[1] * dt + 0.5 * acceleration * dt**2, acceleration * dt]
        covariance = F @ covariance @ F.T + Q
        if np.any(abs(updates - t) < 1e-8):
            pre_sigma.append(np.sqrt(covariance[0, 0]))
            update_time.append(t)
            innovation = 2 * t + 0.3 * np.sin(0.7 * t) - state[0]
            gain = covariance @ H / (H @ covariance @ H + 1.0)
            correction = gain * innovation
            if not broken:
                state += correction
            A = np.eye(3) - np.outer(gain, H)
            covariance = A @ covariance @ A.T + np.outer(gain, gain)
            injections.append(correction)
            post_sigma.append(np.sqrt(covariance[0, 0]))
        states.append(state.copy())
        covariances.append(covariance.copy())
    states = np.asarray(states)
    covariances = np.asarray(covariances)
    signature = [pre_sigma[-1], post_sigma[-1], abs(states[-1, 0] - 40.0)]
    return {
        "signature": signature,
        "metrics": [
            ("prior_sigma", "Last update prior position sigma", signature[0], "m"),
            (
                "posterior_sigma",
                "Last update posterior position sigma",
                signature[1],
                "m",
            ),
            ("terminal_error", "Terminal position error", signature[2], "m"),
            ("bias_error", "Terminal bias error", abs(states[-1, 2] - 0.04), "m/s^2"),
        ],
        "plots": {
            "response": _plot(
                "Injected state",
                "Time (s)",
                "Position (m)",
                [
                    _trace(
                        "Estimated position",
                        time,
                        states[:, 0],
                        "Time",
                        "s",
                        "Position",
                        "m",
                    ),
                    _trace("Truth", time, 2 * time, "Time", "s", "Position", "m"),
                ],
            ),
            "mechanism": _plot(
                "Error and formal sigma",
                "Time (s)",
                "Position error (m)",
                [
                    _trace(
                        "Actual error",
                        time,
                        states[:, 0] - 2 * time,
                        "Time",
                        "s",
                        "Position error",
                        "m",
                    ),
                    _trace(
                        "Formal sigma",
                        time,
                        np.sqrt(covariances[:, 0, 0]),
                        "Time",
                        "s",
                        "Position error",
                        "m",
                    ),
                ],
            ),
        },
        "details": {
            "time": time,
            "states": states,
            "covariances": covariances,
            "update_time": update_time,
            "injections": injections,
            "prior_sigma": pre_sigma,
            "posterior_sigma": post_sigma,
            "reset_error_state": np.zeros(3),
            "reset_jacobian": np.eye(3),
        },
        "observation": "This additive one-axis position/velocity/bias filter propagates covariance and injects each GNSS correction. Error coordinates reset to zero with identity reset Jacobian. Withholding injection can leave optimistic covariance beside actual position drift; this is not a full attitude ESKF.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _append_navigation(
        _result(_model(parameters, broken), broken), parameters, 61
    )


# The same bounded navigation kernel is embedded in P59/P61/P67 so each
# portable experiment's content identity covers every executed Python byte.
def _skew(v):
    x, y, z = v
    return np.array([[0.0, -z, y], [z, 0.0, -x], [-y, x, 0.0]])


def _quat_product(a, b):
    return np.r_[
        a[0] * b[0] - a[1:] @ b[1:],
        a[0] * b[1:] + b[0] * a[1:] + np.cross(a[1:], b[1:]),
    ]


def _quat_increment(rotation):
    angle = np.linalg.norm(rotation)
    return np.r_[np.cos(angle / 2), 0.5 * np.sinc(angle / (2 * np.pi)) * rotation]


def _rotation(q):
    w, v = q[0], q[1:]
    return (w * w - v @ v) * np.eye(3) + 2 * np.outer(v, v) + 2 * w * _skew(v)


def _mechanize(state, omega, force, dt):
    position, velocity, quaternion, accel_bias, gyro_bias = state
    increment = (omega - gyro_bias) * dt
    middle = _quat_product(quaternion, _quat_increment(increment / 2))
    acceleration = _rotation(middle) @ (force - accel_bias) + np.array(
        [0.0, 0.0, -9.80665]
    )
    quaternion = _quat_product(quaternion, _quat_increment(increment))
    quaternion /= np.linalg.norm(quaternion)
    return (
        position + velocity * dt + 0.5 * acceleration * dt * dt,
        velocity + acceleration * dt,
        quaternion,
        accel_bias.copy(),
        gyro_bias.copy(),
    )


def _nav_transition(quaternion, omega, force, dt):
    rotation = _rotation(quaternion)
    f = np.zeros((15, 15))
    f[:3, 3:6] = np.eye(3)
    f[3:6, 6:9] = -rotation @ _skew(force)
    f[3:6, 9:12] = -rotation
    f[6:9, 6:9] = -_skew(omega)
    f[6:9, 12:15] = -np.eye(3)
    return np.eye(15) + dt * f + 0.5 * dt * dt * (f @ f)


def _gnss_fix(position, time):
    # Local Cartesian constellation, receiver clock measured in meters.
    satellites = np.array(
        [
            [16000.0, 12000.0, 21000.0],
            [-18000.0, 11000.0, 22000.0],
            [14000.0, -19000.0, 23000.0],
            [-13000.0, -16000.0, 20000.0],
            [2000.0, 3000.0, 26000.0],
            [24000.0, -2000.0, 12000.0],
        ]
    )
    ranges = (
        np.linalg.norm(satellites - position, axis=1)
        + 75.0
        + 0.03 * np.sin(time + np.arange(6))
    )
    solution = np.zeros(4)
    for _ in range(7):
        d = solution[:3] - satellites
        distance = np.linalg.norm(d, axis=1)
        jacobian = np.column_stack((d / distance[:, None], np.ones(6)))
        correction = np.linalg.lstsq(
            jacobian, ranges - distance - solution[3], rcond=None
        )[0]
        solution += correction
        if np.linalg.norm(correction) < 1e-9:
            break
    return solution, ranges


def _nav_update(state, covariance, fix, inject=True):
    h = np.zeros((3, 15))
    h[:, :3] = np.eye(3)
    noise = np.eye(3) * 0.25
    innovation = fix - state[0]
    s = h @ covariance @ h.T + noise
    gain = np.linalg.solve(s, h @ covariance).T
    delta = gain @ innovation
    a = np.eye(15) - gain @ h
    updated = a @ covariance @ a.T + gain @ noise @ gain.T
    reset = np.eye(15)
    if inject:
        p, v, q, ba, bg = state
        q = _quat_product(q, _quat_increment(delta[6:9]))
        q /= np.linalg.norm(q)
        state = (p + delta[:3], v + delta[3:6], q, ba + delta[9:12], bg + delta[12:15])
        reset[6:9, 6:9] -= 0.5 * _skew(delta[6:9])
    updated = reset @ updated @ reset.T
    return (
        state,
        0.5 * (updated + updated.T),
        delta,
        float(innovation @ np.linalg.solve(s, innovation)),
    )


def _navigation_sequence(
    duration=30.0,
    bias=0.03,
    interval=1.0,
    walk=0.01,
    dropout=0.0,
    turn_limit=12.0,
    mode="fusion",
    broken=False,
):
    steps = 240 if mode == "coast" else 300
    dt = duration / steps
    truth_p = np.array([0.0, 1.0, 0.0])
    truth_v = np.zeros(3)
    truth_q = np.array([1.0, 0.0, 0.0, 0.0])
    heading = 0.0
    state = (truth_p.copy(), truth_v.copy(), truth_q.copy(), np.zeros(3), np.zeros(3))
    covariance = np.diag(
        [1.0] * 3 + [0.25] * 3 + [0.02**2] * 3 + [0.05**2] * 3 + [0.005**2] * 3
    )
    ba = np.array([bias, -0.5 * bias, 0.25 * bias])
    bg = np.array([0.0004, -0.0003, 0.0006])
    waypoints = np.array([[0.0, 0.0], [20.0, 0.0], [20.0, 15.0], [0.0, 15.0]])
    last_fix = 0.0
    next_fix = interval
    leg = 0
    rows = []
    matrices = []
    events = []
    inertial = tuple(x.copy() for x in state)
    for k in range(steps):
        t = k * dt
        # Guidance uses only the estimated state. Truth drives sensor simulation.
        age = t - last_fix
        hold = mode == "survey" and age > 3 and not broken
        if mode == "survey":
            start, finish = waypoints[leg : leg + 2]
            tangent = (finish - start) / np.linalg.norm(finish - start)
            along = (state[0][:2] - start) @ tangent
            if along >= np.linalg.norm(finish - start) - 1 and leg < 2:
                leg += 1
                start, finish = waypoints[leg : leg + 2]
                tangent = (finish - start) / np.linalg.norm(finish - start)
                along = (state[0][:2] - start) @ tangent
            target = (
                start + np.clip(along + 4, 0, np.linalg.norm(finish - start)) * tangent
            )
            estimated_yaw = np.arctan2(
                _rotation(state[2])[1, 0], _rotation(state[2])[0, 0]
            )
            error = (
                np.arctan2(target[1] - state[0][1], target[0] - state[0][0])
                - estimated_yaw
            )
            turn = 1.5 * np.arctan2(np.sin(error), np.cos(error))
            if not broken:
                turn = float(
                    np.clip(turn, -np.deg2rad(turn_limit), np.deg2rad(turn_limit))
                )
            heading += turn * dt
            desired = (
                np.array([2 * np.cos(heading), 2 * np.sin(heading), 0.0])
                if not hold
                else np.zeros(3)
            )
            # Finite acceleration; safe hold commands braking, not instantaneous stop.
            acceleration = np.clip((desired - truth_v) / 0.35, -3.0, 3.0)
            omega = np.array([0.0, 0.0, turn])
        else:
            acceleration = np.array(
                [0.1 * np.cos(0.3 * t), 0.08 * np.sin(0.2 * t), 0.03 * np.cos(0.4 * t)]
            )
            omega = np.array([0.025 * np.cos(0.4 * t), 0.02 * np.sin(0.3 * t), 0.04])
            turn = omega[2]
            hold = False
        middle = _quat_product(truth_q, _quat_increment(omega * dt / 2))
        force = _rotation(middle).T @ (acceleration - np.array([0.0, 0.0, -9.80665]))
        truth_q = _quat_product(truth_q, _quat_increment(omega * dt))
        truth_q /= np.linalg.norm(truth_q)
        truth_p = truth_p + truth_v * dt + 0.5 * acceleration * dt * dt
        truth_v = truth_v + acceleration * dt
        measured_omega = omega + bg
        measured_force = force + ba
        inertial = _mechanize(inertial, measured_omega, measured_force, dt)
        if mode == "coast":
            # Calibration comparison retains a declared 95% bias removal, not an estimated value.
            state = (
                state[0],
                state[1],
                state[2],
                np.zeros(3) if broken else 0.95 * ba,
                np.zeros(3) if broken else 0.95 * bg,
            )
        phi = _nav_transition(
            state[2], measured_omega - state[4], measured_force - state[3], dt
        )
        state = _mechanize(state, measured_omega, measured_force, dt)
        spectral = np.array(
            [0.0] * 3 + [0.02**2] * 3 + [0.001**2] * 3 + [walk**2] * 3 + [0.0001**2] * 3
        )
        covariance = phi @ covariance @ phi.T + np.diag(spectral) * dt
        nis = 0.0
        updated = False
        now = (k + 1) * dt
        if mode != "coast" and now + 1e-9 >= next_fix:
            next_fix += interval
            if not (5 <= now < 5 + dropout):
                fix, ranges = _gnss_fix(truth_p, now)
                before = state
                before_p = covariance.copy()
                state, covariance, delta, nis = _nav_update(
                    state, covariance, fix[:3], not broken
                )
                events.append(
                    {
                        "step": k + 1,
                        "prior_state": [x.tolist() for x in before],
                        "prior_covariance": before_p.tolist(),
                        "fix": fix.tolist(),
                        "ranges": ranges.tolist(),
                        "delta": delta.tolist(),
                        "posterior_state": [x.tolist() for x in state],
                        "posterior_covariance": covariance.tolist(),
                    }
                )
                last_fix = now
                updated = True
        orientation_error = _rotation(state[2]).T @ _rotation(truth_q)
        angle = np.arccos(np.clip((np.trace(orientation_error) - 1) / 2, -1, 1))
        cross = (
            abs(
                tangent[0] * (truth_p[1] - start[1])
                - tangent[1] * (truth_p[0] - start[0])
            )
            if mode == "survey"
            else 0.0
        )
        rows.append(
            [
                now,
                *truth_p,
                *state[0],
                *truth_v,
                *state[1],
                *state[2],
                np.linalg.norm(state[0] - truth_p),
                np.linalg.norm(inertial[0] - truth_p),
                angle,
                np.sqrt(np.trace(covariance[:3, :3])),
                now - last_fix,
                float(updated),
                nis,
                float(hold),
                np.rad2deg(turn),
                cross,
                np.linalg.norm(truth_v),
                *state[3],
                *state[4],
            ]
        )
        matrices.append(covariance.copy())
    return np.asarray(rows), np.asarray(matrices), events


def _append_navigation(result, parameters, number):
    mode = {59: "coast", 61: "fusion", 67: "survey"}[number]
    args = {"mode": mode, "broken": bool(parameters["broken_mode"])}
    if number == 59:
        args.update(
            duration=float(parameters["coast_duration_s"]),
            bias=float(parameters["accelerometer_bias_m_s2"]),
        )
    if number == 61:
        args.update(
            interval=float(parameters["gnss_interval_s"]),
            walk=float(parameters["bias_random_walk"]),
        )
    if number == 67:
        args.update(
            dropout=float(parameters["gnss_dropout_s"]),
            turn_limit=float(parameters["turn_rate_limit_deg_s"]),
        )
    h, covariance, events = _navigation_sequence(**args)
    result["diagnostics"]["navigation_columns"] = [
        "time_s",
        "true_x",
        "true_y",
        "true_z",
        "estimated_x",
        "estimated_y",
        "estimated_z",
        "true_vx",
        "true_vy",
        "true_vz",
        "estimated_vx",
        "estimated_vy",
        "estimated_vz",
        "qw",
        "qx",
        "qy",
        "qz",
        "position_error_m",
        "unaided_error_m",
        "attitude_error_rad",
        "position_sigma_norm_m",
        "gnss_age_s",
        "gnss_update",
        "nis",
        "hold",
        "turn_deg_s",
        "cross_track_m",
        "speed_m_s",
        "bax",
        "bay",
        "baz",
        "bgx",
        "bgy",
        "bgz",
    ]
    result["diagnostics"]["navigation_history"] = h
    result["diagnostics"]["navigation_covariances"] = covariance
    result["diagnostics"]["navigation_updates"] = events
    result["plots"]["navigation_error"] = _plot(
        "3D navigation error",
        "Time (s)",
        "Position error (m)",
        [
            _trace("Estimated", h[:, 0], h[:, 17], "Time", "s", "Position error", "m"),
            _trace("Unaided", h[:, 0], h[:, 18], "Time", "s", "Position error", "m"),
        ],
    )
    result["plots"]["navigation_attitude"] = _plot(
        "Attitude propagation",
        "Time (s)",
        "Attitude error (deg)",
        [
            _trace(
                "Rotation error",
                h[:, 0],
                np.rad2deg(h[:, 19]),
                "Time",
                "s",
                "Attitude error",
                "deg",
            )
        ],
    )
    result["metrics"].append(
        {
            "id": "navigation_terminal_error",
            "label": "3D terminal position error",
            "value": float(h[-1, 17]),
            "unit": "m",
        }
    )
    result["explanations"]["observation"] += (
        " The additional 3D sequence executes body-to-local quaternion propagation, specific-force rotation and gravity compensation. "
        + (
            "Calibration removes a declared 95% of biases; it is not an estimator."
            if number == 59
            else "A 15-state right-error filter couples position, velocity, attitude and IMU biases with pseudorange-derived GNSS fixes, Joseph covariance updates, injection and attitude reset."
        )
        + " Local flat-Earth synthetic scope excludes Earth rotation, ellipsoidal transport, real receivers and hardware."
    )
    if number == 67:
        result["plots"]["integrated_path"] = _plot(
            "Fused survey path",
            "East position (m)",
            "North position (m)",
            [
                _trace(
                    "Truth",
                    h[:, 1],
                    h[:, 2],
                    "East position",
                    "m",
                    "North position",
                    "m",
                ),
                _trace(
                    "Fused estimate",
                    h[:, 4],
                    h[:, 5],
                    "East position",
                    "m",
                    "North position",
                    "m",
                ),
            ],
        )
        result["explanations"]["broken"] += (
            " The 3D sequence also withholds nominal-state correction, retaining a formal covariance update; this deliberately violates estimator consistency."
        )
    selected = sorted({0, 1, *range(9, len(h), 30), len(h) - 1})
    result.setdefault("tables", {})["integration_evidence"] = {
        "columns": [
            "Time (s)",
            "Error (m)",
            "Sigma norm (m)",
            "Attitude error (deg)",
            "GNSS age (s)",
            "Fix applied",
        ],
        "rows": [
            {
                "Time (s)": float(h[k, 0]),
                "Error (m)": float(h[k, 17]),
                "Sigma norm (m)": float(h[k, 20]),
                "Attitude error (deg)": float(np.rad2deg(h[k, 19])),
                "GNSS age (s)": float(h[k, 21]),
                "Fix applied": bool(h[k, 22]),
            }
            for k in selected
        ],
    }
    if events:
        delta = np.asarray(events[-1]["delta"])
        result["tables"]["last_correction"] = {
            "columns": ["State group", "x", "y", "z", "Unit"],
            "rows": [
                {
                    "State group": name,
                    "x": float(delta[3 * i]),
                    "y": float(delta[3 * i + 1]),
                    "z": float(delta[3 * i + 2]),
                    "Unit": unit,
                }
                for i, (name, unit) in enumerate(
                    [
                        ("Position", "m"),
                        ("Velocity", "m/s"),
                        ("Right attitude error", "rad"),
                        ("Accelerometer bias", "m/s^2"),
                        ("Gyro bias", "rad/s"),
                    ]
                )
            ],
        }
    return result
