from __future__ import annotations

from typing import Any

import numpy as np

SEED = 1018
COUNT = 4096


def _layout(title: str, x_label: str, y_label: str) -> dict[str, Any]:
    return {
        "title": {"text": title, "x": 0.02},
        "xaxis": {"title": x_label},
        "yaxis": {"title": y_label},
        "legend": {"orientation": "h", "y": 1.14},
        "margin": {"l": 68, "r": 22, "t": 58, "b": 58},
    }


def _estimate(values: np.ndarray, rate: float) -> float:
    return float(
        np.angle(np.sum(np.conj(values[:-1]) * values[1:])) * rate / (2.0 * np.pi)
    )


def _alias(frequency: float, rate: float) -> float:
    return float((frequency + rate / 2.0) % rate - rate / 2.0)


def _downconversion(offset: float) -> dict[str, Any]:
    sample_rate = 2048.0
    time = np.arange(COUNT) / sample_rate
    upper_rf = np.exp(1j * (2.0 * np.pi * (600.0 + offset) * time + 0.35))
    lower_rf = np.exp(1j * (2.0 * np.pi * (600.0 - offset) * time - 0.35))
    complex_lo = np.exp(-1j * 2.0 * np.pi * 600.0 * time)
    upper_complex = upper_rf * complex_lo
    lower_complex = lower_rf * complex_lo
    centered = np.arange(129) - 64
    ideal = 2.0 * 450.0 / sample_rate * np.sinc(2.0 * 450.0 * centered / sample_rate)
    taps = ideal * np.hamming(129)
    taps /= np.sum(taps)
    real_lo = 2.0 * np.cos(2.0 * np.pi * 600.0 * time)
    upper_real = np.convolve(upper_rf.real * real_lo, taps, mode="same")
    lower_real = np.convolve(lower_rf.real * real_lo, taps, mode="same")
    evaluation = slice(192, -192)
    return {
        "time": time,
        "upper_complex": upper_complex,
        "lower_complex": lower_complex,
        "upper_real": upper_real,
        "lower_real": lower_real,
        "upper_frequency": _estimate(upper_complex, sample_rate),
        "lower_frequency": _estimate(lower_complex, sample_rate),
        "real_collapse_rmse": float(
            np.sqrt(np.mean((upper_real[evaluation] - lower_real[evaluation]) ** 2))
        ),
    }


