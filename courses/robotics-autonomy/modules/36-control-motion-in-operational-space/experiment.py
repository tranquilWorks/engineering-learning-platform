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


def geometry(q, mass):
    lengths = np.array([1.0, 0.8, 0.6])
    angles = np.cumsum(q)
    J = np.zeros((2, 3))
    M = np.eye(3) * 0.03 * mass
    for link in range(3):
        C = np.zeros((2, 3))
        for joint in range(link + 1):
            for k in range(joint, link + 1):
                d = lengths[k] * (0.5 if k == link else 1.0)
                C[:, joint] += d * np.array([-np.sin(angles[k]), np.cos(angles[k])])
        M += mass * (1 - 0.2 * link) * (C.T @ C)
    for joint in range(3):
        for k in range(joint, 3):
            J[:, joint] += lengths[k] * np.array(
                [-np.sin(angles[k]), np.cos(angles[k])]
            )
    return J, M


def run(p):
    mass = float(p["task_inertia_kg"])
    straightness = float(p["jacobian_condition"])
    broken = bool(p["broken_mode"])
    q = np.array([0.4, -1.2 / np.sqrt(straightness), 0.8 / np.sqrt(straightness)])
    J, M = geometry(q, mass)
    A = J @ np.linalg.solve(M, J.T)
    Lambda = np.linalg.inv(A)
    bar = np.linalg.solve(M, J.T) @ Lambda
    projector = np.eye(3) - (np.linalg.pinv(J) @ J if broken else J.T @ bar.T)
    secondary = projector @ np.array([0.5, -0.3, 0.7])
    desired = np.array([0.4, -0.2])
    primary = J.T @ Lambda @ desired
    torque = primary + secondary
    acceleration = J @ np.linalg.solve(M, torque)
    leak = J @ np.linalg.solve(M, secondary)
    scale = np.linspace(0, 1, 121)
    actual = np.array([J @ np.linalg.solve(M, primary + f * secondary) for f in scale])
    angle = np.linspace(0, 2 * np.pi, 121)
    directions = np.column_stack([np.cos(angle), np.sin(angle)])
    inertias = np.einsum("ni,ij,nj->n", directions, Lambda, directions)
    metric = [
        (
            "task_acceleration_error",
            "Actual task acceleration error",
            np.linalg.norm(acceleration - desired),
            "m/s^2",
        ),
        (
            "null_torque_leakage",
            "Secondary acceleration leakage",
            np.linalg.norm(leak),
            "m/s^2",
        ),
        (
            "effective_inertia",
            "Largest task inertia eigenvalue",
            np.linalg.eigvalsh(Lambda)[-1],
            "kg",
        ),
    ]
    plots = {
        "response": plot(
            "Resulting task acceleration",
            "Torque fraction (1)",
            "Acceleration (m/s²)",
            [
                trace(
                    name,
                    scale,
                    actual[:, i],
                    "Secondary torque fraction",
                    "1",
                    "Task acceleration",
                    "m/s^2",
                )
                for i, name in enumerate(["Actual x", "Actual y"])
            ],
        ),
        "mechanism": plot(
            "Directional task inertia",
            "Task direction (rad)",
            "Inertia (kg)",
            [
                trace(
                    "Inertia",
                    angle,
                    inertias,
                    "Task direction",
                    "rad",
                    "Inertia",
                    "kg",
                )
            ],
        ),
    }
    return finish(
        36,
        broken,
        {
            "sample_count": 121,
            "q": q,
            "J": J,
            "M": M,
            "Lambda": Lambda,
            "dynamically_consistent_inverse": bar,
            "torque_projector": projector,
            "secondary_torque": secondary,
            "primary_torque": primary,
            "desired_acceleration": desired,
            "actual_acceleration": acceleration,
            "secondary_acceleration": leak,
            "condition": np.linalg.cond(J),
            "scale": scale,
            "acceleration_sweep": actual,
            "direction": angle,
            "directional_inertia": inertias,
        },
        metric,
        plots,
        "This local zero-velocity calculation uses physical link mass/inertia and actual J M⁻¹ τ. The geometry control determines elbow configuration; the measured Jacobian condition is "
        + f"{np.linalg.cond(J):.3f}"
        + ". Gravity is assumed exactly compensated.",
        "The fault uses an ordinary Euclidean null projector for torque, which need not remain null after acceleration is weighted by M⁻¹.",
        "Restore the dynamically consistent torque projector and compare actual secondary task acceleration; no integrated trajectory or global singularity avoidance is claimed.",
    )
