from __future__ import annotations

from typing import Any

import numpy as np


def _plot(title, xlabel, ylabel, traces):
    data = []
    for name, x, y in traces:
        x, y = np.asarray(x), np.asarray(y)
        indices = np.unique(np.linspace(0, len(x) - 1, min(len(x), 512)).astype(int))
        data.append(
            {
                "type": "scatter",
                "mode": "lines",
                "name": name,
                "x": x[indices].tolist(),
                "y": y[indices].tolist(),
            }
        )
    return {
        "data": data,
        "layout": {
            "title": {"text": title},
            "xaxis": {"title": xlabel},
            "yaxis": {"title": ylabel},
            "legend": {"orientation": "h"},
        },
        "config": {"responsive": True, "displaylogo": False},
    }


def _result(signature, fields, plots, explanations, seed, broken, extra=None):
    return {
        "metrics": [
            {
                "id": fields[i][0],
                "label": fields[i][0].replace("_", " "),
                "value": float(v),
                "unit": fields[i][1],
            }
            for i, v in enumerate(signature)
        ],
        "plots": plots,
        "explanations": explanations,
        "diagnostics": {
            "signature": [float(v) for v in signature],
            "signature_fields": [f[0] for f in fields],
            "seed": seed,
            "broken_active": broken,
            **(extra or {}),
        },
    }


BEFORE = np.array([0.8, -0.5, 0.3, 0.2, -0.15, 0.1, 0.05, -0.03])
AFTER = np.array([0.35, 0.7, -0.45, 0.25, 0.15, -0.1, 0.08, 0.03])


def _signals():
    rng = np.random.default_rng(2601)
    streams = [rng.standard_normal(6000) for _ in range(3)]
    x, independent, noise = [v / np.sqrt(np.mean(v * v)) for v in streams]
    time = np.arange(6000) / 8000
    desired = 0.25 * np.sin(2 * np.pi * 700 * time) + 0.18 * np.sin(
        2 * np.pi * 1100 * time + 0.4
    )
    interference = np.convolve(x, BEFORE)[:6000]
    interference[3000:] = np.convolve(x, AFTER)[3000:6000]
    return x, independent, desired, interference, desired + 0.05 * noise + interference


def _lms(mu, correlation):
    x, independent, _desired, interference, primary = _signals()
    reference = correlation * x + np.sqrt(1 - correlation**2) * independent
    weights = np.zeros(8)
    buffer = np.zeros(8)
    errors = []
    residual = []
    mismatch = []
    history = []
    guard = 6000
    for n in range(6000):
        buffer[1:] = buffer[:-1]
        buffer[0] = reference[n]
        estimate = float(weights @ buffer)
        error = float(primary[n] - estimate)
        candidate = weights + mu * error * buffer
        if (
            not np.all(np.isfinite(candidate))
            or np.linalg.norm(candidate) > 1e4
            or abs(error) > 1e6
        ):
            guard = n
            break
        weights = candidate
        errors.append(error)
        residual.append(interference[n] - estimate)
        mismatch.append(
            float(np.sqrt(np.mean((weights - (BEFORE if n < 3000 else AFTER)) ** 2)))
        )
        history.append(weights.copy())
    return (
        np.asarray(errors),
        np.asarray(residual),
        np.asarray(mismatch),
        weights,
        guard,
        np.asarray(history),
    )


