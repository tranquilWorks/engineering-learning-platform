from __future__ import annotations

import numpy as np

C = 299792458.0


def _plot(title, x_label, y_label, traces):
    data = []
    for name, x, y in traces:
        x, y = np.asarray(x), np.asarray(y)
        i = np.unique(np.linspace(0, len(x) - 1, min(512, len(x))).astype(int))
        data.append(
            {
                "type": "scatter",
                "mode": "lines",
                "name": name,
                "x": x[i].tolist(),
                "y": y[i].tolist(),
            }
        )
    return {
        "data": data,
        "layout": {
            "title": {"text": title},
            "xaxis": {"title": x_label},
            "yaxis": {"title": y_label},
            "legend": {"orientation": "h"},
        },
        "config": {"responsive": True, "displaylogo": False},
    }


def _heat_indices(axis, score, limit):
    # Keep physical zero and the strongest local peaks when thinning a display.
    axis, score = np.asarray(axis), np.asarray(score)
    peaks = np.flatnonzero((score[1:-1] > score[:-2]) & (score[1:-1] >= score[2:])) + 1
    strongest = peaks[np.argsort(score[peaks], kind="stable")[-3:]]
    mandatory = np.unique(
        np.r_[0, len(axis) - 1, np.argmin(abs(axis)), np.argmax(score), strongest]
    )
    uniform = np.linspace(
        0, len(axis) - 1, max(2, min(len(axis), limit) - len(mandatory))
    ).astype(int)
    return np.unique(np.r_[uniform, mandatory])


def _heat(title, x, y, z, x_label, y_label):
    xi = _heat_indices(x, np.max(z, axis=0), 128)
    yi = _heat_indices(y, np.max(z, axis=1), 64)
    return {
        "data": [
            {
                "type": "heatmap",
                "x": np.asarray(x)[xi].tolist(),
                "y": np.asarray(y)[yi].tolist(),
                "z": np.asarray(z)[np.ix_(yi, xi)].tolist(),
                "colorbar": {"title": "Magnitude (dB)"},
            }
        ],
        "layout": {
            "title": {"text": title},
            "xaxis": {"title": x_label},
            "yaxis": {"title": y_label},
        },
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


def _db(x):
    return 20 * np.log10(np.maximum(np.abs(x), 1e-12))


def run(parameters):
    target_range, velocity, broken = _controls(
        parameters,
        [
            ("middle_target_range_m", 900, [750, 900, 1050]),
            ("middle_velocity_mps", 12, [-18, 0, 12, 18]),
        ],
    )
    wavelength = C / 1e10
    prf = 5000
    fs = 20e6
    rows = 256
    columns = 32
    ranges = [450, target_range, 1200]
    velocities = [0, velocity, -18]
    bins = np.rint(2 * np.array(ranges) / C * fs).astype(int)
    fast = np.arange(rows)
    slow = np.arange(columns) / prf
    clean = np.zeros((rows, columns), complex)
    for b, v, a, phase in zip(bins, velocities, [1, 0.75, 0.55], [0, 40, -30]):
        envelope = np.exp(-0.5 * ((fast - b) / 1.2) ** 2)
        sequence = a * np.exp(
            1j * (np.deg2rad(phase) + 2 * np.pi * 2 * v / wavelength * slow)
        )
        clean += envelope[:, None] * sequence[None, :]
    rng = np.random.default_rng(3701)
    data = clean + 0.02 / np.sqrt(2) * (
        rng.normal(size=clean.shape) + 1j * rng.normal(size=clean.shape)
    )
    active = abs(data) if broken else data
    selected = active[bins[1]]
    phase = np.angle(np.sum(np.conj(selected[:-1]) * selected[1:]))
    estimated = phase * prf / (2 * np.pi)
    doppler_axis = np.fft.fftshift(np.fft.fftfreq(columns, 1 / prf))
    spectrum = np.fft.fftshift(np.fft.fft(selected * np.hanning(columns)))
    spacing = C / (2 * fs)
    ra = fast * spacing
    values = {
        "middle_range_bin": (bins[1], "zero-based index"),
        "sampled_middle_range": (bins[1] * spacing, "m"),
        "range_error": (bins[1] * spacing - target_range, "m"),
        "true_middle_doppler": (2 * velocity / wavelength, "Hz"),
        "active_middle_doppler": (estimated, "Hz"),
        "active_fft_peak": (doppler_axis[np.argmax(abs(spectrum))], "Hz"),
        "range_axis_span": (ra[-1], "m"),
        "prf_unambiguous_range": (C / (2 * prf), "m"),
        "neglected_migration": (
            max(abs(np.array(velocities))) * (columns - 1) / prf / spacing,
            "bins",
        ),
        "model_valid": (not broken, "boolean"),
    }
    rs = np.array([300, 750, 1200])
    vs = np.array([-18, 0, 18])
    plots = {
        "matrix": _heat(
            "Rows are fast time; columns are coherent pulses",
            np.arange(columns),
            ra,
            _db(data / np.max(abs(data))),
            "Pulse (index)",
            "Range (m)",
        ),
        "profiles": _plot(
            "Moving across a column changes fast-time range",
            "Range (m)",
            "Magnitude (relative)",
            [(f"Pulse {i + 1}", ra, abs(data[:, i])) for i in [0, 15, 31]],
        ),
        "phase": _plot(
            "Moving across a row follows slow-time phase",
            "Slow time (ms)",
            "Unwrapped phase (rad)",
            [
                (f"Target {i + 1}", slow * 1000, np.unwrap(np.angle(active[b])))
                for i, b in enumerate(bins)
            ],
        ),
        "doppler": _plot(
            "Middle-target slow-time FFT",
            "Doppler (Hz)",
            "Normalized magnitude (dB)",
            [("Active", doppler_axis, _db(spectrum / max(abs(spectrum))))],
        ),
        "range_sweep": _plot(
            "Range moves the Gaussian response across rows",
            "Range (m)",
            "Range response (relative)",
            [
                (
                    f"Target {r:g} m",
                    ra,
                    np.exp(-0.5 * ((fast - round(2 * r / C * fs)) / 1.2) ** 2),
                )
                for r in rs
            ],
        ),
        "velocity_sweep": _plot(
            "Velocity moves phase without changing range row",
            "Velocity (m/s)",
            "Phase increment (rad/pulse)",
            [("2π fd / PRF", vs, 2 * np.pi * 2 * vs / wavelength / prf)],
        ),
    }
    return _finish(
        values,
        plots,
        "Three separable range-envelope × slow-time-phasor components form a 256×32 complex matrix. The captured range span is shorter than the PRF ambiguity interval.",
        "Taking magnitude of the matrix preserves target-looking range peaks but destroys the middle target's Doppler phase.",
        "Disable the failure to restore the complex matrix, row/column meaning and exact noise realization.",
        3701,
        broken,
        fast_time_samples=rows,
        pulse_count=columns,
    )
