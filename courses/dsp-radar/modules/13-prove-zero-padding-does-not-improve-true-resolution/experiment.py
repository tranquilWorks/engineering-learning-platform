from __future__ import annotations

from typing import Any

import numpy as np

SEED = 1013
FS_HZ = 1024.0


def _layout(title: str, x_label: str, y_label: str) -> dict[str, Any]:
    return {
        "title": {"text": title, "x": 0.02},
        "xaxis": {"title": x_label},
        "yaxis": {"title": y_label},
        "legend": {"orientation": "h", "y": 1.14},
        "margin": {"l": 68, "r": 22, "t": 58, "b": 58},
    }


def _long_record() -> np.ndarray:
    sample = np.arange(512)
    signal = np.cos(2 * np.pi * 198 * sample / FS_HZ) + np.cos(
        2 * np.pi * 202 * sample / FS_HZ
    )
    rng = np.random.default_rng(SEED)
    noise = rng.standard_normal(512)
    noise *= 0.002 / np.sqrt(np.mean(noise**2))
    return signal + noise


def _case(
    padding_factor: int, observation_multiplier: int, broken: bool
) -> dict[str, Any]:
    if padding_factor not in {1, 4, 16} or observation_multiplier not in {1, 2, 4}:
        raise ValueError(
            "padding_factor and observation_multiplier must use retained cases"
        )
    count = 128 * observation_multiplier
    fft_count = count * padding_factor
    if fft_count > 8192:
        raise ValueError("FFT exceeds the bounded 8192-point ceiling")
    signal = _long_record()[:count]
    spectrum = np.abs(np.fft.rfft(signal, fft_count)) / count
    frequency = np.fft.rfftfreq(fft_count, 1 / FS_HZ)
    region = (frequency >= 180) & (frequency <= 220)
    region_f = frequency[region]
    region_s = spectrum[region]
    left_peak = float(np.max(region_s[region_f <= 200]))
    right_peak = float(np.max(region_s[region_f >= 200]))
    center_value = float(region_s[int(np.argmin(np.abs(region_f - 200)))])
    valley_ratio = center_value / max(min(left_peak, right_peak), 1e-15)
    display_spacing = FS_HZ / fft_count
    rayleigh = FS_HZ / count
    displayed_resolution = display_spacing if broken else rayleigh
    return {
        "count": count,
        "fft_count": fft_count,
        "frequency": region_f,
        "spectrum": region_s,
        "display_spacing": display_spacing,
        "rayleigh": rayleigh,
        "valley_ratio": valley_ratio,
        "displayed_resolution": displayed_resolution,
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    padding = int(parameters["padding_factor"])
    observation = int(parameters["observation_multiplier"])
    broken = bool(parameters["broken_mode"])
    case = _case(padding, observation, broken)
    padding_sweep = np.array([1, 4, 16])
    display_sweep = [FS_HZ / (128 * value) for value in padding_sweep]
    padding_valley = [
        _case(int(value), 1, False)["valley_ratio"] for value in padding_sweep
    ]
    observation_sweep = np.array([1, 2, 4])
    rayleigh_sweep = [FS_HZ / (128 * value) for value in observation_sweep]
    observation_valley = [
        _case(16, int(value), False)["valley_ratio"] for value in observation_sweep
    ]
    signature = [
        float(padding),
        float(observation),
        float(case["count"]),
        float(case["fft_count"]),
        case["display_spacing"],
        case["rayleigh"],
        case["valley_ratio"],
        case["displayed_resolution"],
    ]
    return {
        "metrics": [
            {
                "id": "measured_samples",
                "label": "Measured samples",
                "value": case["count"],
                "unit": "samples",
            },
            {
                "id": "display_spacing",
                "label": "FFT display spacing",
                "value": case["display_spacing"],
                "unit": "Hz",
            },
            {
                "id": "rayleigh",
                "label": "Observation Rayleigh scale",
                "value": case["rayleigh"],
                "unit": "Hz",
                "emphasis": "primary",
            },
            {
                "id": "displayed_resolution",
                "label": "Displayed resolution claim",
                "value": case["displayed_resolution"],
                "unit": "Hz",
            },
        ],
        "plots": {
            "padded_spectrum": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "two-tone spectrum",
                        "x": case["frequency"],
                        "y": case["spectrum"],
                    }
                ],
                "layout": _layout(
                    "Same measurements on the selected FFT grid",
                    "Frequency (Hz)",
                    "Magnitude (V)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "padding_sweep": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "display spacing",
                        "x": padding_sweep,
                        "y": display_sweep,
                    },
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "valley ratio",
                        "x": padding_sweep,
                        "y": padding_valley,
                        "yaxis": "y2",
                    },
                ],
                "layout": _layout(
                    "Zero-padding sweep: denser grid, same response",
                    "Padding factor",
                    "Spacing (Hz)",
                )
                | {
                    "yaxis2": {
                        "title": "Valley ratio",
                        "overlaying": "y",
                        "side": "right",
                    }
                },
                "config": {"responsive": True, "displaylogo": False},
            },
            "observation_sweep": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "Rayleigh scale",
                        "x": observation_sweep,
                        "y": rayleigh_sweep,
                    },
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "valley ratio",
                        "x": observation_sweep,
                        "y": observation_valley,
                        "yaxis": "y2",
                    },
                ],
                "layout": _layout(
                    "Measured-duration sweep",
                    "Observation multiplier",
                    "Rayleigh scale (Hz)",
                )
                | {
                    "yaxis2": {
                        "title": "Valley ratio",
                        "overlaying": "y",
                        "side": "right",
                    }
                },
                "config": {"responsive": True, "displaylogo": False},
            },
            "broken_case": {
                "data": [
                    {
                        "type": "bar",
                        "name": "resolution scale",
                        "x": ["display grid", "physical observation", "displayed"],
                        "y": [
                            case["display_spacing"],
                            case["rayleigh"],
                            case["displayed_resolution"],
                        ],
                    }
                ],
                "layout": _layout(
                    "Display density is not resolving power",
                    "Scale",
                    "Frequency interval (Hz)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "Zero padding samples the same finite-record transform more densely. Only more measured duration narrows the physical main lobe and separates the 4 Hz pair.",
            "broken": "Broken mode reports fs/NFFT as physical resolution, even though the measured sample count and finite-record response did not change.",
            "recovery": "Report display spacing separately from fs/Nmeasured and compare separability against the genuinely longer shared-prefix record.",
        },
        "diagnostics": {
            "seed": SEED,
            "signature": signature,
            "tone_separation_hz": 4.0,
            "broken_active": broken,
        },
    }
