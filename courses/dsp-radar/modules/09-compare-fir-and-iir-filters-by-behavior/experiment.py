from __future__ import annotations

from typing import Any

import numpy as np

SEED = 909
MAX_SAMPLES = 2048


def _layout(title: str, x_label: str, y_label: str) -> dict[str, Any]:
    return {
        "title": {"text": title, "x": 0.02},
        "xaxis": {"title": x_label},
        "yaxis": {"title": y_label},
        "legend": {"orientation": "h", "y": 1.14},
        "margin": {"l": 68, "r": 22, "t": 58, "b": 58},
    }


def _fir(taps: int, cutoff_hz: float, fs: float) -> np.ndarray:
    if taps % 2 == 0:
        raise ValueError("FIR tap count must be odd")
    center = (taps - 1) / 2.0
    index = np.arange(taps) - center
    ideal = 2.0 * cutoff_hz / fs * np.sinc(2.0 * cutoff_hz * index / fs)
    coefficients = ideal * np.hamming(taps)
    return coefficients / np.sum(coefficients)


def _biquad(
    q: float, cutoff_hz: float, fs: float, radius_override: float | None = None
) -> tuple[np.ndarray, np.ndarray]:
    if radius_override is not None:
        angle = 2.0 * np.pi * cutoff_hz / fs
        denominator = np.array(
            [1.0, -2.0 * radius_override * np.cos(angle), radius_override**2]
        )
        numerator = np.array([1.0 - radius_override, 0.0, 0.0])
        return numerator, denominator
    omega = 2.0 * np.pi * cutoff_hz / fs
    alpha = np.sin(omega) / (2.0 * q)
    cosine = np.cos(omega)
    numerator = np.array([(1.0 - cosine) / 2.0, 1.0 - cosine, (1.0 - cosine) / 2.0]) / (
        1.0 + alpha
    )
    denominator = np.array(
        [1.0, -2.0 * cosine / (1.0 + alpha), (1.0 - alpha) / (1.0 + alpha)]
    )
    return numerator, denominator


def _filter(
    numerator: np.ndarray, denominator: np.ndarray, signal: np.ndarray
) -> np.ndarray:
    output = np.zeros_like(signal, dtype=float)
    for index in range(len(signal)):
        for tap, coefficient in enumerate(numerator):
            if index >= tap:
                output[index] += coefficient * signal[index - tap]
        for tap in range(1, len(denominator)):
            if index >= tap:
                output[index] -= denominator[tap] * output[index - tap]
    return output / denominator[0]


