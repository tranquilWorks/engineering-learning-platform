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


def run(p):
    force, length, broken = (
        float(p["force_n"]),
        float(p["lever_arm_m"]),
        bool(p["broken_mode"]),
    )
    f = force * np.array([0.6, 0.8])
    velocity = np.array([0.7, -0.4])
    angles = np.linspace(-0.8, 0.8, 121)
    torques = []
    powers = []
    matrices = []
    for elbow in angles:
        q1 = 0.4
        q12 = q1 + elbow
        l2 = 0.7 * length
        J = np.array(
            [
                [-length * np.sin(q1) - l2 * np.sin(q12), -l2 * np.sin(q12)],
                [length * np.cos(q1) + l2 * np.cos(q12), l2 * np.cos(q12)],
            ]
        )
        tau = (J if broken else J.T) @ f
        v = J @ velocity
        torques.append(tau)
        powers.append([tau @ velocity, f @ v])
        matrices.append(J)
    torques, powers, matrices = map(np.asarray, (torques, powers, matrices))
    metric = [
        ("joint_torque", "Peak joint torque", np.max(abs(torques)), "N*m"),
        (
            "virtual_power_error",
            "Maximum virtual-power mismatch",
            np.max(abs(powers[:, 0] - powers[:, 1])),
            "W",
        ),
        (
            "force_to_torque_gain",
            "Peak force-to-torque gain",
            max(np.linalg.norm(J.T @ np.array([0.6, 0.8])) for J in matrices),
            "m",
        ),
    ]
    plots = {
        "response": plot(
            "Mapped joint torques",
            "Elbow angle (rad)",
            "Torque (N·m)",
            [
                trace(
                    f"Joint {i + 1}",
                    angles,
                    torques[:, i],
                    "Elbow angle",
                    "rad",
                    "Torque",
                    "N*m",
                )
                for i in range(2)
            ],
        ),
        "mechanism": plot(
            "Virtual power check",
            "Elbow angle (rad)",
            "Power (W)",
            [
                trace(name, angles, powers[:, i], "Elbow angle", "rad", "Power", "W")
                for i, name in enumerate(["Joint", "Cartesian"])
            ],
        ),
    }
    return finish(
        30,
        broken,
        {
            "sample_count": len(angles),
            "angles": angles,
            "jacobians": matrices,
            "torques": torques,
            "powers": powers,
            "force": f,
            "joint_velocity": velocity,
        },
        metric,
        plots,
        "The two powers use the same force, configuration and joint velocity. Their equality tests the transpose map, not a torque magnitude proxy.",
        "The fault applies J F instead of Jᵀ F for this square planar Jacobian, retaining the selected force and link scale.",
        "Restore Jᵀ F and compare both powers; at zero force both maps produce zero power and the fault is unobservable.",
    )
