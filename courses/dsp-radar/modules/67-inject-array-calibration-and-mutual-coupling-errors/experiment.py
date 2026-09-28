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
    ("error_scale", 1, [0, 0.5, 1, 1.5]),
    ("coupling_magnitude", 0.18, [0, 0.18, 0.3]),
]


def _manifold(angles, positions):
    return np.exp(
        2j
        * np.pi
        * np.asarray(positions)[:, None]
        * np.sin(np.deg2rad(np.atleast_1d(angles)))
    )


def _scene(scale, coupling):
    u = _uniform(6701, 30).reshape(3, 10)
    u -= u.mean(axis=1, keepdims=True)
    u /= np.sqrt(np.mean(u * u, axis=1, keepdims=True))
    positions = np.arange(10) / 2 + 0.05 * scale * u[2]
    gains = (1 + 0.18 * scale * u[0]) * np.exp(1j * np.deg2rad(20 * scale * u[1]))
    near = coupling * np.exp(1j * np.deg2rad(25))
    c = np.eye(10, dtype=complex)
    for d, v in [(1, near), (2, 0.3 * near**2)]:
        c += np.diag(np.full(10 - d, v), d) + np.diag(np.full(10 - d, v), -d)
    error = gains[:, None] * c
    nominal = _steer([-15, 10], 10)
    actual = error @ _manifold([-15, 10], positions)
    waves = (
        np.array([np.exp(2j * np.pi * _uniform(s, 512)) for s in [6702, 6703]])
        * np.sqrt([10**2.5, 10])[:, None]
    )
    noise = _noise(6704, 10, 512)
    ideal = nominal @ waves + noise
    impaired = actual @ waves + noise
    cw = np.exp(2j * np.pi * _uniform(6705, 256))
    ca = error @ _manifold(10, positions)[:, 0]
    caldata = ca[:, None] * np.sqrt(1000) * cw + _noise(6706, 10, 256)
    measured = caldata @ cw.conj() / 256 / np.sqrt(1000)
    response = measured / _steer(10, 10)[:, 0]
    return (
        nominal,
        actual,
        ideal,
        impaired,
        1 / response,
        1 / measured,
        gains,
        positions,
        c,
        ca,
    )


def _outputs(x, noise_diagonal, grid):
    r = _cov(x)
    a = _steer(grid, 10)
    bart = np.real(np.sum(a.conj() * (r @ a), axis=0)) / 100
    loaded = r + 0.02 * np.trace(r).real / 10 * np.eye(10)
    capon = 1 / np.real(np.sum(a.conj() * np.linalg.solve(loaded, a), axis=0))
    whitening = 1 / np.sqrt(noise_diagonal)
    wr = whitening[:, None] * r * whitening[None, :]
    _, v = np.linalg.eigh(wr)
    en = v[:, :8]
    wa = whitening[:, None] * a
    music = 1 / np.maximum(np.sum(abs(en.conj().T @ wa) ** 2, axis=0), 1e-30)
    return [_db(p, -60, True) for p in [bart, capon, music]]


def _account(x, a, noise):
    w = _mvdr(_cov(x), _steer(10, 10)[:, 0], 0.02)
    response = abs(w.conj() @ a) ** 2
    p = np.array([10 * response[1], 10**2.5 * response[0], np.sum(abs(w) ** 2 * noise)])
    return 10 * np.log10(p[0] / sum(p[1:])), 10 * np.log10(response[1]), w


