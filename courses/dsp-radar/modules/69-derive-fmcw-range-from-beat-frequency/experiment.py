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


CONTROLS = [("target_range_m", 45, [15, 45, 75]), ("bandwidth_mhz", 20, [10, 20, 30])]


def _beat(range_m, bandwidth):
    fs = 80e6
    t = np.arange(3200) / fs
    s = bandwidth * 1e6 / 40e-6
    delay = 2 * range_m / 3e8
    mask = t >= delay
    tx = np.exp(1j * np.pi * s * (t - 20e-6) ** 2)
    rx = np.zeros(3200, complex)
    rx[mask] = (
        0.7 * np.exp(1j * np.pi * s * (t[mask] - delay - 20e-6) ** 2)
        + 0.01 * _noise(6901, 3200)[:, 0][mask]
    )
    beat = tx[mask] * rx[mask].conj()
    power = abs(np.fft.fft(beat * np.hanning(len(beat)), 65536)[:32769]) ** 2
    k = 1 + np.argmax(power[1:])
    l, c, r = np.log(power[k - 1 : k + 2])
    offset = np.clip(0.5 * (l - r) / (l - 2 * c + r), -0.5, 0.5)
    frequency = (k + offset) * fs / 65536
    phase = np.angle(np.vdot(beat[:-1], beat[1:])) * fs / (2 * np.pi)
    return t, tx, rx, mask, beat, power, frequency, phase


def run(parameters):
    range_m, bandwidth, broken = _controls(parameters, CONTROLS)
    s = bandwidth * 1e6 / 40e-6
    t, tx, rx, mask, beat, power, f, phase = _beat(range_m, bandwidth)
    estimated = 3e8 * f / (2 * s)
    active = estimated * (2 if broken else 1)
    ranges = np.array([15, 30, 45, 60, 75])
    bandwidths = np.array([10, 15, 20, 25, 30])
    rs = [_beat(r, bandwidth)[6] for r in ranges]
    bs = [_beat(range_m, b)[6] for b in bandwidths]
    values = {
        "active_range": (active, "m"),
        "fft_beat": (f / 1000, "kHz"),
        "theoretical_beat": (2 * s * range_m / 3e8 / 1000, "kHz"),
        "phase_beat": (phase / 1000, "kHz"),
        "corrected_range": (estimated, "m"),
        "range_error": (active - range_m, "m"),
        "valid_samples": (len(beat), "count"),
        "range_sweep_last_beat": (rs[-1] / 1000, "kHz"),
        "slope_sweep_last_beat": (bs[-1] / 1000, "kHz"),
        "nominal_resolution": (3e8 / (2 * bandwidth * 1e6), "m"),
        "model_valid": (not broken, "boolean"),
    }
    freq = np.arange(32769) * 80e6 / 65536
    keep = freq <= 500000
    plots = {
        "raw_iq": _plot(
            "Transmit and delayed noisy receive IQ",
            "Time (us)",
            "I voltage (ratio)",
            [("Tx", t * 1e6, tx.real), ("Rx", t * 1e6, rx.real)],
        ),
        "chirp": _plot(
            "Transmit and physically delayed echo",
            "Time (us)",
            "Instantaneous frequency (MHz)",
            [
                ("Tx", t * 1e6, s * (t - 20e-6) / 1e6),
                (
                    "Rx valid overlap",
                    t[mask] * 1e6,
                    s * (t[mask] - 2 * range_m / 3e8 - 20e-6) / 1e6,
                ),
            ],
        ),
        "mixer": _plot(
            "Tx times conjugate Rx",
            "Valid time (us)",
            "Voltage (ratio)",
            [("I", t[mask] * 1e6, beat.real), ("Q", t[mask] * 1e6, beat.imag)],
        ),
        "spectrum": _plot(
            "Hann-windowed beat with log-power peak interpolation",
            "Beat frequency (kHz)",
            "Normalized power (dB)",
            [("Beat", freq[keep] / 1000, _db(power[keep], -80, True))],
        ),
        "range_sweep": _plot(
            "Fixed-slope range sweep",
            "True range (m)",
            "Beat frequency (kHz)",
            [
                ("Measured", ranges, np.array(rs) / 1000),
                ("S tau", ranges, 2 * s * ranges / 3e8 / 1000),
            ],
        ),
        "slope_sweep": _plot(
            "Fixed-range slope sweep",
            "Bandwidth (MHz)",
            "Beat frequency (kHz)",
            [("Measured", bandwidths, np.array(bs) / 1000)],
        ),
        "conversion": _plot(
            "Same beat, round-trip conversion",
            "Truth/wrong/recovered/selected (index)",
            "Estimated range (m)",
            [("Range", [0, 1, 2, 3], [range_m, 2 * estimated, estimated, active])],
        ),
    }
    return _finish(
        values,
        plots,
        "An 80 MHz sampled,40 us centered chirp returns after tau=2R/c. Only valid overlap is mixed as Tx conj(Rx), giving positive beat S tau. A Hann window and 65536-point FFT interpolate the beat; zero-padding does not improve the physical c/(2B) resolution.",
        "Using R=c fbeat/S omits round-trip propagation and doubles the same estimate.",
        "Restore R=c fbeat/(2S) without changing the observed beat.",
        6901,
        broken,
        range_sweep_beats_khz=(np.array(rs) / 1000).tolist(),
        slope_sweep_beats_khz=(np.array(bs) / 1000).tolist(),
        sample_rate_hz=80e6,
        fft_length=65536,
    )
