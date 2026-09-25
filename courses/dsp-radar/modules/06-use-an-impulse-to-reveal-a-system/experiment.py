from __future__ import annotations

from typing import Any

import numpy as np

SEED = 606
MAX_SAMPLES = 1024


def _layout(title: str, x_label: str, y_label: str) -> dict[str, Any]:
    return {
        "title": {"text": title, "x": 0.02},
        "xaxis": {"title": x_label},
        "yaxis": {"title": y_label},
        "legend": {"orientation": "h", "y": 1.14},
        "margin": {"l": 68, "r": 22, "t": 58, "b": 58},
    }


def _resonator_direct(
    signal: np.ndarray, radius: float, frequency_hz: float, fs: float, gain: float
) -> np.ndarray:
    coefficient = 2.0 * radius * np.cos(2.0 * np.pi * frequency_hz / fs)
    output = np.zeros_like(signal)
    for index in range(len(signal)):
        previous = output[index - 1] if index >= 1 else 0.0
        previous_two = output[index - 2] if index >= 2 else 0.0
        output[index] = (
            gain * signal[index] + coefficient * previous - radius**2 * previous_two
        )
    return output


def _impulse_response(
    radius: float, frequency_hz: float, fs: float, gain: float, count: int
) -> np.ndarray:
    impulse = np.zeros(count)
    impulse[0] = 1.0
    return _resonator_direct(impulse, radius, frequency_hz, fs, gain)


def _case(echo_delay: int, radius: float, broken: bool) -> dict[str, Any]:
    if echo_delay < 1 or echo_delay > 96 or not 0.1 <= radius <= 0.98:
        raise ValueError("system controls exceed the bounded range")
    count = 256
    if count > MAX_SAMPLES:
        raise ValueError("record exceeds the resource ceiling")
    rng = np.random.default_rng(SEED)
    signal = rng.standard_normal(count)
    delay = 18
    delay_h = np.zeros(delay + 1)
    delay_h[-1] = 1.0
    ma_h = np.ones(9) / 9.0
    echo_h = np.zeros(echo_delay + 1)
    echo_h[0], echo_h[-1] = 1.0, 0.55
    resonator_h = _impulse_response(radius, 90.0, 1000.0, 0.15, count)

    delay_direct = np.pad(signal, (delay, 0))[:count]
    ma_direct = np.array(
        [
            np.mean(signal[max(0, index - 8) : index + 1]) * min(index + 1, 9) / 9.0
            for index in range(count)
        ]
    )
    echo_direct = signal.copy()
    echo_direct[echo_delay:] += 0.55 * signal[:-echo_delay]
    resonator_direct = _resonator_direct(signal, radius, 90.0, 1000.0, 0.15)
    direct = {
        "delay": delay_direct,
        "moving_average": ma_direct,
        "echo": echo_direct,
        "resonator": resonator_direct,
    }
    impulses = {
        "delay": delay_h,
        "moving_average": ma_h,
        "echo": echo_h,
        "resonator": resonator_h,
    }
    convolution = {
        name: np.convolve(signal, impulse)[:count] for name, impulse in impulses.items()
    }
    errors = {
        name: float(np.max(np.abs(direct[name] - convolution[name]))) for name in direct
    }

    linear = convolution["echo"]
    circular = np.fft.ifft(np.fft.fft(signal) * np.fft.fft(echo_h, count)).real
    broken_output = circular if broken else linear
    wrap_error = float(np.max(np.abs(circular - linear)))
    display_error = float(np.max(np.abs(broken_output - linear)))
    return {
        "signal": signal,
        "impulses": impulses,
        "direct": direct,
        "convolution": convolution,
        "errors": errors,
        "linear": linear,
        "displayed": broken_output,
        "wrap_error": wrap_error,
        "display_error": display_error,
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    echo_delay = int(parameters["echo_delay_samples"])
    radius = float(parameters["resonator_radius"])
    broken = bool(parameters["broken_mode"])
    case = _case(echo_delay, radius, broken)
    delay_sweep = np.array([16, 32, 48])
    echo_peak = [
        float(np.argmax(np.abs(_case(int(value), 0.86, False)["impulses"]["echo"])))
        for value in delay_sweep
    ]
    radius_sweep = np.array([0.6, 0.86, 0.96])
    ring_energy = [
        float(np.sum(_case(32, float(value), False)["impulses"]["resonator"] ** 2))
        for value in radius_sweep
    ]
    index = np.arange(256)
    return {
        "metrics": [
            {
                "id": "maximum_equivalence_error",
                "label": "Direct/convolution error",
                "value": max(case["errors"].values()),
                "unit": "a.u.",
            },
            {
                "id": "circular_wrap_error",
                "label": "Circular wrap error",
                "value": case["wrap_error"],
                "unit": "a.u.",
                "emphasis": "primary",
            },
            {
                "id": "echo_delay",
                "label": "Echo delay",
                "value": echo_delay,
                "unit": "samples",
            },
            {
                "id": "resonator_radius",
                "label": "Resonator radius",
                "value": radius,
                "unit": "ratio",
            },
        ],
        "plots": {
            "impulse_responses": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": name,
                        "x": np.arange(len(value)),
                        "y": value,
                    }
                    for name, value in case["impulses"].items()
                ],
                "layout": _layout(
                    "An impulse reveals each system",
                    "Lag (samples)",
                    "Impulse response (a.u.)",
                ),
            },
            "equivalence": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "direct resonator",
                        "x": index,
                        "y": case["direct"]["resonator"],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "convolution",
                        "x": index,
                        "y": case["convolution"]["resonator"],
                    },
                ],
                "layout": _layout(
                    "Direct implementation equals linear convolution",
                    "Sample index",
                    "Output amplitude (a.u.)",
                ),
            },
            "parameter_sweeps": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "echo-delay sweep",
                        "x": delay_sweep,
                        "y": echo_peak,
                    },
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "pole-radius sweep",
                        "x": radius_sweep,
                        "y": ring_energy,
                    },
                ],
                "layout": _layout(
                    "Two system sweeps",
                    "Delay (samples) or radius",
                    "Echo lag or ringing energy",
                ),
            },
            "broken_case": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "linear recovery",
                        "x": index,
                        "y": case["linear"],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "displayed output",
                        "x": index,
                        "y": case["displayed"],
                    },
                ],
                "layout": _layout(
                    "Circular convolution wraps the tail",
                    "Sample index",
                    "Echo output (a.u.)",
                ),
            },
        },
        "explanations": {
            "observation": "Delay, moving average, echo, and resonator outputs match convolution with their measured impulse responses.",
            "broken": "Broken mode uses an unpadded N-point FFT product. The linear tail wraps into the beginning of the record.",
            "recovery": "Use linear convolution or zero-pad the FFT to N+M−1. The recovered output matches the direct system to numerical precision.",
        },
        "diagnostics": {
            "seed": SEED,
            "sample_count": 256,
            "broken_active": broken,
            "direct_convolution_errors": case["errors"],
            "circular_wrap_error": case["wrap_error"],
            "signature": [
                echo_delay,
                radius,
                *case["errors"].values(),
                case["wrap_error"],
                case["display_error"],
            ],
        },
    }
