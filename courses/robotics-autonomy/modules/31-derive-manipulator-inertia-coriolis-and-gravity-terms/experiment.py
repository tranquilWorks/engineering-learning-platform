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


def terms(q, v, payload):
    # Two point masses, with the distal payload lumped into the second mass.
    l1, l2, m1, m2 = 0.7, 0.5, 1.0, 0.8 + payload
    b = m2 * l1 * l2
    c = np.cos(q[1])
    h = b * np.sin(q[1])
    M = np.array(
        [
            [(m1 + m2) * l1 * l1 + m2 * l2 * l2 + 2 * b * c, m2 * l2 * l2 + b * c],
            [m2 * l2 * l2 + b * c, m2 * l2 * l2],
        ]
    )
    C = np.array([[-h * v[1], -h * (v[0] + v[1])], [h * v[0], 0.0]])
    g = 9.81 * np.array(
        [
            (m1 + m2) * l1 * np.cos(q[0]) + m2 * l2 * np.cos(q.sum()),
            m2 * l2 * np.cos(q.sum()),
        ]
    )
    Md = -b * np.sin(q[1]) * v[1] * np.array([[2.0, 1.0], [1.0, 0.0]])
    return M, C, g, Md


def run(p):
    payload = float(p["payload_kg"])
    elbow = np.deg2rad(float(p["elbow_angle_deg"]))
    broken = bool(p["broken_mode"])
    angles = np.linspace(-np.pi, np.pi, 121)
    velocity = np.array([0.6, -0.35])
    inertia = []
    gravity = []
    defects = []

    def evaluate(a):
        q = np.array([0.4, a])
        M, C, g, Md = terms(q, velocity, payload)
        if broken:
            C[0, 1] = 0.0
        S = Md - 2 * C
        return M, C, g, Md, np.linalg.norm(S + S.T)

    for a in angles:
        M, C, g, Md, e = evaluate(a)
        inertia.append(np.linalg.eigvalsh(M))
        gravity.append(g)
        defects.append(e)
    M, C, g, Md, error = evaluate(elbow)
    inertia, gravity = np.array(inertia), np.array(gravity)
    metric = [
        (
            "minimum_inertia_eigenvalue",
            "Minimum inertia eigenvalue",
            np.linalg.eigvalsh(M)[0],
            "kg*m^2",
        ),
        ("skew_identity_error", "Symmetric skew-identity defect", error, "kg*m^2/s"),
        ("gravity_torque", "Shoulder gravity torque", g[0], "N*m"),
    ]
    plots = {
        "response": plot(
            "Joint inertia eigenvalues",
            "Elbow angle (rad)",
            "Inertia (kg·m²)",
            [
                trace(
                    ["Min eig", "Max eig"][i],
                    angles,
                    inertia[:, i],
                    "Elbow angle",
                    "rad",
                    "Inertia eigenvalue",
                    "kg*m^2",
                )
                for i in range(2)
            ],
        ),
        "mechanism": plot(
            "Joint gravity torques",
            "Elbow angle (rad)",
            "Torque (N·m)",
            [
                trace(
                    f"Joint {i + 1}",
                    angles,
                    gravity[:, i],
                    "Elbow angle",
                    "rad",
                    "Gravity torque",
                    "N*m",
                )
                for i in range(2)
            ],
        ),
    }
    return finish(
        31,
        broken,
        {
            "sample_count": 121,
            "angles": angles,
            "inertia_eigenvalues": inertia,
            "gravity_sweep": gravity,
            "skew_defects": defects,
            "M": M,
            "C": C,
            "Mdot": Md,
            "gravity": g,
            "q": np.array([0.4, elbow]),
            "velocity": velocity,
        },
        metric,
        plots,
        "M comes from the kinetic energy of two moving point masses. The reported skew defect is ||S+Sᵀ|| with S=Mdot−2C, twice the conventional symmetric-part norm, with inertia-rate units.",
        "The fault deletes C[0,1] while leaving M and its derivative intact.",
        "Restore the coupling and verify positive inertia plus the skew identity; a straight elbow can hide the missing sine coupling.",
    )
