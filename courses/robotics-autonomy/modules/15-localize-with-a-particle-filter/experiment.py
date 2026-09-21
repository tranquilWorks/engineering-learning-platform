from __future__ import annotations

from typing import Any

import numpy as np


def _layout(title: str, x: str, y: str) -> dict[str, Any]:
    return {
        "title": {"text": title, "x": 0.02},
        "xaxis": {"title": x},
        "yaxis": {"title": y},
        "legend": {"orientation": "h"},
        "margin": {"l": 65, "r": 20, "t": 55, "b": 55},
        "hovermode": "closest",
        "uirevision": "keep-view",
    }


def _trace(name: str, x: Any, y: Any) -> dict[str, Any]:
    return {"type": "scatter", "mode": "lines+markers", "name": name, "x": x, "y": y}


def _statistics(values: np.ndarray, length: float) -> tuple[float, float]:
    angles = 2.0 * np.pi * values / length
    sine = np.mean(np.sin(angles))
    cosine = np.mean(np.cos(angles))
    mean = (np.arctan2(sine, cosine) % (2.0 * np.pi)) * length / (2.0 * np.pi)
    resultant = max(np.hypot(sine, cosine), 1e-15)
    std = length * np.sqrt(max(0.0, -2.0 * np.log(resultant))) / (2.0 * np.pi)
    return float(mean), float(std)


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    count = round(float(parameters["particle_count"]))
    motion_noise = float(parameters["motion_noise_m"])
    sensor_noise = float(parameters["sensor_noise_m"])
    steps = round(float(parameters["steps"]))
    broken = bool(parameters["broken_mode"])
    length = 20.0
    particles = (np.arange(count) + 0.5) * length / count
    weights = np.full(count, 1.0 / count)
    truth = 18.0
    minimum_ess = float(count)
    indexes = np.arange(count, dtype=float) + 1.0
    means: list[float] = []
    truths: list[float] = []
    errors: list[float] = []
    ess_history: list[float] = []
    for step in range(steps):
        truth = (truth + 0.7) % length
        pattern = np.sin(indexes * (step + 1.0) * 1.61803398875)
        pattern = (pattern - np.mean(pattern)) / np.std(pattern)
        particles = (particles + 0.7 + motion_noise * pattern) % length
        truth_range = min(truth, length - truth)
        measurement = truth_range + 0.35 * sensor_noise * np.sin(0.73 * (step + 1.0))
        direct_distance = np.abs(particles)
        predicted = (
            direct_distance
            if broken
            else np.minimum(direct_distance, length - direct_distance)
        )
        likelihood = (
            np.exp(-0.5 * ((measurement - predicted) / sensor_noise) ** 2) + 1e-300
        )
        weights = likelihood / np.sum(likelihood)
        ess = 1.0 / np.sum(weights**2)
        minimum_ess = min(minimum_ess, ess)
        cumulative = np.cumsum(weights)
        locations = (np.arange(count) + 0.5) / count
        particles = particles[np.searchsorted(cumulative, locations, side="left")]
        weights.fill(1.0 / count)
        mean, _ = _statistics(particles, length)
        error = abs((mean - truth + 0.5 * length) % length - 0.5 * length)
        means.append(mean)
        truths.append(truth)
        errors.append(error)
        ess_history.append(ess)
    mean, std = _statistics(particles, length)
    final_error = abs((mean - truth + 0.5 * length) % length - 0.5 * length)
    histogram, edges = np.histogram(
        particles, bins=50, range=(0.0, length), density=True
    )
    centers = 0.5 * (edges[:-1] + edges[1:])
    signature = [mean, std, truth, final_error, minimum_ess]
    return {
        "metrics": [
            {
                "id": "position_error",
                "label": "Final cyclic position error",
                "value": final_error,
                "unit": "m",
                "emphasis": "primary",
            },
            {
                "id": "posterior_std",
                "label": "Circular posterior spread",
                "value": std,
                "unit": "m",
            },
            {
                "id": "minimum_ess",
                "label": "Minimum effective sample size",
                "value": minimum_ess,
                "unit": "particles",
            },
            {
                "id": "final_mean",
                "label": "Posterior mean position",
                "value": mean,
                "unit": "m",
            },
        ],
        "plots": {
            "response": {
                "data": [
                    {
                        "type": "bar",
                        "name": "Posterior density",
                        "x": centers,
                        "y": histogram,
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "True position",
                        "x": [truth, truth],
                        "y": [0.0, max(histogram) * 1.05],
                    },
                ],
                "layout": _layout(
                    "Final cyclic-position belief",
                    "Corridor position (m)",
                    "Probability density (1/m)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "mechanism": {
                "data": [
                    _trace("Position error", np.arange(1, steps + 1), errors),
                    _trace(
                        "ESS fraction",
                        np.arange(1, steps + 1),
                        np.asarray(ess_history) / count,
                    ),
                ],
                "layout": _layout(
                    "Filter error and particle diversity",
                    "Filter step (-)",
                    "Error (m) / ESS fraction (-)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "Likelihood weighting concentrates particles that predict the measured landmark range; systematic resampling turns that likelihood into a new equally weighted posterior population.",
            "broken": "Broken mode uses straight-line distance to the landmark in a cyclic corridor, assigning the wrong likelihood near the wrap boundary and reducing effective sample size.",
            "recovery": "Use the minimum wrapped distance in the sensor model, normalize weights, and monitor effective sample size before deterministic resampling.",
        },
        "diagnostics": {
            "item_id": "P15",
            "reference_basis": "separately formulated deterministic bootstrap-filter recurrence",
            "broken_active": broken,
            "sample_count": count,
            "signature": [float(value) for value in signature],
        },
    }