def _case(offset: float, rate: float, broken: bool) -> dict[str, Any]:
    if offset not in {40.0, 160.0, 400.0}:
        raise ValueError("offset_frequency_hz must be 40, 160, or 400")
    if rate not in {256.0, 512.0, 2048.0}:
        raise ValueError("sample_rate_hz must be 256, 512, or 2048")
    count = int(rate * 0.5)
    time = np.arange(count) / rate
    positive_clean = np.exp(1j * (2.0 * np.pi * offset * time + 0.35))
    rng = np.random.default_rng(SEED)
    noise = (
        0.002
        / np.sqrt(2.0)
        * (rng.standard_normal(count) + 1j * rng.standard_normal(count))
    )
    positive = positive_clean + noise
    negative = np.conj(positive)
    real_positive = positive.real
    real_negative = negative.real
    if broken:
        estimated_positive = _estimate(real_positive.astype(complex), rate)
        estimated_negative = _estimate(real_negative.astype(complex), rate)
    else:
        estimated_positive = _estimate(positive, rate)
        estimated_negative = _estimate(negative, rate)
    frequency = np.fft.fftshift(np.fft.fftfreq(count, 1.0 / rate))
    positive_spectrum = np.abs(np.fft.fftshift(np.fft.fft(positive))) / count
    negative_spectrum = np.abs(np.fft.fftshift(np.fft.fft(negative))) / count
    real_spectrum = np.abs(np.fft.fftshift(np.fft.fft(real_positive))) / count
    return {
        "time": time,
        "positive": positive,
        "negative": negative,
        "real_positive": real_positive,
        "real_negative": real_negative,
        "frequency": frequency,
        "positive_spectrum": positive_spectrum,
        "negative_spectrum": negative_spectrum,
        "real_spectrum": real_spectrum,
        "positive_estimate": estimated_positive,
        "negative_estimate": estimated_negative,
        "positive_alias": _alias(offset, rate),
        "negative_alias": _alias(-offset, rate),
        "projection_rmse": float(
            np.sqrt(np.mean((real_positive - real_negative) ** 2))
        ),
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    offset = float(parameters["offset_frequency_hz"])
    rate = float(parameters["sample_rate_hz"])
    broken = bool(parameters["broken_mode"])
    case = _case(offset, rate, broken)
    downconversion = _downconversion(offset)
    offsets = np.array([40.0, 160.0, 400.0])
    positive_offset = [
        _case(float(value), 2048.0, False)["positive_estimate"] for value in offsets
    ]
    negative_offset = [
        _case(float(value), 2048.0, False)["negative_estimate"] for value in offsets
    ]
    rates = np.array([2048.0, 512.0, 256.0])
    positive_alias = [
        _case(160.0, float(value), False)["positive_alias"] for value in rates
    ]
    negative_alias = [
        _case(160.0, float(value), False)["negative_alias"] for value in rates
    ]
    baseline = _case(160.0, 2048.0, False)
    broken_case = _case(160.0, 2048.0, True)
    display = np.arange(
        0, len(case["frequency"]), max(1, len(case["frequency"]) // 512)
    )
    signature = [
        offset,
        rate,
        case["positive_alias"],
        case["negative_alias"],
        case["positive_estimate"],
        case["negative_estimate"],
        case["projection_rmse"],
        broken_case["positive_estimate"],
        broken_case["negative_estimate"],
        baseline["positive_estimate"],
        baseline["negative_estimate"],
        downconversion["upper_frequency"],
        downconversion["lower_frequency"],
        downconversion["real_collapse_rmse"],
    ]
    return {
        "metrics": [
            {
                "id": "positive_frequency",
                "label": "Positive-rotation estimate",
                "value": case["positive_estimate"],
                "unit": "Hz",
                "emphasis": "primary",
            },
            {
                "id": "negative_frequency",
                "label": "Negative-rotation estimate",
                "value": case["negative_estimate"],
                "unit": "Hz",
            },
            {
                "id": "real_projection_rmse",
                "label": "Real-projection difference",
                "value": case["projection_rmse"],
                "unit": "V",
            },
            {
                "id": "nyquist_limit",
                "label": "Complex signed Nyquist limit",
                "value": rate / 2.0,
                "unit": "Hz",
            },
            {
                "id": "complex_upper_side",
                "label": "Complex upper-side result",
                "value": downconversion["upper_frequency"],
                "unit": "Hz",
            },
            {
                "id": "complex_lower_side",
                "label": "Complex lower-side result",
                "value": downconversion["lower_frequency"],
                "unit": "Hz",
            },
            {
                "id": "real_mixer_collapse",
                "label": "Real-mixer side collapse",
                "value": downconversion["real_collapse_rmse"],
                "unit": "V RMS",
            },
        ],
        "plots": {
            "iq_rotation": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "+f rotation",
                        "x": case["positive"].real[:40],
                        "y": case["positive"].imag[:40],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "-f rotation",
                        "x": case["negative"].real[:40],
                        "y": case["negative"].imag[:40],
                    },
                ],
                "layout": _layout("I/Q preserves rotation direction", "I (V)", "Q (V)"),
                "config": {"responsive": True, "displaylogo": False},
            },
            "centered_spectra": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "+f complex",
                        "x": case["frequency"][display],
                        "y": case["positive_spectrum"][display],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "-f complex",
                        "x": case["frequency"][display],
                        "y": case["negative_spectrum"][display],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "real projection",
                        "x": case["frequency"][display],
                        "y": case["real_spectrum"][display],
                    },
                ],
                "layout": _layout(
                    "Centered signed spectra", "Signed frequency (Hz)", "Magnitude (V)"
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "downconversion": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "complex upper side",
                        "x": downconversion["upper_complex"].real[:40],
                        "y": downconversion["upper_complex"].imag[:40],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "complex lower side",
                        "x": downconversion["lower_complex"].real[:40],
                        "y": downconversion["lower_complex"].imag[:40],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "real upper side after LPF",
                        "x": downconversion["time"][192:272],
                        "y": downconversion["upper_real"][192:272],
                        "yaxis": "y2",
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "real lower side after LPF",
                        "x": downconversion["time"][192:272],
                        "y": downconversion["lower_real"][192:272],
                        "yaxis": "y2",
                    },
                ],
                "layout": _layout(
                    "Real versus complex downconversion around 600 Hz",
                    "I (V) / time (s)",
                    "Q (V)",
                )
                | {
                    "yaxis2": {
                        "title": "Real baseband (V)",
                        "overlaying": "y",
                        "side": "right",
                    }
                },
                "config": {"responsive": True, "displaylogo": False},
            },
            "offset_sweep": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "+ rotation",
                        "x": offsets,
                        "y": positive_offset,
                    },
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "- rotation",
                        "x": offsets,
                        "y": negative_offset,
                    },
                ],
                "layout": _layout(
                    "Offset-frequency sign sweep",
                    "Offset magnitude (Hz)",
                    "Estimated signed frequency (Hz)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "alias_and_broken": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "+f alias",
                        "x": rates,
                        "y": positive_alias,
                    },
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "-f alias",
                        "x": rates,
                        "y": negative_alias,
                    },
                    {
                        "type": "bar",
                        "name": "discard-Q estimates",
                        "x": [2048.0, 2048.0],
                        "y": [
                            broken_case["positive_estimate"],
                            broken_case["negative_estimate"],
                        ],
                    },
                ],
                "layout": _layout(
                    "Under-Nyquist aliases and discard-Q failure",
                    "Sample rate (samples/s)",
                    "Signed frequency (Hz)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "Conjugate complex rotations have opposite phase progression and signed spectral peaks even though their real projections are identical.",
            "broken": "Discarding Q projects both rotations onto the same cosine; the adjacent-product phase then collapses both sign estimates to zero.",
            "recovery": "Retain I and Q and interpret frequency on the centered signed interval, including the deterministic aliases produced below Nyquist.",
        },
        "diagnostics": {
            "seed": SEED,
            "signature": signature,
            "broken_active": broken,
            "expected_positive_alias_hz": case["positive_alias"],
            "expected_negative_alias_hz": case["negative_alias"],
            "complex_downconversion_hz": [
                downconversion["upper_frequency"],
                downconversion["lower_frequency"],
            ],
            "real_mixer_collapse_rmse_v": downconversion["real_collapse_rmse"],
        },
    }
