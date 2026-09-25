from __future__ import annotations

from typing import Any

import numpy as np

SEED = 1010
MAX_SAMPLES = 5000


def _layout(title: str, x_label: str, y_label: str) -> dict[str, Any]:
    return {
        "title": {"text": title, "x": 0.02},
        "xaxis": {"title": x_label},
        "yaxis": {"title": y_label},
        "legend": {"orientation": "h", "y": 1.14},
        "margin": {"l": 68, "r": 22, "t": 58, "b": 58},
    }


def _lowpass(taps: int, cutoff_hz: float, fs: float, gain: float = 1.0) -> np.ndarray:
    if taps < 5 or taps > 129 or taps % 2 == 0:
        raise ValueError("filter tap count must be odd and bounded")
    center = (taps - 1) / 2.0
    index = np.arange(taps) - center
    coefficients = (
        2.0 * cutoff_hz / fs * np.sinc(2.0 * cutoff_hz * index / fs) * np.hamming(taps)
    )
    return gain * coefficients / np.sum(coefficients)


def _tone_amplitude(signal: np.ndarray, frequency_hz: float, fs: float) -> float:
    time = np.arange(len(signal)) / fs
    return float(
        2.0
        * abs(np.vdot(np.exp(-1j * 2.0 * np.pi * frequency_hz * time), signal))
        / len(signal)
    )


def _case(high_hz: float, reconstruction_taps: int, broken: bool) -> dict[str, Any]:
    if not 180.0 <= high_hz <= 900.0:
        raise ValueError("high_tone_hz exceeds the bounded range")
    fs = 2400.0
    factor = 4
    count = 2400
    if count > MAX_SAMPLES:
        raise ValueError("record exceeds the resource ceiling")
    rng = np.random.default_rng(SEED)
    time = np.arange(count) / fs
    source = (
        np.sin(2.0 * np.pi * 90.0 * time)
        + 0.65 * np.sin(2.0 * np.pi * high_hz * time)
        + 0.01 * rng.standard_normal(count)
    )
    anti_alias = _lowpass(65, 240.0, fs)
    filtered = np.convolve(source, anti_alias, mode="same")
    decimated = source[::factor] if broken else filtered[::factor]
    low_fs = fs / factor
    folded_hz = abs(high_hz - round(high_hz / low_fs) * low_fs)
    folded_amplitude = _tone_amplitude(decimated, folded_hz, low_fs)
    zero_stuffed = np.zeros(len(decimated) * factor)
    zero_stuffed[::factor] = decimated
    reconstruction = _lowpass(reconstruction_taps, 240.0, fs, gain=factor)
    recovered = (
        zero_stuffed
        if broken
        else np.convolve(zero_stuffed, reconstruction, mode="same")
    )
    imaging_hz = low_fs - 90.0
    image_amplitude = _tone_amplitude(recovered, imaging_hz, fs)
    low_tone_amplitude = _tone_amplitude(recovered, 90.0, fs)
    return {
        "time": time,
        "source": source,
        "filtered": filtered,
        "decimated": decimated,
        "low_fs": low_fs,
        "folded_hz": folded_hz,
        "folded_amplitude": folded_amplitude,
        "zero_stuffed": zero_stuffed,
        "recovered": recovered,
        "image_hz": imaging_hz,
        "image_amplitude": image_amplitude,
        "low_tone_amplitude": low_tone_amplitude,
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    high_hz = float(parameters["high_tone_hz"])
    reconstruction_taps = int(parameters["reconstruction_taps"])
    broken = bool(parameters["broken_mode"])
    case = _case(high_hz, reconstruction_taps, broken)
    high_sweep = np.array([220.0, 280.0, 340.0, 420.0])
    folded_sweep = [
        _case(float(value), 65, False)["folded_amplitude"] for value in high_sweep
    ]
    tap_sweep = np.array([9, 17, 33, 65])
    image_sweep = [
        _case(420.0, int(value), False)["image_amplitude"] for value in tap_sweep
    ]
    low_time = np.arange(len(case["decimated"])) / case["low_fs"]
    return {
        "metrics": [
            {
                "id": "output_sample_rate",
                "label": "Decimated sample rate",
                "value": case["low_fs"],
                "unit": "Sa/s",
            },
            {
                "id": "folded_frequency",
                "label": "High-tone folded frequency",
                "value": case["folded_hz"],
                "unit": "Hz",
            },
            {
                "id": "folded_amplitude",
                "label": "Folded component",
                "value": case["folded_amplitude"],
                "unit": "a.u.",
                "emphasis": "primary",
            },
            {
                "id": "image_amplitude",
                "label": "First image component",
                "value": case["image_amplitude"],
                "unit": "a.u.",
            },
        ],
        "plots": {
            "decimation": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "source",
                        "x": case["time"][:300],
                        "y": case["source"][:300],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "anti-alias filtered",
                        "x": case["time"][:300],
                        "y": case["filtered"][:300],
                    },
                    {
                        "type": "scatter",
                        "mode": "markers",
                        "name": "decimated",
                        "x": low_time[:75],
                        "y": case["decimated"][:75],
                    },
                ],
                "layout": _layout(
                    "Filter before dropping samples", "Time (s)", "Amplitude (a.u.)"
                ),
            },
            "interpolation": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "zero-stuffed",
                        "x": case["time"][:300],
                        "y": case["zero_stuffed"][:300],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "reconstruction output",
                        "x": case["time"][:300],
                        "y": case["recovered"][:300],
                    },
                ],
                "layout": _layout(
                    "Filter after zero insertion", "Time (s)", "Amplitude (a.u.)"
                ),
            },
            "parameter_sweeps": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "offending-tone sweep",
                        "x": high_sweep,
                        "y": folded_sweep,
                    },
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "reconstruction-tap sweep",
                        "x": tap_sweep,
                        "y": image_sweep,
                    },
                ],
                "layout": _layout(
                    "Two multirate sweeps",
                    "Tone frequency (Hz) or taps",
                    "Folded or image amplitude (a.u.)",
                ),
            },
        },
        "explanations": {
            "observation": "The 4:1 decimator needs an anti-alias low-pass before sample dropping. The interpolator needs a gain-corrected low-pass after zero insertion to remove spectral images.",
            "broken": "Broken mode drops samples directly and leaves inserted zeros unfiltered, exposing a folded high tone and strong images.",
            "recovery": "Low-pass before decimation and after interpolation. Longer reconstruction filters suppress the first image more strongly.",
        },
        "diagnostics": {
            "seed": SEED,
            "source_samples": 2400,
            "decimated_samples": len(case["decimated"]),
            "broken_active": broken,
            "folded_frequency_hz": case["folded_hz"],
            "folded_amplitude": case["folded_amplitude"],
            "image_frequency_hz": case["image_hz"],
            "image_amplitude": case["image_amplitude"],
            "signature": [
                high_hz,
                reconstruction_taps,
                case["low_fs"],
                case["folded_hz"],
                case["folded_amplitude"],
                case["image_amplitude"],
                case["low_tone_amplitude"],
            ],
        },
    }
