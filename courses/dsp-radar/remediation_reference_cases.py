"""Independent numerical references for the P02-P20 fidelity repair.

This module deliberately imports no course experiment.  It recreates the selected
source equations from scenario parameters so evidence is not self-comparison.
"""

from __future__ import annotations

from typing import Any

import numpy as np

SCENARIOS: dict[str, dict[str, dict[str, Any]]] = {
    "P02": {
        "baseline": {
            "sample_rate_hz": 80.0,
            "clock_offset_samples": 0.0,
            "broken_mode": False,
        },
        "sweep_1": {
            "sample_rate_hz": 16.0,
            "clock_offset_samples": 0.0,
            "broken_mode": False,
        },
        "sweep_2": {
            "sample_rate_hz": 80.0,
            "clock_offset_samples": 0.5,
            "broken_mode": False,
        },
        "broken": {
            "sample_rate_hz": 80.0,
            "clock_offset_samples": 0.0,
            "broken_mode": True,
        },
        "recovery": {
            "sample_rate_hz": 80.0,
            "clock_offset_samples": 0.0,
            "broken_mode": False,
        },
    },
    "P03": {
        "baseline": {
            "input_frequency_hz": 700.0,
            "sample_rate_hz": 1000.0,
            "broken_mode": False,
        },
        "sweep_1": {
            "input_frequency_hz": 1300.0,
            "sample_rate_hz": 1000.0,
            "broken_mode": False,
        },
        "sweep_2": {
            "input_frequency_hz": 700.0,
            "sample_rate_hz": 1600.0,
            "broken_mode": False,
        },
        "broken": {
            "input_frequency_hz": 700.0,
            "sample_rate_hz": 1000.0,
            "broken_mode": True,
        },
        "recovery": {
            "input_frequency_hz": 700.0,
            "sample_rate_hz": 1000.0,
            "broken_mode": False,
        },
    },
    "P04": {
        "baseline": {
            "bit_depth": 6,
            "amplitude_v": 0.9,
            "dither_enabled": False,
            "broken_mode": False,
        },
        "sweep_1": {
            "bit_depth": 8,
            "amplitude_v": 0.9,
            "dither_enabled": False,
            "broken_mode": False,
        },
        "sweep_2": {
            "bit_depth": 6,
            "amplitude_v": 0.5,
            "dither_enabled": False,
            "broken_mode": False,
        },
        "broken": {
            "bit_depth": 6,
            "amplitude_v": 0.9,
            "dither_enabled": False,
            "broken_mode": True,
        },
        "recovery": {
            "bit_depth": 6,
            "amplitude_v": 0.9,
            "dither_enabled": False,
            "broken_mode": False,
        },
    },
    "P05": {
        "baseline": {
            "colored_memory": 0.92,
            "interferer_offset_hz": 100.0,
            "noise_rms_v": 0.25,
            "broken_mode": False,
        },
        "sweep_1": {
            "colored_memory": 0.7,
            "interferer_offset_hz": 100.0,
            "noise_rms_v": 0.25,
            "broken_mode": False,
        },
        "sweep_2": {
            "colored_memory": 0.92,
            "interferer_offset_hz": 300.0,
            "noise_rms_v": 0.25,
            "broken_mode": False,
        },
        "broken": {
            "colored_memory": 0.92,
            "interferer_offset_hz": 100.0,
            "noise_rms_v": 0.25,
            "broken_mode": True,
        },
        "recovery": {
            "colored_memory": 0.92,
            "interferer_offset_hz": 100.0,
            "noise_rms_v": 0.25,
            "broken_mode": False,
        },
    },
    "P06": {
        "baseline": {
            "echo_delay_samples": 32,
            "resonator_radius": 0.86,
            "broken_mode": False,
        },
        "sweep_1": {
            "echo_delay_samples": 48,
            "resonator_radius": 0.86,
            "broken_mode": False,
        },
        "sweep_2": {
            "echo_delay_samples": 32,
            "resonator_radius": 0.96,
            "broken_mode": False,
        },
        "broken": {
            "echo_delay_samples": 32,
            "resonator_radius": 0.86,
            "broken_mode": True,
        },
        "recovery": {
            "echo_delay_samples": 32,
            "resonator_radius": 0.86,
            "broken_mode": False,
        },
    },
    "P07": {
        "baseline": {
            "middle_echo_delay_samples": 5,
            "third_echo_gain": -0.35,
            "broken_mode": False,
        },
        "sweep_1": {
            "middle_echo_delay_samples": 7,
            "third_echo_gain": -0.35,
            "broken_mode": False,
        },
        "sweep_2": {
            "middle_echo_delay_samples": 5,
            "third_echo_gain": 0.35,
            "broken_mode": False,
        },
        "broken": {
            "middle_echo_delay_samples": 5,
            "third_echo_gain": -0.35,
            "broken_mode": True,
        },
        "recovery": {
            "middle_echo_delay_samples": 5,
            "third_echo_gain": -0.35,
            "broken_mode": False,
        },
    },
    "P08": {
        "baseline": {
            "target_amplitude": 0.65,
            "noise_sigma": 0.5,
            "target_separation_samples": 50,
            "broken_mode": False,
        },
        "sweep_1": {
            "target_amplitude": 1.0,
            "noise_sigma": 0.5,
            "target_separation_samples": 50,
            "broken_mode": False,
        },
        "sweep_2": {
            "target_amplitude": 0.65,
            "noise_sigma": 1.0,
            "target_separation_samples": 50,
            "broken_mode": False,
        },
        "broken": {
            "target_amplitude": 0.65,
            "noise_sigma": 0.5,
            "target_separation_samples": 50,
            "broken_mode": True,
        },
        "recovery": {
            "target_amplitude": 0.65,
            "noise_sigma": 0.5,
            "target_separation_samples": 50,
            "broken_mode": False,
        },
    },
    "P09": {
        "baseline": {"fir_taps": 21, "iir_q": 0.70710678, "broken_mode": False},
        "sweep_1": {"fir_taps": 41, "iir_q": 0.70710678, "broken_mode": False},
        "sweep_2": {"fir_taps": 21, "iir_q": 2.0, "broken_mode": False},
        "broken": {"fir_taps": 21, "iir_q": 0.70710678, "broken_mode": True},
        "recovery": {"fir_taps": 21, "iir_q": 0.70710678, "broken_mode": False},
    },
    "P10": {
        "baseline": {
            "high_tone_hz": 420.0,
            "reconstruction_taps": 65,
            "broken_mode": False,
        },
        "sweep_1": {
            "high_tone_hz": 280.0,
            "reconstruction_taps": 65,
            "broken_mode": False,
        },
        "sweep_2": {
            "high_tone_hz": 420.0,
            "reconstruction_taps": 33,
            "broken_mode": False,
        },
        "broken": {
            "high_tone_hz": 420.0,
            "reconstruction_taps": 65,
            "broken_mode": True,
        },
        "recovery": {
            "high_tone_hz": 420.0,
            "reconstruction_taps": 65,
            "broken_mode": False,
        },
    },
    "P11": {
        "baseline": {
            "record_sample_count": 64,
            "tone_bin_offset": 0.0,
            "broken_mode": False,
        },
        "sweep_1": {
            "record_sample_count": 128,
            "tone_bin_offset": 0.0,
            "broken_mode": False,
        },
        "sweep_2": {
            "record_sample_count": 64,
            "tone_bin_offset": 0.5,
            "broken_mode": False,
        },
        "broken": {
            "record_sample_count": 64,
            "tone_bin_offset": 0.0,
            "broken_mode": True,
        },
        "recovery": {
            "record_sample_count": 64,
            "tone_bin_offset": 0.0,
            "broken_mode": False,
        },
    },
    "P12": {
        "baseline": {
            "window_name": "Hann",
            "tone_bin_offset": 0.35,
            "broken_mode": False,
        },
        "sweep_1": {
            "window_name": "Rectangular",
            "tone_bin_offset": 0.35,
            "broken_mode": False,
        },
        "sweep_2": {
            "window_name": "Hann",
            "tone_bin_offset": 0.5,
            "broken_mode": False,
        },
        "broken": {"window_name": "Hann", "tone_bin_offset": 0.35, "broken_mode": True},
        "recovery": {
            "window_name": "Hann",
            "tone_bin_offset": 0.35,
            "broken_mode": False,
        },
    },
    "P13": {
        "baseline": {
            "padding_factor": 4,
            "observation_multiplier": 1,
            "broken_mode": False,
        },
        "sweep_1": {
            "padding_factor": 16,
            "observation_multiplier": 1,
            "broken_mode": False,
        },
        "sweep_2": {
            "padding_factor": 4,
            "observation_multiplier": 4,
            "broken_mode": False,
        },
        "broken": {
            "padding_factor": 16,
            "observation_multiplier": 1,
            "broken_mode": True,
        },
        "recovery": {
            "padding_factor": 16,
            "observation_multiplier": 1,
            "broken_mode": False,
        },
    },
    "P14": {
        "baseline": {
            "segment_length": 512,
            "overlap_fraction": 0.5,
            "broken_mode": False,
        },
        "sweep_1": {
            "segment_length": 1024,
            "overlap_fraction": 0.5,
            "broken_mode": False,
        },
        "sweep_2": {
            "segment_length": 512,
            "overlap_fraction": 0.75,
            "broken_mode": False,
        },
        "broken": {"segment_length": 512, "overlap_fraction": 0.5, "broken_mode": True},
        "recovery": {
            "segment_length": 512,
            "overlap_fraction": 0.5,
            "broken_mode": False,
        },
    },
    "P15": {
        "baseline": {
            "window_length": 128,
            "overlap_fraction": 0.5,
            "broken_mode": False,
        },
        "sweep_1": {
            "window_length": 512,
            "overlap_fraction": 0.5,
            "broken_mode": False,
        },
        "sweep_2": {
            "window_length": 128,
            "overlap_fraction": 0.75,
            "broken_mode": False,
        },
        "broken": {"window_length": 64, "overlap_fraction": 0.5, "broken_mode": True},
        "recovery": {
            "window_length": 64,
            "overlap_fraction": 0.5,
            "broken_mode": False,
        },
    },
    "P16": {
        "baseline": {
            "envelope_depth": 0.6,
            "phase_deviation_rad": 0.6,
            "broken_mode": False,
        },
        "sweep_1": {
            "envelope_depth": 0.9,
            "phase_deviation_rad": 0.6,
            "broken_mode": False,
        },
        "sweep_2": {
            "envelope_depth": 0.6,
            "phase_deviation_rad": 1.2,
            "broken_mode": False,
        },
        "broken": {
            "envelope_depth": 0.6,
            "phase_deviation_rad": 0.6,
            "broken_mode": True,
        },
        "recovery": {
            "envelope_depth": 0.6,
            "phase_deviation_rad": 0.6,
            "broken_mode": False,
        },
    },
    "P17": {
        "baseline": {
            "lo_frequency_hz": 240.0,
            "lo_phase_rad": 0.0,
            "broken_mode": False,
        },
        "sweep_1": {
            "lo_frequency_hz": 204.0,
            "lo_phase_rad": 0.0,
            "broken_mode": False,
        },
        "sweep_2": {
            "lo_frequency_hz": 240.0,
            "lo_phase_rad": 1.5707963267948966,
            "broken_mode": False,
        },
        "broken": {"lo_frequency_hz": 216.0, "lo_phase_rad": 0.0, "broken_mode": True},
        "recovery": {
            "lo_frequency_hz": 216.0,
            "lo_phase_rad": 0.0,
            "broken_mode": False,
        },
    },
    "P18": {
        "baseline": {
            "offset_frequency_hz": 160.0,
            "sample_rate_hz": 2048.0,
            "broken_mode": False,
        },
        "sweep_1": {
            "offset_frequency_hz": 400.0,
            "sample_rate_hz": 2048.0,
            "broken_mode": False,
        },
        "sweep_2": {
            "offset_frequency_hz": 160.0,
            "sample_rate_hz": 256.0,
            "broken_mode": False,
        },
        "broken": {
            "offset_frequency_hz": 160.0,
            "sample_rate_hz": 2048.0,
            "broken_mode": True,
        },
        "recovery": {
            "offset_frequency_hz": 160.0,
            "sample_rate_hz": 2048.0,
            "broken_mode": False,
        },
    },
    "P19": {
        "baseline": {"i_gain": 1.15, "quadrature_error_deg": 8.0, "broken_mode": False},
        "sweep_1": {"i_gain": 1.3, "quadrature_error_deg": 8.0, "broken_mode": False},
        "sweep_2": {"i_gain": 1.15, "quadrature_error_deg": 15.0, "broken_mode": False},
        "broken": {"i_gain": 1.15, "quadrature_error_deg": 8.0, "broken_mode": True},
        "recovery": {"i_gain": 1.15, "quadrature_error_deg": 8.0, "broken_mode": False},
    },
    "P20": {
        "baseline": {"snr_db": 8.0, "record_sample_count": 256, "broken_mode": False},
        "sweep_1": {"snr_db": -10.0, "record_sample_count": 256, "broken_mode": False},
        "sweep_2": {"snr_db": 8.0, "record_sample_count": 512, "broken_mode": False},
        "broken": {"snr_db": 8.0, "record_sample_count": 256, "broken_mode": True},
        "recovery": {"snr_db": 8.0, "record_sample_count": 256, "broken_mode": False},
    },
}


def _p02(p: dict[str, Any]) -> list[float]:
    fs = 12.0 if p["broken_mode"] else float(p["sample_rate_hz"])
    offset = float(p["clock_offset_samples"])
    count = round(fs)
    dense_t = np.linspace(0.0, 1.0, 2000, endpoint=False)
    sample_t = (np.arange(count) + offset) / fs
    samples = np.cos(2 * np.pi * 7 * sample_t + np.pi / 5)
    dense = np.cos(2 * np.pi * 7 * dense_t + np.pi / 5)
    estimate = np.interp(dense_t, sample_t, samples, left=samples[0], right=samples[-1])
    reflected = np.cos(
        2 * np.pi * abs(7 - fs) * sample_t - np.pi / 5 + 2 * np.pi * offset
    )
    high = np.cos(2 * np.pi * (7 + fs) * sample_t + np.pi / 5 - 2 * np.pi * offset)
    return [
        fs,
        offset,
        count,
        np.sqrt(np.mean((estimate - dense) ** 2)),
        np.max(np.abs(samples - reflected)),
        np.max(np.abs(samples - high)),
    ]


def _p03(p: dict[str, Any]) -> list[float]:
    frequency = float(p["input_frequency_hz"])
    fs = float(p["sample_rate_hz"])
    signed = frequency - round(frequency / fs) * fs
    apparent = abs(signed)
    phase = np.pi / 5 if signed >= 0 or p["broken_mode"] else -np.pi / 5
    time = np.arange(round(0.2 * fs)) / fs
    samples = np.cos(2 * np.pi * frequency * time + np.pi / 5)
    alias = np.cos(2 * np.pi * apparent * time + phase)
    ratio = np.dot(samples[1:-1], samples[:-2] + samples[2:]) / (
        2 * np.dot(samples[1:-1], samples[1:-1])
    )
    estimate = fs * np.arccos(np.clip(ratio, -1, 1)) / (2 * np.pi)
    return [frequency, fs, signed, apparent, estimate, np.max(np.abs(samples - alias))]


def _quantize(signal: np.ndarray, bits: int) -> tuple[np.ndarray, np.ndarray, float]:
    step = 2.0 / 2**bits
    clipped = np.clip(signal, -1.0, np.nextafter(1.0, -np.inf))
    codes = np.clip(np.floor((clipped + 1.0) / step).astype(int), 0, 2**bits - 1)
    return -1.0 + (codes + 0.5) * step, codes, step


def _p04(p: dict[str, Any]) -> list[float]:
    bits = int(p["bit_depth"])
    amplitude = float(p["amplitude_v"])
    time = np.arange(1024) / 4096
    signal = amplitude * np.sin(2 * np.pi * 128 * time)
    _, _, step = _quantize(signal, bits)
    if p["dither_enabled"]:
        rng = np.random.default_rng(404)
        signal = signal + (rng.random(1024) - rng.random(1024)) * step
    if p["broken_mode"]:
        signal = 1.35 * np.sin(2 * np.pi * 128 * time)
    quantized, _, step = _quantize(signal, bits)
    error = quantized - signal
    valid = np.abs(signal) < 1
    sqnr = 10 * np.log10(np.mean(signal**2) / np.mean(error**2))
    return [
        bits,
        amplitude,
        float(p["dither_enabled"]),
        step,
        sqnr,
        np.max(np.abs(error[valid])),
        np.count_nonzero(~valid),
    ]


def _noise_normalize(values: np.ndarray, rms: float) -> np.ndarray:
    values = values - np.mean(values)
    return values * rms / np.sqrt(np.mean(values**2))


def _p05(p: dict[str, Any]) -> list[float]:
    alpha = float(p["colored_memory"])
    offset = float(p["interferer_offset_hz"])
    rms = float(p["noise_rms_v"])
    count, fs = 4096, 4096.0
    time = np.arange(count) / fs
    rng = np.random.default_rng(505)
    white = rng.standard_normal(count)
    colored = np.empty(count)
    colored[0] = white[0]
    for index in range(1, count):
        colored[index] = alpha * colored[index - 1] + white[index]
    narrow = np.sin(2 * np.pi * (512 + offset) * time + 0.3)
    impulsive = rng.standard_normal(count)
    mask = rng.random(count) < 0.01
    impulsive[mask] += 12 * rng.choice(np.array([-1.0, 1.0]), np.count_nonzero(mask))
    raw = [white, colored, narrow, impulsive]
    records = (
        raw if p["broken_mode"] else [_noise_normalize(value, rms) for value in raw]
    )
    white_rms = np.sqrt(np.mean(records[0] ** 2))
    colored_lag = np.corrcoef(records[1][:-1], records[1][1:])[0, 1]
    impulsive_rms = np.sqrt(np.mean(records[3] ** 2))
    crest = np.max(np.abs(records[3])) / impulsive_rms
    tone = 0.18 * np.sin(2 * np.pi * 512 * time)
    basis = np.exp(-1j * 2 * np.pi * 512 * time)
    estimate = 2 * abs(np.vdot(basis, tone + records[2])) / count
    residual = max(
        abs(np.sqrt(np.mean(_noise_normalize(value, rms) ** 2)) - rms) for value in raw
    )
    return [
        alpha,
        offset,
        rms,
        white_rms,
        colored_lag,
        crest,
        abs(estimate - 0.18),
        residual,
    ]


def _resonator(signal: np.ndarray, radius: float) -> np.ndarray:
    output = np.zeros_like(signal)
    coefficient = 2 * radius * np.cos(2 * np.pi * 90 / 1000)
    for index in range(len(signal)):
        output[index] = 0.15 * signal[index]
        if index >= 1:
            output[index] += coefficient * output[index - 1]
        if index >= 2:
            output[index] -= radius**2 * output[index - 2]
    return output


def _p06(p: dict[str, Any]) -> list[float]:
    delay = int(p["echo_delay_samples"])
    radius = float(p["resonator_radius"])
    signal = np.random.default_rng(606).standard_normal(256)
    delay_h = np.r_[np.zeros(18), 1.0]
    ma_h = np.ones(9) / 9
    echo_h = np.r_[1.0, np.zeros(delay - 1), 0.55]
    impulse = np.zeros(256)
    impulse[0] = 1
    resonator_h = _resonator(impulse, radius)
    direct_delay = np.pad(signal, (18, 0))[:256]
    direct_ma = np.array(
        [np.mean(signal[max(0, i - 8) : i + 1]) * min(i + 1, 9) / 9 for i in range(256)]
    )
    direct_echo = signal.copy()
    direct_echo[delay:] += 0.55 * signal[:-delay]
    direct_resonator = _resonator(signal, radius)
    direct = [direct_delay, direct_ma, direct_echo, direct_resonator]
    impulses = [delay_h, ma_h, echo_h, resonator_h]
    errors = [
        np.max(np.abs(value - np.convolve(signal, h)[:256]))
        for value, h in zip(direct, impulses, strict=True)
    ]
    linear = np.convolve(signal, echo_h)[:256]
    circular = np.fft.ifft(np.fft.fft(signal) * np.fft.fft(echo_h, 256)).real
    wrap_error = np.max(np.abs(circular - linear))
    display_error = wrap_error if p["broken_mode"] else 0.0
    return [delay, radius, *errors, wrap_error, display_error]


def _p07(p: dict[str, Any]) -> list[float]:
    delay = int(p["middle_echo_delay_samples"])
    gain = float(p["third_echo_gain"])
    pulse = np.zeros(40)
    pulse[5:12] = [0.2, 0.7, 1, 0.8, 0.45, 0.15, -0.1]
    delays, gains = [0, delay, 9], [1.0, 0.6, gain]
    paths = []
    for lag, scale in zip(delays, gains, strict=True):
        path = np.zeros(49)
        path[lag : lag + 40] = scale * pulse
        paths.append(path)
    explicit = sum(paths)
    impulse = np.zeros(10)
    for lag, scale in zip(delays, gains, strict=True):
        impulse[lag] += scale
    manual = np.zeros(49)
    for index, value in enumerate(pulse):
        for lag, scale in zip(delays, gains, strict=True):
            manual[index + lag] += value * scale
    overwritten = np.zeros(49)
    for path in paths:
        overwritten[path != 0] = path[path != 0]
    overwrite_error = np.max(np.abs(explicit - overwritten))
    display_error = overwrite_error if p["broken_mode"] else 0.0
    return [
        delay,
        gain,
        np.max(np.abs(explicit - np.convolve(pulse, impulse))),
        np.max(np.abs(explicit - manual)),
        overwrite_error,
        display_error,
    ]


def _p08(p: dict[str, Any]) -> list[float]:
    amplitude = float(p["target_amplitude"])
    sigma = float(p["noise_sigma"])
    separation = int(p["target_separation_samples"])
    reference = np.repeat(
        np.array([1, 1, -1, 1, -1, -1, 1, -1, 1, 1, 1, -1, -1], dtype=float), 2
    )
    record = sigma * np.random.default_rng(808).standard_normal(256)
    record[137 : 137 + len(reference)] += amplitude * reference
    record[137 + separation : 137 + separation + len(reference)] += (
        0.55 * amplitude * reference
    )
    correlation = np.correlate(record, reference, mode="full")
    convolution = np.convolve(record, reference[::-1], mode="full")
    peak = int(np.argmax(correlation))
    recovered = peak - (len(reference) - 1)
    displayed = peak if p["broken_mode"] else recovered
    return [
        amplitude,
        sigma,
        separation,
        recovered,
        displayed,
        np.max(np.abs(correlation - convolution)),
    ]


def _fir(taps: int) -> np.ndarray:
    index = np.arange(taps) - (taps - 1) / 2
    values = 0.24 * np.sinc(0.24 * index) * np.hamming(taps)
    return values / np.sum(values)


def _p09(p: dict[str, Any]) -> list[float]:
    taps = int(p["fir_taps"])
    q = float(p["iir_q"])
    omega_c = 2 * np.pi * 100 / 1000
    alpha = np.sin(omega_c) / (2 * q)
    cosine = np.cos(omega_c)
    numerator = np.array([(1 - cosine) / 2, 1 - cosine, (1 - cosine) / 2]) / (1 + alpha)
    denominator = np.array([1.0, -2 * cosine / (1 + alpha), (1 - alpha) / (1 + alpha)])
    omega = np.linspace(0, np.pi, 160)
    z = np.exp(-1j * omega)
    response = sum(value * z**i for i, value in enumerate(numerator)) / sum(
        value * z**i for i, value in enumerate(denominator)
    )
    fir = _fir(taps)
    fir_response = sum(value * z**i for i, value in enumerate(fir))
    radius = 1.02 if p["broken_mode"] else 0.98
    pole_angle = 2 * np.pi * 90 / 1000
    pole_output = np.zeros(400)
    pole_output[0] = 1 - radius
    for index in range(1, len(pole_output)):
        pole_output[index] += 2 * radius * np.cos(pole_angle) * pole_output[index - 1]
        if index >= 2:
            pole_output[index] -= radius**2 * pole_output[index - 2]
    displayed_tail_ratio = abs(pole_output[-1]) / max(abs(pole_output[20]), 1e-30)
    return [
        taps,
        q,
        np.max(np.abs(response)),
        np.mean(np.abs(fir_response)[-30:] ** 2),
        taps,
        5,
        displayed_tail_ratio,
    ]


def _lp(taps: int, gain: float = 1.0) -> np.ndarray:
    index = np.arange(taps) - (taps - 1) / 2
    values = 0.2 * np.sinc(0.2 * index) * np.hamming(taps)
    return gain * values / np.sum(values)


def _amplitude(signal: np.ndarray, frequency: float, fs: float) -> float:
    time = np.arange(len(signal)) / fs
    return (
        2
        * abs(np.vdot(np.exp(-1j * 2 * np.pi * frequency * time), signal))
        / len(signal)
    )


def _p10(p: dict[str, Any]) -> list[float]:
    high = float(p["high_tone_hz"])
    taps = int(p["reconstruction_taps"])
    time = np.arange(2400) / 2400
    source = (
        np.sin(2 * np.pi * 90 * time)
        + 0.65 * np.sin(2 * np.pi * high * time)
        + 0.01 * np.random.default_rng(1010).standard_normal(2400)
    )
    filtered = np.convolve(source, _lp(65), mode="same")
    decimated = source[::4] if p["broken_mode"] else filtered[::4]
    fold = abs(high - round(high / 600) * 600)
    folded_amplitude = _amplitude(decimated, fold, 600)
    zeroed = np.zeros(2400)
    zeroed[::4] = decimated
    recovered = (
        zeroed if p["broken_mode"] else np.convolve(zeroed, _lp(taps, 4), mode="same")
    )
    return [
        high,
        taps,
        600,
        fold,
        folded_amplitude,
        _amplitude(recovered, 510, 2400),
        _amplitude(recovered, 90, 2400),
    ]


def _p11(p: dict[str, Any]) -> list[float]:
    count = int(p["record_sample_count"])
    offset = float(p["tone_bin_offset"])
    spacing = 1024.0 / count
    frequency = 144.0 + offset * spacing
    sample = np.arange(count)
    rng = np.random.default_rng(1011)
    noise = (
        0.002
        / np.sqrt(2.0)
        * (rng.standard_normal(count) + 1j * rng.standard_normal(count))
    )
    values = np.exp(1j * (2 * np.pi * frequency * sample / 1024.0 + 0.35)) + noise
    fft_values = np.fft.fft(values)
    explicit = np.array(
        [
            np.sum(values * np.exp(-1j * 2 * np.pi * k * sample / count))
            for k in range(count)
        ]
    )
    magnitude = np.abs(fft_values) / count
    peak = int(np.argmax(magnitude))
    signed = peak if peak <= count // 2 else peak - count
    correct = signed * spacing
    reported = correct + spacing if p["broken_mode"] else correct
    lower = int(np.floor(frequency / spacing)) % count
    upper = (lower + 1) % count
    return [
        count,
        offset,
        spacing,
        frequency,
        peak,
        correct,
        reported,
        np.max(np.abs(explicit - fft_values)),
        magnitude[lower],
        magnitude[upper],
    ]


def _p12_window(name: str) -> np.ndarray:
    index = np.arange(128)
    angle = 2 * np.pi * index / 127
    terms = {
        "Rectangular": np.ones(128),
        "Hann": 0.5 - 0.5 * np.cos(angle),
        "Hamming": 0.54 - 0.46 * np.cos(angle),
        "Blackman": 0.42 - 0.5 * np.cos(angle) + 0.08 * np.cos(2 * angle),
        "Flat-top": 1
        - 1.93 * np.cos(angle)
        + 1.29 * np.cos(2 * angle)
        - 0.388 * np.cos(3 * angle)
        + 0.0322 * np.cos(4 * angle),
    }
    return terms[name]


def _p12(p: dict[str, Any]) -> list[float]:
    names = ["Rectangular", "Hann", "Hamming", "Blackman", "Flat-top"]
    name = str(p["window_name"])
    offset = float(p["tone_bin_offset"])
    sample = np.arange(128)
    tone = np.exp(1j * (2 * np.pi * (17 + offset) * sample / 128 + 0.25))
    rng = np.random.default_rng(1012)
    noise = (
        0.02 / np.sqrt(2.0) * (rng.standard_normal(128) + 1j * rng.standard_normal(128))
    )
    window = _p12_window(name)
    gain = float(np.sum(window) / 128)
    clean = np.abs(np.fft.fft(tone * window, 2048)) / (128 * abs(gain))
    noise_spectrum = np.abs(np.fft.fft(noise * window, 2048)) / (128 * abs(gain))
    peak_index = int(np.argmax(clean))
    peak = float(clean[peak_index])
    above = np.flatnonzero(clean >= peak / np.sqrt(2.0))
    nearby = above[np.abs(above - peak_index) < 128]
    width = (nearby[-1] - nearby[0]) * 1024.0 / 2048
    excluded = {
        "Rectangular": 4,
        "Hann": 8,
        "Hamming": 8,
        "Blackman": 12,
        "Flat-top": 20,
    }[name] * 16
    mask = np.ones(2048, dtype=bool)
    mask[max(0, peak_index - excluded) : min(2048, peak_index + excluded + 1)] = False
    sidelobe = 20 * np.log10(max(np.max(clean[mask]) / peak, 1e-15))
    amplitude_error = 20 * np.log10(max(peak, 1e-15))
    coarse = np.abs(np.fft.fft(tone)) / 128
    offpeak = np.sum(coarse**2) - np.max(coarse) ** 2
    actual_noise = np.median(noise_spectrum)
    clean_offpeak = np.median(clean[mask])
    displayed = clean_offpeak if p["broken_mode"] else actual_noise
    return [
        names.index(name),
        offset,
        gain,
        width,
        amplitude_error,
        sidelobe,
        offpeak,
        actual_noise,
        displayed,
    ]


def _p13(p: dict[str, Any]) -> list[float]:
    padding = int(p["padding_factor"])
    multiplier = int(p["observation_multiplier"])
    count = 128 * multiplier
    sample = np.arange(512)
    values = np.cos(2 * np.pi * 198 * sample / 1024.0) + np.cos(
        2 * np.pi * 202 * sample / 1024.0
    )
    noise = np.random.default_rng(1013).standard_normal(512)
    noise *= 0.002 / np.sqrt(np.mean(noise**2))
    fft_count = count * padding
    spectrum = np.abs(np.fft.rfft((values + noise)[:count], fft_count)) / count
    frequency = np.fft.rfftfreq(fft_count, 1 / 1024.0)
    selected = (frequency >= 180) & (frequency <= 220)
    local_frequency = frequency[selected]
    local_spectrum = spectrum[selected]
    left = np.max(local_spectrum[local_frequency <= 200])
    right = np.max(local_spectrum[local_frequency >= 200])
    center = local_spectrum[int(np.argmin(np.abs(local_frequency - 200)))]
    valley = center / max(min(left, right), 1e-15)
    display_spacing = 1024.0 / fft_count
    rayleigh = 1024.0 / count
    claim = display_spacing if p["broken_mode"] else rayleigh
    return [
        padding,
        multiplier,
        count,
        fft_count,
        display_spacing,
        rayleigh,
        valley,
        claim,
    ]


