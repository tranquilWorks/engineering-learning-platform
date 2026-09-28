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
    ("target_range_m", 45, [15, 45, 75]),
    ("velocity_mps", 20, [-30, 0, 20, 30]),
]


def _pair(range_m, velocity, noise_rms=0.002):
    t = np.arange(3200) / 80e6
    mask = t >= 2 * range_m / 3e8
    s = 5e11
    fd = 2 * velocity / (3e8 / 77e9)
    tau = 2 * range_m / 3e8
    beats = []
    freq = []
    for sign, seed in [(1, 7201), (-1, 7202)]:
        tx = np.exp(sign * 1j * np.pi * s * (t - 20e-6) ** 2)
        rx = np.exp(
            1j * (sign * np.pi * s * (t - tau - 20e-6) ** 2 + 2 * np.pi * fd * t + 0.35)
        )
        b = tx[mask] * rx[mask].conj() + noise_rms * _noise(seed, 3200)[:, 0][mask]
        beats.append(b)
        freq.append(np.angle(np.vdot(b[:-1], b[1:])) * 80e6 / (2 * np.pi))
    return t[mask], beats, np.array(freq)


def _solve(up, down):
    return 3e8 * (up - down) / (4 * 5e11), -(3e8 / 77e9) * (up + down) / 4


def _detect(samples):
    spectrum = abs(
        np.fft.fftshift(np.fft.fft(samples * np.hanning(len(samples)), 32768))
    )
    search = spectrum.copy()
    axis = np.fft.fftshift(np.fft.fftfreq(32768, 1 / 80e6))
    frequencies = []
    width = int(np.ceil(60000 / (80e6 / 32768)))
    for _ in range(2):
        k = np.argmax(search)
        l, c, r = spectrum[k - 1 : k + 2]
        offset = np.clip(0.5 * (l - r) / (l - 2 * c + r), -0.5, 0.5)
        frequencies.append(axis[k] + offset * 80e6 / 32768)
        search[max(0, k - width) : k + width + 1] = 0
    return np.sort(frequencies), axis, spectrum


def _multi():
    t = np.arange(3200) / 80e6
    mask = t >= 130 / 3e8
    out = []
    for sign, seed in [(1, 7701), (-1, 7702)]:
        tx = np.exp(sign * 1j * np.pi * 5e11 * (t - 20e-6) ** 2)
        rx = np.zeros(3200, complex)
        for r, v, amp, phi in zip([30, 65], [15, -10], [1, 0.8], [0.2, -0.6]):
            tau = 2 * r / 3e8
            m = t >= tau
            rx[m] += amp * np.exp(
                1j
                * (
                    sign * np.pi * 5e11 * (t[m] - tau - 20e-6) ** 2
                    + 2 * np.pi * 2 * v / (3e8 / 77e9) * t[m]
                    + phi
                )
            )
        beat = tx[mask] * rx[mask].conj() + 0.002 * _noise(seed, 3200)[:, 0][mask]
        out.append(_detect(beat))
    return out


