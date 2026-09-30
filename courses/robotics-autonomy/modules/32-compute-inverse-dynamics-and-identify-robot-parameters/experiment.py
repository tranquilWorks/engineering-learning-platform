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


def motion(t, amplitude, fault=False):
    if fault:
        q = np.full_like(t, 0.4)
        v = np.zeros_like(t)
        a = np.zeros_like(t)
    else:
        q = 0.4 + amplitude * (np.sin(1.3 * t) + 0.25 * np.sin(3.1 * t))
        v = amplitude * (1.3 * np.cos(1.3 * t) + 0.775 * np.cos(3.1 * t))
        a = -amplitude * (1.69 * np.sin(1.3 * t) + 2.4025 * np.sin(3.1 * t))
    return q, v, a


def run(p):
    amplitude = float(p["excitation_amplitude_rad"])
    guess = float(p["payload_guess_kg"])
    broken = bool(p["broken_mode"])
    t = np.linspace(0, 6, 121)
    q, v, a = motion(t, amplitude, broken)
    # Identify load mass and viscous damping; known rotor inertia is subtracted.
    Y = np.column_stack([0.25 * a + 4.905 * np.cos(q), v])
    truth = np.array([1.0, 0.12])
    prior = np.array([guess, 0.08])
    ridge = 0.02
    torque = 0.08 * a + Y @ truth + 0.015 * np.sin(2.7 * t + 0.2)
    augmented = np.vstack([Y, np.sqrt(ridge) * np.eye(2)])
    rhs = np.r_[torque - 0.08 * a, np.sqrt(ridge) * prior]
    fitted = np.linalg.lstsq(augmented, rhs, rcond=None)[0]
    qt = 0.3 + 0.45 * np.cos(1.7 * t)
    vt = -0.765 * np.sin(1.7 * t)
    at = -1.3005 * np.cos(1.7 * t)
    testY = np.column_stack([0.25 * at + 4.905 * np.cos(qt), vt])
    actual = 0.08 * at + testY @ truth
    predicted = 0.08 * at + testY @ fitted
    residual = predicted - actual
    metric = [
        (
            "inverse_dynamics_residual",
            "Held-out torque RMS",
            np.sqrt(np.mean(residual**2)),
            "N*m",
        ),
        ("payload_error", "Identified payload error", abs(fitted[0] - truth[0]), "kg"),
        (
            "regressor_condition",
            "Regularized design condition",
            np.linalg.cond(augmented),
            "1",
        ),
    ]
    plots = {
        "response": plot(
            "Training and test motion",
            "Time (s)",
            "Joint angle (rad)",
            [
                trace("Training", t, q, "Time", "s", "Joint angle", "rad"),
                trace("Held-out", t, qt, "Time", "s", "Joint angle", "rad"),
            ],
        ),
        "mechanism": plot(
            "Held-out torque prediction",
            "Time (s)",
            "Torque (N·m)",
            [
                trace("Predicted", t, predicted, "Time", "s", "Torque", "N*m"),
                trace("Truth", t, actual, "Time", "s", "Torque", "N*m"),
            ],
        ),
    }
    return finish(
        32,
        broken,
        {
            "sample_count": 121,
            "time": t,
            "training_q": q,
            "training_velocity": v,
            "training_acceleration": a,
            "regressor": Y,
            "augmented_design": augmented,
            "training_torque": torque,
            "fitted_parameters": fitted,
            "true_parameters": truth,
            "prior": prior,
            "ridge": ridge,
            "rank": int(np.linalg.matrix_rank(Y)),
            "heldout_regressor": testY,
            "heldout_true_torque": actual,
            "heldout_predicted_torque": predicted,
            "heldout_residual": residual,
        },
        metric,
        plots,
        "A regularized two-parameter fit uses training torque only. The separate held-out motion tests predicted torque; raw design rank is "
        + str(np.linalg.matrix_rank(Y))
        + " of 2. Columns use declared 1 kg and 1 N·m·s parameter scales.",
        "The fault holds the training joint still. Payload remains observable through gravity, but viscous damping is unexcited and falls back to its prior.",
        "Restore multisine excitation, inspect raw rank, and compare held-out error. A finite regularized condition number does not prove both parameters were observed.",
    )