def _p14_record(seed: int) -> np.ndarray:
    sample = np.arange(4096)
    return (
        np.cos(2 * np.pi * 160 * sample / 1024.0 + 0.3)
        + 0.12 * np.cos(2 * np.pi * 172 * sample / 1024.0 - 0.7)
        + 0.35 * np.random.default_rng(seed).standard_normal(4096)
    )


def _p14_psd(values: np.ndarray, window: np.ndarray) -> np.ndarray:
    density = np.abs(np.fft.rfft(values * window)) ** 2 / (1024.0 * np.sum(window**2))
    density[1:-1] *= 2
    return density


def _p14_welch(values: np.ndarray, length: int, overlap: float) -> np.ndarray:
    hop = round(length * (1 - overlap))
    starts = np.arange(0, 4096 - length + 1, hop)
    window = 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(length) / (length - 1))
    return np.array(
        [_p14_psd(values[start : start + length], window) for start in starts]
    )


def _p14_effective(length: int, overlap: float, count: int) -> float:
    hop = round(length * (1 - overlap))
    window = 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(length) / (length - 1))
    energy = np.sum(window**2)
    correction = 1.0
    for lag in range(1, count):
        shift = lag * hop
        if shift >= length:
            break
        correlation = np.sum(window[:-shift] * window[shift:]) / energy
        correction += 2 * (1 - lag / count) * correlation**2
    return count / correction


def _p14(p: dict[str, Any]) -> list[float]:
    length = int(p["segment_length"])
    overlap = float(p["overlap_fraction"])
    pieces = _p14_welch(_p14_record(1014), length, overlap)
    frequency = np.fft.rfftfreq(length, 1 / 1024.0)
    probe = int(np.argmin(np.abs(frequency - 360)))
    linear_db = 10 * np.log10(max(np.mean(pieces[:, probe]), 1e-20))
    logarithmic_mean = np.mean(10 * np.log10(np.maximum(pieces[:, probe], 1e-20)))
    periodogram_trials = []
    welch_trials = []
    for seed in range(1014, 1038):
        record = _p14_record(seed)
        full_frequency = np.fft.rfftfreq(4096, 1 / 1024.0)
        full = _p14_psd(record, np.ones(4096))
        periodogram_trials.append(full[int(np.argmin(np.abs(full_frequency - 360)))])
        retained = _p14_welch(record, 512, 0.5)
        retained_frequency = np.fft.rfftfreq(512, 1 / 1024.0)
        welch_trials.append(
            np.mean(retained[:, int(np.argmin(np.abs(retained_frequency - 360)))])
        )
    periodogram_cv = np.std(periodogram_trials) / np.mean(periodogram_trials)
    welch_cv = np.std(welch_trials) / np.mean(welch_trials)
    displayed = logarithmic_mean if p["broken_mode"] else linear_db
    effective = _p14_effective(length, overlap, len(pieces))
    return [
        length,
        overlap,
        len(pieces),
        effective,
        1024.0 / 4096,
        1024.0 / length,
        periodogram_cv,
        welch_cv,
        linear_db,
        logarithmic_mean,
        displayed,
    ]


def _p15_signal() -> np.ndarray:
    sample = np.arange(4096)
    time = sample / 1024.0
    values = 0.35 * np.cos(2 * np.pi * 90 * time + 0.2)
    gate = (time >= 0.5) & (time < 2.25)
    local_time = time - 0.5
    slope = 100 / 1.75
    values += (
        0.25
        * np.cos(2 * np.pi * (220 * local_time + 0.5 * slope * local_time**2) - 0.4)
        * gate
    )
    burst = (sample >= 1536) & (sample < 1600)
    values += 0.8 * np.cos(2 * np.pi * 380 * time + 0.7) * burst
    hop_phase = np.where(
        time < 2.75,
        2 * np.pi * 156 * time - 0.3,
        2 * np.pi * (156 * 2.75 + 174 * (time - 2.75)) - 0.3,
    )
    values += 0.28 * np.cos(hop_phase)
    return values + 0.02 * np.random.default_rng(1015).standard_normal(4096)


def _p15_stft(
    length: int, overlap: float, fft_length: int | None = None
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    fft_length = length if fft_length is None else fft_length
    hop = round(length * (1 - overlap))
    starts = np.arange(0, 4096 - length + 1, hop)
    window = 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(length) / (length - 1))
    scale = 1024.0 * np.sum(window**2)
    columns = []
    values = _p15_signal()
    for start in starts:
        density = (
            np.abs(np.fft.rfft(values[start : start + length] * window, fft_length))
            ** 2
            / scale
        )
        density[1:-1] *= 2
        columns.append(density)
    return (
        np.fft.rfftfreq(fft_length, 1 / 1024.0),
        (starts + (length - 1) / 2) / 1024.0,
        np.array(columns).T,
    )


def _p15(p: dict[str, Any]) -> list[float]:
    length = int(p["window_length"])
    overlap = float(p["overlap_fraction"])
    frequency, frame_time, density = _p15_stft(length, overlap)
    burst_bin = int(np.argmin(np.abs(frequency - 380)))
    burst_time = frame_time[int(np.argmax(density[burst_bin]))]
    burst_error = abs(burst_time - (1536 + 31.5) / 1024.0)
    before = int(np.argmin(np.abs(frame_time - 2.65)))
    after = int(np.argmin(np.abs(frame_time - 2.85)))
    before_156 = density[int(np.argmin(np.abs(frequency - 156))), before]
    before_174 = density[int(np.argmin(np.abs(frequency - 174))), before]
    after_156 = density[int(np.argmin(np.abs(frequency - 156))), after]
    after_174 = density[int(np.argmin(np.abs(frequency - 174))), after]
    contrast = 10 * np.log10(
        max(before_156 * after_174, 1e-30) / max(before_174 * after_156, 1e-30)
    )
    chirp_frames = (frame_time >= 0.6) & (frame_time <= 2.15)
    chirp_band = (frequency >= 200) & (frequency <= 340)
    chirp_frequency = frequency[chirp_band]
    chirp_density = density[np.ix_(chirp_band, chirp_frames)]
    ridge = chirp_frequency[np.argmax(chirp_density, axis=0)]
    expected_ridge = 220 + (100 / 1.75) * (frame_time[chirp_frames] - 0.5)
    chirp_rmse = np.sqrt(np.mean((ridge - expected_ridge) ** 2))
    physical = 4 * 1024.0 / length
    claim = 2.0 if p["broken_mode"] else physical
    return [
        length,
        overlap,
        len(frame_time),
        np.mean(np.diff(frame_time)),
        1024.0 / length,
        physical,
        burst_error,
        contrast,
        claim,
        chirp_rmse,
    ]


def _p16(p: dict[str, Any]) -> list[float]:
    depth = float(p["envelope_depth"])
    deviation = float(p["phase_deviation_rad"])
    sample = np.arange(4096)
    time = sample / 2048.0
    envelope = 1 + depth * np.cos(2 * np.pi * 2 * time)
    phase = 2 * np.pi * 240 * time + 0.35 + deviation * np.sin(2 * np.pi * 3 * time)
    designed_frequency = 240 + 3 * deviation * np.cos(2 * np.pi * 3 * time)
    rng = np.random.default_rng(1016)
    if p["broken_mode"]:
        envelope = 1 - 0.999 * np.exp(-0.5 * ((time - 1) / 0.025) ** 2)
        noise = 0.010 * rng.standard_normal(4096)
    else:
        noise = 0.002 * rng.standard_normal(4096)
    observed = envelope * np.cos(phase) + noise
    mask = np.r_[1.0, np.full(2047, 2.0), 1.0, np.zeros(2047)]
    analytic = np.fft.ifft(np.fft.fft(observed) * mask)
    recovered_envelope = np.abs(analytic)
    recovered_phase = np.unwrap(np.angle(analytic))
    raw_frequency = np.r_[240.0, np.diff(recovered_phase) * 2048.0 / (2 * np.pi)]
    reliable = recovered_envelope >= 0.05
    reliable[1:] &= reliable[:-1]
    reliable[:128] = False
    reliable[-128:] = False
    evaluation = np.zeros(4096, dtype=bool)
    evaluation[128:-128] = True
    envelope_rmse = np.sqrt(
        np.mean((recovered_envelope[evaluation] - envelope[evaluation]) ** 2)
    )
    frequency_rmse = np.sqrt(
        np.mean((raw_frequency[reliable] - designed_frequency[reliable]) ** 2)
    )
    spectrum = np.fft.fftshift(np.fft.fft(analytic)) / 4096
    frequency = np.fft.fftshift(np.fft.fftfreq(4096, 1 / 2048.0))
    suppression = 10 * np.log10(
        max(np.sum(np.abs(spectrum[frequency > 0]) ** 2), 1e-30)
        / max(np.sum(np.abs(spectrum[frequency < 0]) ** 2), 1e-30)
    )
    low = recovered_envelope < 0.05
    spike = (
        np.max(np.abs(raw_frequency[low] - designed_frequency[low]))
        if np.any(low)
        else 0.0
    )
    withheld = np.count_nonzero(evaluation & ~reliable)
    return [
        depth,
        deviation,
        envelope_rmse,
        frequency_rmse,
        suppression,
        np.min(recovered_envelope),
        spike,
        withheld,
    ]


def _p17_fir() -> np.ndarray:
    centered = np.arange(129) - 64
    values = 2 * 80 / 2048.0 * np.sinc(2 * 80 * centered / 2048.0) * np.hamming(129)
    return values / np.sum(values)


def _p17_case(lo_frequency: float, lo_phase: float, broken: bool) -> list[float]:
    time = np.arange(4096) / 2048.0
    passband = np.cos(2 * np.pi * 240 * time + 0.35) + 0.002 * np.random.default_rng(
        1017
    ).standard_normal(4096)
    oscillator = np.exp(
        1j * ((1 if broken else -1) * 2 * np.pi * lo_frequency * time - lo_phase)
    )
    mixed = passband * oscillator
    filtered = np.convolve(mixed, _p17_fir(), mode="same")
    baseband = 2 * filtered
    selected = slice(192, -192)
    adjacent = np.conj(baseband[selected][:-1]) * baseband[selected][1:]
    estimated = np.angle(np.sum(adjacent)) * 2048.0 / (2 * np.pi)
    expected = 240 - lo_frequency
    reference = np.exp(1j * (2 * np.pi * expected * time[selected] + 0.35 - lo_phase))
    projection = np.mean(baseband[selected] * np.conj(reference))
    image = -(240 + lo_frequency)
    image_reference = np.exp(1j * 2 * np.pi * image * time[selected])
    before = abs(np.mean(mixed[selected] * np.conj(image_reference)))
    after = abs(np.mean(filtered[selected] * np.conj(image_reference)))
    suppression = 20 * np.log10(max(before, 1e-15) / max(after, 1e-15))
    return [expected, estimated, abs(projection), np.angle(projection), suppression]


def _p17(p: dict[str, Any]) -> list[float]:
    lo_frequency = float(p["lo_frequency_hz"])
    lo_phase = float(p["lo_phase_rad"])
    current = _p17_case(lo_frequency, lo_phase, bool(p["broken_mode"]))
    broken_frequency = _p17_case(216, 0, True)[1]
    recovered_frequency = _p17_case(216, 0, False)[1]
    return [lo_frequency, lo_phase, *current, broken_frequency, recovered_frequency]


def _p18_case(offset: float, rate: float, broken: bool) -> list[float]:
    count = int(rate * 0.5)
    time = np.arange(count) / rate
    positive = np.exp(1j * (2 * np.pi * offset * time + 0.35))
    rng = np.random.default_rng(1018)
    positive += (
        0.002
        / np.sqrt(2.0)
        * (rng.standard_normal(count) + 1j * rng.standard_normal(count))
    )
    negative = np.conj(positive)
    real_positive = positive.real
    real_negative = negative.real
    selected_positive = real_positive.astype(complex) if broken else positive
    selected_negative = real_negative.astype(complex) if broken else negative
    positive_estimate = (
        np.angle(np.sum(np.conj(selected_positive[:-1]) * selected_positive[1:]))
        * rate
        / (2 * np.pi)
    )
    negative_estimate = (
        np.angle(np.sum(np.conj(selected_negative[:-1]) * selected_negative[1:]))
        * rate
        / (2 * np.pi)
    )
    positive_alias = (offset + rate / 2) % rate - rate / 2
    negative_alias = (-offset + rate / 2) % rate - rate / 2
    rmse = np.sqrt(np.mean((real_positive - real_negative) ** 2))
    return [positive_alias, negative_alias, positive_estimate, negative_estimate, rmse]


def _p18_downconversion(offset: float) -> list[float]:
    time = np.arange(4096) / 2048.0
    upper = np.exp(1j * (2 * np.pi * (600 + offset) * time + 0.35))
    lower = np.exp(1j * (2 * np.pi * (600 - offset) * time - 0.35))
    oscillator = np.exp(-1j * 2 * np.pi * 600 * time)
    upper_complex = upper * oscillator
    lower_complex = lower * oscillator
    centered = np.arange(129) - 64
    taps = 2 * 450 / 2048.0 * np.sinc(2 * 450 * centered / 2048.0) * np.hamming(129)
    taps /= np.sum(taps)
    real_lo = 2 * np.cos(2 * np.pi * 600 * time)
    upper_real = np.convolve(upper.real * real_lo, taps, mode="same")
    lower_real = np.convolve(lower.real * real_lo, taps, mode="same")
    upper_frequency = (
        np.angle(np.sum(np.conj(upper_complex[:-1]) * upper_complex[1:]))
        * 2048.0
        / (2 * np.pi)
    )
    lower_frequency = (
        np.angle(np.sum(np.conj(lower_complex[:-1]) * lower_complex[1:]))
        * 2048.0
        / (2 * np.pi)
    )
    collapse = np.sqrt(np.mean((upper_real[192:-192] - lower_real[192:-192]) ** 2))
    return [upper_frequency, lower_frequency, collapse]


def _p18(p: dict[str, Any]) -> list[float]:
    offset = float(p["offset_frequency_hz"])
    rate = float(p["sample_rate_hz"])
    current = _p18_case(offset, rate, bool(p["broken_mode"]))
    broken = _p18_case(160, 2048, True)
    recovered = _p18_case(160, 2048, False)
    return [
        offset,
        rate,
        *current,
        broken[2],
        broken[3],
        recovered[2],
        recovered[3],
        *_p18_downconversion(offset),
    ]


def _p19_metrics(values: np.ndarray, phase: np.ndarray) -> list[float]:
    centered_i = values.real - np.mean(values.real)
    centered_q = values.imag - np.mean(values.imag)
    desired = abs(np.mean(values * np.exp(-1j * phase)))
    image = abs(np.mean(values * np.exp(1j * phase)))
    irr = 20 * np.log10(max(desired, 1e-12) / max(image, 1e-12))
    dc = 20 * np.log10(max(abs(np.mean(values)), 1e-12) / max(desired, 1e-12))
    correlation = np.mean(centered_i * centered_q) / np.sqrt(
        np.mean(centered_i**2) * np.mean(centered_q**2)
    )
    eigenvalues = np.linalg.eigvalsh(np.cov(np.vstack((centered_i, centered_q))))
    axis_ratio = np.sqrt(max(eigenvalues) / max(min(eigenvalues), 1e-15))
    return [dc, irr, correlation, axis_ratio]


def _p19_case(
    i_gain: float, error_deg: float, broken: bool
) -> tuple[list[list[float]], list[float], list[list[float]]]:
    time = np.arange(4096) / 2048.0
    phase = 2 * np.pi * 160 * time + 0.35
    rng = np.random.default_rng(1019)
    clean = np.exp(1j * phase) + 0.002 / np.sqrt(2.0) * (
        rng.standard_normal(4096) + 1j * rng.standard_normal(4096)
    )
    error = np.deg2rad(error_deg)
    dc_only = clean.real + 0.12 + 1j * (clean.imag - 0.08)
    gain_only = i_gain * clean.real + 1j * 0.85 * clean.imag
    phase_only = clean.real + 1j * (
        clean.imag * np.cos(error) + clean.real * np.sin(error)
    )
    impaired = (
        i_gain * clean.real
        + 0.12
        + 1j * (0.85 * (clean.imag * np.cos(error) + clean.real * np.sin(error)) - 0.08)
    )
    mean_corrected = impaired - np.mean(impaired)
    estimated_i = np.sqrt(2 * np.mean(mean_corrected.real**2))
    estimated_q = np.sqrt(2 * np.mean(mean_corrected.imag**2))
    normalized_i = mean_corrected.real / estimated_i
    normalized_q = mean_corrected.imag / estimated_q
    normalized = normalized_i + 1j * normalized_q
    estimated_error = np.arcsin(
        np.clip(2 * np.mean(normalized_i * normalized_q), -1, 1)
    )
    if broken:
        corrected = normalized * np.exp(-1j * estimated_error)
    else:
        corrected = normalized_i + 1j * (
            normalized_q - normalized_i * np.sin(estimated_error)
        ) / np.cos(estimated_error)
    stages = [
        _p19_metrics(value, phase)
        for value in [impaired, mean_corrected, normalized, corrected]
    ]
    estimates = [estimated_i, estimated_q, np.rad2deg(estimated_error)]
    isolated = [
        _p19_metrics(value, phase)
        for value in [clean, dc_only, gain_only, phase_only, impaired]
    ]
    return stages, estimates, isolated


def _p19(p: dict[str, Any]) -> list[float]:
    i_gain = float(p["i_gain"])
    error = float(p["quadrature_error_deg"])
    stages, estimates, isolated = _p19_case(i_gain, error, bool(p["broken_mode"]))
    broken, _, _ = _p19_case(1.15, 8, True)
    recovered, _, _ = _p19_case(1.15, 8, False)
    return [
        i_gain,
        error,
        *stages[0],
        stages[-1][1],
        stages[-1][2],
        stages[-1][3],
        *estimates,
        broken[-1][1],
        recovered[-1][1],
        isolated[1][0],
        isolated[2][1],
        isolated[3][1],
    ]


