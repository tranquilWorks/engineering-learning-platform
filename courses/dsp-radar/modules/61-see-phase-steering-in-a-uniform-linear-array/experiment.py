from __future__ import annotations

import numpy as np


def _controls(p, spec):
    values = []
    for key, default, choices in spec:
        value = p.get(key, default)
        if isinstance(value, bool) or value not in choices:
            raise ValueError("Choose a retained physical control: " + key)
        values.append(float(value))
    broken = p.get("broken_mode", False)
    if not isinstance(broken, bool):
        raise TypeError("broken_mode must be boolean")
    return (*values, broken)


def _plot(title, xlabel, ylabel, traces):
    data = []
    for name, x, y in traces:
        x, y = np.asarray(x), np.asarray(y)
        if len(x) <= 512:
            ix = np.arange(len(x))
        else:
            peaks = np.flatnonzero((y[1:-1] >= y[:-2]) & (y[1:-1] > y[2:])) + 1
            selected = peaks[np.argsort(y[peaks])[-12:]]
            keep = np.unique(
                np.r_[
                    0,
                    len(x) - 1,
                    np.argmin(abs(x)),
                    np.argmin(y),
                    np.argmax(y),
                    selected,
                ]
            )
            grid = np.linspace(0, len(x) - 1, 512 - len(keep)).astype(int)
            ix = np.unique(np.r_[keep, grid])
        data.append(
            {
                "type": "scatter",
                "mode": "lines",
                "name": name,
                "x": x[ix].tolist(),
                "y": y[ix].tolist(),
            }
        )
    return {
        "data": data,
        "layout": {
            "title": {"text": title},
            "xaxis": {"title": xlabel},
            "yaxis": {"title": ylabel},
            "legend": {"orientation": "h"},
        },
        "config": {"responsive": True, "displaylogo": False},
    }


def _heat(title, xlabel, ylabel, x, y, z, unit):
    x, y, z = np.asarray(x), np.asarray(y), np.asarray(z)

    def indices(axis, scores, limit):
        peaks = np.flatnonzero(
            (scores >= np.r_[-np.inf, scores[:-1]])
            & (scores >= np.r_[scores[1:], -np.inf])
        )
        keep = list(peaks[np.argsort(scores[peaks])[-12:]]) + [
            int(np.argmin(abs(axis))),
            0,
            len(axis) - 1,
        ]
        keep = np.unique(keep)
        grid = np.linspace(
            0, len(axis) - 1, min(len(axis), max(2, limit - len(keep)))
        ).astype(int)
        return np.unique(np.r_[keep, grid])

    ix = indices(x, np.max(z, axis=0), 128)
    iy = indices(y, np.max(z, axis=1), 64)
    return {
        "data": [
            {
                "type": "heatmap",
                "x": x[ix].tolist(),
                "y": y[iy].tolist(),
                "z": z[np.ix_(iy, ix)].tolist(),
                "colorbar": {"title": unit},
            }
        ],
        "layout": {
            "title": {"text": title},
            "xaxis": {"title": xlabel},
            "yaxis": {"title": ylabel},
        },
        "config": {"responsive": True, "displaylogo": False},
    }


def _finish(values, plots, observation, failure, recovery, seed, broken, **extra):
    return {
        "metrics": [
            {"id": k, "label": k.replace("_", " "), "value": float(v), "unit": u}
            for k, (v, u) in values.items()
        ],
        "plots": plots,
        "explanations": {
            "observation": observation,
            "broken": failure,
            "recovery": recovery,
        },
        "diagnostics": dict(
            signature=[float(v[0]) for v in values.values()],
            signature_fields=list(values),
            seed=seed,
            broken_active=broken,
            **extra,
        ),
    }


def _uniform(seed, count, offset=0.5):
    states = np.empty(count)
    state = int(seed)
    for k in range(count):
        state = (16807 * state) % 2147483647
        states[k] = (state + offset) / 2147483647
    return states


