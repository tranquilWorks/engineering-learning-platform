from __future__ import annotations

from typing import Any

import numpy as np

SEED = 1014
FS_HZ = 1024.0
COUNT = 4096


def _layout(title: str, x_label: str, y_label: str) -> dict[str, Any]:
    return {
        "title": {"text": title, "x": 0.02},
        "xaxis": {"title": x_label},
        "yaxis": {"title": y_label},
        "legend": {"orientation": "h", "y": 1.14},
        "margin": {"l": 68, "r": 22, "t": 58, "b": 58},
    }


def _record(seed: int) -> np.ndarray:
    sample = np.arange(COUNT)
    rng = np.random.default_rng(seed)
    return (
        np.cos(2 * np.pi * 160 * sample / FS_HZ + 0.3)
        + 0.12 * np.cos(2 * np.pi * 172 * sample / FS_HZ - 0.7)
        + 0.35 * rng.standard_normal(COUNT)
    )


def _one_sided_psd(
    values: np.ndarray, window: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    transformed = np.fft.rfft(values * window)
    psd = np.abs(transformed) ** 2 / (FS_HZ * np.sum(window**2))
    if len(psd) > 2:
        psd[1:-1] *= 2.0
    return np.fft.rfftfreq(len(values), 1 / FS_HZ), psd


def _welch(
    values: np.ndarray, segment_length: int, overlap: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    hop = round(segment_length * (1.0 - overlap))
    if hop < 1:
        raise ValueError("overlap leaves no hop")
    starts = np.arange(0, len(values) - segment_length + 1, hop)
    if len(starts) > 32:
        raise ValueError("segment ceiling exceeded")
    n = np.arange(segment_length)
    window = 0.5 - 0.5 * np.cos(2 * np.pi * n / (segment_length - 1))
    pieces = np.array(
        [
            _one_sided_psd(values[start : start + segment_length], window)[1]
            for start in starts
        ]
    )
    frequency = np.fft.rfftfreq(segment_length, 1 / FS_HZ)
    return frequency, np.mean(pieces, axis=0), pieces


def _effective_average_count(
    segment_length: int, overlap: float, segment_count: int
) -> float:
    hop = round(segment_length * (1.0 - overlap))
    index = np.arange(segment_length)
    window = 0.5 - 0.5 * np.cos(2 * np.pi * index / (segment_length - 1))
    energy = np.sum(window**2)
    correction = 1.0
    for lag in range(1, segment_count):
        shift = lag * hop
        if shift >= segment_length:
            break
        correlation = np.sum(window[:-shift] * window[shift:]) / energy
        correction += 2.0 * (1.0 - lag / segment_count) * correlation**2
    return float(segment_count / correction)


def _case(segment_length: int, overlap: float, broken: bool) -> dict[str, Any]:
    if segment_length not in {256, 512, 1024} or overlap not in {0.0, 0.5, 0.75}:
        raise ValueError("use retained segment and overlap cases")
    values = _record(SEED)
    full_frequency, periodogram = _one_sided_psd(values, np.ones(COUNT))
    welch_frequency, welch, pieces = _welch(values, segment_length, overlap)
    probe_index = int(np.argmin(np.abs(welch_frequency - 360.0)))
    correct_probe = float(welch[probe_index])
    broken_probe_db = float(
        np.mean(10 * np.log10(np.maximum(pieces[:, probe_index], 1e-20)))
    )
    correct_probe_db = float(10 * np.log10(max(correct_probe, 1e-20)))
    displayed_probe_db = broken_probe_db if broken else correct_probe_db
    periodogram_trials = []
    welch_trials = []
    for seed in range(SEED, SEED + 24):
        trial = _record(seed)
        f_full, p_full = _one_sided_psd(trial, np.ones(COUNT))
        f_welch, p_welch, _ = _welch(trial, 512, 0.5)
        periodogram_trials.append(p_full[int(np.argmin(np.abs(f_full - 360.0)))])
        welch_trials.append(p_welch[int(np.argmin(np.abs(f_welch - 360.0)))])
    periodogram_cv = float(np.std(periodogram_trials) / np.mean(periodogram_trials))
    welch_cv = float(np.std(welch_trials) / np.mean(welch_trials))
    segment_count = len(pieces)
    return {
        "full_frequency": full_frequency,
        "periodogram": periodogram,
        "welch_frequency": welch_frequency,
        "welch": welch,
        "segment_count": segment_count,
        "effective_average_count": _effective_average_count(
            segment_length, overlap, segment_count
        ),
        "correct_probe_db": correct_probe_db,
        "broken_probe_db": broken_probe_db,
        "displayed_probe_db": displayed_probe_db,
        "periodogram_cv": periodogram_cv,
        "welch_cv": welch_cv,
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    segment = int(parameters["segment_length"])
    overlap = float(parameters["overlap_fraction"])
    broken = bool(parameters["broken_mode"])
    case = _case(segment, overlap, broken)
    lengths = np.array([1024, 512, 256])
    ripple = []
    for value in lengths:
        sub = _case(int(value), 0.5, False)
        band = (sub["welch_frequency"] >= 300) & (sub["welch_frequency"] <= 450)
        band_db = 10 * np.log10(np.maximum(sub["welch"][band], 1e-20))
        ripple.append(float(np.std(band_db)))
    overlaps = np.array([0.0, 0.5, 0.75])
    segment_counts = [
        _case(512, float(value), False)["segment_count"] for value in overlaps
    ]
    effective_counts = [
        _case(512, float(value), False)["effective_average_count"] for value in overlaps
    ]
    show_full = case["full_frequency"] <= 500
    show_welch = case["welch_frequency"] <= 500
    signature = [
        float(segment),
        overlap,
        float(case["segment_count"]),
        case["effective_average_count"],
        FS_HZ / COUNT,
        FS_HZ / segment,
        case["periodogram_cv"],
        case["welch_cv"],
        case["correct_probe_db"],
        case["broken_probe_db"],
        case["displayed_probe_db"],
    ]
    return {
        "metrics": [
            {
                "id": "segment_count",
                "label": "Welch segments",
                "value": case["segment_count"],
                "unit": "segments",
            },
            {
                "id": "effective_average_count",
                "label": "Effective independent averages",
                "value": case["effective_average_count"],
                "unit": "averages",
            },
            {
                "id": "segment_spacing",
                "label": "Segment-bin spacing",
                "value": FS_HZ / segment,
                "unit": "Hz",
            },
            {
                "id": "welch_cv",
                "label": "Welch probe variation",
                "value": case["welch_cv"],
                "unit": "CV",
                "emphasis": "primary",
            },
            {
                "id": "probe_psd",
                "label": "Displayed 360 Hz PSD",
                "value": case["displayed_probe_db"],
                "unit": "dB V²/Hz",
            },
        ],
        "plots": {
            "psd_comparison": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "full periodogram",
                        "x": case["full_frequency"][show_full],
                        "y": 10
                        * np.log10(np.maximum(case["periodogram"][show_full], 1e-20)),
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "Welch average",
                        "x": case["welch_frequency"][show_welch],
                        "y": 10
                        * np.log10(np.maximum(case["welch"][show_welch], 1e-20)),
                    },
                ],
                "layout": _layout(
                    "Fine jagged periodogram versus steadier Welch PSD",
                    "Frequency (Hz)",
                    "PSD (dB V²/Hz)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "segment_sweep": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "noise-band ripple",
                        "x": lengths,
                        "y": ripple,
                    }
                ],
                "layout": _layout(
                    "Segment-length tradeoff",
                    "Segment length (samples)",
                    "Noise-band ripple (dB std)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "overlap_sweep": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "raw segment count",
                        "x": overlaps,
                        "y": segment_counts,
                    },
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "effective independent averages",
                        "x": overlaps,
                        "y": effective_counts,
                    },
                ],
                "layout": _layout(
                    "Overlap reuses the record", "Overlap fraction", "Segment count"
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "broken_case": {
                "data": [
                    {
                        "type": "bar",
                        "name": "360 Hz estimate",
                        "x": ["linear average then dB", "average dB", "displayed"],
                        "y": [
                            case["correct_probe_db"],
                            case["broken_probe_db"],
                            case["displayed_probe_db"],
                        ],
                    }
                ],
                "layout": _layout("PSD averaging order", "Method", "PSD (dB V²/Hz)"),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "Welch lowers realization variance by averaging shorter windowed records, trading each segment's frequency resolution against a steadier random-noise estimate.",
            "broken": "Broken mode averages logarithmic dB samples; concavity biases the result below the logarithm of the correctly averaged linear power.",
            "recovery": "Average V²/Hz estimates first and convert to dB once. Treat overlap as reused information, not one independent record per raw segment.",
        },
        "diagnostics": {
            "seed": SEED,
            "signature": signature,
            "periodogram_cv": case["periodogram_cv"],
            "welch_cv": case["welch_cv"],
            "broken_active": broken,
        },
    }
