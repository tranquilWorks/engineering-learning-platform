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


def _lfm(bandwidth, duration):
    n = round(duration * 40e6)
    t = (np.arange(n) - (n - 1) / 2) / 40e6
    return np.exp(1j * np.pi * bandwidth / duration * t * t)


def run(parameters):
    bandwidth, duration, broken = _controls(
        parameters,
        [("bandwidth_mhz", 8, [4, 8, 16]), ("pulse_duration_us", 10, [5, 10, 20])],
    )
    fs = 40e6
    b = bandwidth * 1e6
    t = duration * 1e-6
    pulse = _lfm(b, t)
    n = len(pulse)
    delay = round(2 * 2400 / C * fs)
    second = round(2 * 2475 / C * fs)
    first = np.zeros(1600, complex)
    other = first.copy()
    first[delay : delay + n] = pulse
    other[second : second + n] = 0.65 * pulse
    rng = np.random.default_rng(3201)
    noise = 2 / np.sqrt(2) * (rng.normal(size=1600) + 1j * rng.normal(size=1600))
    replica = _lfm(0.55 * b, t) if broken else pulse
    h = np.conj(replica[::-1])
    matched = np.convolve(first + other + noise, h)
    isolated = np.convolve(first, h)
    correct = np.convolve(first, np.conj(pulse[::-1]))
    nr = np.convolve(noise, np.conj(pulse[::-1]))
    out_noise = np.mean(abs(nr[n - 1 : 1600]) ** 2)
    output_snr = 10 * np.log10(max(abs(correct)) ** 2 / out_noise)
    input_inband = 10 * np.log10(1 / (4 * b / fs))
    spacing = C / (2 * fs)
    values = {
        "time_bandwidth": (b * t, "ratio"),
        "raw_range_extent": (C * t / 2, "m"),
        "nominal_resolution": (C / (2 * b), "m"),
        "correct_width": (_width(correct, spacing), "m"),
        "active_width": (_width(isolated, spacing), "m"),
        "active_peak_loss": (
            20 * np.log10(max(abs(isolated)) / max(abs(correct))),
            "dB",
        ),
        "predicted_bt_gain": (10 * np.log10(b * t), "dB"),
        "measured_bt_gain": (output_snr - input_inband, "dB"),
        "sampled_gain": (10 * np.log10(n), "dB"),
        "model_valid": (not broken, "boolean"),
    }
    axis = (np.arange(len(matched)) - (n - 1)) * spacing
    view = (axis > 2200) & (axis < 2700)
    bs = np.array([4, 8, 16])
    ts = np.array([5, 10, 20])
    width_for = lambda bb, tt: _width(
        np.convolve(_lfm(bb, tt), np.conj(_lfm(bb, tt)[::-1])), spacing
    )
    plots = {
        "chirp": _plot(
            "LFM has constant magnitude and rotating phase",
            "Pulse time (µs)",
            "Amplitude (relative)",
            [
                ("I", np.arange(n) / fs * 1e6, pulse.real),
                ("Q", np.arange(n) / fs * 1e6, pulse.imag),
            ],
        ),
        "frequency": _plot(
            "Frequency labels time inside the pulse",
            "Pulse time (µs)",
            "Instantaneous frequency (MHz)",
            [
                (
                    "Frequency",
                    np.arange(n) / fs * 1e6,
                    b / t * (np.arange(n) - (n - 1) / 2) / fs / 1e6,
                )
            ],
        ),
        "raw": _plot(
            "Long raw echoes overlap",
            "Fast time (µs)",
            "Echo magnitude (relative)",
            [
                ("Clean", np.arange(1600) / fs * 1e6, abs(first + other)),
                ("Noisy", np.arange(1600) / fs * 1e6, abs(first + other + noise)),
            ],
        ),
        "compression": _plot(
            "Delay-corrected matched output",
            "Range (m)",
            "Magnitude relative to exact peak (dB)",
            [
                ("Noisy pair", axis[view], _db(matched[view] / n)),
                ("Active isolated", axis[view], _db(isolated[view] / n)),
                ("Exact replica", axis[view], _db(correct[view] / n)),
            ],
        ),
        "bandwidth_sweep": _plot(
            "Bandwidth sets compressed width",
            "Bandwidth (MHz)",
            "Width (m)",
            [("Width", bs, [width_for(v * 1e6, t) for v in bs])],
        ),
        "duration_width": _plot(
            "Duration changes energy at fixed bandwidth",
            "Duration (µs)",
            "Width (m)",
            [("Width", ts, [width_for(b, v * 1e-6) for v in ts])],
        ),
        "duration_gain": _plot(
            "Gain referenced to B-Hz input noise",
            "Duration (µs)",
            "BT gain (dB)",
            [("Gain", ts, 10 * np.log10(b * ts * 1e-6))],
        ),
    }
    return _finish(
        values,
        plots,
        "The conjugate-reversed chirp compresses long overlapping echoes. Bandwidth sets width; duration supplies energy. FsT and BT use different input-noise references.",
        "A 0.55B replica leaves phase mismatch: the isolated peak loses height and broadens on the same reference scale.",
        "Disable the failure to use the exact transmitted replica and reproduce the baseline seeded record.",
        3201,
        broken,
        record_samples=1600,
        pulse_samples=n,
    )
