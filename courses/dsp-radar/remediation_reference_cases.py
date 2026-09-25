"""Independent numerical references for the P02-P10 fidelity repair.

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
}


def expected_signature(item_id: str, scenario: str) -> list[float]:
    """Return a separately formulated numeric signature for one retained scenario."""

    return [
        float(value) for value in _REFERENCES[item_id](SCENARIOS[item_id][scenario])
    ]
