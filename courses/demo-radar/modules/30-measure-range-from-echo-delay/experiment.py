from __future__ import annotations

from typing import Any

import numpy as np

C = 299_792_458.0
CAPTURE_US = 16.0
SECOND_AMPLITUDE = 0.65


def _fractional_pulse(record_samples: int, pulse_samples: int, delay_samples: float, amplitude: float = 1.0) -> np.ndarray:
    n = np.arange(record_samples, dtype=float)
    position = n - delay_samples
    left = np.floor(position).astype(int)
    fraction = position - left
    left_value = ((left >= 0) & (left < pulse_samples)).astype(float)
    right = left + 1
    right_value = ((right >= 0) & (right < pulse_samples)).astype(float)
    return amplitude * ((1.0 - fraction) * left_value + fraction * right_value)


def _correlate(received: np.ndarray, pulse_samples: int) -> np.ndarray:
    template = np.ones(pulse_samples, dtype=float)
    return np.abs(np.correlate(received, template, mode="valid"))


def _peak(correlation: np.ndarray) -> tuple[int, float]:
    index = int(np.argmax(correlation))
    offset = 0.0
    if 0 < index < correlation.size - 1:
        left, middle, right = correlation[index - 1 : index + 2]
        denominator = left - 2.0 * middle + right
        if abs(denominator) > 1e-12:
            offset = 0.5 * (left - right) / denominator
    return index, index + float(np.clip(offset, -0.5, 0.5))


def _visible_peaks(values: np.ndarray) -> int:
    threshold = 0.25 * float(values.max(initial=0.0))
    return int(
        np.sum(
            (values[1:-1] > values[:-2])
            & (values[1:-1] >= values[2:])
            & (values[1:-1] > threshold)
        )
    )


def _simulate(parameters: dict[str, Any], *, noise: bool = True, delay_samples_override: float | None = None):
    fs = float(parameters["sample_rate_mhz"]) * 1e6
    delay_us = float(parameters["round_trip_delay_us"])
    pulse_width_us = float(parameters["pulse_width_us"])
    record_samples = max(20, round(CAPTURE_US * 1e-6 * fs))
    pulse_samples = max(1, round(pulse_width_us * 1e-6 * fs))
    delay_samples = delay_samples_override if delay_samples_override is not None else delay_us * 1e-6 * fs

    clean = _fractional_pulse(record_samples, pulse_samples, delay_samples)
    if bool(parameters["second_target"]) and delay_samples_override is None:
        separation = float(parameters["target_separation_us"]) * 1e-6 * fs
        clean += _fractional_pulse(
            record_samples,
            pulse_samples,
            delay_samples + separation,
            SECOND_AMPLITUDE,
        )

    received = clean.copy()
    if noise and float(parameters["noise_sigma"]) > 0:
        rng = np.random.default_rng(3001)
        received += float(parameters["noise_sigma"]) * rng.standard_normal(record_samples)

    correlation = _correlate(received, pulse_samples)
    integer_lag, refined_lag = _peak(correlation)
    return {
        "fs": fs,
        "delay_us": delay_us,
        "pulse_width_us": pulse_width_us,
        "record_samples": record_samples,
        "pulse_samples": pulse_samples,
        "delay_samples": delay_samples,
        "clean": clean,
        "received": received,
        "correlation": correlation,
        "integer_lag": integer_lag,
        "refined_lag": refined_lag,
    }


