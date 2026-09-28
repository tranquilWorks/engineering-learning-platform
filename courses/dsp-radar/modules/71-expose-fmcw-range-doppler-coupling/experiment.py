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


CONTROLS = [("velocity_mps", 20, [-30, 0, 20, 30]), ("bandwidth_mhz", 20, [10, 20, 30])]


def _moving_beat(velocity, bandwidth):
    t = np.arange(3200) / 80e6
    s = bandwidth * 1e6 / 40e-6
    tau = 90 / 3e8
    mask = t >= tau
    fd = 2 * velocity / (3e8 / 77e9)
    tx = np.exp(1j * np.pi * s * (t - 20e-6) ** 2)
    rx = np.exp(1j * (np.pi * s * (t - tau - 20e-6) ** 2 + 2 * np.pi * fd * t + 0.35))
    beat = tx[mask] * rx[mask].conj() + 0.002 * _noise(7101, 3200)[:, 0][mask]
    f = np.angle(np.vdot(beat[:-1], beat[1:])) * 80e6 / (2 * np.pi)
    return t[mask], beat, f


def run(parameters):
    velocity, bandwidth, broken = _controls(parameters, CONTROLS)
    s = bandwidth * 1e6 / 40e-6
    fd = 2 * velocity / (3e8 / 77e9)
    t, beat, f = _moving_beat(velocity, bandwidth)
    stationary = 3e8 * f / (2 * s)
    corrected = 3e8 * (f + fd) / (2 * s)
    wrong = 3e8 * (f - fd) / (2 * s)
    active = wrong if broken else corrected
    vs = np.array([-30, -15, 0, 15, 30])
    bs = np.array([10, 15, 20, 25, 30])
    vb = [3e8 * _moving_beat(v, bandwidth)[2] / (2 * s) - 45 for v in vs]
    bb = [3e8 * _moving_beat(velocity, b)[2] / (2 * b * 1e6 / 40e-6) - 45 for b in bs]
    values = {
        "signed_beat": (f / 1000, "kHz"),
        "doppler": (fd / 1000, "kHz"),
        "stationary_range": (stationary, "m"),
        "stationary_bias": (stationary - 45, "m"),
        "ideal_bias": (-77e9 * velocity / s, "m"),
        "active_range": (active, "m"),
        "active_error": (active - 45, "m"),
        "corrected_range": (corrected, "m"),
        "velocity_sweep_last_bias": (vb[-1], "m"),
        "slope_sweep_last_bias": (bb[-1], "m"),
        "model_valid": (not broken, "boolean"),
    }
    ff = np.fft.fftshift(np.fft.fftfreq(16384, 1 / 80e6))
    spec = abs(np.fft.fftshift(np.fft.fft(beat * np.hanning(len(beat)), 16384))) ** 2
    keep = abs(ff) < 400000
    plots = {
        "chirp_frequency": _plot(
            "Delay and Doppler in the transmitted and received chirps",
            "Overlap time (us)",
            "Instantaneous frequency (MHz)",
            [
                ("Tx", t * 1e6, s * (t - 20e-6) / 1e6),
                ("Moving Rx", t * 1e6, (s * (t - 90 / 3e8 - 20e-6) + fd) / 1e6),
            ],
        ),
        "mixer": _plot(
            "Signed beat from delayed moving echo",
            "Overlap time (us)",
            "Voltage (ratio)",
            [("I", t * 1e6, beat.real), ("Q", t * 1e6, beat.imag)],
        ),
        "spectrum": _plot(
            "Retain the sign of the beat",
            "Signed mixer frequency (kHz)",
            "Normalized power (dB)",
            [("Beat", ff[keep] / 1000, _db(spec[keep], -80, True))],
        ),
        "ranges": _plot(
            "Independent velocity corrects a single coupled beat",
            "Truth/stationary/wrong/corrected/selected (index)",
            "Range (m)",
            [("Estimates", np.arange(5), [45, stationary, wrong, corrected, active])],
        ),
        "velocity": _plot(
            "Change only radial velocity",
            "Approaching velocity (m/s)",
            "Stationary range bias (m)",
            [("Measured", vs, vb), ("-fc v/S", vs, -77e9 * vs / s)],
        ),
        "slope": _plot(
            "Change only chirp slope",
            "Bandwidth (MHz)",
            "Stationary range bias (m)",
            [
                ("Measured", bs, bb),
                ("-fc v/S", bs, -77e9 * velocity / (bs * 1e6 / 40e-6)),
            ],
        ),
    }
    return _finish(
        values,
        plots,
        "With approaching-positive velocity, Rx has +fd but Tx conj(Rx) yields fbeat=S tau-fd. The frozen-delay 45 m model measures lag-one signed frequency. A single chirp cannot identify both range and velocity; correction uses independently supplied velocity.",
        "Subtracting fd again gives the wrong-sign correction and doubles the ideal stationary range bias.",
        "Add the independently known signed fd to the unchanged beat before converting delay to range.",
        7101,
        broken,
        velocity_sweep_bias=vb,
        bandwidth_sweep_bias=bb,
        velocity_is_independent_input=True,
    )
