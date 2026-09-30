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
    delay = float(p["round_trip_delay_ms"]) / 1000
    bound = float(p["force_limit_n"])
    broken = bool(p["broken_mode"])
    dt = 0.005
    t = np.arange(401) * dt
    omega = 2 * np.pi * 3
    position = 0.02 * np.sin(omega * t)
    velocity = 0.02 * omega * np.cos(omega * t)
    delayed = np.maximum(t - delay, 0.0)
    request = -900 * 0.02 * np.sin(omega * delayed) - 0.4 * 0.02 * omega * np.cos(
        omega * delayed
    )
    # Before the first delayed sample, the buffer is explicitly initialized to zero.
    request[t < delay] = 0.0
    saturated = np.clip(request, -bound, bound)
    energy = 0.01
    energies = [energy]
    applied = []
    work = []
    limited = []
    for f, v in zip(saturated, velocity, strict=True):
        desired_work = f * v * dt
        cut = (not broken) and desired_work > energy
        used = f if not cut else energy / (v * dt)
        w = used * v * dt
        energy -= w
        applied.append(used)
        work.append(w)
        limited.append(cut)
        energies.append(energy)
    applied = np.array(applied)
    energies = np.array(energies)
    work = np.array(work)
    metric = [
        ("passivity_energy", "Minimum observed tank energy", min(energies), "J"),
        (
            "saturation_fraction",
            "Force saturation fraction",
            np.mean(abs(request) > bound),
            "1",
        ),
        (
            "removed_active_work",
            "Active work removed by limiter",
            sum((saturated - applied) * velocity * dt),
            "J",
        ),
    ]
    plots = {
        "response": plot(
            "Port energy balance",
            "Time (s)",
            "Energy (J)",
            [
                trace("Tank", t, energies[1:], "Time", "s", "Energy", "J"),
                trace("Zero", t, np.zeros_like(t), "Time", "s", "Energy", "J"),
            ],
        ),
        "mechanism": plot(
            "Requested and applied force",
            "Time (s)",
            "Force (N)",
            [
                trace("Requested", t, saturated, "Time", "s", "Force", "N"),
                trace("Applied", t, applied, "Time", "s", "Force", "N"),
            ],
        ),
    }
    return finish(
        39,
        broken,
        {
            "sample_count": 401,
            "time": t,
            "dt": dt,
            "position": position,
            "velocity": velocity,
            "requested_force": request,
            "saturated_force": saturated,
            "applied_force": applied,
            "work": work,
            "energy": energies,
            "initial_energy": 0.01,
            "intervention": limited,
            "force_limit": bound,
        },
        metric,
        plots,
        "Positive F·v is energy delivered by the force source to the prescribed moving port. The observer uses applied force after saturation and limiting. Its sampled work identity is exact for this declared quadrature.",
        "The fault bypasses the energy limiter while retaining the selected delay, saturation and moving-port samples.",
        "Restore the limiter and reconcile initial energy minus cumulative applied work. This prescribed-port experiment is not a closed-loop robot stability certificate or a measured delay margin.",
    )
