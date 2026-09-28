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
    ("error_rms_wavelengths", 0.125, [0, 0.03125, 0.0625, 0.125, 0.25]),
    ("random_fraction", 0.25, [0, 0.25, 0.5, 0.75, 1]),
]


def _half_uniform80(seed, count):
    return _uniform(seed, count) + 0.5 / 2147483647


def _rms_normal80(values):
    centered = values - np.mean(values)
    return centered / np.sqrt(np.mean(centered**2))


def _scene80():
    p = np.arange(-15, 15.125, 0.25)
    tx = np.array([-1, 0.35, 1.45])
    r = np.array([990, 1000, 1009])
    amp = np.array([1, 0.7, 0.5]) * np.exp(2j * np.pi * _half_uniform80(8001, 3))
    history = amp[None, :] * np.exp(
        -4j * np.pi * (np.hypot(p[:, None] - tx[None, :], r[None, :]) - 1000) / 0.03
    )
    u = _half_uniform80(8002, 726)
    normal = np.empty(726)
    rad = np.sqrt(-2 * np.log(u[::2]))
    ang = 2 * np.pi * u[1::2]
    normal[::2] = rad * np.cos(ang)
    normal[1::2] = rad * np.sin(ang)
    noise = (
        10 ** (-35 / 20)
        / np.sqrt(2)
        * (
            normal[:363].reshape(121, 3, order="F")
            + 1j * normal[363:].reshape(121, 3, order="F")
        )
    )
    t = (p - p[0]) / (p[-1] - p[0])
    smooth = _rms_normal80(
        np.sin(2 * np.pi * t + 0.3) + 0.35 * np.sin(6 * np.pi * t - 0.4)
    )
    random = _rms_normal80(
        np.convolve(
            _half_uniform80(8003, 121) - 0.5,
            np.array([1, 2, 3, 4, 3, 2, 1]) / 16,
            mode="same",
        )
    )
    return p, tx, r, history, noise, smooth, random


def _focus80(history, p, r, x):
    return np.array(
        [
            history[:, k]
            @ np.exp(4j * np.pi * (np.hypot(p[:, None] - x[None, :], rr) - 1000) / 0.03)
            / len(p)
            for k, rr in enumerate(r)
        ]
    )


def _gradient80(reference, p, tx, rr):
    deramped = reference * np.exp(4j * np.pi * (np.hypot(p - tx, rr) - 1000) / 0.03)
    increments = np.angle(deramped[1:] * deramped[:-1].conj())
    return np.r_[np.angle(deramped[0]), np.angle(deramped[0]) + np.cumsum(increments)]


def _metrics80(gates, ideal):
    power = abs(gates) ** 2
    prob = power / np.sum(power, axis=1)[:, None]
    return float(
        np.mean(np.max(abs(gates), axis=1) / np.max(abs(ideal), axis=1))
    ), float(np.mean(-np.sum(prob * np.log(np.maximum(prob, 1e-300)), axis=1)))


def _compose80(gates, y):
    frequencies = np.linspace(-1e8, 1e8, 129)
    responses = np.array(
        [
            np.mean(
                np.exp(4j * np.pi * frequencies[:, None] * (y - off)[None, :] / 3e8),
                axis=0,
            )
            for off in [-10, 0, 9]
        ]
    )
    return responses.T @ gates


