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
    ("target_delay_samples", 24, [12, 24, 48]),
    ("reference_quality_db", 35, [35, 15, 5]),
]


def _qpsk82(seed, count):
    u = _uniform(seed, 2 * count)
    z = ((2 * (u[::2] >= 0.5) - 1) + 1j * (2 * (u[1::2] >= 0.5) - 1)) / np.sqrt(2)
    z -= np.mean(z)
    return z / np.sqrt(np.mean(abs(z) ** 2))


def _delay82(signal, delay):
    return (
        np.r_[np.zeros(delay, complex), signal[: len(signal) - delay]]
        if delay
        else signal.copy()
    )


def _channels82(delay, doppler, quality):
    impulses = np.zeros(4096, complex)
    impulses[::4] = _qpsk82(8201, 1024)
    k = np.arange(-12, 13)
    pulse = np.sinc(k / 4) * (0.5 + 0.5 * np.cos(np.pi * k / 12))
    pulse /= np.linalg.norm(pulse)
    clean = np.convolve(impulses, pulse, "same")
    clean /= np.sqrt(np.mean(abs(clean) ** 2))
    reference = clean + 10 ** (-quality / 20) * _qpsk82(8202, 4096)
    reference /= np.sqrt(np.mean(abs(reference) ** 2))
    time = np.arange(4096) / 200000
    surveillance = (
        2.5 * clean
        + 0.1 * _delay82(clean, 11)
        + 0.18 * _delay82(clean, delay) * np.exp(2j * np.pi * doppler * time)
        + 0.08 * _qpsk82(8203, 4096)
    )
    return reference, surveillance


def _cancel82(reference, surveillance, fraction=1):
    coefficient = np.vdot(reference, surveillance) / np.vdot(reference, reference)
    return surveillance - fraction * coefficient * reference, coefficient


def _caf82(reference, surveillance):
    n = len(reference)
    t = np.arange(n) / 200000
    doppler = np.arange(-1000, 1001, 50)
    delayed = np.array([_delay82(reference, k) for k in range(65)])
    products = surveillance[None, :] * delayed.conj()
    coherent = np.exp(-2j * np.pi * doppler[:, None] * t[None, :]) @ products.T
    reference_energy = np.sum(abs(delayed) ** 2, axis=1)
    coherence = abs(coherent) / np.sqrt(
        np.sum(abs(surveillance) ** 2) * reference_energy[None, :]
    )
    return coherence, abs(coherent) / reference_energy[None, :]


