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


def run(p):
    target = float(p["force_setpoint_n"])
    angle = np.deg2rad(float(p["surface_angle_deg"]))
    broken = bool(p["broken_mode"])
    normal = np.array([-np.sin(angle), np.cos(angle)])
    tangent = np.array([np.cos(angle), np.sin(angle)])
    used = np.array([0.0, 1.0]) if broken else normal
    Pf = np.outer(used, used)
    Pt = np.eye(2) - Pf
    correct = np.outer(normal, normal)
    stiffness = 600.0
    t = np.linspace(0, 2, 121)
    speed = 0.03

    def command(time, x):
        force = stiffness * max(0.0, normal @ x)
        goal = speed * time * tangent
        return Pt @ (speed * tangent + 5 * (goal - x)) + used * 0.012 * (target - force)

    sol = solve_ivp(
        command,
        (0, 2),
        [0.0, 0.0],
        t_eval=t,
        method="DOP853",
        rtol=2e-11,
        atol=2e-12,
        max_step=0.02,
    )
    assert sol.success
    state = sol.y.T
    velocity = np.array([command(time, x) for time, x in zip(t, state, strict=True)])
    force = stiffness * np.maximum(state @ normal, 0)
    leak = velocity @ tangent - speed
    metric = [
        ("force_error", "Terminal normal-force error", abs(force[-1] - target), "N"),
        (
            "motion_leakage",
            "Tangential speed-error RMS",
            np.sqrt(np.mean(leak**2)),
            "m/s",
        ),
        (
            "selection_frame_error",
            "Force-projector frame mismatch",
            np.linalg.norm(Pf - correct),
            "1",
        ),
    ]
    plots = {
        "response": plot(
            "Normal force feedback",
            "Time (s)",
            "Normal force (N)",
            [
                trace("Actual", t, force, "Time", "s", "Normal force", "N"),
                trace(
                    "Setpoint",
                    t,
                    np.full(121, target),
                    "Time",
                    "s",
                    "Normal force",
                    "N",
                ),
            ],
        ),
        "mechanism": plot(
            "Tangential motion",
            "Time (s)",
            "Velocity (m/s)",
            [
                trace(
                    "Actual",
                    t,
                    velocity @ tangent,
                    "Time",
                    "s",
                    "Tangential velocity",
                    "m/s",
                ),
                trace(
                    "Desired",
                    t,
                    np.full(121, speed),
                    "Time",
                    "s",
                    "Tangential velocity",
                    "m/s",
                ),
            ],
        ),
    }
    # Keep roundoff around the constant nominal speed in a physical plotting range.
    tangent_speed = velocity @ tangent
    low, high = (
        min(0.0, float(min(tangent_speed))),
        max(0.06, float(max(tangent_speed))),
    )
    span = high - low
    plots["mechanism"]["layout"]["yaxis"].update(
        range=[low - 0.05 * span, high + 0.05 * span], tickformat=".3f"
    )
    return finish(
        38,
        broken,
        {
            "sample_count": 121,
            "time": t,
            "position": state,
            "velocity": velocity,
            "normal_force": force,
            "normal": normal,
            "tangent": tangent,
            "force_projector": Pf,
            "motion_projector": Pt,
            "correct_force_projector": correct,
            "projector_product": Pt @ Pf,
            "stiffness": stiffness,
            "target_force": target,
            "target_tangent_speed": speed,
        },
        metric,
        plots,
        "The normal force comes from actual spring penetration. Both projector pairs remain orthogonal; the failure is their alignment with the physical surface, measured separately.",
        "The fault keeps world-axis force/motion selection while the surface normal rotates.",
        "Restore contact-frame projectors and compare actual force and tangential speed. At zero surface angle the two frames coincide and this fault is invisible.",
    )
