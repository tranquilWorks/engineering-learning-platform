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


CONTROLS = [("fast_samples", 512, [128, 256, 512]), ("chirps", 64, [16, 32, 64])]


def _process(data, broken=False):
    n, m = data.shape
    wr = np.hanning(n)
    wd = np.hanning(m)
    ranges = np.fft.fft(data * wr[:, None], axis=0)[: n // 2 + 1] / sum(wr)
    active = abs(ranges) if broken else ranges
    rd = np.fft.fftshift(np.fft.fft(active * wd, axis=1), axes=1) / sum(wd)
    raxis = np.arange(n // 2 + 1) * 3e8 * 12.8e6 / (2 * 3.75e12 * n)
    vaxis = -np.fft.fftshift(np.fft.fftfreq(m, 50e-6)) * (3e8 / 77e9) / 2
    return ranges, rd, raxis, vaxis


def run(parameters):
    n, m, broken = _controls(parameters, CONTROLS)
    n, m = int(n), int(m)
    ranges = np.array([20, 20, 23])
    dv = (3e8 / 77e9) / (2 * 64 * 50e-6)
    velocities = np.array([-3, 3, 3]) * dv
    tf = np.arange(512) / 12.8e6
    ts = np.arange(64) * 50e-6
    data = np.zeros((512, 64), complex)
    for r, v, amp, phase in zip(
        ranges, velocities, [1, 0.82, 0.68], [0.1, 0.75, -0.55]
    ):
        data += amp * np.exp(
            2j
            * np.pi
            * (2 * 3.75e12 * r / 3e8 * tf[:, None] - 2 * v / (3e8 / 77e9) * ts)
            + 1j * phase
        )
    data += 0.01 * _noise(7001, 512, 64)
    range_data, rd, ra, va = _process(data[:n, :m], broken)
    _, good, _, _ = _process(data[:n, :m])
    isolated = int(np.argmin(abs(ra - 23)))
    peak = int(np.argmax(abs(rd[isolated])))
    recovered = int(np.argmax(abs(good[isolated])))
    # Truth only defines audit neighborhoods; it never forms either transform.
    peaks = []
    for r, v in zip(ranges, velocities):
        ri = int(np.argmin(abs(ra - r)))
        vi = int(np.argmin(abs(va - v)))
        rr = np.arange(max(0, ri - 1), min(len(ra), ri + 2))
        vv = np.arange(max(0, vi - 1), min(len(va), vi + 2))
        local = abs(good[np.ix_(rr, vv)])
        i, j = np.unravel_index(
            np.argmax(local.ravel(order="F")), local.shape, order="F"
        )
        peaks.append([float(ra[rr[i]]), float(va[vv[j]]), float(local[i, j])])
    ns = np.array([128, 256, 512])
    ms = np.array([16, 32, 64])
    dr = 3e8 * 12.8e6 / (2 * 3.75e12 * ns)
    dvs = (3e8 / 77e9) / (2 * ms * 50e-6)
    values = {
        "range_bin_spacing": (ra[1] - ra[0], "m"),
        "velocity_bin_spacing": (abs(va[1] - va[0]), "m/s"),
        "active_isolated_velocity": (va[peak], "m/s"),
        "recovered_isolated_velocity": (va[recovered], "m/s"),
        "isolated_true_velocity": (velocities[2], "m/s"),
        "active_peak_magnitude": (abs(rd[isolated, peak]), "voltage"),
        "first_target_range": (peaks[0][0], "m"),
        "first_target_velocity": (peaks[0][1], "m/s"),
        "third_target_range": (peaks[2][0], "m"),
        "third_target_voltage": (peaks[2][2], "voltage"),
        "model_valid": (not broken, "boolean"),
    }
    plots = {
        "raw": _heat(
            "Two acquisition clocks before transforms",
            "Chirp (index)",
            "Fast time (us)",
            np.arange(m),
            tf[:n] * 1e6,
            data[:n, :m].real,
            "I voltage",
        ),
        "range": _heat(
            "Range FFT retains complex slow-time columns",
            "Chirp (index)",
            "Range (m)",
            np.arange(m),
            ra,
            _db(abs(range_data) ** 2, -70, True),
            "dB",
        ),
        "map": _heat(
            "Selected signed range-Doppler map",
            "Approaching velocity (m/s)",
            "Range (m)",
            va[::-1],
            ra,
            _db(abs(rd[:, ::-1]) ** 2, -70, True),
            "dB",
        ),
        "phase": _plot(
            "Isolated range-bin slow-time phase",
            "Chirp time (ms)",
            "Unwrapped phase (rad)",
            [
                (
                    "Complex range bin",
                    ts[:m] * 1000,
                    np.unwrap(np.angle(range_data[isolated])),
                )
            ],
        ),
        "velocity_sweep": _plot(
            "Coherent dwell controls velocity spacing",
            "Chirps (count)",
            "Velocity bin spacing (m/s)",
            [("lambda/(2 M Tr)", ms, dvs)],
        ),
        "range_sweep": _plot(
            "Retained fast-time aperture controls range spacing",
            "Fast samples (count)",
            "Range bin spacing (m)",
            [("c fs/(2 S N)", ns, dr)],
        ),
        "recovery": _plot(
            "Preserve complex phase before slow FFT",
            "Approaching velocity (m/s)",
            "Isolated-bin voltage (ratio)",
            [
                ("Selected", va[::-1], abs(rd[isolated, ::-1])),
                ("Complex recovery", va[::-1], abs(good[isolated, ::-1])),
            ],
        ),
    }
    # Prefix transforms are retained as measured sweep evidence, not just formula labels.
    sweep_peaks = {}
    for nn, mm in [(512, k) for k in ms] + [(k, 64) for k in ns]:
        _, z, r, v = _process(data[:nn, :mm])
        row = np.argmin(abs(r - 23))
        sweep_peaks[f"{nn}x{mm}"] = float(v[np.argmax(abs(z[row]))])
    return _finish(
        values,
        plots,
        "The 512x64 stop-and-hop scene separates two 20 m targets by signed velocity and a third at 23 m. Hann FFTs transform fast-time rows then coherent chirp columns. Tx conj(Rx) gives slow frequency -2v/lambda; the plotted velocity axis reverses that sign. Within-chirp Doppler coupling belongs to P71.",
        "Taking absolute value of range data before its slow-time FFT erases signed phase and collapses the isolated moving target near zero velocity.",
        "Retain the unchanged complex range data and transform the chirp dimension. Toggle off reproduces the selected coherent map exactly.",
        7001,
        broken,
        target_audit=peaks,
        prefix_velocity_peaks=sweep_peaks,
        raw_shape=[n, m],
        range_shape=list(range_data.shape),
        target_velocities=velocities.tolist(),
    )