def run(parameters):
    scale, coupling, broken = _controls(parameters, CONTROLS)
    grid = np.linspace(-40, 40, 801)
    nominal, actual, ideal, impaired, eq, wrong, gains, positions, c, ca = _scene(
        scale, coupling
    )
    calibrated = eq[:, None] * impaired
    activeeq = wrong if broken else eq
    active = activeeq[:, None] * impaired
    curves = [
        _outputs(x, n, grid)
        for x, n in [
            (ideal, np.ones(10)),
            (impaired, np.ones(10)),
            (active, abs(activeeq) ** 2),
        ]
    ]
    stats = [
        _account(x, a, n)
        for x, a, n in [
            (ideal, nominal, np.ones(10)),
            (impaired, actual, np.ones(10)),
            (active, activeeq[:, None] * actual, abs(activeeq) ** 2),
            (calibrated, eq[:, None] * actual, abs(eq) ** 2),
        ]
    ]
    peaks = _peaks(curves[2][2], grid, 2, 2)
    rmse = np.sqrt(np.mean((peaks - [-15, 10]) ** 2)) if len(peaks) == 2 else 80.0
    error = lambda q: float(
        np.linalg.norm(q * ca - nominal[:, 1]) / np.linalg.norm(nominal[:, 1])
    )
    scales = np.array([0, 0.25, 0.5, 0.75, 1, 1.25, 1.5])
    couplings = np.array([0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3])

    def sweep(xs, which):
        before = []
        after = []
        for v in xs:
            _, a, _, x, e, *_ = _scene(
                v if which == 0 else scale, coupling if which == 0 else v
            )
            before.append(_account(x, a, np.ones(10))[0])
            after.append(_account(e[:, None] * x, e[:, None] * a, abs(e) ** 2)[0])
        return before, after

    es = sweep(scales, 0)
    cs = sweep(couplings, 1)
    values = {
        "active_sinr": (stats[2][0], "dB"),
        "impaired_sinr": (stats[1][0], "dB"),
        "ideal_sinr": (stats[0][0], "dB"),
        "recovered_sinr": (stats[3][0], "dB"),
        "active_known_response": (stats[2][1], "dB"),
        "manifold_error_before": (error(np.ones(10)), "ratio"),
        "manifold_error_active": (error(activeeq), "ratio"),
        "manifold_error_recovered": (error(eq), "ratio"),
        "music_rmse": (rmse, "deg"),
        "first_music_peak": (peaks[0] if len(peaks) else 0, "deg"),
        "other_direction_residual": (
            np.linalg.norm(eq * actual[:, 0] - nominal[:, 0]) / np.sqrt(10),
            "ratio",
        ),
        "model_valid": (not broken, "boolean"),
    }
    plots = {
        "channels": _plot(
            "Fixed channel gain and estimated equalizer",
            "Sensor (index)",
            "Voltage magnitude (ratio)",
            [
                ("Gain", np.arange(10), abs(gains)),
                ("Composite estimate", np.arange(10), abs(1 / eq)),
            ],
        ),
        "phase": _plot(
            "Position and channel phase errors",
            "Sensor (index)",
            "Channel phase (deg)",
            [
                ("Injected", np.arange(10), np.rad2deg(np.angle(gains))),
                ("Estimated composite", np.arange(10), np.rad2deg(np.angle(1 / eq))),
            ],
        ),
        "bartlett": _plot(
            "Conventional beam with channel errors",
            "Angle (deg)",
            "Normalized power (dB)",
            [
                (k, grid, v[0])
                for k, v in zip(["Ideal", "Impaired", "Selected calibration"], curves)
            ],
        ),
        "capon": _plot(
            "Loaded Capon spatial spectrum",
            "Angle (deg)",
            "Normalized power (dB)",
            [
                (k, grid, v[1])
                for k, v in zip(["Ideal", "Impaired", "Selected calibration"], curves)
            ],
        ),
        "music": _plot(
            "Noise-whitened MUSIC",
            "Angle (deg)",
            "Normalized spectrum (dB)",
            [
                (k, grid, v[2])
                for k, v in zip(["Ideal", "Impaired", "Selected calibration"], curves)
            ],
        ),
        "error_sweep": _plot(
            "Fixed gain/phase/position patterns scaled together",
            "Error scale (ratio)",
            "Output SINR (dB)",
            [("Before", scales, es[0]), ("After", scales, es[1])],
        ),
        "coupling": _plot(
            "Nearest-neighbor coupling sweep",
            "Coupling magnitude (ratio)",
            "Output SINR (dB)",
            [("Before", couplings, cs[0]), ("After", couplings, cs[1])],
        ),
    }
    return _finish(
        values,
        plots,
        "A known 10-degree calibration source estimates each composite response after removing nominal steering. Equalization also colors receiver noise; MUSIC whitens with diag(|equalizer|²). Coupling and position errors make the residual direction-dependent.",
        "Dividing by the raw calibration response without removing its known steering phase makes the calibration source appear at boresight.",
        "Divide the measured response by nominal 10-degree steering before equalization. This repairs the known direction on unchanged data; it does not identify a global coupling inverse.",
        6701,
        broken,
        positions=positions.tolist(),
        coupling_real=c.real.tolist(),
        coupling_imag=c.imag.tolist(),
        music_peaks=peaks.tolist(),
        error_sweep_before=es[0],
        error_sweep_after=es[1],
        coupling_sweep_after=cs[1],
    )
