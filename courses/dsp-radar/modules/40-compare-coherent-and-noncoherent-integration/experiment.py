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


def run(parameters):
    count, snr, broken = _controls(
        parameters,
        [
            ("pulse_count", 32, [4, 8, 16, 32, 64]),
            ("input_snr_db", -8, [-16, -8, 0, 8]),
        ],
    )
    n = int(count)
    rho = 10 ** (snr / 10)
    noise_power = 1 / rho
    k = np.arange(n)
    phase = np.deg2rad(25 + 35 * k)
    reference = np.exp(1j * phase)
    rng = np.random.default_rng(4001)
    noise = np.sqrt(noise_power / 2) * (rng.normal(size=n) + 1j * rng.normal(size=n))
    observed = reference + noise
    aligned = observed * np.conj(reference)
    cumulative = np.cumsum(aligned)
    power_sum = np.cumsum(abs(observed) ** 2)
    cycle = np.deg2rad(np.resize([0, 90, 180, -90], n))
    bad = reference * np.exp(1j * cycle)
    active = bad * np.conj(reference) if broken else np.ones(n, complex)
    recovered = bad * np.conj(reference) * np.exp(-1j * cycle)
    active_fraction = abs(sum(active)) ** 2 / n**2
    recovered_fraction = abs(sum(recovered)) ** 2 / n**2
    values = {
        "coherent_output_snr": (10 * np.log10(n * rho), "dB"),
        "coherent_detectability": (n * rho, "noise std"),
        "noncoherent_detectability": (np.sqrt(n) * rho, "noise std"),
        "active_signal_power_fraction": (active_fraction, "ratio"),
        "recovered_signal_power_fraction": (recovered_fraction, "ratio"),
        "noncoherent_signal_energy_fraction": (np.mean(abs(bad) ** 2), "ratio"),
        "observed_coherent_statistic": (abs(cumulative[-1]) ** 2, "relative power"),
        "observed_noncoherent_statistic": (power_sum[-1], "relative power"),
        "jitter_90deg_effective_gain": (
            1 + (n - 1) * np.exp(-((np.pi / 2) ** 2)),
            "ratio",
        ),
        "model_valid": (not broken, "boolean"),
    }
    counts = np.array([1, 2, 4, 8, 16, 32, 64])
    jitter = np.array([0, 5, 15, 30, 60, 90, 120, 180])
    gain = 1 + (n - 1) * np.exp(-(np.deg2rad(jitter) ** 2))
    plots = {
        "iq": _plot(
            "Align a trustworthy phase reference before summing",
            "I (relative)",
            "Q (relative)",
            [
                ("Raw", observed.real, observed.imag),
                ("Aligned", aligned.real, aligned.imag),
            ],
        ),
        "coherent_path": _plot(
            "Cumulative complex sum",
            "Sum I (relative)",
            "Sum Q (relative)",
            [("Cumulative", cumulative.real, cumulative.imag)],
        ),
        "power": _plot(
            "Power sums contain positive noise energy",
            "Integrated pulses (count)",
            "Power statistic (relative)",
            [
                ("Observed", k + 1, power_sum),
                ("Noise-only mean", k + 1, (k + 1) * noise_power),
                ("Target-present mean", k + 1, (k + 1) * (1 + noise_power)),
            ],
        ),
        "count_snr": _plot(
            "Stable-phase coherent gain",
            "Pulse count (pulses)",
            "Output SNR (dB)",
            [("Coherent", counts, 10 * np.log10(counts * rho))],
        ),
        "detectability": _plot(
            "Compare noise-standardized mean separations",
            "Pulse count (pulses)",
            "Detectability (noise std)",
            [
                ("Coherent power", counts, counts * rho),
                ("Noncoherent power", counts, np.sqrt(counts) * rho),
            ],
        ),
        "jitter": _plot(
            "Independent Gaussian phase jitter removes cross terms",
            "Jitter std (deg)",
            "Normalized signal power (ratio)",
            [
                ("Coherent expectation", jitter, gain / n),
                ("Noncoherent energy", jitter, np.ones(len(jitter))),
            ],
        ),
        "failure": _plot(
            "Quadrature cancellation and known-error recovery",
            "Case: active, tracked, power (index)",
            "Signal fraction (ratio)",
            [
                (
                    "Fraction",
                    [0, 1, 2],
                    [active_fraction, recovered_fraction, np.mean(abs(bad) ** 2)],
                )
            ],
        ),
    }
    return _finish(
        values,
        plots,
        "Known phase alignment gives coherent SNR Nρ. Noncoherent power has a different distribution: its standardized separation is √Nρ. The Gaussian-jitter sweep is an ensemble expectation.",
        "The prescribed 0°,90°,180°,-90° error cycle cancels the clean nominally aligned sum while preserving pulse energy. It is not a typical random-jitter realization.",
        "Track and derotate the actual pulse errors to restore unit coherent signal fraction; disable the demonstration to replay the baseline. Recovery assumes known phase errors.",
        4001,
        broken,
        pulse_count=n,
    )
