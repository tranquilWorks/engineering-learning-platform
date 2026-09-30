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


def kinematics(q):
    a, b = q
    c = a + b
    return np.array(
        [np.cos(a) + 0.7 * np.cos(c), np.sin(a) + 0.7 * np.sin(c)]
    ), np.array(
        [
            [-np.sin(a) - 0.7 * np.sin(c), -0.7 * np.sin(c)],
            [np.cos(a) + 0.7 * np.cos(c), 0.7 * np.cos(c)],
        ]
    )


def run(p):
    geometry = float(p["jacobian_condition"])
    gain = float(p["joint_gain_per_s"])
    broken = bool(p["broken_mode"])
    goal = np.array([0.4, -1.2 / np.sqrt(geometry)])
    desired, Jgoal = kinematics(goal)
    initial = goal + np.array([0.18, -0.12])
    t = np.linspace(0, 4, 121)

    def commands(state):
        joint = gain * (goal - state[:2])
        position, J = kinematics(state[2:])
        e = gain * (desired - position)
        task = (J.T if broken else np.linalg.pinv(J, rcond=1e-10)) @ e
        return np.r_[np.clip(joint, -2, 2), np.clip(task, -2, 2)]

    solution = solve_ivp(
        lambda _, y: commands(y),
        (0, 4),
        np.r_[initial, initial],
        t_eval=t,
        method="DOP853",
        rtol=2e-11,
        atol=2e-12,
        max_step=0.04,
    )
    assert solution.success
    states = solution.y.T
    velocities = np.array([commands(y) for y in states])
    joint_error = np.linalg.norm(states[:, :2] - goal, axis=1)
    positions = np.array([[kinematics(y[:2])[0], kinematics(y[2:])[0]] for y in states])
    task_errors = np.linalg.norm(positions - desired, axis=2)
    metric = [
        (
            "joint_error",
            "Task-controller terminal joint error",
            np.linalg.norm(states[-1, 2:] - goal),
            "rad",
        ),
        (
            "task_error",
            "Task-controller terminal Cartesian error",
            task_errors[-1, 1],
            "m",
        ),
        (
            "control_effort",
            "Peak applied task joint speed",
            max(abs(velocities[:, 2:]).ravel()),
            "rad/s",
        ),
    ]
    plots = {
        "response": plot(
            "Joint tracking errors",
            "Time (s)",
            "Joint error (rad)",
            [
                trace(
                    "Joint servo",
                    t,
                    joint_error,
                    "Time",
                    "s",
                    "Joint error",
                    "rad",
                ),
                trace(
                    "Task servo",
                    t,
                    np.linalg.norm(states[:, 2:] - goal, axis=1),
                    "Time",
                    "s",
                    "Joint error",
                    "rad",
                ),
            ],
        ),
        "mechanism": plot(
            "Cartesian tracking errors",
            "Time (s)",
            "Position error (m)",
            [
                trace(name, t, task_errors[:, i], "Time", "s", "Position error", "m")
                for i, name in enumerate(["Joint servo", "Task servo"])
            ],
        ),
    }
    return finish(
        34,
        broken,
        {
            "sample_count": 121,
            "time": t,
            "states": states,
            "applied_velocity": velocities,
            "positions": positions,
            "task_errors": task_errors,
            "goal_q": goal,
            "goal_position": desired,
            "goal_J": Jgoal,
            "actual_condition": np.linalg.cond(Jgoal),
            "speed_limit": 2.0,
        },
        metric,
        plots,
        "Both trajectories execute ideal joint velocity servos capped at 2 rad/s. Geometry controls the goal elbow, whose measured Jacobian condition is "
        + f"{np.linalg.cond(Jgoal):.3f}"
        + ". No actuator torque dynamics are simulated.",
        "The fault substitutes a transpose task-gradient law for the velocity inverse while keeping the same gain; it no longer realizes the requested Cartesian velocity.",
        "Restore the inverse and compare both actual joint and Cartesian errors. A transpose gradient is a valid alternative with different convergence, not an inverse with the same bandwidth.",
    )
