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


def _bank(ebn0):
    rng = np.random.default_rng(2701)
    symbols = 2 * (rng.random(4000) >= 0.5).astype(int) - 1
    noise = rng.standard_normal((16, 4000))
    pulse = np.ones(16) / 4
    waveform = pulse[:, None] * symbols + np.sqrt(1 / (2 * 10 ** (ebn0 / 10))) * noise
    statistic = np.sum(pulse[:, None] * waveform, axis=0)
    errors = (np.where(statistic >= 0, 1, -1) != symbols).astype(int)
    return symbols, statistic, errors


def _wilson(errors):
    counts = np.arange(1, len(errors) + 1)
    rate = np.cumsum(errors) / counts
    denominator = 1 + 1.96**2 / counts
    center = (rate + 1.96**2 / (2 * counts)) / denominator
    half = (
        1.96
        / denominator
        * np.sqrt(rate * (1 - rate) / counts + 1.96**2 / (4 * counts**2))
    )
    return rate, np.maximum(0, center - half), np.minimum(1, center + half)


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    import math

    trials = int(parameters.get("trial_count", 4000))
    ebn0 = float(parameters.get("ebn0_db", 2))
    broken = bool(parameters.get("broken_mode", False))
    if trials not in {10, 25, 100, 500, 4000} or ebn0 not in {-4, -2, 0, 2, 4}:
        raise ValueError("Choose a retained independent-trial count and Eb/N0")
    _symbols, statistic, errors = _bank(ebn0)
    lucky = int(np.flatnonzero(errors == 0)[0])
    active_statistics = (
        np.repeat(statistic[lucky], trials) if broken else statistic[:trials]
    )
    active_errors = np.zeros(trials, dtype=int) if broken else errors[:trials]
    rate, low, high = _wilson(active_errors)
    recovery = _wilson(errors[:trials])
    theory = 0.5 * math.erfc(np.sqrt(10 ** (ebn0 / 10)))
    signature = [
        trials,
        ebn0,
        rate[-1],
        low[-1],
        high[-1],
        theory,
        len(np.unique(active_statistics)),
        float(not broken),
        recovery[0][-1],
        recovery[1][-1],
        recovery[2][-1],
        float(np.std(errors.reshape(40, 100).mean(axis=1), ddof=1)),
    ]
    fields = [
        ("reported_trials", "trials"),
        ("ebn0", "dB"),
        ("empirical_ber", "ratio"),
        ("nominal_wilson_lower", "ratio"),
        ("nominal_wilson_upper", "ratio"),
        ("analytic_awgn_ber", "ratio"),
        ("unique_statistics", "trials"),
        ("independence_valid", "boolean"),
        ("recovery_ber", "ratio"),
        ("recovery_ci_lower", "ratio"),
        ("recovery_ci_upper", "ratio"),
        ("hundred_trial_block_std", "ratio"),
    ]
    counts = [10, 25, 100, 500, 4000]
    snrs = [-4, -2, 0, 2, 4]
    count_runs = [_wilson(errors[:n]) for n in counts]
    hist, edges = np.histogram(statistic, bins=np.arange(-3, 3.15, 0.15))
    plots = {
        "running_ber": _plot(
            "Running BER and nominal 95% Wilson limits"
            + (" — INVALID independence" if broken else ""),
            "Trials processed (integer)",
            "Bit error probability (ratio)",
            [
                ("running BER", np.arange(1, trials + 1), rate),
                ("lower", np.arange(1, trials + 1), low),
                ("upper", np.arange(1, trials + 1), high),
                ("AWGN theory", [1, trials], [theory, theory]),
            ],
        ),
        "matched_statistics": _plot(
            "Independent-bank matched-filter distribution",
            "Matched output (normalized amplitude)",
            "Count (trials)",
            [("histogram", (edges[:-1] + edges[1:]) / 2, hist)],
        ),
        "blocks": _plot(
            "Forty independent 100-trial blocks",
            "Block index (integer)",
            "Bit error rate (ratio)",
            [("block BER", np.arange(40), errors.reshape(40, 100).mean(axis=1))],
        ),
        "trial_sweep": _plot(
            "More independent data constrains uncertainty",
            "Independent trial count (integer)",
            "Probability (ratio)",
            [
                ("BER", counts, [r[0][-1] for r in count_runs]),
                ("Wilson lower", counts, [r[1][-1] for r in count_runs]),
                ("Wilson upper", counts, [r[2][-1] for r in count_runs]),
            ],
        ),
        "snr_sweep": _plot(
            "Common random bank; change only Eb/N0",
            "Eb/N0 (dB)",
            "Bit error rate (ratio)",
            [
                ("empirical 4000 trials", snrs, [np.mean(_bank(s)[2]) for s in snrs]),
                (
                    "analytic",
                    snrs,
                    [0.5 * math.erfc(np.sqrt(10 ** (s / 10))) for s in snrs],
                ),
            ],
        ),
    }
    return _result(
        signature,
        fields,
        plots,
        {
            "observation": "Every BPSK trial uses its own 16-sample noise waveform and a unit-energy rectangular matched filter. Running error counts are Bernoulli observations; Wilson bounds quantify finite-sample uncertainty.",
            "broken": "Repeating one lucky correct waveform creates one unique statistic, zero errors, and a misleadingly narrow nominal interval. The independence validity flag is false, so that interval has no binomial coverage claim.",
            "recovery": "Rebuild the independent bank from seed 2701. The bank and decisions reproduce exactly, while block variability remains visible. More trials reduce uncertainty; they do not improve the underlying detector.",
        },
        2701,
        broken,
        {
            "samples_per_trial": 16,
            "independent_bank_trials": 4000,
            "histogram_tail_trials": int(4000 - hist.sum()),
            "lucky_trial_index": lucky,
            "bit_energy": 1.0,
        },
    )
