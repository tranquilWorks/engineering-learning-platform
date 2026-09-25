from __future__ import annotations

from typing import Any

import numpy as np

SEED = 404
MAX_SAMPLES = 5000


def _layout(title: str, x_label: str, y_label: str) -> dict[str, Any]:
    return {
        "title": {"text": title, "x": 0.02},
        "xaxis": {"title": x_label},
        "yaxis": {"title": y_label},
        "legend": {"orientation": "h", "y": 1.14},
        "margin": {"l": 68, "r": 22, "t": 58, "b": 58},
    }


def _quantize(
    signal: np.ndarray, bits: int, full_scale_v: float
) -> tuple[np.ndarray, np.ndarray, float]:
    levels = 2**bits
    step = 2.0 * full_scale_v / levels
    clipped = np.clip(signal, -full_scale_v, np.nextafter(full_scale_v, -np.inf))
    codes = np.clip(
        np.floor((clipped + full_scale_v) / step).astype(int), 0, levels - 1
    )
    quantized = -full_scale_v + (codes.astype(float) + 0.5) * step
    return quantized, codes, step


def _case(bits: int, amplitude_v: float, dither: bool, broken: bool) -> dict[str, Any]:
    if bits < 2 or bits > 14 or not 0.05 <= amplitude_v <= 1.5:
        raise ValueError("bit depth or amplitude is outside the bounded range")
    fs = 4096.0
    count = int(fs * 0.25)
    if count > MAX_SAMPLES:
        raise ValueError("sample record exceeds the resource ceiling")
    time = np.arange(count, dtype=float) / fs
    signal = amplitude_v * np.sin(2.0 * np.pi * 128.0 * time)
    _, _, step = _quantize(signal, bits, 1.0)
    rng = np.random.default_rng(SEED)
    applied = (
        signal + (rng.random(count) - rng.random(count)) * step if dither else signal
    )
    if broken:
        applied = 1.35 * np.sin(2.0 * np.pi * 128.0 * time)
    quantized, codes, step = _quantize(applied, bits, 1.0)
    error = quantized - applied
    unclipped = np.abs(applied) < 1.0
    bounded_error = (
        float(np.max(np.abs(error[unclipped]))) if np.any(unclipped) else 0.0
    )
    noise_power = float(np.mean(error**2))
    signal_power = float(np.mean(applied**2))
    sqnr = 10.0 * np.log10(signal_power / max(noise_power, 1e-30))
    return {
        "time": time,
        "signal": applied,
        "quantized": quantized,
        "error": error,
        "codes": codes,
        "step": step,
        "max_unclipped_error": bounded_error,
        "sqnr_db": float(sqnr),
        "clipped": int(np.count_nonzero(np.abs(applied) >= 1.0)),
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    bits = int(parameters["bit_depth"])
    amplitude = float(parameters["amplitude_v"])
    dither = bool(parameters["dither_enabled"])
    broken = bool(parameters["broken_mode"])
    case = _case(bits, amplitude, dither, broken)
    bit_sweep = np.array([4, 6, 8])
    bit_sqnr = [_case(int(value), 0.9, False, False)["sqnr_db"] for value in bit_sweep]
    utilization = np.array([0.2, 0.5, 0.9])
    utilization_sqnr = [
        _case(6, float(value), False, False)["sqnr_db"] for value in utilization
    ]
    view = slice(0, 96)
    return {
        "metrics": [
            {"id": "lsb", "label": "LSB", "value": case["step"], "unit": "V"},
            {
                "id": "half_lsb",
                "label": "Half-LSB bound",
                "value": case["step"] / 2.0,
                "unit": "V",
            },
            {
                "id": "measured_sqnr",
                "label": "Measured SQNR",
                "value": case["sqnr_db"],
                "unit": "dB",
                "emphasis": "primary",
            },
            {
                "id": "ideal_sqnr",
                "label": "Ideal full-scale SQNR",
                "value": 6.02 * bits + 1.76,
                "unit": "dB",
            },
            {
                "id": "clipped_samples",
                "label": "Overload samples",
                "value": case["clipped"],
                "unit": "samples",
            },
        ],
        "plots": {
            "quantized_waveform": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "input",
                        "x": case["time"][view],
                        "y": case["signal"][view],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "mid-rise output",
                        "x": case["time"][view],
                        "y": case["quantized"][view],
                    },
                ],
                "layout": _layout(
                    "Bipolar mid-rise quantizer", "Time (s)", "Voltage (V)"
                ),
            },
            "error": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "quantization error",
                        "x": case["time"],
                        "y": case["error"],
                    }
                ],
                "layout": _layout(
                    "Quantization error and overload", "Time (s)", "Error (V)"
                ),
            },
            "parameter_sweeps": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "bit-depth sweep",
                        "x": bit_sweep,
                        "y": bit_sqnr,
                    },
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "range-utilization sweep",
                        "x": utilization,
                        "y": utilization_sqnr,
                    },
                ],
                "layout": _layout(
                    "Two quantizer sweeps",
                    "Bits or fraction of full scale",
                    "Measured SQNR (dB)",
                ),
            },
        },
        "explanations": {
            "observation": "For samples inside ±1 V, a saturated bipolar mid-rise quantizer keeps the error within half an LSB. More bits reduce the step; better range utilization improves SQNR.",
            "broken": "Broken mode drives the converter beyond full scale. Saturation creates overload error larger than half an LSB; that is clipping, not ordinary quantization noise.",
            "recovery": "Return the peak to 0.9 V. Optional seeded triangular dither decorrelates the error but adds noise. Audio playback from the MATLAB lesson is deliberately omitted.",
        },
        "diagnostics": {
            "seed": SEED,
            "sample_count": len(case["signal"]),
            "broken_active": broken,
            "max_unclipped_error_v": case["max_unclipped_error"],
            "half_lsb_v": case["step"] / 2.0,
            "code_min": int(np.min(case["codes"])),
            "code_max": int(np.max(case["codes"])),
            "signature": [
                bits,
                amplitude,
                float(dither),
                case["step"],
                case["sqnr_db"],
                case["max_unclipped_error"],
                case["clipped"],
            ],
        },
    }