def run(parameters):
    fraction, mix, broken = _controls(parameters, CONTROLS)
    p, tx, r, signal, noise, smooth, random = _scene80()
    x = np.linspace(-4, 4, 401)
    y = np.linspace(-15, 15, 81)
    template = _rms_normal80((1 - mix) * smooth + mix * random)
    phase = -4 * np.pi * fraction * template
    measured = signal * np.exp(1j * phase[:, None]) + noise
    ideal = _focus80(signal + noise, p, r, x)
    blurred = _focus80(measured, p, r, x)
    clean_est = _gradient80(measured[:, 0], p, tx[0], r[0])
    ref = measured[:, 0] + 0.95 * measured[:, 1] if broken else measured[:, 0]
    estimate = _gradient80(ref, p, tx[0], r[0])
    active = _focus80(measured * np.exp(-1j * estimate[:, None]), p, r, x)
    corrected = _focus80(measured * np.exp(-1j * clean_est[:, None]), p, r, x)
    peak, entropy = _metrics80(active, ideal)
    blur_peak, blur_entropy = _metrics80(blurred, ideal)
    good_peak, _ = _metrics80(corrected, ideal)
    residual = estimate - phase
    phase_rmse = np.sqrt(np.mean((residual - np.mean(residual)) ** 2))
    fractions = [0, 0.03125, 0.0625, 0.125, 0.25]
    mixes = [0, 0.25, 0.5, 0.75, 1]

    def sweep(fr, mi):
        ph = -4 * np.pi * fr * _rms_normal80((1 - mi) * smooth + mi * random)
        h = signal * np.exp(1j * ph[:, None]) + noise
        est = _gradient80(h[:, 0], p, tx[0], r[0])
        before = _focus80(h, p, r, x)
        after = _focus80(h * np.exp(-1j * est[:, None]), p, r, x)
        return _metrics80(before, ideal)[0], _metrics80(after, ideal)[0]

    fs = np.array([sweep(v, mix) for v in fractions])
    ms = np.array([sweep(fraction, v) for v in mixes])
    image = _compose80(active, y)
    values = {
        "path_error_rms": (fraction * 0.03 * 1000, "mm"),
        "phase_error_rms": (np.sqrt(np.mean(phase**2)), "rad"),
        "active_peak_retention": (peak, "ratio"),
        "blurred_peak_retention": (blur_peak, "ratio"),
        "recovered_peak_retention": (good_peak, "ratio"),
        "active_entropy": (entropy, "nat"),
        "blurred_entropy": (blur_entropy, "nat"),
        "centered_phase_rmse": (phase_rmse, "rad"),
        "mean_half_power_width": (
            np.mean([_amplitude_width(x, abs(a)) for a in active]),
            "m",
        ),
        "random_fraction": (mix, "ratio"),
        "model_valid": (not broken, "boolean"),
    }
    plots = {
        "screen": _plot(
            "Phase-gradient estimate after known-path deramping",
            "Platform position (m)",
            "Centered phase (rad)",
            [
                ("Injected", p, phase - np.mean(phase)),
                ("Estimated", p, estimate - np.mean(estimate)),
            ],
        ),
        "cut": _plot(
            "Reference-gate focus on a common ideal scale",
            "Cross-range (m)",
            "Magnitude (dB)",
            [
                (label, x, _db(abs(g[0]) ** 2 / max(abs(ideal[0])) ** 2))
                for label, g in [
                    ("Ideal", ideal),
                    ("Blurred", blurred),
                    ("Isolated-gate recovery", corrected),
                    ("Selected reference", active),
                ]
            ],
        ),
        "image": _heat(
            "Autofocused isolated-gate scene",
            "Cross-range (m)",
            "Range offset (m)",
            x,
            y,
            _db(abs(image) ** 2, relative=True),
            "dB",
        ),
        "error_sweep": _plot(
            "RMS path error controls phase loss",
            "Path RMS / wavelength (ratio)",
            "Mean peak retention (ratio)",
            [("Blurred", fractions, fs[:, 0]), ("Corrected", fractions, fs[:, 1])],
        ),
        "mixture_sweep": _plot(
            "Error correlation changes the blur",
            "Short-correlated mixture (ratio)",
            "Mean peak retention (ratio)",
            [("Blurred", mixes, ms[:, 0]), ("Corrected", mixes, ms[:, 1])],
        ),
    }
    return _finish(
        values,
        plots,
        "A few millimeters of nonlinear path error creates order-one two-way phase error. Deramp an isolated strong range gate, integrate adjacent phase differences, and remove the common phase screen before focusing.",
        "The named failure mixes 0.95 of a second range gate into the reference. Its different geometric phase contaminates the estimated common error and lowers recovered focus.",
        "Disable the mixed-reference failure and re-estimate from the unchanged isolated first gate. Absolute phase is unobservable here; compare centered phase and retain the known-geometry and isolated-gate assumptions.",
        8001,
        broken,
        error_sweep=fs.tolist(),
        mixture_sweep=ms.tolist(),
        phase_increment_max=float(np.max(abs(np.diff(phase)))),
        computed_image_shape=list(image.shape),
        known_isolated_reference_gate=True,
    )