def run(parameters):
    r, v, broken = _controls(parameters, CONTROLS)
    t, beats, f = _pair(r, v)
    er, ev = _solve(*f)
    up, down = _multi()
    ghost_r, ghost_v = _solve(up[0], down[0])
    rec_r, rec_v = _solve(up[0], down[0][::-1])
    active_r = ghost_r[0] if broken else er
    active_v = ghost_v[0] if broken else ev
    rs = np.array([15, 30, 45, 60, 75])
    vs = np.array([-30, -15, 0, 15, 30])
    ns = np.array([0, 0.002, 0.01, 0.03, 0.08])
    rsol = np.array([_solve(*_pair(q, v)[2]) for q in rs])
    vsol = np.array([_solve(*_pair(r, q)[2]) for q in vs])
    nsol = np.array([_solve(*_pair(r, v, q)[2]) for q in ns])
    values = {
        "up_beat": (f[0] / 1000, "kHz"),
        "down_beat": (f[1] / 1000, "kHz"),
        "active_range": (active_r, "m"),
        "active_velocity": (active_v, "m/s"),
        "selected_range_error": (er - r, "m"),
        "selected_velocity_error": (ev - v, "m/s"),
        "first_ghost_range": (ghost_r[0], "m"),
        "first_ghost_velocity": (ghost_v[0], "m/s"),
        "first_recovered_range": (rec_r[0], "m"),
        "first_recovered_velocity": (rec_v[0], "m/s"),
        "noise_high_range_error": (nsol[-1, 0] - r, "m"),
        "noise_high_velocity_error": (nsol[-1, 1] - v, "m/s"),
        "model_valid": (not broken, "boolean"),
    }
    plots = {
        "chirp_frequency": _plot(
            "Opposite chirp slopes with delayed moving echoes",
            "Overlap time (us)",
            "Instantaneous frequency (MHz)",
            [
                ("Up Tx", t * 1e6, 5e11 * (t - 20e-6) / 1e6),
                (
                    "Up Rx",
                    t * 1e6,
                    (5e11 * (t - 2 * r / 3e8 - 20e-6) + 2 * v / (3e8 / 77e9)) / 1e6,
                ),
                ("Down Tx", t * 1e6, -5e11 * (t - 20e-6) / 1e6),
                (
                    "Down Rx",
                    t * 1e6,
                    (-5e11 * (t - 2 * r / 3e8 - 20e-6) + 2 * v / (3e8 / 77e9)) / 1e6,
                ),
            ],
        ),
        "beats": _plot(
            "Opposite signed chirp legs",
            "Overlap time (us)",
            "Mixer I voltage (ratio)",
            [(name, t * 1e6, b.real) for name, b in zip(["Up", "Down"], beats)],
        ),
        "range": _plot(
            "Difference isolates delay",
            "True range (m)",
            "Estimated range (m)",
            [("Paired solve", rs, rsol[:, 0])],
        ),
        "velocity": _plot(
            "Sum isolates signed Doppler",
            "True velocity (m/s)",
            "Estimated velocity (m/s)",
            [("Paired solve", vs, vsol[:, 1])],
        ),
        "noise": _plot(
            "Fixed waveforms with scaled receiver noise",
            "Noise RMS (voltage)",
            "Range error (m)",
            [("Error", ns, nsol[:, 0] - r)],
        ),
        "multi_spectrum": _plot(
            "Two targets yield two peaks per leg",
            "Signed beat frequency (kHz)",
            "Normalized magnitude (dB)",
            [
                (
                    name,
                    record[1][abs(record[1]) < 400000] / 1000,
                    _db(record[2][abs(record[1]) < 400000] ** 2, -80, True),
                )
                for name, record in [("Up", up), ("Down", down)]
            ],
        ),
        "pairing_range": _plot(
            "Same peak lists, different associations",
            "Paired report (index)",
            "Range (m)",
            [
                ("Wrong pairing", [0, 1], ghost_r),
                ("Correct pairing", [0, 1], rec_r),
                ("Truth", [0, 1], [30, 65]),
            ],
        ),
        "pairing_velocity": _plot(
            "Ghost velocity from wrong pairing",
            "Paired report (index)",
            "Approaching velocity (m/s)",
            [
                ("Wrong pairing", [0, 1], ghost_v),
                ("Correct pairing", [0, 1], rec_v),
                ("Truth", [0, 1], [15, -10]),
            ],
        ),
    }
    return _finish(
        values,
        plots,
        "Signed legs satisfy fup=S tau-fd and fdown=-S tau-fd. Their difference isolates delay and negative sum isolates Doppler. Single-target estimates use lag-one phase; the separate two-target scene uses separated interpolated FFT peaks.",
        "Sorting signed up/down peak lists in the same order cross-pairs the two targets and creates plausible ghost reports.",
        "Reverse the down list for this reviewed association and solve using unchanged detections. This requires correct association evidence and is not a general multi-target matching algorithm. Disable the toggle for the selected single-target result.",
        7201,
        broken,
        detected_up_khz=(up[0] / 1000).tolist(),
        detected_down_khz=(down[0] / 1000).tolist(),
        recovered_ranges=rec_r.tolist(),
        recovered_velocities=rec_v.tolist(),
        ghost_ranges=ghost_r.tolist(),
        ghost_velocities=ghost_v.tolist(),
        noise_sweep_range_error=(nsol[:, 0] - r).tolist(),
    )
