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
    ("snapshots", 128, [4, 16, 128, 256]),
    ("loading_alpha", 0.01, [1e-6, 0.01, 0.1, 1]),
]


def _components(w, a):
    powers = np.array(
        [
            10 ** (-0.3) * abs(np.vdot(w, a[:, 0])) ** 2,
            10**2.5 * abs(np.vdot(w, a[:, 1])) ** 2,
            np.vdot(w, w).real,
        ]
    )
    return powers, 10 * np.log10(powers[0] / sum(powers[1:]))


def run(parameters):
    count, alpha, broken = _controls(parameters, CONTROLS)
    count = int(count)
    a = _steer([3, 30], 8)
    grid = np.linspace(-50, 50, 1001)
    scan = _steer(grid, 8)
    sources = np.array(
        [np.exp(2j * np.pi * _uniform(seed, 256)) for seed in [6501, 6502]]
    )
    data = a @ (np.sqrt([10 ** (-0.3), 10**2.5])[:, None] * sources) + _noise(
        6503, 8, 256
    )
    r = _cov(data[:, :count])
    good = _mvdr(r, a[:, 0], alpha)
    fixed = a[:, 0] / 8
    starved = _cov(data[:, :4])
    bad = _mvdr(starved, _steer(6, 8)[:, 0], 1e-6)
    loaded = _mvdr(starved, _steer(6, 8)[:, 0], 0.1)
    corrected = _mvdr(starved, a[:, 0], 0.1)
    w = bad if broken else good
    powers, sinr = _components(w, a)
    ns = np.array([4, 8, 16, 32, 64, 128, 256])
    support = [_components(_mvdr(_cov(data[:, :k]), a[:, 0], alpha), a)[1] for k in ns]
    alphas = np.array([1e-6, 1e-4, 1e-3, 0.01, 0.1, 1])
    mismatch = _cov(data[:, :8])
    loading = [
        _components(_mvdr(mismatch, _steer(6, 8)[:, 0], v), a)[1] for v in alphas
    ]
    raw_rcond = 1 / np.linalg.cond(starved, 1).real
    values = {
        "output_sinr": (sinr, "dB"),
        "fixed_sinr": (_components(fixed, a)[1], "dB"),
        "true_response": (abs(np.vdot(w, a[:, 0])), "ratio"),
        "interferer_response": (abs(np.vdot(w, a[:, 1])), "ratio"),
        "noise_power": (powers[2], "power"),
        "loading_power": (alpha * np.trace(r).real / 8, "power"),
        "distortionless_error": (abs(np.vdot(good, a[:, 0]) - 1), "ratio"),
        "raw_solve_refused": (int(raw_rcond < 1e-12), "boolean"),
        "loaded_recovery_sinr": (_components(loaded, a)[1], "dB"),
        "corrected_recovery_sinr": (_components(corrected, a)[1], "dB"),
        "snapshot4_sinr": (support[0], "dB"),
        "loading_small_sinr": (loading[0], "dB"),
        "model_valid": (not broken, "boolean"),
    }
    plots = {
        "covariance": _heat(
            "Measured covariance before adaptation",
            "Sensor (index)",
            "Sensor (index)",
            np.arange(8),
            np.arange(8),
            _db(abs(r), relative=True),
            "dB",
        ),
        "eigenvalues": _plot(
            "Covariance eigenvalues",
            "Descending mode (index)",
            "Noise-relative eigenvalue (dB)",
            [("Measured", np.arange(8), _db(np.linalg.eigvalsh(r)[::-1]))],
        ),
        "pattern": _plot(
            "Constrained response and adaptive interference null",
            "Angle (deg)",
            "Voltage response (dB)",
            [
                (label, grid, _db(abs(weight.conj() @ scan) ** 2))
                for label, weight in [
                    ("Conventional", fixed),
                    ("Selected", w),
                    ("Loaded recovery", loaded),
                    ("Corrected recovery", corrected),
                ]
            ],
        ),
        "components": _plot(
            "Output component accounting",
            "Component: desired/interference/noise (index)",
            "Output power (dB)",
            [
                (label, [0, 1, 2], _db(_components(weight, a)[0]))
                for label, weight in [("Conventional", fixed), ("Selected", w)]
            ],
        ),
        "support": _plot(
            "Nested snapshot prefixes",
            "Snapshots (count)",
            "Output SINR (dB)",
            [("Loaded matched look", ns, support)],
        ),
        "loading": _plot(
            "Eight-snapshot mismatched look at 6 degrees",
            "Log10 loading alpha (ratio)",
            "Output SINR (dB)",
            [("Same covariance", np.log10(alphas), loading)],
        ),
    }
    return _finish(
        values,
        plots,
        "Eight half-wavelength sensors observe a weak 3-degree source and a 25 dB interferer at 30 degrees. R=X X^H/N; loading is alpha trace(R)/8; w=solve(R+delta I,a)/(a^H solve). Components use the true manifold only for performance accounting.",
        "The named four-snapshot covariance is singular without loading. A barely loaded 6-degree look can suppress the true 3-degree source.",
        "On the unchanged four snapshots, alpha=.1 stabilizes the solve; correcting the look restores unit true response. Disable the toggle to restore the selected baseline.",
        6501,
        broken,
        snapshot_sinr=support,
        loading_sinr=loading,
        covariance_real=r.real.tolist(),
        covariance_imag=r.imag.tolist(),
        raw_rcond=float(raw_rcond),
    )
