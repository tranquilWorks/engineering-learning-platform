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
