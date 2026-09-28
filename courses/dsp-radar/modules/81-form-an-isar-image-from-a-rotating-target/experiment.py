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
    ("angular_aperture_deg", 6, [2, 4, 6, 8]),
    ("rotation_rate_deg_s", 6, [3, 6, 12]),
]
_TARGET_X81 = np.array([0, 0, 0, 0, -2, -1, 1, 2, -0.75, 0.75])
_TARGET_Y81 = np.array([-1.5, -0.5, 0.5, 1.5, 0, 0, 0, 0, -1.25, -1.25])


def _isar_record81(aperture, rate):
    theta = np.deg2rad(np.linspace(-aperture / 2, aperture / 2, 65))
    t = theta / np.deg2rad(rate)
    freq = 1e10 + np.linspace(-3e8, 3e8, 129)
    translation = 2 * t
    amp = np.array([1, 0.75, 0.85, 0.9, 0.8, 0.65, 0.65, 0.8, 0.55, 0.55]) * np.exp(
        2j * np.pi * _uniform(8101, 10)
    )
    raw = np.zeros((65, 129), complex)
    for x, y, a in zip(_TARGET_X81, _TARGET_Y81, amp):
        distance = translation + x * np.sin(theta) + y * np.cos(theta)
        raw += a * np.exp(-4j * np.pi * distance[:, None] * freq[None, :] / 3e8)
    aligned = raw * np.exp(4j * np.pi * translation[:, None] * freq[None, :] / 3e8)
    return theta, t, raw, aligned


def _isar_focus81(history, theta):
    profiles = np.fft.fftshift(
        np.fft.ifft(np.fft.ifftshift(history, axes=1), axis=1), axes=1
    )
    spectrum = (
        np.fft.fftshift(np.fft.fft(np.fft.ifftshift(profiles, axes=0), axis=0), axes=0)
        / 65
    )
    ranges = np.arange(-64, 65) * 3e8 / (2 * 129 * (6e8 / 128))
    x = (-0.03 * np.arange(-32, 33) / (2 * 65 * (theta[1] - theta[0])))[::-1]
    return ranges, x, profiles, spectrum[::-1].T


def _capture81(image, ranges, x):
    mask = np.zeros(image.shape, bool)
    for tx, ty in zip(_TARGET_X81, _TARGET_Y81):
        i = int(np.argmin(abs(ranges - ty)))
        j = int(np.argmin(abs(x - tx)))
        mask[max(0, i - 1) : i + 2, max(0, j - 1) : j + 2] = True
    power = abs(image) ** 2
    return float(sum(power[mask]) / sum(power.ravel())), float(
        max(power[mask]) / np.median(power[~mask])
    )


def run(parameters):
    aperture, rate, broken = _controls(parameters, CONTROLS)
    theta, _t, raw, aligned = _isar_record81(aperture, rate)
    ranges, x, raw_profiles, raw_image = _isar_focus81(raw, theta)
    _, _, profiles, good_image = _isar_focus81(aligned, theta)
    active = raw_image if broken else good_image
    capture, contrast = _capture81(active, ranges, x)
    aa = abs(active).ravel()
    bb = abs(good_image).ravel()
    aa = aa - aa.mean()
    bb = bb - bb.mean()
    correlation = np.dot(aa, bb) / (np.linalg.norm(aa) * np.linalg.norm(bb))
    angles = [2, 4, 6, 8]
    rates = [3, 6, 12]
    caps = []
    rate_corr = []
    for angle in angles:
        th, _, _, h = _isar_record81(angle, rate)
        rr, xx, _, im = _isar_focus81(h, th)
        caps.append(_capture81(im, rr, xx)[0])
    for speed in rates:
        th, _, _, h = _isar_record81(aperture, speed)
        _, _, _, im = _isar_focus81(h, th)
        rate_corr.append(float(np.max(abs(abs(im) - abs(good_image)))))
    values = {
        "truth_neighborhood_capture": (capture, "ratio"),
        "truth_background_peak_db": (10 * np.log10(contrast), "dB"),
        "aligned_image_correlation": (correlation, "ratio"),
        "coherent_processing_interval": (aperture / rate, "s"),
        "translation_drift": (2 * aperture / rate, "m"),
        "nominal_range_resolution": (0.25, "m"),
        "nominal_cross_range_resolution": (0.03 / (2 * np.deg2rad(aperture)), "m"),
        "image_peak_voltage": (np.max(abs(active)), "V"),
        "rotation_rate": (rate, "deg/s"),
        "model_valid": (not broken, "boolean"),
    }
    plots = {
        "geometry": _plot(
            "Seeded rigid-target scatterers",
            "Cross-range (m)",
            "Down-range (m)",
            [("Scatterers", _TARGET_X81, _TARGET_Y81)],
        ),
        "raw_profiles": _heat(
            "Range IFFT before translation alignment",
            "Down-range (m)",
            "Aspect angle (deg)",
            ranges,
            np.rad2deg(theta),
            _db(abs(raw_profiles) ** 2, relative=True),
            "dB",
        ),
        "aligned_profiles": _heat(
            "Envelope and phase aligned together",
            "Down-range (m)",
            "Aspect angle (deg)",
            ranges,
            np.rad2deg(theta),
            _db(abs(profiles) ** 2, relative=True),
            "dB",
        ),
        "image": _heat(
            "Selected angle-domain ISAR image",
            "Cross-range (m)",
            "Down-range (m)",
            x,
            ranges,
            _db(abs(active) ** 2 / np.max(abs(good_image) ** 2)),
            "dB relative to aligned peak",
        ),
        "aperture": _plot(
            "Angular span determines cross-range resolution",
            "Angular aperture (deg)",
            "Nominal cross-range resolution (m)",
            [("lambda / (2 Delta theta)", angles, 0.03 / (2 * np.deg2rad(angles)))],
        ),
        "rate": _plot(
            "Rotation rate changes time support",
            "Rotation rate (deg/s)",
            "Coherent processing interval (s)",
            [("Same angular aperture", rates, aperture / np.array(rates))],
        ),
    }
    plots["geometry"]["data"][0]["mode"] = "markers"
    return _finish(
        values,
        plots,
        "Target rotation projects scatterers onto changing range directions. Range compression precedes the signed angle FFT; translation correction removes both envelope migration and carrier phase.",
        "Omitting the known centroid translation correction spreads energy and shifts the apparent shape. A faster rotation alone cannot replace alignment.",
        "Disable the failure and multiply the original frequency history by the opposite translational phase. The small-angle cross-range approximation and uniform aspect sampling remain explicit assumptions.",
        8101,
        broken,
        aperture_truth_capture=caps,
        rate_image_max_magnitude_differences=rate_corr,
        computed_image_shape=list(active.shape),
        cross_range_axis_m=x.tolist(),
        range_axis_m=ranges.tolist(),
        truth_used_for_scoring_only=True,
    )
