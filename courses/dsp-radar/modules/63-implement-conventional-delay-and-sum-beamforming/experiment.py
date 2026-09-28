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


def _complex_noise(seed, rows, columns):
    u = _uniform(seed, 2 * rows * columns)
    z = np.sqrt(-np.log(u[::2])) * np.exp(2j * np.pi * u[1::2])
    return z.reshape(columns, rows).T


def _scene(seed, elements, angles, snr):
    sources = np.exp(2j * np.pi * _uniform(seed, 256)).reshape(128, 2).T
    noise = _complex_noise(seed + 1, 16, 128)[:elements] * 10 ** (-snr / 20)
    steering = np.exp(
        1j * np.pi * np.arange(elements)[:, None] * np.sin(np.deg2rad(angles))
    )
    return steering @ sources + noise


def _scan(data, angles, sign=1):
    m = len(data)
    weights = (
        np.exp(1j * sign * np.pi * np.arange(m)[:, None] * np.sin(np.deg2rad(angles)))
        / m
    )
    output = np.einsum("ma,ml->al", weights.conj(), data, optimize=False)
    return np.mean(abs(output) ** 2, axis=1)


def _peaks(angles, power, expected, radius=5):
    peaks = []
    local = []
    for truth in expected:
        candidates = np.flatnonzero(abs(angles - truth) <= radius + 1e-10)
        j = candidates[np.argmax(power[candidates])]
        peaks.append(float(angles[j]))
        local.append(
            bool(
                0 < j < len(power) - 1
                and power[j] >= power[j - 1]
                and power[j] > power[j + 1]
            )
        )
    return peaks, local


def run(parameters):
    elements, snr, broken = _controls(
        parameters,
        [("elements", 8, [4, 8, 16]), ("source_snr_db", 10, [-15, 0, 10, 15])],
    )
    elements = int(elements)
    angles = np.linspace(-60, 60, 1201)
    data = _scene(6301, elements, [-20, 25], snr)
    baseline = _scan(data, angles)
    bad_data = _scene(6315, elements, [-20, 30], snr)
    wrong = _scan(bad_data, angles, -1)
    recovery = _scan(bad_data, angles, 1)
    active = wrong if broken else baseline
    peaks, _ = _peaks(angles, active, [-30, 20] if broken else [-20, 25])
    background = (abs(angles + 20) > 10) & (abs(angles - 25) > 10)
    db = lambda a: 10 * np.log10(np.maximum(a / a.max(), 10 ** (-35 / 10)))
    separation = []
    resolved = []
    for sep in [6, 12, 24]:
        a = _scan(_scene(6311, elements, [-sep / 2, sep / 2], snr), angles)
        p, local = _peaks(angles, a, [-sep / 2, sep / 2], 4)
        separation.append(a)
        resolved.append(bool(all(local) and p[1] - p[0] > sep / 2))
    aperture = []
    aperture_resolved = []
    for m in [4, 8, 16]:
        a = _scan(_scene(6312, m, [-8, 8], snr), angles)
        p, local = _peaks(angles, a, [-8, 8])
        aperture.append(a)
        aperture_resolved.append(bool(all(local) and p[1] - p[0] > 8))
    snr_power = [
        _scan(_scene(6313, elements, [-20, 25], s), angles) for s in [-15, 0, 15]
    ]
    floors = [
        float(10 * np.log10(np.median(a[background]) / a.max())) for a in snr_power
    ]
    snapshot_data = _scene(6314, elements, [-20, 25], 0)
    snapshot_power = [_scan(snapshot_data[:, :l], angles) for l in [1, 8, 128]]
    ripple = [float(np.std(db(a)[background], ddof=1)) for a in snapshot_power]
    # Source-direction conjugation aligns one source's sensor contributions.
    align = (
        np.exp(-1j * np.pi * np.arange(elements) * np.sin(np.deg2rad(-20))) * data[:, 0]
    )
    active_background = (
        (abs(angles + 30) > 10) & (abs(angles - 20) > 10) if broken else background
    )
    values = {
        "model_valid": (not broken, "boolean"),
        "first_peak_angle": (peaks[0], "deg"),
        "second_peak_angle": (peaks[1], "deg"),
        "maximum_output_power": (active.max(), "voltage²"),
        "median_relative_background": (
            10 * np.log10(np.median(active[active_background]) / active.max()),
            "dB",
        ),
        "wrong_sign_mirror_error": (abs(wrong - recovery[::-1]).max(), "voltage²"),
        "wide_separation_resolved": (resolved[-1], "boolean"),
        "large_aperture_resolved": (aperture_resolved[-1], "boolean"),
        "snapshot128_ripple": (ripple[-1], "dB"),
        "snr15_relative_floor": (floors[-1], "dB"),
    }
    plots = {
        "scan": _plot(
            "Hermitian steering and mean beam-output power",
            "Scan angle (deg)",
            "Relative output power (dB)",
            [("Active scan", angles, db(active))],
        ),
        "alignment": _plot(
            "Element contributions after steering toward -20 degrees",
            "Element index (count)",
            "Snapshot voltage (normalized)",
            [
                ("Aligned I", np.arange(elements), align.real),
                ("Aligned Q", np.arange(elements), align.imag),
            ],
        ),
        "separation": _plot(
            "Same noise: change source separation",
            "Scan angle (deg)",
            "Relative output power (dB)",
            [
                (f"{s} degree separation", angles, db(a))
                for s, a in zip([6, 12, 24], separation)
            ],
        ),
        "aperture": _plot(
            "Same +/-8 degree sources: change aperture",
            "Scan angle (deg)",
            "Relative output power (dB)",
            [(f"{m} elements", angles, db(a)) for m, a in zip([4, 8, 16], aperture)],
        ),
        "snr": _plot(
            "Per-source, per-sensor SNR changes scan floor",
            "Input SNR (dB)",
            "Median relative background (dB)",
            [("128 snapshots", [-15, 0, 15], floors)],
        ),
        "snapshots": _plot(
            "More snapshots average random scan variation",
            "Snapshots (count)",
            "Background ripple standard deviation (dB)",
            [("Same 0 dB record prefixes", [1, 8, 128], ripple)],
        ),
        "failure": _plot(
            "Wrong phase sign mirrors the source directions",
            "Scan angle (deg)",
            "Relative output power (dB)",
            [
                ("Wrong sign, source scene -20/+30", angles, db(wrong)),
                ("Correct sign recovery, same data", angles, db(recovery)),
            ],
        ),
    }
    plots["sensor_data"] = _heat(
        "Received matrix before spatial matching: baseline I channel",
        "Snapshot (index)",
        "Sensor (index)",
        np.arange(1, 129),
        np.arange(1, elements + 1),
        data.real,
        "normalized voltage",
    )
    return _finish(
        values,
        plots,
        "The narrowband sensor matrix X=A S+N is matched by w=a(theta)/M. Hermitian steering aligns the chosen direction before mean squared output measures spatial response.",
        "Reversing the steering phase convention mirrors the named -20/+30 degree scene. The failure keeps sensor data fixed and changes only the steering sign.",
        "Restore the conjugate steering convention on that same named scene. Disable the toggle to return exactly to the selected -20/+25 degree baseline. Fixed phase weights assume narrowband signals.",
        6301,
        broken,
        separation_resolved=resolved,
        aperture_resolved=aperture_resolved,
        snr_sweep_floor=floors,
        snapshot_sweep_ripple=ripple,
        calculation_angle_samples=1201,
        snapshots=128,
        broken_scene_seed=6315,
    )
