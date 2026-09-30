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
    environment = float(p["environment_stiffness_n_m"])
    damping = float(p["virtual_damping_n_s_m"])
    broken = bool(p["broken_mode"])
    # Ideal contact perturbations about a preloaded bilateral spring equilibrium.
    mass = 2.0
    virtual_k = 150.0
    effective_damping = -damping if broken else damping
    t = np.linspace(0, 0.4, 241)

    def rhs(_, y):
        x, v, z, w = y
        return [
            v,
            -((environment + virtual_k) * x + effective_damping * v) / mass,
            w,
            -((environment + virtual_k) * z + effective_damping * w) / mass,
        ]

    # Impedance starts with displacement; admittance with force-induced velocity.
    initial = [0.01, 0.0, 0.0, 0.2]
    sol = solve_ivp(
        rhs,
        (0, 0.4),
        initial,
        t_eval=t,
        method="DOP853",
        rtol=2e-11,
        atol=2e-12,
        max_step=0.002,
    )
    assert sol.success
    y = sol.y.T
    force = environment * y[:, [0, 2]]
    energy = (
        0.5 * mass * y[:, [1, 3]] ** 2
        + 0.5 * (environment + virtual_k) * y[:, [0, 2]] ** 2
    )
    norm = np.maximum(abs(y[:, 0]) / 0.01, abs(y[:, 1]) / 0.2)
    outside = np.flatnonzero(norm > 0.02)
    settled = not len(outside) or outside[-1] < len(t) - 1
    settling = 0.0 if not len(outside) else t[outside[-1] + 1] if settled else t[-1]
    metric = [
        (
            "peak_contact_force",
            "Peak contact-force perturbation",
            max(abs(force).ravel()),
            "N",
        ),
        ("settling_time", "Impedance settling observation", settling, "s"),
        (
            "interaction_energy",
            "Maximum impedance stored energy",
            max(energy[:, 0]),
            "J",
        ),
    ]
    plots = {
        "response": plot(
            "Contact perturbations",
            "Time (s)",
            "Contact force (N)",
            [
                trace(name, t, force[:, i], "Time", "s", "Contact force", "N")
                for i, name in enumerate(["Impedance", "Admittance"])
            ],
        ),
        "mechanism": plot(
            "Stored contact energy",
            "Time (s)",
            "Stored energy (J)",
            [
                trace(name, t, energy[:, i], "Time", "s", "Stored energy", "J")
                for i, name in enumerate(["Impedance", "Admittance"])
            ],
        ),
    }
    return finish(
        37,
        broken,
        {
            "sample_count": 241,
            "time": t,
            "state": y,
            "contact_force": force,
            "energy": energy,
            "mass": mass,
            "virtual_stiffness": virtual_k,
            "environment_stiffness": environment,
            "effective_damping": effective_damping,
            "energy_derivative": -effective_damping * y[:, [1, 3]] ** 2,
            "settled": bool(settled),
            "settling_censored": not settled,
            "initial_state": initial,
        },
        metric,
        plots,
        "An ideal torque-rendered impedance and ideal position-servo admittance share the declared mass–spring–damper equation under different initial excitation. "
        + (
            "The impedance meets the sampled 2% state band."
            if settled
            else "The impedance has not settled by 0.4 s; the displayed horizon is censored."
        ),
        "The fault reverses damping in both differential equations. The 0.4 s observation window bounds the displayed experiment; growing energy is calculated from the states.",
        "Restore positive damping and check dE/dt=−b v². These signed spring-force perturbations assume maintained preload, not unilateral impact or actuator bandwidth limits.",
    )
