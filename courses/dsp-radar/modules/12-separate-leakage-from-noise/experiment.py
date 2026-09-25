from __future__ import annotations

from typing import Any

import numpy as np

SEED = 1012
FS_HZ = 1024.0
COUNT = 128
WINDOWS = ["Rectangular", "Hann", "Hamming", "Blackman", "Flat-top"]


def _layout(title: str, x_label: str, y_label: str) -> dict[str, Any]:
    return {
        "title": {"text": title, "x": 0.02},
        "xaxis": {"title": x_label},
        "yaxis": {"title": y_label},
        "legend": {"orientation": "h", "y": 1.14},
        "margin": {"l": 68, "r": 22, "t": 58, "b": 58},
    }


def _window(name: str) -> np.ndarray:
    n = np.arange(COUNT)
    angle = 2.0 * np.pi * n / (COUNT - 1)
    if name == "Rectangular":
        return np.ones(COUNT)
    if name == "Hann":
        return 0.5 - 0.5 * np.cos(angle)
    if name == "Hamming":
        return 0.54 - 0.46 * np.cos(angle)
    if name == "Blackman":
        return 0.42 - 0.5 * np.cos(angle) + 0.08 * np.cos(2.0 * angle)
    if name == "Flat-top":
        return (
            1.0
            - 1.93 * np.cos(angle)
            + 1.29 * np.cos(2 * angle)
            - 0.388 * np.cos(3 * angle)
            + 0.0322 * np.cos(4 * angle)
        )
    raise ValueError("unknown window")


