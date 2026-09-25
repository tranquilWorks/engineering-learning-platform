from __future__ import annotations

from typing import Any

import numpy as np

SEED = 1011
FS_HZ = 1024.0


def _layout(title: str, x_label: str, y_label: str) -> dict[str, Any]:
    return {
        "title": {"text": title, "x": 0.02},
        "xaxis": {"title": x_label},
        "yaxis": {"title": y_label},
        "legend": {"orientation": "h", "y": 1.14},
        "margin": {"l": 68, "r": 22, "t": 58, "b": 58},
    }


def _case(
    record_sample_count: int, tone_bin_offset: float, broken: bool
) -> dict[str, Any]:
    if record_sample_count not in {32, 64, 128}:
        raise ValueError("record_sample_count must be 32, 64, or 128")
    if not np.isfinite(tone_bin_offset) or not 0.0 <= tone_bin_offset <= 0.5:
        raise ValueError("tone_bin_offset must lie in [0, 0.5]")
    sample = np.arange(record_sample_count)
    spacing = FS_HZ / record_sample_count
    tone_frequency = 144.0 + tone_bin_offset * spacing
    rng = np.random.default_rng(SEED)
    noise = (
        0.002
        / np.sqrt(2.0)
        * (
            rng.standard_normal(record_sample_count)
            + 1j * rng.standard_normal(record_sample_count)
        )
    )
    observed = (
        np.exp(1j * (2.0 * np.pi * tone_frequency * sample / FS_HZ + 0.35)) + noise
    )
    basis = np.exp(
        -1j
        * 2.0
        * np.pi
        * np.outer(np.arange(record_sample_count), sample)
        / record_sample_count
    )
    explicit = basis @ observed
    accelerated = np.fft.fft(observed)
    magnitude = np.abs(accelerated) / record_sample_count
    phase = np.angle(accelerated)
    phase[magnitude < 0.05] = 0.0
    peak_bin = int(np.argmax(magnitude))
    signed_bin = (
        peak_bin
        if peak_bin <= record_sample_count // 2
        else peak_bin - record_sample_count
    )
    correct_frequency = signed_bin * spacing
    reported_frequency = correct_frequency + spacing if broken else correct_frequency
    lower = int(np.floor(tone_frequency / spacing)) % record_sample_count
    upper = (lower + 1) % record_sample_count
    return {
        "sample": sample,
        "observed": observed,
        "magnitude": magnitude,
        "phase": phase,
        "spacing": spacing,
        "tone_frequency": tone_frequency,
        "peak_bin": peak_bin,
        "correct_frequency": correct_frequency,
        "reported_frequency": reported_frequency,
        "dft_error": float(np.max(np.abs(explicit - accelerated))),
        "neighbor_magnitudes": [float(magnitude[lower]), float(magnitude[upper])],
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    count = int(parameters["record_sample_count"])
    offset = float(parameters["tone_bin_offset"])
    broken = bool(parameters["broken_mode"])
    case = _case(count, offset, broken)
    offset_sweep = np.array([0.0, 0.25, 0.5])
    neighbor_balance = []
    for value in offset_sweep:
        pair = _case(64, float(value), False)["neighbor_magnitudes"]
        neighbor_balance.append(min(pair) / max(max(pair), 1e-15))
    length_sweep = np.array([32, 64, 128])
    spacing_sweep = FS_HZ / length_sweep
    bins = np.arange(count)
    signed_frequency = (
        np.where(bins <= count // 2, bins, bins - count) * case["spacing"]
    )
    signature = [
        float(count),
        offset,
        case["spacing"],
        case["tone_frequency"],
        float(case["peak_bin"]),
        case["correct_frequency"],
        case["reported_frequency"],
        case["dft_error"],
        *case["neighbor_magnitudes"],
    ]
    return {
        "metrics": [
            {
                "id": "bin_spacing",
                "label": "Bin spacing",
                "value": case["spacing"],
                "unit": "Hz",
                "emphasis": "primary",
            },
            {
                "id": "peak_bin",
                "label": "Zero-based peak bin",
                "value": case["peak_bin"],
                "unit": "bin",
            },
            {
                "id": "reported_frequency",
                "label": "Reported frequency",
                "value": case["reported_frequency"],
                "unit": "Hz",
            },
            {
                "id": "dft_error",
                "label": "Explicit DFT/FFT error",
                "value": case["dft_error"],
                "unit": "V",
            },
        ],
        "plots": {
            "bin_map": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "magnitude",
                        "x": signed_frequency,
                        "y": case["magnitude"],
                    },
                    {
                        "type": "scatter",
                        "mode": "markers",
                        "name": "reported peak",
                        "x": [case["reported_frequency"]],
                        "y": [max(case["magnitude"])],
                    },
                ],
                "layout": _layout(
                    "Signed FFT-bin map",
                    "Signed frequency (Hz)",
                    "Normalized magnitude (V)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "neighboring_bins": {
                "data": [
                    {
                        "type": "bar",
                        "name": "neighbor magnitude",
                        "x": ["lower", "upper"],
                        "y": case["neighbor_magnitudes"],
                    },
                ],
                "layout": _layout(
                    "Off-bin projections", "Nearest projection", "Magnitude (V)"
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "parameter_sweeps": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "neighbor balance",
                        "x": offset_sweep,
                        "y": neighbor_balance,
                    },
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "bin spacing",
                        "x": length_sweep,
                        "y": spacing_sweep,
                        "yaxis": "y2",
                    },
                ],
                "layout": _layout(
                    "Fractional offset and record-length sweeps",
                    "Control value",
                    "Response",
                )
                | {
                    "yaxis2": {
                        "title": "Bin spacing (Hz)",
                        "overlaying": "y",
                        "side": "right",
                    }
                },
                "config": {"responsive": True, "displaylogo": False},
            },
            "broken_case": {
                "data": [
                    {
                        "type": "bar",
                        "name": "frequency label",
                        "x": ["correct k", "displayed"],
                        "y": [case["correct_frequency"], case["reported_frequency"]],
                    },
                ],
                "layout": _layout(
                    "One-based index error and recovery",
                    "Axis convention",
                    "Frequency (Hz)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "Each zero-based DFT bin is one finite-record complex-sinusoid projection; changing N changes both duration and the projection spacing.",
            "broken": "Broken mode treats the one-based storage index as zero-based k, shifting every physical-frequency label upward by exactly one bin.",
            "recovery": "Use k=index-1, then f=k fs/N. Phase is interpreted only where the associated projection magnitude clears the retained threshold.",
        },
        "diagnostics": {
            "seed": SEED,
            "signature": signature,
            "signed_frequency_hz": signed_frequency.tolist(),
            "broken_active": broken,
        },
    }