def _p20_estimate(values: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    count = len(values)
    magnitude = np.abs(np.fft.fft(values)) / count
    peak = int(np.argmax(magnitude))
    signed = peak if peak < count // 2 else peak - count
    peak_frequency = signed * 1024.0 / count
    left = np.log(max(magnitude[(peak - 1) % count], 1e-15))
    center = np.log(max(magnitude[peak], 1e-15))
    right = np.log(max(magnitude[(peak + 1) % count], 1e-15))
    denominator = left - 2 * center + right
    offset = np.clip(0.5 * (left - right) / denominator, -0.5, 0.5)
    interpolated = (signed + offset) * 1024.0 / count
    adjacent = np.conj(values[:-1]) * values[1:]
    coherent = np.sum(adjacent)
    increment = np.angle(coherent) * 1024.0 / (2 * np.pi)
    coherence = abs(coherent) / np.sum(np.abs(adjacent))
    frequencies = np.array([peak_frequency, interpolated, increment])
    time = np.arange(count) / 1024.0
    phases = np.array(
        [
            np.angle(np.sum(values * np.exp(-1j * 2 * np.pi * frequency * time)))
            for frequency in frequencies
        ]
    )
    return frequencies, phases, coherence


def _p20_trial(
    snr: float, count: int, seed: int, amplitude: float = 1.0
) -> tuple[np.ndarray, np.ndarray, float]:
    time = np.arange(count) / 1024.0
    clean = amplitude * np.exp(1j * (2 * np.pi * 123.25 * time + 2.70))
    rng = np.random.default_rng(seed)
    noise = (
        10 ** (-snr / 20)
        / np.sqrt(2)
        * (rng.standard_normal(count) + 1j * rng.standard_normal(count))
    )
    return _p20_estimate(clean + noise)


def _p20_monte_carlo(snr: float, count: int) -> list[float]:
    frequency_errors = []
    phase_errors = []
    coherences = []
    for trial in range(40):
        frequencies, phases, coherence = _p20_trial(snr, count, 2020 + trial)
        frequency_errors.append(frequencies - 123.25)
        phase_errors.append(np.arctan2(np.sin(phases - 2.70), np.cos(phases - 2.70)))
        coherences.append(coherence)
    frequency_errors_array = np.array(frequency_errors)
    phase_errors_array = np.array(phase_errors)
    return [
        np.mean(frequency_errors_array, axis=0)[2],
        np.std(frequency_errors_array, axis=0, ddof=1)[2],
        np.sqrt(np.mean(phase_errors_array**2, axis=0))[2],
        np.mean(coherences),
    ]


def _p20(p: dict[str, Any]) -> list[float]:
    snr = float(p["snr_db"])
    count = int(p["record_sample_count"])
    frequencies, phases, coherence = _p20_trial(snr, count, 1020)
    total = 2 * np.pi * 123.25 * (count - 1) / 1024.0
    wrapped = np.arctan2(np.sin(total), np.cos(total))
    broken_endpoint = wrapped * 1024.0 / (2 * np.pi * (count - 1))
    time = np.arange(count) / 1024.0
    clean = np.exp(1j * (2 * np.pi * 123.25 * time + 2.70))
    recovered = _p20_estimate(clean)[0][2]
    low_frequencies, _, low_coherence = _p20_trial(-20, count, 1119, 0.02)
    low_reported = low_frequencies[2] if low_coherence >= 0.2 else 0.0
    reported = broken_endpoint if p["broken_mode"] else frequencies[2]
    return [
        snr,
        count,
        *frequencies,
        *phases,
        coherence,
        broken_endpoint,
        recovered,
        low_coherence,
        low_reported,
        reported,
        *_p20_monte_carlo(snr, count),
    ]


_REFERENCES = {
    "P02": _p02,
    "P03": _p03,
    "P04": _p04,
    "P05": _p05,
    "P06": _p06,
    "P07": _p07,
    "P08": _p08,
    "P09": _p09,
    "P10": _p10,
    "P11": _p11,
    "P12": _p12,
    "P13": _p13,
    "P14": _p14,
    "P15": _p15,
    "P16": _p16,
    "P17": _p17,
    "P18": _p18,
    "P19": _p19,
    "P20": _p20,
}


def expected_signature(item_id: str, scenario: str) -> list[float]:
    """Return a separately formulated numeric signature for one retained scenario."""

    return [
        float(value) for value in _REFERENCES[item_id](SCENARIOS[item_id][scenario])
    ]


# P21-P28: independent formulations. Shared seeded inputs define reproducible
# Python scenarios; they do not claim the MATLAB random streams are identical.


def _p21(p: dict[str, Any]) -> list[float]:
    from scipy.signal import hilbert

    depth = 1.4 if p["broken_mode"] else p["modulation_depth"]
    frequency = p["message_frequency_hz"]
    t = np.arange(2000) / 20000
    noise = np.random.default_rng(1021).normal(size=2000) * 0.005
    carrier = np.cos(6000 * np.pi * t)
    message = np.cos(2 * np.pi * frequency * t)
    voltage = (1 + depth * message) * carrier + noise
    envelope = (np.abs(hilbert(voltage)) - 1) / depth
    # Real Fourier-series projection, independently expressing the 900 Hz LPF.
    basis = 2 * np.pi * np.arange(1, 91)[:, None] * 10 * t
    mixed = 2 * voltage * carrier
    dc = np.mean(mixed)
    recovered = (
        dc
        + 2
        / 2000
        * (
            (np.cos(basis) @ mixed) @ np.cos(basis)
            + (np.sin(basis) @ mixed) @ np.sin(basis)
        )
        - 1
    ) / depth
    amplitude = lambda f, v: 2 * abs(np.sum(v * np.exp(-2j * np.pi * f * t))) / 2000
    multi = (
        1
        + p["modulation_depth"]
        * (0.6 * np.cos(200 * np.pi * t) + 0.4 * np.cos(700 * np.pi * t))
    ) * carrier + noise
    return [
        depth,
        frequency,
        amplitude(3000, voltage),
        amplitude(3000 - frequency, voltage),
        amplitude(3000 + frequency, voltage),
        np.min(1 + depth * message),
        np.linalg.norm(envelope - message) / np.sqrt(2000),
        np.linalg.norm(recovered - message) / np.sqrt(2000),
        *[amplitude(f, multi) for f in [2650, 2900, 3100, 3350]],
    ]


def _p22(p: dict[str, Any]) -> list[float]:
    from scipy.special import jv

    deviation, fm = p["deviation_hz"], p["message_frequency_hz"]

    def bandwidth(d, f):
        orders = np.arange(-150, 151)
        power = jv(orders, d / f) ** 2
        return (
            2
            * f
            * next(
                k
                for k in range(151)
                if np.sum(power[abs(orders) <= k]) >= 0.98 * np.sum(power)
            )
        )

    def phase_errors(fs, fc, d, f):
        t = np.arange(round(0.2 * fs)) / fs
        theta = 2 * np.pi * fc * t + d / f * np.sin(2 * np.pi * f * t)
        delta = np.diff(theta)
        derivative = ((delta + np.pi) % (2 * np.pi) - np.pi) * fs / (2 * np.pi)
        error = abs(derivative - (fc + d * np.cos(2 * np.pi * f * t[1:])))
        return np.mean(error > 6000), np.max(error)

    alias, error = (
        phase_errors(24000, 8000, 5000, 100)
        if p["broken_mode"]
        else phase_errors(24000, 3000, deviation, fm)
    )
    recovery_bw = bandwidth(5000, 100)
    return [
        deviation / fm,
        bandwidth(deviation, fm),
        2 * (deviation + fm),
        0,
        alias,
        error,
        recovery_bw,
        phase_errors(30000, 8000, 5000, 100)[1],
        15000 - 8000 - recovery_bw / 2,
    ]


def _p23(p: dict[str, Any]) -> list[float]:
    snr, phase = (16, 55) if p["broken_mode"] else (p["ebn0_db"], p["phase_error_deg"])
    rng = np.random.default_rng(1023)
    b = 2 * (rng.random(400) >= 0.5).astype(int) - 1
    q = 2 * (rng.random((2, 400)) >= 0.5).astype(int) - 1
    br, _bi, qr, qi = [rng.normal(size=400) for _ in range(4)]
    c, s = np.cos(np.deg2rad(phase)), np.sin(np.deg2rad(phase))
    sb, sq = (2 * 10 ** (snr / 10)) ** -0.5, (4 * 10 ** (snr / 10)) ** -0.5
    observed_b = b * c + sb * br
    observed_i = (q[0] * c - q[1] * s) / np.sqrt(2) + sq * qr
    observed_q = (q[0] * s + q[1] * c) / np.sqrt(2) + sq * qi
    corrected_i = c * observed_i + s * observed_q
    corrected_q = -s * observed_i + c * observed_q
    return [
        snr,
        phase,
        1,
        1,
        sb,
        sq,
        np.mean(np.sign(observed_b) != b),
        (
            np.count_nonzero(np.sign(observed_i) != q[0])
            + np.count_nonzero(np.sign(observed_q) != q[1])
        )
        / 800,
        (
            np.count_nonzero(np.sign(corrected_i) != q[0])
            + np.count_nonzero(np.sign(corrected_q) != q[1])
        )
        / 800,
    ]


def _oracle_rrc(alpha, span):
    x = np.linspace(-span / 2, span / 2, span * 8 + 1)
    y = np.zeros_like(x)
    zero = x == 0
    singular = np.isclose(abs(x), 1 / (4 * alpha), atol=1e-12, rtol=0)
    regular = ~(zero | singular)
    t = x[regular]
    # sinc form keeps the removable zero branch separate from ±1/(4 alpha).
    y[regular] = (
        np.sinc((1 - alpha) * t) * (1 - alpha)
        + 4 * alpha / np.pi * np.cos(np.pi * (1 + alpha) * t)
    ) / (1 - 16 * alpha**2 * t * t)
    y[zero] = 1 - alpha + 4 * alpha / np.pi
    y[singular] = (
        alpha
        / np.sqrt(2)
        * (
            (1 + 2 / np.pi) * np.sin(np.pi / (4 * alpha))
            + (1 - 2 / np.pi) * np.cos(np.pi / (4 * alpha))
        )
    )
    return y / np.linalg.norm(y)


def _p24(p: dict[str, Any]) -> list[float]:
    from scipy.signal import fftconvolve

    alpha, span = p["rolloff"], p["span_symbols"]
    rng = np.random.default_rng(1024)
    bits = rng.random((2, 320)) >= 0.5
    symbols = (
        (2 * bits[0].astype(int) - 1) + 1j * (2 * bits[1].astype(int) - 1)
    ) / np.sqrt(2)
    impulses = np.zeros(2560, complex)
    impulses[::8] = symbols
    noise = (rng.normal(size=2625) + 1j * rng.normal(size=2625)) * np.sqrt(
        0.5 * 10 ** (-14 / 10)
    )
    pulse = _oracle_rrc(alpha, span)
    tx = fftconvolve(impulses, pulse)
    rx = tx + noise[: len(tx)]
    matched = fftconvolve(rx, pulse[::-1])
    indices = span * 8 + np.arange(320) * 8
    aligned = matched[indices]
    selected = matched[indices + (4 if p["broken_mode"] else 0)]
    raw = rx[span * 4 + np.arange(320) * 8] / pulse[span * 4]
    clean = fftconvolve(tx, pulse[::-1])[indices]
    rectangular = np.ones(8) / np.sqrt(8)
    rect_tx = fftconvolve(impulses, rectangular)
    rect = fftconvolve(rect_tx + noise[: len(rect_tx)], rectangular)[
        7 + np.arange(320) * 8
    ]

    def evm(v):
        error = v[span:-span] - symbols[span:-span]
        return 100 * np.linalg.norm(error) / np.sqrt(320 - 2 * span)

    errors = np.logical_or(
        (selected.real >= 0) != bits[0], (selected.imag >= 0) != bits[1]
    )
    return [
        np.dot(pulse, pulse),
        span * 8,
        evm(rect),
        evm(raw),
        evm(selected),
        evm(clean),
        np.count_nonzero(errors) / 320,
        evm(aligned),
        np.max(abs(pulse - pulse[::-1])),
    ]


def _oracle_channel(echo, lam, deep):
    from scipy.signal import fftconvolve

    rng = np.random.default_rng(1025)
    bits = rng.random((2, 480)) >= 0.5
    symbols = (
        (2 * bits[0].astype(int) - 1) + 1j * (2 * bits[1].astype(int) - 1)
    ) / np.sqrt(2)
    pulse = _oracle_rrc(0.25, 8)
    tx = np.zeros(3840 + 64, complex)
    # Overlap-add the explicit delayed pulse for each symbol, independent of convolution.
    for i, symbol in enumerate(symbols):
        tx[8 * i : 8 * i + 65] += symbol * pulse
    taps = (
        np.array([1, -0.999], complex)
        if deep
        else np.array([1, echo * np.exp(0.45j), 0.2 * np.exp(-0.8j)])
    )
    propagated = np.zeros(len(tx) + 8 * (len(taps) - 1), complex)
    for i, tap in enumerate(taps):
        propagated[8 * i : 8 * i + len(tx)] += tap * tx
    noise = (rng.normal(size=3920) + 1j * rng.normal(size=3920)) * np.sqrt(
        0.5 * 10 ** (-18 / 10)
    )
    matched = fftconvolve(propagated + noise[: len(propagated)], pulse[::-1])
    sampled = matched[64 + 8 * np.arange(480 + len(taps) - 1)]
    inverse = np.zeros(31, complex)
    inverse[0] = 1 / taps[0]
    for k in range(1, 31):
        inverse[k] = (
            -sum(taps[j] * inverse[k - j] for j in range(1, min(k + 1, len(taps))))
            / taps[0]
        )
    rows = np.arange(len(taps) + 30)[:, None] - np.arange(31)[None, :]
    matrix = np.where(
        (rows >= 0) & (rows < len(taps)), taps[np.clip(rows, 0, len(taps) - 1)], 0
    )
    target = np.zeros(len(taps) + 30)
    target[0] = 1
    augmented = np.vstack([matrix, np.sqrt(lam) * np.eye(31)])
    regular = np.linalg.lstsq(augmented, np.r_[target, np.zeros(31)], rcond=None)[0]
    outputs = [
        sampled[:480],
        fftconvolve(sampled, inverse)[:480],
        fftconvolve(sampled, regular)[:480],
    ]
    evm = [100 * np.linalg.norm(v[40:-40] - symbols[40:-40]) / 20 for v in outputs]
    ser = [
        np.mean(
            np.logical_or(
                (v.real[40:-40] >= 0) != bits[0, 40:-40],
                (v.imag[40:-40] >= 0) != bits[1, 40:-40],
            )
        )
        for v in outputs
    ]
    gains = [10 * np.log10(np.vdot(w, w).real) for w in [inverse, regular]]
    residual = 100 * np.linalg.norm(matrix @ regular - target)
    omega = 2 * np.pi * np.arange(2048) / 2048
    response = sum(taps[j] * np.exp(-1j * j * omega) for j in range(len(taps)))
    return [*evm, *ser, *gains, residual, 20 * np.log10(max(min(abs(response)), 1e-12))]


def _p25(p: dict[str, Any]) -> list[float]:
    active = _oracle_channel(p["echo_gain"], p["regularization"], p["broken_mode"])
    deep = _oracle_channel(p["echo_gain"], 0.01, True)
    return [*active, deep[1], deep[2], deep[6], deep[7], deep[8]]


def _oracle_lms(mu, correlation):
    before = np.array([0.8, -0.5, 0.3, 0.2, -0.15, 0.1, 0.05, -0.03])
    after = np.array([0.35, 0.7, -0.45, 0.25, 0.15, -0.1, 0.08, 0.03])
    rng = np.random.default_rng(2601)
    x, other, noise = [rng.normal(size=6000) for _ in range(3)]
    x = x / np.sqrt(np.dot(x, x) / 6000)
    other = other / np.sqrt(np.dot(other, other) / 6000)
    noise = noise / np.sqrt(np.dot(noise, noise) / 6000)
    t = np.arange(6000) / 8000
    desired = 0.25 * np.sin(1400 * np.pi * t) + 0.18 * np.sin(2200 * np.pi * t + 0.4)
    delay = np.lib.stride_tricks.sliding_window_view(np.pad(x, (7, 0)), 8)[:, ::-1]
    interference = np.r_[delay[:3000] @ before, delay[3000:] @ after]
    primary = desired + 0.05 * noise + interference
    ref = correlation * x + np.sqrt(1 - correlation**2) * other
    vectors = np.lib.stride_tricks.sliding_window_view(np.pad(ref, (7, 0)), 8)[:, ::-1]
    weights = np.zeros(8)
    error = []
    residual = []
    mismatch = []
    stop = 6000
    for k, row in enumerate(vectors):
        predicted = np.sum(weights * row)
        e = primary[k] - predicted
        candidate = (np.eye(8) - mu * np.outer(row, row)) @ weights + mu * primary[
            k
        ] * row
        if np.linalg.norm(candidate) > 1e4 or abs(e) > 1e6:
            stop = k
            break
        weights = candidate
        error.append(e)
        residual.append(interference[k] - predicted)
        mismatch.append(
            np.linalg.norm(weights - (before if k < 3000 else after)) / np.sqrt(8)
        )
    if stop < 6000:
        return [], stop + 1
    values = []
    error = np.array(error)
    residual = np.array(residual)
    for a, b in [(1976, 3000), (4976, 6000)]:
        values.extend(
            [
                10
                * np.log10(
                    np.dot(interference[a:b], interference[a:b])
                    / np.dot(residual[a:b], residual[a:b])
                ),
                np.dot(error[a:b], desired[a:b]) / np.dot(desired[a:b], desired[a:b]),
            ]
        )
    count = 0
    reacquired = 3001
    for k, value in enumerate(mismatch[3000:]):
        count = count + 1 if value < 0.08 else 0
        if count == 64:
            reacquired = k + 1
            break
    return [*values, mismatch[2999], mismatch[-1], reacquired], 6001


def _p26(p: dict[str, Any]) -> list[float]:
    stable, _ = _oracle_lms(p["step_size"], p["reference_correlation"])
    _, stop = _oracle_lms(0.35, 1)
    recovery, _ = _oracle_lms(0.006, 1)
    return [*stable, stop, float(not p["broken_mode"]), *recovery[:2]]


def _oracle_interval(k, n):
    # Wilson limits are the roots of the binomial score-test quadratic.
    a = n + 1.96**2
    b = -(2 * k + 1.96**2)
    c = k * k / n
    root = np.sqrt(max(b * b - 4 * a * c, 0))
    return max(0, (-b - root) / (2 * a)), min(1, (-b + root) / (2 * a))


def _p27(p: dict[str, Any]) -> list[float]:
    import math

    rng = np.random.default_rng(2701)
    bits = rng.random(4000) >= 0.5
    noise = rng.normal(size=(16, 4000))
    statistic = (
        2 * bits.astype(int)
        - 1
        + np.sum(noise, axis=0) * np.sqrt(1 / (2 * 10 ** (p["ebn0_db"] / 10))) / 4
    )
    errors = (statistic >= 0) != bits
    n = p["trial_count"]
    k = int(np.count_nonzero(errors[:n]))
    lo, hi = _oracle_interval(k, n)
    active_k = 0 if p["broken_mode"] else k
    alo, ahi = _oracle_interval(active_k, n)
    blocks = np.array(
        [np.mean(errors[start : start + 100]) for start in range(0, 4000, 100)]
    )
    return [
        n,
        p["ebn0_db"],
        active_k / n,
        alo,
        ahi,
        0.5 * math.erfc(np.sqrt(10 ** (p["ebn0_db"] / 10))),
        1 if p["broken_mode"] else n,
        float(not p["broken_mode"]),
        k / n,
        lo,
        hi,
        np.std(blocks, ddof=1),
    ]


def _p28(p: dict[str, Any]) -> list[float]:
    import math

    template = np.array([1, 1, 1, -1, 1, -1, -1, 1, -1, 1, -1, -1, -1, 1, 1, -1])
    rng = np.random.default_rng(2801)
    noise0, noise1 = rng.normal(size=(16, 12000)), rng.normal(size=(16, 12000))
    projection0 = template @ noise0 / 4
    projection1 = template @ noise1 / 4
    dprime = 10 ** (p["matched_snr_db"] / 20)
    threshold = p["threshold_sigma"]
    score0, score1 = projection0, dprime + projection1
    estimates = 1 + projection1 / dprime
    selected = estimates[score1 >= threshold]
    active = selected if p["broken_mode"] else estimates
    q = lambda x: math.erfc(x / np.sqrt(2)) / 2
    alpha = threshold - dprime
    return [
        np.mean(score0 >= threshold),
        np.mean(score1 >= threshold),
        q(threshold),
        q(alpha),
        np.mean(active) - 1,
        np.var(active, ddof=1),
        1 / dprime**2,
        np.mean(selected) - 1,
        np.exp(-(alpha**2) / 2) / (np.sqrt(2 * np.pi) * q(alpha) * dprime),
        np.mean(estimates) - 1,
        len(active),
        float(not p["broken_mode"]),
    ]


_REFERENCES.update(
    {
        "P21": _p21,
        "P22": _p22,
        "P23": _p23,
        "P24": _p24,
        "P25": _p25,
        "P26": _p26,
        "P27": _p27,
        "P28": _p28,
    }
)

# Scenario declarations for the P21-P28 continuation.
SCENARIOS.update({'P21': {'baseline': {'modulation_depth': 0.6, 'message_frequency_hz': 200, 'broken_mode': False}, 'sweep_1': {'modulation_depth': 1.4, 'message_frequency_hz': 200, 'broken_mode': False}, 'sweep_2': {'modulation_depth': 0.6, 'message_frequency_hz': 700, 'broken_mode': False}, 'broken': {'modulation_depth': 0.6, 'message_frequency_hz': 200, 'broken_mode': True}, 'recovery': {'modulation_depth': 0.6, 'message_frequency_hz': 200, 'broken_mode': False}}, 'P22': {'baseline': {'deviation_hz': 400, 'message_frequency_hz': 100, 'broken_mode': False}, 'sweep_1': {'deviation_hz': 800, 'message_frequency_hz': 100, 'broken_mode': False}, 'sweep_2': {'deviation_hz': 400, 'message_frequency_hz': 400, 'broken_mode': False}, 'broken': {'deviation_hz': 400, 'message_frequency_hz': 100, 'broken_mode': True}, 'recovery': {'deviation_hz': 400, 'message_frequency_hz': 100, 'broken_mode': False}}, 'P23': {'baseline': {'ebn0_db': 6, 'phase_error_deg': 12, 'broken_mode': False}, 'sweep_1': {'ebn0_db': 0, 'phase_error_deg': 12, 'broken_mode': False}, 'sweep_2': {'ebn0_db': 6, 'phase_error_deg': 50, 'broken_mode': False}, 'broken': {'ebn0_db': 6, 'phase_error_deg': 12, 'broken_mode': True}, 'recovery': {'ebn0_db': 6, 'phase_error_deg': 12, 'broken_mode': False}}, 'P24': {'baseline': {'rolloff': 0.25, 'span_symbols': 8, 'broken_mode': False}, 'sweep_1': {'rolloff': 0.1, 'span_symbols': 8, 'broken_mode': False}, 'sweep_2': {'rolloff': 0.25, 'span_symbols': 2, 'broken_mode': False}, 'broken': {'rolloff': 0.25, 'span_symbols': 8, 'broken_mode': True}, 'recovery': {'rolloff': 0.25, 'span_symbols': 8, 'broken_mode': False}}, 'P25': {'baseline': {'echo_gain': 0.45, 'regularization': 0.015848931924611134, 'broken_mode': False}, 'sweep_1': {'echo_gain': 0.75, 'regularization': 0.015848931924611134, 'broken_mode': False}, 'sweep_2': {'echo_gain': 0.45, 'regularization': 0.1, 'broken_mode': False}, 'broken': {'echo_gain': 0.45, 'regularization': 0.015848931924611134, 'broken_mode': True}, 'recovery': {'echo_gain': 0.45, 'regularization': 0.015848931924611134, 'broken_mode': False}}, 'P26': {'baseline': {'step_size': 0.006, 'reference_correlation': 1.0, 'broken_mode': False}, 'sweep_1': {'step_size': 0.0005, 'reference_correlation': 1.0, 'broken_mode': False}, 'sweep_2': {'step_size': 0.006, 'reference_correlation': 0, 'broken_mode': False}, 'broken': {'step_size': 0.006, 'reference_correlation': 1.0, 'broken_mode': True}, 'recovery': {'step_size': 0.006, 'reference_correlation': 1.0, 'broken_mode': False}}, 'P27': {'baseline': {'trial_count': 4000, 'ebn0_db': 2, 'broken_mode': False}, 'sweep_1': {'trial_count': 100, 'ebn0_db': 2, 'broken_mode': False}, 'sweep_2': {'trial_count': 4000, 'ebn0_db': -2, 'broken_mode': False}, 'broken': {'trial_count': 4000, 'ebn0_db': 2, 'broken_mode': True}, 'recovery': {'trial_count': 4000, 'ebn0_db': 2, 'broken_mode': False}}, 'P28': {'baseline': {'matched_snr_db': 6, 'threshold_sigma': 1.5, 'broken_mode': False}, 'sweep_1': {'matched_snr_db': 0, 'threshold_sigma': 1.5, 'broken_mode': False}, 'sweep_2': {'matched_snr_db': 6, 'threshold_sigma': 3, 'broken_mode': False}, 'broken': {'matched_snr_db': 6, 'threshold_sigma': 1.5, 'broken_mode': True}, 'recovery': {'matched_snr_db': 6, 'threshold_sigma': 1.5, 'broken_mode': False}}})

# P29-P40 independent references. Earlier bytes are retained verbatim.
# Alternate propagation/correlation formulations and analytic sufficient statistics.
def _oracle_echo(pulse, length, delay):
    """Distribute each source sample into its two neighboring destination bins."""
    destination = np.arange(len(pulse)) + delay
    lower = np.floor(destination).astype(int)
    fraction = destination - lower
    result = np.zeros(length, dtype=np.asarray(pulse).dtype)
    for offset, weights in [(0, 1 - fraction), (1, fraction)]:
        indexes = lower + offset
        valid = (indexes >= 0) & (indexes < length)
        np.add.at(result, indexes[valid], np.asarray(pulse)[valid] * weights[valid])
    return result


def _oracle_width(values, spacing):
    a = abs(values)
    peak = int(np.argmax(a))
    threshold = a[peak] / np.sqrt(2)
    left = np.flatnonzero(a[:peak] < threshold)[-1]
    right = peak + 1 + np.flatnonzero(a[peak + 1 :] < threshold)[0]
    l = left + np.interp(threshold, a[left : left + 2], [0.0, 1.0])
    r = right - np.interp(threshold, a[right - 1 : right + 1][::-1], [0.0, 1.0])
    return (r - l) * spacing


def _oracle_refine(values, index=None):
    a = abs(values)
    i = int(np.argmax(a)) if index is None else int(index)
    # Solve the three-point quadratic explicitly as a small least-squares fit.
    coefficients = np.polynomial.polynomial.polyfit(
        [-1.0, 0.0, 1.0], a[i - 1 : i + 2], 2
    )
    offset = (
        -coefficients[1] / (2 * coefficients[2]) if 2 * coefficients[2] < -1e-10 else 0
    )
    return i + np.clip(offset, -0.5, 0.5)


def _oracle_peaks(a, threshold=0.35):
    # Source rule chooses the first sample of a flat top, if present.
    a = abs(a)
    return sum(
        a[i] > a[i - 1] and a[i] >= a[i + 1] and a[i] >= max(a) * threshold
        for i in range(1, len(a) - 1)
    )


def _p29(p):
    c = 299792458.0
    rcs = p["rcs_m2"]
    power = p["transmit_power_kw"]
    broken = p["broken_mode"]
    # Log-domain link budget independently verifies the multiplicative production equation.
    received = (
        10 * np.log10(power * 1000)
        + 70
        + 20 * np.log10(c / 1e10)
        + 10 * np.log10(rcs)
        - 30 * np.log10(4 * np.pi)
        - 40 * np.log10(40000)
        - 6
        + 30
    )
    noise_db = 10 * np.log10(1.380649e-23) + 10 * np.log10(290) + 60 + 4 + 30
    margin = received - noise_db - 13
    rng = np.random.default_rng(2901)
    iq = rng.normal(size=(2, 4096))
    measured = noise_db + 10 * np.log10(np.mean(iq[0] ** 2 + iq[1] ** 2) / 2)
    return [
        received,
        noise_db,
        measured,
        margin,
        40 * 10 ** (margin / 40),
        -20 if broken else -40,
        10 * np.log10(16),
        16,
        received - (20 if broken else 40) * np.log10(2.5),
        float(not broken),
    ]


def _p30(p):
    from scipy.signal import correlate

    c = 299792458.0
    fs = p["sample_rate_mhz"] * 1e6
    delay = p["delay_us"] * 1e-6
    pulse = np.ones(round(fs * 1e-6))
    count = round(fs * 16e-6)
    echo = _oracle_echo(pulse, count, delay * fs)
    received = echo + 0.03 * np.random.default_rng(3001).normal(size=count)
    response = correlate(received, pulse, mode="valid", method="fft")
    integer = int(np.argmax(abs(response)))
    refined = _oracle_refine(response) * c / (2 * fs)
    counts = []
    for separation in [0.5, 1.5]:
        second = 0.65 * _oracle_echo(pulse, count, (delay + separation * 1e-6) * fs)
        counts.append(
            _oracle_peaks(
                correlate(echo + second, pulse, mode="valid", method="direct"), 0.25
            )
        )
    return [
        c * delay / 2,
        c * integer / (2 * fs),
        refined,
        refined * (2 if p["broken_mode"] else 1),
        c / (2 * fs),
        refined - c * delay / 2,
        max(response),
        *counts,
        float(not p["broken_mode"]),
    ]


def _oracle_gaussian(bandwidth, separation):
    from scipy.signal import fftconvolve

    c = 299792458.0
    fs = 80e6
    sigma = np.sqrt(np.log(2)) / (np.pi * bandwidth)
    half = int(np.ceil(4 * sigma * fs))
    t = np.arange(-half, half + 1) / fs
    pulse = np.exp(-((t / sigma) ** 2) / 2)
    pulse /= np.sqrt(np.dot(pulse, pulse))
    first = _oracle_echo(pulse, 960, 2 * 900.37 / c * fs)
    second = _oracle_echo(pulse, 960, 2 * (900.37 + separation) / c * fs)
    clean = fftconvolve(first, pulse[::-1], mode="valid")
    rng = np.random.default_rng(3101)
    noise = rng.normal(size=960)
    scale = max(clean) / np.sqrt(1e5)
    pair = fftconvolve(first + second + scale * noise, pulse[::-1], mode="valid")
    single = fftconvolve(first + scale * noise, pulse[::-1], mode="valid")
    return pulse, first, clean, pair, single, rng


def _p31(p):
    from scipy.signal import fftconvolve

    c = 299792458.0
    spacing = c / 160e6
    b = p["bandwidth_mhz"] * 1e6
    sep = p["target_separation_m"]
    pulse, first, clean, pair, single, rng = _oracle_gaussian(b, sep)
    axis = np.arange(len(clean)) * spacing
    gate = np.flatnonzero(abs(axis - 900.37) <= 80)
    i = gate[np.argmax(abs(single[gate]))]
    refined = _oracle_refine(single, i) * spacing
    mask = abs(clean) >= max(abs(clean)) / np.sqrt(2)
    locations = np.flatnonzero(mask)
    fine = np.linspace(axis[0], axis[-1], (len(axis) - 1) * 16 + 1)
    display = np.interp(fine, axis, abs(pair))
    g = np.flatnonzero((fine >= 820.37) & (fine <= 980.37 + sep))
    largest = g[np.argsort(display[g], kind="stable")[-2:]]
    noise = rng.normal(size=(128, 960))
    rmses = []
    for snr in [0, 30]:
        errors = []
        for row in noise:
            output = fftconvolve(
                first + max(clean) / 10 ** (snr / 20) * row, pulse[::-1], mode="valid"
            )
            index = gate[np.argmax(abs(output[gate]))]
            errors.append(_oracle_refine(output, index) * spacing - 900.37)
        rmses.append(np.linalg.norm(errors) / np.sqrt(128))
    count = _oracle_peaks(pair)
    wide = _oracle_peaks(_oracle_gaussian(8e6, sep)[3])
    return [
        c / (2 * b),
        (locations[-1] - locations[0]) * spacing,
        count,
        2 if p["broken_mode"] else count,
        abs(fine[largest[1]] - fine[largest[0]]),
        axis[i] - 900.37,
        refined - 900.37,
        *rmses,
        wide,
        float(not p["broken_mode"]),
    ]


def _oracle_chirp(b, t):
    # Phase as a polynomial in integer sample coordinate, rather than squared time.
    count = round(t * 40e6)
    coordinate = np.arange(count) - (count - 1) / 2
    phase = np.pi * b / (t * 40e6**2) * coordinate**2
    return np.cos(phase) + 1j * np.sin(phase)


def _p32(p):
    from scipy.signal import fftconvolve

    c = 299792458.0
    b = p["bandwidth_mhz"] * 1e6
    t = p["pulse_duration_us"] * 1e-6
    wave = _oracle_chirp(b, t)
    n = len(wave)
    first = np.pad(wave, (round(4800 / c * 40e6), 1600 - n - round(4800 / c * 40e6)))
    matched = fftconvolve(first, np.conj(wave[::-1]))
    replica = _oracle_chirp(0.55 * b, t) if p["broken_mode"] else wave
    active = fftconvolve(first, np.conj(replica[::-1]))
    rng = np.random.default_rng(3201)
    noise = np.sqrt(2) * (rng.normal(size=1600) + 1j * rng.normal(size=1600))
    filtered = fftconvolve(noise, np.conj(wave[::-1]))[n - 1 : 1600]
    measured = 10 * np.log10(
        max(abs(matched)) ** 2 / np.mean(abs(filtered) ** 2)
    ) + 10 * np.log10(4 * b / 40e6)
    return [
        b * t,
        c * t / 2,
        c / (2 * b),
        _oracle_width(matched, c / 80e6),
        _oracle_width(active, c / 80e6),
        20 * np.log10(max(abs(active)) / max(abs(matched))),
        10 * np.log10(b * t),
        measured,
        10 * np.log10(n),
        float(not p["broken_mode"]),
    ]


def _oracle_pslr(a):
    from scipy.signal import find_peaks

    a = abs(a)
    i = int(np.argmax(a))
    minima = find_peaks(-a)[0]
    l = minima[minima < i][-1]
    r = minima[minima > i][0]
    return 20 * np.log10(max(max(a[:l]), max(a[r + 1 :])) / a[i])


def _p33(p):
    from scipy.signal import fftconvolve

    c = 299792458.0
    n = 400
    wave = _oracle_chirp(8e6, 10e-6)
    delay = round(4800 / c * 40e6)
    alpha = 1 if p["broken_mode"] else p["taper_strength"]
    sep = 7 if p["broken_mode"] else int(p["separation_samples"])
    weights = 1 - alpha + alpha * np.sin(np.pi * np.arange(n) / (n - 1)) ** 2
    strong = np.pad(wave, (delay, 1600 - delay - n))
    weak = 0.04 * np.pad(wave, (delay + sep, 1600 - delay - sep - n))
    rect = fftconvolve(strong, np.conj(wave[::-1]))
    response = fftconvolve(strong, np.conj((wave * weights)[::-1]))
    clean = fftconvolve(strong + weak, np.conj((wave * weights)[::-1]))
    i = delay + sep + n - 1
    rng = np.random.default_rng(3301)
    noise = 0.12 / np.sqrt(2) * (rng.normal(size=1600) + 1j * rng.normal(size=1600))
    noisy = fftconvolve(strong + weak + noise, np.conj((wave * weights)[::-1]))
    return [
        _oracle_width(rect, c / 80e6),
        _oracle_width(response, c / 80e6),
        _oracle_pslr(rect),
        _oracle_pslr(response),
        10 * np.log10(np.mean(weights) ** 2 / np.mean(weights**2)),
        20 * np.log10(0.04 * sum(weights) / abs(response[i])),
        float(abs(clean[i]) > max(abs(clean[i - 1]), abs(clean[i + 1]))),
        sep * c / 80e6,
        abs(noisy[i]) / sum(weights),
        float(not p["broken_mode"]),
    ]


def _oracle_ambiguity(signal, fd):
    from scipy.signal import correlate

    # Modulate first, then correlate: a different summation order from overlap matrices.
    n = len(signal)
    energy = float(np.vdot(signal, signal).real)
    return np.array(
        [
            abs(
                correlate(
                    signal * np.exp(-2j * np.pi * f * np.arange(n) / 1e7),
                    signal,
                    mode="full",
                    method="direct",
                )
            )
            / energy
            for f in fd
        ]
    )


def _p34(p):
    b = p["bandwidth_mhz"] * 1e6
    t = p["duration_us"] * 1e-6
    n = round(t * 1e7)
    time = (np.arange(n) - (n - 1) / 2) / 1e7
    phase = np.pi * b / t * time * time
    lfm = np.cos(phase) + 1j * np.sin(phase)
    polarities = np.where(np.random.default_rng(3401).random(31) >= 0.5, 1.0, -1.0)
    code = np.kron(polarities[:13], np.ones(10))
    fd = np.linspace(-200e3, 200e3, 101)
    rect = _oracle_ambiguity(np.ones(n), fd)
    chirp = _oracle_ambiguity(lfm, fd)
    coded = _oracle_ambiguity(code, [0])[0]
    delay = np.arange(1 - n, n) / 10
    ridge = delay[np.argmax(chirp[80])]
    pslr = 20 * np.log10(max(coded[abs(np.arange(-129, 130)) >= 10]))
    return [
        _oracle_width(rect[50], 0.1),
        _oracle_width(chirp[50], 0.1),
        _oracle_width(coded, 0.1),
        _oracle_width(rect[:, n - 1], 4),
        ridge,
        120000 / (b / t) * 1e6,
        1 if p["broken_mode"] else 1 / n,
        1 / n,
        pslr,
        float(not p["broken_mode"]),
    ]


def _p35(p):
    c = 299792458.0
    prf = p["prf_khz"] * 1000
    true = p["true_range_km"] * 1000
    pri = 1 / prf
    delay = 2 * true / c
    order = int(delay // pri)
    remainder = delay - order * pri
    ru = c * pri / 2
    samples = round(20e6 / prf)
    count = 6 * samples
    rng = np.random.default_rng(3501)
    iq = rng.normal(size=(2, count))
    return [
        ru / 1000,
        order,
        remainder * c / 2000,
        true / 1000 if p["broken_mode"] else remainder * c / 2000,
        (round(delay * 20e6) - order * samples) * c / 40e9,
        delay * 1e6,
        (ru - 25) / 1000,
        0.025,
        0.004**2 * np.mean(iq[0] ** 2 + iq[1] ** 2) / 2,
        float(not p["broken_mode"]),
    ]


def _p36(p):
    c = 299792458.0
    wavelength = c / (p["carrier_ghz"] * 1e9)
    fd = 2 * p["velocity_mps"] / wavelength
    n = 32
    prf = 4000
    phase = np.deg2rad(25) + 2 * np.pi * fd * np.arange(n) / prf
    rng = np.random.default_rng(3601)
    real = np.cos(phase) + 0.1 / np.sqrt(2) * rng.normal(size=n)
    imag = np.sin(phase) + 0.1 / np.sqrt(2) * rng.normal(size=n)
    if p["broken_mode"]:
        real, imag = np.hypot(real, imag), np.zeros(n)
    angle = np.arctan2(
        np.dot(real[:-1], imag[1:]) - np.dot(imag[:-1], real[1:]),
        np.dot(real[:-1], real[1:]) + np.dot(imag[:-1], imag[1:]),
    )
    estimate = angle * prf / (2 * np.pi)
    slope = np.polynomial.polynomial.polyfit(
        np.arange(n) / prf, np.unwrap(np.arctan2(imag, real)), 1
    )[1] / (2 * np.pi)
    # Direct DFT matrix independently checks the production FFT peak convention.
    frequencies = np.arange(-n // 2, n // 2) * prf / n
    spectrum = np.exp(
        -2j * np.pi * frequencies[:, None] * np.arange(n)[None, :] / prf
    ) @ ((real + 1j * imag) * np.hanning(n))
    peak = frequencies[np.argmax(abs(spectrum))]
    return [
        fd,
        2 * np.pi * fd / prf,
        estimate,
        slope,
        peak,
        estimate * wavelength / 2,
        wavelength * prf / 4,
        prf / n,
        float(not p["broken_mode"]),
    ]


def _p37(p):
    c = 299792458.0
    wavelength = c / 1e10
    prf = 5000
    spacing = c / 40e6
    rows = 256
    columns = 32
    ranges = np.array([450, p["middle_target_range_m"], 1200])
    bins = np.rint(ranges / spacing).astype(int)
    velocities = np.array([0, p["middle_velocity_mps"], -18])
    amplitudes = np.array([1, 0.75, 0.55])
    phases = np.deg2rad([0, 40, -30])
    # Only the selected row is needed; compute its three physical contributions directly.
    gains = np.exp(-0.5 * ((bins[1] - bins) / 1.2) ** 2) * amplitudes
    angles = (
        phases[:, None]
        + 2 * np.pi * (2 * velocities / wavelength)[:, None] * np.arange(columns) / prf
    )
    signal = gains @ np.exp(1j * angles)
    rng = np.random.default_rng(3701)
    noise = rng.normal(size=(rows, columns)) + 1j * rng.normal(size=(rows, columns))
    trace = signal + 0.02 / np.sqrt(2) * noise[bins[1]]
    if p["broken_mode"]:
        trace = abs(trace)
    adjacent = np.vdot(trace[:-1], trace[1:])
    estimate = np.arctan2(adjacent.imag, adjacent.real) * prf / (2 * np.pi)
    freq = np.arange(-16, 16) * prf / columns
    dft = np.exp(-2j * np.pi * freq[:, None] * np.arange(columns) / prf) @ (
        trace * np.hanning(columns)
    )
    return [
        bins[1],
        bins[1] * spacing,
        bins[1] * spacing - ranges[1],
        2 * velocities[1] / wavelength,
        estimate,
        freq[np.argmax(abs(dft))],
        (rows - 1) * spacing,
        c / (2 * prf),
        max(abs(velocities)) * 31 / prf / spacing,
        float(not p["broken_mode"]),
    ]


def _p38(p):
    from scipy.signal import lfilter

    c = 299792458.0
    wavelength = c / 1e10
    prf = p["prf_khz"] * 1000
    phase = 2 * np.pi * 2 * p["slow_target_velocity_mps"] / wavelength / prf
    gain = 2 * abs(np.sin(phase / 2))
    rng = np.random.default_rng(3801)
    noise = rng.normal(size=(128, 64)) + 1j * rng.normal(size=(128, 64))
    two = lfilter([1, -1], [1], noise, axis=1)[:, 1:]
    three = lfilter([1, -2, 1], [1], noise, axis=1)[:, 2:]
    variance = np.mean(abs(noise) ** 2)
    profile = sum(
        a
        * np.exp(1j * np.deg2rad(phase_deg))
        * np.exp(-0.5 * ((np.arange(128) - b) / 1.8) ** 2)
        for a, b, phase_deg in zip([20, 12, 8], [24, 62, 99], [0, 50, -35])
    )
    residual = (
        np.sqrt(np.mean(abs(np.diff(profile)) ** 2) / np.mean(abs(profile) ** 2))
        if p["broken_mode"]
        else 0
    )
    return [
        residual,
        gain,
        gain**2,
        np.mean(abs(two) ** 2) / variance,
        np.mean(abs(three) ** 2) / variance,
        2,
        6,
        wavelength * prf / 2,
        127 if p["broken_mode"] else 128,
        64 if p["broken_mode"] else 63,
        float(not p["broken_mode"]),
    ]


def _p39(p):
    from scipy.signal import lfilter

    c = 299792458.0
    wavelength = c / 1e10
    fd = p["primary_blind_speed_multiple"] * 4000
    velocity = fd * wavelength / 2
    secondary = 4000 if p["broken_mode"] else p["secondary_prf_khz"] * 1000
    first = abs(np.sin(np.pi * fd / 4000))
    second = abs(np.sin(np.pi * fd / secondary))
    recovered = max(first, abs(np.sin(np.pi * fd / 5300)))
    rng = np.random.default_rng(3901)
    rng.normal(size=32)
    rng.normal(size=32)
    noise = 0.02 / np.sqrt(2) * (rng.normal(size=32) + 1j * rng.normal(size=32))
    sequence = (
        np.exp(1j * (np.deg2rad(20) + 2 * np.pi * fd * np.arange(32) / secondary))
        + noise
    )
    observed = lfilter([1, -1], [1], sequence)[1:]
    return [
        velocity,
        fd,
        first,
        second,
        max(first, second),
        recovered,
        float(max(first, second) >= 0.3),
        secondary,
        0,
        np.sqrt(np.mean(abs(observed) ** 2)) / 2,
        float(not p["broken_mode"]),
    ]


def _p40(p):
    n = int(p["pulse_count"])
    rho = 10 ** (p["input_snr_db"] / 10)
    angle = np.deg2rad(25 + 35 * np.arange(n))
    rng = np.random.default_rng(4001)
    x = np.cos(angle) + rng.normal(size=n) / np.sqrt(2 * rho)
    y = np.sin(angle) + rng.normal(size=n) / np.sqrt(2 * rho)
    rotated_real = x * np.cos(angle) + y * np.sin(angle)
    rotated_imag = y * np.cos(angle) - x * np.sin(angle)
    coherent = rotated_real.sum() ** 2 + rotated_imag.sum() ** 2
    power = np.dot(x, x) + np.dot(y, y)
    # A complete four-point roots-of-unity cycle has zero sum and unit energy.
    return [
        10 * np.log10(n * rho),
        n * rho,
        np.sqrt(n) * rho,
        0 if p["broken_mode"] else 1,
        1,
        1,
        coherent,
        power,
        1 + (n - 1) * np.exp(-((np.pi / 2) ** 2)),
        float(not p["broken_mode"]),
    ]


_REFERENCES.update({f"P{n}": globals()[f"_p{n}"] for n in range(29, 41)})

# Scenario declarations for P29-P40.
SCENARIOS.update({'P29': {'baseline': {'rcs_m2': 1, 'transmit_power_kw': 100, 'broken_mode': False}, 'sweep_1': {'rcs_m2': 0.1, 'transmit_power_kw': 100, 'broken_mode': False}, 'sweep_2': {'rcs_m2': 1, 'transmit_power_kw': 400, 'broken_mode': False}, 'broken': {'rcs_m2': 1, 'transmit_power_kw': 100, 'broken_mode': True}, 'recovery': {'rcs_m2': 1, 'transmit_power_kw': 100, 'broken_mode': False}}, 'P30': {'baseline': {'sample_rate_mhz': 20, 'delay_us': 6.0175, 'broken_mode': False}, 'sweep_1': {'sample_rate_mhz': 40, 'delay_us': 6.0175, 'broken_mode': False}, 'sweep_2': {'sample_rate_mhz': 20, 'delay_us': 6.0375, 'broken_mode': False}, 'broken': {'sample_rate_mhz': 20, 'delay_us': 6.0175, 'broken_mode': True}, 'recovery': {'sample_rate_mhz': 20, 'delay_us': 6.0175, 'broken_mode': False}}, 'P31': {'baseline': {'bandwidth_mhz': 4, 'target_separation_m': 22, 'broken_mode': False}, 'sweep_1': {'bandwidth_mhz': 8, 'target_separation_m': 22, 'broken_mode': False}, 'sweep_2': {'bandwidth_mhz': 4, 'target_separation_m': 45, 'broken_mode': False}, 'broken': {'bandwidth_mhz': 4, 'target_separation_m': 22, 'broken_mode': True}, 'recovery': {'bandwidth_mhz': 4, 'target_separation_m': 22, 'broken_mode': False}}, 'P32': {'baseline': {'bandwidth_mhz': 8, 'pulse_duration_us': 10, 'broken_mode': False}, 'sweep_1': {'bandwidth_mhz': 16, 'pulse_duration_us': 10, 'broken_mode': False}, 'sweep_2': {'bandwidth_mhz': 8, 'pulse_duration_us': 20, 'broken_mode': False}, 'broken': {'bandwidth_mhz': 8, 'pulse_duration_us': 10, 'broken_mode': True}, 'recovery': {'bandwidth_mhz': 8, 'pulse_duration_us': 10, 'broken_mode': False}}, 'P33': {'baseline': {'taper_strength': 1, 'separation_samples': 17, 'broken_mode': False}, 'sweep_1': {'taper_strength': 0, 'separation_samples': 17, 'broken_mode': False}, 'sweep_2': {'taper_strength': 1, 'separation_samples': 7, 'broken_mode': False}, 'broken': {'taper_strength': 1, 'separation_samples': 17, 'broken_mode': True}, 'recovery': {'taper_strength': 1, 'separation_samples': 17, 'broken_mode': False}}, 'P34': {'baseline': {'bandwidth_mhz': 3, 'duration_us': 13, 'broken_mode': False}, 'sweep_1': {'bandwidth_mhz': 1.5, 'duration_us': 13, 'broken_mode': False}, 'sweep_2': {'bandwidth_mhz': 3, 'duration_us': 6.5, 'broken_mode': False}, 'broken': {'bandwidth_mhz': 3, 'duration_us': 13, 'broken_mode': True}, 'recovery': {'bandwidth_mhz': 3, 'duration_us': 13, 'broken_mode': False}}, 'P35': {'baseline': {'prf_khz': 20, 'true_range_km': 18, 'broken_mode': False}, 'sweep_1': {'prf_khz': 10, 'true_range_km': 18, 'broken_mode': False}, 'sweep_2': {'prf_khz': 20, 'true_range_km': 8, 'broken_mode': False}, 'broken': {'prf_khz': 20, 'true_range_km': 18, 'broken_mode': True}, 'recovery': {'prf_khz': 20, 'true_range_km': 18, 'broken_mode': False}}, 'P36': {'baseline': {'velocity_mps': 15, 'carrier_ghz': 10, 'broken_mode': False}, 'sweep_1': {'velocity_mps': -10, 'carrier_ghz': 10, 'broken_mode': False}, 'sweep_2': {'velocity_mps': 15, 'carrier_ghz': 15, 'broken_mode': False}, 'broken': {'velocity_mps': 15, 'carrier_ghz': 10, 'broken_mode': True}, 'recovery': {'velocity_mps': 15, 'carrier_ghz': 10, 'broken_mode': False}}, 'P37': {'baseline': {'middle_target_range_m': 900, 'middle_velocity_mps': 12, 'broken_mode': False}, 'sweep_1': {'middle_target_range_m': 750, 'middle_velocity_mps': 12, 'broken_mode': False}, 'sweep_2': {'middle_target_range_m': 900, 'middle_velocity_mps': -18, 'broken_mode': False}, 'broken': {'middle_target_range_m': 900, 'middle_velocity_mps': 12, 'broken_mode': True}, 'recovery': {'middle_target_range_m': 900, 'middle_velocity_mps': 12, 'broken_mode': False}}, 'P38': {'baseline': {'slow_target_velocity_mps': 3, 'prf_khz': 5, 'broken_mode': False}, 'sweep_1': {'slow_target_velocity_mps': 15, 'prf_khz': 5, 'broken_mode': False}, 'sweep_2': {'slow_target_velocity_mps': 3, 'prf_khz': 9, 'broken_mode': False}, 'broken': {'slow_target_velocity_mps': 3, 'prf_khz': 5, 'broken_mode': True}, 'recovery': {'slow_target_velocity_mps': 3, 'prf_khz': 5, 'broken_mode': False}}, 'P39': {'baseline': {'secondary_prf_khz': 5.3, 'primary_blind_speed_multiple': 1, 'broken_mode': False}, 'sweep_1': {'secondary_prf_khz': 4.5, 'primary_blind_speed_multiple': 1, 'broken_mode': False}, 'sweep_2': {'secondary_prf_khz': 5.3, 'primary_blind_speed_multiple': 0.5, 'broken_mode': False}, 'broken': {'secondary_prf_khz': 5.3, 'primary_blind_speed_multiple': 1, 'broken_mode': True}, 'recovery': {'secondary_prf_khz': 5.3, 'primary_blind_speed_multiple': 1, 'broken_mode': False}}, 'P40': {'baseline': {'pulse_count': 32, 'input_snr_db': -8, 'broken_mode': False}, 'sweep_1': {'pulse_count': 64, 'input_snr_db': -8, 'broken_mode': False}, 'sweep_2': {'pulse_count': 32, 'input_snr_db': 0, 'broken_mode': False}, 'broken': {'pulse_count': 32, 'input_snr_db': -8, 'broken_mode': True}, 'recovery': {'pulse_count': 32, 'input_snr_db': -8, 'broken_mode': False}}})
# P41-P52 independent references. Prior bytes above remain immutable.
# Inputs use the same documented NumPy draws, never production computations.
# Alternate filters, real-coordinate algebra, direct stencil summation,
# quadrature calibration, and independent score/interval equations are used.


def _r41_normal(rng, shape):
    return rng.normal(size=shape), rng.normal(size=shape)


def _r41_filter(white, rho, axis):
    from scipy.signal import lfilter

    x = np.array(white, copy=True) * np.sqrt(1 - rho * rho)
    first = [slice(None)] * x.ndim
    first[axis] = 0
    x[tuple(first)] = white[tuple(first)]
    return lfilter([1], [1, -rho], x, axis=axis)


def _p41(p):
    rho = p["range_correlation"]
    snr = p["target_snr_db"]
    rng = np.random.default_rng(4101)
    a, b = _r41_normal(rng, (64, 96))
    field = _r41_filter(_r41_filter((a + 1j * b) / np.sqrt(2), rho, 1), 0.92, 0)
    _r41_normal(rng, (64, 96))

    def correlation(x, y):
        cross = np.sum(x.real * y.real + x.imag * y.imag)
        return cross / np.sqrt(
            np.sum(x.real * x.real + x.imag * x.imag)
            * np.sum(y.real * y.real + y.imag * y.imag)
        )

    rc = correlation(field[:, :-1], field[:, 1:])
    tc = correlation(field[:-1], field[1:])
    power = 10 ** (snr / 10)
    slow = -power * np.log(rng.random((2000, 1)))
    fast = -power * np.log(rng.random((2000, 32)))
    slow2 = -power / 2 * (np.log(rng.random((2000, 1))) + np.log(rng.random((2000, 1))))
    fast2 = (
        -power / 2 * (np.log(rng.random((2000, 32))) + np.log(rng.random((2000, 32))))
    )
    cv = []
    for x in [slow, fast[:, :16], slow2, fast2[:, :16]]:
        means = np.sum(x, axis=1) / x.shape[1]
        avg = np.sum(means) / 2000
        cv.append(np.sqrt(np.sum((means - avg) ** 2) / 1999) / avg)
    nr, ni = _r41_normal(rng, (2000, 32))
    hr, hi = _r41_normal(rng, (2000, 32))
    h0 = (hr * hr + hi * hi) / 2
    threshold = np.partition(np.sum(h0[:, :16], axis=1) / 16, 1899)[1899]
    probabilities = []
    for target_power in [np.full((2000, 16), power), fast[:, :16]]:
        re = np.sqrt(target_power) * np.cos(np.deg2rad(35)) + nr[:, :16] / np.sqrt(2)
        im = np.sqrt(target_power) * np.sin(np.deg2rad(35)) + ni[:, :16] / np.sqrt(2)
        probabilities.append(
            np.count_nonzero(np.sum(re * re + im * im, axis=1) / 16 > threshold) / 2000
        )
    a, b = _r41_normal(rng, (1024, 96))
    w = _r41_filter((a + 1j * b) / np.sqrt(2), rho, 1)
    a, b = _r41_normal(rng, (1024, 96))
    ranges = 0.25 + 0.05 * np.arange(96)
    profile = 0.1 + 25 * (0.25 / ranges) ** 2
    re = w.real * np.sqrt(profile) + a / np.sqrt(2)
    im = w.imag * np.sqrt(profile) + b / np.sqrt(2)
    bp = re * re + im * im
    good = np.sum(bp > -(profile + 1) * np.log(0.05), axis=0) / 1024
    threshold = (
        -np.sum(profile + 1) / 96 * np.log(0.05)
        if p["broken_mode"]
        else -(profile + 1) * np.log(0.05)
    )
    active = np.sum(bp > threshold, axis=0) / 1024
    return [
        profile[0],
        profile[-1],
        rc,
        tc,
        *cv,
        np.sum(active[:16]) / 16,
        np.sum(active[-16:]) / 16,
        np.sum(good[:16]) / 16,
        *probabilities,
        float(not p["broken_mode"]),
    ]


def _p42(p):
    from scipy.signal import fftconvolve

    c = 299792458.0
    wavelength = c / 1e10
    n = int(p["pulse_count"])
    taper = p["hann_weight"]
    t = (np.arange(48) - 23.5) / 20e6
    angle = np.pi * 8e6 / 2.4e-6 * t * t
    pulse = np.cos(angle) + 1j * np.sin(angle)
    raw = np.zeros((512, 64), complex)
    delays = [160, 160, 320]
    for d, v, amp, phase in zip(
        delays, [-7.5, 10.3, 10.3], [1, 0.8, 0.65], [0, 35, -50]
    ):
        a = np.deg2rad(phase) + 4 * np.pi * v / wavelength * np.arange(64) / 4000
        raw[d : d + 48] += amp * np.outer(pulse, np.cos(a) + 1j * np.sin(a))
    rng = np.random.default_rng(4201)
    ds = np.floor(np.linspace(24, 452, 24) + 0.5).astype(int)
    a, b = _r41_normal(rng, 24)
    coef = 0.055 / np.sqrt(2 * (1 + ds / 80)) * (a + 1j * b)
    for d, value in zip(ds, coef):
        raw[d : d + 48] += value * pulse[:, None]
    a, b = _r41_normal(rng, (512, 64))
    raw += 0.35 / np.sqrt(2) * (a + 1j * b)
    rc = fftconvolve(raw, pulse[::-1, None].conj(), mode="full", axes=0)[47:559, :n]
    window = (1 - taper) + taper * (
        0.5 - 0.5 * np.cos(2 * np.pi * np.arange(n) / (n - 1))
    )
    # Direct DFT on pulse columns, independently of the production FFT.
    bins = np.arange(-n // 2, n // 2)
    basis = np.exp(-2j * np.pi * np.outer(np.arange(n), bins) / n)
    rd = (rc * window) @ basis / np.sum(window)
    va = bins * 4000 / n * wavelength / 2
    ra = np.arange(512) * c / 40e6
    measured = []
    peaks = []
    for d, v in zip(delays, [-7.5, 10.3, 10.3]):
        j = int(np.argmin(abs(va - v)))
        rr = np.arange(d - 4, d + 5)
        jj = np.arange(max(0, j - 2), min(n, j + 3))
        mag = abs(rd[np.ix_(rr, jj)])
        row, col = np.unravel_index(np.argmax(mag), mag.shape)
        measured.append((ra[rr[row]], va[jj[col]]))
        peaks.append(mag[row, col])
    side = []
    k = np.arange(64)
    tone = np.exp(2j * np.pi * 10.1 * k / 64)
    dft = np.exp(-2j * np.pi * np.outer(k, np.arange(-32, 32)) / 64)
    for window in [np.ones(64), 0.5 - 0.5 * np.cos(2 * np.pi * k / 63)]:
        mag = abs((tone * window) @ dft) / sum(window)
        db = 20 * np.log10(np.maximum(mag / max(mag), 10 ** (-55 / 20)))
        side.append(max(db[abs(k - np.argmax(mag)) > 2]))
    active_peak = (
        np.max(abs(np.fft.fft(rc, axis=0)))
        if p["broken_mode"]
        else max(abs(rd).ravel())
    )
    return [
        c / 40e6,
        c / 16e6,
        4000 / n * wavelength / 2,
        measured[0][0],
        measured[0][1],
        measured[1][1],
        measured[2][0],
        peaks[0],
        *side,
        active_peak,
        float(not p["broken_mode"]),
    ]


def _p43(p):
    from scipy.stats import norm

    sigma = p["noise_rms"]
    mu = p["clutter_pedestal"]
    rng = np.random.default_rng(4301)
    h0 = rng.normal(size=20000)
    h1 = rng.normal(size=20000)
    profile = rng.normal(size=256)
    targets = [47, 102, 170, 225]
    profile[targets] += 4
    gamma = norm.isf(0.01)
    active = sigma * gamma if p["broken_mode"] else gamma
    fa = np.count_nonzero(h0 > (active - mu) / sigma) / 20000
    pd = np.count_nonzero(h1 > (active - mu - 4) / sigma) / 20000
    return [
        gamma,
        active,
        fa,
        pd,
        20000 * (1 - pd),
        norm.sf((active - mu) / sigma),
        norm.sf((active - mu - 4) / sigma),
        np.count_nonzero(h0 > (gamma - mu) / sigma) / 20000,
        np.count_nonzero(profile[targets] > gamma),
        np.count_nonzero(h0 > (gamma if p["broken_mode"] else gamma / 2)) / 20000,
        float(not p["broken_mode"]),
    ]


def _p44(p):
    from scipy.stats import norm

    rng = np.random.default_rng(4401)
    template = np.array([1, 1, 1, -1, 1, -1, -1, 1, -1, 1, -1, -1, -1, 1, 1, -1]) / 4
    a = rng.normal(size=(16, 60000))
    h0 = np.einsum("i,ij->j", template, a)
    a = rng.normal(size=(16, 60000))
    h1 = np.einsum("i,ij->j", template, a)
    g = p["threshold_sigma"]
    shift = np.sqrt(10 ** (p["matched_snr_db"] / 10))
    active = np.partition(h0, 249)[249] if p["broken_mode"] else g
    fa = np.count_nonzero(h0 > active) / 60000
    pd = np.count_nonzero(h1 > active - shift) / 60000
    return [
        16,
        active,
        fa,
        pd,
        norm.sf(g),
        norm.sf(g - shift),
        1e6 * fa,
        0,
        1,
        np.count_nonzero(h0 > g) / 60000,
        float(not p["broken_mode"]),
    ]


def _r45_stencil(power, t, g, geometric=False):
    # Direct per-CUT summation independently of production's indexed matrix.
    out = []
    for cut in range(t + g, len(power) - t - g):
        samples = list(power[cut - g - t : cut - g]) + list(
            power[cut + g + 1 : cut + g + t + 1]
        )
        out.append(
            np.exp(sum(np.log(samples)) / (2 * t))
            if geometric
            else sum(samples) / (2 * t)
        )
    return np.asarray(out)


def _r45_alpha(n, p):
    return n * (p ** (-1 / n) - 1)


def _p45(p):
    index = np.arange(1, 257)
    mean = 0.65 + 0.0045 * index + 0.32 * (1 + np.sin(2 * np.pi * (index - 18) / 190))
    rng = np.random.default_rng(4501)
    a, b = _r41_normal(rng, 256)
    re = a * np.sqrt(mean / 2)
    im = b * np.sqrt(mean / 2)
    targets = np.array([61, 131, 210])
    amplitude = np.sqrt(mean[targets] * 10 ** (np.array([19, 17, 20]) / 10))
    ph = np.array([0.2, -0.8, 1.1])
    re[targets] += amplitude * np.cos(ph)
    im[targets] += amplitude * np.sin(ph)
    power = p["scene_power_scale"] * (re * re + im * im)
    avg = _r45_stencil(power, 12, 2)
    geo = _r45_stencil(power, 12, 2, True)
    alpha = _r45_alpha(24, p["design_pfa"])
    active = geo if p["broken_mode"] else avg
    det = power[14:-14] > alpha * active
    mask = np.isin(np.arange(14, 242), targets)
    j = 131 - 14
    return [
        alpha,
        228,
        28,
        np.count_nonzero(det & mask),
        np.count_nonzero(det & ~mask),
        active[j],
        alpha * active[j],
        np.median(geo / avg),
        np.count_nonzero((power[14:-14] > alpha * avg) & mask),
        float(not p["broken_mode"]),
    ]


def _p46(p):
    t = int(p["training_cells"])
    g = int(p["guard_cells"])
    cells = np.arange(1, 257)
    mean = 0.75 + 0.003 * cells + 2.8 / (1 + np.exp((178 - cells) / 5.5))
    rng = np.random.default_rng(4601)
    a, b = _r41_normal(rng, 256)
    re = a * np.sqrt(mean / 2)
    im = b * np.sqrt(mean / 2)
    offs = np.arange(-18, 19)
    response = np.sinc(offs / 5)
    amp = np.sqrt(mean[87] * 10**3.5)
    re[87 + offs] += amp * response * np.cos(0.4)
    im[87 + offs] += amp * response * np.sin(0.4)
    ampw = np.sqrt(mean[137] * 10**1.8)
    re[137] += ampw * np.cos(-0.7)
    im[137] += ampw * np.sin(-0.7)
    power = re * re + im * im
    threshold = _r45_alpha(2 * t, 0.001) * _r45_stencil(power, t, g)
    re[125] += np.sqrt(mean[125] * 10**3.2) * np.cos(1.1)
    im[125] += np.sqrt(mean[125] * 10**3.2) * np.sin(1.1)
    bad = re * re + im * im
    bt = _r45_alpha(24, 0.001) * _r45_stencil(bad, 12, 4)
    rt = _r45_alpha(24, 0.001) * _r45_stencil(bad, 12, 12)
    target = np.zeros(256)
    target[87 + offs] = amp * amp * response * response
    target[137] = ampw * ampw
    leak = [_r45_stencil(target, 12, guard)[87 - 12 - guard] for guard in [0, 10]]
    locality = []
    for train in [4, 36]:
        expected = _r45_stencil(mean, train, 6)
        locality.append(
            np.mean(abs(expected[np.arange(164, 190) - train - 6] / mean[164:190] - 1))
        )
    bm = bad[137] / bt[121]
    rm = bad[137] / rt[113]
    wm = power[137] / threshold[137 - t - g]
    return [
        (2 * (t + g) + 1) * 15,
        2 * (t + g),
        power[87] / threshold[87 - t - g],
        bm if p["broken_mode"] else wm,
        bm,
        rm,
        bad[137] - power[137],
        *leak,
        *locality,
        float(not p["broken_mode"]),
    ]


def _p47(p):
    from scipy.interpolate import interp1d

    n = int(p["training_count"])
    pfa = p["design_pfa"]
    rng = np.random.default_rng(4701)
    a, b = _r41_normal(rng, 50000)
    a /= np.sqrt(2)
    b /= np.sqrt(2)
    angle = 2 * np.pi * rng.random(50000)
    means = np.empty((50000, 4))
    ns = [8, 16, 32, 64]
    for start in range(0, 50000, 2000):
        x, y = _r41_normal(rng, (2000, 64))
        squares = (x * x + y * y) / 2
        for j, num in enumerate(ns):
            means[start : start + 2000, j] = np.sum(squares[:, :num], axis=1) / num
    snrs = np.linspace(3, 17, 29)
    amplitudes = 10 ** (snrs / 20)
    scores = (a[:, None] + np.cos(angle)[:, None] * amplitudes) ** 2 + (
        b[:, None] + np.sin(angle)[:, None] * amplitudes
    ) ** 2
    known = -np.log(pfa)
    estimate = means[:, ns.index(n)]
    proper = _r45_alpha(n, pfa)
    active = known if p["broken_mode"] else proper

    def inverse(threshold):
        raw = (
            np.count_nonzero(scores > np.asarray(threshold)[:, None], axis=0) / 50000
            if np.ndim(threshold)
            else np.count_nonzero(scores > threshold, axis=0) / 50000
        )
        envelope = np.maximum.accumulate(raw)
        upper = np.flatnonzero(envelope >= 0.8)[0]
        lo = upper - 1
        result = float(interp1d(envelope[lo : upper + 1], snrs[lo : upper + 1])(0.8))
        return result, float(max(envelope - raw))

    ksnr, kadj = inverse(known)
    asnr, aadj = inverse(active * estimate)
    rsnr, _ = inverse(proper * estimate)
    adjustments = [kadj, aadj] + [
        inverse(_r45_alpha(num, pfa) * means[:, j])[1] for j, num in enumerate(ns)
    ]
    h0 = a * a + b * b
    return [
        known,
        active,
        ksnr,
        asnr,
        asnr - ksnr,
        np.count_nonzero(h0 > active * estimate) / 50000,
        (1 + active / n) ** (-n),
        rsnr - ksnr,
        np.sqrt(np.mean((estimate - np.mean(estimate)) ** 2)),
        max(adjustments),
        float(not p["broken_mode"]),
    ]


from functools import lru_cache as _r48_cache


@_r48_cache(maxsize=128)
def _r48_probability(alpha, t, variant):
    from scipy.integrate import quad
    from scipy.special import gammainc, gammaincc, gammaln

    # Integrate the density of max/min of two independent Gamma side means.
    def integrand(x):
        if x <= 0:
            return 0.0
        pdf = np.exp(t * np.log(t) + (t - 1) * np.log(x) - t * x - gammaln(t))
        weight = gammainc(t, t * x) if variant == "GO" else gammaincc(t, t * x)
        return 2 * np.exp(-alpha * x) * pdf * weight

    return quad(integrand, 0, np.inf, epsabs=1e-13, epsrel=1e-11)[0]


@_r48_cache(maxsize=128)
def _r48_scale(t, p, variant):
    from scipy.optimize import brentq

    return brentq(lambda a: _r48_probability(a, t, variant) - p, 0.01, 100, xtol=1e-12)


def _r49_probability(alpha, n, k):
    from scipy.special import gammaln

    # Laplace transform through the beta-function form of the order statistic.
    return np.exp(
        gammaln(n + 1)
        - gammaln(n - k + 1)
        + gammaln(n - k + alpha + 1)
        - gammaln(n + alpha + 1)
    )


@_r48_cache(maxsize=128)
def _r49_scale(n, k, p):
    from scipy.optimize import brentq

    return brentq(lambda a: _r49_probability(a, n, k) - p, 0.001, 100, xtol=1e-12)


def _p48(p):
    rng = np.random.default_rng(4801)
    cells = np.arange(240)
    mean = np.where(cells >= 120, 10 ** (p["clutter_step_db"] / 10), 1)
    bg = -mean * np.log(rng.random(240))
    ago = _r48_scale(12, 0.001, "GO")
    aso = _r48_scale(12, 0.001, "SO")
    ca = _r45_alpha(24, 0.001)
    left = -np.log(rng.random((25000, 12)))
    right = -np.log(rng.random((25000, 12)))
    cut = -np.log(rng.random(25000))
    lm = np.sum(left, axis=1) / 12
    rm = np.sum(right, axis=1) / 12
    a, b = _r41_normal(rng, 25000)
    target = (a / np.sqrt(2) + np.sqrt(10**1.3)) ** 2 + b * b / 2
    q = 10 ** (p["clutter_step_db"] / 10)
    contaminated = lm + 10 ** (p["interferer_power_db"] / 10) / 12
    gp = np.count_nonzero(q * cut > ago * np.maximum(lm, q * rm)) / 25000
    sp = np.count_nonzero(q * cut > aso * np.minimum(lm, q * rm)) / 25000
    el = np.sum(bg[106:118]) / 12
    er = np.sum(bg[123:135]) / 12
    return [
        ago,
        aso,
        sp if p["broken_mode"] else gp,
        gp,
        np.count_nonzero(target > ago * np.maximum(contaminated, rm)) / 25000,
        np.count_nonzero(target > aso * np.minimum(contaminated, rm)) / 25000,
        _r48_probability(ca, 12, "GO"),
        _r48_probability(ca, 12, "SO"),
        ago * max(el, er),
        aso * min(el, er),
        float(not p["broken_mode"]),
    ]


def _p49(p):
    k = int(p["os_rank"])
    db = p["interferer_power_db"]
    rng = np.random.default_rng(4901)
    power = -np.log(rng.random(256))
    power[127] += 10**1.5
    power[[114, 119, 135, 140]] += 10 ** (db / 10)
    refs = np.r_[power[113:125], power[130:142]]
    proper = _r49_scale(24, k, 0.001)
    active = _r49_scale(24, 18, 0.001) if p["broken_mode"] else proper
    rank = 22 if p["broken_mode"] else k
    bank = -np.log(rng.random((20000, 24)))
    a, b = _r41_normal(rng, 20000)
    target = (a / np.sqrt(2) + np.sqrt(10**1.3)) ** 2 + b * b / 2
    bank[:, :4] += 10 ** (db / 10)
    order = np.partition(bank, rank - 1, axis=1)[:, rank - 1]
    return [
        rank,
        active,
        _r49_probability(active, 24, rank),
        24 - rank,
        power[127] / (_r45_alpha(24, 0.001) * sum(refs) / 24),
        power[127] / (active * np.partition(refs, rank - 1)[rank - 1]),
        np.count_nonzero(target > active * order) / 20000,
        proper,
        _r49_probability(proper, 24, k),
        float(not p["broken_mode"]),
    ]


def _p50(p):
    rng = np.random.default_rng(5001)
    r = np.arange(96) * 30
    v = np.arange(-32, 32) * 0.625
    mean = np.outer(0.8 + 1.2 * (r / r[-1]) ** 2, 1 + 2.5 * np.exp(-((v / 2.5) ** 2)))
    a, b = _r41_normal(rng, (96, 64))
    power = mean * (a * a + b * b) / 2
    support = np.zeros((96, 64), bool)
    rows = [27, 52, 75, 3]
    cols = [44, 21, 34, 7]
    rw = [0.015, 0.05, 0.2, 0.55, 1, 0.55, 0.2, 0.05, 0.015]
    dw = [0.01, 0.04, 0.18, 0.5, 1, 0.5, 0.18, 0.04, 0.01]
    for rr, cc, snr in zip(rows, cols, [24, 20, 18, 20]):
        for dr in range(-4, 5):
            for dc in range(-4, 5):
                if 0 <= rr + dr < 96 and 0 <= cc + dc < 64:
                    power[rr + dr, cc + dc] += (
                        mean[rr, cc] * 10 ** (snr / 10) * rw[dr + 4] * dw[dc + 4]
                    )
                    support[rr + dr, cc + dc] = True
    hr = int(p["range_training_half_width"]) + 2
    hd = int(p["doppler_training_half_width"]) + 2
    n = (2 * hr + 1) * (2 * hd + 1) - 25
    alpha = _r45_alpha(n, 0.001)
    # Summed-area rectangle subtraction, not production convolution.
    cumulative = np.pad(power, ((1, 0), (1, 0))).cumsum(0).cumsum(1)

    def rectangle(r0, r1, c0, c1):
        r0, r1 = max(r0, 0), min(r1, 96)
        c0, c1 = max(c0, 0), min(c1, 64)
        return (
            cumulative[r1, c1]
            - cumulative[r0, c1]
            - cumulative[r1, c0]
            + cumulative[r0, c0]
        )

    threshold = np.empty((96, 64))
    eligible = np.zeros((96, 64), bool)
    eligible[hr:-hr, hd:-hd] = True
    for rr in range(96):
        for cc in range(64):
            threshold[rr, cc] = (
                alpha
                * (
                    rectangle(rr - hr, rr + hr + 1, cc - hd, cc + hd + 1)
                    - rectangle(rr - 2, rr + 3, cc - 2, cc + 3)
                )
                / n
            )
    det = (power > threshold) & eligible
    active = power > threshold if p["broken_mode"] else det
    return [
        n,
        alpha,
        np.count_nonzero(eligible),
        np.count_nonzero(eligible) / 6144,
        np.count_nonzero(det[rows[:3], cols[:3]]),
        float(active[3, 7]),
        np.count_nonzero(active & ~eligible),
        float(eligible[3, 7]),
        power[27, 44] / threshold[27, 44],
        np.count_nonzero(det & ~support),
        float(not p["broken_mode"]),
    ]


def _p51(p):
    k = int(p["os_rank"])
    ca = _r45_alpha(24, 0.001)
    scales = [
        ca,
        _r48_scale(12, 0.001, "GO"),
        _r48_scale(12, 0.001, "SO"),
        _r49_scale(24, k, 0.001),
    ]
    if p["broken_mode"]:
        scales = [ca] * 4
    cells = np.arange(1, 257)
    rng = np.random.default_rng(5101)
    u = -np.log(rng.random(256))
    mean = (
        (1 + 0.2 * np.cos(2 * np.pi * cells / 83))
        * np.where(cells >= 145, 10 ** (p["clutter_contrast_db"] / 10), 1)
        * (1 + 2.5 * np.exp(-0.5 * ((cells - 220) / 18) ** 2))
    )
    power = u * mean
    response = np.array(
        [
            0.004,
            0.008,
            0.015,
            0.025,
            0.01,
            0.05,
            0.02,
            0.12,
            0.03,
            0.25,
            0.55,
            0.85,
            1,
            0.85,
            0.55,
            0.25,
            0.03,
            0.12,
            0.02,
            0.05,
            0.01,
            0.025,
            0.015,
            0.008,
            0.004,
        ]
    )
    targets = [69, 81, 140, 204, 193, 197, 211, 215]
    total = np.zeros(256)
    for center, snr in zip(targets, [28, 14, 14, 13, 20, 20, 20, 20]):
        addition = mean[center] * 10 ** (snr / 10) * response
        power[center - 12 : center + 13] += addition
        total[center - 12 : center + 13] += addition
    detection = np.zeros((256, 4), bool)
    for cut in range(15, 241):
        left = power[cut - 15 : cut - 3]
        right = power[cut + 4 : cut + 16]
        refs = np.r_[left, right]
        lm = sum(left) / 12
        rm = sum(right) / 12
        statistics = [
            sum(refs) / 24,
            max(lm, rm),
            min(lm, rm),
            np.partition(refs, k - 1)[k - 1],
        ]
        detection[cut] = [power[cut] > a * x for a, x in zip(scales, statistics)]
    truth = np.zeros(256, bool)
    truth[targets] = True
    artifact = (total > 0) & ~truth
    misses = np.count_nonzero(~detection[targets], axis=0)
    h0 = np.count_nonzero(detection[:, 0] & ~truth & ~artifact)
    art = np.count_nonzero(detection[:, 0] & artifact)
    disagree = np.count_nonzero(np.any(detection != detection[:, [0]], axis=1))
    law = [
        (1 + scales[0] / 24) ** -24,
        _r48_probability(scales[1], 12, "GO"),
        _r48_probability(scales[2], 12, "SO"),
        _r49_probability(scales[3], 24, k),
    ]
    return [*law, *misses, h0, art, disagree, scales[3], float(not p["broken_mode"])]


def _r52_interval(count, n):
    # Solve the Wilson score inequality's quadratic in the unknown probability.
    z2 = 1.96**2
    rate = count / n
    a = n + z2
    b = -(2 * n * rate + z2)
    c = n * rate * rate
    disc = np.sqrt(b * b - 4 * a * c)
    return (-b - disc) / (2 * a), (-b + disc) / (2 * a)


def _p52(p):
    n = int(p["training_count"])
    pfa = p["design_pfa"]
    rng = np.random.default_rng(5201)
    proper = _r45_alpha(n, pfa)
    known = -np.log(pfa)
    good = bad = 0
    for _ in range(100):
        a, b = _r41_normal(rng, (2000, 65))
        square = (a * a + b * b) / 2
        ratio = square[:, 0] / (np.sum(square[:, 1 : n + 1], axis=1) / n)
        good += np.count_nonzero(ratio > proper)
        bad += np.count_nonzero(ratio > known)
    correlated = textured = 0
    for _ in range(100):
        cr, ci = _r41_normal(rng, (2000, 1))
        ir, ii = _r41_normal(rng, (2000, n + 1))
        re = (np.sqrt(0.65) * cr + np.sqrt(0.35) * ir) / np.sqrt(2)
        im = (np.sqrt(0.65) * ci + np.sqrt(0.35) * ii) / np.sqrt(2)
        cp = re * re + im * im
        correlated += np.count_nonzero(
            n * cp[:, 0] / np.sum(cp[:, 1:], axis=1) > proper
        )
        a, b = _r41_normal(rng, (2000, n + 1))
        driver = rng.normal(size=(2000, n + 1))
        tp = (a * a + b * b) / 2 * np.exp(0.9 * driver - 0.405)
        textured += np.count_nonzero(n * tp[:, 0] / np.sum(tp[:, 1:], axis=1) > proper)
    count = bad if p["broken_mode"] else good
    alpha = known if p["broken_mode"] else proper
    lo, hi = _r52_interval(count, 200000)
    return [
        alpha,
        count,
        count / 200000,
        (1 + alpha / n) ** (-n),
        lo,
        hi,
        correlated / 200000,
        textured / 200000,
        good / 200000,
        (1 + proper / n) ** (-n),
        float(not p["broken_mode"]),
    ]


_REFERENCES.update({f"P{n}": globals()[f"_p{n}"] for n in range(41, 53)})

# Scenario declarations for P41-P52.
SCENARIOS.update({'P41': {'baseline': {'range_correlation': 0.85, 'target_snr_db': -3, 'broken_mode': False}, 'sweep_1': {'range_correlation': 0.5, 'target_snr_db': -3, 'broken_mode': False}, 'sweep_2': {'range_correlation': 0.85, 'target_snr_db': 0, 'broken_mode': False}, 'broken': {'range_correlation': 0.85, 'target_snr_db': -3, 'broken_mode': True}, 'recovery': {'range_correlation': 0.85, 'target_snr_db': -3, 'broken_mode': False}}, 'P42': {'baseline': {'pulse_count': 64, 'hann_weight': 1, 'broken_mode': False}, 'sweep_1': {'pulse_count': 32, 'hann_weight': 1, 'broken_mode': False}, 'sweep_2': {'pulse_count': 64, 'hann_weight': 0, 'broken_mode': False}, 'broken': {'pulse_count': 64, 'hann_weight': 1, 'broken_mode': True}, 'recovery': {'pulse_count': 64, 'hann_weight': 1, 'broken_mode': False}}, 'P43': {'baseline': {'noise_rms': 1, 'clutter_pedestal': 0, 'broken_mode': False}, 'sweep_1': {'noise_rms': 2, 'clutter_pedestal': 0, 'broken_mode': False}, 'sweep_2': {'noise_rms': 1, 'clutter_pedestal': 1, 'broken_mode': False}, 'broken': {'noise_rms': 1, 'clutter_pedestal': 0, 'broken_mode': True}, 'recovery': {'noise_rms': 1, 'clutter_pedestal': 0, 'broken_mode': False}}, 'P44': {'baseline': {'matched_snr_db': 6, 'threshold_sigma': 3.090232306, 'broken_mode': False}, 'sweep_1': {'matched_snr_db': 12, 'threshold_sigma': 3.090232306, 'broken_mode': False}, 'sweep_2': {'matched_snr_db': 6, 'threshold_sigma': 2, 'broken_mode': False}, 'broken': {'matched_snr_db': 6, 'threshold_sigma': 3.090232306, 'broken_mode': True}, 'recovery': {'matched_snr_db': 6, 'threshold_sigma': 3.090232306, 'broken_mode': False}}, 'P45': {'baseline': {'design_pfa': 0.001, 'scene_power_scale': 1, 'broken_mode': False}, 'sweep_1': {'design_pfa': 0.01, 'scene_power_scale': 1, 'broken_mode': False}, 'sweep_2': {'design_pfa': 0.001, 'scene_power_scale': 2, 'broken_mode': False}, 'broken': {'design_pfa': 0.001, 'scene_power_scale': 1, 'broken_mode': True}, 'recovery': {'design_pfa': 0.001, 'scene_power_scale': 1, 'broken_mode': False}}, 'P46': {'baseline': {'guard_cells': 4, 'training_cells': 12, 'broken_mode': False}, 'sweep_1': {'guard_cells': 0, 'training_cells': 12, 'broken_mode': False}, 'sweep_2': {'guard_cells': 4, 'training_cells': 36, 'broken_mode': False}, 'broken': {'guard_cells': 4, 'training_cells': 12, 'broken_mode': True}, 'recovery': {'guard_cells': 4, 'training_cells': 12, 'broken_mode': False}}, 'P47': {'baseline': {'training_count': 16, 'design_pfa': 0.001, 'broken_mode': False}, 'sweep_1': {'training_count': 64, 'design_pfa': 0.001, 'broken_mode': False}, 'sweep_2': {'training_count': 16, 'design_pfa': 0.01, 'broken_mode': False}, 'broken': {'training_count': 16, 'design_pfa': 0.001, 'broken_mode': True}, 'recovery': {'training_count': 16, 'design_pfa': 0.001, 'broken_mode': False}}, 'P48': {'baseline': {'clutter_step_db': 12, 'interferer_power_db': 20, 'broken_mode': False}, 'sweep_1': {'clutter_step_db': 18, 'interferer_power_db': 20, 'broken_mode': False}, 'sweep_2': {'clutter_step_db': 12, 'interferer_power_db': 10, 'broken_mode': False}, 'broken': {'clutter_step_db': 12, 'interferer_power_db': 20, 'broken_mode': True}, 'recovery': {'clutter_step_db': 12, 'interferer_power_db': 20, 'broken_mode': False}}, 'P49': {'baseline': {'os_rank': 18, 'interferer_power_db': 20, 'broken_mode': False}, 'sweep_1': {'os_rank': 22, 'interferer_power_db': 20, 'broken_mode': False}, 'sweep_2': {'os_rank': 18, 'interferer_power_db': 30, 'broken_mode': False}, 'broken': {'os_rank': 18, 'interferer_power_db': 20, 'broken_mode': True}, 'recovery': {'os_rank': 18, 'interferer_power_db': 20, 'broken_mode': False}}, 'P50': {'baseline': {'range_training_half_width': 6, 'doppler_training_half_width': 4, 'broken_mode': False}, 'sweep_1': {'range_training_half_width': 12, 'doppler_training_half_width': 4, 'broken_mode': False}, 'sweep_2': {'range_training_half_width': 6, 'doppler_training_half_width': 8, 'broken_mode': False}, 'broken': {'range_training_half_width': 6, 'doppler_training_half_width': 4, 'broken_mode': True}, 'recovery': {'range_training_half_width': 6, 'doppler_training_half_width': 4, 'broken_mode': False}}, 'P51': {'baseline': {'clutter_contrast_db': 12, 'os_rank': 18, 'broken_mode': False}, 'sweep_1': {'clutter_contrast_db': 18, 'os_rank': 18, 'broken_mode': False}, 'sweep_2': {'clutter_contrast_db': 12, 'os_rank': 22, 'broken_mode': False}, 'broken': {'clutter_contrast_db': 12, 'os_rank': 18, 'broken_mode': True}, 'recovery': {'clutter_contrast_db': 12, 'os_rank': 18, 'broken_mode': False}}, 'P52': {'baseline': {'training_count': 24, 'design_pfa': 0.001, 'broken_mode': False}, 'sweep_1': {'training_count': 8, 'design_pfa': 0.001, 'broken_mode': False}, 'sweep_2': {'training_count': 24, 'design_pfa': 0.003, 'broken_mode': False}, 'broken': {'training_count': 24, 'design_pfa': 0.001, 'broken_mode': True}, 'recovery': {'training_count': 24, 'design_pfa': 0.001, 'broken_mode': False}}})

# P53-P64 independent references. The preceding reference prefix is immutable.
# Seeded input definitions are shared by specification, not by executable imports.
# References use labeling/moments, sparse batch recursion, covariance subtraction,
# whitened distances, event records, scalar assignment, second-moment IMM mixing,
# analytic array sums and covariance-domain beam power.


def _r53_uniform(seed, count, offset=0.5):
    modulus = 2147483647
    return np.array(
        [
            (seed * pow(16807, k + 1, modulus) % modulus + offset) / modulus
            for k in range(count)
        ]
    )


def _r53_normal(seed, count, offset=0.5):
    import math

    uniforms = _r53_uniform(seed, 2 * ((count + 1) // 2), offset)
    values = []
    for first, second in zip(uniforms[::2], uniforms[1::2]):
        radius = math.sqrt(-2 * math.log(first))
        values.extend(
            [
                radius * math.cos(2 * math.pi * second),
                radius * math.sin(2 * math.pi * second),
            ]
        )
    return np.array(values[:count])


def _p53(p):
    from scipy import ndimage

    r, v = np.arange(72) * 15.0, (np.arange(65) - 32) * 0.5
    noise = abs(np.random.default_rng(5301).standard_normal((72, 65)))
    score = 0.25 + 0.20 * noise / noise.max()
    for rt, vt, amplitude, wr, wv in [
        (365.25, 4.2, 5, 20.25, 0.55),
        (742.5, -6.25, 3.6, 15.75, 0.65),
        (392.25, 4.6, 1.8, 10.5, 0.325),
    ]:
        score += amplitude * np.outer(
            np.exp(-0.5 * ((r - rt) / wr) ** 2), np.exp(-0.5 * ((v - vt) / wv) ** 2)
        )
    for a, b, value in [
        (22, 17, 1.42),
        (22, 18, 1.24),
        (55, 52, 1.38),
        (56, 52, 1.20),
        (10, 55, 1.31),
        (35, 9, 1.27),
        (64, 31, 1.34),
    ]:
        score[a - 1, b - 1] = value
    detected = score > 1
    labels, count = ndimage.label(detected, np.ones((3, 3)))
    sizes = np.bincount(labels.ravel())
    accepted = np.flatnonzero(sizes[1:] >= p["minimum_cells"]) + 1
    peaks = np.count_nonzero(
        detected & (score == ndimage.maximum_filter(score, size=3))
    )
    target_ids = [labels[24, 40], labels[50, 20]]
    cells = labels == target_ids[0]
    weights = np.where(cells, np.maximum(score - 1, 0) ** p["weight_exponent"], 0.0)
    center = ndimage.center_of_mass(weights)
    mr, mv = center[0] * 15, (center[1] - 32) * 0.5
    neff = weights.sum() ** 2 / np.sum(weights**2)
    variance = np.sum(weights * (r[:, None] - mr) ** 2) / weights.sum()
    return [
        not p["broken_mode"],
        detected.sum(),
        peaks,
        count,
        peaks if p["broken_mode"] else len(accepted),
        sum(t in accepted for t in target_ids),
        mr,
        mv,
        np.sqrt(variance / neff + 225 / 12),
        neff,
    ]


def _p54(p):
    from scipy.sparse import lil_matrix
    from scipy.sparse.linalg import spsolve

    velocity = np.r_[np.full(40, 20.0), np.full(41, 32.0)]
    position = 1000 + np.r_[0.0, np.cumsum(velocity[:-1])]
    reports = position + 30 * np.random.default_rng(5401).standard_normal(81)
    available = ~np.isin(np.arange(1, 82), [18, 19, 20, 66, 67, 68])
    # Solve all state-recursion constraints together as a block triangular system.
    matrix = lil_matrix((162, 162))
    rhs = np.zeros(162)
    matrix[:2, :2] = np.eye(2)
    rhs[:2] = [reports[0], 0]
    f = np.array([[1.0, 1.0], [0.0, 1.0]])
    for k in range(1, 81):
        gain = (
            np.array([p["alpha_gain"], 0 if p["broken_mode"] else p["beta_gain"]])
            if available[k]
            else np.zeros(2)
        )
        matrix[2 * k : 2 * k + 2, 2 * k : 2 * k + 2] = np.eye(2)
        matrix[2 * k : 2 * k + 2, 2 * k - 2 : 2 * k] = (
            -(np.eye(2) - np.outer(gain, [1.0, 0.0])) @ f
        )
        rhs[2 * k : 2 * k + 2] = gain * reports[k]
    state = spsolve(matrix.tocsr(), rhs).reshape(81, 2)
    prediction = np.r_[state[:1, 0], state[:-1, 0] + state[:-1, 1]]
    mask = available & (np.arange(81) >= 10)
    rms = lambda a: np.sqrt(np.mean(a * a))
    return [
        not p["broken_mode"],
        rms(state[10:, 0] - position[10:]),
        rms(state[10:, 1] - velocity[10:]),
        rms(state[10:40, 0] - position[10:40]),
        state[-1, 1],
        6,
        state[-1, 0],
        rms((reports - prediction)[mask]),
    ]


def _r55_filter(z, sigma_a, sigma_z):
    # Covariance subtraction P+ = P- - C S^-1 C^T, independently of Joseph form.
    f = np.array([[1.0, 1.0], [0.0, 1.0]])
    q = sigma_a**2 * np.array([[0.25, 0.5], [0.5, 1.0]])
    x = np.array([z[0], 0.0])
    cov = np.diag([625.0, 225.0])
    states = [x.copy()]
    covs = [cov.copy()]
    gains = [0.0]
    nis = [0.0]
    for sample in z[1:]:
        x = f @ x
        cov = f @ cov @ f.T + q
        cross = cov[:, 0].copy()
        s = cov[0, 0] + sigma_z**2
        error = sample - x[0]
        x = x + cross / s * error
        cov = cov - np.outer(cross, cross) / s
        cov = (cov + cov.T) / 2
        states.append(x.copy())
        covs.append(cov.copy())
        gains.append(cross[0] / s)
        nis.append(error * error / s)
    return np.array(states), np.array(covs), np.array(gains), np.array(nis)


def _p55(p):
    rng = np.random.default_rng(5501)
    a = 0.8 * rng.standard_normal(100)
    v = 20 + np.r_[0.0, np.cumsum(a)]
    x = 1000 + np.r_[0.0, np.cumsum(v[:-1] + a / 2)]
    z = x + 25 * rng.standard_normal(101)
    state, cov, gain, nis = _r55_filter(
        z, 0 if p["broken_mode"] else p["acceleration_sigma_mps2"], p["report_sigma_m"]
    )
    low_r = _r55_filter(z, p["acceleration_sigma_mps2"], 0.5)[0]
    rms = lambda a: np.sqrt(np.mean(a * a))
    return [
        not p["broken_mode"],
        rms(state[15:, 0] - x[15:]),
        rms(state[15:, 1] - v[15:]),
        nis[15:].mean(),
        np.sqrt(cov[-1, 0, 0]),
        np.sqrt(cov[-1, 1, 1]),
        gain[15:].mean(),
        rms(low_r[15:, 0] - x[15:]),
        np.linalg.eigvalsh(cov).min(),
    ]


def _p56(p):
    from scipy.linalg import cho_factor, cho_solve

    rng = np.random.default_rng(5601)
    a = 0.25 * rng.standard_normal((2, 100))
    velocity = np.array([4.0, -12.0])[:, None] + np.column_stack(
        [np.zeros(2), np.cumsum(a, axis=1)]
    )
    position = np.array([-1600.0, 600.0])[:, None] + np.column_stack(
        [np.zeros(2), np.cumsum(velocity[:, :-1] + a / 2, axis=1)]
    )
    radius = np.sqrt(np.sum(position**2, axis=0))
    theta = np.arctan2(position[1], position[0])
    z = np.column_stack(
        [
            radius + 18 * rng.standard_normal(101),
            theta + np.deg2rad(0.8) * rng.standard_normal(101),
        ]
    )
    z[:, 1] = np.angle(np.exp(1j * z[:, 1]))
    # Independent state ordering [px,py,vx,vy] and Cholesky innovation solves.
    f = np.block([[np.eye(2), np.eye(2)], [np.zeros((2, 2)), np.eye(2)]])
    g = np.vstack([0.5 * np.eye(2), np.eye(2)])
    q = 0.25**2 * g @ g.T
    r = np.diag([324.0, np.deg2rad(p["bearing_sigma_deg"]) ** 2])
    c, si = np.cos(z[0, 1]), np.sin(z[0, 1])
    j = np.array([[c, -z[0, 0] * si], [si, z[0, 0] * c]])
    state = np.array([z[0, 0] * c, z[0, 0] * si, 0.0, 0.0])
    cov = np.zeros((4, 4))
    cov[:2, :2] = j @ np.diag([324.0, np.deg2rad(0.8) ** 2]) @ j.T
    cov[2:, 2:] = 400 * np.eye(2)
    estimates = [state.copy()]
    covs = [cov.copy()]
    angles = [0.0]
    nis = [0.0]
    for sample in z[1:]:
        state = f @ state
        cov = f @ cov @ f.T + q
        xx, yy = state[:2]
        rr = xx * xx + yy * yy
        radius = np.sqrt(rr)
        h = np.array([[xx / radius, yy / radius, 0, 0], [-yy / rr, xx / rr, 0, 0]])
        nu = sample - [radius, np.arctan2(yy, xx)]
        if not p["broken_mode"]:
            nu[1] = np.angle(np.exp(1j * nu[1]))
        cross = cov @ h.T
        s = h @ cross + r
        factor = cho_factor(s)
        gain = cho_solve(factor, cross.T).T
        state += gain @ nu
        cov -= gain @ cross.T
        cov = (cov + cov.T) / 2
        estimates.append(state.copy())
        covs.append(cov.copy())
        angles.append(nu[1])
        nis.append(nu @ cho_solve(factor, nu))
    estimates = np.array(estimates)
    covs = np.array(covs)
    error = estimates[:, :2] - position.T
    tangent = p["geometry_range_m"] * np.deg2rad(p["bearing_sigma_deg"])
    return [
        not p["broken_mode"],
        np.sqrt(np.mean(np.sum(error[15:] ** 2, axis=1))),
        np.mean(nis[15:]),
        np.rad2deg(np.max(abs(np.array(angles)))),
        estimates[-1, 0],
        estimates[-1, 1],
        np.sqrt(np.trace(covs[-1, :2, :2])),
        tangent,
        max(18, tangent),
        np.linalg.eigvalsh(covs).min(),
    ]


def _r57_assignment(cost, gate):
    # Sorted edges with explicit exclusion sets, independent of matrix erasure.
    pairs = sorted(
        (float(cost[i, j]), j, i)
        for i in range(cost.shape[0])
        for j in range(cost.shape[1])
        if gate[i, j]
    )
    used_rows = set()
    used_columns = set()
    result = np.full(cost.shape[0], -1, int)
    for _, j, i in pairs:
        if i not in used_rows and j not in used_columns:
            result[i] = j
            used_rows.add(i)
            used_columns.add(j)
    return result


def _p57(p):
    position = np.array([[0.0, 0.0], [200.0, 50.0], [400.0, -100.0]])
    variance = np.array(
        [
            [45**2 + 5**2 + 0.25, 7**2 + 2**2 + 0.25],
            [12**2 + 4**2 + 0.25, 12**2 + 4**2 + 0.25],
            [14**2 + 4**2 + 0.25, 10**2 + 3**2 + 0.25],
        ]
    )
    targets = (
        position + [[44, 0], [4, -5], [-6, 7]] + 6 * _r53_normal(5701, 6).reshape(3, 2)
    )
    reports = np.array(
        [targets[1], [0, 30], targets[0], [110, 140], targets[2], [520, 40]]
    )
    variances = p["covariance_scale"] * variance + 36
    residual = reports[None, :, :] - position[:, None, :]
    whitened = residual / np.sqrt(variances[:, None, :])
    distance = np.sum(whitened**2, axis=2)
    valid = distance <= p["gate_d2"]
    cost = np.sum(residual**2, axis=2) if p["broken_mode"] else distance
    assignment = _r57_assignment(
        cost, np.ones_like(valid) if p["broken_mode"] else valid
    )
    labels = [2, 0, 1, 0, 3, 0]
    correct = sum(j >= 0 and labels[j] == i + 1 for i, j in enumerate(assignment))
    return [
        not p["broken_mode"],
        sum(assignment >= 0),
        correct,
        valid.sum(),
        distance[0, 2],
        distance[0, 1],
        np.pi * p["gate_d2"] * np.sqrt(np.prod(variances[0])),
        *(assignment + 1),
    ]


def _p58(p):
    scans = np.arange(1, 31)
    target_scans = scans[(scans >= 4) & (scans <= 24) & ~np.isin(scans, [6, 12, 13])]
    target_values = (
        1000 + 12 * (target_scans - 4) + 3 * _r53_normal(5802, len(target_scans), 0)
    )
    targets = dict(zip(target_scans, target_values))
    false_scans = [2, 5, 8, 11, 15, 18, 22, 26]
    false_values = 100 + 100 * np.arange(8) + 20 * (_r53_uniform(5801, 8, 0) - 0.5)
    false = dict(zip(false_scans, false_values))
    records = [
        sorted(
            ([(targets[k], 1)] if k in targets else [])
            + ([(false[k], 0)] if k in false else [])
        )
        for k in scans
    ]
    required, window, coasts = (
        (1, 1, 30)
        if p["broken_mode"]
        else (int(p["confirmation_hits"]), 4, int(p["coast_limit_scans"]))
    )
    tracks = []
    active_counts = []
    # Object/event formulation: lists of observation booleans and state transitions.
    for scan, record in enumerate(records, 1):
        eligible = [i for i, t in enumerate(tracks) if t["deleted"] == 0]
        predictions = {
            i: tracks[i]["position"] + tracks[i]["velocity"] for i in eligible
        }
        edges = sorted(
            (abs(value - predictions[i]), j, i)
            for i in eligible
            for j, (value, _) in enumerate(record)
            if abs(value - predictions[i]) <= 40
        )
        assigned = {}
        used = set()
        for _, j, i in edges:
            if i not in assigned and j not in used:
                assigned[i] = j
                used.add(j)
        for i in eligible:
            t = tracks[i]
            hit = i in assigned
            t["observations"].append(hit)
            t["observations"] = t["observations"][-window:]
            if hit:
                innovation = record[assigned[i]][0] - predictions[i]
                t["position"] = predictions[i] + 0.7 * innovation
                t["velocity"] += 0.2 * innovation
                t["misses"] = 0
            else:
                t["position"] = predictions[i]
                t["misses"] += 1
            if not t["confirmed"] and sum(t["observations"]) >= required:
                t["confirmed"] = scan
            if (
                not t["confirmed"]
                and scan - t["born"] + 1 >= window
                and sum(t["observations"]) < required
            ) or (t["confirmed"] and t["misses"] > coasts):
                t["deleted"] = scan
            t["states"][scan] = (
                4
                if t["deleted"]
                else (1 if not t["confirmed"] else (3 if t["misses"] else 2))
            )
        for j, (value, label) in enumerate(record):
            if j not in used:
                tracks.append(
                    {
                        "position": value,
                        "velocity": 0.0,
                        "observations": [True],
                        "misses": 0,
                        "born": scan,
                        "confirmed": scan if required == 1 else 0,
                        "deleted": 0,
                        "origin": label,
                        "states": {scan: 2 if required == 1 else 1},
                    }
                )
        active_counts.append(sum(t["deleted"] == 0 for t in tracks))
    targets = [t for t in tracks if t["origin"] == 1 and t["confirmed"]]
    first = targets[0] if targets else None
    survived = int(
        first is not None
        and [first["states"].get(k, 0) for k in [12, 13, 14]] == [3, 3, 2]
    )
    return [
        not p["broken_mode"],
        len(tracks),
        sum(t["origin"] == 0 and t["confirmed"] > 0 for t in tracks),
        len(targets),
        min((t["confirmed"] for t in targets), default=0),
        max((t["deleted"] for t in targets), default=0),
        survived,
        max(active_counts),
        active_counts[-1],
    ]


def _r59_scene(seed, sigma, dt, separation=0):
    noise = _r53_normal(seed, 200).reshape(25, 2, 4)
    velocity = np.array([[20.0, 5.0], [20.0, -5.0]])
    times = (np.arange(25) - 12) * dt
    truth = np.array(
        [velocity * t + [[-separation / 2, 0], [separation / 2, 0]] for t in times]
    )
    reports = truth + sigma * noise[:, :, :2]
    vr = velocity + 3 * noise[:, :, 2:]
    reports[1::2] = reports[1::2, ::-1].copy()
    vr[1::2] = vr[1::2, ::-1].copy()
    return truth, reports, vr


def _r59_track(scene, sigma, dt, weight, reuse=False):
    truth, reports, velocity_reports = scene
    x = truth[0].copy()
    velocity = np.array([[20.0, 5.0], [20.0, -5.0]])
    states = []
    truth_ids = []
    duplicates = 0
    for k in range(25):
        predicted = x.copy() if k == 0 else x + dt * velocity
        costs = np.empty((2, 2))
        for i in range(2):
            for j in range(2):
                dx, dy = reports[k, j] - predicted[i]
                dvx, dvy = velocity_reports[k, j] - velocity[i]
                costs[i, j] = (dx * dx + dy * dy) / sigma**2 + weight * (
                    dvx * dvx + dvy * dvy
                ) / 9
        if reuse:
            assignment = np.argmin(costs, axis=1)
        else:
            assignment = _r57_assignment(costs, np.ones((2, 2), bool))
        duplicates += int(assignment[0] == assignment[1])
        truth_ids.append(assignment if k % 2 == 0 else 1 - assignment)
        for i, j in enumerate(assignment):
            residual = reports[k, j] - predicted[i]
            x[i] = predicted[i] + 0.6 * residual
            velocity[i] += 0.25 / dt * residual
        states.append(x.copy())
    ids = np.array(truth_ids)
    wrong = int(np.count_nonzero(ids != [0, 1]))
    changes = int(np.count_nonzero(ids[1:] != ids[:-1]))
    rmse = np.sqrt(np.mean(np.sum((np.array(states) - truth) ** 2, axis=2)))
    return wrong, changes, duplicates, rmse


def _p59(p):
    sigma = p["position_sigma_m"]
    dt = p["scan_interval_s"]
    scene = _r59_scene(5908, sigma, dt)
    position = _r59_track(scene, sigma, dt, 0)
    active = _r59_track(
        scene, sigma, dt, 0 if p["broken_mode"] else 1, p["broken_mode"]
    )
    counts = np.zeros(3)
    for seed in range(5901, 6101):
        high = _r59_scene(seed, 10, dt)
        wide = _r59_scene(seed, sigma, dt, 24)
        counts[0] += _r59_track(high, 10, dt, 0)[0] > 0
        counts[1] += _r59_track(high, 10, dt, 1)[0] > 0
        counts[2] += _r59_track(wide, sigma, dt, 0)[0] > 0
    return [
        not p["broken_mode"],
        active[0],
        position[0],
        active[1],
        active[2],
        active[3],
        *(counts / 200),
    ]


def _r60_scene(strength):
    acceleration = np.zeros((60, 2))
    acceleration[15:25, 1] = strength
    acceleration[38:48, 0] = -strength
    velocity = np.array([20.0, 5.0]) + np.cumsum(acceleration, axis=0)
    position = np.cumsum(velocity - 0.5 * acceleration, axis=0)
    truth = np.column_stack(
        [
            position[:, 0],
            velocity[:, 0],
            acceleration[:, 0],
            position[:, 1],
            velocity[:, 1],
            acceleration[:, 1],
        ]
    )
    return (
        truth,
        position + 10 * _r53_normal(6007, 120).reshape(60, 2),
        np.any(acceleration != 0, axis=1),
    )


def _r60_filter(reports, stay, broken):
    from scipy.linalg import cho_factor, cho_solve

    f = [
        np.kron(np.eye(2), [[1.0, 1, 0], [0, 1, 0], [0, 0, 0]]),
        np.kron(np.eye(2), [[1.0, 1, 0.5], [0, 1, 1], [0, 0, 1]]),
    ]
    g = [np.array([0.5, 1, 1]), np.array([1 / 6, 0.5, 1])]
    q = [np.kron(np.eye(2), s * s * np.outer(a, a)) for s, a in zip([0.35, 0.8], g)]
    matrix = np.eye(2) if broken else np.array([[stay, 1 - stay], [1 - stay, stay]])
    prob = np.array([1.0, 0.0]) if broken else np.array([0.85, 0.15])
    states = np.tile([0.0, 20, 0, 0, 5, 0], (2, 1))
    covs = np.tile(np.diag([100.0, 100, 16, 100, 100, 16]), (2, 1, 1))
    combined = []
    combined_cov = []
    probabilities = []
    indices = [0, 3]
    for z in reports:
        prior = matrix.T @ prob
        next_states = []
        next_cov = []
        logweights = []
        for j in range(2):
            w = prob * matrix[:, j] / prior[j] if prior[j] else np.eye(2)[j]
            mean = w @ states
            # Total second moment minus outer mixed mean, rather than offset accumulation.
            second = sum(
                w[i] * (covs[i] + np.outer(states[i], states[i])) for i in range(2)
            )
            mixed = second - np.outer(mean, mean)
            xp = f[j] @ mean
            pp = f[j] @ mixed @ f[j].T + q[j]
            innovation = z - xp[indices]
            s = pp[np.ix_(indices, indices)] + 100 * np.eye(2)
            factor = cho_factor(s)
            cross = pp[:, indices]
            gain = cho_solve(factor, cross.T).T
            updated = xp + gain @ innovation
            covariance = pp - gain @ cross.T
            next_states.append(updated)
            next_cov.append((covariance + covariance.T) / 2)
            ll = -0.5 * (
                2 * np.log(2 * np.pi)
                + np.linalg.slogdet(s)[1]
                + innovation @ cho_solve(factor, innovation)
            )
            logweights.append(np.log(prior[j]) + ll if prior[j] else -np.inf)
        states = np.array(next_states)
        covs = np.array(next_cov)
        logweights = np.array(logweights)
        prob = np.exp(logweights - max(logweights))
        prob /= prob.sum()
        mean = prob @ states
        second = sum(
            prob[i] * (covs[i] + np.outer(states[i], states[i])) for i in range(2)
        )
        cov = second - np.outer(mean, mean)
        combined.append(mean)
        combined_cov.append((cov + cov.T) / 2)
        probabilities.append(prob.copy())
    return np.array(combined), np.array(combined_cov), np.array(probabilities)


def _p60(p):
    truth, reports, maneuver = _r60_scene(p["maneuver_acceleration_mps2"])
    state, cov, prob = _r60_filter(
        reports, p["mode_stay_probability"], p["broken_mode"]
    )
    fixed = _r60_filter(reports, p["mode_stay_probability"], True)[0]
    rmse = lambda x: np.sqrt(
        np.mean(np.sum((x[:, [0, 3]] - truth[:, [0, 3]]) ** 2, axis=1))
    )
    return [
        not p["broken_mode"],
        rmse(state),
        rmse(fixed),
        prob[maneuver, 1].mean(),
        prob[:, 1].max(),
        state[-1, 0],
        state[-1, 3],
        abs(prob.sum(axis=1) - 1).max(),
        np.linalg.eigvalsh(cov).min(),
    ]


def _r61_snapshot(angle, q, noise=True):
    m = np.arange(8)
    phase = np.deg2rad(20) + 2 * np.pi * q * m * np.sin(np.deg2rad(angle))
    real = np.cos(phase)
    imag = np.sin(phase)
    if noise:
        z = _r53_normal(6101, 16) * 10 ** (-35 / 20) / np.sqrt(2)
        real += z[:8]
        imag += z[8:]
    principal = np.arctan2(imag, real)
    unwrapped = np.unwrap(principal)
    coefficients = np.polynomial.polynomial.polyfit(m, unwrapped, 1)
    fit = coefficients[0] + coefficients[1] * m
    cross_real = np.sum(real[:-1] * real[1:] + imag[:-1] * imag[1:])
    cross_imag = np.sum(real[:-1] * imag[1:] - imag[:-1] * real[1:])
    step = np.arctan2(cross_imag, cross_real)
    return (
        coefficients[1],
        step,
        np.rad2deg(np.arcsin(np.clip(coefficients[1] / (2 * np.pi * q), -1, 1))),
        np.sqrt(np.mean((unwrapped - fit) ** 2)),
        real + 1j * imag,
    )


def _p61(p):
    true_alias = np.rad2deg(np.arcsin(0.6))
    alias = np.rad2deg(np.arcsin(-0.4))
    angle = true_alias if p["broken_mode"] else p["arrival_angle_deg"]
    q = 1 if p["broken_mode"] else p["spacing_wavelengths"]
    active = _r61_snapshot(angle, q, not p["broken_mode"])
    wrong = _r61_snapshot(true_alias, 1, False)
    other = _r61_snapshot(alias, 1, False)
    recovery = _r61_snapshot(true_alias, 0.5, False)
    return [
        not p["broken_mode"],
        2 * np.pi * q * np.sin(np.deg2rad(angle)),
        active[0],
        active[1],
        active[2],
        active[2] - angle,
        active[3],
        max(abs(wrong[4] - other[4])),
        recovery[2],
        -7 * q * np.sin(np.deg2rad(angle)) / 3e9 * 1e12,
    ]


def _r62_sum(m, phase):
    # Analytic finite geometric series, including removable singularities.
    phase = np.asarray(phase)
    den = np.sin(phase / 2)
    out = np.empty(phase.shape, complex)
    singular = abs(den) < 1e-12
    out[singular] = m
    out[~singular] = (
        np.exp(0.5j * (m - 1) * phase[~singular])
        * np.sin(m * phase[~singular] / 2)
        / den[~singular]
    )
    return out


def _r62_pattern(m, q, steer, angles, taper=False):
    phase = 2 * np.pi * q * (np.sin(np.deg2rad(angles)) - np.sin(np.deg2rad(steer)))
    if not taper:
        return abs(_r62_sum(m, phase)) / m
    shift = 2 * np.pi / (m - 1)
    response = 0.54 * _r62_sum(m, phase) - 0.23 * (
        _r62_sum(m, phase + shift) + _r62_sum(m, phase - shift)
    )
    return abs(response) / (0.54 * m - 0.46)


def _r62_metrics(angles, response, steer):
    from scipy.signal import find_peaks

    indices = np.flatnonzero(abs(angles - steer) <= 5)
    peak = indices[np.argmax(response[indices])]
    response = response / response[peak]
    half = 2**-0.5
    lo = np.flatnonzero(response[:peak] <= half)[-1]
    hi = peak + np.flatnonzero(response[peak:] <= half)[0]
    left = np.interp(half, response[lo : lo + 2], angles[lo : lo + 2])
    right = np.interp(
        half, response[hi - 1 : hi + 1][::-1], angles[hi - 1 : hi + 1][::-1]
    )
    nulls = find_peaks(-response)[0]
    a = nulls[nulls < peak][-1]
    b = nulls[nulls > peak][0]
    sidelobe = np.max(response[np.r_[np.arange(a + 1), np.arange(b, len(response))]])
    return right - left, angles[b] - angles[a], 20 * np.log10(sidelobe), angles[peak]


def _p62(p):
    m = int(p["elements"])
    q = 1 if p["broken_mode"] else p["spacing_wavelengths"]
    steer = 30 if p["broken_mode"] else 0
    angles = np.linspace(-90, 90, 7201)
    metrics = _r62_metrics(angles, _r62_pattern(m, q, steer, angles), steer)
    taper = _r62_metrics(angles, _r62_pattern(8, 0.5, 0, angles, True), 0)
    visible = sum(
        abs(np.sin(np.deg2rad(steer)) + order / q) <= 1
        for order in range(-int(np.ceil(2 * q)), int(np.ceil(2 * q)) + 1)
        if order
    )
    return [
        not p["broken_mode"],
        *metrics,
        visible,
        _r62_pattern(m, q, steer, np.array([-30]))[0],
        taper[0],
        taper[2],
        _r62_pattern(m, 0.5, 30, np.array([-30]))[0],
        _r62_pattern(m, q, steer, np.array([-60 + 120 * _r53_uniform(6201, 4)[0]]))[0],
    ]


def _r63_noise(seed, rows, columns):
    u = _r53_uniform(seed, 2 * rows * columns)
    amplitude = np.sqrt(-np.log(u[::2]))
    phase = 2 * np.pi * u[1::2]
    return (
        (amplitude * np.cos(phase) + 1j * amplitude * np.sin(phase))
        .reshape(columns, rows)
        .T
    )


def _r63_scene(seed, m, directions, snr):
    phases = 2 * np.pi * _r53_uniform(seed, 256).reshape(128, 2).T
    source = np.cos(phases) + 1j * np.sin(phases)
    data = _r63_noise(seed + 1, 16, 128)[:m] * 10 ** (-snr / 20)
    for j, direction in enumerate(directions):
        phase = np.pi * np.arange(m) * np.sin(np.deg2rad(direction))
        data += (np.cos(phase) + 1j * np.sin(phase))[:, None] * source[j]
    return data


def _r63_power(data, angles, sign=1):
    # Covariance-domain Bartlett power independently checks snapshot-domain sums.
    m = len(data)
    cov = data @ data.conj().T / data.shape[1]
    phase = sign * np.pi * np.arange(m)[:, None] * np.sin(np.deg2rad(angles))
    a = np.cos(phase) + 1j * np.sin(phase)
    return np.real(np.einsum("ia,ij,ja->a", a.conj(), cov, a, optimize=False)) / m**2


def _r63_peaks(angles, power, truth, radius):
    from scipy.signal import find_peaks

    local = set(find_peaks(power)[0])
    result = []
    flags = []
    for angle in truth:
        domain = np.flatnonzero(abs(angles - angle) <= radius + 1e-10)
        j = domain[np.argmax(power[domain])]
        result.append(angles[j])
        flags.append(j in local)
    return result, flags


def _p63(p):
    m = int(p["elements"])
    snr = p["source_snr_db"]
    angles = np.linspace(-60, 60, 1201)
    baseline = _r63_power(_r63_scene(6301, m, [-20, 25], snr), angles)
    data = _r63_scene(6315, m, [-20, 30], snr)
    bad = _r63_power(data, angles, -1)
    good = _r63_power(data, angles)
    active = bad if p["broken_mode"] else baseline
    expected = [-30, 20] if p["broken_mode"] else [-20, 25]
    peaks, _ = _r63_peaks(angles, active, expected, 5)
    background = (abs(angles + 20) > 10) & (abs(angles - 25) > 10)
    wide = _r63_power(_r63_scene(6311, m, [-12, 12], snr), angles)
    wp, wf = _r63_peaks(angles, wide, [-12, 12], 4)
    large = _r63_power(_r63_scene(6312, 16, [-8, 8], snr), angles)
    lp, lf = _r63_peaks(angles, large, [-8, 8], 5)
    snap = _r63_power(_r63_scene(6314, m, [-20, 25], 0), angles)
    ripple = np.std(
        10 * np.log10(np.maximum(snap / snap.max(), 10 ** (-3.5)))[background], ddof=1
    )
    high = _r63_power(_r63_scene(6313, m, [-20, 25], 15), angles)
    active_background = (
        (abs(angles + 30) > 10) & (abs(angles - 20) > 10)
        if p["broken_mode"]
        else background
    )
    return [
        not p["broken_mode"],
        *peaks,
        active.max(),
        10 * np.log10(np.median(active[active_background]) / active.max()),
        abs(bad - good[::-1]).max(),
        all(wf) and wp[1] - wp[0] > 12,
        all(lf) and lp[1] - lp[0] > 8,
        ripple,
        10 * np.log10(np.median(high[background]) / high.max()),
    ]


def _r64_pattern(q, angles):
    # After boresight phase alignment, both channels share the centered-array phase.
    direction = np.sin(np.deg2rad(angles))
    squint = np.sin(np.deg2rad(q))
    common = np.exp(5.5j * np.pi * direction)

    def real_factor(offset):
        x = np.pi * offset / 2
        return np.divide(
            np.sin(12 * x), 12 * np.sin(x), out=np.ones_like(x), where=abs(x) > 1e-14
        )

    return common * real_factor(direction + squint), common * real_factor(
        direction - squint
    )


def _p64(p):
    squint = p["beam_squint_deg"]
    snr = p["receiver_snr_db"]
    angles = np.linspace(-10, 10, 401)
    left, right = _r64_pattern(squint, angles)
    ratio = ((right - left) / (right + left)).real
    mask = abs(angles) <= 4 + 1e-10
    grid = angles[mask]
    cal = ratio[mask]
    noise = _r63_noise(6401, 16, 256)
    signal = np.exp(1j * (np.pi * np.arange(12) * np.sin(np.deg2rad(2)) + 0.4))
    data = signal[:, None] + noise[:12] * 10 ** (-snr / 20)
    channels = []
    for steer in [-squint, squint]:
        phase = -np.pi * np.arange(12) * np.sin(np.deg2rad(steer))
        coeff = (np.cos(phase) + 1j * np.sin(phase)) / 12
        alignment = np.exp(-1j * np.angle(sum(coeff)))
        channel = sum(coeff[m] * data[m] for m in range(12)) * alignment
        channels.append(channel)
    l, r = channels
    sigma = (r + l) / 2
    delta = (r - l) / 2
    valid = abs(sigma) >= 0.15
    ratios = (delta / sigma).real
    estimates = np.interp(ratios[valid], cal, grid)
    mean_ratio = float((delta.mean() / sigma.mean()).real)
    estimate = np.interp(mean_ratio, cal, grid)
    rmse = np.sqrt(np.mean((estimates - 2) ** 2))
    clipped = np.count_nonzero((ratios[valid] < cal[0]) | (ratios[valid] > cal[-1]))
    bias = np.interp(0.12 / 2.12, cal, grid)
    recovered = np.interp(0.0, cal, grid)
    active = bias if p["broken_mode"] else estimate
    truth = 0 if p["broken_mode"] else 2
    return [
        not p["broken_mode"],
        active,
        active - truth,
        rmse,
        valid.sum(),
        clipped,
        mean_ratio,
        bias,
        recovered,
        (ratio[220] - ratio[180]) / 2,
        abs((right[200] + left[200]) / 2),
    ]


_REFERENCES.update({f"P{n}": globals()[f"_p{n}"] for n in range(53, 65)})

# Scenario declarations for P53-P64.
SCENARIOS.update({'P53': {'baseline': {'minimum_cells': 3, 'weight_exponent': 1, 'broken_mode': False}, 'sweep_1': {'minimum_cells': 18, 'weight_exponent': 1, 'broken_mode': False}, 'sweep_2': {'minimum_cells': 3, 'weight_exponent': 2, 'broken_mode': False}, 'broken': {'minimum_cells': 3, 'weight_exponent': 1, 'broken_mode': True}, 'recovery': {'minimum_cells': 3, 'weight_exponent': 1, 'broken_mode': False}}, 'P54': {'baseline': {'alpha_gain': 0.35, 'beta_gain': 0.08, 'broken_mode': False}, 'sweep_1': {'alpha_gain': 0.85, 'beta_gain': 0.08, 'broken_mode': False}, 'sweep_2': {'alpha_gain': 0.35, 'beta_gain': 0.3, 'broken_mode': False}, 'broken': {'alpha_gain': 0.35, 'beta_gain': 0.08, 'broken_mode': True}, 'recovery': {'alpha_gain': 0.35, 'beta_gain': 0.08, 'broken_mode': False}}, 'P55': {'baseline': {'acceleration_sigma_mps2': 0.8, 'report_sigma_m': 25, 'broken_mode': False}, 'sweep_1': {'acceleration_sigma_mps2': 3.2, 'report_sigma_m': 25, 'broken_mode': False}, 'sweep_2': {'acceleration_sigma_mps2': 0.8, 'report_sigma_m': 100, 'broken_mode': False}, 'broken': {'acceleration_sigma_mps2': 0.8, 'report_sigma_m': 25, 'broken_mode': True}, 'recovery': {'acceleration_sigma_mps2': 0.8, 'report_sigma_m': 25, 'broken_mode': False}}, 'P56': {'baseline': {'bearing_sigma_deg': 0.8, 'geometry_range_m': 1500, 'broken_mode': False}, 'sweep_1': {'bearing_sigma_deg': 3.2, 'geometry_range_m': 1500, 'broken_mode': False}, 'sweep_2': {'bearing_sigma_deg': 0.8, 'geometry_range_m': 3000, 'broken_mode': False}, 'broken': {'bearing_sigma_deg': 0.8, 'geometry_range_m': 1500, 'broken_mode': True}, 'recovery': {'bearing_sigma_deg': 0.8, 'geometry_range_m': 1500, 'broken_mode': False}}, 'P57': {'baseline': {'gate_d2': 5.991, 'covariance_scale': 1, 'broken_mode': False}, 'sweep_1': {'gate_d2': 0.5, 'covariance_scale': 1, 'broken_mode': False}, 'sweep_2': {'gate_d2': 5.991, 'covariance_scale': 4, 'broken_mode': False}, 'broken': {'gate_d2': 5.991, 'covariance_scale': 1, 'broken_mode': True}, 'recovery': {'gate_d2': 5.991, 'covariance_scale': 1, 'broken_mode': False}}, 'P58': {'baseline': {'confirmation_hits': 3, 'coast_limit_scans': 2, 'broken_mode': False}, 'sweep_1': {'confirmation_hits': 4, 'coast_limit_scans': 2, 'broken_mode': False}, 'sweep_2': {'confirmation_hits': 3, 'coast_limit_scans': 0, 'broken_mode': False}, 'broken': {'confirmation_hits': 3, 'coast_limit_scans': 2, 'broken_mode': True}, 'recovery': {'confirmation_hits': 3, 'coast_limit_scans': 2, 'broken_mode': False}}, 'P59': {'baseline': {'position_sigma_m': 6, 'scan_interval_s': 1, 'broken_mode': False}, 'sweep_1': {'position_sigma_m': 10, 'scan_interval_s': 1, 'broken_mode': False}, 'sweep_2': {'position_sigma_m': 6, 'scan_interval_s': 2, 'broken_mode': False}, 'broken': {'position_sigma_m': 6, 'scan_interval_s': 1, 'broken_mode': True}, 'recovery': {'position_sigma_m': 6, 'scan_interval_s': 1, 'broken_mode': False}}, 'P60': {'baseline': {'maneuver_acceleration_mps2': 2, 'mode_stay_probability': 0.94, 'broken_mode': False}, 'sweep_1': {'maneuver_acceleration_mps2': 3.2, 'mode_stay_probability': 0.94, 'broken_mode': False}, 'sweep_2': {'maneuver_acceleration_mps2': 2, 'mode_stay_probability': 0.99, 'broken_mode': False}, 'broken': {'maneuver_acceleration_mps2': 2, 'mode_stay_probability': 0.94, 'broken_mode': True}, 'recovery': {'maneuver_acceleration_mps2': 2, 'mode_stay_probability': 0.94, 'broken_mode': False}}, 'P61': {'baseline': {'arrival_angle_deg': 30, 'spacing_wavelengths': 0.5, 'broken_mode': False}, 'sweep_1': {'arrival_angle_deg': -30, 'spacing_wavelengths': 0.5, 'broken_mode': False}, 'sweep_2': {'arrival_angle_deg': 30, 'spacing_wavelengths': 0.25, 'broken_mode': False}, 'broken': {'arrival_angle_deg': 30, 'spacing_wavelengths': 0.5, 'broken_mode': True}, 'recovery': {'arrival_angle_deg': 30, 'spacing_wavelengths': 0.5, 'broken_mode': False}}, 'P62': {'baseline': {'elements': 8, 'spacing_wavelengths': 0.5, 'broken_mode': False}, 'sweep_1': {'elements': 16, 'spacing_wavelengths': 0.5, 'broken_mode': False}, 'sweep_2': {'elements': 8, 'spacing_wavelengths': 1, 'broken_mode': False}, 'broken': {'elements': 8, 'spacing_wavelengths': 0.5, 'broken_mode': True}, 'recovery': {'elements': 8, 'spacing_wavelengths': 0.5, 'broken_mode': False}}, 'P63': {'baseline': {'elements': 8, 'source_snr_db': 10, 'broken_mode': False}, 'sweep_1': {'elements': 16, 'source_snr_db': 10, 'broken_mode': False}, 'sweep_2': {'elements': 8, 'source_snr_db': -15, 'broken_mode': False}, 'broken': {'elements': 8, 'source_snr_db': 10, 'broken_mode': True}, 'recovery': {'elements': 8, 'source_snr_db': 10, 'broken_mode': False}}, 'P64': {'baseline': {'beam_squint_deg': 3, 'receiver_snr_db': 15, 'broken_mode': False}, 'sweep_1': {'beam_squint_deg': 5, 'receiver_snr_db': 15, 'broken_mode': False}, 'sweep_2': {'beam_squint_deg': 3, 'receiver_snr_db': -5, 'broken_mode': False}, 'broken': {'beam_squint_deg': 3, 'receiver_snr_db': 15, 'broken_mode': True}, 'recovery': {'beam_squint_deg': 3, 'receiver_snr_db': 15, 'broken_mode': False}}})

# P65-P76 independent references. Inputs follow the source specification;
# solvers, projections, transforms and accounting are formulated separately.
from functools import lru_cache


@lru_cache(maxsize=48)
def _r65_uniform(seed, count):
    modulus = 2147483647
    return (
        np.array(
            [(seed * pow(16807, k, modulus)) % modulus for k in range(1, count + 1)],
            float,
        )
        / modulus
    )


def _r65_noise(seed, rows, cols=1, interleaved=False):
    u = _r65_uniform(seed, 2 * rows * cols)
    a, b = (u[::2], u[1::2]) if interleaved else (u[: rows * cols], u[rows * cols :])
    radius = np.sqrt(-np.log(a))
    theta = 2 * np.pi * b
    return (radius * np.cos(theta) + 1j * radius * np.sin(theta)).reshape(cols, rows).T


def _r65_a(angles, n, sign=1, positions=None):
    positions = np.arange(n) / 2 if positions is None else np.asarray(positions)
    phase = (
        sign
        * 2
        * np.pi
        * np.outer(positions, np.sin(np.deg2rad(np.atleast_1d(angles))))
    )
    return np.cos(phase) + 1j * np.sin(phase)


def _r65_cov(x):
    return np.einsum("it,jt->ij", x, x.conj()) / x.shape[1]


def _r65_weight(r, a, alpha):
    from scipy.linalg import cho_factor, cho_solve

    loaded = (r + r.conj().T) / 2 + np.eye(len(r)) * alpha * np.trace(r).real / len(r)
    u = cho_solve(cho_factor(loaded, lower=True), a)
    return u / np.dot(a.conj(), u)


def _r65_account(w, a):
    response = np.sum(w.conj()[:, None] * a, axis=0)
    desired = 10 ** (-0.3) * abs(response[0]) ** 2
    interference = 10**2.5 * abs(response[1]) ** 2
    noise = sum(abs(w) ** 2)
    return (
        10 * np.log10(desired / (interference + noise)),
        abs(response[0]),
        abs(response[1]),
        noise,
    )


def _p65(p):
    n = int(p["snapshots"])
    alpha = p["loading_alpha"]
    a = _r65_a([3, 30], 8)
    x = sum(
        amp * a[:, i, None] * np.exp(2j * np.pi * _r65_uniform(seed, 256))[None, :]
        for i, amp, seed in [(0, 10 ** (-0.15), 6501), (1, 10**1.25, 6502)]
    ) + _r65_noise(6503, 8, 256)
    r = _r65_cov(x[:, :n])
    starved = _r65_cov(x[:, :4])
    wrong = _r65_a(6, 8)[:, 0]
    good = _r65_weight(r, a[:, 0], alpha)
    active = _r65_weight(starved, wrong, 1e-6) if p["broken_mode"] else good
    sinr, true, inter, noise = _r65_account(active, a)
    return [
        sinr,
        _r65_account(a[:, 0] / 8, a)[0],
        true,
        inter,
        noise,
        alpha * np.trace(r).real / 8,
        abs(np.vdot(good, a[:, 0]) - 1),
        float(np.linalg.matrix_rank(starved) < 8),
        _r65_account(_r65_weight(starved, wrong, 0.1), a)[0],
        _r65_account(_r65_weight(starved, a[:, 0], 0.1), a)[0],
        _r65_account(_r65_weight(starved, a[:, 0], alpha), a)[0],
        _r65_account(_r65_weight(_r65_cov(x[:, :8]), wrong, 1e-6), a)[0],
        not p["broken_mode"],
    ]


def _r66_scan(x, angles):
    # Left singular vectors span covariance eigenspaces without forming R.
    u, s, _ = np.linalg.svd(x, full_matrices=False)
    a = _r65_a(angles, len(x))
    projection = u[:, 2:].conj().T @ a
    music = 1 / np.maximum(
        np.einsum("ij,ij->j", projection.conj(), projection).real, 1e-30
    )
    bart = np.mean(abs(a.conj().T @ x / len(x)) ** 2, axis=1)
    return (
        10 * np.log10(np.maximum(bart / max(bart), 1e-6)),
        10 * np.log10(np.maximum(music / max(music), 1e-6)),
        s * s / x.shape[1],
    )


def _r66_peaks(curve, axis, separation=1):
    from scipy.signal import find_peaks

    candidates = find_peaks(curve)[0]
    selected = []
    for i in sorted(candidates, key=lambda i: (-curve[i], i)):
        if not selected or min(abs(axis[i] - axis[selected])) >= separation:
            selected.append(i)
            if len(selected) == 2:
                break
    return np.sort(axis[selected])


def _r66_error(peaks, truth):
    return np.linalg.norm(peaks - truth) / np.sqrt(2) if len(peaks) == 2 else 80.0


def _p66(p):
    d = p["source_separation_deg"]
    snr = p["source_snr_db"]
    truth = np.array([-d / 2, d / 2])
    grid = np.linspace(-40, 40, 801)
    a = _r65_a(truth, 10)
    waves = np.exp(
        2j * np.pi * np.array([_r65_uniform(6601, 512), _r65_uniform(6602, 512)])
    )
    noise = _r65_noise(6603, 10, 512)
    x = 10 ** (snr / 20) * (a @ waves) + noise
    bart, music, _ = _r66_scan(x, grid)
    coherent = (
        10 ** (snr / 20) * np.outer(a[:, 0] + np.exp(0.7j) * a[:, 1], waves[0]) + noise
    )
    _, cm, ce = _r66_scan(coherent, grid)
    # Smoothing via a Hankel-like sample matrix with subarray views.
    stacked = (
        np.lib.stride_tricks.sliding_window_view(coherent, 7, axis=0)
        .transpose(2, 0, 1)
        .reshape(7, -1)
    )
    _, sm, se = _r66_scan(stacked, grid)
    peaks = _r66_peaks(cm if p["broken_mode"] else music, grid)
    indices = [np.argmin(abs(grid - v)) for v in truth]
    mid = 400
    low = _r66_peaks(_r66_scan(10 ** (-10 / 20) * a @ waves + noise, grid)[1], grid)
    short = _r66_peaks(_r66_scan((a @ waves + noise)[:, :16], grid)[1], grid)
    return [
        _r66_error(peaks, truth),
        len(peaks),
        peaks[0] if len(peaks) else 0,
        peaks[-1] if len(peaks) else 0,
        min(music[indices]) - music[mid],
        min(bart[indices]) - bart[mid],
        10 * np.log10(ce[1] / ce[2]),
        10 * np.log10(se[1] / se[2]),
        _r66_error(_r66_peaks(sm, grid), truth),
        _r66_error(low, truth),
        _r66_error(short, truth),
        not p["broken_mode"],
    ]


def _p67(p):
    from scipy.linalg import eigh

    scale = p["error_scale"]
    coupling = p["coupling_magnitude"]
    nominal = _r65_a([-15, 10], 10)
    patterns = []
    for chunk in np.split(_r65_uniform(6701, 30), 3):
        z = chunk - sum(chunk) / 10
        patterns.append(z / np.linalg.norm(z) * np.sqrt(10))
    positions = np.arange(10) / 2 + 0.05 * scale * patterns[2]
    gain = (1 + 0.18 * scale * patterns[0]) * np.exp(
        1j * np.deg2rad(20 * scale * patterns[1])
    )
    near = coupling * np.exp(1j * np.deg2rad(25))
    c = np.array(
        [
            [
                1
                if i == j
                else near
                if abs(i - j) == 1
                else 0.3 * near * near
                if abs(i - j) == 2
                else 0
                for j in range(10)
            ]
            for i in range(10)
        ]
    )
    actual = gain[:, None] * (c @ _r65_a([-15, 10], 10, positions=positions))
    wave = np.array(
        [
            np.sqrt(power) * np.exp(2j * np.pi * _r65_uniform(seed, 512))
            for power, seed in [(10**2.5, 6702), (10, 6703)]
        ]
    )
    noise = _r65_noise(6704, 10, 512)
    ideal = nominal @ wave + noise
    impaired = actual @ wave + noise
    ca = gain * (c @ _r65_a(10, 10, positions=positions)[:, 0])
    cw = np.exp(2j * np.pi * _r65_uniform(6705, 256))
    cn = _r65_noise(6706, 10, 256)
    measured = ca + np.einsum("it,t->i", cn, cw.conj()) / (256 * np.sqrt(1000))
    eq = nominal[:, 1] / measured
    activeeq = 1 / measured if p["broken_mode"] else eq

    def account(x, manifold, n):
        w = _r65_weight(_r65_cov(x), nominal[:, 1], 0.02)
        response = abs(w.conj() @ manifold) ** 2
        return 10 * np.log10(
            10 * response[1] / (10**2.5 * response[0] + sum(abs(w) ** 2 * n))
        ), 10 * np.log10(response[1])

    active = activeeq[:, None] * impaired
    stats = account(active, activeeq[:, None] * actual, abs(activeeq) ** 2)
    # Generalized Hermitian eigenvectors directly account for colored noise.
    _, vectors = eigh(_r65_cov(active), np.diag(abs(activeeq) ** 2))
    grid = np.linspace(-40, 40, 801)
    proj = vectors[:, :8].conj().T @ _r65_a(grid, 10)
    music = 1 / np.sum(abs(proj) ** 2, axis=0)
    peaks = _r66_peaks(music, grid, 2)
    err = lambda z: np.linalg.norm(z * ca - nominal[:, 1]) / np.sqrt(10)
    return [
        stats[0],
        account(impaired, actual, np.ones(10))[0],
        account(ideal, nominal, np.ones(10))[0],
        account(eq[:, None] * impaired, eq[:, None] * actual, abs(eq) ** 2)[0],
        stats[1],
        err(np.ones(10)),
        err(activeeq),
        err(eq),
        _r66_error(peaks, np.array([-15, 10])),
        peaks[0] if len(peaks) else 0,
        np.linalg.norm(eq * actual[:, 0] - nominal[:, 0]) / np.sqrt(10),
        not p["broken_mode"],
    ]


def _p68(p):
    n = int(p["training_cells"])
    frac = 0.4 if p["broken_mode"] else p["contamination_fraction"]

    # Reference channel order is pulse-within-sensor, a permutation of runtime.
    def steer(angle, fd):
        return np.kron(_r65_a(angle, 8)[:, 0], np.exp(2j * np.pi * np.arange(8) * fd))

    angles = np.arange(-60, 61, 2)
    powers = np.cos(np.deg2rad(angles)) ** 2
    powers *= 1000 / sum(powers)
    a = np.column_stack(
        [
            steer(t, 0.35 * np.sin(np.deg2rad(t))) * np.sqrt(power)
            for t, power in zip(angles, powers)
        ]
    )
    perm = np.arange(64).reshape(8, 8).T.ravel()
    noise = _r65_noise(6802, 64, 128)[perm]
    full = a @ _r65_noise(6801, 61, 128) + noise
    x = full[:, :n]
    r = _r65_cov(x)
    population = a @ a.conj().T + np.eye(64)
    assumed = steer(10, 0.2)
    actual = steer(10.7, 0.208)
    clean = _r65_weight(r, assumed, 0.03)
    space = np.zeros((8, 8), complex)
    time = np.zeros((8, 8), complex)
    for k in range(n):
        cell = x[:, k].reshape(8, 8)
        space += cell @ cell.conj().T / (8 * n)
        time += cell.T @ cell.conj() / (8 * n)
    separate = np.kron(
        _r65_weight(space, _r65_a(10, 8)[:, 0], 0.03),
        _r65_weight(time, np.exp(2j * np.pi * np.arange(8) * 0.2), 0.03),
    )
    waveform = _r65_noise(6803, 1, 128)[0]

    def contaminated(frac):
        contaminated = x.copy()
        k = int(np.floor(frac * n + 0.5))
        contaminated[:, :k] += 10 * np.outer(actual, waveform[:k])
        return _r65_weight(_r65_cov(contaminated), assumed, 0.03)

    def stats(w):
        signal = abs(sum(w.conj() * actual)) ** 2
        inter = np.real(sum(w.conj() * (population @ w)))
        return [
            10 * np.log10(signal / inter),
            10 * np.log10(signal),
            10 * np.log10(inter),
        ]

    w = contaminated(frac)
    s = stats(w)
    cut = a @ _r65_noise(6804, 61)[:, 0] + _r65_noise(6805, 64)[:, 0][perm] + actual
    return [
        s[0],
        stats(assumed / 64)[0],
        stats(separate)[0],
        stats(clean)[0],
        s[1],
        s[2],
        abs(sum(w.conj() * assumed) - 1),
        stats(_r65_weight(_r65_cov(full[:, :8]), assumed, 0.03))[0],
        stats(contaminated(0.4))[0],
        abs(sum(w.conj() * cut)),
        np.floor(frac * n + 0.5),
        not p["broken_mode"],
    ]


def _r69_est(range_m, bandwidth):
    fs = 80e6
    s = bandwidth * 1e6 / 40e-6
    t = np.arange(3200) / fs
    tau = 2 * range_m / 3e8
    mask = t >= tau
    phase = 2 * np.pi * s * tau * (t[mask] - 20e-6) - np.pi * s * tau * tau
    tx = np.exp(1j * np.pi * s * (t[mask] - 20e-6) ** 2)
    beat = (
        0.7 * (np.cos(phase) + 1j * np.sin(phase))
        + 0.01 * tx * _r65_noise(6901, 3200)[:, 0][mask].conj()
    )
    count = len(beat)
    window = 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(count) / (count - 1))
    # Evaluate just five DFT bins around the specified tone, independently of FFT.
    center = int(np.floor(s * tau / fs * 65536 + 0.5))
    bins = np.arange(center - 2, center + 3)
    spectrum = np.exp(-2j * np.pi * np.outer(bins, np.arange(count)) / 65536) @ (
        window * beat
    )
    power = abs(spectrum) ** 2
    k = np.argmax(power)
    coef = np.polyfit([-1, 0, 1], np.log(power[k - 1 : k + 2]), 2)
    offset = np.clip(-coef[1] / (2 * coef[0]), -0.5, 0.5)
    frequency = (bins[k] + offset) * fs / 65536
    product = beat[1:] * beat[:-1].conj()
    lag = np.arctan2(sum(product.imag), sum(product.real)) * fs / (2 * np.pi)
    return frequency, lag, count


def _p69(p):
    r = p["target_range_m"]
    b = p["bandwidth_mhz"]
    s = b * 1e6 / 40e-6
    f, lag, n = _r69_est(r, b)
    estimate = 3e8 * f / (2 * s)
    active = estimate * (2 if p["broken_mode"] else 1)
    return [
        active,
        f / 1000,
        2 * s * r / 3e8 / 1000,
        lag / 1000,
        estimate,
        active - r,
        n,
        _r69_est(75, b)[0] / 1000,
        _r69_est(r, 30)[0] / 1000,
        150 / b,
        not p["broken_mode"],
    ]


def _p70(p):
    n = int(p["fast_samples"])
    m = int(p["chirps"])
    lam = 3e8 / 77e9
    truthr = [20, 20, 23]
    truthv = np.array([-3, 3, 3]) * lam / (2 * 64 * 50e-6)
    x = np.zeros((n, m), complex)
    for r, v, amp, phase in zip(truthr, truthv, [1, 0.82, 0.68], [0.1, 0.75, -0.55]):
        fast = np.exp(2j * np.pi * (2 * 3.75e12 * r / 3e8) * np.arange(n) / 12.8e6)
        slow = np.exp(-2j * np.pi * (2 * v / lam) * np.arange(m) * 50e-6 + 1j * phase)
        x += amp * np.outer(fast, slow)
    x += 0.01 * _r65_noise(7001, 512, 64)[:n, :m]
    ra = np.arange(n // 2 + 1) * (512 / n)
    va = -np.arange(-m // 2, m // 2) / (m * 50e-6) * lam / 2
    rows = {int(np.argmin(abs(ra - 23)))}
    for r in truthr:
        k = int(np.argmin(abs(ra - r)))
        rows.update(range(max(0, k - 1), min(len(ra), k + 2)))
    rows = np.array(sorted(rows))
    wr = np.hanning(n)
    wd = np.hanning(m)
    fast = (
        np.exp(-2j * np.pi * np.outer(rows, np.arange(n)) / n)
        @ (x * wr[:, None])
        / sum(wr)
    )
    slow = np.exp(-2j * np.pi * np.outer(np.arange(-m // 2, m // 2), np.arange(m)) / m)
    good = (fast * wd) @ slow.T / sum(wd)
    active = ((abs(fast) if p["broken_mode"] else fast) * wd) @ slow.T / sum(wd)
    isolated = np.where(rows == np.argmin(abs(ra - 23)))[0][0]
    k = np.argmax(abs(active[isolated]))
    kr = np.argmax(abs(good[isolated]))
    audit = []
    for r, v in zip(truthr, truthv):
        ri = np.argmin(abs(ra - r))
        vi = np.argmin(abs(va - v))
        rr = np.arange(max(0, ri - 1), min(len(ra), ri + 2))
        vv = np.arange(max(0, vi - 1), min(m, vi + 2))
        local = abs(good[np.ix_([int(np.where(rows == q)[0][0]) for q in rr], vv)])
        j, i = np.unravel_index(np.argmax(local.T), local.T.shape)
        audit.append((ra[rr[i]], va[vv[j]], local[i, j]))
    return [
        512 / n,
        lam / (2 * m * 50e-6),
        va[k],
        va[kr],
        truthv[2],
        abs(active[isolated, k]),
        audit[0][0],
        audit[0][1],
        audit[2][0],
        audit[2][2],
        not p["broken_mode"],
    ]


def _r71_frequency(range_m, velocity, bandwidth, seed, sign=1, noise=0.002):
    t = np.arange(3200) / 80e6
    tau = 2 * range_m / 3e8
    t = t[t >= tau]
    s = bandwidth * 1e6 / 40e-6
    fd = 2 * velocity / (3e8 / 77e9)
    phase = (
        sign * (2 * np.pi * s * tau * (t - 20e-6) - np.pi * s * tau * tau)
        - 2 * np.pi * fd * t
        - 0.35
    )
    z = (
        np.cos(phase)
        + 1j * np.sin(phase)
        + noise * _r65_noise(seed, 3200)[:, 0][-len(t) :]
    )
    cross = z[:-1].real * z[1:].imag - z[:-1].imag * z[1:].real
    dot = z[:-1].real * z[1:].real + z[:-1].imag * z[1:].imag
    return np.arctan2(sum(cross), sum(dot)) * 80e6 / (2 * np.pi)


def _p71(p):
    v = p["velocity_mps"]
    b = p["bandwidth_mhz"]
    s = b * 1e6 / 40e-6
    fd = 2 * v / (3e8 / 77e9)
    f = _r71_frequency(45, v, b, 7101)
    stationary = 3e8 * f / (2 * s)
    corrected = stationary + 3e8 * fd / (2 * s)
    active = stationary + (-1 if p["broken_mode"] else 1) * 3e8 * fd / (2 * s)
    return [
        f / 1000,
        fd / 1000,
        stationary,
        stationary - 45,
        -77e9 * v / s,
        active,
        active - 45,
        corrected,
        3e8 * _r71_frequency(45, 30, b, 7101) / (2 * s) - 45,
        3e8 * _r71_frequency(45, v, 30, 7101) / (2 * 30e6 / 40e-6) - 45,
        not p["broken_mode"],
    ]


def _r72_solve(up, down):
    # Linear system inversion in physical range/velocity coordinates.
    matrix = np.array(
        [[2 * 5e11 / 3e8, -2 / (3e8 / 77e9)], [-2 * 5e11 / 3e8, -2 / (3e8 / 77e9)]]
    )
    return np.linalg.solve(matrix, np.array([up, down]))


def _r72_multipeaks(sign, seed):
    from scipy.signal import czt

    t = np.arange(3200) / 80e6
    t = t[t >= 130 / 3e8]
    beat = np.zeros(len(t), complex)
    for r, v, amp, phi in zip([30, 65], [15, -10], [1, 0.8], [0.2, -0.6]):
        tau = 2 * r / 3e8
        phase = (
            sign * (2 * np.pi * 5e11 * tau * (t - 20e-6) - np.pi * 5e11 * tau * tau)
            - 2 * np.pi * 2 * v / (3e8 / 77e9) * t
            - phi
        )
        beat += amp * np.exp(1j * phase)
    beat += 0.002 * _r65_noise(seed, 3200)[:, 0][-len(t) :]
    # Chirp-z evaluates the same signed Fourier grid with Bluestein convolution.
    magnitude = abs(
        czt(beat * np.hanning(len(t)), 32768, w=np.exp(-2j * np.pi / 32768), a=-1)
    )
    search = magnitude.copy()
    df = 80e6 / 32768
    out = []
    blank = int(np.ceil(60000 / df))
    for _ in range(2):
        k = np.argmax(search)
        coef = np.polyfit([-1, 0, 1], magnitude[k - 1 : k + 2], 2)
        delta = np.clip(-coef[1] / (2 * coef[0]), -0.5, 0.5)
        out.append((-16384 + k + delta) * df)
        search[max(0, k - blank) : k + blank + 1] = 0
    return np.sort(out)


def _p72(p):
    r = p["target_range_m"]
    v = p["velocity_mps"]
    up = _r71_frequency(r, v, 20, 7201)
    down = _r71_frequency(r, v, 20, 7202, -1)
    estimate = _r72_solve(up, down)
    ups = _r72_multipeaks(1, 7701)
    downs = _r72_multipeaks(-1, 7702)
    ghost = _r72_solve(ups, downs)
    rec = _r72_solve(ups, downs[::-1])
    high = _r72_solve(
        _r71_frequency(r, v, 20, 7201, noise=0.08),
        _r71_frequency(r, v, 20, 7202, -1, 0.08),
    )
    active = ghost[:, 0] if p["broken_mode"] else estimate
    return [
        up / 1000,
        down / 1000,
        active[0],
        active[1],
        estimate[0] - r,
        estimate[1] - v,
        ghost[0, 0],
        ghost[1, 0],
        rec[0, 0],
        rec[1, 0],
        high[0] - r,
        high[1] - v,
        not p["broken_mode"],
    ]


def _r73_data(v, seed):
    lam = 3e8 / 77e9
    slots = np.repeat([0, 1], 4)
    spatial = _r65_a(18, 8, -1)[:, 0]
    slow = np.exp(-2j * np.pi * 2 * v / lam * np.arange(64) * 80e-6)
    slot = np.exp(-2j * np.pi * 2 * v / lam * slots * 40e-6)
    x = np.outer(spatial * slot, slow) + 0.1 * _r65_noise(seed, 8, 64, True)
    correlation = np.vdot(x[:, :-1], x[:, 1:])
    fd = -np.arctan2(correlation.imag, correlation.real) / (2 * np.pi * 80e-6)
    y = (
        np.cos(2 * np.pi * fd * slots * 40e-6)
        + 1j * np.sin(2 * np.pi * fd * slots * 40e-6)
    )[:, None] * x
    return x, y, fd


def _r73_power(n, grid, source):
    # Squared finite geometric series, including its removable singularity.
    delta = (np.sin(np.deg2rad(source)) - np.sin(np.deg2rad(grid))) / 2
    return (np.sinc(n * delta) / np.sinc(delta)) ** 2


def _r73_width(axis, power):

    k = int(np.argmax(power))  # Use the actual half-maximum level, not prominence.
    lo = np.flatnonzero(power[:k] < power[k] / 2)[-1]
    hi = k + np.flatnonzero(power[k:] < power[k] / 2)[0]
    return np.interp(
        power[k] / 2, power[hi - 1 : hi + 1][::-1], axis[hi - 1 : hi + 1][::-1]
    ) - np.interp(power[k] / 2, power[lo : lo + 2], axis[lo : lo + 2])


def _p73(p):
    v = p["velocity_mps"]
    sep = p["source_separation_deg"]
    grid = np.linspace(-60, 60, 1201)
    a = _r65_a(grid, 8, -1)
    x, y, fd = _r73_data(v, 7301)
    bad, rec, badfd = _r73_data(10, 7401)

    def scan(data):
        r = _r65_cov(data)
        return np.real(np.einsum("ik,ij,jk->k", a.conj(), r, a)) / 64

    def peak(data):
        return grid[np.argmax(scan(data))]

    def dip(n):
        power = _r73_power(n, grid, -sep / 2) + _r73_power(n, grid, sep / 2)
        mid = 600
        return max(
            0, 10 * np.log10(min(max(power[: mid + 1]), max(power[mid:])) / power[mid])
        )

    angle = peak(bad if p["broken_mode"] else y)
    return [
        angle,
        angle - 18,
        peak(x),
        fd * (3e8 / 77e9) / 2,
        _r73_width(grid, _r73_power(4, grid, 18)),
        _r73_width(grid, _r73_power(8, grid, 18)),
        dip(4),
        dip(8),
        peak(bad),
        peak(rec),
        badfd * (3e8 / 77e9) / 2,
        not p["broken_mode"],
    ]


def _p74(p):
    from scipy.signal import stft

    speed = p["swing_speed_mps"]
    window = int(p["window_samples"])
    time = np.arange(19200) / 4800
    # Sum analytic phase-modulated torso/limb returns directly.
    common = -4 * np.pi * 1.2 * time / 0.0125
    modulation = 4 * np.pi * speed / (3 * np.pi * 0.0125) * np.sin(3 * np.pi * time)
    clean = (
        np.exp(1j * common)
        + 0.35 * np.exp(1j * (common - modulation + 0.7))
        + 0.28 * np.exp(1j * (common + modulation - 0.9))
    )
    x = (
        clean
        + np.sqrt(1 + 0.35**2 + 0.28**2)
        * 10 ** (-25 / 20)
        * _r65_noise(7401, 1, 19200, True)[0]
    )

    def dominant(record):
        f, _, z = stft(
            record,
            fs=4800,
            window=np.hanning(window),
            nperseg=window,
            noverlap=3 * window // 4,
            nfft=2048,
            return_onesided=False,
            boundary=None,
            padded=False,
        )
        return -f[np.argmax(np.sum(abs(z) ** 2, axis=1))]

    selected = abs(x) if p["broken_mode"] else x
    w = np.hanning(window)
    # Parseval independently verifies the sum of spectral power in frame zero.
    energy = 2048 * np.sum(abs(selected[:window] * w) ** 2) / sum(w) ** 2
    return [
        192,
        2 * (1.2 - speed) / 0.0125,
        2 * (1.2 + speed) / 0.0125,
        dominant(selected),
        dominant(x),
        dominant(abs(x)),
        1 + (19200 - window) // (window // 4),
        window / 4.8,
        4800 / window,
        (window - 1) / (2 * 4800),
        energy,
        not p["broken_mode"],
    ]


def _p75(p):
    target = p["target_cross_range_m"]
    length = p["aperture_length_m"]
    fullpos = np.linspace(-40, 40, 401)
    keep = abs(fullpos) <= length / 2 + 1e-12
    pos = fullpos[keep]
    slant = np.hypot(1000, pos - target)
    phase = -4 * np.pi * (slant - 1000) / 0.06
    axis = np.linspace(995, 1005, 201)
    noise = 10 ** (-30 / 20) * _r65_noise(7501, 401, 201, True)[keep]
    indices = np.argmin(abs(axis[None, :] - slant[:, None]), axis=1)
    measurement = (
        np.exp(-0.5 * ((axis[indices] - slant) / 0.6) ** 2 + 1j * phase)
        + noise[np.arange(len(pos)), indices]
    )
    candidates = np.linspace(-26, 26, 209)

    def score(z):
        return np.array(
            [
                abs(
                    np.vdot(
                        np.exp(-4j * np.pi * (np.hypot(1000, pos - q) - 1000) / 0.06), z
                    )
                )
                / np.linalg.norm(z, 1)
                for q in candidates
            ]
        )

    good = score(measurement)
    active = score(abs(measurement)) if p["broken_mode"] else good
    excursion = max(slant) - min(slant)
    return [
        excursion,
        2 * excursion / 3e8 * 1e9,
        (max(phase) - min(phase)) / (2 * np.pi),
        max(abs(np.diff(phase))),
        len(pos),
        max(active),
        candidates[np.argmax(active)],
        max(good),
        candidates[np.argmax(good)],
        np.mean(noise.real**2 + noise.imag**2),
        not p["broken_mode"],
    ]


def _r76_chirp(b):
    time = (np.arange(240) - 119.5) / 120e6
    phase = np.pi * b * 1e6 / 2e-6 * time * time
    return np.cos(phase) + 1j * np.sin(phase)


def _r76_pair(b, spacing):
    c = _r76_chirp(b)
    auto = np.correlate(c, c, "full") / 240
    profile = np.zeros(600, complex)
    starts = np.floor((np.array([1000, 1000 + spacing]) - 950) / 1.25 + 0.5).astype(int)
    for start in starts:
        profile[start : start + 479] += auto
    centers = starts + 239
    half = max(1, int(np.floor(0.25 * (150 / b) / 1.25 + 0.5)))
    level = min(max(abs(profile[k - half : k + half + 1])) for k in centers)
    return min(abs(profile[centers[0] : centers[1] + 1])) / level


def _p76(p):
    b = p["bandwidth_mhz"]
    spacing = p["pair_spacing_m"]
    c = _r76_chirp(b)
    pos = np.linspace(-40, 40, 401)
    ranges = np.array([1000, 1025, 1070])
    slant = np.hypot(pos[:, None] - [-15, 0, 18], ranges)
    delays = np.floor((slant - 950) / 1.25 + 0.5).astype(int)
    phase = np.array([0, 0.6, -0.9]) - 4 * np.pi * (slant - ranges) / 0.06
    # Compute only matched-filter samples needed for the signature using inner
    # products of zero-extended shifted pulses, rather than an FFT convolution.
    noise = 0.2 * _r65_noise(7601, 401, 361, True)
    ridge = np.zeros(401, complex)
    for row in range(401):
        raw = noise[row].copy()
        for q, amp in enumerate([1, 0.8, 0.6]):
            indices = delays[row, q] + np.arange(240)
            raw[indices] += amp * np.exp(1j * phase[row, q]) * c
        ridge[row] = np.vdot(c, raw[delays[row, 2] : delays[row, 2] + 240]) / 240
        if row == 200:
            center = np.array(
                [
                    np.sum(raw * np.conj(np.pad(c, (k, 361 - 240 - k)))) / 240
                    for k in range(delays[row, 2] - 2, delays[row, 2] + 3)
                ]
            )
    expected = np.exp(1j * phase[:, 2])
    unit = ridge / abs(ridge)
    good = abs(np.mean(unit * expected.conj()))
    bad = abs(np.mean(expected.conj()))
    auto = np.correlate(c, c, "full") / 240
    axis = np.arange(-239, 240) * 1.25
    hpbw = _r73_width(axis, abs(auto) ** 2)
    k = np.argmax(abs(center))
    center_range = 950 + (delays[200, 2] - 2 + k) * 1.25
    return [
        150 / b,
        1.25,
        240,
        bad if p["broken_mode"] else good,
        good,
        bad,
        np.max(abs(slant - (950 + delays * 1.25))),
        hpbw,
        _r76_pair(b, spacing),
        center_range,
        abs(ridge[200]),
        not p["broken_mode"],
    ]


_REFERENCES.update({f"P{n}": globals()[f"_p{n}"] for n in range(65, 77)})

SCENARIOS.update({'P65': {'baseline': {'snapshots': 128, 'loading_alpha': 0.01, 'broken_mode': False}, 'sweep_1': {'snapshots': 4, 'loading_alpha': 0.01, 'broken_mode': False}, 'sweep_2': {'snapshots': 128, 'loading_alpha': 0.1, 'broken_mode': False}, 'broken': {'snapshots': 128, 'loading_alpha': 0.01, 'broken_mode': True}, 'recovery': {'snapshots': 128, 'loading_alpha': 0.01, 'broken_mode': False}}, 'P66': {'baseline': {'source_separation_deg': 6, 'source_snr_db': 10, 'broken_mode': False}, 'sweep_1': {'source_separation_deg': 2, 'source_snr_db': 10, 'broken_mode': False}, 'sweep_2': {'source_separation_deg': 6, 'source_snr_db': -10, 'broken_mode': False}, 'broken': {'source_separation_deg': 6, 'source_snr_db': 10, 'broken_mode': True}, 'recovery': {'source_separation_deg': 6, 'source_snr_db': 10, 'broken_mode': False}}, 'P67': {'baseline': {'error_scale': 1, 'coupling_magnitude': 0.18, 'broken_mode': False}, 'sweep_1': {'error_scale': 1.5, 'coupling_magnitude': 0.18, 'broken_mode': False}, 'sweep_2': {'error_scale': 1, 'coupling_magnitude': 0.3, 'broken_mode': False}, 'broken': {'error_scale': 1, 'coupling_magnitude': 0.18, 'broken_mode': True}, 'recovery': {'error_scale': 1, 'coupling_magnitude': 0.18, 'broken_mode': False}}, 'P68': {'baseline': {'training_cells': 128, 'contamination_fraction': 0, 'broken_mode': False}, 'sweep_1': {'training_cells': 8, 'contamination_fraction': 0, 'broken_mode': False}, 'sweep_2': {'training_cells': 128, 'contamination_fraction': 0.4, 'broken_mode': False}, 'broken': {'training_cells': 128, 'contamination_fraction': 0, 'broken_mode': True}, 'recovery': {'training_cells': 128, 'contamination_fraction': 0, 'broken_mode': False}}, 'P69': {'baseline': {'target_range_m': 45, 'bandwidth_mhz': 20, 'broken_mode': False}, 'sweep_1': {'target_range_m': 75, 'bandwidth_mhz': 20, 'broken_mode': False}, 'sweep_2': {'target_range_m': 45, 'bandwidth_mhz': 30, 'broken_mode': False}, 'broken': {'target_range_m': 45, 'bandwidth_mhz': 20, 'broken_mode': True}, 'recovery': {'target_range_m': 45, 'bandwidth_mhz': 20, 'broken_mode': False}}, 'P70': {'baseline': {'fast_samples': 512, 'chirps': 64, 'broken_mode': False}, 'sweep_1': {'fast_samples': 128, 'chirps': 64, 'broken_mode': False}, 'sweep_2': {'fast_samples': 512, 'chirps': 16, 'broken_mode': False}, 'broken': {'fast_samples': 512, 'chirps': 64, 'broken_mode': True}, 'recovery': {'fast_samples': 512, 'chirps': 64, 'broken_mode': False}}, 'P71': {'baseline': {'velocity_mps': 20, 'bandwidth_mhz': 20, 'broken_mode': False}, 'sweep_1': {'velocity_mps': -30, 'bandwidth_mhz': 20, 'broken_mode': False}, 'sweep_2': {'velocity_mps': 20, 'bandwidth_mhz': 30, 'broken_mode': False}, 'broken': {'velocity_mps': 20, 'bandwidth_mhz': 20, 'broken_mode': True}, 'recovery': {'velocity_mps': 20, 'bandwidth_mhz': 20, 'broken_mode': False}}, 'P72': {'baseline': {'target_range_m': 45, 'velocity_mps': 20, 'broken_mode': False}, 'sweep_1': {'target_range_m': 75, 'velocity_mps': 20, 'broken_mode': False}, 'sweep_2': {'target_range_m': 45, 'velocity_mps': -30, 'broken_mode': False}, 'broken': {'target_range_m': 45, 'velocity_mps': 20, 'broken_mode': True}, 'recovery': {'target_range_m': 45, 'velocity_mps': 20, 'broken_mode': False}}, 'P73': {'baseline': {'velocity_mps': 0, 'source_separation_deg': 16, 'broken_mode': False}, 'sweep_1': {'velocity_mps': 10, 'source_separation_deg': 16, 'broken_mode': False}, 'sweep_2': {'velocity_mps': 0, 'source_separation_deg': 8, 'broken_mode': False}, 'broken': {'velocity_mps': 0, 'source_separation_deg': 16, 'broken_mode': True}, 'recovery': {'velocity_mps': 0, 'source_separation_deg': 16, 'broken_mode': False}}, 'P74': {'baseline': {'swing_speed_mps': 2, 'window_samples': 512, 'broken_mode': False}, 'sweep_1': {'swing_speed_mps': 3, 'window_samples': 512, 'broken_mode': False}, 'sweep_2': {'swing_speed_mps': 2, 'window_samples': 1536, 'broken_mode': False}, 'broken': {'swing_speed_mps': 2, 'window_samples': 512, 'broken_mode': True}, 'recovery': {'swing_speed_mps': 2, 'window_samples': 512, 'broken_mode': False}}, 'P75': {'baseline': {'target_cross_range_m': 0, 'aperture_length_m': 80, 'broken_mode': False}, 'sweep_1': {'target_cross_range_m': 20, 'aperture_length_m': 80, 'broken_mode': False}, 'sweep_2': {'target_cross_range_m': 0, 'aperture_length_m': 20, 'broken_mode': False}, 'broken': {'target_cross_range_m': 0, 'aperture_length_m': 80, 'broken_mode': True}, 'recovery': {'target_cross_range_m': 0, 'aperture_length_m': 80, 'broken_mode': False}}, 'P76': {'baseline': {'bandwidth_mhz': 20, 'pair_spacing_m': 10, 'broken_mode': False}, 'sweep_1': {'bandwidth_mhz': 40, 'pair_spacing_m': 10, 'broken_mode': False}, 'sweep_2': {'bandwidth_mhz': 20, 'pair_spacing_m': 15, 'broken_mode': False}, 'broken': {'bandwidth_mhz': 20, 'pair_spacing_m': 10, 'broken_mode': True}, 'recovery': {'bandwidth_mhz': 20, 'pair_spacing_m': 10, 'broken_mode': False}}})

# P77-P84: alternate numerical formulations from the pinned source equations.
# No production imports or retained production results enter these calculations.
from functools import lru_cache as _last_cache

from scipy.linalg import cho_factor as _last_factor
from scipy.linalg import cho_solve as _last_solve
from scipy.ndimage import map_coordinates as _last_sample
from scipy.signal import czt as _last_czt


@_last_cache(maxsize=16)
def _last_uniform(seed, count, half=False):
    modulus = 2147483647
    return np.fromiter(
        (
            (seed * pow(16807, i + 1, modulus) % modulus + (0.5 if half else 0))
            / modulus
            for i in range(count)
        ),
        float,
        count,
    )


def _last_noise(seed, rows, columns=1, interleaved=False):
    count = rows * columns
    u = _last_uniform(seed, 2 * count)
    a, b = (u[::2], u[1::2]) if interleaved else (u[:count], u[count:])
    magnitude = np.sqrt(-np.log(a))
    phase = 2 * np.pi * b
    return (magnitude * np.cos(phase) + 1j * magnitude * np.sin(phase)).reshape(
        (rows, columns), order="F"
    )


def _last_width(axis, magnitude):
    i = np.argmax(magnitude)
    a = magnitude / max(magnitude)
    level = 2**-0.5
    lo = np.flatnonzero(a[:i] < level)
    hi = np.flatnonzero(a[i + 1 :] < level) + i + 1
    if not len(lo) or not len(hi):
        return float(axis[-1] - axis[0])
    j = lo[-1]
    k = hi[0]
    return float(
        np.interp(level, [a[k], a[k - 1]], [axis[k], axis[k - 1]])
        - np.interp(level, [a[j], a[j + 1]], [axis[j], axis[j + 1]])
    )


def _last_interp(history, indices, queries, start, step):
    shape = queries.shape
    coords = np.vstack(
        (
            np.broadcast_to(np.asarray(indices)[:, None], shape).ravel(),
            ((queries - start) / step).ravel(),
        )
    )
    result = (
        _last_sample(
            history.real, coords, order=1, mode="constant", cval=0, prefilter=False
        )
        + 1j
        * _last_sample(
            history.imag, coords, order=1, mode="constant", cval=0, prefilter=False
        )
    ).reshape(shape)
    return np.where(queries < start + step * (history.shape[1] - 1), result, 0)


def _p77(p):
    count = int(p["aperture_looks"])
    error = 0.01 if p["broken_mode"] else p["path_error_m"]
    platform = np.linspace(-15, 15, 121)
    r_axis = np.linspace(990, 1035, 91)
    target_ranges = np.sqrt(
        (platform[:, None] - np.array([-6, 7])) ** 2 + np.array([1002, 1020]) ** 2
    )
    ph = np.array([0, 0.7]) - 4 * np.pi * (target_ranges - 990) / 0.06
    h = np.zeros((121, 91), complex)
    for k, amplitude in enumerate([1, 0.75]):
        h += (
            amplitude
            * np.sinc((r_axis[None, :] - target_ranges[:, k, None]) / 2.5)
            * (np.cos(ph[:, k, None]) + 1j * np.sin(ph[:, k, None]))
        )
    h += 0.015 * _last_noise(7701, 121, 91, True)
    ids = np.arange((121 - count) // 2, (121 + count) // 2)
    x = np.linspace(-15, 15, 121)
    y = np.linspace(995, 1027, 65)
    profile = np.sin(np.linspace(0, 2 * np.pi, 121))

    def image(e):
        result = []
        for ground in y:
            ranges = np.sqrt(
                (platform[ids, None] - x[None, :]) ** 2
                + (ground + e * profile[ids, None]) ** 2
            )
            sampled = _last_interp(h, ids, ranges, 990, 0.5)
            result.append(
                np.sum(sampled * np.exp(4j * np.pi * (ranges - 990) / 0.06), axis=0)
            )
        return np.array(result)

    clean = image(0)
    active = image(error) if error else clean
    query = np.sqrt((platform[ids] + 6) ** 2 + (1002 + error * profile[ids]) ** 2)[
        :, None
    ]
    terms = _last_interp(h, ids, query, 990, 0.5)[:, 0] * np.exp(
        4j * np.pi * (query[:, 0] - 990) / 0.06
    )
    ridge = _last_interp(h, ids, target_ranges[ids, 0, None], 990, 0.5)[:, 0]
    errs = []
    for tx, ty in [(-6, 1002), (7, 1020)]:
        eligible = (abs(x[None, :] - tx) <= 3) & (abs(y[:, None] - ty) <= 4)
        iy, ix = np.unravel_index(
            np.argmax(np.where(eligible, abs(active), -1)), active.shape
        )
        errs.append([abs(x[ix] - tx), abs(y[iy] - ty)])
    return [
        abs(active[14, 36]),
        abs(clean[14, 36]),
        abs(np.sum(terms)) / np.sum(abs(terms)),
        _last_width(x, abs(active[14])),
        abs(np.mean(ridge / abs(ridge) * np.exp(-1j * ph[ids, 0]))),
        np.max(np.array(errs)[:, 0]),
        np.max(np.array(errs)[:, 1]),
        error,
        count,
        float(not p["broken_mode"]),
    ]


def _p78(p):
    length = p["aperture_length_m"]
    squint = p["squint_offset_m"]
    full = np.linspace(-200, 200, 1601)
    keep = abs(full) <= length / 2
    platform = full[keep]
    axis = np.linspace(955, 1075, 241)
    r = np.sqrt((platform - squint) ** 2 + 1000**2)
    h = (
        np.sinc((axis[None, :] - r[:, None]) / 2)
        * np.exp(1j * (0.3 - 4 * np.pi * (r[:, None] - 955) / 0.3))
        + 0.02 * _last_noise(7801, 1601, 241, True)[keep]
    )
    ids = np.arange(len(platform))
    delta = r - r[len(r) // 2]

    def aligned(sign):
        return _last_interp(h, ids, axis[None, :] + sign * delta[:, None], 955, 0.5)

    correct = aligned(1)
    active = aligned(-1) if p["broken_mode"] else correct
    comp = np.exp(4j * np.pi * (r - 955) / 0.3)
    fixed = np.sum(comp[:, None] * h, axis=0)
    profile = np.sum(comp[:, None] * active, axis=0)
    concentration = lambda a: np.max(abs(a) ** 2) / np.sum(abs(a) ** 2)
    true = r[:, None]
    fixed_ranges = np.full(true.shape, np.sqrt(squint * squint + 1000**2))
    following = np.sum(_last_interp(h, ids, true, 955, 0.5)[:, 0] * comp)
    fixed_pixel = np.sum(_last_interp(h, ids, fixed_ranges, 955, 0.5)[:, 0] * comp)
    return [
        np.ptp(r),
        np.ptp(axis[np.argmax(abs(h), axis=1)]),
        np.ptp(axis[np.argmax(abs(active), axis=1)]),
        max(abs(profile)) / max(abs(fixed)),
        concentration(profile) / concentration(fixed),
        abs(fixed_pixel) / abs(following),
        np.ptp(axis[np.argmax(abs(correct), axis=1)]),
        length,
        squint,
        float(not p["broken_mode"]),
    ]


def _last_psl(axis, a):
    a = abs(a)
    a /= max(a)
    peak = np.argmax(a)
    low = [i for i in range(1, peak) if a[i] <= a[i - 1] and a[i] < a[i + 1]][-1]
    high = next(
        i for i in range(peak + 1, len(a) - 1) if a[i] <= a[i - 1] and a[i] < a[i + 1]
    )
    return _last_width(axis, a), 20 * np.log10(max(max(a[: low + 1]), max(a[high:])))


def _last_aperture79(axis, positions, weights):
    # Rationalized path difference avoids subtracting two near-equal slant ranges.
    delta = (axis[None, :] ** 2 - 2 * positions[:, None] * axis[None, :]) / (
        np.sqrt((positions[:, None] - axis[None, :]) ** 2 + 1e6)
        + np.sqrt(positions[:, None] ** 2 + 1e6)
    )
    phase = 4 * np.pi * delta / 0.03
    return (
        np.sum(weights[:, None] * np.cos(phase), axis=0)
        + 1j * np.sum(weights[:, None] * np.sin(phase), axis=0)
    ) / sum(weights)


def _p79(p):
    bandwidth = p["bandwidth_mhz"] * 1e6
    length = p["aperture_length_m"]
    broken = p["broken_mode"]
    r = np.linspace(-6, 6, 2401)
    x = np.linspace(-8, 8, 3201)
    # Exact centered finite-frequency geometric series, not a continuous-band sinc.
    step = bandwidth / 256
    angle = 2 * np.pi * step * r / 3e8
    response = np.ones(len(r))
    nonzero = abs(np.sin(angle)) > 1e-14
    response[nonzero] = np.sin(257 * angle[nonzero]) / (257 * np.sin(angle[nonzero]))
    dense = np.linspace(-length / 2, length / 2, int(length / 0.25) + 1)
    spacing = 5 if broken else 0.25
    activepos = np.linspace(-length / 2, length / 2, int(length / spacing) + 1)
    active = _last_aperture79(x, activepos, np.ones(len(activepos)))
    weights = 0.54 - 0.46 * np.cos(2 * np.pi * np.arange(len(dense)) / (len(dense) - 1))
    tapered = _last_aperture79(x, dense, weights)
    rw, rsl = _last_psl(r, response)
    cw, csl = _last_psl(x, active)
    hw, hsl = _last_psl(x, tapered)
    return [
        rw,
        cw,
        rsl,
        csl,
        hw,
        hsl,
        max(abs(active[abs(x) > 1.5])),
        len(activepos),
        3e8 / (2 * bandwidth),
        15 / length,
        float(not broken),
    ]


def _p80(p):
    fraction = p["error_rms_wavelengths"]
    mix = p["random_fraction"]
    platform = np.linspace(-15, 15, 121)
    targets = np.array([-1, 0.35, 1.45])
    ground = np.array([990, 1000, 1009])
    x = np.linspace(-4, 4, 401)
    amp = np.array([1, 0.7, 0.5]) * np.exp(2j * np.pi * _last_uniform(8001, 3, True))
    paths = np.sqrt((platform[:, None] - targets[None, :]) ** 2 + ground[None, :] ** 2)
    signal = amp * np.exp(-4j * np.pi * (paths - 1000) / 0.03)
    u = _last_uniform(8002, 726, True)
    circle = np.sqrt(-2 * np.log(u[::2])) * np.exp(2j * np.pi * u[1::2])
    normal = np.column_stack((circle.real, circle.imag)).ravel()
    noise = (
        10 ** (-35 / 20)
        / np.sqrt(2)
        * (
            normal[:363].reshape((121, 3), order="F")
            + 1j * normal[363:].reshape((121, 3), order="F")
        )
    )
    norm = lambda a: (a - np.mean(a)) / np.std(a)
    s = np.linspace(0, 1, 121)
    smooth = norm(np.sin(2 * np.pi * s + 0.3) + 0.35 * np.sin(6 * np.pi * s - 0.4))
    raw = _last_uniform(8003, 121, True) - 0.5
    # The symmetric seven-point smoothing is summed by offsets rather than convolved.
    padded = np.pad(raw, (3, 3))
    random = norm(
        sum(
            weight * padded[k : k + 121]
            for k, weight in enumerate(np.array([1, 2, 3, 4, 3, 2, 1]) / 16)
        )
    )
    phase = -4 * np.pi * fraction * norm((1 - mix) * smooth + mix * random)
    measured = signal * np.exp(1j * phase[:, None]) + noise

    def estimate(reference):
        return np.unwrap(
            np.angle(reference * np.exp(4j * np.pi * (paths[:, 0] - 1000) / 0.03))
        )

    correct_est = estimate(measured[:, 0])
    est = (
        estimate(measured[:, 0] + 0.95 * measured[:, 1])
        if p["broken_mode"]
        else correct_est
    )

    def focus(h):
        focused = []
        for k, rr in enumerate(ground):
            hypothesized = np.sqrt((platform[:, None] - x[None, :]) ** 2 + rr**2)
            focused.append(
                np.sum(
                    h[:, k, None] * np.exp(4j * np.pi * (hypothesized - 1000) / 0.03),
                    axis=0,
                )
                / 121
            )
        return np.array(focused)

    ideal = focus(signal + noise)
    blurred = focus(measured)
    active = focus(measured * np.exp(-1j * est[:, None]))
    recovered = focus(measured * np.exp(-1j * correct_est[:, None]))

    def metrics(h):
        power = abs(h) ** 2
        prob = power / np.sum(power, axis=1)[:, None]
        return np.mean(np.max(abs(h), axis=1) / np.max(abs(ideal), axis=1)), np.mean(
            -np.sum(prob * np.log(np.maximum(prob, 1e-300)), axis=1)
        )

    peak, entropy = metrics(active)
    bp, be = metrics(blurred)
    gp, _ = metrics(recovered)
    residual = est - phase
    residual -= np.mean(residual)
    return [
        30 * fraction,
        np.sqrt(np.mean(phase**2)),
        peak,
        bp,
        gp,
        entropy,
        be,
        np.sqrt(np.mean(residual**2)),
        np.mean([_last_width(x, abs(a)) for a in active]),
        mix,
        float(not p["broken_mode"]),
    ]


def _p81(p):
    aperture = p["angular_aperture_deg"]
    rate = p["rotation_rate_deg_s"]
    theta = np.linspace(-aperture / 2, aperture / 2, 65) * np.pi / 180
    time = theta / (rate * np.pi / 180)
    f = np.linspace(9.7e9, 10.3e9, 129)
    xx = np.array([0, 0, 0, 0, -2, -1, 1, 2, -0.75, 0.75])
    yy = np.array([-1.5, -0.5, 0.5, 1.5, 0, 0, 0, 0, -1.25, -1.25])
    weights = np.array([1, 0.75, 0.85, 0.9, 0.8, 0.65, 0.65, 0.8, 0.55, 0.55]) * np.exp(
        2j * np.pi * _last_uniform(8101, 10)
    )
    distances = (
        2 * time[:, None] + np.sin(theta[:, None]) * xx + np.cos(theta[:, None]) * yy
    )
    raw = np.sum(
        weights[None, None, :]
        * np.exp(-4j * np.pi * f[None, :, None] * distances[:, None, :] / 3e8),
        axis=2,
    )
    aligned = raw * np.exp(4j * np.pi * f[None, :] * (2 * time[:, None]) / 3e8)
    k = np.arange(-64, 65)
    l = np.arange(-32, 33)
    range_matrix = np.exp(2j * np.pi * np.outer(k, k) / 129) / 129
    angle_matrix = np.exp(-2j * np.pi * np.outer(l, l) / 65) / 65
    focus = lambda h: (angle_matrix @ h @ range_matrix)[::-1].T
    good = focus(aligned)
    active = focus(raw) if p["broken_mode"] else good
    ranges = k * 3e8 / (2 * 129 * (6e8 / 128))
    cross = (-0.03 * l / (2 * 65 * (theta[1] - theta[0])))[::-1]
    mask = np.zeros(active.shape, bool)
    for x, y in zip(xx, yy):
        row = np.argmin(abs(ranges - y))
        col = np.argmin(abs(cross - x))
        mask[max(0, row - 1) : row + 2, max(0, col - 1) : col + 2] = True
    power = abs(active) ** 2
    corr = np.corrcoef(abs(active).ravel(), abs(good).ravel())[0, 1]
    return [
        np.sum(power[mask]) / np.sum(power),
        10 * np.log10(np.max(power[mask]) / np.median(power[~mask])),
        corr,
        aperture / rate,
        2 * aperture / rate,
        0.25,
        0.03 / (2 * aperture * np.pi / 180),
        np.max(abs(active)),
        rate,
        float(not p["broken_mode"]),
    ]


def _last_qpsk82(seed, n):
    u = _last_uniform(seed, 2 * n).reshape(n, 2)
    bits = np.where(u >= 0.5, 1.0, -1.0)
    z = bits[:, 0] + 1j * bits[:, 1]
    z -= np.mean(z)
    return z / np.sqrt(np.mean(abs(z) ** 2))


def _p82(p):
    delay = int(p["target_delay_samples"])
    quality = p["reference_quality_db"]
    n = 4096
    symbols = _last_qpsk82(8201, 1024)
    symbols -= symbols.mean()
    symbols /= np.sqrt(np.mean(abs(symbols) ** 2))
    impulses = np.zeros(n, complex)
    impulses[::4] = symbols
    k = np.arange(-12, 13)
    pulse = np.sinc(k / 4) * (0.5 + 0.5 * np.cos(np.pi * k / 12))
    pulse /= np.linalg.norm(pulse)
    clean = np.convolve(impulses, pulse, "same")
    clean /= np.sqrt(np.mean(abs(clean) ** 2))
    reference = clean + 10 ** (-quality / 20) * _last_qpsk82(8202, n)
    reference /= np.sqrt(np.mean(abs(reference) ** 2))
    shifted = lambda d: np.r_[np.zeros(d, complex), clean[: n - d]]
    surveillance = (
        2.5 * clean
        + 0.1 * shifted(11)
        + 0.18 * shifted(delay) * np.exp(2j * np.pi * 500 * np.arange(n) / 2e5)
        + 0.08 * _last_qpsk82(8203, n)
    )
    coefficient = np.linalg.lstsq(reference[:, None], surveillance, rcond=None)[0][0]
    residual = surveillance - (0.2 if p["broken_mode"] else 1) * coefficient * reference
    lags = np.array(
        [np.r_[np.zeros(d, complex), reference[: n - d]] for d in range(65)]
    )
    products = residual[None, :] * lags.conj()
    ambiguity = _last_czt(
        products,
        m=41,
        w=np.exp(-2j * np.pi * 50 / 2e5),
        a=np.exp(-2j * np.pi * 1000 / 2e5),
        axis=1,
    ).T
    coherence = abs(ambiguity) / np.sqrt(
        np.sum(abs(residual) ** 2) * np.sum(abs(lags) ** 2, axis=1)[None, :]
    )
    mask = np.ones(coherence.shape, bool)
    mask[29:32, max(0, delay - 2) : delay + 3] = False
    peak = np.unravel_index(np.argmax(coherence), coherence.shape)
    return [
        peak[1],
        -1000 + 50 * peak[0],
        1.5 * peak[1],
        coherence[30, delay],
        20 * np.log10(coherence[30, delay] / np.median(coherence[mask])),
        coherence[20, 0],
        abs(coefficient),
        np.sqrt(np.mean(abs(residual) ** 2)),
        quality,
        float(not p["broken_mode"]),
    ]


def _p83(p):
    support = int(p["training_cells"])
    fraction = 0.25 if p["broken_mode"] else p["contaminated_fraction"]
    # Sensor-major vectors are a permutation of the source's pulse-major storage.
    steering = lambda a, d: np.exp(
        1j
        * (
            np.pi * np.arange(4)[:, None] * np.sin(np.deg2rad(a))
            + 2 * np.pi * np.arange(8)[None, :] * d
        )
    ).ravel()
    perm = np.arange(32).reshape(8, 4).T.ravel()
    angles = np.arange(-60, 61, 3)
    power = np.cos(np.deg2rad(angles)) ** 2
    power *= 10**3.2 / np.sum(power)
    manifold = np.array(
        [
            steering(a, 0.3 * np.sin(np.deg2rad(a))) * np.sqrt(q)
            for a, q in zip(angles, power)
        ]
    ).T
    known = np.einsum("ik,jk->ij", manifold, manifold.conj()) + np.eye(32)
    background = manifold @ _last_noise(8301, 41, 48) + _last_noise(8302, 32, 48)[perm]
    actual = steering(12.5, 0.125)
    record = background.copy()
    record[:, 24] += 10**0.9 * actual
    selected = background[:, np.r_[4:22, 27:45][:support]]
    active = selected.copy()
    count = int(np.floor(fraction * support + 0.5))
    active[:, :count] += (
        np.sqrt(1000) * actual[:, None] * _last_noise(8303, 1, 36)[:, :count]
    )
    cov = lambda a: np.einsum("ik,jk->ij", a, a.conj()) / support
    clean = cov(selected)
    contaminated = cov(active)
    load = lambda r: r + np.eye(32) * (0.05 * np.trace(r).real / 32)
    grid = np.linspace(-0.25, 0.25, 51)
    s = np.array([steering(12, d) for d in grid]).T

    def solve(r):
        u = _last_solve(_last_factor(load(r)), s)
        den = np.einsum("ij,ij->j", s.conj(), u).real
        return u, u / den, den

    u, w, den = solve(contaminated)
    _, wc, _ = solve(clean)
    fixed = s / 32
    adaptive = abs(u.conj().T @ record) ** 2 / den[:, None]
    rd = (
        abs(fixed.conj().T @ record) ** 2
        / np.einsum("ij,ij->j", fixed.conj(), load(clean) @ fixed).real[:, None]
    )

    def components(weight):
        sig = 10**1.8 * abs(np.sum(weight.conj() * actual)) ** 2
        inter = np.sum(weight.conj() * (known @ weight)).real
        return 10 * np.log10(sig / inter), sig, inter

    a, signal, interference = components(w[:, 37])
    c, cs, ci = components(wc[:, 37])
    r, _, _ = components(fixed[:, 37])
    mask = np.ones(adaptive.shape, bool)
    mask[36:39, 22:27] = False
    contrast = lambda m: 10 * np.log10(m[37, 24] / np.median(m[mask]))
    peak = np.unravel_index(np.argmax(adaptive), adaptive.shape)
    return [
        a,
        c,
        r,
        contrast(adaptive),
        contrast(rd),
        10 * np.log10(signal / cs),
        10 * np.log10(interference / ci),
        abs(np.sum(w[:, 37].conj() * s[:, 37]) - 1),
        peak[1] + 1,
        grid[peak[0]],
        count,
        float(not p["broken_mode"]),
    ]


def _last_scan84(scan):
    time = (np.arange(32) - 15.5) / 4e6
    pulse = np.exp(1j * np.pi * 2.5e11 * time**2) / np.sqrt(32)
    velocity = np.array([0, 30, -15, -15])
    ranges = np.array([900, 1650, 2550, 2625]) - velocity * (scan - 1)
    indices = np.floor(ranges / 37.5 + 0.5).astype(int)
    amps = np.array([1.8, 2.2, 3, 0.22])
    amps[1] *= scan != 4
    scale = np.where(np.arange(128) < 48, 0.015, 0.2)
    raw = np.broadcast_to(
        (scale * _last_noise(8411, 128).ravel())[:, None], (128, 32)
    ).copy()
    for j in range(4):
        raw[indices[j]] += amps[j] * np.exp(
            2j * np.pi * (2 * velocity[j] / 0.03) * np.arange(32) / 31250
        )
    cube = np.column_stack([np.convolve(raw[:, j], pulse)[:128] for j in range(32)])
    cube[104:] += 0.85 * pulse[:24, None] * np.exp(2j * np.pi * 5 * np.arange(32) / 32)
    cube += 0.18 * _last_noise(8501 + scan, 128, 32)
    measured = cube + 0.12 * cube.conj() + 0.04 + 0.03j
    # Solve the two real receiver quadratures instead of complex image inversion.
    corrected = (measured.real - 0.04) / 1.12 + 1j * (measured.imag - 0.03) / 0.88
    return (
        pulse,
        corrected,
        ranges,
        velocity,
        indices,
        float(np.max(abs(corrected - cube))),
    )


def _last_reports84(power, pfa):
    noise = np.zeros((116, 24))
    for dr in range(-6, 7):
        for dd in range(-4, 5):
            if abs(dr) > 2 or abs(dd) > 1:
                noise += power[6 + dr : 122 + dr, 4 + dd : 28 + dd]
    threshold = np.zeros_like(power)
    threshold[6:122, 4:28] = (pfa ** (-1 / 102) - 1) * noise
    eligible = np.zeros(power.shape, bool)
    eligible[6:122, 4:28] = True
    detection = eligible & (power > threshold)
    unseen = set(map(tuple, np.argwhere(detection)))
    reports = []
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        queue = [start]
        component = []
        while queue:
            r, d = queue.pop()
            component.append((r, d))
            for rr in range(r - 1, r + 2):
                for dd in range(d - 1, d + 2):
                    if (rr, dd) in unseen:
                        unseen.remove((rr, dd))
                        queue.append((rr, dd))
        cells = np.array(sorted(component))
        r, d = cells.T
        weights = np.maximum(power[r, d] / threshold[r, d] - 1, 0)
        reports.append(
            (
                np.average(r * 37.5, weights=weights),
                np.average((d - 16) * 14.6484375, weights=weights),
                np.max(power[r, d]),
            )
        )
    return reports, detection, eligible


def _last_process84(cube, pulse, pfa, taper, wrong=False):
    replica = pulse * (
        1 - taper + taper * (0.5 - 0.5 * np.cos(2 * np.pi * np.arange(32) / 31))
    )
    replica /= np.sqrt(np.sum(abs(replica) ** 2))
    kernel = replica[::-1] if wrong else replica[::-1].conj()
    compressed = np.column_stack(
        [np.convolve(cube[:, j], kernel)[31:159] for j in range(32)]
    )
    window = 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(32) / 31)
    transform = np.exp(-2j * np.pi * np.outer(np.arange(32), np.arange(-16, 16)) / 32)
    power = abs((compressed * window) @ transform / np.sum(window)) ** 2
    return (power, *_last_reports84(power, pfa))


def _last_score84(product, ranges, velocity, indices):
    _power, reports, detected, eligible = product
    # Dynamic programming over four truth bits finds maximum one-to-one cardinality.
    masks = {0}
    for r, v, _ in reports:
        edges = [
            i
            for i in range(4)
            if abs(r - ranges[i]) <= 75 and abs(v - velocity[i]) <= 1.5 * 14.6484375
        ]
        masks |= {
            mask | (1 << i)
            for mask in list(masks)
            for i in edges
            if not mask & (1 << i)
        }
    count = max(mask.bit_count() for mask in masks)
    background = eligible.copy()
    bins = np.floor((2 * velocity / 0.03) / 31250 * 32 + 0.5).astype(int) + 16
    for r, d in zip(indices, bins):
        background[max(0, r - 2) : min(128, r + 3), max(0, d - 1) : min(32, d + 2)] = (
            False
        )
    return (
        count,
        len(reports) - count,
        np.sum(detected & background) / np.sum(background),
    )


@_last_cache(maxsize=1)
def _last_tracking84():
    history = []
    matches = 0
    for scan in range(1, 9):
        pulse, cube, r, v, indices, _ = _last_scan84(scan)
        out = _last_process84(cube, pulse, 0.001, 0)
        history.append(out[1])
        matches += _last_score84(out, r, v, indices)[0]
    first = max(
        (a for a in history[0] if 1300 < a[0] < 2000 and a[1] > 0), key=lambda a: a[2]
    )
    state = np.array([first[0], -first[1]])
    positions = [state[0]]
    coasts = [0]
    for reports in history[1:]:
        state = np.array([[1, 1], [0, 1]]) @ state
        candidates = [
            a
            for a in reports
            if abs(a[0] - state[0]) <= 225 and abs(a[1] + state[1]) <= 35
        ]
        if candidates:
            chosen = min(
                candidates,
                key=lambda a: abs(a[0] - state[0]) / 225 + abs(a[1] + state[1]) / 35,
            )
            state += np.array([0.65, 0.18]) * (chosen[0] - state[0])
            coasts.append(0)
        else:
            coasts.append(coasts[-1] + 1)
        positions.append(state[0])
    return (
        matches / 32,
        np.sqrt(np.mean((np.array(positions) - (1650 - 30 * np.arange(8))) ** 2)),
        coasts[3],
    )


def _p84(p):
    pulse, cube, r, v, indices, error = _last_scan84(1)
    pfa = p["design_pfa"]
    taper = p["replica_taper"]
    good = _last_process84(cube, pulse, pfa, taper)
    active = (
        _last_process84(cube, pulse, pfa, taper, True) if p["broken_mode"] else good
    )
    matches, false, rate = _last_score84(active, r, v, indices)
    pd, rmse, coast = _last_tracking84()
    return [
        np.max(active[0]),
        np.max(active[0]) / np.max(good[0]),
        np.sum(active[2]),
        len(active[1]),
        matches,
        false,
        rate,
        pd,
        rmse,
        coast,
        error,
        float(not p["broken_mode"]),
    ]


_REFERENCES.update({f"P{n}": globals()[f"_p{n}"] for n in range(77, 85)})
SCENARIOS.update({'P77': {'baseline': {'aperture_looks': 121,
                      'path_error_m': 0,
                      'broken_mode': False},
         'sweep_1': {'aperture_looks': 21,
                     'path_error_m': 0,
                     'broken_mode': False},
         'sweep_2': {'aperture_looks': 121,
                     'path_error_m': 0.005,
                     'broken_mode': False},
         'broken': {'aperture_looks': 121,
                    'path_error_m': 0,
                    'broken_mode': True},
         'recovery': {'aperture_looks': 121,
                      'path_error_m': 0,
                      'broken_mode': False}},
 'P78': {'baseline': {'aperture_length_m': 400,
                      'squint_offset_m': 60,
                      'broken_mode': False},
         'sweep_1': {'aperture_length_m': 100,
                     'squint_offset_m': 60,
                     'broken_mode': False},
         'sweep_2': {'aperture_length_m': 400,
                     'squint_offset_m': 80,
                     'broken_mode': False},
         'broken': {'aperture_length_m': 400,
                    'squint_offset_m': 60,
                    'broken_mode': True},
         'recovery': {'aperture_length_m': 400,
                      'squint_offset_m': 60,
                      'broken_mode': False}},
 'P79': {'baseline': {'bandwidth_mhz': 200,
                      'aperture_length_m': 30,
                      'broken_mode': False},
         'sweep_1': {'bandwidth_mhz': 400,
                     'aperture_length_m': 30,
                     'broken_mode': False},
         'sweep_2': {'bandwidth_mhz': 200,
                     'aperture_length_m': 10,
                     'broken_mode': False},
         'broken': {'bandwidth_mhz': 200,
                    'aperture_length_m': 30,
                    'broken_mode': True},
         'recovery': {'bandwidth_mhz': 200,
                      'aperture_length_m': 30,
                      'broken_mode': False}},
 'P80': {'baseline': {'error_rms_wavelengths': 0.125,
                      'random_fraction': 0.25,
                      'broken_mode': False},
         'sweep_1': {'error_rms_wavelengths': 0.25,
                     'random_fraction': 0.25,
                     'broken_mode': False},
         'sweep_2': {'error_rms_wavelengths': 0.125,
                     'random_fraction': 0.75,
                     'broken_mode': False},
         'broken': {'error_rms_wavelengths': 0.125,
                    'random_fraction': 0.25,
                    'broken_mode': True},
         'recovery': {'error_rms_wavelengths': 0.125,
                      'random_fraction': 0.25,
                      'broken_mode': False}},
 'P81': {'baseline': {'angular_aperture_deg': 6,
                      'rotation_rate_deg_s': 6,
                      'broken_mode': False},
         'sweep_1': {'angular_aperture_deg': 2,
                     'rotation_rate_deg_s': 6,
                     'broken_mode': False},
         'sweep_2': {'angular_aperture_deg': 6,
                     'rotation_rate_deg_s': 12,
                     'broken_mode': False},
         'broken': {'angular_aperture_deg': 6,
                    'rotation_rate_deg_s': 6,
                    'broken_mode': True},
         'recovery': {'angular_aperture_deg': 6,
                      'rotation_rate_deg_s': 6,
                      'broken_mode': False}},
 'P82': {'baseline': {'target_delay_samples': 24,
                      'reference_quality_db': 35,
                      'broken_mode': False},
         'sweep_1': {'target_delay_samples': 48,
                     'reference_quality_db': 35,
                     'broken_mode': False},
         'sweep_2': {'target_delay_samples': 24,
                     'reference_quality_db': 5,
                     'broken_mode': False},
         'broken': {'target_delay_samples': 24,
                    'reference_quality_db': 35,
                    'broken_mode': True},
         'recovery': {'target_delay_samples': 24,
                      'reference_quality_db': 35,
                      'broken_mode': False}},
 'P83': {'baseline': {'training_cells': 36,
                      'contaminated_fraction': 0,
                      'broken_mode': False},
         'sweep_1': {'training_cells': 8,
                     'contaminated_fraction': 0,
                     'broken_mode': False},
         'sweep_2': {'training_cells': 36,
                     'contaminated_fraction': 0.5,
                     'broken_mode': False},
         'broken': {'training_cells': 36,
                    'contaminated_fraction': 0,
                    'broken_mode': True},
         'recovery': {'training_cells': 36,
                      'contaminated_fraction': 0,
                      'broken_mode': False}},
 'P84': {'baseline': {'design_pfa': 0.001,
                      'replica_taper': 0,
                      'broken_mode': False},
         'sweep_1': {'design_pfa': 0.01,
                     'replica_taper': 0,
                     'broken_mode': False},
         'sweep_2': {'design_pfa': 0.001,
                     'replica_taper': 1,
                     'broken_mode': False},
         'broken': {'design_pfa': 0.001,
                    'replica_taper': 0,
                    'broken_mode': True},
         'recovery': {'design_pfa': 0.001,
                      'replica_taper': 0,
                      'broken_mode': False}}})
