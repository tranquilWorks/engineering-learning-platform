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


def _width(a, spacing):
    a = np.abs(a)
    peak = int(np.argmax(a))
    h = a[peak] / np.sqrt(2)
    left = right = peak
    while left > 0 and a[left] >= h:
        left -= 1
    while right < len(a) - 1 and a[right] >= h:
        right += 1
    l = left + (h - a[left]) / (a[left + 1] - a[left])
    r = right - 1 + (h - a[right - 1]) / (a[right] - a[right - 1])
    return float((r - l) * spacing)


def _ambiguity(signal, dopplers):
    n = len(signal)
    delays = np.arange(1 - n, n)
    out = np.empty((len(dopplers), len(delays)))
    for j, d in enumerate(delays):
        current = np.arange(max(0, d), min(n, n + d))
        other = current - d
        products = signal[current] * np.conj(signal[other])
        out[:, j] = (
            abs(
                np.sum(
                    products[None, :]
                    * np.exp(
                        -2j
                        * np.pi
                        * np.asarray(dopplers)[:, None]
                        * current[None, :]
                        / 1e7
                    ),
                    axis=1,
                )
            )
            / np.vdot(signal, signal).real
        )
    return out


def run(parameters):
    bandwidth, duration, broken = _controls(
        parameters,
        [("bandwidth_mhz", 3, [1.5, 3, 4.5]), ("duration_us", 13, [6.5, 13])],
    )
    n = round(duration * 10)
    time = (np.arange(n) - (n - 1) / 2) / 1e7
    rect = np.ones(n)
    lfm = np.exp(1j * np.pi * bandwidth * 1e6 / (duration * 1e-6) * time * time)
    code = 2 * (np.random.default_rng(3401).random(31) >= 0.5) - 1
    coded = np.repeat(code[:13], 10).astype(complex)
    # Code comparison keeps the source's 13-chip duration; duration control is rectangular/LFM only.
    fd = np.linspace(-200e3, 200e3, 101)
    delays = np.arange(1 - n, n) / 10
    surfaces = [_ambiguity(s, fd) for s in [rect, lfm, coded]]
    zero = 50
    cuts = [a[zero] for a in surfaces]
    code_axis = np.arange(1 - len(coded), len(coded)) / 10
    ridge = delays[np.argmax(surfaces[1], axis=1)]
    probe = 80
    active = np.ones_like(cuts[0]) if broken else cuts[0]
    pslr = 20 * np.log10(max(cuts[2][abs(code_axis) >= 1]))
    values = {
        "rectangular_delay_width": (_width(cuts[0], 0.1), "µs"),
        "lfm_delay_width": (_width(cuts[1], 0.1), "µs"),
        "code_delay_width": (_width(cuts[2], 0.1), "µs"),
        "rectangular_doppler_width": (_width(surfaces[0][:, n - 1], 4), "kHz"),
        "positive_ridge_delay": (ridge[probe], "µs"),
        "predicted_ridge_delay": (0.12 * duration / bandwidth, "µs"),
        "active_extreme_delay": (active[0], "ratio"),
        "zero_filled_extreme": (1 / n, "ratio"),
        "code_pslr": (pslr, "dB"),
        "model_valid": (not broken, "boolean"),
    }
    ds = np.array([6.5, 13, 26])
    bs = np.array([1.5, 3, 4.5])
    lengths = [7, 13, 31]
    durations = [np.ones(round(d * 10)) for d in ds]
    lfm_cases = [
        np.exp(1j * np.pi * b * 1e6 / (duration * 1e-6) * time * time) for b in bs
    ]
    plots = {
        name: _heat(
            name + " delay-Doppler magnitude",
            delays if i < 2 else code_axis,
            fd / 1000,
            _db(surfaces[i]),
            "Delay mismatch (µs)",
            "Doppler mismatch (kHz)",
        )
        for i, name in enumerate(["rectangular_surface", "lfm_surface", "code_surface"])
    }
    plots.update(
        delay_cut=_plot(
            "Zero-Doppler cut and circular-wrap failure",
            "Delay (µs)",
            "Normalized magnitude (ratio)",
            [
                ("Rectangular", delays, cuts[0]),
                ("Active rectangular", delays, active),
                ("LFM", delays, cuts[1]),
                ("Code", code_axis, cuts[2]),
            ],
        ),
        doppler_cut=_plot(
            "Zero-delay cut",
            "Doppler (kHz)",
            "Normalized magnitude (ratio)",
            [
                (name, fd / 1000, surfaces[i][:, len(s) - 1])
                for i, (name, s) in enumerate(
                    [("Rectangular", rect), ("LFM", lfm), ("Code", coded)]
                )
            ],
        ),
        ridge=_plot(
            "LFM delay and Doppler are coupled",
            "Doppler mismatch (kHz)",
            "Peak delay (µs)",
            [
                ("Measured", fd / 1000, ridge),
                (
                    "fd / chirp rate",
                    fd / 1000,
                    fd / (bandwidth * 1e6 / (duration * 1e-6)) * 1e6,
                ),
            ],
        ),
        duration_delay=_plot(
            "Duration widens delay response",
            "Duration (µs)",
            "Delay width (µs)",
            [
                (
                    "Rectangle",
                    ds,
                    [_width(_ambiguity(s, [0])[0], 0.1) for s in durations],
                )
            ],
        ),
        duration_doppler=_plot(
            "Longer duration narrows Doppler response",
            "Duration (µs)",
            "Doppler width (kHz)",
            [
                (
                    "Rectangle",
                    ds,
                    [
                        _width(
                            abs(
                                np.exp(
                                    -2j
                                    * np.pi
                                    * fd[:, None]
                                    * np.arange(len(s))[None, :]
                                    / 1e7
                                ).sum(axis=1)
                            )
                            / len(s),
                            4,
                        )
                        for s in durations
                    ],
                )
            ],
        ),
        bandwidth_sweep=_plot(
            "Bandwidth narrows the LFM delay cut",
            "Bandwidth (MHz)",
            "Delay width (µs)",
            [("LFM", bs, [_width(_ambiguity(s, [0])[0], 0.1) for s in lfm_cases])],
        ),
        code_sweep=_plot(
            "Seeded prefixes change code sidelobes",
            "Code length (chips)",
            "Peak sidelobe ratio (dB)",
            [
                (
                    "Outside one chip",
                    lengths,
                    [
                        20
                        * np.log10(
                            max(
                                _ambiguity(np.repeat(code[:k], 10), [0])[0][
                                    abs(np.arange(1 - 10 * k, 10 * k)) >= 10
                                ]
                            )
                        )
                        for k in lengths
                    ],
                )
            ],
        ),
    )
    plots["code_delay_width"] = _plot(
        "Chip length and finite-code delay width",
        "Code length (chips)",
        "Delay width (µs)",
        [
            (
                "Code",
                lengths,
                [
                    _width(_ambiguity(np.repeat(code[:k], 10), [0])[0], 0.1)
                    for k in lengths
                ],
            )
        ],
    )
    plots["code_doppler_width"] = _plot(
        "Longer code narrows Doppler cut",
        "Code length (chips)",
        "Doppler width (kHz)",
        [
            (
                "Code",
                lengths,
                [
                    _width(
                        abs(
                            np.exp(
                                -2j
                                * np.pi
                                * fd[:, None]
                                * np.arange(k * 10)[None, :]
                                / 1e7
                            ).sum(axis=1)
                        )
                        / (k * 10),
                        4,
                    )
                    for k in lengths
                ],
            )
        ],
    )
    return _finish(
        values,
        plots,
        "Delay-Doppler sums use only zero-filled overlap. Rectangle, LFM and a seeded 13-chip code expose different cuts; the LFM ridge follows fd divided by chirp rate.",
        "Circularly wrapping the rectangular pulse produces unit correlation even at extreme delay, inventing overlap that propagation cannot supply.",
        "Disable the failure to restore finite zero-filled overlap; the extreme-delay magnitude returns to 1/N.",
        3401,
        broken,
        surface_doppler_bins=101,
        surface_samples=n,
    )
