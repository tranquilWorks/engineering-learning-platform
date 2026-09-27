from __future__ import annotations

import numpy as np


def _controls(p, spec):
    values = []
    for key, default, choices in spec:
        value = p.get(key, default)
        if isinstance(value, bool) or value not in choices:
            raise ValueError("Choose a retained physical control: " + key)
        values.append(float(value))
    broken = p.get("broken_mode", False)
    if not isinstance(broken, bool):
        raise TypeError("broken_mode must be boolean")
    return (*values, broken)


def _plot(title, xlabel, ylabel, traces):
    data = []
    for name, x, y in traces:
        x, y = np.asarray(x), np.asarray(y)
        ix = np.unique(np.linspace(0, len(x) - 1, min(512, len(x))).astype(int))
        data.append(
            {
                "type": "scatter",
                "mode": "lines",
                "name": name,
                "x": x[ix].tolist(),
                "y": y[ix].tolist(),
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


def _finish(values, plots, observation, failure, recovery, seed, broken, **extra):
    return {
        "metrics": [
            {"id": k, "label": k.replace("_", " "), "value": float(v), "unit": u}
            for k, (v, u) in values.items()
        ],
        "plots": plots,
        "explanations": {
            "observation": observation,
            "broken": failure,
            "recovery": recovery,
        },
        "diagnostics": dict(
            signature=[float(v[0]) for v in values.values()],
            signature_fields=list(values),
            seed=seed,
            broken_active=broken,
            **extra,
        ),
    }


def _alpha(n, p):
    return n * np.expm1(-np.log(p) / n)


def _refs(length, t, g):
    cuts = np.arange(t + g, length - t - g)
    offsets = np.r_[np.arange(-t - g, -g), np.arange(g + 1, g + t + 1)]
    return cuts, cuts[:, None] + offsets


def _os_pfa(a, n, k):
    j = np.arange(n - k + 1, n + 1, dtype=float)
    return float(np.exp(np.sum(np.log(j) - np.log(j + a))))


def _calibrate(probability, p):
    lo, hi = 0.0, 1.0
    for _ in range(32):
        if probability(hi) <= p:
            break
        hi *= 2
    else:
        raise ValueError("Calibration not bracketed")
    for _ in range(80):
        mid = (lo + hi) / 2
        if probability(mid) > p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def run(parameters):
    rank, strength, broken = _controls(
        parameters,
        [("os_rank", 18, [12, 18, 22]), ("interferer_power_db", 20, [0, 10, 20, 30])],
    )
    k = int(rank)
    n = 24
    p = 0.001
    ca = _alpha(n, p)
    base_os = _calibrate(lambda a: _os_pfa(a, n, 18), p)
    proper = _calibrate(lambda a: _os_pfa(a, n, k), p)
    # The named failure changes rank to 22 but reuses rank-18 calibration.
    active_rank = 22 if broken else k
    alpha = base_os if broken else proper
    rng = np.random.default_rng(4901)
    power = -np.log(rng.random(256))
    power[127] += 10**1.5
    power[np.array([114, 119, 135, 140])] += 10 ** (strength / 10)
    cuts, refs = _refs(256, 12, 2)
    samples = power[refs]
    sorted_power = np.sort(samples, axis=1)
    ct = ca * samples.mean(axis=1)
    ot = alpha * sorted_power[:, active_rank - 1]
    trials = 20000
    reference = -np.log(rng.random((trials, 24)))
    noise = (rng.normal(size=trials) + 1j * rng.normal(size=trials)) / np.sqrt(2)
    target = abs(noise + np.sqrt(10**1.3)) ** 2
    counts = np.array([0, 2, 4, 6, 7, 8])
    count_pd = []
    for m in counts:
        bank = reference.copy()
        bank[:, :m] += 10 ** (strength / 10)
        count_pd.append(
            [
                np.mean(target > ca * bank.mean(axis=1)),
                np.mean(target > proper * np.sort(bank, axis=1)[:, k - 1]),
            ]
        )
    strengths = np.array([-20, 0, 10, 20, 30])
    strength_pd = []
    for db in strengths:
        bank = reference.copy()
        bank[:, :4] += 10 ** (db / 10)
        strength_pd.append(
            [
                np.mean(target > ca * bank.mean(axis=1)),
                np.mean(target > proper * np.sort(bank, axis=1)[:, k - 1]),
            ]
        )
    ranks = np.array([12, 16, 18, 20, 22, 24])
    rank_pd = []
    rank_alphas = []
    wrong = []
    contaminated = reference.copy()
    contaminated[:, :4] += 10 ** (strength / 10)
    ordered = np.sort(contaminated, axis=1)
    for rk in ranks:
        a = _calibrate(lambda value, rk=rk: _os_pfa(value, n, int(rk)), p)
        rank_alphas.append(a)
        rank_pd.append(np.mean(target > a * ordered[:, rk - 1]))
        wrong.append(_os_pfa(base_os, n, int(rk)))
    index = 127 - cuts[0]
    active_pd = np.mean(target > alpha * ordered[:, active_rank - 1])
    values = {
        "active_rank": (active_rank, "ascending rank"),
        "active_alpha": (alpha, "ratio"),
        "active_homogeneous_pfa": (_os_pfa(alpha, n, active_rank), "probability"),
        "outlier_capacity": (n - active_rank, "cells"),
        "primary_ca_margin": (power[127] / ct[index], "ratio"),
        "primary_os_margin": (power[127] / ot[index], "ratio"),
        "contaminated_active_pd": (active_pd, "probability"),
        "recovered_alpha": (proper, "ratio"),
        "recovered_pfa": (_os_pfa(proper, n, k), "probability"),
        "model_valid": (not broken, "boolean"),
    }
    count_pd = np.array(count_pd)
    strength_pd = np.array(strength_pd)
    plots = {
        "profile": _plot(
            "CA mean versus calibrated OS rank",
            "Range cell (index)",
            "Power (relative)",
            [
                ("Observed", np.arange(1, 257), power),
                ("CA", cuts + 1, ct),
                ("Active OS", cuts + 1, ot),
            ],
        ),
        "sorted": _plot(
            "Primary CUT reference powers in ascending order",
            "Ascending rank (index)",
            "Reference power (relative)",
            [("Ordered references", np.arange(1, 25), sorted_power[index])],
        ),
        "count": _plot(
            "Contamination crosses the N−k outlier capacity",
            "Strong interferers (count)",
            "Pd (probability)",
            [("CA", counts, count_pd[:, 0]), ("Selected OS", counts, count_pd[:, 1])],
        ),
        "strength": _plot(
            "Four contaminated cells grow stronger",
            "Interferer excess power (dB)",
            "Pd (probability)",
            [
                ("CA", strengths, strength_pd[:, 0]),
                ("OS", strengths, strength_pd[:, 1]),
            ],
        ),
        "rank": _plot(
            "Rank trades sensitivity for contamination tolerance",
            "Ascending rank (index)",
            "Pd (probability)",
            [("Recalibrated OS", ranks, rank_pd)],
        ),
        "failure": _plot(
            "Rank changes require recalibration",
            "Ascending rank (index)",
            "Homogeneous Pfa (probability)",
            [
                ("Reused rank-18 alpha", ranks, wrong),
                ("Recalibrated", ranks, np.full(6, p)),
            ],
        ),
    }
    return _finish(
        values,
        plots,
        "OS-CFAR uses the kth ascending reference power and calibrates its product-form false-alarm law. Its N−k capacity is a strong-outlier limit, not immunity to arbitrary contamination.",
        "The failure selects rank 22 while retaining rank-18 alpha. Its homogeneous Pfa changes, so a Pd comparison no longer has equal calibration.",
        "Recompute alpha for the selected rank, inspect contamination count and strength, and state the lost outlier capacity. Disable the toggle for the selected rank-specific baseline.",
        4901,
        broken,
        trials=trials,
        count_pd=count_pd.tolist(),
        strength_pd=strength_pd.tolist(),
        rank_pd=rank_pd,
        rank_alphas=rank_alphas,
    )
