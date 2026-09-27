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


def _echo(pulse, count, delay):
    # Zero-extended piecewise-linear interpolation includes the two edge ramps.
    indices = np.arange(count) - delay
    return np.interp(
        indices, np.arange(-1, len(pulse) + 1), np.r_[0, pulse, 0], left=0, right=0
    )


def _refine(a, index=None):
    a = np.abs(a)
    i = int(np.argmax(a)) if index is None else int(index)
    if not 0 < i < len(a) - 1:
        raise ValueError("Peak needs two neighbors")
    d = a[i - 1] - 2 * a[i] + a[i + 1]
    return i + (
        np.clip(0.5 * (a[i - 1] - a[i + 1]) / d, -0.5, 0.5) if d < -1e-10 else 0
    )


def _peaks(a, ratio=0.35):
    a = np.abs(a)
    return (
        np.flatnonzero(
            (a[1:-1] > a[:-2]) & (a[1:-1] >= a[2:]) & (a[1:-1] >= ratio * max(a))
        )
        + 1
    )


def _range_case(fs, delay, noise=False):
    pulse = np.ones(round(fs * 1e-6))
    count = round(fs * 16e-6)
    echo = _echo(pulse, count, delay * fs)
    received = (
        echo + 0.03 * np.random.default_rng(3001).normal(size=count) if noise else echo
    )
    correlation = np.array(
        [
            np.dot(received[k : k + len(pulse)], pulse)
            for k in range(count - len(pulse) + 1)
        ]
    )
    return (
        pulse,
        echo,
        received,
        correlation,
        int(np.argmax(abs(correlation))),
        _refine(correlation),
    )


def run(parameters):
    rate, delay_us, broken = _controls(
        parameters,
        [
            ("sample_rate_mhz", 20, [10, 20, 40]),
            ("delay_us", 6.0175, [6, 6.0125, 6.0175, 6.025, 6.0375]),
        ],
    )
    fs = rate * 1e6
    delay = delay_us * 1e-6
    pulse, echo, received, corr, integer, refined = _range_case(fs, delay, True)
    true = C * delay / 2
    estimated = C * refined / (2 * fs)
    rates = np.array([10, 20, 40])
    cases = [_range_case(r * 1e6, delay) for r in rates]
    fractions = np.array([0, 0.25, 0.5, 0.75])
    fraction_cases = [_range_case(fs, (120 + v) / fs) for v in fractions]
    pairs = []
    counts = []
    for sep in [0.5, 1, 1.5]:
        record = echo + 0.65 * _echo(pulse, len(echo), (delay + sep * 1e-6) * fs)
        response = np.convolve(record, pulse[::-1], mode="valid")
        pairs.append(
            (f"Separation {sep} µs", np.arange(len(response)) * C / (2 * fs), response)
        )
        counts.append(len(_peaks(response, 0.25)))
    values = {
        "true_range": (true, "m"),
        "integer_range": (C * integer / (2 * fs), "m"),
        "refined_range": (estimated, "m"),
        "active_reported_range": (estimated * (2 if broken else 1), "m"),
        "range_sample_step": (C / (2 * fs), "m"),
        "refined_error": (estimated - true, "m"),
        "peak": (max(corr), "amplitude sum"),
        "close_pair_peaks": (counts[0], "count"),
        "wide_pair_peaks": (counts[-1], "count"),
        "model_valid": (not broken, "boolean"),
    }
    plots = {
        "echo": _plot(
            "Sample the continuous delay before locating its peak",
            "Fast time (µs)",
            "Amplitude (relative)",
            [
                ("Received", np.arange(len(echo)) / fs * 1e6, received),
                ("Clean echo", np.arange(len(echo)) / fs * 1e6, echo),
            ],
        ),
        "pulse": _plot(
            "Finite transmitted pulse",
            "Pulse time (µs)",
            "Amplitude (relative)",
            [("Pulse", np.arange(len(pulse)) / fs * 1e6, pulse)],
        ),
        "correlation": _plot(
            "Nonnegative-lag matched sum",
            "Candidate range (m)",
            "Correlation (amplitude sum)",
            [("Matched output", np.arange(len(corr)) * C / (2 * fs), corr)],
        ),
        "rate_sweep": _plot(
            "Sampling changes the grid",
            "Sample rate (MHz)",
            "Range error (m)",
            [
                (
                    "Integer",
                    rates,
                    [C * c[4] / (2 * r * 1e6) - true for c, r in zip(cases, rates)],
                ),
                (
                    "Refined",
                    rates,
                    [C * c[5] / (2 * r * 1e6) - true for c, r in zip(cases, rates)],
                ),
            ],
        ),
        "fraction_sweep": _plot(
            "A staircase versus a local peak fit",
            "Fractional delay (samples)",
            "Delay error (samples)",
            [
                (
                    "Integer",
                    fractions,
                    [c[4] - 120 - f for c, f in zip(fraction_cases, fractions)],
                ),
                (
                    "Refined",
                    fractions,
                    [c[5] - 120 - f for c, f in zip(fraction_cases, fractions)],
                ),
            ],
        ),
        "separation": _plot(
            "A finer grid does not narrow the pulse",
            "Range (m)",
            "Correlation (amplitude sum)",
            pairs,
        ),
        "ranging": _plot(
            "Round-trip geometry",
            "Method: true, refined, active (index)",
            "Range (m)",
            [
                (
                    "Range",
                    [0, 1, 2],
                    [true, estimated, values["active_reported_range"][0]],
                )
            ],
        ),
    }
    return _finish(
        values,
        plots,
        "A zero-extended fractional echo is correlated with a one-microsecond pulse. Parabolic refinement locates the peak but does not add bandwidth.",
        "Using cτ reports twice the refined monostatic range.",
        "Disable the failure to restore cτ/2 with identical samples and correlation.",
        3001,
        broken,
        record_samples=len(echo),
    )