def _response(
    numerator: np.ndarray, denominator: np.ndarray, count: int = 160
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    omega = np.linspace(0.0, np.pi, count)
    z = np.exp(-1j * omega)
    top = sum(value * z**index for index, value in enumerate(numerator))
    bottom = sum(value * z**index for index, value in enumerate(denominator))
    response = top / bottom
    phase = np.unwrap(np.angle(response))
    group_delay = -np.gradient(phase, omega)
    return omega, np.abs(response), group_delay


def _case(taps: int, q: float, broken: bool) -> dict[str, Any]:
    if taps < 5 or taps > 81 or taps % 2 == 0 or not 0.3 <= q <= 4.0:
        raise ValueError("filter controls exceed the bounded range")
    fs = 1000.0
    count = 400
    if count > MAX_SAMPLES:
        raise ValueError("record exceeds the resource ceiling")
    fir_b = _fir(taps, 120.0, fs)
    iir_b, iir_a = _biquad(q, 100.0, fs)
    omega, fir_mag, fir_delay = _response(fir_b, np.array([1.0]))
    _, iir_mag, iir_delay = _response(iir_b, iir_a)
    impulse = np.zeros(count)
    impulse[0] = 1.0
    step = np.ones(count)
    pulse = np.zeros(count)
    pulse[80:140] = 1.0
    rng = np.random.default_rng(SEED)
    time = np.arange(count) / fs
    signal = (
        np.sin(2.0 * np.pi * 40.0 * time)
        + 0.45 * np.sin(2.0 * np.pi * 260.0 * time)
        + 0.15 * rng.standard_normal(count)
    )
    fir_impulse = np.convolve(impulse, fir_b)[:count]
    iir_impulse = _filter(iir_b, iir_a, impulse)
    fir_signal = np.convolve(signal, fir_b)[:count]
    iir_signal = _filter(iir_b, iir_a, signal)
    broken_b, broken_a = _biquad(q, 90.0, fs, 1.02 if broken else 0.98)
    broken_impulse = _filter(broken_b, broken_a, impulse)
    recovered_b, recovered_a = _biquad(q, 90.0, fs, 0.98)
    recovered_impulse = _filter(recovered_b, recovered_a, impulse)
    return {
        "frequency": omega * fs / (2.0 * np.pi),
        "fir_mag": fir_mag,
        "iir_mag": iir_mag,
        "fir_delay": fir_delay,
        "iir_delay": iir_delay,
        "fir_impulse": fir_impulse,
        "iir_impulse": iir_impulse,
        "fir_step": np.convolve(step, fir_b)[:count],
        "iir_step": _filter(iir_b, iir_a, step),
        "fir_pulse": np.convolve(pulse, fir_b)[:count],
        "iir_pulse": _filter(iir_b, iir_a, pulse),
        "signal": signal,
        "fir_signal": fir_signal,
        "iir_signal": iir_signal,
        "broken_impulse": broken_impulse,
        "recovered_impulse": recovered_impulse,
        "fir_multiplies": taps,
        "iir_multiplies": 5,
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    taps = int(parameters["fir_taps"])
    q = float(parameters["iir_q"])
    broken = bool(parameters["broken_mode"])
    case = _case(taps, q, broken)
    tap_sweep = np.array([9, 21, 41])
    stopband = [
        float(np.mean(_case(int(value), 1 / np.sqrt(2), False)["fir_mag"][-30:] ** 2))
        for value in tap_sweep
    ]
    q_sweep = np.array([0.5, 1 / np.sqrt(2), 2.0])
    resonance = [
        float(np.max(_case(21, float(value), False)["iir_mag"])) for value in q_sweep
    ]
    index = np.arange(400)
    displayed = case["broken_impulse"] if broken else case["recovered_impulse"]
    displayed_tail_ratio = float(abs(displayed[-1]) / max(abs(displayed[20]), 1e-30))
    return {
        "metrics": [
            {
                "id": "fir_group_delay",
                "label": "FIR passband delay",
                "value": (taps - 1) / 2.0,
                "unit": "samples",
            },
            {
                "id": "iir_peak_gain",
                "label": "IIR peak gain",
                "value": float(np.max(case["iir_mag"])),
                "unit": "ratio",
                "emphasis": "primary",
            },
            {
                "id": "fir_multiplies",
                "label": "FIR multiplies/output",
                "value": case["fir_multiplies"],
                "unit": "multiplies",
            },
            {
                "id": "iir_multiplies",
                "label": "IIR multiplies/output",
                "value": case["iir_multiplies"],
                "unit": "multiplies",
            },
        ],
        "plots": {
            "frequency_behavior": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "FIR magnitude",
                        "x": case["frequency"],
                        "y": case["fir_mag"],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "IIR magnitude",
                        "x": case["frequency"],
                        "y": case["iir_mag"],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "FIR group delay",
                        "x": case["frequency"],
                        "y": case["fir_delay"],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "IIR group delay",
                        "x": case["frequency"],
                        "y": case["iir_delay"],
                    },
                ],
                "layout": _layout(
                    "FIR and IIR frequency behavior",
                    "Frequency (Hz)",
                    "Magnitude or delay (samples)",
                ),
            },
            "time_behavior": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "FIR impulse",
                        "x": index,
                        "y": case["fir_impulse"],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "IIR impulse",
                        "x": index,
                        "y": case["iir_impulse"],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "FIR pulse",
                        "x": index,
                        "y": case["fir_pulse"],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "IIR pulse",
                        "x": index,
                        "y": case["iir_pulse"],
                    },
                ],
                "layout": _layout(
                    "Impulse, step, and pulse behavior",
                    "Sample index",
                    "Amplitude (a.u.)",
                ),
            },
            "signal_behavior": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "input plus noise",
                        "x": index,
                        "y": case["signal"],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "FIR output",
                        "x": index,
                        "y": case["fir_signal"],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "IIR output",
                        "x": index,
                        "y": case["iir_signal"],
                    },
                ],
                "layout": _layout(
                    "Signal and noise behavior", "Sample index", "Amplitude (a.u.)"
                ),
            },
            "parameter_sweeps": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "FIR-tap sweep",
                        "x": tap_sweep,
                        "y": stopband,
                    },
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "IIR-Q sweep",
                        "x": q_sweep,
                        "y": resonance,
                    },
                ],
                "layout": _layout(
                    "Two filter sweeps", "Tap count or Q", "Stopband power or peak gain"
                ),
            },
            "stability_failure": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "stable radius 0.98",
                        "x": index,
                        "y": case["recovered_impulse"],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "displayed",
                        "x": index,
                        "y": displayed,
                    },
                ],
                "layout": _layout(
                    "Pole radius controls decay or growth",
                    "Sample index",
                    "Impulse response (a.u.)",
                ),
            },
        },
        "explanations": {
            "observation": "The linear-phase FIR trades more arithmetic and fixed delay for a finite response; the biquad uses fewer multiplies but has nonlinear delay and Q-dependent resonance.",
            "broken": "Broken mode puts a pole radius at 1.02, so the impulse envelope grows instead of decaying.",
            "recovery": "Move the pole radius to 0.98. The recovered response decays while retaining the resonant frequency.",
        },
        "diagnostics": {
            "seed": SEED,
            "sample_count": 400,
            "broken_active": broken,
            "broken_tail_ratio": float(
                abs(case["broken_impulse"][-1])
                / max(abs(case["broken_impulse"][20]), 1e-30)
            ),
            "recovered_tail_ratio": float(
                abs(case["recovered_impulse"][-1])
                / max(abs(case["recovered_impulse"][20]), 1e-30)
            ),
            "signature": [
                taps,
                q,
                float(np.max(case["iir_mag"])),
                float(np.mean(case["fir_mag"][-30:] ** 2)),
                case["fir_multiplies"],
                case["iir_multiplies"],
                displayed_tail_ratio,
            ],
        },
    }
