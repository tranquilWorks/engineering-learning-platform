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


def _gaussian_case(bandwidth, separation):
    fs = 80e6
    sigma = np.sqrt(np.log(2)) / (np.pi * bandwidth)
    half = int(np.ceil(4 * sigma * fs))
    pulse = np.exp(-0.5 * (np.arange(-half, half + 1) / fs / sigma) ** 2)
    pulse /= np.linalg.norm(pulse)
    first = _echo(pulse, 960, 2 * 900.37 / C * fs)
    second = _echo(pulse, 960, 2 * (900.37 + separation) / C * fs)
    clean = np.correlate(first, pulse, "valid")
    rng = np.random.default_rng(3101)
    noise = rng.normal(size=960)
    sigma_noise = max(clean) / 10**2.5
    pair = np.correlate(first + second + sigma_noise * noise, pulse, "valid")
    single = np.correlate(first + sigma_noise * noise, pulse, "valid")
    axis = np.arange(len(clean)) * C / (2 * fs)
    above = np.flatnonzero(abs(clean) >= max(abs(clean)) / np.sqrt(2))
    width = (above[-1] - above[0]) * C / (2 * fs)
    return pulse, first, clean, pair, single, axis, width, rng


def run(parameters):
    bandwidth, spacing, broken = _controls(
        parameters,
        [("bandwidth_mhz", 4, [2, 4, 8]), ("target_separation_m", 22, [10, 22, 45])],
    )
    pulse, first, clean, pair, single, axis, width, rng = _gaussian_case(
        bandwidth * 1e6, spacing
    )
    peaks = _peaks(pair)
    gate = np.flatnonzero(abs(axis - 900.37) <= 80)
    peak = gate[np.argmax(abs(single[gate]))]
    refined = _refine(single, peak) * C / 160e6
    noises = rng.normal(size=(128, 960))
    snrs = [0, 15, 30]
    errors = []
    for snr in snrs:
        estimates = []
        for noise in noises:
            response = np.correlate(
                first + max(clean) / 10 ** (snr / 20) * noise, pulse, "valid"
            )
            i = gate[np.argmax(abs(response[gate]))]
            estimates.append(_refine(response, i) * C / 160e6)
        errors.append(np.array(estimates) - 900.37)
    fine = np.linspace(axis[0], axis[-1], (len(axis) - 1) * 16 + 1)
    display = np.interp(fine, axis, abs(pair))
    g = np.flatnonzero((fine >= 820.37) & (fine <= 980.37 + spacing))
    top = g[np.argsort(display[g], kind="stable")[-2:]]
    false_separation = abs(fine[top[1]] - fine[top[0]])
    bandwidth_cases = [_gaussian_case(b * 1e6, spacing) for b in [2, 4, 8]]
    separation_cases = [_gaussian_case(bandwidth * 1e6, s) for s in [10, 22, 45]]
    values = {
        "nominal_range_scale": (C / (2 * bandwidth * 1e6), "m"),
        "measured_response_width": (width, "m"),
        "physical_peak_count": (len(peaks), "count"),
        "active_claimed_count": (2 if broken else len(peaks), "count"),
        "false_display_separation": (false_separation, "m"),
        "integer_error": (axis[peak] - 900.37, "m"),
        "refined_error": (refined - 900.37, "m"),
        "low_snr_rmse": (np.sqrt(np.mean(errors[0] ** 2)), "m"),
        "high_snr_rmse": (np.sqrt(np.mean(errors[2] ** 2)), "m"),
        "wideband_peak_count": (len(_peaks(bandwidth_cases[-1][3])), "count"),
        "model_valid": (not broken, "boolean"),
    }
    view = (axis > 780) & (axis < 1050)
    plots = {
        "pair": _plot(
            "Count physical peaks, not adjacent display points",
            "Range (m)",
            "Matched magnitude (relative)",
            [
                ("Pair", axis[view], abs(pair)[view]),
                ("Single response", axis[view], abs(clean)[view]),
            ],
        ),
        "bandwidth_sweep": _plot(
            "Bandwidth changes width",
            "Bandwidth (MHz)",
            "Response width (m)",
            [
                ("Measured", [2, 4, 8], [c[6] for c in bandwidth_cases]),
                ("Nominal c/2B", [2, 4, 8], C / (2 * np.array([2, 4, 8]) * 1e6)),
            ],
        ),
        "separation_sweep": _plot(
            "Actual separation creates distinct peaks",
            "Separation (m)",
            "Physical maxima (count)",
            [("Peaks", [10, 22, 45], [len(_peaks(c[3])) for c in separation_cases])],
        ),
        "accuracy": _plot(
            "Accuracy improves while waveform width stays fixed",
            "Matched SNR (dB)",
            "Distance (m)",
            [
                ("RMSE", snrs, [np.sqrt(np.mean(e**2)) for e in errors]),
                ("Std deviation", snrs, [np.std(e, ddof=1) for e in errors]),
                ("Bias", snrs, [np.mean(e) for e in errors]),
                ("Response width", snrs, [width] * 3),
            ],
        ),
        "display": _plot(
            "Dense interpolation adds no independent information",
            "Range (m)",
            "Magnitude (relative)",
            [
                (
                    "Interpolated",
                    fine[(fine > 870) & (fine < 960 + spacing)],
                    display[(fine > 870) & (fine < 960 + spacing)],
                )
            ],
        ),
    }
    return _finish(
        values,
        plots,
        "A unit-energy Gaussian pulse separates matched-response width from isolated-target bias, standard deviation and RMSE over 128 trials.",
        "Selecting the two largest adjacent interpolated samples invents a second target within one crest.",
        "Disable the false count; count physical local maxima. Increase actual bandwidth to 8 MHz to resolve the baseline 22 m pair.",
        3101,
        broken,
        trial_count=128,
        record_samples=960,
    )