def _settled(run):
    _, _, desired, interference, _ = _signals()
    error, residual, mismatch, _, _, _ = run
    values = []
    for indices in [slice(1976, 3000), slice(4976, 6000)]:
        values.extend(
            [
                10
                * np.log10(
                    np.mean(interference[indices] ** 2)
                    / np.mean(residual[indices] ** 2)
                ),
                np.sum(error[indices] * desired[indices])
                / np.sum(desired[indices] ** 2),
            ]
        )
    streak = np.convolve(
        (mismatch[3000:] < 0.08).astype(int), np.ones(64, dtype=int), "valid"
    )
    qualifying = np.flatnonzero(streak == 64)
    return [
        *values,
        float(mismatch[2999]),
        float(mismatch[-1]),
        float(qualifying[0] + 64 if len(qualifying) else 3001),
    ]


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    mu = float(parameters.get("step_size", 0.006))
    correlation = float(parameters.get("reference_correlation", 1.0))
    broken = bool(parameters.get("broken_mode", False))
    if mu not in {0.0005, 0.002, 0.006, 0.012} or correlation not in {
        0,
        0.25,
        0.5,
        0.75,
        1,
    }:
        raise ValueError("Choose a bounded stable LMS step and reference correlation")
    stable = _lms(mu, correlation)
    failure = _lms(0.35, 1)
    recovery = _lms(0.006, 1)
    signature = [
        *_settled(stable),
        float(failure[4] + 1),
        float(not broken),
        *_settled(recovery)[:2],
    ]
    fields = [
        ("stable_pre_suppression", "dB"),
        ("stable_pre_desired_gain", "ratio"),
        ("stable_post_suppression", "dB"),
        ("stable_post_desired_gain", "ratio"),
        ("stable_pre_coefficient_rmse", "gain"),
        ("stable_post_coefficient_rmse", "gain"),
        ("stable_reacquisition_or_3001_sentinel", "samples"),
        ("unstable_guard_sample", "samples"),
        ("active_stability_valid", "boolean"),
        ("reset_suppression", "dB"),
        ("reset_desired_gain", "ratio"),
    ]
    steps = [0.0005, 0.002, 0.006, 0.012]
    correlations = [1, 0.75, 0.5, 0.25, 0]
    step_runs = [_lms(m, 1) for m in steps]
    correlation_runs = [_lms(0.006, c) for c in correlations]
    time = np.arange(6000) / 8000
    active = failure if broken else stable
    _, _, desired, _, primary = _signals()
    frequency = np.fft.rfftfreq(2048, 1 / 8000)
    window = 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(1024) / 1024)
    plots = {
        "residual_power": _plot(
            "128-sample running residual power",
            "Sample index (integer)",
            "Mean squared amplitude (normalized squared)",
            [
                (
                    "residual interference",
                    np.arange(64, 5937),
                    np.convolve(stable[1] ** 2, np.ones(128) / 128, "valid"),
                ),
                (
                    "canceller output",
                    np.arange(64, 5937),
                    np.convolve(stable[0] ** 2, np.ones(128) / 128, "valid"),
                ),
            ],
        ),
        "waveforms": _plot(
            "Desired waveform survives cancellation",
            "Time (s)",
            "Amplitude (normalized)",
            [
                ("desired", time[4976:5176], desired[4976:5176]),
                ("primary", time[4976:5176], primary[4976:5176]),
                ("stable output", time[4976:5176], stable[0][4976:5176]),
            ],
        ),
        "convergence": _plot(
            "Path changes at sample 3001",
            "Sample index (integer)",
            "Coefficient RMSE (gain)",
            [
                ("selected stable step", np.arange(1, 6001), stable[2]),
                ("reset at 0.006", np.arange(1, 6001), recovery[2]),
            ],
        ),
        "coefficients": _plot(
            "Final estimated coupling coefficients",
            "Tap index (integer)",
            "Coefficient (gain)",
            [
                ("true after path change", np.arange(8), AFTER),
                ("learned", np.arange(8), stable[3]),
            ],
        ),
        "step_sweep": _plot(
            "Step-size convergence tradeoff",
            "LMS step (ratio)",
            "Post-change suppression (dB)",
            [("correlated reference", steps, [_settled(r)[2] for r in step_runs])],
        ),
        "correlation_sweep": _plot(
            "An unrelated reference cannot predict interference",
            "Reference correlation (ratio)",
            "Post-change suppression (dB)",
            [("step 0.006", correlations, [_settled(r)[2] for r in correlation_runs])],
        ),
        "guard": _plot(
            "Active LMS output ends before unsafe weights",
            "Sample index (integer)",
            "Error amplitude (normalized)",
            [("active output", np.arange(1, len(active[0]) + 1), active[0])],
        ),
        "spectrum": _plot(
            "Settled post-change windowed spectra",
            "Frequency (Hz)",
            "Amplitude (dB normalized)",
            [
                (
                    name,
                    frequency,
                    20
                    * np.log10(
                        np.maximum(
                            abs(np.fft.rfft(v[-1024:] * window, 2048)) / sum(window),
                            1e-10,
                        )
                    ),
                )
                for name, v in [
                    ("primary", primary),
                    ("stable output", stable[0]),
                    ("desired", desired),
                ]
            ],
        ),
    }
    return _result(
        signature,
        fields,
        plots,
        {
            "observation": "Each sample predicts the coupled reference, subtracts it, then updates eight taps by mu*error*reference. The desired two-tone output should remain; zero output is not the objective.",
            "broken": "Step 0.35 exceeds the white-Gaussian mean-square reference limit 0.2. The guard stops before weights exceed 10000 or error exceeds one million; no unsafe tail is fabricated.",
            "recovery": "Reset all taps and replay the same seed at step 0.006 with the correlated reference. Reacquisition requires 64 consecutive coefficient errors below 0.08; sentinel 3001 means not reacquired.",
        },
        2601,
        broken,
        {
            "sample_count": 6000,
            "path_change_sample": 3001,
            "filter_taps": 8,
            "failure_guard_triggered": failure[4] < 6000,
            "active_output_samples": len(active[0]),
            "reset_weights": recovery[3].tolist(),
        },
    )
