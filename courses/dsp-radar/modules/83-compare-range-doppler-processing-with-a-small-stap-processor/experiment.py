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


def _amplitude_width(axis, magnitude):
    peak = int(np.argmax(magnitude))
    level = magnitude[peak] / np.sqrt(2)
    left = right = peak
    while left > 0 and magnitude[left] >= level:
        left -= 1
    while right < len(axis) - 1 and magnitude[right] >= level:
        right += 1
    if magnitude[left] >= level or magnitude[right] >= level:
        return float(axis[-1] - axis[0])
    lo = axis[left] + (level - magnitude[left]) * (axis[left + 1] - axis[left]) / (
        magnitude[left + 1] - magnitude[left]
    )
    hi = axis[right - 1] + (level - magnitude[right - 1]) * (
        axis[right] - axis[right - 1]
    ) / (magnitude[right] - magnitude[right - 1])
    return float(hi - lo)


def _linear_row(row, axis, query):
    f = (query - axis[0]) / (axis[1] - axis[0])
    left = np.floor(f).astype(int)
    valid = (left >= 0) & (left < len(axis) - 1)
    j = np.clip(left, 0, len(axis) - 2)
    w = f - left
    return np.where(valid, (1 - w) * row[j] + w * row[j + 1], 0)


CONTROLS = [
    ("training_cells", 36, [8, 16, 24, 36]),
    ("contaminated_fraction", 0, [0, 0.25, 0.5]),
]


def _steering83(angle, doppler):
    space = np.exp(1j * np.pi * np.arange(4) * np.sin(np.deg2rad(angle)))
    return np.kron(np.exp(2j * np.pi * np.arange(8) * doppler), space)


def _record83():
    angles = np.arange(-60, 61, 3)
    ridge = 0.3 * np.sin(np.deg2rad(angles))
    powers = np.cos(np.deg2rad(angles)) ** 2
    powers *= 10**3.2 / sum(powers)
    manifold = np.column_stack(
        [_steering83(a, d) * np.sqrt(q) for a, d, q in zip(angles, ridge, powers)]
    )
    known = manifold @ manifold.conj().T + np.eye(32)
    background = manifold @ _noise(8301, 41, 48) + _noise(8302, 32, 48)
    train = np.r_[np.arange(4, 22), np.arange(27, 45)]
    actual = _steering83(12.5, 0.125)
    measured = background.copy()
    measured[:, 24] += np.sqrt(10**1.8) * actual
    return angles, ridge, known, background[:, train], measured, actual


def _solve83(covariance, steering):
    loaded = covariance + 0.05 * np.trace(covariance).real / 32 * np.eye(32)
    solution = np.linalg.solve(loaded, steering)
    denominator = np.sum(steering.conj() * solution, axis=0).real
    return solution, solution / denominator, denominator, loaded


def _component83(weight, actual, known):
    signal = 10**1.8 * abs(np.vdot(weight, actual)) ** 2
    interference = np.vdot(weight, known @ weight).real
    return (
        float(10 * np.log10(signal / interference)),
        float(signal),
        float(interference),
    )