def _metrics(name: str, offset: float, broken: bool) -> dict[str, Any]:
    if name not in WINDOWS or not np.isfinite(offset) or not 0.0 <= offset <= 0.5:
        raise ValueError("invalid window or fractional-bin offset")
    sample = np.arange(COUNT)
    tone = np.exp(1j * (2.0 * np.pi * (17.0 + offset) * sample / COUNT + 0.25))
    rng = np.random.default_rng(SEED)
    noise = (
        0.02
        / np.sqrt(2.0)
        * (rng.standard_normal(COUNT) + 1j * rng.standard_normal(COUNT))
    )
    window = _window(name)
    coherent_gain = float(np.mean(window))
    fft_count = 2048
    clean_spectrum = np.abs(np.fft.fft(tone * window, fft_count)) / (
        COUNT * abs(coherent_gain)
    )
    noise_spectrum = np.abs(np.fft.fft(noise * window, fft_count)) / (
        COUNT * abs(coherent_gain)
    )
    frequency_bins = np.arange(fft_count) * FS_HZ / fft_count
    peak_index = int(np.argmax(clean_spectrum))
    peak = float(clean_spectrum[peak_index])
    threshold = peak / np.sqrt(2.0)
    above = np.flatnonzero(clean_spectrum >= threshold)
    near = above[np.abs(above - peak_index) < 128]
    main_lobe_width_hz = float((near[-1] - near[0]) * FS_HZ / fft_count)
    exclusion_bins = {
        "Rectangular": 4,
        "Hann": 8,
        "Hamming": 8,
        "Blackman": 12,
        "Flat-top": 20,
    }[name] * (fft_count // COUNT)
    mask = np.ones(fft_count, dtype=bool)
    mask[
        max(0, peak_index - exclusion_bins) : min(
            fft_count, peak_index + exclusion_bins + 1
        )
    ] = False
    sidelobe_db = float(
        20.0 * np.log10(max(np.max(clean_spectrum[mask]) / peak, 1e-15))
    )
    amplitude_error_db = float(20.0 * np.log10(max(peak, 1e-15)))
    coarse = np.abs(np.fft.fft(tone)) / COUNT
    offpeak_energy = float(np.sum(coarse**2) - np.max(coarse) ** 2)
    actual_noise_floor = float(np.median(noise_spectrum))
    clean_offpeak = float(np.median(clean_spectrum[mask]))
    displayed_noise = clean_offpeak if broken else actual_noise_floor
    return {
        "frequency": frequency_bins[:1025],
        "clean": clean_spectrum[:1025],
        "noise": noise_spectrum[:1025],
        "coherent_gain": coherent_gain,
        "main_lobe_width_hz": main_lobe_width_hz,
        "sidelobe_db": sidelobe_db,
        "amplitude_error_db": amplitude_error_db,
        "offpeak_energy": offpeak_energy,
        "actual_noise_floor": actual_noise_floor,
        "displayed_noise": displayed_noise,
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    name = str(parameters["window_name"])
    offset = float(parameters["tone_bin_offset"])
    broken = bool(parameters["broken_mode"])
    case = _metrics(name, offset, broken)
    window_width = [
        _metrics(value, 0.35, False)["main_lobe_width_hz"] for value in WINDOWS
    ]
    offset_sweep = np.array([0.0, 0.2, 0.35, 0.5])
    leakage_sweep = [
        _metrics("Rectangular", float(value), False)["offpeak_energy"]
        for value in offset_sweep
    ]
    signature = [
        float(WINDOWS.index(name)),
        offset,
        case["coherent_gain"],
        case["main_lobe_width_hz"],
        case["amplitude_error_db"],
        case["sidelobe_db"],
        case["offpeak_energy"],
        case["actual_noise_floor"],
        case["displayed_noise"],
    ]
    return {
        "metrics": [
            {
                "id": "coherent_gain",
                "label": "Coherent gain",
                "value": case["coherent_gain"],
                "unit": "ratio",
            },
            {
                "id": "main_lobe_width",
                "label": "-3 dB main-lobe width",
                "value": case["main_lobe_width_hz"],
                "unit": "Hz",
                "emphasis": "primary",
            },
            {
                "id": "amplitude_error",
                "label": "Peak amplitude error",
                "value": case["amplitude_error_db"],
                "unit": "dB",
            },
            {
                "id": "sidelobe",
                "label": "Maximum sidelobe",
                "value": case["sidelobe_db"],
                "unit": "dBc",
            },
            {
                "id": "noise_floor",
                "label": "Displayed noise floor",
                "value": case["displayed_noise"],
                "unit": "V",
            },
        ],
        "plots": {
            "leakage_spectrum": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "clean finite-record tone",
                        "x": case["frequency"],
                        "y": 20 * np.log10(np.maximum(case["clean"], 1e-8)),
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "seeded noise",
                        "x": case["frequency"],
                        "y": 20 * np.log10(np.maximum(case["noise"], 1e-8)),
                    },
                ],
                "layout": _layout(
                    "Structured leakage versus random noise",
                    "Frequency (Hz)",
                    "Magnitude (dB re 1 V)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "window_tradeoffs": {
                "data": [
                    {
                        "type": "bar",
                        "name": "main-lobe width",
                        "x": WINDOWS,
                        "y": window_width,
                    }
                ],
                "layout": _layout("Window tradeoff", "Window", "-3 dB width (Hz)"),
                "config": {"responsive": True, "displaylogo": False},
            },
            "parameter_sweeps": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "rectangular off-peak energy",
                        "x": offset_sweep,
                        "y": leakage_sweep,
                    }
                ],
                "layout": _layout(
                    "Fractional-bin leakage sweep",
                    "Fractional-bin offset",
                    "Off-peak energy (V²)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "broken_case": {
                "data": [
                    {
                        "type": "bar",
                        "name": "noise estimate",
                        "x": ["actual seeded noise", "displayed estimate"],
                        "y": [case["actual_noise_floor"], case["displayed_noise"]],
                    }
                ],
                "layout": _layout(
                    "Leakage mislabeled as noise", "Estimator", "Median magnitude (V)"
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "Finite observation creates a repeat-boundary discontinuity and a deterministic leakage pattern; a window reshapes that pattern with measurable width, sidelobe, and amplitude tradeoffs.",
            "broken": "Broken mode calls the clean tone's nonpeak projections noise even though the controlled input contains no random component there.",
            "recovery": "Separate the known clean-tone response from the seeded noise realization and average or characterize noise only in linear physical units.",
        },
        "diagnostics": {
            "seed": SEED,
            "signature": signature,
            "window": name,
            "broken_active": broken,
        },
    }
