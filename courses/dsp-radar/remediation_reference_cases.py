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
