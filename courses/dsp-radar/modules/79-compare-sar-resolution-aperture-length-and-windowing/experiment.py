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
    ("bandwidth_mhz", 200, [100, 200, 400]),
    ("aperture_length_m", 30, [10, 20, 30]),
]


def _range_psf79(offset, bandwidth):
    frequencies = np.linspace(-bandwidth / 2, bandwidth / 2, 257)
    return np.mean(
        np.exp(4j * np.pi * frequencies[:, None] * np.asarray(offset)[None, :] / 3e8),
        axis=0,
    )


def _aperture_psf79(axis, target_x, target_r, positions, weights):
    residual = (
        np.hypot(positions[:, None] - np.asarray(axis)[None, :], target_r)
        - np.hypot(positions - target_x, target_r)[:, None]
    )
    return weights @ np.exp(4j * np.pi * residual / 0.03) / sum(weights)


def _psf_metrics79(axis, response):
    a = abs(response)
    a = a / max(a)
    peak = int(np.argmax(a))
    minima = np.flatnonzero((a[1:-1] <= a[:-2]) & (a[1:-1] < a[2:])) + 1
    left = minima[minima < peak][-1]
    right = minima[minima > peak][0]
    return _amplitude_width(axis, a), 20 * np.log10(
        max(np.r_[a[: left + 1], a[right:]])
    )


def _scene79(bandwidth, length, spacing):
    x = np.arange(-5, 5.025, 0.05)
    y = np.arange(-2, 2.025, 0.05)
    pos = np.arange(-length / 2, length / 2 + spacing / 2, spacing)
    phase = 2 * np.pi * (_uniform(7901, 3) + 0.5 / 2147483647)
    amp = np.array([1, 0.65, 0.55]) * np.exp(1j * phase)
    image = np.zeros((len(y), len(x)), complex)
    for xx, rr, a in zip([0, 0.8, 0], [0, 0, 1.2], amp):
        image += a * np.outer(
            _range_psf79(y - rr, bandwidth),
            _aperture_psf79(x, xx, 1000 + rr, pos, np.ones(len(pos))),
        )
    return x, y, image


def run(parameters):
    mhz, length, broken = _controls(parameters, CONTROLS)
    bandwidth = mhz * 1e6
    ra = np.linspace(-6, 6, 2401)
    xa = np.linspace(-8, 8, 3201)
    dense = np.arange(-length / 2, length / 2 + 0.125, 0.25)
    activepos = np.arange(-length / 2, length / 2 + 2.5, 5) if broken else dense
    range_response = _range_psf79(ra, bandwidth)
    rect = _aperture_psf79(xa, 0, 1000, dense, np.ones(len(dense)))
    active = _aperture_psf79(xa, 0, 1000, activepos, np.ones(len(activepos)))
    hamming = _aperture_psf79(xa, 0, 1000, dense, np.hamming(len(dense)))
    rw, rsl = _psf_metrics79(ra, range_response)
    cw, csl = _psf_metrics79(xa, active)
    hw, hsl = _psf_metrics79(xa, hamming)
    bandwidths = [100, 200, 400]
    lengths = [10, 20, 30]
    spacings = [0.25, 1, 5]
    rwidth = [_psf_metrics79(ra, _range_psf79(ra, b * 1e6))[0] for b in bandwidths]
    cwidth = []
    aliases = []
    for ell in lengths:
        p = np.arange(-ell / 2, ell / 2 + 0.125, 0.25)
        cwidth.append(
            _psf_metrics79(xa, _aperture_psf79(xa, 0, 1000, p, np.ones(len(p))))[0]
        )
    for spacing in spacings:
        p = np.arange(-length / 2, length / 2 + spacing / 2, spacing)
        v = _aperture_psf79(xa, 0, 1000, p, np.ones(len(p)))
        aliases.append(max(abs(v[abs(xa) > 1.5])))
    x, y, image = _scene79(bandwidth, length, 5 if broken else 0.25)
    values = {
        "range_half_power_width": (rw, "m"),
        "cross_range_half_power_width": (cw, "m"),
        "range_peak_sidelobe": (rsl, "dB"),
        "cross_range_peak_sidelobe": (csl, "dB"),
        "hamming_half_power_width": (hw, "m"),
        "hamming_peak_sidelobe": (hsl, "dB"),
        "far_cross_range_peak": (max(abs(active[abs(xa) > 1.5])), "ratio"),
        "aperture_samples": (len(activepos), "count"),
        "nominal_range_resolution": (3e8 / (2 * bandwidth), "m"),
        "nominal_cross_range_resolution": (0.03 * 1000 / (2 * length), "m"),
        "model_valid": (not broken, "boolean"),
    }
    plots = {
        "range": _plot(
            "Finite-bandwidth coherent point response",
            "Range offset (m)",
            "Magnitude (dB)",
            [("Uniform frequency samples", ra, _db(abs(range_response) ** 2))],
        ),
        "cross": _plot(
            "Dense, tapered and selected aperture responses",
            "Cross-range offset (m)",
            "Magnitude (dB)",
            [
                (label, xa, _db(abs(v) ** 2))
                for label, v in [
                    ("Dense uniform", rect),
                    ("Dense Hamming", hamming),
                    ("Selected sampling", active),
                ]
            ],
        ),
        "bandwidth": _plot(
            "Bandwidth controls range width",
            "Bandwidth (MHz)",
            "Half-power width (m)",
            [("Measured", bandwidths, rwidth)],
        ),
        "aperture": _plot(
            "Aperture controls cross-range width",
            "Aperture length (m)",
            "Half-power width (m)",
            [("Measured", lengths, cwidth)],
        ),
        "sampling": _plot(
            "Sparse aperture creates false copies",
            "Platform spacing (m)",
            "Far-region peak voltage (ratio)",
            [("Outside +/-1.5 m", spacings, aliases)],
        ),
        "image": _heat(
            "Three-target separable narrow-scene image",
            "Cross-range (m)",
            "Range offset (m)",
            x,
            y,
            _db(abs(image) ** 2, relative=True),
            "dB",
        ),
    }
    return _finish(
        values,
        plots,
        "Frequency sums set range resolution; phase-coherent aperture sums set cross-range resolution. Hamming weighting lowers sidelobes at the cost of a wider mainlobe.",
        "The named 5 m platform spacing undersamples aperture phase, creating near-unity cross-range copies about 3 m apart. A narrow mainlobe alone does not establish unambiguous localization.",
        "Disable the failure to recompute the same seeded scene with dense 0.25 m aperture sampling. This is reacquisition with a reviewed sampling grid, not recovery of missing information from the sparse image.",
        7901,
        broken,
        bandwidth_widths=rwidth,
        aperture_widths=cwidth,
        spacing_far_peaks=list(map(float, aliases)),
        predicted_sparse_alias_spacing_m=3.0,
        computed_image_shape=list(image.shape),
        model_is_separable_narrow_scene=True,
    )
