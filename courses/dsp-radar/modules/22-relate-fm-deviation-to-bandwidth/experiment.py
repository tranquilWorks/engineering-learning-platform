from __future__ import annotations

from typing import Any

import numpy as np


def _plot(title, xlabel, ylabel, traces):
    data = []
    for name, x, y in traces:
        x, y = np.asarray(x), np.asarray(y)
        indices = np.unique(np.linspace(0, len(x) - 1, min(len(x), 512)).astype(int))
        data.append(
            {
                "type": "scatter",
                "mode": "lines",
                "name": name,
                "x": x[indices].tolist(),
                "y": y[indices].tolist(),
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


def _result(signature, fields, plots, explanations, seed, broken, extra=None):
    return {
        "metrics": [
            {
                "id": fields[i][0],
                "label": fields[i][0].replace("_", " "),
                "value": float(v),
                "unit": fields[i][1],
            }
            for i, v in enumerate(signature)
        ],
        "plots": plots,
        "explanations": explanations,
        "diagnostics": {
            "signature": [float(v) for v in signature],
            "signature_fields": [f[0] for f in fields],
            "seed": seed,
            "broken_active": broken,
            **(extra or {}),
        },
    }


def _fm(deviation, message_frequency, carrier=3000.0, fs=24000.0):
    n = int(fs * 0.2)
    time = np.arange(n) / fs
    phase = 2 * np.pi * carrier * time + deviation / message_frequency * np.sin(
        2 * np.pi * message_frequency * time
    )
    phasor = np.exp(1j * phase)
    intended = carrier + deviation * np.cos(2 * np.pi * message_frequency * time)
    observed = np.r_[
        intended[0], np.angle(phasor[1:] * phasor[:-1].conj()) * fs / (2 * np.pi)
    ]
    amplitude = 2 * np.abs(np.fft.rfft(phasor.real)) / n
    amplitude[[0, -1]] /= 2
    max_order = int(min(carrier, fs / 2 - carrier) // message_frequency)
    orders = np.arange(-max_order, max_order + 1)
    power = (
        amplitude[np.rint((carrier + orders * message_frequency) / 5).astype(int)] ** 2
    )
    order = next(
        k
        for k in range(max_order + 1)
        if power[np.abs(orders) <= k].sum() >= 0.98 * power.sum()
    )
    return (
        time,
        phasor,
        intended,
        observed,
        amplitude,
        orders,
        power / power.sum(),
        2 * order * message_frequency,
    )


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    deviation = float(parameters.get("deviation_hz", 400))
    fm = float(parameters.get("message_frequency_hz", 100))
    broken = bool(parameters.get("broken_mode", False))
    if deviation not in {50, 200, 400, 800} or fm not in {50, 100, 200, 400}:
        raise ValueError("Choose a retained FM deviation and message frequency")
    selected = _fm(deviation, fm)
    failed = _fm(5000, 100, 8000)
    recovered = _fm(5000, 100, 8000, 30000)
    active = failed if broken else selected
    t, phasor, intended, observed, _amplitude, orders, power, _bandwidth = active
    alias_fraction = float(np.mean(np.abs(observed[1:] - intended[1:]) > 6000))
    signature = [
        deviation / fm,
        selected[7],
        2 * (deviation + fm),
        float(np.max(np.abs(np.abs(phasor) - 1))),
        alias_fraction,
        float(np.max(np.abs(observed[1:] - intended[1:]))),
        recovered[7],
        float(np.max(np.abs(recovered[3][1:] - recovered[2][1:]))),
        float(15000 - (8000 + recovered[7] / 2)),
    ]
    fields = [
        ("selected_modulation_index", "ratio"),
        ("selected_occupied_98_bandwidth", "Hz"),
        ("selected_carson_bandwidth", "Hz"),
        ("magnitude_error", "V"),
        ("aliased_sample_fraction", "ratio"),
        ("phase_slope_error", "Hz"),
        ("recovery_98_bandwidth", "Hz"),
        ("recovery_slope_error", "Hz"),
        ("recovery_occupied_margin", "Hz"),
    ]
    deviations, frequencies = [50, 200, 400, 800], [50, 100, 200, 400]
    noise = 0.002 * np.random.default_rng(1022).standard_normal(4800)
    noisy_spectrum = 2 * np.abs(np.fft.rfft(selected[1].real + noise)) / 4800
    plots = {
        "rf_waveform": _plot(
            "Real RF observation at the selected baseline",
            "Time (ms)",
            "Voltage (V)",
            [
                ("clean FM", 1000 * selected[0][:480], selected[1].real[:480]),
                (
                    "seeded received RF",
                    1000 * selected[0][:480],
                    selected[1].real[:480] + noise[:480],
                ),
            ],
        ),
        "phase_slope": _plot(
            "Intended and sampled phase slope",
            "Time (ms)",
            "Frequency (Hz)",
            [
                ("intended", 1000 * t[:480], intended[:480]),
                ("observed", 1000 * t[:480], observed[:480]),
                ("30 kHz recovery", 1000 * recovered[0][:600], recovered[3][:600]),
            ],
        ),
        "magnitude": _plot(
            "FM keeps constant phasor magnitude",
            "Time (ms)",
            "Magnitude (V)",
            [("active phasor", 1000 * t[:480], np.abs(phasor[:480]))],
        ),
        "spectrum": _plot(
            "Noisy baseline RF spectrum",
            "RF frequency (Hz)",
            "Amplitude (V)",
            [("received", np.arange(300, 901) * 5, noisy_spectrum[300:901])],
        ),
        "sideband_power": _plot(
            "Retained line-power ladder",
            "Sideband order (integer)",
            "Power fraction (ratio)",
            [("active lines", orders, power)],
        ),
        "deviation_sweep": _plot(
            "Deviation-only bandwidth sweep",
            "Deviation (Hz)",
            "Bandwidth (Hz)",
            [
                ("98 percent", deviations, [_fm(d, fm)[7] for d in deviations]),
                ("Carson", deviations, [2 * (d + fm) for d in deviations]),
            ],
        ),
        "frequency_sweep": _plot(
            "Message-frequency-only bandwidth sweep",
            "Message frequency (Hz)",
            "Bandwidth (Hz)",
            [
                (
                    "98 percent",
                    frequencies,
                    [_fm(deviation, f)[7] for f in frequencies],
                ),
                ("Carson", frequencies, [2 * (deviation + f) for f in frequencies]),
            ],
        ),
    }
    return _result(
        signature,
        fields,
        plots,
        {
            "observation": "FM phase slope moves while magnitude stays fixed. The smallest symmetric span containing 98% of retained RF line power is measured separately from Carson's approximation.",
            "broken": "An 8 kHz carrier with 5 kHz deviation exceeds 12 kHz Nyquist at 24 ksample/s; the observed phase increments wrap. Its aliased spectrum cannot certify occupied bandwidth.",
            "recovery": "Resample the same physical failure at 30 ksample/s. The 10.2 kHz occupied span and positive guard are retained; finite-difference phase-slope error remains visible.",
        },
        1022,
        broken,
        {
            "sample_count": 4800,
            "recovery_sample_count": 6000,
            "active_bandwidth_valid": not broken,
        },
    )
