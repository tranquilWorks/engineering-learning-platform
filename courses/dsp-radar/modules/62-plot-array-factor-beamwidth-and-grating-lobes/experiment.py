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


def _factor(m, q, steer, angles, taper=False):
    index = np.arange(m)
    weights = 0.54 - 0.46 * np.cos(2 * np.pi * index / (m - 1)) if taper else np.ones(m)
    contributions = weights[:, None] * np.exp(
        2j
        * np.pi
        * q
        * index[:, None]
        * (np.sin(np.deg2rad(angles)) - np.sin(np.deg2rad(steer)))
    )
    return abs(contributions.sum(axis=0)) / weights.sum()


def _metrics(angles, response, steer):
    nearby = np.flatnonzero(abs(angles - steer) <= 5)
    peak = nearby[np.argmax(response[nearby])]
    normalized = response / response[peak]
    target = 1 / np.sqrt(2)
    left = np.flatnonzero(normalized[:peak] <= target)[-1]
    right = peak + np.flatnonzero(normalized[peak:] <= target)[0]
    cross = lambda i, j: (
        angles[i]
        + (target - normalized[i])
        * (angles[j] - angles[i])
        / (normalized[j] - normalized[i])
    )
    width = cross(right - 1, right) - cross(left, left + 1)
    minima = (
        np.flatnonzero(
            (normalized[1:-1] <= normalized[:-2]) & (normalized[1:-1] < normalized[2:])
        )
        + 1
    )
    ln = minima[minima < peak][-1]
    rn = minima[minima > peak][0]
    sll = 20 * np.log10(max(normalized[: ln + 1].max(), normalized[rn:].max()))
    return float(width), float(angles[rn] - angles[ln]), float(sll), float(angles[peak])


def run(parameters):
    elements, spacing, broken = _controls(
        parameters,
        [("elements", 8, [4, 8, 16]), ("spacing_wavelengths", 0.5, [0.5, 0.75, 1])],
    )
    elements = int(elements)
    angles = np.linspace(-90, 90, 7201)
    steer = 30 if broken else 0
    q = 1 if broken else spacing
    active = _factor(elements, q, steer, angles)
    metrics = _metrics(angles, active, steer)
    uniform8 = _factor(8, 0.5, 0, angles)
    taper8 = _factor(8, 0.5, 0, angles, True)
    taper_metrics = _metrics(angles, taper8, 0)
    counts = [4, 8, 16]
    spaces = [0.5, 0.75, 1]
    count_patterns = [_factor(m, spacing, 0, angles) for m in counts]
    space_patterns = [_factor(elements, q, 0, angles) for q in spaces]
    widths = [_metrics(angles, a, 0)[0] for a in count_patterns]
    wrong = _factor(elements, 1, 30, angles)
    recovery = _factor(elements, 0.5, 30, angles)
    db = lambda a: 20 * np.log10(np.maximum(a, 1e-3))
    orders = np.arange(-int(np.ceil(2 * q)), int(np.ceil(2 * q)) + 1)
    directions = np.sin(np.deg2rad(steer)) + orders / q
    visible = np.rad2deg(np.arcsin(directions[(orders != 0) & (abs(directions) <= 1)]))
    values = {
        "model_valid": (not broken, "boolean"),
        "half_power_beamwidth": (metrics[0], "deg"),
        "first_null_beamwidth": (metrics[1], "deg"),
        "peak_sidelobe_level": (metrics[2], "dB"),
        "main_peak_angle": (metrics[3], "deg"),
        "visible_grating_lobes": (len(visible), "lobes"),
        "alias_response_at_minus30": (
            _factor(elements, q, steer, np.array([-30]))[0],
            "voltage",
        ),
        "taper8_half_power_beamwidth": (taper_metrics[0], "deg"),
        "taper8_sidelobe_level": (taper_metrics[2], "dB"),
        "recovered_alias_response": (
            _factor(elements, 0.5, 30, np.array([-30]))[0],
            "voltage",
        ),
    }
    plots = {
        "pattern": _plot(
            "Explicit coherent array factor",
            "Observation angle (deg)",
            "Normalized response (dB)",
            [("Selected uniform array", angles, db(active))],
        ),
        "aperture_sweep": _plot(
            "More elements narrow the beam at fixed spacing",
            "Observation angle (deg)",
            "Normalized response (dB)",
            [(f"M={m}", angles, db(a)) for m, a in zip(counts, count_patterns)],
        ),
        "spacing_sweep": _plot(
            "Increasing spacing admits visible aliases",
            "Observation angle (deg)",
            "Normalized response (dB)",
            [(f"d/lambda={q}", angles, db(a)) for q, a in zip(spaces, space_patterns)],
        ),
        "taper": _plot(
            "Reviewed M=8, d/lambda=.5: taper tradeoff",
            "Observation angle (deg)",
            "Normalized response (dB)",
            [("Uniform", angles, db(uniform8)), ("Hamming", angles, db(taper8))],
        ),
        "beamwidth": _plot(
            "Interpolated half-power width on the full angle grid",
            "Elements (count)",
            "Half-power beamwidth (deg)",
            [("Uniform", counts, widths)],
        ),
        "alias": _plot(
            "Steered +30 degree beam: grating-lobe failure and recovery",
            "Observation angle (deg)",
            "Normalized response (dB)",
            [
                ("d/lambda=1", angles, db(wrong)),
                ("d/lambda=.5 recovery", angles, db(recovery)),
            ],
        ),
    }
    # The source's four private off-grid probes do not alter ideal-grid metrics.
    state = 6201
    probe_angles = []
    for _ in range(4):
        state = (16807 * state) % 2147483647
        probe_angles.append(-60 + 120 * (state + 0.5) / 2147483647)
    probe_angles = np.array(probe_angles)
    probes = _factor(elements, q, steer, probe_angles)
    values["first_offgrid_probe_response"] = (probes[0], "voltage")
    plots["linear_pattern"] = _plot(
        "Linear array factor and seeded off-grid probes",
        "Observation angle (deg)",
        "Normalized array factor (ratio)",
        [
            ("Full-grid calculation", angles, active),
            ("Seed 6201 probes", probe_angles, probes),
        ],
    )
    plots["linear_pattern"]["data"][1]["mode"] = "markers"
    index = np.arange(elements)
    contribution = np.exp(
        2j
        * np.pi
        * q
        * index
        * (np.sin(np.deg2rad(probe_angles[0])) - np.sin(np.deg2rad(steer)))
    )
    plots["contributions"] = _plot(
        "Element phasors at the first off-grid probe",
        "Element index (count)",
        "Element contribution (normalized voltage)",
        [("I", index, contribution.real), ("Q", index, contribution.imag)],
    )
    return _finish(
        values,
        plots,
        "Coherent element phasors sum to the normalized array factor. Full 0.025-degree calculations measure interpolated half-power width, first nulls and sidelobes; the separate reviewed eight-element Hamming comparison shows its width/sidelobe tradeoff.",
        "One-wavelength spacing while steering to +30 degrees produces an equally strong -30-degree grating lobe. A narrow main lobe alone is not unambiguous.",
        "Restore half-wavelength spacing on the same +30-degree steering case. The selected broadside scene returns exactly when the toggle is disabled.",
        6201,
        broken,
        probe_angles_deg=probe_angles.tolist(),
        probe_responses=probes.tolist(),
        visible_grating_angles_deg=visible.tolist(),
        element_sweep_hpbw=widths,
        calculation_angle_samples=7201,
        taper_comparison_elements=8,
        taper_comparison_spacing=0.5,
    )
