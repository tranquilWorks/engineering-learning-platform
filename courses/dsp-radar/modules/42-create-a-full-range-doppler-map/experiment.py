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
        ix = np.unique(np.linspace(0, len(x) - 1, min(512, len(x))).astype(int))
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


def _compress(raw, pulse):
    return np.column_stack(
        [
            np.convolve(raw[:, j], np.conj(pulse[::-1]), "full")[
                len(pulse) - 1 : len(pulse) - 1 + len(raw)
            ]
            for j in range(raw.shape[1])
        ]
    )


def run(parameters):
    count, taper, broken = _controls(
        parameters, [("pulse_count", 64, [16, 32, 64]), ("hann_weight", 1, [0, 1])]
    )
    n = int(count)
    c = 299792458.0
    fs = 20e6
    prf = 4000.0
    wavelength = c / 1e10
    time = (np.arange(48) - 23.5) / fs
    pulse = np.exp(1j * np.pi * (8e6 / 2.4e-6) * time * time)
    ranges = np.array([1200, 1200, 2400])
    vel = np.array([-7.5, 10.3, 10.3])
    amp = [1, 0.8, 0.65]
    phase = np.deg2rad([0, 35, -50])
    delays = np.floor(2 * ranges / c * fs + 0.5).astype(int)
    slow = np.arange(64) / prf
    raw = np.zeros((512, 64), complex)
    for d, v, a, ph in zip(delays, vel, amp, phase):
        raw[d : d + 48] += (
            a
            * pulse[:, None]
            * np.exp(1j * (ph + 2 * np.pi * (2 * v / wavelength) * slow))
        )
    rng = np.random.default_rng(4201)
    clutter_delays = np.floor(np.linspace(24, 452, 24) + 0.5).astype(int)
    coeff = (
        0.055
        / np.sqrt(1 + clutter_delays / 80)
        * (rng.normal(size=24) + 1j * rng.normal(size=24))
        / np.sqrt(2)
    )
    for d, a in zip(clutter_delays, coeff):
        raw[d : d + 48] += a * pulse[:, None]
    raw += (
        0.35
        / np.sqrt(2)
        * (rng.normal(size=(512, 64)) + 1j * rng.normal(size=(512, 64)))
    )
    compressed = _compress(raw, pulse)
    rc = compressed[:, :n]
    window = (1 - taper) + taper * np.hanning(n)
    rd = np.fft.fftshift(np.fft.fft(rc * window, axis=1), axes=1) / window.sum()
    vaxis = np.fft.fftshift(np.fft.fftfreq(n, 1 / prf)) * wavelength / 2
    raxis = np.arange(512) * c / (2 * fs)
    bad = np.fft.fftshift(np.fft.fft(rc, axis=0), axes=0)
    active = bad if broken else rd
    measured = []
    peaks = []
    for d, v in zip(delays, vel):
        j = int(np.argmin(abs(vaxis - v)))
        rr = np.arange(d - 4, d + 5)
        jj = np.arange(max(0, j - 2), min(n, j + 3))
        patch = abs(rd[np.ix_(rr, jj)])
        a, b = np.unravel_index(np.argmax(patch), patch.shape)
        measured.append([raxis[rr[a]], vaxis[jj[b]]])
        peaks.append(patch[a, b])
    measured = np.array(measured)
    tone = np.exp(2j * np.pi * 10.1 * np.arange(64) / 64)
    spectra = []
    width = []
    side = []
    for w in [np.ones(64), np.hanning(64)]:
        z = abs(np.fft.fftshift(np.fft.fft(tone * w))) / sum(w)
        db = 20 * np.log10(np.maximum(z / max(z), 10 ** (-55 / 20)))
        pk = np.argmax(z)
        mask = np.abs(np.arange(64) - pk) > 2
        spectra.append(db)
        width.append(int(sum(db >= -6)))
        side.append(max(db[mask]))
    values = {
        "range_spacing": (c / (2 * fs), "m"),
        "range_resolution": (c / (16e6), "m"),
        "velocity_spacing": (prf / n * wavelength / 2, "m/s"),
        "first_range": (measured[0, 0], "m"),
        "first_velocity": (measured[0, 1], "m/s"),
        "second_velocity": (measured[1, 1], "m/s"),
        "third_range": (measured[2, 0], "m"),
        "first_peak": (peaks[0], "amplitude"),
        "rectangular_sidelobe": (side[0], "dB"),
        "hann_sidelobe": (side[1], "dB"),
        "active_peak": (np.max(abs(active)), "amplitude"),
        "model_valid": (not broken, "boolean"),
    }
    db = lambda x: 20 * np.log10(np.maximum(abs(x) / np.max(abs(x)), 10 ** (-55 / 20)))
    plots = {
        "waveform": _plot(
            "Explicit LFM phase law",
            "Fast time (µs)",
            "Amplitude (relative)",
            [("I", time * 1e6, pulse.real), ("Q", time * 1e6, pulse.imag)],
        ),
        "raw": _heat(
            "Echoes before range compression",
            "Pulse (index)",
            "Fast-time range (m)",
            np.arange(n),
            raxis,
            db(raw[:, :n]),
            "dB",
        ),
        "compressed": _heat(
            "Matched filter with N−1 delay removed",
            "Pulse (index)",
            "Range (m)",
            np.arange(n),
            raxis,
            db(rc),
            "dB",
        ),
        "map": _heat(
            "Range–Doppler map",
            "Approaching velocity (m/s)",
            "Range (m)",
            vaxis,
            raxis,
            db(rd),
            "dB",
        ),
        "shared": _plot(
            "Two velocities at the same range",
            "Velocity (m/s)",
            "Amplitude (relative)",
            [("Shared row", vaxis, abs(rd[delays[0]]))],
        ),
        "cpi": _plot(
            "Longer coherent dwell narrows Doppler bins",
            "Pulse count (pulses)",
            "Velocity spacing (m/s)",
            [("Spacing", [16, 32, 64], prf / np.array([16, 32, 64]) * wavelength / 2)],
        ),
        "windows": _plot(
            "Window sidelobes and mainlobe width",
            "Doppler bin (index)",
            "Relative amplitude (dB)",
            [
                (label, np.arange(-32, 32), z)
                for label, z in zip(["Rectangular", "Hann"], spectra)
            ],
        ),
        "failure": _heat(
            "Wrong-axis fast-time FFT: columns are still pulses",
            "Pulse (index)",
            "Fast-time frequency (cycles/sample)",
            np.arange(n),
            np.arange(-256, 256) / 512,
            db(bad),
            "dB",
        ),
    }
    return _finish(
        values,
        plots,
        "Fast-time matched filtering separates range; the slow-time FFT separates signed velocity. Targets can share either coordinate and remain distinct in the two-dimensional map.",
        "FFT along fast time creates fast-time frequency, not Doppler. Relabeling pulse columns as velocity cannot repair it.",
        "Restore delay-corrected range compression, apply the selected slow-time window and FFT across pulse columns; disable the toggle for the exact selected map.",
        4201,
        broken,
        shape=[512, n],
        measured_targets=measured.tolist(),
        window_width_bins=width,
        window_sidelobes_db=side,
        coherent_gain=float(sum(window)),
    )
