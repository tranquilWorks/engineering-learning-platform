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
    ("training_cells", 128, [8, 32, 128]),
    ("contamination_fraction", 0, [0, 0.1, 0.4]),
]


def _st(angle, doppler):
    return np.kron(np.exp(2j * np.pi * np.arange(8) * doppler), _steer(angle, 8)[:, 0])


def _metrics(w, a, r):
    signal = abs(np.vdot(w, a)) ** 2
    interference = np.vdot(w, r @ w).real
    return np.array(
        [
            10 * np.log10(signal / interference),
            10 * np.log10(signal),
            10 * np.log10(interference),
        ]
    )


def run(parameters):
    support, fraction, broken = _controls(parameters, CONTROLS)
    support = int(support)
    angles = np.arange(-60, 61, 2)
    ridge = 0.35 * np.sin(np.deg2rad(angles))
    powers = np.cos(np.deg2rad(angles)) ** 2
    powers *= 1000 / sum(powers)
    manifold = np.column_stack([_st(t, d) for t, d in zip(angles, ridge)])
    weighted = manifold * np.sqrt(powers)
    population = weighted @ weighted.conj().T + np.eye(64)
    full = weighted @ _noise(6801, 61, 128) + _noise(6802, 64, 128)
    train = full[:, :support]
    assumed = _st(10, 0.2)
    actual = _st(10.7, 0.208)
    r = _cov(train)
    cube = train.reshape((8, 8, support), order="F")
    spatial = np.einsum("ipk,jpk->ij", cube, cube.conj()) / (8 * support)
    temporal = np.einsum("ipk,iqk->pq", cube, cube.conj()) / (8 * support)
    fixed = assumed / 64
    separate = np.kron(
        _mvdr(temporal, np.exp(2j * np.pi * np.arange(8) * 0.2), 0.03),
        _mvdr(spatial, _steer(10, 8)[:, 0], 0.03),
    )
    clean = _mvdr(r, assumed, 0.03)
    waveform = _noise(6803, 1, 128)[0]

    def contaminated(frac):
        x = train.copy()
        k = int(np.floor(frac * support + 0.5))
        x[:, :k] += 10 * actual[:, None] * waveform[:k]
        return _mvdr(_cov(x), assumed, 0.03)

    selected_fraction = 0.4 if broken else fraction
    active = contaminated(selected_fraction)
    components = np.array(
        [_metrics(w, actual, population) for w in [fixed, separate, active, clean]]
    )
    ns = np.array([8, 16, 32, 64, 128])
    scnr = [
        _metrics(_mvdr(_cov(full[:, :n]), assumed, 0.03), actual, population)[0]
        for n in ns
    ]
    fractions = np.array([0, 0.05, 0.1, 0.2, 0.4])
    loss = np.array([_metrics(contaminated(f), actual, population) for f in fractions])
    dopplers = np.linspace(-0.45, 0.45, 61)
    mapping = np.column_stack([_st(t, d) for d in dopplers for t in angles])
    clutter = np.real(np.sum(mapping.conj() * (r @ mapping), axis=0)) / 64**2
    maps = [
        abs(w.conj() @ mapping).reshape(61, 61) ** 2 for w in [fixed, separate, active]
    ]
    cut = weighted @ _noise(6804, 61, 1)[:, 0] + _noise(6805, 64, 1)[:, 0] + actual
    values = {
        "active_scnr": (components[2, 0], "dB"),
        "fixed_scnr": (components[0, 0], "dB"),
        "separate_scnr": (components[1, 0], "dB"),
        "clean_scnr": (components[3, 0], "dB"),
        "target_response": (components[2, 1], "dB"),
        "interference_output": (components[2, 2], "dB"),
        "distortionless_error": (abs(np.vdot(active, assumed) - 1), "ratio"),
        "support8_scnr": (scnr[0], "dB"),
        "contaminated_scnr": (loss[-1, 0], "dB"),
        "cut_output_magnitude": (abs(np.vdot(active, cut)), "voltage"),
        "selected_contaminated_cells": (
            np.floor(selected_fraction * support + 0.5),
            "count",
        ),
        "model_valid": (not broken, "boolean"),
    }
    plots = {
        "ridge": _heat(
            "Measured angle-Doppler clutter ridge",
            "Angle (deg)",
            "Normalized Doppler (cycles/pulse)",
            angles,
            dopplers,
            _db(clutter.reshape(61, 61), -60, True),
            "dB",
        ),
        "covariance": _heat(
            "Joint sensor/pulse sample covariance",
            "Space-time channel (index)",
            "Space-time channel (index)",
            np.arange(64),
            np.arange(64),
            _db(abs(r), -60, True),
            "dB",
        ),
        "fixed": _heat(
            "Fixed response",
            "Angle (deg)",
            "Normalized Doppler (cycles/pulse)",
            angles,
            dopplers,
            _db(maps[0], -60, True),
            "dB",
        ),
        "separate": _heat(
            "Separate spatial and temporal response",
            "Angle (deg)",
            "Normalized Doppler (cycles/pulse)",
            angles,
            dopplers,
            _db(maps[1], -60, True),
            "dB",
        ),
        "joint": _heat(
            "Selected joint response",
            "Angle (deg)",
            "Normalized Doppler (cycles/pulse)",
            angles,
            dopplers,
            _db(maps[2], -60, True),
            "dB",
        ),
        "support": _plot(
            "Clean training prefixes",
            "Training cells (count)",
            "Output SCNR (dB)",
            [("Joint", ns, scnr)],
        ),
        "contamination": _plot(
            "Target-like training contaminates adaptation",
            "Contamination fraction (ratio)",
            "Output response (dB)",
            [
                ("SCNR", fractions, loss[:, 0]),
                ("Target response", fractions, loss[:, 1]),
            ],
        ),
        "components": _plot(
            "Target and interference output accounting",
            "Fixed/separate/selected/clean (index)",
            "Output power (dB)",
            [
                ("Target", np.arange(4), components[:, 1]),
                ("Interference", np.arange(4), components[:, 2]),
            ],
        ),
    }
    return _finish(
        values,
        plots,
        "The 64-channel vector stacks all eight sensors inside each of eight pulses. Clutter obeys normalized Doppler=.35 sin(theta). Joint covariance keeps angle-Doppler coupling that separate covariance estimates discard. The cell under test uses independent seeds and never trains covariance.",
        "The named failure contaminates 40% of training cells with the actual slightly mismatched target. Unit response at the assumed steering does not prevent self-nulling at the actual steering.",
        "Restore unchanged clean training cells. This recovers the clean joint weight; removing a target component requires justified training selection, not knowledge available from every operational scene. Toggle off restores the selected contamination control.",
        6801,
        broken,
        training_support_scnr=scnr,
        contamination_scnr=loss[:, 0].tolist(),
        clutter_ridge=ridge.tolist(),
        stack_order="sensor-within-pulse",
        training_rank=int(np.linalg.matrix_rank(r)),
        clean_weight_real=clean.real.tolist(),
        clean_weight_imag=clean.imag.tolist(),
    )
