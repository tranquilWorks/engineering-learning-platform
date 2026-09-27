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


def _sidelobes(response):
    a = abs(response)
    i = int(np.argmax(a))
    left = i - 1
    right = i + 1
    while left > 0 and a[left - 1] < a[left]:
        left -= 1
    while right < len(a) - 1 and a[right + 1] < a[right]:
        right += 1
    return 20 * np.log10(max(np.max(a[:left]), np.max(a[right + 1 :])) / a[i])


def run(parameters):
    alpha, separation, broken = _controls(
        parameters,
        [
            ("taper_strength", 1, [0, 0.5, 1]),
            ("separation_samples", 17, [7, 13, 17, 32]),
        ],
    )
    fs = 40e6
    n = 400
    t = (np.arange(n) - (n - 1) / 2) / fs
    pulse = np.exp(1j * np.pi * 8e6 / 10e-6 * t * t)
    hann = 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(n) / (n - 1))
    weights = (1 - alpha) + alpha * hann
    active_weights = hann if broken else weights
    sep = 7 if broken else int(separation)
    delay = round(2 * 2400 / C * fs)
    strong = np.zeros(1600, complex)
    weak = strong.copy()
    strong[delay : delay + n] = pulse
    weak[delay + sep : delay + sep + n] = 0.04 * pulse
    rng = np.random.default_rng(3301)
    noise = 0.12 / np.sqrt(2) * (rng.normal(size=1600) + 1j * rng.normal(size=1600))
    rect = np.convolve(strong, np.conj(pulse[::-1]))
    tapered = np.convolve(strong, np.conj((pulse * active_weights)[::-1]))
    response = np.convolve(
        strong + weak + noise, np.conj((pulse * active_weights)[::-1])
    )
    clean = np.convolve(strong + weak, np.conj((pulse * active_weights)[::-1]))
    index = delay + sep + n - 1
    margin = 20 * np.log10(0.04 * sum(active_weights) / abs(tapered[index]))
    spacing = C / (2 * fs)
    snr_loss = 10 * np.log10(sum(active_weights) ** 2 / (n * sum(active_weights**2)))
    metrics = []
    for a in [0, 0.5, 1]:
        w = 1 - a + a * hann
        r = np.convolve(strong, np.conj((pulse * w)[::-1]))
        metrics.append(
            (
                _width(r, spacing),
                _sidelobes(r),
                10 * np.log10(sum(w) ** 2 / (n * sum(w * w))),
            )
        )
    values = {
        "rectangular_width": (_width(rect, spacing), "m"),
        "active_width": (_width(tapered, spacing), "m"),
        "rectangular_pslr": (_sidelobes(rect), "dB"),
        "active_pslr": (_sidelobes(tapered), "dB"),
        "active_snr_loss": (snr_loss, "dB"),
        "active_visibility_margin": (margin, "dB"),
        "weak_local_peak": (
            abs(clean[index]) > max(abs(clean[index - 1]), abs(clean[index + 1])),
            "boolean",
        ),
        "active_separation": (sep * spacing, "m"),
        "noisy_weak_bin": (abs(response[index]) / sum(active_weights), "relative"),
        "model_valid": (not broken, "boolean"),
    }
    axis = (np.arange(len(rect)) - (n - 1)) * spacing
    view = (axis > 2300) & (axis < 2550)
    separations = np.array([7, 13, 17, 32])
    full_hann = np.convolve(strong, np.conj((pulse * hann)[::-1]))
    plots = {
        "weights": _plot(
            "Receive weighting only",
            "Pulse sample (index)",
            "Weight (ratio)",
            [
                ("Active", np.arange(n), active_weights),
                ("Rectangular", np.arange(n), np.ones(n)),
            ],
        ),
        "isolated": _plot(
            "Sidelobes and mainlobe width",
            "Range (m)",
            "Magnitude relative to own peak (dB)",
            [
                ("Rectangular", axis[view], _db(rect[view] / n)),
                ("Active taper", axis[view], _db(tapered[view] / sum(active_weights))),
            ],
        ),
        "scene": _plot(
            "Can the weak target clear strong-target leakage?",
            "Range (m)",
            "Magnitude relative to strong peak (dB)",
            [
                ("Noisy scene", axis[view], _db(response[view] / sum(active_weights))),
                ("Clean scene", axis[view], _db(clean[view] / sum(active_weights))),
                (
                    "Rectangular scene",
                    axis[view],
                    _db(
                        np.convolve(strong + weak + noise, np.conj(pulse[::-1]))[view]
                        / n
                    ),
                ),
            ],
        ),
        "taper_width": _plot(
            "Taper broadens the mainlobe",
            "Taper strength (ratio)",
            "Width (m)",
            [("Width", [0, 0.5, 1], [m[0] for m in metrics])],
        ),
        "taper_cost": _plot(
            "Sidelobe reduction has a noise cost",
            "Taper strength (ratio)",
            "Relative power (dB)",
            [
                ("PSLR", [0, 0.5, 1], [m[1] for m in metrics]),
                ("SNR change", [0, 0.5, 1], [m[2] for m in metrics]),
            ],
        ),
        "separation_sweep": _plot(
            "Width can mask a close target despite low sidelobes",
            "Separation (m)",
            "Weak / leakage margin (dB)",
            [
                (
                    "Rectangular",
                    separations * spacing,
                    20 * np.log10(0.04 * n / abs(rect[delay + n - 1 + separations])),
                ),
                (
                    "Hann",
                    separations * spacing,
                    20
                    * np.log10(
                        0.04 * sum(hann) / abs(full_hann[delay + n - 1 + separations])
                    ),
                ),
            ],
        ),
    }
    return _finish(
        values,
        plots,
        "Cosine receive weighting lowers sidelobes while broadening the mainlobe and losing output SNR. Weak-target margin compares its peak with strong-target leakage.",
        "The failure forces full Hann weighting and seven-sample separation: low sidelobes alone do not reveal a target inside the broadened response.",
        "Disable the failure and restore 17-sample separation with full taper; inspect margin, local peak and width together.",
        3301,
        broken,
        record_samples=1600,
        pulse_samples=400,
    )
