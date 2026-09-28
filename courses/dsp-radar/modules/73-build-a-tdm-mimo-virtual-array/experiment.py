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
    ("velocity_mps", 0, [-10, 0, 10]),
    ("source_separation_deg", 16, [8, 16, 28]),
]


def _tdm(velocity, seed):
    positions = np.arange(8) / 2
    slots = np.repeat([0, 1], 4)
    times = np.arange(64) * 80e-6 + slots[:, None] * 40e-6
    data = np.exp(
        -2j * np.pi * positions[:, None] * np.sin(np.deg2rad(18))
        - 2j * np.pi * (2 * velocity / (3e8 / 77e9)) * times
    ) + 0.1 * _noise(seed, 8, 64, True)
    fd = -np.angle(np.sum(data[:, :-1].conj() * data[:, 1:])) / (2 * np.pi * 80e-6)
    corrected = data * np.exp(2j * np.pi * fd * slots[:, None] * 40e-6)
    return data, corrected, fd


def _scan(x, grid):
    a = _steer(grid, len(x), -1)
    return np.mean(abs(a.conj().T @ x / len(x)) ** 2, axis=1)


def _pair_power(grid, count, separation):
    a = _steer([-separation / 2, separation / 2], count, -1)
    scan = _steer(grid, count, -1)
    return np.sum(abs(scan.conj().T @ a / count) ** 2, axis=1)


def _dip(power, grid):
    k = np.argmin(abs(grid))
    lo = np.argmax(power[: k + 1])
    hi = k + np.argmax(power[k:])
    dip = max(0, 10 * np.log10(min(power[lo], power[hi]) / power[k]))
    return dip, bool(dip >= 0.25 and grid[lo] < -0.25 and grid[hi] > 0.25)


def run(parameters):
    velocity, separation, broken = _controls(parameters, CONTROLS)
    grid = np.linspace(-60, 60, 1201)
    data, corrected, fd = _tdm(velocity, 7301)
    bad, rec, badfd = _tdm(10, 7401)
    active = bad if broken else corrected
    p = _scan(active, grid)
    rawp = _scan(data, grid)
    recp = _scan(rec, grid)
    physical = abs(_steer(grid, 4, -1).conj().T @ _steer(18, 4, -1)[:, 0] / 4) ** 2
    virtual = abs(_steer(grid, 8, -1).conj().T @ _steer(18, 8, -1)[:, 0] / 8) ** 2
    sep = np.array([8, 16, 28])
    pd = [_dip(_pair_power(grid, 4, s), grid) for s in sep]
    vd = [_dip(_pair_power(grid, 8, s), grid) for s in sep]
    vs = np.array([-10, -5, 0, 5, 10])
    before = []
    after = []
    for v in vs:
        x, y, _ = _tdm(v, 7401)
        before.append(grid[np.argmax(_scan(x, grid))])
        after.append(grid[np.argmax(_scan(y, grid))])
    values = {
        "active_angle": (grid[np.argmax(p)], "deg"),
        "angle_error": (grid[np.argmax(p)] - 18, "deg"),
        "selected_raw_angle": (grid[np.argmax(rawp)], "deg"),
        "estimated_velocity": (fd * (3e8 / 77e9) / 2, "m/s"),
        "physical_hpbw": (_width(grid, physical), "deg"),
        "virtual_hpbw": (_width(grid, virtual), "deg"),
        "selected_physical_dip": (
            _dip(_pair_power(grid, 4, separation), grid)[0],
            "dB",
        ),
        "selected_virtual_dip": (_dip(_pair_power(grid, 8, separation), grid)[0], "dB"),
        "named_broken_angle": (grid[np.argmax(_scan(bad, grid))], "deg"),
        "named_recovered_angle": (grid[np.argmax(recp)], "deg"),
        "named_estimated_velocity": (badfd * (3e8 / 77e9) / 2, "m/s"),
        "model_valid": (not broken, "boolean"),
    }
    plots = {
        "geometry": _plot(
            "TX plus RX positions give eight distinct virtual channels",
            "Channel (index)",
            "Position (wavelengths)",
            [
                ("RX", np.arange(4), np.arange(4) / 2),
                ("TX+RX", np.arange(8), np.arange(8) / 2),
            ],
        ),
        "patterns": _plot(
            "Physical and virtual apertures",
            "Angle (deg)",
            "Normalized response (dB)",
            [
                ("4 RX", grid, _db(physical, -50, True)),
                ("8 virtual", grid, _db(virtual, -50, True)),
                ("Selected measurement", grid, _db(p, -50, True)),
            ],
        ),
        "separation": _plot(
            "Equal incoherent pair: physical versus virtual",
            "Angle (deg)",
            "Normalized pair power (dB)",
            [
                ("4 RX", grid, _db(_pair_power(grid, 4, separation), -50, True)),
                ("8 virtual", grid, _db(_pair_power(grid, 8, separation), -50, True)),
            ],
        ),
        "resolution": _plot(
            "Separation and the valley between peaks",
            "Pair separation (deg)",
            "Midpoint dip (dB)",
            [
                ("Physical", sep, [v[0] for v in pd]),
                ("Virtual", sep, [v[0] for v in vd]),
            ],
        ),
        "motion": _plot(
            "TDM motion bias and same-TX Doppler correction",
            "Approaching velocity (m/s)",
            "Estimated angle (deg)",
            [("Uncompensated", vs, before), ("Compensated", vs, after)],
        ),
        "recovery": _plot(
            "Same 10 m/s record before and after slot compensation",
            "Angle (deg)",
            "Normalized power (dB)",
            [
                ("Broken", grid, _db(_scan(bad, grid), -50, True)),
                ("Recovered", grid, _db(recp, -50, True)),
            ],
        ),
    }
    return _finish(
        values,
        plots,
        "Two TX at 0/2 wavelengths and four RX at 0:.5:1.5 create eight TX+RX positions. Tx-conjugate processing has negative spatial and Doppler phase. A lag-one estimate across 80 us same-TX cycles measures Doppler; correcting the 40 us slot offset restores virtual-array coherence.",
        "Treating the named 10 m/s TDM record as simultaneous lets motion phase masquerade as angle.",
        "Multiply each virtual channel by exp(+j2pi fd slot_time) using the same-TX estimate. Recovery reuses the noisy record and assumes one unaliased target Doppler; the reviewed speed range lies below same-TX Nyquist.",
        7301,
        broken,
        virtual_positions=(np.arange(8) / 2).tolist(),
        tx_slots=np.repeat([0, 1], 4).tolist(),
        physical_resolved=[x[1] for x in pd],
        virtual_resolved=[x[1] for x in vd],
        motion_angles_before=before,
        motion_angles_after=after,
    )
