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


CONTROLS = [("bandwidth_mhz", 20, [10, 20, 40]), ("pair_spacing_m", 10, [3.75, 10, 15])]


def _chirp(bandwidth):
    t = (np.arange(240) - 119.5) / 120e6
    return np.exp(1j * np.pi * (bandwidth * 1e6 / 2e-6) * t * t)


def _compress(x, chirp):
    # Zero-padding to1024 implements linear convolution along fast time only.
    length = x.shape[-1] + len(chirp) - 1
    return (
        np.fft.ifft(
            np.fft.fft(x, 1024, axis=-1) * np.fft.fft(chirp[::-1].conj(), 1024), axis=-1
        )[..., :length]
        / np.vdot(chirp, chirp).real
    )


def _pair_profile(bandwidth, spacing):
    chirp = _chirp(bandwidth)
    raw = np.zeros(361, complex)
    starts = np.floor((np.array([1000, 1000 + spacing]) - 950) / 1.25 + 0.5).astype(int)
    for k in starts:
        raw[k : k + 240] += chirp
    p = _compress(raw, chirp)
    ix = starts + 239
    half = max(1, int(np.floor(0.25 * (150 / bandwidth) / 1.25 + 0.5)))
    peaks = [max(abs(p[k - half : k + half + 1])) for k in ix]
    valley = min(abs(p[ix[0] : ix[1] + 1])) / min(peaks)
    return p, float(valley)


