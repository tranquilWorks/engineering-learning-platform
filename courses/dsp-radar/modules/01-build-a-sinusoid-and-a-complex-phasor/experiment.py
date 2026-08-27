from __future__ import annotations

from typing import Any

import numpy as np

MAX_SAMPLES = 5000
SEED = 84


def _layout(title: str, x_label: str, y_label: str) -> dict[str, Any]:
    return {
        "title": {"text": title, "x": 0.02, "xanchor": "left"},
        "margin": {"l": 68, "r": 22, "t": 58, "b": 58},
        "xaxis": {"title": x_label, "showgrid": True, "zeroline": False},
        "yaxis": {"title": y_label, "showgrid": True, "zeroline": False},
        "legend": {"orientation": "h", "y": 1.14},
        "hovermode": "closest",
        "uirevision": "keep-view",
    }


def _sample_count(sample_rate_hz: float, duration_s: float) -> int:
    requested = sample_rate_hz * duration_s
    count = round(requested)
    if count < 2 or abs(count - requested) > 1e-9:
        raise ValueError("sample_rate_hz * duration_s must be an integer of at least two")
    if count > MAX_SAMPLES:
        raise ValueError(f"record exceeds the {MAX_SAMPLES}-sample resource ceiling")
    return count


def _alias_frequency(true_hz: float, sample_rate_hz: float) -> tuple[float, float]:
    signed = true_hz - round(true_hz / sample_rate_hz) * sample_rate_hz
    return float(signed), float(abs(signed))


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    amplitude = float(parameters["amplitude"])
    requested_frequency = float(parameters["frequency_hz"])
    phase = float(parameters["phase_rad"])
    requested_fs = float(parameters["sample_rate_hz"])
    duration = float(parameters["duration_s"])
    alias_mode = bool(parameters["alias_mode"])

    frequency = 5.0 if alias_mode else requested_frequency
    sample_rate = 8.0 if alias_mode else requested_fs
    count = _sample_count(sample_rate, duration)
    time = np.arange(count, dtype=float) / sample_rate
    theta = 2.0 * np.pi * frequency * time + phase
    phasor = amplitude * np.exp(1j * theta)
    cosine = amplitude * np.cos(theta)
    projection_error = float(np.max(np.abs(cosine - phasor.real)))
    radius_error = float(np.max(np.abs(np.abs(phasor) - amplitude)))

    direction_count = max(2, min(count, int(sample_rate / max(4.0 * abs(frequency), 1.0)) + 1))
    direction_time = np.arange(direction_count, dtype=float) / sample_rate
    positive = amplitude * np.exp(1j * (2.0 * np.pi * abs(frequency) * direction_time + phase))
    negative = amplitude * np.exp(1j * (-2.0 * np.pi * abs(frequency) * direction_time + phase))
    positive_step = float(np.angle(np.conj(positive[0]) * positive[1]))
    negative_step = float(np.angle(np.conj(negative[0]) * negative[1]))

    dense_count = min(MAX_SAMPLES, max(400, round(200.0 * duration)))
    dense_time = np.arange(dense_count, dtype=float) / (dense_count / duration)
    true_dense = amplitude * np.cos(2.0 * np.pi * frequency * dense_time + phase)
    signed_alias, apparent_alias = _alias_frequency(frequency, sample_rate)
    alias_phase = -phase if signed_alias < 0 else phase
    alias_dense = amplitude * np.cos(2.0 * np.pi * apparent_alias * dense_time + alias_phase)
    alias_at_samples = amplitude * np.cos(2.0 * np.pi * apparent_alias * time + alias_phase)
    alias_error = float(np.max(np.abs(cosine - alias_at_samples)))

    amplitude_cases = np.array([0.5, 1.0, 1.5])
    phase_cases = np.array([0.0, np.pi / 4.0, np.pi / 2.0])
    frequency_cases = np.array([2.5, 5.0, 10.0])

    metrics = [
        {"id": "samples", "label": "Samples", "value": count, "unit": "samples"},
        {"id": "cycles", "label": "Cycles in record", "value": abs(frequency) * duration, "unit": "cycles", "emphasis": "primary"},
        {"id": "samples_per_cycle", "label": "Samples/cycle", "value": sample_rate / max(abs(frequency), 1e-12), "unit": "samples/cycle"},
        {"id": "initial_i", "label": "Initial I", "value": float(phasor.real[0]), "unit": "a.u."},
        {"id": "initial_q", "label": "Initial Q", "value": float(phasor.imag[0]), "unit": "a.u."},
        {"id": "phase_step", "label": "Signed phase step", "value": float(np.angle(np.conj(phasor[0]) * phasor[1])), "unit": "rad/sample"},
    ]
    if alias_mode or abs(frequency) >= sample_rate / 2.0:
        metrics.append({"id": "apparent_alias", "label": "Apparent real frequency", "value": apparent_alias, "unit": "Hz", "emphasis": "danger"})

    time_layout = _layout("Real cosine is the I-axis projection", "Time (s)", "Amplitude (a.u.)")
    iq_layout = _layout("Ordered IQ trajectory", "In-phase I (a.u.)", "Quadrature Q (a.u.)")
    iq_layout["yaxis"]["scaleanchor"] = "x"
    iq_layout["shapes"] = [{"type": "circle", "x0": -amplitude, "x1": amplitude, "y0": -amplitude, "y1": amplitude, "line": {"dash": "dot", "color": "#64748b"}}]

    sweep_layout = _layout("One-variable sweeps", "Case index", "Normalized observation")
    alias_layout = _layout("True waveform and its sampled alias", "Time (s)", "Amplitude (a.u.)")

    broken = (
        f"At {sample_rate:.1f} Sa/s, |f|={abs(frequency):.1f} Hz is not below Nyquist. "
        f"The samples also fit an apparent {apparent_alias:.1f} Hz cosine; agreement error is {alias_error:.3g}."
        if abs(frequency) >= sample_rate / 2.0
        else "The current sampling rate is above Nyquist; the forced broken toggle reproduces the exact 5 Hz at 8 Sa/s ambiguity."
    )

    return {
        "metrics": metrics,
        "plots": {
            "time_projection": {
                "data": [
                    {"type": "scattergl", "mode": "lines+markers", "name": "x(t)=A cos(θ)", "x": time, "y": cosine, "marker": {"size": 3}},
                    {"type": "scatter", "mode": "lines", "name": "I=real(z)", "x": time, "y": phasor.real, "line": {"dash": "dash"}},
                    {"type": "scatter", "mode": "lines", "name": "Q=imag(z)", "x": time, "y": phasor.imag, "line": {"dash": "dot"}},
                ],
                "layout": time_layout,
                "config": {"responsive": True, "displaylogo": False},
            },
            "iq_trajectory": {
                "data": [
                    {"type": "scattergl", "mode": "lines+markers", "name": "ordered I+jQ", "x": phasor.real, "y": phasor.imag, "marker": {"size": 4}},
                    {"type": "scatter", "mode": "markers", "name": "start", "x": [phasor.real[0]], "y": [phasor.imag[0]], "marker": {"size": 11}},
                ],
                "layout": iq_layout,
                "config": {"responsive": True, "displaylogo": False},
            },
            "rotation_direction": {
                "data": [
                    {"type": "scatter", "mode": "lines+markers", "name": "+|f|", "x": positive.real, "y": positive.imag},
                    {"type": "scatter", "mode": "lines+markers", "name": "-|f|", "x": negative.real, "y": negative.imag},
                ],
                "layout": {**_layout("Frequency sign reverses ordered rotation", "I (a.u.)", "Q (a.u.)"), "yaxis": {"title": "Q (a.u.)", "scaleanchor": "x", "showgrid": True}},
                "config": {"responsive": True, "displaylogo": False},
            },
            "parameter_sweeps": {
                "data": [
                    {"type": "scatter", "mode": "lines+markers", "name": "Amplitude → radius", "x": [1, 2, 3], "y": amplitude_cases},
                    {"type": "scatter", "mode": "lines+markers", "name": "Phase → initial Q", "x": [1, 2, 3], "y": np.sin(phase_cases)},
                    {"type": "scatter", "mode": "lines+markers", "name": "Frequency → cycles/0.4 s", "x": [1, 2, 3], "y": 0.4 * frequency_cases},
                ],
                "layout": sweep_layout,
                "config": {"responsive": True, "displaylogo": False},
            },
            "alias_comparison": {
                "data": [
                    {"type": "scatter", "mode": "lines", "name": f"true {frequency:.1f} Hz", "x": dense_time, "y": true_dense},
                    {"type": "scatter", "mode": "lines", "name": f"apparent {apparent_alias:.1f} Hz", "x": dense_time, "y": alias_dense, "line": {"dash": "dash"}},
                    {"type": "scatter", "mode": "markers", "name": f"samples at {sample_rate:.1f} Sa/s", "x": time, "y": cosine, "marker": {"size": 8}},
                ],
                "layout": alias_layout,
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": f"A={amplitude:.2f} sets both peak height and IQ radius. f={frequency:+.2f} Hz sets {abs(frequency) * duration:.2f} rotations in this record; φ={phase:.3f} rad sets the starting point.",
            "broken": broken,
            "recovery": "Turn off the forced alias case and restore 200 Sa/s. Then the 5 Hz tone has 40 samples/cycle and five rotations in one second.",
        },
        "diagnostics": {
            "seed": SEED,
            "sample_count": count,
            "projection_error": projection_error,
            "radius_error": radius_error,
            "positive_step_angle": positive_step,
            "negative_step_angle": negative_step,
            "alias_sample_error": alias_error,
            "signature": [
                float(count),
                float(sample_rate / max(abs(frequency), 1e-12)),
                float(abs(frequency) * duration),
                float(phasor.real[0]),
                float(phasor.imag[0]),
                projection_error,
                radius_error,
            ],
        },
    }
