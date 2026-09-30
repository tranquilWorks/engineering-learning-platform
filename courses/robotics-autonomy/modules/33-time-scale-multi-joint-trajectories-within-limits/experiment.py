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
    distance = float(p["path_distance_rad"])
    limit = float(p["speed_limit_rad_s"])
    broken = bool(p["broken_mode"])
    displacement = np.array([distance, -0.6 * distance])
    acc_limit = 3.0
    required = max(
        1.5 * max(abs(displacement)) / limit,
        np.sqrt(6 * max(abs(displacement)) / acc_limit),
    )
    duration = 1.0 if broken else required
    t = np.linspace(0, duration, 121)
    s = t / duration
    q = (3 * s * s - 2 * s * s * s)[:, None] * displacement
    v = (6 * s * (1 - s) / duration)[:, None] * displacement
    a = (6 * (1 - 2 * s) / duration**2)[:, None] * displacement
    peak_v = max(abs(v).ravel())
    peak_a = max(abs(a).ravel())
    excess = max(0.0, peak_v - limit)
    metric = [
        ("minimum_duration", "Applied cubic duration", duration, "s"),
        ("peak_acceleration", "Peak joint acceleration", peak_a, "rad/s^2"),
        ("limit_violation", "Measured speed-limit excess", excess, "rad/s"),
    ]
    plots = {
        "response": plot(
            "Synchronized velocities",
            "Time (s)",
            "Velocity (rad/s)",
            [
                trace(
                    f"Joint {i + 1}",
                    t,
                    v[:, i],
                    "Time",
                    "s",
                    "Angular velocity",
                    "rad/s",
                )
                for i in range(2)
            ]
            + [
                trace(
                    "Speed +",
                    t,
                    np.full(121, limit),
                    "Time",
                    "s",
                    "Angular velocity",
                    "rad/s",
                ),
                trace(
                    "Speed −",
                    t,
                    np.full(121, -limit),
                    "Time",
                    "s",
                    "Angular velocity",
                    "rad/s",
                ),
            ],
        ),
        "mechanism": plot(
            "Joint accelerations",
            "Time (s)",
            "Acceleration (rad/s²)",
            [
                trace(
                    f"Joint {i + 1}",
                    t,
                    a[:, i],
                    "Time",
                    "s",
                    "Angular acceleration",
                    "rad/s^2",
                )
                for i in range(2)
            ],
        ),
    }
    return finish(
        33,
        broken,
        {
            "sample_count": 121,
            "time": t,
            "position": q,
            "velocity": v,
            "acceleration": a,
            "displacement": displacement,
            "required_duration": required,
            "speed_limit": limit,
            "acceleration_limit": acc_limit,
            "acceleration_excess": max(0.0, peak_a - acc_limit),
        },
        metric,
        plots,
        "The minimum duration is within the declared rest-to-rest cubic family, using both the exact 1.5 velocity peak and the 6/T² acceleration peak. It is not a global time-optimal trajectory.",
        "The fault applies a fixed one-second cubic with the selected displacement and speed bound.",
        "Restore bound-derived duration and check both joints. Small moves with permissive limits may make the fixed one-second fault feasible.",
    )
