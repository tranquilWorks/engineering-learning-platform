from __future__ import annotations

from typing import Any

import numpy as np

SEED = 1019
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


def _metrics(
    values: np.ndarray, reference_phase: np.ndarray
) -> tuple[float, float, float, float]:
    centered_i = values.real - np.mean(values.real)
    centered_q = values.imag - np.mean(values.imag)
    desired = abs(np.mean(values * np.exp(-1j * reference_phase)))
    image = abs(np.mean(values * np.exp(1j * reference_phase)))
    irr = float(20.0 * np.log10(max(desired, 1e-12) / max(image, 1e-12)))
    dc = float(20.0 * np.log10(max(abs(np.mean(values)), 1e-12) / max(desired, 1e-12)))
    correlation = float(
        np.mean(centered_i * centered_q)
        / np.sqrt(np.mean(centered_i**2) * np.mean(centered_q**2))
    )
    covariance = np.cov(np.vstack((centered_i, centered_q)))
    eigenvalues = np.linalg.eigvalsh(covariance)
    axis_ratio = float(np.sqrt(max(eigenvalues) / max(min(eigenvalues), 1e-15)))
    return dc, irr, correlation, axis_ratio


def _case(i_gain: float, error_deg: float, broken: bool) -> dict[str, Any]:
    if i_gain not in {1.0, 1.1, 1.15, 1.3}:
        raise ValueError("i_gain must be 1, 1.1, 1.15, or 1.3")
    if error_deg not in {0.0, 5.0, 8.0, 15.0}:
        raise ValueError("quadrature_error_deg must be 0, 5, 8, or 15")
    time = np.arange(COUNT) / FS_HZ
    phase = 2.0 * np.pi * 160.0 * time + 0.35
    rng = np.random.default_rng(SEED)
    clean = np.exp(1j * phase) + 0.002 / np.sqrt(2.0) * (
        rng.standard_normal(COUNT) + 1j * rng.standard_normal(COUNT)
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
    estimated_i_gain = np.sqrt(2.0 * np.mean(mean_corrected.real**2))
    estimated_q_gain = np.sqrt(2.0 * np.mean(mean_corrected.imag**2))
    gain_corrected_i = mean_corrected.real / estimated_i_gain
    gain_corrected_q = mean_corrected.imag / estimated_q_gain
    gain_corrected = gain_corrected_i + 1j * gain_corrected_q
    correlation = np.clip(2.0 * np.mean(gain_corrected_i * gain_corrected_q), -1.0, 1.0)
    estimated_error = float(np.arcsin(correlation))
    if broken:
        corrected = gain_corrected * np.exp(-1j * estimated_error)
    else:
        corrected_q = (
            gain_corrected_q - gain_corrected_i * np.sin(estimated_error)
        ) / np.cos(estimated_error)
        corrected = gain_corrected_i + 1j * corrected_q
    stages = [impaired, mean_corrected, gain_corrected, corrected]
    stage_metrics = [_metrics(value, phase) for value in stages]
    isolated = [clean, dc_only, gain_only, phase_only, impaired]
    isolated_metrics = [_metrics(value, phase) for value in isolated]
    frequency = np.fft.fftshift(np.fft.fftfreq(COUNT, 1.0 / FS_HZ))
    spectrum = np.abs(np.fft.fftshift(np.fft.fft(impaired))) / COUNT
    corrected_spectrum = np.abs(np.fft.fftshift(np.fft.fft(corrected))) / COUNT
    isolated_spectra = [
        np.abs(np.fft.fftshift(np.fft.fft(value))) / COUNT for value in isolated
    ]
    return {
        "time": time,
        "phase": phase,
        "clean": clean,
        "impaired": impaired,
        "corrected": corrected,
        "frequency": frequency,
        "spectrum": spectrum,
        "corrected_spectrum": corrected_spectrum,
        "stage_metrics": stage_metrics,
        "isolated_metrics": isolated_metrics,
        "isolated_spectra": isolated_spectra,
        "estimated_error_deg": float(np.rad2deg(estimated_error)),
        "estimated_i_gain": float(estimated_i_gain),
        "estimated_q_gain": float(estimated_q_gain),
        "corrected_rmse": float(np.sqrt(np.mean(np.abs(corrected - clean) ** 2))),
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    i_gain = float(parameters["i_gain"])
    error = float(parameters["quadrature_error_deg"])
    broken = bool(parameters["broken_mode"])
    case = _case(i_gain, error, broken)
    gain_sweep = np.array([1.0, 1.1, 1.3])
    gain_irr = [
        _case(float(value), 0.0, False)["stage_metrics"][0][1] for value in gain_sweep
    ]
    gain_axis = [
        _case(float(value), 0.0, False)["stage_metrics"][0][3] for value in gain_sweep
    ]
    phase_sweep = np.array([0.0, 5.0, 15.0])
    phase_correlation = [
        _case(1.15, float(value), False)["stage_metrics"][0][2] for value in phase_sweep
    ]
    broken_case = _case(1.15, 8.0, True)
    recovered_case = _case(1.15, 8.0, False)
    raw = case["stage_metrics"][0]
    final = case["stage_metrics"][-1]
    display = np.arange(0, COUNT, 8)
    trajectory = np.arange(0, 80)
    signature = [
        i_gain,
        error,
        raw[0],
        raw[1],
        raw[2],
        raw[3],
        final[1],
        final[2],
        final[3],
        case["estimated_i_gain"],
        case["estimated_q_gain"],
        case["estimated_error_deg"],
        broken_case["stage_metrics"][-1][1],
        recovered_case["stage_metrics"][-1][1],
        case["isolated_metrics"][1][0],
        case["isolated_metrics"][2][1],
        case["isolated_metrics"][3][1],
    ]
    return {
        "metrics": [
            {"id": "dc_spike", "label": "Raw DC level", "value": raw[0], "unit": "dBc"},
            {
                "id": "raw_irr",
                "label": "Raw image rejection",
                "value": raw[1],
                "unit": "dB",
            },
            {
                "id": "corrected_irr",
                "label": "Corrected image rejection",
                "value": final[1],
                "unit": "dB",
                "emphasis": "primary",
            },
            {
                "id": "axis_ratio",
                "label": "Corrected axis ratio",
                "value": final[3],
                "unit": "ratio",
            },
            {
                "id": "dc_only_level",
                "label": "DC-only level",
                "value": case["isolated_metrics"][1][0],
                "unit": "dBc",
            },
            {
                "id": "gain_only_irr",
                "label": "Gain-only image rejection",
                "value": case["isolated_metrics"][2][1],
                "unit": "dB",
            },
            {
                "id": "phase_only_irr",
                "label": "Phase-only image rejection",
                "value": case["isolated_metrics"][3][1],
                "unit": "dB",
            },
        ],
        "plots": {
            "impairment_spectrum": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "raw",
                        "x": case["frequency"][display],
                        "y": case["spectrum"][display],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "corrected",
                        "x": case["frequency"][display],
                        "y": case["corrected_spectrum"][display],
                    },
                ],
                "layout": _layout(
                    "DC spike, desired tone, and image",
                    "Signed frequency (Hz)",
                    "Magnitude (V)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "trajectory": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "impaired",
                        "x": case["impaired"].real[trajectory],
                        "y": case["impaired"].imag[trajectory],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "corrected",
                        "x": case["corrected"].real[trajectory],
                        "y": case["corrected"].imag[trajectory],
                    },
                ],
                "layout": _layout("I/Q trajectory geometry", "I (V)", "Q (V)"),
                "config": {"responsive": True, "displaylogo": False},
            },
            "isolated_impairments": {
                "data": [
                    {
                        "type": "bar",
                        "name": "DC level",
                        "x": [
                            "clean",
                            "DC only",
                            "gain only",
                            "phase only",
                            "combined",
                        ],
                        "y": [value[0] for value in case["isolated_metrics"]],
                    },
                    {
                        "type": "bar",
                        "name": "image rejection",
                        "x": [
                            "clean",
                            "DC only",
                            "gain only",
                            "phase only",
                            "combined",
                        ],
                        "y": [value[1] for value in case["isolated_metrics"]],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "I/Q correlation",
                        "x": [
                            "clean",
                            "DC only",
                            "gain only",
                            "phase only",
                            "combined",
                        ],
                        "y": [value[2] for value in case["isolated_metrics"]],
                        "yaxis": "y2",
                    },
                ],
                "layout": _layout(
                    "Separate and combined impairment signatures",
                    "Impairment case",
                    "Level / image rejection (dB)",
                )
                | {
                    "yaxis2": {
                        "title": "I/Q correlation (ratio)",
                        "overlaying": "y",
                        "side": "right",
                    }
                },
                "config": {"responsive": True, "displaylogo": False},
            },
            "parameter_sweeps": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "gain-sweep axis ratio",
                        "x": gain_sweep,
                        "y": gain_axis,
                    },
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "gain-sweep IRR",
                        "x": gain_sweep,
                        "y": gain_irr,
                        "yaxis": "y2",
                    },
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "phase-sweep correlation",
                        "x": phase_sweep,
                        "y": phase_correlation,
                    },
                ],
                "layout": _layout(
                    "Gain and quadrature-error sweeps",
                    "Control value",
                    "Geometry response",
                )
                | {
                    "yaxis2": {
                        "title": "Image rejection (dB)",
                        "overlaying": "y",
                        "side": "right",
                    }
                },
                "config": {"responsive": True, "displaylogo": False},
            },
            "correction_stages": {
                "data": [
                    {
                        "type": "bar",
                        "name": "image rejection",
                        "x": ["raw", "mean", "gain", "phase/shear"],
                        "y": [value[1] for value in case["stage_metrics"]],
                    },
                    {
                        "type": "bar",
                        "name": "broken global rotation",
                        "x": ["rotation", "shear recovery"],
                        "y": [
                            broken_case["stage_metrics"][-1][1],
                            recovered_case["stage_metrics"][-1][1],
                        ],
                    },
                ],
                "layout": _layout(
                    "Ordered correction and broken rotation",
                    "Correction stage",
                    "Image rejection (dB)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "DC shifts the center, branch-gain mismatch stretches the ellipse, and quadrature error shears its axes; each creates a distinct spectrum and geometry signature.",
            "broken": "A global complex rotation changes phase but preserves desired/image magnitudes, so it cannot undo quadrature shear or improve image rejection.",
            "recovery": "Correct mean first, normalize branch gains second, then apply the inverse shear using the estimated I/Q correlation.",
        },
        "diagnostics": {
            "seed": SEED,
            "signature": signature,
            "broken_active": broken,
            "stage_order": ["mean", "gain", "shear"],
            "isolated_case_metrics": {
                name: list(values)
                for name, values in zip(
                    ["clean", "dc_only", "gain_only", "phase_only", "combined"],
                    case["isolated_metrics"],
                    strict=True,
                )
            },
        },
    }
