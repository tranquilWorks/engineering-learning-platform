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
    ("aperture_looks", 121, [21, 61, 121]),
    ("path_error_m", 0, [0, 0.005, 0.01]),
]


def _history77():
    pos = np.arange(-15, 15.125, 0.25)
    axis = np.arange(990, 1035.25, 0.5)
    ranges = np.hypot(pos[:, None] - [-6, 7], [1002, 1020])
    phase = np.array([0, 0.7]) - 4 * np.pi * (ranges - 990) / 0.06
    h = sum(
        a
        * np.sinc((axis[None, :] - ranges[:, k, None]) / 2.5)
        * np.exp(1j * phase[:, k, None])
        for k, a in enumerate([1, 0.75])
    )
    return pos, axis, h + 0.015 * _noise(7701, len(pos), len(axis), True), ranges, phase


def _backproject77(history, pos, axis, x, y, indices, error):
    xx, yy = np.meshgrid(x, y)
    image = np.zeros(xx.shape, complex)
    for i in indices:
        r = np.hypot(pos[i] - xx, yy + error[i])
        image += _linear_row(history[i], axis, r) * np.exp(
            4j * np.pi * (r - 990) / 0.06
        )
    return image


def run(parameters):
    looks, error, broken = _controls(parameters, CONTROLS)
    looks = int(looks)
    pos, axis, h, ranges, phase = _history77()
    start = (121 - looks) // 2
    ix = np.arange(start, start + looks)
    x = np.arange(-15, 15.125, 0.25)
    y = np.arange(995, 1027.25, 0.5)
    profile = np.sin(2 * np.pi * np.arange(121) / 120)
    error = 0.01 if broken else error
    clean = _backproject77(h, pos, axis, x, y, ix, np.zeros(121))
    active = _backproject77(h, pos, axis, x, y, ix, error * profile) if error else clean
    tx = int(np.argmin(abs(x + 6)))
    ty = int(np.argmin(abs(y - 1002)))
    terms = []
    ridge = []
    for i in ix:
        r = np.hypot(pos[i] + 6, 1002 + error * profile[i])
        terms.append(_linear_row(h[i], axis, r) * np.exp(4j * np.pi * (r - 990) / 0.06))
        ridge.append(_linear_row(h[i], axis, ranges[i, 0]))
    terms = np.array(terms)
    ridge = np.array(ridge)
    widths = []
    gains = []
    for count in [21, 61, 121]:
        ids = np.arange((121 - count) // 2, (121 + count) // 2)
        cut = _backproject77(h, pos, axis, x, [1002], ids, np.zeros(121))[0]
        widths.append(_amplitude_width(x, abs(cut)))
        gains.append(abs(cut[tx]))
    path_gains = []
    for e in [0, 0.005, 0.01]:
        v = _backproject77(h, pos, axis, [-6], [1002], ix, e * profile)[0, 0]
        path_gains.append(abs(v) / abs(clean[ty, tx]))
    errors = []
    for xt, yt in [(-6, 1002), (7, 1020)]:
        mask = (abs(x[None, :] - xt) <= 3) & (abs(y[:, None] - yt) <= 4)
        iy, iz = np.unravel_index(
            np.argmax(np.where(mask, abs(active), -1)), active.shape
        )
        errors.append([abs(x[iz] - xt), abs(y[iy] - yt)])
    values = {
        "active_true_voltage": (abs(active[ty, tx]), "V"),
        "clean_true_voltage": (abs(clean[ty, tx]), "V"),
        "phase_coherence": (abs(sum(terms)) / sum(abs(terms)), "ratio"),
        "cross_range_width": (_amplitude_width(x, abs(active[ty])), "m"),
        "input_phase_coherence": (
            abs(np.mean(ridge / abs(ridge) * np.exp(-1j * phase[ix, 0]))),
            "ratio",
        ),
        "max_x_error": (np.max(np.array(errors)[:, 0]), "m"),
        "max_y_error": (np.max(np.array(errors)[:, 1]), "m"),
        "path_error": (error, "m"),
        "aperture_looks": (looks, "count"),
        "model_valid": (not broken, "boolean"),
    }
    plots = {
        "history": _heat(
            "Complex range-compressed input magnitude",
            "Slant range (m)",
            "Platform position (m)",
            axis,
            pos,
            _db(abs(h) ** 2, relative=True),
            "dB",
        ),
        "phase": _plot(
            "Measured and expected target-1 ridge phase",
            "Platform position (m)",
            "Relative phase (rad)",
            [
                ("Measured", pos[ix], np.unwrap(np.angle(ridge)) - np.angle(ridge[0])),
                ("Modeled", pos[ix], phase[ix, 0] - phase[ix[0], 0]),
            ],
        ),
        "image": _heat(
            "Backprojection with selected assumed path",
            "Cross-range (m)",
            "Ground range (m)",
            x,
            y,
            _db(abs(active) ** 2 / np.max(abs(clean) ** 2)),
            "dB relative to correct focus",
        ),
        "cuts": _plot(
            "Target-1 cross-range cut on a common scale",
            "Cross-range (m)",
            "Magnitude (dB)",
            [
                (
                    "Correct path",
                    x,
                    _db(abs(clean[ty]) ** 2 / np.max(abs(clean[ty]) ** 2)),
                ),
                (
                    "Selected path",
                    x,
                    _db(abs(active[ty]) ** 2 / np.max(abs(clean[ty]) ** 2)),
                ),
            ],
        ),
        "looks": _plot(
            "More centered looks narrow the point response",
            "Aperture looks (count)",
            "Half-power width (m)",
            [("Measured width", [21, 61, 121], widths)],
        ),
        "path": _plot(
            "Millimeter path error destroys coherent gain",
            "Assumed path error (mm)",
            "True-pixel voltage ratio (ratio)",
            [("Same input", [0, 5, 10], path_gains)],
        ),
    }
    return _finish(
        values,
        plots,
        "For each image pixel, predict slant range, interpolate the complex range row, cancel its two-way phase, and sum aperture looks. More coherent looks narrow the cross-range response.",
        "The named failure assumes a sinusoidal 10 mm ground-range path error. Misaligned phasors reduce the true-pixel gain despite unchanged measurements.",
        "Disable the failure and restore path error to 0 m; refocus the retained complex input with correct geometry.",
        7701,
        broken,
        partial_widths=widths,
        partial_voltages=gains,
        path_gain_ratios=path_gains,
        localization_errors=errors,
        computed_image_shape=list(active.shape),
        pixel_look_count=int(active.size * looks),
    )