def _caf_metrics82(ambiguity, delay, doppler):
    i = int((doppler + 1000) // 50)
    mask = np.ones(ambiguity.shape, bool)
    mask[max(0, i - 1) : i + 2, max(0, delay - 2) : delay + 3] = False
    peak = np.unravel_index(np.argmax(ambiguity), ambiguity.shape)
    return [
        float(peak[1]),
        float(-1000 + 50 * peak[0]),
        float(ambiguity[i, delay]),
        float(20 * np.log10(ambiguity[i, delay] / np.median(ambiguity[mask]))),
        float(ambiguity[20, 0]),
    ]


def run(parameters):
    delay, quality, broken = _controls(parameters, CONTROLS)
    delay = int(delay)
    ref, surveillance = _channels82(delay, 500, quality)
    cleaned, coefficient = _cancel82(ref, surveillance)
    active, _ = _cancel82(ref, surveillance, 0.2 if broken else 1)
    raw_caf, raw_voltage = _caf82(ref, surveillance)
    good_caf, good_voltage = _caf82(ref, cleaned)
    active_caf, active_voltage = (
        _caf82(ref, active) if broken else (good_caf, good_voltage)
    )
    peak_delay, peak_doppler, target, contrast, origin = _caf_metrics82(
        active_caf, delay, 500
    )
    delays = [12, 24, 48]
    dopplers = [-500, 0, 500]
    counts = [1024, 2048, 4096]
    qualities = [35, 15, 5]
    delay_peaks = []
    doppler_peaks = []
    integration = []
    qualities_contrast = []
    for d in delays:
        r, s = _channels82(d, 500, quality)
        c, _ = _cancel82(r, s)
        a, _ = _caf82(r, c)
        delay_peaks.append(_caf_metrics82(a, d, 500)[0])
    for fd in dopplers:
        r, s = _channels82(delay, fd, quality)
        c, _ = _cancel82(r, s)
        a, _ = _caf82(r, c)
        doppler_peaks.append(_caf_metrics82(a, delay, fd)[1])
    for count in counts:
        r, s = ref[:count], surveillance[:count]
        c, _ = _cancel82(r, s)
        a, _ = _caf82(r, c)
        integration.append(_caf_metrics82(a, delay, 500)[3])
    for q in qualities:
        r, s = _channels82(delay, 500, q)
        c, _ = _cancel82(r, s)
        a, _ = _caf82(r, c)
        qualities_contrast.append(_caf_metrics82(a, delay, 500)[3])
    values = {
        "peak_delay": (peak_delay, "samples"),
        "peak_doppler": (peak_doppler, "Hz"),
        "peak_excess_path": (1500 * peak_delay / 1000, "km"),
        "target_coherence": (target, "ratio"),
        "target_contrast": (contrast, "dB"),
        "origin_coherence": (origin, "ratio"),
        "cancellation_coefficient_magnitude": (abs(coefficient), "ratio"),
        "residual_rms": (np.sqrt(np.mean(abs(active) ** 2)), "V"),
        "reference_quality": (quality, "dB"),
        "model_valid": (not broken, "boolean"),
    }
    axis = np.arange(65) * 1.5
    fd = np.arange(-1000, 1001, 50)
    scale = np.max(raw_voltage) ** 2
    plots = {
        "channels": _plot(
            "Reference and surveillance channels",
            "Time (ms)",
            "Magnitude (V)",
            [
                ("Reference", np.arange(320) / 200, abs(ref[:320])),
                ("Surveillance", np.arange(320) / 200, abs(surveillance[:320])),
            ],
        ),
        "raw": _heat(
            "Before direct-path cancellation",
            "Bistatic excess path (km)",
            "Doppler (Hz)",
            axis,
            fd,
            _db(raw_voltage**2 / scale),
            "dB on common matched-voltage scale",
        ),
        "active": _heat(
            "Selected cancellation before cross-ambiguity",
            "Bistatic excess path (km)",
            "Doppler (Hz)",
            axis,
            fd,
            _db(active_voltage**2 / scale),
            "dB on common matched-voltage scale",
        ),
        "recovery": _heat(
            "Full-cancellation comparison",
            "Bistatic excess path (km)",
            "Doppler (Hz)",
            axis,
            fd,
            _db(good_voltage**2 / scale),
            "dB on common matched-voltage scale",
        ),
        "delay": _plot(
            "Delay sweep moves the path coordinate",
            "True delay (samples)",
            "Global peak delay (samples)",
            [("Measured", delays, delay_peaks)],
        ),
        "doppler": _plot(
            "Doppler sweep moves the frequency coordinate",
            "True Doppler (Hz)",
            "Global peak Doppler (Hz)",
            [("Measured", dopplers, doppler_peaks)],
        ),
        "integration": _plot(
            "Longer coherent records improve contrast",
            "Integration samples (count)",
            "Target / median background (dB)",
            [("Measured", counts, integration)],
        ),
        "quality": _plot(
            "Reference quality limits cancellation",
            "Reference quality (dB)",
            "Target / median background (dB)",
            [("Measured", qualities, qualities_contrast)],
        ),
    }
    return _finish(
        values,
        plots,
        "Cross-ambiguity multiplies surveillance by a conjugate delayed reference and a negative trial Doppler phasor before coherent summation. Least-squares direct-path cancellation reveals the delayed target.",
        "Cancelling only 20 percent of the estimated direct term leaves the origin dominant. Poor reference quality also limits cancellation and coherent matching.",
        "Disable the failure to subtract the full estimated coefficient from the unchanged measured channels. Delay measures bistatic excess path c tau; geometry is still needed for target position.",
        8201,
        broken,
        delay_peak_samples=delay_peaks,
        doppler_peak_hz=doppler_peaks,
        integration_contrast_db=integration,
        quality_contrast_db=qualities_contrast,
        raw_peak_delay=float(np.unravel_index(np.argmax(raw_caf), raw_caf.shape)[1]),
        orthogonality_residual=float(
            abs(np.vdot(ref, cleaned)) / np.vdot(ref, ref).real
        ),
        caf_shape=list(active_caf.shape),
    )