def _plot_layout(title: str, x_title: str, y_title: str) -> dict[str, Any]:
    return {
        "title": {"text": title, "x": 0.02, "xanchor": "left"},
        "margin": {"l": 65, "r": 20, "t": 55, "b": 55},
        "xaxis": {"title": x_title, "showgrid": True, "zeroline": False},
        "yaxis": {"title": y_title, "showgrid": True, "zeroline": False},
        "legend": {"orientation": "h", "y": 1.12},
        "hovermode": "x unified",
        "uirevision": "keep-view",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    simulation = _simulate(parameters)
    fs = simulation["fs"]
    delay_us = simulation["delay_us"]
    true_range = C * delay_us * 1e-6 / 2.0
    range_bin = C / (2.0 * fs)
    integer_range = range_bin * simulation["integer_lag"]
    refined_range = range_bin * simulation["refined_lag"]
    reported_range = 2.0 * refined_range if bool(parameters["broken_formula"]) else refined_range

    time_us = np.arange(simulation["record_samples"]) / fs * 1e6
    lag_range = np.arange(simulation["correlation"].size) * range_bin

    fractional = np.linspace(0.0, 1.0, 41)
    integer_error: list[float] = []
    refined_error: list[float] = []
    base_lag = 120.0
    sweep_parameters = dict(parameters)
    sweep_parameters["second_target"] = False
    sweep_parameters["noise_sigma"] = 0.0
    for fraction in fractional:
        item = _simulate(
            sweep_parameters,
            noise=False,
            delay_samples_override=base_lag + float(fraction),
        )
        integer_error.append(item["integer_lag"] - base_lag - fraction)
        refined_error.append(item["refined_lag"] - base_lag - fraction)

    rates_mhz = np.linspace(5.0, 50.0, 181)
    ruler = C / (2.0 * rates_mhz * 1e6)

    metrics = [
        {"id": "true_range", "label": "True range", "value": true_range, "unit": "m", "emphasis": "primary"},
        {"id": "delay_samples", "label": "Delay", "value": simulation["delay_samples"], "unit": "samples"},
        {"id": "range_bin", "label": "Range/bin", "value": range_bin, "unit": "m"},
        {"id": "integer_range", "label": "Integer estimate", "value": integer_range, "unit": "m"},
        {"id": "refined_range", "label": "Refined estimate", "value": refined_range, "unit": "m"},
    ]
    if bool(parameters["broken_formula"]):
        metrics.append(
            {
                "id": "reported_range",
                "label": "Broken reported range",
                "value": reported_range,
                "unit": "m",
                "emphasis": "danger",
                "detail": "Uses cτ instead of cτ/2",
            }
        )

    fast_time_layout = _plot_layout(
        "Transmit reference and received echo",
        "Fast time after transmit (µs)",
        "Amplitude",
    )
    fast_time_layout["shapes"] = [
        {
            "type": "rect",
            "xref": "x",
            "yref": "paper",
            "x0": 0,
            "x1": float(parameters["pulse_width_us"]),
            "y0": 0,
            "y1": 0.16,
            "opacity": 0.22,
            "line": {"width": 0},
        }
    ]

    correlation_layout = _plot_layout(
        "Correlation peak on a monostatic range axis",
        "Range cτ/2 (m)",
        "|Correlation|",
    )
    correlation_layout["shapes"] = [
        {"type": "line", "x0": true_range, "x1": true_range, "y0": 0, "y1": 1, "yref": "paper", "line": {"dash": "dash"}},
        {"type": "line", "x0": refined_range, "x1": refined_range, "y0": 0, "y1": 1, "yref": "paper", "line": {"dash": "dot"}},
    ]
    if bool(parameters["broken_formula"]):
        correlation_layout["shapes"].append(
            {"type": "line", "x0": reported_range, "x1": reported_range, "y0": 0, "y1": 1, "yref": "paper", "line": {"dash": "dashdot", "width": 3}}
        )

    explanations = {
        "geometry": f"The measured {delay_us:.4f} µs is a round trip, so the physical range is {true_range:.2f} m.",
        "sampling": f"At {fs / 1e6:.0f} MHz, adjacent integer lag bins are {range_bin:.3f} m apart.",
        "refinement": f"Parabolic interpolation moved the peak from {simulation['integer_lag']} to {simulation['refined_lag']:.3f} samples.",
    }
    if bool(parameters["second_target"]):
        separation_m = C * float(parameters["target_separation_us"]) * 1e-6 / 2.0
        count = _visible_peaks(simulation["correlation"])
        explanations["second_target"] = (
            f"The targets are separated by {separation_m:.1f} m and the current local-peak rule sees {count} peak(s)."
        )
    if bool(parameters["broken_formula"]):
        explanations["broken"] = (
            f"The invalid one-way formula reports {reported_range:.2f} m—exactly twice the refined monostatic result."
        )

    return {
        "metrics": metrics,
        "plots": {
            "fast_time": {
                "data": [
                    {"type": "scattergl", "mode": "lines", "name": "Received", "x": time_us, "y": simulation["received"]},
                    {"type": "scatter", "mode": "lines", "name": "Clean echo", "x": time_us, "y": simulation["clean"], "line": {"dash": "dash"}},
                ],
                "layout": fast_time_layout,
                "config": {"responsive": True, "displaylogo": False},
            },
            "correlation": {
                "data": [
                    {"type": "scattergl", "mode": "lines", "name": "Correlation", "x": lag_range, "y": simulation["correlation"]}
                ],
                "layout": correlation_layout,
                "config": {"responsive": True, "displaylogo": False},
            },
            "fractional_error": {
                "data": [
                    {"type": "scatter", "mode": "lines+markers", "name": "Integer lag", "x": fractional, "y": integer_error},
                    {"type": "scatter", "mode": "lines+markers", "name": "Refined lag", "x": fractional, "y": refined_error, "line": {"dash": "dash"}},
                ],
                "layout": _plot_layout("Fractional-delay staircase", "Fractional true delay (samples)", "Estimation error (samples)"),
                "config": {"responsive": True, "displaylogo": False},
            },
            "sample_rate_ruler": {
                "data": [
                    {"type": "scatter", "mode": "lines", "name": "Range/bin", "x": rates_mhz, "y": ruler},
                    {"type": "scatter", "mode": "markers", "name": "Current", "x": [fs / 1e6], "y": [range_bin], "marker": {"size": 11}},
                ],
                "layout": _plot_layout("Sampling rate as a range ruler", "Sample rate (MHz)", "Range-bin spacing (m)"),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": explanations,
        "diagnostics": {
            "integer_lag": simulation["integer_lag"],
            "refined_lag": simulation["refined_lag"],
            "visible_peaks": _visible_peaks(simulation["correlation"]),
        },
    }
