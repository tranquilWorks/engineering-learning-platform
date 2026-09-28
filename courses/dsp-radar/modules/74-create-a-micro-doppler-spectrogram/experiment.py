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
    ("swing_speed_mps", 2, [1, 2, 3]),
    ("window_samples", 512, [192, 512, 1536]),
]


def _return(speed, carrier=24e9, seed=7401):
    t = np.arange(19200) / 4800
    angle = 2 * np.pi * 1.5 * t
    advance = np.array(
        [
            1.2 * t,
            1.2 * t + speed / (3 * np.pi) * np.sin(angle),
            1.2 * t + speed / (3 * np.pi) * np.sin(angle + np.pi),
        ]
    )
    phase = -4 * np.pi * advance / (3e8 / carrier) + np.array([0, 0.7, -0.9])[:, None]
    x = np.sum(np.array([1, 0.35, 0.28])[:, None] * np.exp(1j * phase), axis=0)
    return (
        x
        + np.sqrt(1 + 0.35**2 + 0.28**2)
        * 10 ** (-25 / 20)
        * _noise(seed, 1, 19200, True)[0]
    )


def _stft(x, window):
    hop = window // 4
    starts = np.arange(0, len(x) - window + 1, hop)
    ix = starts[:, None] + np.arange(window)
    z = np.fft.fftshift(
        np.fft.fft(x[ix] * np.hanning(window), 2048, axis=1), axes=1
    ).T / sum(np.hanning(window))
    frequencies = -np.fft.fftshift(np.fft.fftfreq(2048, 1 / 4800))[::-1]
    return z[::-1], (starts + (window - 1) / 2) / 4800, frequencies


def _dominant(z, f):
    return f[np.argmax(np.sum(abs(z) ** 2, axis=1))]


def run(parameters):
    speed, window, broken = _controls(parameters, CONTROLS)
    window = int(window)
    x = _return(speed)
    z, t, f = _stft(abs(x) if broken else x, window)
    good, _, _ = _stft(x, window)
    bad, _, _ = _stft(abs(x), window)
    speeds = np.array([1, 2, 3])
    carriers = np.array([10, 24, 77])
    wins = np.array([192, 512, 1536])
    speed_specs = [_stft(_return(v, seed=7501), 512)[0] for v in speeds]
    carrier_specs = [_stft(_return(speed, fc * 1e9, 7601), 512)[0] for fc in carriers]
    win_specs = [_stft(x, int(w))[0] for w in wins]
    values = {
        "bulk_doppler": (2 * 1.2 / 0.0125, "Hz"),
        "limb_low": (2 * (1.2 - speed) / 0.0125, "Hz"),
        "limb_high": (2 * (1.2 + speed) / 0.0125, "Hz"),
        "active_dominant_doppler": (_dominant(z, f), "Hz"),
        "complex_dominant_doppler": (_dominant(good, f), "Hz"),
        "magnitude_dominant_doppler": (_dominant(bad, f), "Hz"),
        "frame_count": (len(t), "count"),
        "window_duration": (1000 * window / 4800, "ms"),
        "native_frequency_scale": (4800 / window, "Hz"),
        "first_frame_time": (t[0], "s"),
        "active_frame_energy": (np.sum(abs(z[:, 0]) ** 2), "voltage²"),
        "model_valid": (not broken, "boolean"),
    }
    keep = abs(f) < 1900
    st = np.arange(19200) / 4800
    plots = {
        "velocity": _plot(
            "Three physical scatterer velocities",
            "Time (s)",
            "Approaching velocity (m/s)",
            [
                ("Torso", st, np.full(len(st), 1.2)),
                ("Limb A", st, 1.2 + speed * np.cos(3 * np.pi * st)),
                ("Limb B", st, 1.2 - speed * np.cos(3 * np.pi * st)),
            ],
        ),
        "spectrogram": _heat(
            "Selected coherent slow-time spectrogram",
            "Frame center time (s)",
            "Approaching Doppler (Hz)",
            t,
            f[keep],
            _db(abs(z[keep]) ** 2, -55, True),
            "dB",
        ),
        "recovery": _heat(
            "Original complex-IQ spectrogram",
            "Frame center time (s)",
            "Approaching Doppler (Hz)",
            t,
            f[keep],
            _db(abs(good[keep]) ** 2, -55, True),
            "dB",
        ),
        "speed": _plot(
            "Swing speed changes sideband extent",
            "Approaching Doppler (Hz)",
            "Integrated spectral power (dB)",
            [
                (
                    f"{s:g} m/s",
                    f[keep],
                    _db(np.sum(abs(v[keep]) ** 2, axis=1), -55, True),
                )
                for s, v in zip(speeds, speed_specs)
            ],
        ),
        "carrier": _plot(
            "Same physical speeds at different carriers",
            "Approaching Doppler (Hz)",
            "Integrated spectral power (dB)",
            [
                (
                    f"{fc:g} GHz",
                    f[keep],
                    _db(np.sum(abs(v[keep]) ** 2, axis=1), -55, True),
                )
                for fc, v in zip(carriers, carrier_specs)
            ],
        ),
        "window": _plot(
            "Same record and different Hann durations",
            "Approaching Doppler (Hz)",
            "Integrated spectral power (dB)",
            [
                (
                    f"{w} samples",
                    f[keep],
                    _db(np.sum(abs(v[keep]) ** 2, axis=1), -55, True),
                )
                for w, v in zip(wins, win_specs)
            ],
        ),
        "tradeoff": _plot(
            "Window duration versus native frequency scale",
            "Window duration (ms)",
            "Native 1/T scale (Hz)",
            [("Hann support", wins / 4800 * 1000, 4800 / wins)],
        ),
    }
    return _finish(
        values,
        plots,
        "Three scatterers integrate torso and opposite sinusoidal limb velocities into -4pi displacement/lambda phase. Explicit Hann windows use 75% overlap and a 2048-point FFT. The negative raw frequency axis is reversed so positive means approaching. Longer windows narrow frequency response but blur motion timing.",
        "Absolute value of the slow-time IQ record removes carrier phase and signed bulk Doppler; magnitude fluctuations cannot reconstruct the original motion phase.",
        "Use the retained unchanged complex IQ record. The plots use full STFT calculations; display coordinates are decimated and zero-padding is not independent frequency resolution.",
        7401,
        broken,
        speed_extents=(2 * speeds / 0.0125).tolist(),
        carrier_bulk_doppler=(2 * 1.2 / (3e8 / (carriers * 1e9))).tolist(),
        carrier_extents=(2 * speed / (3e8 / (carriers * 1e9))).tolist(),
        window_frame_counts=[v.shape[1] for v in win_specs],
        fft_length=2048,
        sample_count=19200,
        phase_sign=-1,
    )
