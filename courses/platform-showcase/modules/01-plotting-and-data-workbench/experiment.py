from __future__ import annotations

from typing import Any

import numpy as np
from scipy import signal


def _layout(title: str, x: str = "", y: str = "") -> dict[str, Any]:
    return {
        "title": {"text": title, "x": 0.02, "xanchor": "left"},
        "margin": {"l": 62, "r": 24, "t": 55, "b": 55},
        "xaxis": {"title": x, "showgrid": True, "zeroline": False},
        "yaxis": {"title": y, "showgrid": True, "zeroline": False},
        "legend": {"orientation": "h", "y": 1.12},
        "uirevision": "keep-view",
    }


def _window(name: str, count: int) -> np.ndarray:
    if name == "hann":
        return np.hanning(count)
    if name == "blackman":
        return np.blackman(count)
    return np.ones(count)


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    fs = float(parameters["sample_rate_hz"])
    tone = float(parameters["tone_hz"])
    sigma = float(parameters["noise_sigma"])
    count = int(fs * 2)
    t = np.arange(count) / fs
    rng = np.random.default_rng(4102)
    analytic = np.exp(1j * (2 * np.pi * tone * t + 0.35))
    if bool(parameters["second_tone"]):
        analytic += 0.55 * np.exp(1j * (2 * np.pi * (tone + 13) * t - 0.7))
    analytic += sigma * (rng.standard_normal(count) + 1j * rng.standard_normal(count))
    real_signal = analytic.real

    window = _window(str(parameters["window"]), count)
    coherent_gain = max(float(window.mean()), 1e-12)
    spectrum = np.fft.rfft(real_signal * window)
    frequencies = np.fft.rfftfreq(count, 1 / fs)
    magnitude_db = 20 * np.log10(np.maximum(np.abs(spectrum) / (count * coherent_gain / 2), 1e-10))

    peak_indices, _properties = signal.find_peaks(
        magnitude_db, height=-45, distance=max(1, int(count / fs * 5))
    )
    ordered = sorted(peak_indices, key=lambda index: magnitude_db[index], reverse=True)[:8]
    rows = [
        {
            "rank": rank,
            "frequency_hz": float(frequencies[index]),
            "magnitude_db": float(magnitude_db[index]),
            "nearest_expected_hz": tone if abs(frequencies[index] - tone) < 7 else tone + 13,
        }
        for rank, index in enumerate(ordered, start=1)
    ]

    segment = min(128, max(32, count // 8))
    stft_f, stft_t, stft_z = signal.stft(real_signal, fs=fs, nperseg=segment, noverlap=segment // 2)
    stft_db = 20 * np.log10(np.maximum(np.abs(stft_z), 1e-8))

    axis = np.linspace(-1, 1, 91)
    range_axis, doppler_axis = np.meshgrid(axis, axis)
    width = float(parameters["surface_width"])
    surface = (np.sinc(range_axis / width) * np.sinc(doppler_axis / (width * 0.72))) ** 2
    surface_db = 10 * np.log10(np.maximum(surface, 1e-5))

    theta = np.linspace(0, 360, 361)
    pattern = np.abs(np.cos(np.deg2rad(theta))) ** 3
    if bool(parameters["second_tone"]):
        pattern = np.clip(pattern + 0.28 * np.abs(np.cos(np.deg2rad(theta - 48))) ** 8, 0, None)
    pattern_db = 20 * np.log10(np.maximum(pattern / pattern.max(), 1e-3))

    preview = min(count, int(fs * 0.12))
    time_layout = _layout("Sampled signal", "Time (s)", "Amplitude")
    spectrum_layout = _layout("Windowed spectrum", "Frequency (Hz)", "Magnitude (dB)")
    spectrum_layout["yaxis"]["range"] = [-80, 8]
    iq_layout = _layout("Complex analytic trajectory", "In-phase", "Quadrature")
    iq_layout["yaxis"]["scaleanchor"] = "x"
    spectrogram_layout = _layout("Short-time Fourier transform", "Time (s)", "Frequency (Hz)")

    return {
        "metrics": [
            {"id": "primary_tone", "label": "Primary tone", "value": tone, "unit": "Hz", "emphasis": "primary"},
            {"id": "nyquist", "label": "Nyquist", "value": fs / 2, "unit": "Hz"},
            {"id": "frequency_bin", "label": "FFT bin", "value": fs / count, "unit": "Hz"},
            {"id": "sample_count", "label": "Samples", "value": count},
        ],
        "plots": {
            "time_domain": {
                "data": [{"type": "scattergl", "mode": "lines+markers", "name": "x[n]", "x": t[:preview], "y": real_signal[:preview], "marker": {"size": 3}}],
                "layout": time_layout,
                "config": {"responsive": True, "displaylogo": False},
            },
            "spectrum": {
                "data": [{"type": "scattergl", "mode": "lines", "name": "FFT", "x": frequencies, "y": magnitude_db}],
                "layout": spectrum_layout,
                "config": {"responsive": True, "displaylogo": False},
            },
            "iq_plane": {
                "data": [{"type": "scattergl", "mode": "lines", "name": "I+jQ", "x": analytic[:preview].real, "y": analytic[:preview].imag}],
                "layout": iq_layout,
                "config": {"responsive": True, "displaylogo": False},
            },
            "spectrogram": {
                "data": [{"type": "heatmap", "x": stft_t, "y": stft_f, "z": stft_db, "colorscale": "Viridis", "colorbar": {"title": "dB"}}],
                "layout": spectrogram_layout,
                "config": {"responsive": True, "displaylogo": False},
            },
            "response_surface": {
                "data": [{"type": "surface", "x": axis, "y": axis, "z": surface_db, "colorscale": "Cividis", "cmin": -50, "cmax": 0}],
                "layout": {
                    "title": {"text": "Synthetic range–Doppler response", "x": 0.02},
                    "scene": {"xaxis": {"title": "Normalized range"}, "yaxis": {"title": "Normalized Doppler"}, "zaxis": {"title": "Response (dB)", "range": [-50, 0]}},
                    "margin": {"l": 12, "r": 12, "t": 52, "b": 10},
                    "uirevision": "keep-view",
                },
                "config": {"responsive": True, "displaylogo": False},
            },
            "polar_pattern": {
                "data": [{"type": "scatterpolar", "mode": "lines", "name": "Pattern", "theta": theta, "r": pattern_db, "fill": "toself"}],
                "layout": {"title": {"text": "Normalized polar pattern", "x": 0.02}, "polar": {"radialaxis": {"range": [-60, 0], "title": "dB"}}, "margin": {"l": 35, "r": 35, "t": 55, "b": 30}},
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "tables": {"spectral_peaks": {"columns": ["rank", "frequency_hz", "magnitude_db", "nearest_expected_hz"], "rows": rows}},
        "explanations": {
            "coherence": "All signal-derived views use the same parameter state and deterministic data realization.",
        },
        "diagnostics": {"peak_count": len(rows), "window": parameters["window"]},
    }