def run(parameters):
    support, fraction, broken = _controls(parameters, CONTROLS)
    support = int(support)
    fraction = 0.25 if broken else fraction
    angles, ridge, known, training, measured, actual = _record83()
    selected = training[:, :support]
    clean = selected @ selected.conj().T / support
    contaminated = selected.copy()
    count = int(np.floor(fraction * support + 0.5))
    contamination = _noise(8303, 1, 36)[0, :count]
    contaminated[:, :count] += np.sqrt(1000) * actual[:, None] * contamination[None, :]
    active_cov = contaminated @ contaminated.conj().T / support
    grid = np.linspace(-0.25, 0.25, 51)
    s = np.column_stack([_steering83(12, d) for d in grid])
    target_bin = 37
    u, w, den, _loaded = _solve83(active_cov, s)
    uc, wc, denc, cleanloaded = _solve83(clean, s)
    amap = abs(u.conj().T @ measured) ** 2 / den[:, None]
    cmap = abs(uc.conj().T @ measured) ** 2 / denc[:, None]
    fixed = s / 32
    fixedvar = np.sum(fixed.conj() * (cleanloaded @ fixed), axis=0).real
    rdmap = abs(fixed.conj().T @ measured) ** 2 / fixedvar[:, None]
    active_scnr, signal, interference = _component83(w[:, target_bin], actual, known)
    clean_scnr, clean_signal, clean_interference = _component83(
        wc[:, target_bin], actual, known
    )
    rd_scnr, _, _ = _component83(fixed[:, target_bin], actual, known)
    mask = np.ones(amap.shape, bool)
    mask[target_bin - 1 : target_bin + 2, 22:27] = False
    contrast = lambda a: float(10 * np.log10(a[target_bin, 24] / np.median(a[mask])))
    supports = [8, 16, 24, 36]
    support_scnr = []
    ranks = []
    conditions = []
    for n in supports:
        r = training[:, :n] @ training[:, :n].conj().T / n
        _, ww, _, ll = _solve83(r, s[:, target_bin])
        support_scnr.append(_component83(ww, actual, known)[0])
        ranks.append(
            int(np.linalg.matrix_rank(r, tol=np.max(abs(np.linalg.eigvalsh(r))) * 1e-8))
        )
        conditions.append(float(np.linalg.cond(ll)))
    offsets = [0.01, 0.03, 0.06, 0.1]
    ridge_rd = []
    ridge_stap = []
    full = training @ training.conj().T / 36
    for offset in offsets:
        a = _steering83(12.5, 0.3 * np.sin(np.deg2rad(12.5)) + offset)
        _, ww, _, _ = _solve83(full, a)
        ridge_rd.append(_component83(a / 32, a, known)[0])
        ridge_stap.append(_component83(ww, a, known)[0])
    peak = np.unravel_index(np.argmax(amap), amap.shape)
    values = {
        "active_scnr": (active_scnr, "dB"),
        "clean_scnr": (clean_scnr, "dB"),
        "fixed_scnr": (rd_scnr, "dB"),
        "active_target_contrast": (contrast(amap), "dB"),
        "fixed_target_contrast": (contrast(rdmap), "dB"),
        "target_output_change": (10 * np.log10(signal / clean_signal), "dB"),
        "interference_output_change": (
            10 * np.log10(interference / clean_interference),
            "dB",
        ),
        "distortionless_error": (
            abs(np.vdot(w[:, target_bin], s[:, target_bin]) - 1),
            "ratio",
        ),
        "peak_range_cell": (peak[1] + 1, "cell"),
        "peak_normalized_doppler": (grid[peak[0]], "cycles/pulse"),
        "contaminated_cells": (count, "count"),
        "model_valid": (not broken, "boolean"),
    }
    plots = {
        "ridge": _plot(
            "Moving-platform clutter ridge",
            "Azimuth angle (deg)",
            "Normalized Doppler (cycles/pulse)",
            [("0.30 sin(theta)", angles, ridge)],
        ),
        "fixed": _heat(
            "Fixed beam then Doppler filtering",
            "Range cell (cell)",
            "Normalized Doppler (cycles/pulse)",
            np.arange(1, 49),
            grid,
            _db(rdmap),
            "normalized power (dB)",
        ),
        "active": _heat(
            "Selected training: adaptive matched-filter map",
            "Range cell (cell)",
            "Normalized Doppler (cycles/pulse)",
            np.arange(1, 49),
            grid,
            _db(amap),
            "normalized power (dB)",
        ),
        "clean": _heat(
            "Clean training comparison on identical measurements",
            "Range cell (cell)",
            "Normalized Doppler (cycles/pulse)",
            np.arange(1, 49),
            grid,
            _db(cmap),
            "normalized power (dB)",
        ),
        "cut": _plot(
            "Target-cell Doppler slice",
            "Normalized Doppler (cycles/pulse)",
            "Normalized output power (dB)",
            [
                ("Fixed", grid, _db(rdmap[:, 24])),
                ("Clean adaptive", grid, _db(cmap[:, 24])),
                ("Selected adaptive", grid, _db(amap[:, 24])),
            ],
        ),
        "support": _plot(
            "Clean training support",
            "Training snapshots (count)",
            "Known-component SCNR (dB)",
            [("Loaded adaptive", supports, support_scnr)],
        ),
        "offset": _plot(
            "Distance from the angle-Doppler ridge",
            "Target ridge offset (cycles/pulse)",
            "Known-component SCNR (dB)",
            [("Fixed", offsets, ridge_rd), ("Adaptive", offsets, ridge_stap)],
        ),
    }
    return _finish(
        values,
        plots,
        "A joint space-time covariance adapts across the moving-platform clutter ridge. The conventional and adaptive maps use the same range record and explicitly normalized output power.",
        "At baseline, target-like training contamination preserves the assumed unit response but increases interference output by over 20 dB. This failure is interference growth, not the target-null mechanism from P68.",
        "Disable the named failure and set contamination to zero to recompute from retained clean neighboring training cells and unchanged measurements. These normalized maps do not by themselves establish detection probability or false-alarm rate.",
        8301,
        broken,
        support_scnr_db=support_scnr,
        support_ranks=ranks,
        support_conditions=conditions,
        ridge_rd_scnr_db=ridge_rd,
        ridge_stap_scnr_db=ridge_stap,
        training_indices=(np.r_[np.arange(4, 22), np.arange(27, 45)] + 1).tolist(),
        space_time_dimension=32,
        range_record_shape=list(measured.shape),
    )
