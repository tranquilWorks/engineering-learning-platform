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
    velocity, carrier, broken = _controls(
        parameters,
        [
            ("velocity_mps", 15, [-20, -10, 0, 10, 15, 20]),
            ("carrier_ghz", 10, [5, 10, 15]),
        ],
    )
    wavelength = C / (carrier * 1e9)
    fd = 2 * velocity / wavelength
    prf = 4000
    n = 32
    k = np.arange(n)
    time = k / prf
    clean = np.exp(1j * (np.deg2rad(25) + 2 * np.pi * fd * time))
    rng = np.random.default_rng(3601)
    received = clean + 0.1 / np.sqrt(2) * (rng.normal(size=n) + 1j * rng.normal(size=n))
    active = abs(received) if broken else received
    phase = np.angle(np.sum(np.conj(active[:-1]) * active[1:]))
    phase_fd = phase * prf / (2 * np.pi)
    unwrapped = np.unwrap(np.angle(active))
    center = time - np.mean(time)
    slope = (
        np.dot(center, unwrapped - np.mean(unwrapped))
        / np.dot(center, center)
        / (2 * np.pi)
    )
    axis = np.fft.fftshift(np.fft.fftfreq(n, 1 / prf))
    spectrum = np.fft.fftshift(np.fft.fft(active * np.hanning(n)))
    peak = axis[np.argmax(abs(spectrum))]
    counts = np.array([8, 16, 32, 64])
    vs = np.array([-20, -10, 0, 10, 20])
    cs = np.array([5, 10, 15])
    values = {
        "true_doppler": (fd, "Hz"),
        "true_phase_increment": (2 * np.pi * fd / prf, "rad/pulse"),
        "active_phase_doppler": (phase_fd, "Hz"),
        "active_slope_doppler": (slope, "Hz"),
        "active_fft_doppler": (peak, "Hz"),
        "active_velocity": (phase_fd * wavelength / 2, "m/s"),
        "velocity_limit": (wavelength * prf / 4, "m/s"),
        "fft_bin_spacing": (prf / n, "Hz"),
        "model_valid": (not broken, "boolean"),
    }
    plots = {
        "iq": _plot(
            "A coherent phasor retains direction",
            "I (relative)",
            "Q (relative)",
            [("Received", np.real(active), np.imag(active))],
        ),
        "phase": _plot(
            "Approaching motion is positive phase progression",
            "Slow time (ms)",
            "Unwrapped phase (rad)",
            [
                ("Active", time * 1000, unwrapped),
                ("Clean", time * 1000, np.unwrap(np.angle(clean))),
            ],
        ),
        "spectrum": _plot(
            "Magnitude-only processing collapses Doppler toward DC",
            "Doppler (Hz)",
            "Normalized magnitude (dB)",
            [("Active FFT", axis, _db(spectrum / max(abs(spectrum))))],
        ),
        "velocity_sweep": _plot(
            "Signed velocity changes signed Doppler",
            "Velocity (m/s)",
            "Doppler (Hz)",
            [("fd=2v/λ", vs, 2 * vs / wavelength)],
        ),
        "carrier_sweep": _plot(
            "Same velocity at different wavelengths",
            "Carrier (GHz)",
            "Doppler (Hz)",
            [("Doppler", cs, 2 * velocity * cs * 1e9 / C)],
        ),
        "count_sweep": _plot(
            "Longer dwell gives closer Doppler bins",
            "Pulse count (pulses)",
            "Doppler spacing (Hz)",
            [("PRF/N", counts, prf / counts)],
        ),
    }
    count_peaks = []
    for count in counts:
        sequence = np.exp(
            1j * (np.deg2rad(25) + 2 * np.pi * fd * np.arange(count) / prf)
        )
        transformed = np.fft.fftshift(np.fft.fft(sequence * np.hanning(count)))
        count_peaks.append(
            np.fft.fftshift(np.fft.fftfreq(count, 1 / prf))[np.argmax(abs(transformed))]
        )
    plots["count_peaks"] = _plot(
        "Finite FFT peak versus physical Doppler",
        "Pulse count (pulses)",
        "Doppler (Hz)",
        [("FFT peak", counts, count_peaks), ("True", counts, np.full(len(counts), fd))],
    )
    return _finish(
        values,
        plots,
        "Complex samples preserve pulse-to-pulse phase. Adjacent products, an unwrapped phase slope and a windowed FFT estimate signed Doppler; frequencies outside ±PRF/2 alias.",
        "Taking magnitude first erases phase: adjacent-product Doppler becomes zero and the FFT peaks at DC.",
        "Disable the failure to restore coherent I/Q and the identical private-seed samples.",
        3601,
        broken,
        pulse_count=n,
    )