def _normal(seed, count, offset=0.5):
    u = _uniform(seed, 2 * ((count + 1) // 2), offset)
    radius = np.sqrt(-2 * np.log(u[::2]))
    phase = 2 * np.pi * u[1::2]
    return np.column_stack([radius * np.cos(phase), radius * np.sin(phase)]).ravel()[
        :count
    ]


def _greedy(cost, valid):
    working = np.where(valid, cost, np.inf).copy()
    assignment = np.full(cost.shape[0], -1, dtype=int)
    for _ in range(min(cost.shape)):
        flat = int(np.argmin(working.ravel(order="F")))
        i, j = np.unravel_index(flat, working.shape, order="F")
        if not np.isfinite(working[i, j]):
            break
        assignment[i] = j
        working[i, :] = np.inf
        working[:, j] = np.inf
    return assignment


def _snapshot(angle, spacing, noise=True):
    m = np.arange(8)
    phase = np.deg2rad(20) + 2 * np.pi * m * spacing * np.sin(np.deg2rad(angle))
    x = np.exp(1j * phase)
    if noise:
        z = _normal(6101, 16)
        x += 10 ** (-35 / 20) / np.sqrt(2) * (z[:8] + 1j * z[8:])
    wrapped = np.angle(x)
    unwrapped = np.unwrap(wrapped)
    center = m - m.mean()
    slope = center @ (unwrapped - unwrapped.mean()) / (center @ center)
    adjacent = np.angle(np.sum(x[:-1].conj() * x[1:]))
    estimate = np.rad2deg(np.arcsin(np.clip(slope / (2 * np.pi * spacing), -1, 1)))
    residual = unwrapped - (unwrapped.mean() + slope * center)
    return (
        x,
        wrapped,
        unwrapped,
        slope,
        adjacent,
        estimate,
        float(np.sqrt(np.mean(residual**2))),
    )


def run(parameters):
    angle, spacing, broken = _controls(
        parameters,
        [
            ("arrival_angle_deg", 30, [-60, -30, 0, 30, 60]),
            ("spacing_wavelengths", 0.5, [0.25, 0.375, 0.5]),
        ],
    )
    m = np.arange(8)
    wavelength = 299792458 / 3e9
    baseline = _snapshot(angle, spacing)
    true_alias = np.rad2deg(np.arcsin(0.6))
    alias = np.rad2deg(np.arcsin(-0.4))
    wrong = _snapshot(true_alias, 1, False)
    recovery = _snapshot(true_alias, 0.5, False)
    active = wrong if broken else baseline
    actual_angle = true_alias if broken else angle
    q = 1 if broken else spacing
    mismatch = max(abs(wrong[0] - _snapshot(alias, 1, False)[0]))
    slope = 2 * np.pi * q * np.sin(np.deg2rad(actual_angle))
    delays = -m * q * wavelength * np.sin(np.deg2rad(actual_angle)) / 299792458
    angle_sweep = [_snapshot(a, spacing)[5] for a in [-60, -30, 0, 30, 60]]
    spacing_sweep = [_snapshot(angle, q)[3] for q in [0.25, 0.375, 0.5]]
    values = {
        "model_valid": (not broken, "boolean"),
        "theoretical_phase_slope": (slope, "rad/element"),
        "estimated_phase_slope": (active[3], "rad/element"),
        "adjacent_phase_step": (active[4], "rad/element"),
        "estimated_angle": (active[5], "deg"),
        "angle_error": (active[5] - actual_angle, "deg"),
        "phase_fit_rmse": (active[6], "rad"),
        "alias_snapshot_mismatch": (mismatch, "voltage"),
        "recovered_alias_angle": (recovery[5], "deg"),
        "last_sensor_delay": (delays[-1] * 1e12, "ps"),
    }
    plots = {
        "geometry": _plot(
            "Positive bearing creates a relative arrival advance",
            "Element position (m)",
            "Relative propagation delay (ps)",
            [("Geometry", m * q * wavelength, delays * 1e12)],
        ),
        "samples": _plot(
            "Simultaneous complex sensor voltages",
            "Element index (count)",
            "Voltage (normalized)",
            [("In phase", m, active[0].real), ("Quadrature", m, active[0].imag)],
        ),
        "phase": _plot(
            "Wrapped and unwrapped spatial phase",
            "Element index (count)",
            "Phase (rad)",
            [
                ("Principal phase", m, active[1]),
                ("Unwrapped", m, active[2]),
                ("Physical model", m, np.deg2rad(20) + m * slope),
            ],
        ),
        "angle_sweep": _plot(
            "Arrival angle changes phase slope",
            "True angle (deg)",
            "Estimated angle (deg)",
            [("Noisy fit", [-60, -30, 0, 30, 60], angle_sweep)],
        ),
        "electrical_spacing": _plot(
            "Spacing or carrier changes the same electrical aperture",
            "Spacing d/lambda (ratio)",
            "Phase slope (rad/element)",
            [
                ("Spacing sweep", [0.25, 0.375, 0.5], spacing_sweep),
                (
                    "1.5/2.25/3 GHz at fixed d",
                    [0.25, 0.375, 0.5],
                    [
                        2 * np.pi * q * np.sin(np.deg2rad(angle))
                        for q in [0.25, 0.375, 0.5]
                    ],
                ),
            ],
        ),
        "alias": _plot(
            "Different directions produce identical aliased phases",
            "Element index (count)",
            "Principal phase (rad)",
            [
                ("True q=1", m, wrong[1]),
                ("Alias q=1", m, _snapshot(alias, 1, False)[1]),
                ("Recovery q=.5", m, recovery[1]),
            ],
        ),
    }
    return _finish(
        values,
        plots,
        "A positive broadside angle advances arrival time and creates positive spatial phase under exp(+j2pi f t). Unwrapped least-squares and adjacent-sensor phase estimates reveal the direction.",
        "At one wavelength, direction cosines .6 and -.4 produce identical sensor phasors. The wrapped step infers the wrong direction; more averaging cannot remove this ambiguity.",
        "Use half-wavelength spacing for the same true angle, frequency, phase and sensor count. The named noiseless alias recovery is distinct from the selected noisy scene; disable the toggle to restore that scene.",
        6101,
        broken,
        received_real=active[0].real.tolist(),
        received_imag=active[0].imag.tolist(),
        angle_sweep_estimates=angle_sweep,
        spacing_sweep_slopes=spacing_sweep,
        carrier_sweep_hz=[1.5e9, 2.25e9, 3e9],
    )
