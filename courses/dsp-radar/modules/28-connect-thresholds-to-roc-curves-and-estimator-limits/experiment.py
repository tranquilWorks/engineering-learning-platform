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


TEMPLATE = np.array([1, 1, 1, -1, 1, -1, -1, 1, -1, 1, -1, -1, -1, 1, 1, -1], float)


def _detection(snr):
    rng = np.random.default_rng(2801)
    noise0 = rng.standard_normal((16, 12000))
    noise1 = rng.standard_normal((16, 12000))
    sigma = np.sqrt(16 / 10 ** (snr / 10))
    received0 = sigma * noise0
    received1 = TEMPLATE[:, None] + sigma * noise1
    matched0 = np.sum(TEMPLATE[:, None] * received0, axis=0)
    matched1 = np.sum(TEMPLATE[:, None] * received1, axis=0)
    return matched0 / (4 * sigma), matched1 / (4 * sigma), matched1 / 16, sigma


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    import math

    snr = float(parameters.get("matched_snr_db", 6))
    threshold = float(parameters.get("threshold_sigma", 1.5))
    broken = bool(parameters.get("broken_mode", False))
    if snr not in {-6, -3, 0, 3, 6, 9, 12} or threshold not in {
        -1,
        -0.5,
        0,
        0.5,
        1,
        1.5,
        2,
        2.5,
        3,
    }:
        raise ValueError("Choose a retained matched-filter SNR and threshold")
    score0, score1, estimates, sigma = _detection(snr)
    selected = estimates[score1 >= threshold]
    if len(selected) < 2:
        raise ValueError("Too few selected trials to report sample variance")
    active = selected if broken else estimates
    q = lambda value: 0.5 * math.erfc(value / np.sqrt(2))
    dprime = np.sqrt(10 ** (snr / 10))
    bound = sigma**2 / 16
    alpha = threshold - dprime
    selected_bias = (
        np.sqrt(bound) * np.exp(-(alpha**2) / 2) / np.sqrt(2 * np.pi) / q(alpha)
    )
    signature = [
        float(np.mean(score0 >= threshold)),
        float(np.mean(score1 >= threshold)),
        q(threshold),
        q(alpha),
        float(np.mean(active) - 1),
        float(np.var(active, ddof=1)),
        bound,
        float(np.mean(selected) - 1),
        selected_bias,
        float(np.mean(estimates) - 1),
        len(active),
        float(not broken),
    ]
    fields = [
        ("empirical_false_alarm", "ratio"),
        ("empirical_detection", "ratio"),
        ("analytic_false_alarm", "ratio"),
        ("analytic_detection", "ratio"),
        ("active_estimator_bias", "normalized amplitude"),
        ("active_estimator_variance", "amplitude squared"),
        ("unbiased_variance_bound", "amplitude squared"),
        ("selected_bias", "normalized amplitude"),
        ("analytic_selected_bias", "normalized amplitude"),
        ("all_trial_recovery_bias", "normalized amplitude"),
        ("active_estimator_trials", "trials"),
        ("unbiased_claim_valid", "boolean"),
    ]
    thresholds = np.arange(-1, 3.1, 0.5)
    snrs = [-6, -3, 0, 3, 6, 9, 12]
    snr_runs = [_detection(s) for s in snrs]
    edges = np.arange(-5, 7.25, 0.25)
    h0, _ = np.histogram(score0, edges)
    h1, _ = np.histogram(score1, edges)
    plots = {
        "score_distributions": _plot(
            "Independent H0 and H1 matched scores",
            "Statistic (noise sigma)",
            "Probability per bin (ratio)",
            [
                ("H0", (edges[:-1] + edges[1:]) / 2, h0 / 12000),
                ("H1", (edges[:-1] + edges[1:]) / 2, h1 / 12000),
            ],
        ),
        "roc": _plot(
            "Threshold ROC with exact limiting decisions",
            "False alarm probability (ratio)",
            "Detection probability (ratio)",
            [
                (
                    "empirical",
                    [1, *[np.mean(score0 >= t) for t in thresholds], 0],
                    [1, *[np.mean(score1 >= t) for t in thresholds], 0],
                ),
                (
                    "Gaussian tails",
                    [1, *[q(t) for t in thresholds], 0],
                    [1, *[q(t - dprime) for t in thresholds], 0],
                ),
            ],
        ),
        "threshold_sweep": _plot(
            "Raise threshold: both probabilities fall",
            "Threshold (noise sigma)",
            "Probability (ratio)",
            [
                (
                    "false alarms",
                    thresholds,
                    [np.mean(score0 >= t) for t in thresholds],
                ),
                ("detections", thresholds, [np.mean(score1 >= t) for t in thresholds]),
            ],
        ),
        "variance_sweep": _plot(
            "Unconditioned estimator and Fisher-information bound",
            "Matched-filter SNR (dB)",
            "Variance (amplitude squared)",
            [
                ("sample variance", snrs, [np.var(r[2], ddof=1) for r in snr_runs]),
                ("CRLB", snrs, [10 ** (-s / 10) for s in snrs]),
            ],
        ),
        "bias_sweep": _plot(
            "All-trial amplitude bias across SNR",
            "Matched-filter SNR (dB)",
            "Bias (normalized amplitude)",
            [("empirical bias", snrs, [np.mean(r[2]) - 1 for r in snr_runs])],
        ),
        "selection": _plot(
            "Detection-conditioned estimates select the high tail",
            "Population (0=all; 1=detected)",
            "Mean amplitude (normalized)",
            [
                ("empirical", [0, 1], [np.mean(estimates), np.mean(selected)]),
                ("analytic", [0, 1], [1, 1 + selected_bias]),
            ],
        ),
    }
    return _result(
        signature,
        fields,
        plots,
        {
            "observation": "Normalize the known-pulse matched filter by noise standard deviation. Independent H0/H1 banks trace Gaussian-tail ROC probabilities. The all-trial amplitude estimator attains variance sigma²/pulse energy under known timing and white Gaussian noise.",
            "broken": "Keeping only detected H1 trials selects high amplitude estimates. Its positive bias invalidates the unbiased-estimator claim; a smaller selected variance is not evidence of beating the unbiased CRLB.",
            "recovery": "Restore all 12000 independent H1 trials before estimating amplitude. The recovered bias and SNR-dependent variance are checked separately from the detector operating point.",
        },
        2801,
        broken,
        {
            "trial_count": 12000,
            "samples_per_trial": 16,
            "template_energy": 16.0,
            "histogram_h0_tail_probability": float(1 - h0.sum() / 12000),
            "histogram_h1_tail_probability": float(1 - h1.sum() / 12000),
        },
    )
