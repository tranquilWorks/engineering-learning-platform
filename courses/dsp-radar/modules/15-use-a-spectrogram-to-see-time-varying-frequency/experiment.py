from __future__ import annotations

from typing import Any

import numpy as np

SEED = 1015
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


def _signal() -> np.ndarray:
    sample = np.arange(COUNT)
    time = sample / FS_HZ
    signal = 0.35 * np.cos(2 * np.pi * 90 * time + 0.2)
    chirp_gate = (time >= 0.5) & (time < 2.25)
    chirp_time = time - 0.5
    slope = (320 - 220) / (2.25 - 0.5)
    chirp_phase = 2 * np.pi * (220 * chirp_time + 0.5 * slope * chirp_time**2) - 0.4
    signal += 0.25 * np.cos(chirp_phase) * chirp_gate
    burst = (sample >= 1536) & (sample < 1600)
    signal += 0.8 * np.cos(2 * np.pi * 380 * time + 0.7) * burst
    hop_phase = np.where(
        time < 2.75,
        2 * np.pi * 156 * time - 0.3,
        2 * np.pi * (156 * 2.75 + 174 * (time - 2.75)) - 0.3,
    )
    signal += 0.28 * np.cos(hop_phase)
    rng = np.random.default_rng(SEED)
    return signal + 0.02 * rng.standard_normal(COUNT)


