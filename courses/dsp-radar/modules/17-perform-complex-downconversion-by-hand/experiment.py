from __future__ import annotations

from typing import Any

import numpy as np

SEED = 1017
FS_HZ = 2048.0
COUNT = 4096


def _layout(title: str, x_label: str, y_label: str) -> dict[str, Any]:
    return {
        "title": {"text": title, "x": 0.02},
        "xaxis": {"title": x_label},
        "yaxis": {"title": y_label},
        "legend": {"orientation": "h", "y": 1.14},
        "margin": {"l": 68, "r": 22, "t": 58, "b": 58},
    }


def _fir() -> np.ndarray:
    centered = np.arange(129) - 64
    ideal = 2.0 * 80.0 / FS_HZ * np.sinc(2.0 * 80.0 * centered / FS_HZ)
    window = 0.54 - 0.46 * np.cos(2.0 * np.pi * np.arange(129) / 128.0)
    taps = ideal * window
    return taps / np.sum(taps)


def _signed_frequency(values: np.ndarray) -> float:
    adjacent = np.conj(values[:-1]) * values[1:]
    return float(np.angle(np.sum(adjacent)) * FS_HZ / (2.0 * np.pi))


def _case(lo_frequency: float, lo_phase: float, broken: bool) -> dict[str, Any]:
    if lo_frequency not in {204.0, 216.0, 240.0, 276.0}:
        raise ValueError("lo_frequency_hz must be 204, 216, 240, or 276")
    if not np.isfinite(lo_phase) or lo_phase not in {
        0.0,
        float(np.pi / 2.0),
        float(np.pi),
    }:
        raise ValueError("lo_phase_rad must be 0, pi/2, or pi")
    time = np.arange(COUNT) / FS_HZ
    rng = np.random.default_rng(SEED)
    passband = np.cos(2.0 * np.pi * 240.0 * time + 0.35) + 0.002 * rng.standard_normal(
        COUNT
    )
    sign = 1.0 if broken else -1.0
    oscillator = np.exp(1j * (sign * 2.0 * np.pi * lo_frequency * time - lo_phase))
    mixed = passband * oscillator
    taps = _fir()
    filtered = np.convolve(mixed, taps, mode="same")
    baseband = 2.0 * filtered
    evaluation = slice(192, -192)
    estimated_frequency = _signed_frequency(baseband[evaluation])
    expected_frequency = 240.0 - lo_frequency
    reference = np.exp(
        1j * (2.0 * np.pi * expected_frequency * time[evaluation] + 0.35 - lo_phase)
    )
    projection = np.mean(baseband[evaluation] * np.conj(reference))
    amplitude = float(np.abs(projection))
    phase = float(np.angle(projection))
    image_frequency = -(240.0 + lo_frequency)
    image_reference = np.exp(1j * 2.0 * np.pi * image_frequency * time[evaluation])
    before_image = abs(np.mean(mixed[evaluation] * np.conj(image_reference)))
    after_image = abs(np.mean(filtered[evaluation] * np.conj(image_reference)))
    suppression = float(
        20.0 * np.log10(max(before_image, 1e-15) / max(after_image, 1e-15))
    )
    spectrum = np.abs(np.fft.fftshift(np.fft.fft(mixed))) / COUNT
    filtered_spectrum = np.abs(np.fft.fftshift(np.fft.fft(baseband))) / COUNT
    frequency = np.fft.fftshift(np.fft.fftfreq(COUNT, 1.0 / FS_HZ))
    return {
        "time": time,
        "passband": passband,
        "mixed": mixed,
        "baseband": baseband,
        "frequency": frequency,
        "spectrum": spectrum,
        "filtered_spectrum": filtered_spectrum,
        "expected_frequency": expected_frequency,
        "estimated_frequency": estimated_frequency,
        "amplitude": amplitude,
        "phase": phase,
        "suppression": suppression,
        "image_frequency": image_frequency,
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    lo_frequency = float(parameters["lo_frequency_hz"])
    lo_phase = float(parameters["lo_phase_rad"])
    broken = bool(parameters["broken_mode"])
    case = _case(lo_frequency, lo_phase, broken)
    frequency_sweep = np.array([204.0, 240.0, 276.0])
    sweep_estimated = [
        _case(float(value), 0.0, False)["estimated_frequency"]
        for value in frequency_sweep
    ]
    phase_sweep = np.array([0.0, np.pi / 2.0, np.pi])
    sweep_phase = [_case(240.0, float(value), False)["phase"] for value in phase_sweep]
    broken_case = _case(216.0, 0.0, True)
    recovery_case = _case(216.0, 0.0, False)
    display = np.arange(0, COUNT, 8)
    signature = [
        lo_frequency,
        lo_phase,
        case["expected_frequency"],
        case["estimated_frequency"],
        case["amplitude"],
        case["phase"],
        case["suppression"],
        broken_case["estimated_frequency"],
        recovery_case["estimated_frequency"],
    ]
    return {
        "metrics": [
            {
                "id": "baseband_frequency",
                "label": "Estimated baseband frequency",
                "value": case["estimated_frequency"],
                "unit": "Hz",
                "emphasis": "primary",
            },
            {
                "id": "calibrated_amplitude",
                "label": "2x-calibrated amplitude",
                "value": case["amplitude"],
                "unit": "V",
            },
            {
                "id": "image_suppression",
                "label": "Sum-image suppression",
                "value": case["suppression"],
                "unit": "dB",
            },
            {
                "id": "fir_group_delay",
                "label": "FIR group delay",
                "value": 64,
                "unit": "samples",
            },
        ],
        "plots": {
            "mixer_spectrum": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "after complex mixer",
                        "x": case["frequency"][display],
                        "y": case["spectrum"][display],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "after LPF and 2x",
                        "x": case["frequency"][display],
                        "y": case["filtered_spectrum"][display],
                    },
                ],
                "layout": _layout(
                    "Difference term and sum-frequency image",
                    "Signed frequency (Hz)",
                    "Magnitude (V)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "filtered_baseband": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "I",
                        "x": case["time"][:160],
                        "y": case["baseband"].real[:160],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "Q",
                        "x": case["time"][:160],
                        "y": case["baseband"].imag[:160],
                    },
                ],
                "layout": _layout(
                    "Explicit 129-tap low-pass output",
                    "Time (s)",
                    "Baseband voltage (V)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "lo_frequency_sweep": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "expected difference",
                        "x": frequency_sweep,
                        "y": 240.0 - frequency_sweep,
                    },
                    {
                        "type": "scatter",
                        "mode": "markers",
                        "name": "measured signed beat",
                        "x": frequency_sweep,
                        "y": sweep_estimated,
                    },
                ],
                "layout": _layout(
                    "LO-frequency translation",
                    "LO frequency (Hz)",
                    "Baseband frequency (Hz)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "phase_and_broken": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "recovered phase",
                        "x": phase_sweep,
                        "y": sweep_phase,
                    },
                    {
                        "type": "bar",
                        "name": "wrong/correct sign",
                        "x": ["wrong oscillator sign", "negative-exponent recovery"],
                        "y": [
                            broken_case["estimated_frequency"],
                            recovery_case["estimated_frequency"],
                        ],
                        "yaxis": "y2",
                    },
                ],
                "layout": _layout(
                    "LO phase and sign convention",
                    "LO phase (rad) / case",
                    "Recovered phase (rad)",
                )
                | {
                    "yaxis2": {
                        "title": "Signed frequency (Hz)",
                        "overlaying": "y",
                        "side": "right",
                    }
                },
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "A negative-exponent complex LO moves the +240 Hz RF copy to the signed difference frequency while the mirrored copy becomes a distant negative sum-frequency image.",
            "broken": "Reversing the oscillator sign selects the opposite spectral copy, so the retained low-frequency beat has the wrong sign.",
            "recovery": "Restore exp(-j2pi f_LO t), remove the 64-sample FIR delay from evaluation, and apply the visible factor of two for a real RF input.",
        },
        "diagnostics": {
            "seed": SEED,
            "signature": signature,
            "broken_active": broken,
            "image_frequency_hz": case["image_frequency"],
            "fir_taps": 129,
            "calibration": 2.0,
        },
    }
