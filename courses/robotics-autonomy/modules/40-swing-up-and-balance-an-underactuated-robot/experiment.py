from __future__ import annotations

import numpy as np


def trace(name, x, y, x_quantity, x_unit, y_quantity, y_unit):
    x, y = np.asarray(x, float), np.asarray(y, float)
    return {
        "type": "scatter",
        "mode": "lines+markers" if np.ptp(x) == 0 else "lines",
        "name": name,
        "x": x,
        "y": y,
        "meta": {
            "x_quantity": x_quantity,
            "x_unit": x_unit,
            "y_quantity": y_quantity,
            "y_unit": y_unit,
        },
    }


def plot(title, x, y, traces):
    return {
        "data": traces,
        "layout": {
            "title": {"text": title, "x": 0.02},
            "xaxis": {"title": {"text": x, "standoff": 16}},
            "yaxis": {"title": {"text": y, "standoff": 16}},
            "legend": {
                "orientation": "h",
                "y": -0.3,
                "entrywidth": 0.5,
                "entrywidthmode": "fraction",
            },
            "margin": {"l": 72, "r": 25, "t": 65, "b": 115},
            "uirevision": "keep-view",
        },
        "config": {"responsive": True, "displaylogo": False},
    }


def finish(number, broken, diagnostics, metrics, plots, observation, fault, recovery):
    diagnostics.update(
        item_number=number,
        broken_active=broken,
        software_only=True,
        signature=[float(m[2]) for m in metrics],
    )
    return {
        "metrics": [
            {
                "id": key,
                "label": label,
                "value": float(value),
                "unit": unit,
                "emphasis": "primary" if i == 0 else "normal",
            }
            for i, (key, label, value, unit) in enumerate(metrics)
        ],
        "plots": plots,
        "diagnostics": diagnostics,
        "explanations": {
            "observation": observation,
            "broken": fault,
            "recovery": recovery,
        },
    }


from scipy.integrate import solve_ivp


def wrap(angle):
    return np.arctan2(np.sin(angle - np.pi), np.cos(angle - np.pi))


def run(p):
    gain = float(p["energy_gain_per_s"])
    limit = float(p["torque_limit_n_m"])
    broken = bool(p["broken_mode"])
    inertia = 0.05
    rotor = 0.008
    gravity = 0.3 * 9.81 * 0.35
    target_energy = 2 * gravity
    horizon = 12.0
    times = np.linspace(0, horizon, 241)

    def torque(state, balance):
        angle, speed = state[:2]
        energy = 0.5 * inertia * speed**2 + gravity * (1 - np.cos(angle))
        omega_reference = 1.0  # rad/s; gain remains dimensionally 1/s.
        requested = (
            gravity * np.sin(angle) - 2.0 * wrap(angle) - 0.65 * speed
            if balance
            else gain
            * (target_energy - energy)
            * speed
            / omega_reference**2
            * (-1 if broken else 1)
        )
        return np.clip(requested, -limit, limit)

    def rhs(balance):
        def equation(_, state):
            body_torque = torque(state, balance)
            acc = (body_torque - gravity * np.sin(state[0])) / inertia
            # State uses body angle/rate and absolute rotor angle/rate.
            return [state[1], acc, state[3], -body_torque / rotor]

        return equation

    def capture(_, state):
        return max(abs(wrap(state[0])) / 0.2, abs(state[1]) / 1.5) - 1.0

    capture.terminal = True
    capture.direction = -1
    initial = np.array([0.0, 0.15, 0.0, 0.0])
    swing = solve_ivp(
        rhs(False),
        (0, horizon),
        initial,
        events=capture,
        dense_output=True,
        method="DOP853",
        rtol=1e-12,
        atol=1e-13,
        max_step=0.025,
    )
    assert swing.success
    caught = bool(len(swing.t_events[0]))
    capture_time = float(swing.t_events[0][0]) if caught else horizon
    before = times <= capture_time
    state = np.empty((len(times), 4))
    state[before] = swing.sol(times[before]).T
    if caught:
        balanced = solve_ivp(
            rhs(True),
            (capture_time, horizon),
            swing.y_events[0][0],
            dense_output=True,
            method="DOP853",
            rtol=1e-12,
            atol=1e-13,
            max_step=0.025,
        )
        assert balanced.success
        state[~before] = balanced.sol(times[~before]).T
    mode = times > capture_time
    body = np.array([torque(y, bool(m)) for y, m in zip(state, mode, strict=True)])
    energy = 0.5 * inertia * state[:, 1] ** 2 + gravity * (1 - np.cos(state[:, 0]))
    error = np.array([wrap(a) for a in state[:, 0]])
    metric = [
        ("capture_time", "Capture time or observation horizon", capture_time, "s"),
        ("terminal_angle_error", "Terminal upright angle error", abs(error[-1]), "rad"),
        (
            "peak_energy_error",
            "Peak body energy error",
            max(abs(energy - target_energy)),
            "J",
        ),
    ]
    plots = {
        "response": plot(
            "Reaction-wheel swing-up",
            "Time (s)",
            "Angle error (rad)",
            [
                trace(
                    "Body error",
                    times,
                    error,
                    "Time",
                    "s",
                    "Upright angle error",
                    "rad",
                ),
                trace(
                    "Upright",
                    times,
                    np.zeros_like(times),
                    "Time",
                    "s",
                    "Upright angle error",
                    "rad",
                ),
            ],
        ),
        "mechanism": plot(
            "Pendulum body energy",
            "Time (s)",
            "Body energy (J)",
            [
                trace("Body energy", times, energy, "Time", "s", "Body energy", "J"),
                trace(
                    "Target",
                    times,
                    np.full_like(times, target_energy),
                    "Time",
                    "s",
                    "Body energy",
                    "J",
                ),
            ],
        ),
    }
    return finish(
        40,
        broken,
        {
            "sample_count": 241,
            "time": times,
            "state_body_and_absolute_rotor": state,
            "relative_rotor_angle": state[:, 2] - state[:, 0],
            "body_torque": body,
            "rotor_torque": -body,
            "body_energy": energy,
            "upright_error": error,
            "balance_active": mode,
            "captured": caught,
            "capture_censored": not caught,
            "capture_state": swing.y_events[0][0] if caught else [],
            "body_inertia": inertia,
            "rotor_inertia": rotor,
            "gravity_coefficient": gravity,
            "torque_limit": limit,
            "initial_state": initial,
        },
        metric,
        plots,
        (
            f"Capture occurred at {capture_time:.4f} s."
            if caught
            else "No capture occurred by 12 s; the reported time is censored."
        )
        + " Two coordinates share one internal motor torque. Body balance does not regulate rotor position or speed; neither wheel limits nor hardware feasibility are certified.",
        "The fault reverses the body energy-injection sign while preserving the selected gain and motor limit.",
        "Restore energy injection and require both angle and rate capture conditions. The small initial angular velocity starts the motion; exact downward rest stays at rest under this energy law.",
    )