def run(parameters):
    bandwidth, spacing, broken = _controls(parameters, CONTROLS)
    chirp = _chirp(bandwidth)
    pos = np.linspace(-40, 40, 401)
    ra = np.linspace(950, 1400, 361)
    axis = 950 + (np.arange(600) - 239) * 1.25
    truthx = np.array([-15, 0, 18])
    truthr = np.array([1000, 1025, 1070])
    amps = np.array([1, 0.8, 0.6])
    phases = np.array([0, 0.6, -0.9])
    slant = np.sqrt(truthr**2 + (pos[:, None] - truthx) ** 2)
    delay = np.floor((slant - 950) / 1.25 + 0.5).astype(int)
    phase = phases - 4 * np.pi * (slant - truthr) / 0.06
    raw = np.zeros((401, 361), complex)
    for q in range(3):
        for k in range(401):
            raw[k, delay[k, q] : delay[k, q] + 240] += (
                amps[q] * np.exp(1j * phase[k, q]) * chirp
            )
    raw += 0.2 * _noise(7601, 401, 361, True)
    compressed = _compress(raw, chirp)
    active = abs(compressed) if broken else compressed
    ridge = compressed[np.arange(401), delay[:, 2] + 239]
    selected = active[np.arange(401), delay[:, 2] + 239]
    expected = np.exp(1j * phase[:, 2])
    coherence = lambda z: abs(
        np.mean(z / np.maximum(abs(z), np.finfo(float).eps) * expected.conj())
    )
    bs = np.array([10, 20, 40])
    widths = []
    profiles = []
    for b in bs:
        c = _chirp(b)
        x = np.zeros(361, complex)
        x[40:280] = c
        p = _compress(x, c)
        profiles.append(p)
        widths.append(_width(axis, abs(p) ** 2))
    spacings = np.array([3.75, 10, 15])
    pairs = [_pair_profile(bandwidth, s) for s in spacings]
    pair, ratio = _pair_profile(bandwidth, spacing)
    center = abs(compressed[200])
    audit = []
    for q in range(3):
        k = delay[200, q] + 239
        ix = np.arange(k - 2, k + 3)
        audit.append(float(axis[ix[np.argmax(center[ix])]]))
    values = {
        "nominal_resolution": (150 / bandwidth, "m"),
        "range_sample_spacing": (1.25, "m"),
        "pulse_energy": (np.vdot(chirp, chirp).real, "voltage² samples"),
        "active_phase_coherence": (coherence(selected), "ratio"),
        "recovered_phase_coherence": (coherence(ridge), "ratio"),
        "magnitude_phase_coherence": (coherence(abs(ridge)), "ratio"),
        "maximum_range_quantization": (
            max(abs(slant - (950 + delay * 1.25)).ravel()),
            "m",
        ),
        "isolated_hpbw": (widths[list(bs).index(bandwidth)], "m"),
        "selected_pair_valley_ratio": (ratio, "ratio"),
        "third_target_center_range": (audit[2], "m"),
        "third_target_center_voltage": (
            abs(compressed[200, delay[200, 2] + 239]),
            "voltage",
        ),
        "model_valid": (not broken, "boolean"),
    }
    plots = {
        "selected_pair": _plot(
            "Selected noiseless pair spacing",
            "Range (m)",
            "Compressed magnitude (ratio)",
            [("Selected pair", axis, abs(pair))],
        ),
        "waveform": _plot(
            "Energy-normalized matched filter uses the complex chirp",
            "Pulse time (us)",
            "Voltage (ratio)",
            [
                ("I", (np.arange(240) - 119.5) / 120, chirp.real),
                ("Q", (np.arange(240) - 119.5) / 120, chirp.imag),
            ],
        ),
        "raw": _heat(
            "Raw unfocused aperture/fast-time record",
            "Apparent range (m)",
            "Platform cross-range (m)",
            ra,
            pos,
            abs(raw),
            "voltage",
        ),
        "compressed": _heat(
            "Linear range compression preserves aperture rows",
            "Filter-delay-corrected range (m)",
            "Platform cross-range (m)",
            axis,
            pos,
            _db(abs(compressed) ** 2, -60, True),
            "dB",
        ),
        "center": _plot(
            "Center look before and after compression",
            "Range (m)",
            "Magnitude (voltage)",
            [("Raw", ra, abs(raw[200])), ("Compressed", axis, abs(compressed[200]))],
        ),
        "bandwidth": _plot(
            "Isolated noiseless response at fixed pulse duration",
            "Range (m)",
            "Normalized magnitude (ratio)",
            [(f"{b:g} MHz", axis, abs(p)) for b, p in zip(bs, profiles)],
        ),
        "spacing": _plot(
            "Equal coherent targets: spacing changes only the pair scene",
            "Range (m)",
            "Normalized magnitude (ratio)",
            [
                (f"{s:g} m separation", axis, abs(p))
                for s, (p, _) in zip(spacings, pairs)
            ],
        ),
        "phase": _plot(
            "Third target ridge keeps path phase",
            "Platform cross-range (m)",
            "Unwrapped phase (rad)",
            [
                ("Selected", pos, np.unwrap(np.angle(selected))),
                ("Expected", pos, np.unwrap(np.angle(expected))),
                ("Recovered", pos, np.unwrap(np.angle(ridge))),
            ],
        ),
    }
    return _finish(
        values,
        plots,
        "A 240-sample LFM echo is inserted at each quantized delay without wrapping. Independent per-row linear matched filtering divides by 240 and subtracts 239 filter-delay samples from the axis. Three targets retain complex aperture phase. Bandwidth controls the waveform; pair spacing affects a separate noiseless equal-target demonstration.",
        "Magnitude-only range history retains identical range ridges but replaces each aperture phase by zero, destroying later coherent azimuth processing.",
        "Recover the retained original complex range-compressed record; lost phase cannot be reconstructed from magnitude. This lesson performs range compression only, not azimuth focusing.",
        7601,
        broken,
        bandwidth_hpbw=widths,
        pair_valley_ratios=[p[1] for p in pairs],
        pair_resolved=[bool(p[1] < 1 / np.sqrt(2)) for p in pairs],
        raw_shape=[401, 361],
        compressed_shape=[401, 600],
        filter_delay_samples=239,
        center_target_ranges=audit,
        third_ridge_phase=np.unwrap(np.angle(ridge)).tolist(),
    )
