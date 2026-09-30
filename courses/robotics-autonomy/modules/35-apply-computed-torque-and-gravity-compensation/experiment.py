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


def dynamics(q, v):
    b = 0.8 * 0.7 * 0.5
    h = b * np.sin(q[1])
    M = np.array(
        [
            [
                1.8 * 0.7**2 + 0.8 * 0.5**2 + 2 * b * np.cos(q[1]),
                0.8 * 0.5**2 + b * np.cos(q[1]),
            ],
            [0.8 * 0.5**2 + b * np.cos(q[1]), 0.8 * 0.5**2],
        ]
    )
    C = np.array([[-h * v[1], -h * (v[0] + v[1])], [h * v[0], 0.0]])
    g = 9.81 * np.array(
        [
            1.8 * 0.7 * np.cos(q[0]) + 0.8 * 0.5 * np.cos(q.sum()),
            0.8 * 0.5 * np.cos(q.sum()),
        ]
    )
    return M, C, g


def desired(t):
    return (
        np.array([0.4 + 0.15 * np.sin(t), 0.6 + 0.12 * np.cos(1.3 * t)]),
        np.array([0.15 * np.cos(t), -0.156 * np.sin(1.3 * t)]),
        np.array([-0.15 * np.sin(t), -0.2028 * np.cos(1.3 * t)]),
    )


def run(p):
    mismatch = float(p["model_error_fraction"])
    band = float(p["tracking_bandwidth_per_s"])
    broken = bool(p["broken_mode"])
    t = np.linspace(0, 4, 241)

    def evaluate(time, state):
        q, v = state[:2], state[2:]
        qd, vd, ad = desired(time)
        M, C, g = dynamics(q, v)
        nominal = (1 + mismatch) * (
            M @ (ad + 2 * band * (vd - v) + band * band * (qd - q))
            + C @ v
            + (-g if broken else g)
        )
        applied = np.clip(nominal, -20, 20)
        acc = np.linalg.solve(M, applied - C @ v - g)
        return (
            np.r_[v, acc],
            applied,
            nominal,
            (1 + mismatch) * (-g if broken else g) - g,
        )

    initial = np.r_[desired(0)[0] + [0.1, -0.08], [0.0, 0.0]]
    sol = solve_ivp(
        lambda time, y: evaluate(time, y)[0],
        (0, 4),
        initial,
        t_eval=t,
        method="DOP853",
        rtol=2e-11,
        atol=2e-12,
        max_step=0.02,
    )
    assert sol.success
    state = sol.y.T
    data = [evaluate(time, y) for time, y in zip(t, state, strict=True)]
    applied = np.array([r[1] for r in data])
    requested = np.array([r[2] for r in data])
    residual = np.array([r[3] for r in data])
    targets = np.array([desired(time)[0] for time in t])
    errors = state[:, :2] - targets
    metric = [
        (
            "tracking_error",
            "Joint tracking RMS",
            np.sqrt(np.mean(np.sum(errors**2, axis=1))),
            "rad",
        ),
        ("peak_torque", "Peak applied torque", max(abs(applied).ravel()), "N*m"),
        (
            "cancellation_residual",
            "Gravity compensation RMS defect",
            np.sqrt(np.mean(np.sum(residual**2, axis=1))),
            "N*m",
        ),
    ]
    plots = {
        "response": plot(
            "Robot tracking errors",
            "Time (s)",
            "Joint error (rad)",
            [
                trace(
                    f"Joint {i + 1}", t, errors[:, i], "Time", "s", "Joint error", "rad"
                )
                for i in range(2)
            ],
        ),
        "mechanism": plot(
            "Applied computed torque",
            "Time (s)",
            "Torque (N·m)",
            [
                trace(f"Joint {i + 1}", t, applied[:, i], "Time", "s", "Torque", "N*m")
                for i in range(2)
            ],
        ),
    }
    return finish(
        35,
        broken,
        {
            "sample_count": 241,
            "time": t,
            "state": state,
            "desired_position": targets,
            "tracking_error": errors,
            "applied_torque": applied,
            "requested_torque": requested,
            "gravity_compensation_defect": residual,
            "state_derivative": np.array([r[0] for r in data]),
            "torque_limit": 20.0,
        },
        metric,
        plots,
        "The plant integrates coupled inertia, Coriolis and gravity dynamics. Selected model error scales the controller model; actual torques saturate at ±20 N·m. Nominal error dynamics apply only without mismatch or saturation.",
        "The fault reverses the modeled gravity compensation while leaving the plant gravity and selected bandwidth unchanged.",
        "Restore gravity compensation, inspect applied versus requested torque, then sweep model error. A small tracking error alone cannot certify correct compensation.",
    )
