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


def _uniform(seed, count):
    state = int(seed)
    out = np.empty(count)
    for i in range(count):
        state = (16807 * state) % 2147483647
        out[i] = state / 2147483647
    return out


def _noise(seed, rows, columns=1, interleaved=False):
    count = rows * columns
    u = _uniform(seed, 2 * count)
    first, second = (u[::2], u[1::2]) if interleaved else (u[:count], u[count:])
    return (np.sqrt(-np.log(first)) * np.exp(2j * np.pi * second)).reshape(
        (rows, columns), order="F"
    )


def _db(power, floor=-80, relative=False):
    x = np.asarray(power)
    if relative:
        x = x / np.max(x)
    return 10 * np.log10(np.maximum(x, 10 ** (floor / 10)))


def _steer(angles, count, sign=1):
    return np.exp(
        sign
        * 1j
        * np.pi
        * np.arange(count)[:, None]
        * np.sin(np.deg2rad(np.atleast_1d(angles)))
    )


def _cov(data):
    r = data @ data.conj().T / data.shape[1]
    return (r + r.conj().T) / 2


def _mvdr(r, a, alpha):
    loaded = r + alpha * np.trace(r).real / len(r) * np.eye(len(r))
    if 1 / np.linalg.cond(loaded, 1).real < 1e-12:
        raise ValueError("Covariance solve refused: insufficient regularization")
    u = np.linalg.solve(loaded, a)
    return u / np.vdot(a, u)


def _peaks(power, angles, count=2, separation=1):
    ix = np.flatnonzero((power[1:-1] > power[:-2]) & (power[1:-1] >= power[2:])) + 1
    selected = []
    for k in sorted(ix, key=lambda k: (-power[k], k)):
        if all(abs(angles[k] - angles[j]) >= separation for j in selected):
            selected.append(k)
            if len(selected) == count:
                break
    return np.sort(angles[selected])


def _width(axis, power):
    i = int(np.argmax(power))
    left = right = i
    level = power[i] / 2
    while left > 0 and power[left] >= level:
        left -= 1
    while right < len(power) - 1 and power[right] >= level:
        right += 1
    if left == 0 or right == len(power) - 1:
        raise ValueError("Half-power crossing is outside the retained axis")
    lo = axis[left] + (level - power[left]) * (axis[left + 1] - axis[left]) / (
        power[left + 1] - power[left]
    )
    hi = axis[right - 1] + (level - power[right - 1]) * (
        axis[right] - axis[right - 1]
    ) / (power[right] - power[right - 1])
    return hi - lo


CONTROLS = [
    ("target_cross_range_m", 0, [-20, 0, 20]),
    ("aperture_length_m", 80, [20, 40, 80]),
]


def _focus(measurement, positions, candidates):
    paths = np.sqrt(1000**2 + (positions[:, None] - candidates) ** 2)
    compensation = np.exp(4j * np.pi * (paths - 1000) / 0.06)
    return abs(measurement @ compensation) / sum(abs(measurement))


