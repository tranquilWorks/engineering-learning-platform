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
    velocity, prf_khz, broken = _controls(
        parameters,
        [
            ("slow_target_velocity_mps", 3, [-15, -3, 0, 3, 15]),
            ("prf_khz", 5, [3, 4, 5, 7, 9]),
        ],
    )
    prf = prf_khz * 1000
    wavelength = C / 1e10
    rows = 128
    columns = 64
    fast = np.arange(rows)
    slow = np.arange(columns) / prf
    clutter = np.zeros(rows, complex)
    for b, a, phase in zip([24, 62, 99], [20, 12, 8], [0, 50, -35]):
        clutter += (
            a * np.exp(1j * np.deg2rad(phase)) * np.exp(-0.5 * ((fast - b) / 1.8) ** 2)
        )
    clutter_matrix = np.repeat(clutter[:, None], columns, axis=1)
    components = []
    for b, v, a, phase in zip([62, 91], [velocity, 15], [1, 0.8], [25, -45]):
        components.append(
            np.exp(-0.5 * ((fast - b) / 1.2) ** 2)[:, None]
            * a
            * np.exp(1j * (np.deg2rad(phase) + 2 * np.pi * 2 * v / wavelength * slow))[
                None, :
            ]
        )
    rng = np.random.default_rng(3801)
    noise = (
        0.08
        / np.sqrt(2)
        * (rng.normal(size=(rows, columns)) + 1j * rng.normal(size=(rows, columns)))
    )
    data = clutter_matrix + sum(components) + noise
    two = data[:, 1:] - data[:, :-1]
    three = data[:, 2:] - 2 * data[:, 1:-1] + data[:, :-2]
    wrong = data[1:] - data[:-1]
    active = wrong if broken else two
    rms = lambda a: np.sqrt(np.mean(abs(a) ** 2))
    noise2 = noise[:, 1:] - noise[:, :-1]
    noise3 = noise[:, 2:] - 2 * noise[:, 1:-1] + noise[:, :-2]
    target = components[0]
    gain2 = rms(target[:, 1:] - target[:, :-1]) / rms(target)
    gain3 = rms(target[:, 2:] - 2 * target[:, 1:-1] + target[:, :-2]) / rms(target)
    residual = (
        rms(clutter_matrix[1:] - clutter_matrix[:-1]) / rms(clutter_matrix)
        if broken
        else 0
    )
    values = {
        "active_clutter_residual": (residual, "ratio"),
        "slow_target_two_gain": (gain2, "amplitude ratio"),
        "slow_target_three_gain": (gain3, "amplitude ratio"),
        "two_noise_power_gain": (rms(noise2) ** 2 / rms(noise) ** 2, "power ratio"),
        "three_noise_power_gain": (rms(noise3) ** 2 / rms(noise) ** 2, "power ratio"),
        "two_noise_theory": (2, "power ratio"),
        "three_noise_theory": (6, "power ratio"),
        "blind_speed_spacing": (wavelength * prf / 2, "m/s"),
        "active_output_rows": (active.shape[0], "rows"),
        "active_output_columns": (active.shape[1], "pulses"),
        "model_valid": (not broken, "boolean"),
    }
    ra = fast * C / 40e6
    freq = np.linspace(-prf, prf, 1001)
    h = 1 - np.exp(-2j * np.pi * freq / prf)
    vs = np.array([-30, -15, -3, 0, 3, 15, 30])
    ps = np.array([3, 4, 5, 7, 9])
    active_axis = (ra[1:] + ra[:-1]) / 2 if broken else ra
    plots = {
        "scene": _heat(
            "Strong stationary clutter and moving targets",
            np.arange(columns),
            ra,
            _db(data),
            "Pulse (index)",
            "Range (m)",
        ),
        "profiles": _plot(
            "Slow-time subtraction suppresses stationary clutter",
            "Range (m)",
            "RMS amplitude (relative)",
            [
                ("Input", ra, np.sqrt(np.mean(abs(data) ** 2, axis=1))),
                ("Two pulse", ra, np.sqrt(np.mean(abs(two) ** 2, axis=1))),
                ("Three pulse", ra, np.sqrt(np.mean(abs(three) ** 2, axis=1))),
                ("Active", active_axis, np.sqrt(np.mean(abs(active) ** 2, axis=1))),
            ],
        ),
        "response": _plot(
            "Periodic Doppler nulls",
            "Doppler (Hz)",
            "Amplitude gain (ratio)",
            [("1-z^-1", freq, abs(h)), ("(1-z^-1)^2", freq, abs(h) ** 2)],
        ),
        "velocity_sweep": _plot(
            "The deeper DC notch also removes slow targets",
            "Velocity (m/s)",
            "Amplitude gain (ratio)",
            [
                ("Two pulse", vs, 2 * abs(np.sin(np.pi * 2 * vs / wavelength / prf))),
                ("Three pulse", vs, 4 * np.sin(np.pi * 2 * vs / wavelength / prf) ** 2),
            ],
        ),
        "prf_sweep": _plot(
            "Same 12 m/s target, different sample spacing",
            "PRF (kHz)",
            "Amplitude gain (ratio)",
            [
                (
                    "Two pulse",
                    ps,
                    2 * abs(np.sin(np.pi * 24 / wavelength / (ps * 1000))),
                ),
                (
                    "Three pulse",
                    ps,
                    4 * np.sin(np.pi * 24 / wavelength / (ps * 1000)) ** 2,
                ),
            ],
        ),
        "noise": _plot(
            "Amplitude gain must be compared with noise cost",
            "Canceller order (differences)",
            "Noise power gain (ratio)",
            [
                ("Theory", [1, 2], [2, 6]),
                (
                    "Measured",
                    [1, 2],
                    [
                        values["two_noise_power_gain"][0],
                        values["three_noise_power_gain"][0],
                    ],
                ),
            ],
        ),
    }
    selected_velocities = np.array([velocity, 15])
    selected_gain = 2 * abs(np.sin(np.pi * 2 * selected_velocities / wavelength / prf))
    plots["target_snr"] = _plot(
        "Signal amplification is not automatically SNR gain",
        "Target velocity (m/s)",
        "Output / input SNR (dB)",
        [
            (
                "Two pulse",
                selected_velocities,
                10 * np.log10(np.maximum(selected_gain**2 / 2, 1e-12)),
            ),
            (
                "Three pulse",
                selected_velocities,
                10 * np.log10(np.maximum(selected_gain**4 / 6, 1e-12)),
            ),
        ],
    )
    return _finish(
        values,
        plots,
        "[1,-1] and [1,-2,1] operate across coherent pulse columns. Stationary clutter cancels, while white-noise power grows by two and six. Valid outputs have N-1 and N-2 looks.",
        "The failure differences neighboring range rows. Clutter varies across range, so its edges survive and the output has the wrong shape.",
        "Disable the failure to restore slow-time subtraction, correct output axes and the original seeded scene.",
        3801,
        broken,
        fast_time_samples=rows,
        pulse_count=columns,
    )
