from __future__ import annotations

from typing import Any

import numpy as np

SEED = 1020
FS_HZ = 1024.0
TRIALS = 40


def _layout(title: str, x_label: str, y_label: str) -> dict[str, Any]:
    return {
        "title": {"text": title, "x": 0.02},
        "xaxis": {"title": x_label},
        "yaxis": {"title": y_label},
        "legend": {"orientation": "h", "y": 1.14},
        "margin": {"l": 68, "r": 22, "t": 58, "b": 58},
    }


def _wrap(value: float | np.ndarray) -> float | np.ndarray:
    return np.arctan2(np.sin(value), np.cos(value))


def _estimate(values: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    count = len(values)
    spectrum = np.fft.fft(values)
    magnitude = np.abs(spectrum) / count
    peak = int(np.argmax(magnitude))
    signed_peak = peak if peak < count // 2 else peak - count
    peak_frequency = signed_peak * FS_HZ / count
    left = np.log(max(float(magnitude[(peak - 1) % count]), 1e-15))
    center = np.log(max(float(magnitude[peak]), 1e-15))
    right = np.log(max(float(magnitude[(peak + 1) % count]), 1e-15))
    denominator = left - 2.0 * center + right
    offset = (
        np.clip(0.5 * (left - right) / denominator, -0.5, 0.5)
        if abs(denominator) > 1e-15
        else 0.0
    )
    interpolated = (signed_peak + offset) * FS_HZ / count
    adjacent = np.conj(values[:-1]) * values[1:]
    coherent = np.sum(adjacent)
    increment = np.angle(coherent) * FS_HZ / (2.0 * np.pi)
    coherence = float(abs(coherent) / max(float(np.sum(np.abs(adjacent))), 1e-15))
    frequencies = np.array([peak_frequency, interpolated, increment])
    time = np.arange(count) / FS_HZ
    phases = np.array(
        [
            np.angle(np.sum(values * np.exp(-1j * 2.0 * np.pi * value * time)))
            for value in frequencies
        ]
    )
    return frequencies, phases, coherence


def _trial(
    snr: float, count: int, seed: int, amplitude: float = 1.0
) -> tuple[np.ndarray, np.ndarray, float, np.ndarray]:
    if snr < -20.0 or snr > 60.0 or count not in {64, 128, 256, 512}:
        raise ValueError("SNR or record length is outside the bounded cases")
    time = np.arange(count) / FS_HZ
    clean = amplitude * np.exp(1j * (2.0 * np.pi * 123.25 * time + 2.70))
    rng = np.random.default_rng(seed)
    noise_rms = 10.0 ** (-snr / 20.0)
    noise = (
        noise_rms
        / np.sqrt(2.0)
        * (rng.standard_normal(count) + 1j * rng.standard_normal(count))
    )
    observed = clean + noise
    frequencies, phases, coherence = _estimate(observed)
    return frequencies, phases, coherence, observed


def _monte_carlo(
    snr: float, count: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    frequency_error = []
    phase_error = []
    coherences = []
    for trial in range(TRIALS):
        frequencies, phases, coherence, _ = _trial(snr, count, SEED + 1000 + trial)
        frequency_error.append(frequencies - 123.25)
        phase_error.append(_wrap(phases - 2.70))
        coherences.append(coherence)
    frequency_error_array = np.array(frequency_error)
    phase_error_array = np.array(phase_error)
    frequency_bias = np.mean(frequency_error_array, axis=0)
    frequency_spread = np.std(frequency_error_array, axis=0, ddof=1)
    phase_circular_error = np.sqrt(np.mean(phase_error_array**2, axis=0))
    return (
        frequency_bias,
        frequency_spread,
        phase_circular_error,
        float(np.mean(coherences)),
    )


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    snr = float(parameters["snr_db"])
    count = int(parameters["record_sample_count"])
    broken = bool(parameters["broken_mode"])
    frequencies, phases, coherence, _ = _trial(snr, count, SEED)
    time = np.arange(count) / FS_HZ
    true_total = 2.0 * np.pi * 123.25 * (count - 1) / FS_HZ
    wrapped_endpoint = float(_wrap(true_total))
    broken_endpoint = wrapped_endpoint * FS_HZ / (2.0 * np.pi * (count - 1))
    clean = np.exp(1j * (2.0 * np.pi * 123.25 * time + 2.70))
    recovered = _estimate(clean)[0][2]
    low_frequencies, _, low_coherence, _ = _trial(
        -20.0, count, SEED + 99, amplitude=0.02
    )
    low_reported = float(low_frequencies[2]) if low_coherence >= 0.20 else 0.0
    snr_sweep = np.array([-10.0, 0.0, 10.0, 20.0])
    snr_results = [_monte_carlo(float(value), 256) for value in snr_sweep]
    length_sweep = np.array([64, 128, 256, 512])
    length_results = [_monte_carlo(8.0, int(value)) for value in length_sweep]
    selected_trials = _monte_carlo(snr, count)
    reported_frequency = broken_endpoint if broken else frequencies[2]
    signature = [
        snr,
        float(count),
        *frequencies.tolist(),
        *phases.tolist(),
        coherence,
        broken_endpoint,
        recovered,
        low_coherence,
        low_reported,
        reported_frequency,
        selected_trials[0][2],
        selected_trials[1][2],
        selected_trials[2][2],
        selected_trials[3],
    ]
    labels = ["peak FFT bin", "interpolated FFT", "phase increment"]
    return {
        "metrics": [
            {
                "id": "reported_frequency",
                "label": "Reported frequency",
                "value": reported_frequency,
                "unit": "Hz",
                "emphasis": "primary",
            },
            {
                "id": "interpolated_error",
                "label": "Interpolated FFT error",
                "value": frequencies[1] - 123.25,
                "unit": "Hz",
            },
            {
                "id": "phase_error",
                "label": "Phase-increment initial-phase error",
                "value": float(_wrap(phases[2] - 2.70)),
                "unit": "rad",
            },
            {
                "id": "coherence",
                "label": "Adjacent-product coherence",
                "value": coherence,
                "unit": "ratio",
            },
            {
                "id": "trial_frequency_bias",
                "label": "40-trial phase-increment bias",
                "value": selected_trials[0][2],
                "unit": "Hz",
            },
            {
                "id": "trial_frequency_spread",
                "label": "40-trial phase-increment spread",
                "value": selected_trials[1][2],
                "unit": "Hz",
            },
            {
                "id": "trial_circular_phase_error",
                "label": "40-trial circular phase error",
                "value": selected_trials[2][2],
                "unit": "rad RMS",
            },
        ],
        "plots": {
            "frequency_estimators": {
                "data": [
                    {
                        "type": "bar",
                        "name": "frequency estimate",
                        "x": labels,
                        "y": frequencies,
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "truth",
                        "x": labels,
                        "y": [123.25] * 3,
                    },
                ],
                "layout": _layout(
                    "Three bounded frequency estimators", "Estimator", "Frequency (Hz)"
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "phase_estimators": {
                "data": [
                    {
                        "type": "bar",
                        "name": "wrapped phase error",
                        "x": labels,
                        "y": _wrap(phases - 2.70),
                    }
                ],
                "layout": _layout(
                    "De-rotated initial-phase estimates",
                    "Estimator",
                    "Circular phase error (rad)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "snr_and_length_sweeps": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "phase-increment spread vs SNR",
                        "x": snr_sweep,
                        "y": [item[1][2] for item in snr_results],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "phase-increment spread vs N",
                        "x": length_sweep,
                        "y": [item[1][2] for item in length_results],
                        "yaxis": "y2",
                    },
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "circular phase error vs SNR",
                        "x": snr_sweep,
                        "y": [item[2][2] for item in snr_results],
                        "yaxis": "y3",
                    },
                ],
                "layout": _layout(
                    "Forty-trial SNR and coherent-length sweeps",
                    "SNR (dB) / samples",
                    "Frequency spread (Hz)",
                )
                | {
                    "yaxis2": {
                        "title": "Frequency spread (Hz)",
                        "overlaying": "y",
                        "side": "right",
                    },
                    "yaxis3": {
                        "title": "Circular phase error (rad RMS)",
                        "anchor": "free",
                        "overlaying": "y",
                        "side": "right",
                        "position": 0.92,
                    },
                },
                "config": {"responsive": True, "displaylogo": False},
            },
            "broken_and_gate": {
                "data": [
                    {
                        "type": "bar",
                        "name": "endpoint/recovery",
                        "x": ["wrapped endpoint", "adjacent recovery", "truth"],
                        "y": [broken_endpoint, recovered, 123.25],
                    },
                    {
                        "type": "bar",
                        "name": "coherence",
                        "x": ["baseline", "low amplitude"],
                        "y": [coherence, low_coherence],
                        "yaxis": "y2",
                    },
                ],
                "layout": _layout(
                    "Endpoint-wrap failure and confidence gate",
                    "Case",
                    "Frequency (Hz)",
                )
                | {
                    "yaxis2": {
                        "title": "Coherence (ratio)",
                        "overlaying": "y",
                        "side": "right",
                        "range": [0, 1],
                    }
                },
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "The peak bin is grid-limited, three-bin log interpolation estimates a sub-bin maximum, and coherent adjacent products estimate mean phase step directly.",
            "broken": "A first-to-last phase angle is wrapped to one turn before division, so a many-turn record produces a catastrophically wrong frequency.",
            "recovery": "Sum adjacent conjugate products coherently, de-rotate for initial phase, use circular phase error, and withhold low-amplitude evidence below the 0.20 coherence gate.",
        },
        "diagnostics": {
            "seed": SEED,
            "signature": signature,
            "broken_active": broken,
            "trial_count": TRIALS,
            "low_amplitude_rejected": low_coherence < 0.20,
            "frequency_bias_hz": [item[0].tolist() for item in snr_results],
            "phase_circular_error_rad": [item[2].tolist() for item in snr_results],
            "length_frequency_bias_hz": [item[0].tolist() for item in length_results],
            "length_frequency_spread_hz": [item[1].tolist() for item in length_results],
            "length_phase_circular_error_rad": [
                item[2].tolist() for item in length_results
            ],
            "length_mean_coherence": [item[3] for item in length_results],
        },
    }