def run(parameters):
    target, length, broken = _controls(parameters, CONTROLS)
    fullpos = np.linspace(-40, 40, 401)
    keep = abs(fullpos) <= length / 2 + 1e-12
    pos = fullpos[keep]
    ranges = np.linspace(995, 1005, 201)
    # Fixed full-aperture noise cropped with the aperture keeps controls isolated.
    noise = 10 ** (-30 / 20) * _noise(7501, 401, 201, True)[keep]
    slant = np.sqrt(1000**2 + (pos - target) ** 2)
    phase = -4 * np.pi * (slant - 1000) / 0.06
    raw = (
        np.exp(-0.5 * ((ranges[None, :] - slant[:, None]) / 0.6) ** 2)
        * np.exp(1j * phase[:, None])
        + noise
    )
    ridge = np.argmin(abs(ranges[None, :] - slant[:, None]), axis=1)
    measurement = raw[np.arange(len(pos)), ridge]
    candidates = np.linspace(-26, 26, 209)
    good = _focus(measurement, pos, candidates)
    bad = _focus(abs(measurement), pos, candidates)
    active = bad if broken else good
    lengths = np.array([20, 40, 80])
    spans = []
    geometry = []
    for value in lengths:
        p = fullpos[abs(fullpos) <= value / 2 + 1e-12]
        r = np.sqrt(1000**2 + (p - target) ** 2)
        spans.append(float(2 * np.ptp(r) / 0.06))
        geometry.append((p, -2 * (r - 1000) / 0.06))
    xs = np.array([-20, 0, 20])
    paths = [np.sqrt(1000**2 + (fullpos - x) ** 2) for x in xs]
    values = {
        "range_excursion": (np.ptp(slant), "m"),
        "delay_excursion": (2 * np.ptp(slant) / 3e8 * 1e9, "ns"),
        "phase_span": (np.ptp(phase) / (2 * np.pi), "turns"),
        "maximum_phase_step": (max(abs(np.diff(phase))), "rad"),
        "aperture_samples": (len(pos), "count"),
        "active_focus_peak": (max(active), "ratio"),
        "active_focus_coordinate": (candidates[np.argmax(active)], "m"),
        "recovered_focus_peak": (max(good), "ratio"),
        "recovered_coordinate": (candidates[np.argmax(good)], "m"),
        "selected_noise_power": (np.mean(abs(noise) ** 2), "voltage²"),
        "model_valid": (not broken, "boolean"),
    }
    plots = {
        "geometry": _plot(
            "Slant range across the selected aperture",
            "Platform cross-range (m)",
            "Slant range (m)",
            [("Target path", pos, slant)],
        ),
        "phase": _plot(
            "Range-referenced round-trip phase",
            "Platform cross-range (m)",
            "Phase (rad)",
            [
                ("Wrapped", pos, np.angle(np.exp(1j * phase))),
                ("Range-referenced", pos, phase),
            ],
        ),
        "magnitude": _heat(
            "Raw echo delay ridge",
            "Fast-time apparent range (m)",
            "Platform cross-range (m)",
            ranges,
            pos,
            abs(raw),
            "voltage",
        ),
        "iq": _heat(
            "Carrier phase along the aperture",
            "Fast-time apparent range (m)",
            "Platform cross-range (m)",
            ranges,
            pos,
            raw.real,
            "I voltage",
        ),
        "cross_range": _plot(
            "Target cross-range moves the path vertex",
            "Platform cross-range (m)",
            "Range excess (m)",
            [(f"{x:g} m target", fullpos, r - 1000) for x, r in zip(xs, paths)],
        ),
        "aperture": _plot(
            "Longer apertures observe more phase history",
            "Platform cross-range (m)",
            "Round-trip phase (turns)",
            [
                (f"{length:g} m aperture", p, phase)
                for length, (p, phase) in zip(lengths, geometry)
            ],
        ),
        "focus": _plot(
            "Candidate-path coherent sums on the same ridge",
            "Candidate cross-range (m)",
            "Normalized coherent score (ratio)",
            [
                ("Selected", candidates, active),
                ("Magnitude only", candidates, bad),
                ("Retained complex IQ", candidates, good),
            ],
        ),
    }
    return _finish(
        values,
        plots,
        "A 5 GHz antenna visits positions at.2m spacing. R=sqrt(1000²+(x-xt)²), delay=2R/c and phase=-4pi(R-1000)/lambda. A .6 m Gaussian envelope supplies the raw fast-time ridge. Candidate-path phase compensation coherently sums ridge samples; this is a single known-range illustration, not an image former.",
        "Taking magnitude preserves the delay ridge but erases aperture phase, so correct path compensation cannot align the data.",
        "Return to the unchanged complex ridge samples. Controls crop a fixed401x201 noise record when aperture changes, preserving nested measurements rather than regenerating noise.",
        7501,
        broken,
        aperture_phase_spans=spans,
        maximum_aperture_phase_steps=[
            float(max(abs(np.diff(-4 * np.pi * (r - 1000) / 0.06)))) for r in paths
        ],
        ridge_indices=ridge.tolist(),
        raw_shape=list(raw.shape),
        phase_history=phase.tolist(),
    )
