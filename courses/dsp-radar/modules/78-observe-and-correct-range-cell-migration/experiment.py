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
    ("aperture_length_m", 400, [100, 200, 400]),
    ("squint_offset_m", 60, [0, 60, 80]),
]


def _rcm_history78(length, squint):
    full = np.arange(-200, 200.125, 0.25)
    keep = abs(full) <= length / 2
    pos = full[keep]
    axis = np.arange(955, 1075.25, 0.5)
    r = np.hypot(pos - squint, 1000)
    noise = _noise(7801, len(full), len(axis), True)[keep]
    h = (
        np.sinc((axis[None, :] - r[:, None]) / 2)
        * np.exp(1j * (0.3 - 4 * np.pi * (r[:, None] - 955) / 0.3))
        + 0.02 * noise
    )
    return pos, axis, r, h


def _shift78(h, axis, delta, sign):
    return np.array(
        [_linear_row(row, axis, axis + sign * d) for row, d in zip(h, delta)]
    )


def _image78(h, pos, axis, follow):
    x = np.arange(-40, 161, 2)
    y = np.arange(995, 1006)
    xx, yy = np.meshgrid(x, y)
    image = np.zeros(xx.shape, complex)
    fixed = np.hypot(xx, yy)
    for row, pp in zip(h, pos):
        r = np.hypot(pp - xx, yy)
        sampled = _linear_row(row, axis, r if follow else fixed)
        image += sampled * np.exp(4j * np.pi * (r - 955) / 0.3)
    return x, y, image


def run(parameters):
    length, squint, broken = _controls(parameters, CONTROLS)
    pos, axis, r, h = _rcm_history78(length, squint)
    delta = r - r[len(r) // 2]
    correct = _shift78(h, axis, delta, 1)
    active = _shift78(h, axis, delta, -1) if broken else correct
    comp = np.exp(4j * np.pi * (r - 955) / 0.3)
    fixed_profile = comp @ h
    correct_profile = comp @ correct
    active_profile = comp @ active
    raw_ridge = axis[np.argmax(abs(h), axis=1)]
    active_ridge = axis[np.argmax(abs(active), axis=1)]
    concentration = lambda p: float(np.max(abs(p) ** 2) / np.sum(abs(p) ** 2))
    x, y, good_image = _image78(h, pos, axis, True)
    _, _, fixed_image = _image78(h, pos, axis, False)
    tx = int(np.argmin(abs(x - squint)))
    ty = int(np.argmin(abs(y - 1000)))
    lengths = [100, 200, 400]
    squints = [0, 60, 80]
    spans = [
        np.ptp(np.hypot(np.arange(-v / 2, v / 2 + 0.125, 0.25) - squint, 1000))
        for v in lengths
    ]
    squintspans = [np.ptp(np.hypot(pos - v, 1000)) for v in squints]
    values = {
        "geometric_migration": (np.ptp(r), "m"),
        "measured_migration": (np.ptp(raw_ridge), "m"),
        "active_ridge_span": (np.ptp(active_ridge), "m"),
        "profile_peak_gain": (
            max(abs(active_profile)) / max(abs(fixed_profile)),
            "ratio",
        ),
        "profile_concentration_gain": (
            concentration(active_profile) / concentration(fixed_profile),
            "ratio",
        ),
        "fixed_true_pixel_ratio": (
            abs(fixed_image[ty, tx]) / abs(good_image[ty, tx]),
            "ratio",
        ),
        "corrected_ridge_span": (np.ptp(axis[np.argmax(abs(correct), axis=1)]), "m"),
        "aperture_length": (length, "m"),
        "squint_offset": (squint, "m"),
        "model_valid": (not broken, "boolean"),
    }
    plots = {
        "raw": _heat(
            "Range-cell migration before correction",
            "Slant range (m)",
            "Platform position (m)",
            axis,
            pos,
            _db(abs(h) ** 2, relative=True),
            "dB",
        ),
        "aligned": _heat(
            "Selected interpolation sign",
            "Aligned slant range (m)",
            "Platform position (m)",
            axis,
            pos,
            _db(abs(active) ** 2, relative=True),
            "dB",
        ),
        "ridge": _plot(
            "Row-peak range tracks",
            "Platform position (m)",
            "Measured peak slant range (m)",
            [("Before", pos, raw_ridge), ("Selected correction", pos, active_ridge)],
        ),
        "profiles": _plot(
            "Phase-compensated range profiles",
            "Aligned slant range (m)",
            "Magnitude (dB)",
            [
                (label, axis, _db(abs(p) ** 2 / max(abs(correct_profile)) ** 2))
                for label, p in [
                    ("Fixed bins", fixed_profile),
                    ("Correct shift", correct_profile),
                    ("Selected shift", active_profile),
                ]
            ],
        ),
        "fixed_image": _heat(
            "Fixed-bin image loses migrating energy",
            "Cross-range (m)",
            "Ground range (m)",
            x,
            y,
            _db(abs(fixed_image) ** 2 / np.max(abs(good_image) ** 2)),
            "dB relative to path-following peak",
        ),
        "image": _heat(
            "Path-following backprojection",
            "Cross-range (m)",
            "Ground range (m)",
            x,
            y,
            _db(abs(good_image) ** 2, relative=True),
            "dB",
        ),
        "aperture": _plot(
            "Migration grows with aperture",
            "Aperture length (m)",
            "Geometric range span (m)",
            [("Span", lengths, spans)],
        ),
        "squint": _plot(
            "Squint makes migration asymmetric",
            "Target cross-range (m)",
            "Geometric range span (m)",
            [("Span", squints, squintspans)],
        ),
    }
    return _finish(
        values,
        plots,
        "A target moves across fast-range cells as its slant range changes. Sampling each row at r + DeltaR aligns the envelope while preserving the phase needed for coherent focusing.",
        "The wrong-sign shift samples r - DeltaR. At the reviewed baseline it nearly doubles ridge migration and spreads the coherent profile.",
        "Disable the failure to repeat correct-sign interpolation from unchanged complex rows. Path-following image formation uses the same known geometry; it is not blind motion estimation.",
        7801,
        broken,
        aperture_spans=list(map(float, spans)),
        squint_spans=list(map(float, squintspans)),
        range_history_shape=list(h.shape),
        computed_image_shape=list(good_image.shape),
        noise_crop_from_full_aperture=True,
    )