def _stft(
    values: np.ndarray,
    window_length: int,
    overlap: float,
    fft_length: int | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    fft_length = window_length if fft_length is None else fft_length
    hop = round(window_length * (1 - overlap))
    starts = np.arange(0, len(values) - window_length + 1, hop)
    if len(starts) > 256 or fft_length > 512:
        raise ValueError("STFT resource ceiling exceeded")
    n = np.arange(window_length)
    window = 0.5 - 0.5 * np.cos(2 * np.pi * n / (window_length - 1))
    scale = FS_HZ * np.sum(window**2)
    columns = []
    for start in starts:
        transformed = np.fft.rfft(
            values[start : start + window_length] * window, fft_length
        )
        psd = np.abs(transformed) ** 2 / scale
        if len(psd) > 2:
            psd[1:-1] *= 2
        columns.append(psd)
    return (
        np.fft.rfftfreq(fft_length, 1 / FS_HZ),
        (starts + (window_length - 1) / 2) / FS_HZ,
        np.array(columns).T,
    )


def _case(window_length: int, overlap: float, broken: bool) -> dict[str, Any]:
    if window_length not in {64, 128, 512} or overlap not in {0.0, 0.5, 0.75}:
        raise ValueError("use retained window and overlap cases")
    values = _signal()
    frequency, frame_time, psd = _stft(values, window_length, overlap)
    burst_bin = int(np.argmin(np.abs(frequency - 380)))
    burst_frame = int(np.argmax(psd[burst_bin]))
    burst_center = (1536 + 31.5) / FS_HZ
    burst_time_error = float(abs(frame_time[burst_frame] - burst_center))
    before_frame = int(np.argmin(np.abs(frame_time - 2.65)))
    after_frame = int(np.argmin(np.abs(frame_time - 2.85)))
    before_156 = psd[int(np.argmin(np.abs(frequency - 156))), before_frame]
    before_174 = psd[int(np.argmin(np.abs(frequency - 174))), before_frame]
    after_156 = psd[int(np.argmin(np.abs(frequency - 156))), after_frame]
    after_174 = psd[int(np.argmin(np.abs(frequency - 174))), after_frame]
    hop_contrast = float(
        10
        * np.log10(
            max(before_156 * after_174, 1e-30) / max(before_174 * after_156, 1e-30)
        )
    )
    chirp_frames = (frame_time >= 0.6) & (frame_time <= 2.15)
    chirp_band = (frequency >= 200.0) & (frequency <= 340.0)
    chirp_frequency = frequency[chirp_band]
    chirp_density = psd[np.ix_(chirp_band, chirp_frames)]
    ridge_frequency = chirp_frequency[np.argmax(chirp_density, axis=0)]
    expected_ridge = 220.0 + (100.0 / 1.75) * (frame_time[chirp_frames] - 0.5)
    chirp_ridge_rmse = float(np.sqrt(np.mean((ridge_frequency - expected_ridge) ** 2)))
    physical_width = 4 * FS_HZ / window_length
    broken_display_spacing = FS_HZ / 512
    displayed_resolution = broken_display_spacing if broken else physical_width
    return {
        "values": values,
        "frequency": frequency,
        "time": frame_time,
        "psd": psd,
        "frame_count": len(frame_time),
        "time_spacing": float(np.diff(frame_time).mean())
        if len(frame_time) > 1
        else 0.0,
        "bin_spacing": FS_HZ / window_length,
        "physical_width": physical_width,
        "burst_time_error": burst_time_error,
        "hop_contrast": hop_contrast,
        "chirp_ridge_rmse": chirp_ridge_rmse,
        "broken_display_spacing": broken_display_spacing,
        "displayed_resolution": displayed_resolution,
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    window_length = int(parameters["window_length"])
    overlap = float(parameters["overlap_fraction"])
    broken = bool(parameters["broken_mode"])
    case = _case(window_length, overlap, broken)
    lengths = np.array([512, 128, 64])
    burst_error = [
        _case(int(value), 0.5, False)["burst_time_error"] for value in lengths
    ]
    physical_width = [4 * FS_HZ / value for value in lengths]
    overlaps = np.array([0.0, 0.5, 0.75])
    time_spacing = [
        _case(128, float(value), False)["time_spacing"] for value in overlaps
    ]
    downsample = np.arange(0, COUNT, 8)
    signature = [
        float(window_length),
        overlap,
        float(case["frame_count"]),
        case["time_spacing"],
        case["bin_spacing"],
        case["physical_width"],
        case["burst_time_error"],
        case["hop_contrast"],
        case["displayed_resolution"],
        case["chirp_ridge_rmse"],
    ]
    return {
        "metrics": [
            {
                "id": "frame_count",
                "label": "STFT frames",
                "value": case["frame_count"],
                "unit": "frames",
            },
            {
                "id": "time_spacing",
                "label": "Frame-time spacing",
                "value": case["time_spacing"],
                "unit": "s",
            },
            {
                "id": "physical_width",
                "label": "Hann main-lobe scale",
                "value": case["physical_width"],
                "unit": "Hz",
                "emphasis": "primary",
            },
            {
                "id": "burst_error",
                "label": "Burst-time error",
                "value": case["burst_time_error"],
                "unit": "s",
            },
            {
                "id": "chirp_ridge_error",
                "label": "Chirp-ridge RMSE",
                "value": case["chirp_ridge_rmse"],
                "unit": "Hz",
            },
            {
                "id": "hop_contrast",
                "label": "156/174 Hz hop contrast",
                "value": case["hop_contrast"],
                "unit": "dB",
            },
        ],
        "plots": {
            "time_record": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "composite record",
                        "x": downsample / FS_HZ,
                        "y": case["values"][downsample],
                    }
                ],
                "layout": _layout(
                    "Steady tone, chirp, burst, and hop", "Time (s)", "Amplitude (V)"
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "spectrogram": {
                "data": [
                    {
                        "type": "heatmap",
                        "name": "PSD",
                        "x": case["time"],
                        "y": case["frequency"],
                        "z": 10 * np.log10(np.maximum(case["psd"], 1e-20)),
                        "colorscale": "Viridis",
                    }
                ],
                "layout": _layout(
                    "Explicit STFT", "Frame-center time (s)", "Frequency (Hz)"
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "window_sweep": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "burst timing error",
                        "x": lengths,
                        "y": burst_error,
                    },
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "frequency width",
                        "x": lengths,
                        "y": physical_width,
                        "yaxis": "y2",
                    },
                ],
                "layout": _layout(
                    "Time-frequency window tradeoff",
                    "Window length (samples)",
                    "Timing error (s)",
                )
                | {
                    "yaxis2": {
                        "title": "Main-lobe scale (Hz)",
                        "overlaying": "y",
                        "side": "right",
                    }
                },
                "config": {"responsive": True, "displaylogo": False},
            },
            "overlap_and_broken": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "frame spacing",
                        "x": overlaps,
                        "y": time_spacing,
                    },
                    {
                        "type": "bar",
                        "name": "resolution scales",
                        "x": ["zero-padded grid", "physical window", "displayed"],
                        "y": [
                            case["broken_display_spacing"],
                            case["physical_width"],
                            case["displayed_resolution"],
                        ],
                    },
                ],
                "layout": _layout(
                    "Overlap and zero-padding claim",
                    "Overlap or scale",
                    "Time / frequency metric",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "Each spectrogram column is one finite windowed measurement. Short windows localize events; long windows narrow spectral responses; overlap only samples frame centers more densely.",
            "broken": "Broken mode labels the 2 Hz zero-padded grid of a 64-sample window as 2 Hz physical resolution even though its Hann main-lobe scale is about 64 Hz.",
            "recovery": "Keep FFT display spacing, window response width, and frame spacing as separate quantities when interpreting the burst, chirp, and 18 Hz hop.",
        },
        "diagnostics": {"seed": SEED, "signature": signature, "broken_active": broken},
    }
