from __future__ import annotations

from typing import Any

import numpy as np

MAX_SAMPLES = 5000


def _layout(title: str, x_label: str, y_label: str) -> dict[str, Any]:
    return {
        "title": {"text": title, "x": 0.02},
        "xaxis": {"title": x_label},
        "yaxis": {"title": y_label},
        "legend": {"orientation": "h", "y": 1.14},
        "margin": {"l": 68, "r": 22, "t": 58, "b": 58},
    }


def _fold(input_hz: float, sample_rate_hz: float) -> tuple[float, float]:
    signed = input_hz - np.round(input_hz / sample_rate_hz) * sample_rate_hz
    return float(signed), float(abs(signed))


def _estimate(samples: np.ndarray, sample_rate_hz: float) -> float:
    denominator = float(np.dot(samples[1:-1], samples[1:-1]))
    if denominator <= 1e-14:
        return 0.0
    cosine = float(
        np.dot(samples[1:-1], samples[:-2] + samples[2:]) / (2.0 * denominator)
    )
    return float(sample_rate_hz * np.arccos(np.clip(cosine, -1.0, 1.0)) / (2.0 * np.pi))


def _case(input_hz: float, sample_rate_hz: float, wrong_phase: bool) -> dict[str, Any]:
    if not 10.0 <= input_hz <= 3000.0 or not 100.0 <= sample_rate_hz <= 4000.0:
        raise ValueError("frequencies exceed the bounded experiment range")
    count = round(0.2 * sample_rate_hz)
    if count < 8 or count > MAX_SAMPLES:
        raise ValueError("sample record is outside the bounded resource limit")
    phase = np.pi / 5.0
    time = np.arange(count, dtype=float) / sample_rate_hz
    samples = np.cos(2.0 * np.pi * input_hz * time + phase)
    signed, apparent = _fold(input_hz, sample_rate_hz)
    alias_phase = phase if signed >= 0.0 or wrong_phase else -phase
    alias = np.cos(2.0 * np.pi * apparent * time + alias_phase)
    return {
        "time": time,
        "samples": samples,
        "alias": alias,
        "signed": signed,
        "apparent": apparent,
        "phase": alias_phase,
        "agreement": float(np.max(np.abs(samples - alias))),
        "estimate": _estimate(samples, sample_rate_hz),
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    input_hz = float(parameters["input_frequency_hz"])
    sample_rate_hz = float(parameters["sample_rate_hz"])
    broken = bool(parameters["broken_mode"])
    case = _case(input_hz, sample_rate_hz, broken)
    frequency_sweep = np.array([300.0, 700.0, 1300.0])
    frequency_aliases = [_fold(value, 1000.0)[1] for value in frequency_sweep]
    rate_sweep = np.array([800.0, 1000.0, 1600.0])
    rate_aliases = [_fold(700.0, value)[1] for value in rate_sweep]
    dense_time = np.linspace(0.0, 0.02, 800, endpoint=False)
    dense_true = np.cos(2.0 * np.pi * input_hz * dense_time + np.pi / 5.0)
    dense_alias = np.cos(2.0 * np.pi * case["apparent"] * dense_time + case["phase"])
    return {
        "metrics": [
            {
                "id": "signed_alias",
                "label": "Signed folded frequency",
                "value": case["signed"],
                "unit": "Hz",
                "emphasis": "primary",
            },
            {
                "id": "apparent_frequency",
                "label": "Apparent frequency",
                "value": case["apparent"],
                "unit": "Hz",
            },
            {
                "id": "recurrence_estimate",
                "label": "Sample-recurrence estimate",
                "value": case["estimate"],
                "unit": "Hz",
            },
            {
                "id": "sample_agreement",
                "label": "Alias sample error",
                "value": case["agreement"],
                "unit": "a.u.",
            },
        ],
        "plots": {
            "folding": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": f"true {input_hz:g} Hz",
                        "x": dense_time,
                        "y": dense_true,
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": f"folded {case['apparent']:g} Hz",
                        "x": dense_time,
                        "y": dense_alias,
                    },
                    {
                        "type": "scatter",
                        "mode": "markers",
                        "name": "identical samples",
                        "x": case["time"],
                        "y": case["samples"],
                    },
                ],
                "layout": _layout(
                    "Aliasing is signed frequency folding",
                    "Time (s)",
                    "Amplitude (a.u.)",
                ),
            },
            "parameter_sweeps": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "vary input frequency",
                        "x": frequency_sweep,
                        "y": frequency_aliases,
                    },
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "vary sample rate",
                        "x": rate_sweep,
                        "y": rate_aliases,
                    },
                ],
                "layout": _layout(
                    "Two alias-folding sweeps",
                    "Frequency or sample rate (Hz)",
                    "Apparent frequency (Hz)",
                ),
            },
            "phase_check": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "markers",
                        "name": "measured",
                        "x": case["time"],
                        "y": case["samples"],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "alias hypothesis",
                        "x": case["time"],
                        "y": case["alias"],
                    },
                ],
                "layout": _layout(
                    "Reflected aliases require phase reversal",
                    "Time (s)",
                    "Amplitude (a.u.)",
                ),
            },
        },
        "explanations": {
            "observation": "Folding preserves a signed frequency. A negative signed fold becomes a positive-frequency cosine only after reversing phase.",
            "broken": "Broken mode keeps the original phase after reflection, so the supposed alias no longer passes through the measured samples.",
            "recovery": "Apply the signed fold first, reverse phase only for a negative result, and confirm with the independent second-order sample recurrence.",
        },
        "diagnostics": {
            "sample_count": len(case["samples"]),
            "broken_active": broken,
            "signed_alias_hz": case["signed"],
            "alias_phase_rad": case["phase"],
            "sample_agreement_error": case["agreement"],
            "signature": [
                input_hz,
                sample_rate_hz,
                case["signed"],
                case["apparent"],
                case["estimate"],
                case["agreement"],
            ],
        },
    }
