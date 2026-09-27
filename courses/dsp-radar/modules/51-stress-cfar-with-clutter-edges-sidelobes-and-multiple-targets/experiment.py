from __future__ import annotations

import math

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


def _variant_pfa(a, t, variant):
    so = 2 * sum(
        math.exp(
            (t + j) * math.log(t)
            + math.lgamma(t + j)
            - math.lgamma(t)
            - math.lgamma(j + 1)
            - (t + j) * math.log(2 * t + a)
        )
        for j in range(t)
    )
    return so if variant == "SO" else 2 * (t / (t + a)) ** t - so


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


def _scales(t, p, k=18):
    return np.array(
        [
            _alpha(2 * t, p),
            _calibrate(lambda a: _variant_pfa(a, t, "GO"), p),
            _calibrate(lambda a: _variant_pfa(a, t, "SO"), p),
            _calibrate(lambda a: _os_pfa(a, 2 * t, k), p),
        ]
    )


def _four(power, t, g, k, scales):
    cuts, refs = _refs(len(power), t, g)
    r = power[refs]
    left = r[:, :t].mean(axis=1)
    right = r[:, t:].mean(axis=1)
    stats = np.column_stack(
        [
            r.mean(axis=1),
            np.maximum(left, right),
            np.minimum(left, right),
            np.sort(r, axis=1)[:, k - 1],
        ]
    )
    thresholds = stats * scales
    return cuts, thresholds, power[cuts, None] > thresholds, stats


def run(parameters):
    contrast, rank, broken = _controls(
        parameters,
        [("clutter_contrast_db", 12, [0, 6, 12, 18]), ("os_rank", 18, [12, 18, 22])],
    )
    k = int(rank)
    proper = _scales(12, 0.001, k)
    active = np.full(4, proper[0]) if broken else proper
    rng = np.random.default_rng(5101)
    cells = np.arange(1, 257)
    unit = -np.log(rng.random(256))
    targets = np.array([69, 81, 140, 204, 193, 197, 211, 215])
    snrs = np.array([28, 14, 14, 13, 20, 20, 20, 20])
    offsets = np.arange(-12, 13)
    response = np.array(
        [
            0.004,
            0.008,
            0.015,
            0.025,
            0.01,
            0.05,
            0.02,
            0.12,
            0.03,
            0.25,
            0.55,
            0.85,
            1,
            0.85,
            0.55,
            0.25,
            0.03,
            0.12,
            0.02,
            0.05,
            0.01,
            0.025,
            0.015,
            0.008,
            0.004,
        ]
    )
    low = 1 + 0.2 * np.cos(2 * np.pi * cells / 83)
    hump = 1 + 2.5 * np.exp(-0.5 * ((cells - 220) / 18) ** 2)

    def scene(db):
        mean = low * np.where(cells >= 145, 10 ** (db / 10), 1) * hump
        power = mean * unit
        total = np.zeros(256)
        dominant = np.zeros(256)
        owners = np.zeros(256, int)
        for j, (center, snr) in enumerate(zip(targets, snrs)):
            ix = center + offsets
            addition = mean[center] * 10 ** (snr / 10) * response
            power[ix] += addition
            total[ix] += addition
            update = addition > dominant[ix]
            dominant[ix[update]] = addition[update]
            owners[ix[update]] = j
        return power, mean, total, owners

    power, mean, total, owners = scene(contrast)
    cuts, threshold, det, stats = _four(power, 12, 3, k, active)
    truth = np.isin(cuts, targets)
    artifact = (total[cuts] > 0) & ~truth
    categories = np.full(len(cuts), 3, int)
    _, refs = _refs(256, 12, 3)
    near_edge = abs(cells[cuts] - 145) <= 15
    categories[near_edge] = 0
    categories[(categories == 3) & np.any(total[refs] > 0, axis=1)] = 1
    windows = cuts[:, None] + np.arange(-15, 16)
    variation = np.max(mean[windows], axis=1) / np.min(mean[windows], axis=1)
    categories[(categories == 3) & (variation > 1.5)] = 2
    h0_counts = np.array(
        [
            [
                sum(det[:, j] & ~truth & ~artifact & (categories == cat))
                for cat in range(4)
            ]
            for j in range(4)
        ]
    )
    artifacts = np.array(
        [
            [sum(det[:, j] & artifact & (owners[cuts] == owner)) for owner in range(8)]
            for j in range(4)
        ]
    )
    target_indices = targets - cuts[0]
    misses = np.sum(~det[target_indices], axis=0)
    disagreement = np.any(det != det[:, [0]], axis=1)
    contrasts = np.array([0, 6, 12, 18])
    edge_cross = []
    edge_target = []
    for db in contrasts:
        pp, _, _, _ = scene(db)
        cc, _, dd, _ = _four(pp, 12, 3, k, proper)
        zone = (abs(cells[cc] - 145) <= 15) & ~np.isin(cc, targets)
        edge_cross.append(np.sum(dd[zone], axis=0))
        edge_target.append(dd[140 - cc[0]])
    trials = 12000
    reference = -np.log(rng.random((trials, 24)))
    noise = (rng.normal(size=trials) + 1j * rng.normal(size=trials)) / np.sqrt(2)
    cut = abs(noise + np.sqrt(10**1.3)) ** 2
    order = np.array([v for pair in zip(range(12), range(12, 24)) for v in pair])
    counts = np.array([0, 2, 4, 6, 7, 8])
    pd = []
    for m in counts:
        bank = reference.copy()
        bank[:, order[:m]] += 100
        left = bank[:, :12].mean(axis=1)
        right = bank[:, 12:].mean(axis=1)
        statistics = np.column_stack(
            [
                bank.mean(axis=1),
                np.maximum(left, right),
                np.minimum(left, right),
                np.sort(bank, axis=1)[:, k - 1],
            ]
        )
        pd.append(np.mean(cut[:, None] > statistics * proper, axis=0))
    law = lambda a: np.array(
        [
            (1 + a[0] / 24) ** -24,
            _variant_pfa(a[1], 12, "GO"),
            _variant_pfa(a[2], 12, "SO"),
            _os_pfa(a[3], 24, k),
        ]
    )
    calibration = law(active)
    values = {
        "active_ca_pfa": (calibration[0], "probability"),
        "active_go_pfa": (calibration[1], "probability"),
        "active_so_pfa": (calibration[2], "probability"),
        "active_os_pfa": (calibration[3], "probability"),
        "ca_missed_targets": (misses[0], "targets"),
        "go_missed_targets": (misses[1], "targets"),
        "so_missed_targets": (misses[2], "targets"),
        "os_missed_targets": (misses[3], "targets"),
        "ca_h0_crossings": (sum(h0_counts[0]), "cells"),
        "ca_response_artifacts": (sum(artifacts[0]), "cells"),
        "disagreement_cells": (sum(disagreement), "cells"),
        "active_os_alpha": (active[3], "ratio"),
        "model_valid": (not broken, "boolean"),
    }
    names = ["CA", "GO", "SO", "OS"]
    pd = np.array(pd)
    edge_cross = np.array(edge_cross)
    inspect = np.array([81, 140, 204])
    inspection = stats[inspect - cuts[0]]
    plots = {
        "scene": _plot(
            "Same scene, four explicit reference statistics",
            "Range (km)",
            "Power (relative)",
            [("Observed", cells * 0.03, power)]
            + [
                (name, cells[cuts] * 0.03, threshold[:, j])
                for j, name in enumerate(names)
            ],
        ),
        "inspection": _plot(
            "Weak-neighbor, edge and crowded CUT statistics",
            "Probe: weak, edge, crowded (index)",
            "Reference statistic (power)",
            [(name, np.arange(3), inspection[:, j]) for j, name in enumerate(names)],
        ),
        "misses": _plot(
            "Target misses are distinct from noncenter crossings",
            "Detector: CA, GO, SO, OS (index)",
            "Count (cells)",
            [
                ("Target misses", np.arange(4), misses),
                ("True H0 crossings", np.arange(4), h0_counts.sum(axis=1)),
                ("Response artifacts", np.arange(4), artifacts.sum(axis=1)),
            ],
        ),
        "contrast": _plot(
            "Edge-zone noncenter crossings include response artifacts",
            "Clutter contrast (dB)",
            "Crossings (cells)",
            [(name, contrasts, edge_cross[:, j]) for j, name in enumerate(names)],
        ),
        "crowding": _plot(
            "Contamination alternates between both reference sides",
            "Contaminated references (count)",
            "Pd (probability)",
            [(name, counts, pd[:, j]) for j, name in enumerate(names)],
        ),
        "calibration": _plot(
            "Shared alpha breaks equal nominal Pfa",
            "Detector: CA, GO, SO, OS (index)",
            "Homogeneous Pfa (probability)",
            [
                ("Active", np.arange(4), calibration),
                ("Recovered", np.arange(4), law(proper)),
            ],
        ),
    }
    causes = []
    for i in np.flatnonzero(disagreement):
        cell = int(cuts[i] + 1)
        cause = (
            "target-center miss/detection"
            if truth[i]
            else (
                "modeled target-response artifact"
                if artifact[i]
                else [
                    "clutter-edge stencil",
                    "target-contaminated references",
                    "nonuniform background",
                    "homogeneous fluctuation",
                ][categories[i]]
            )
        )
        causes.append(
            {
                "cell": cell,
                "cause": cause,
                "cut_power": float(power[cuts[i]]),
                "thresholds": threshold[i].tolist(),
                "detected": det[i].tolist(),
            }
        )
    return _finish(
        values,
        plots,
        "No single CFAR rule wins across clutter edges, sidelobes and crowded targets. Inspect the reference statistic behind each disagreement and distinguish modeled response artifacts from true H0 crossings.",
        "Applying CA alpha to GO, SO and OS while claiming equal nominal Pfa makes the detector comparison unfair.",
        "Restore all four statistic-specific scale factors on the same scene; disable the toggle. Nonhomogeneous scenes can still depart from homogeneous Pfa calibration.",
        5101,
        broken,
        trials=trials,
        h0_category_counts=h0_counts.tolist(),
        artifact_owner_counts=artifacts.tolist(),
        target_misses=misses.tolist(),
        disagreements=causes,
        crowded_pd=pd.tolist(),
        target_margins_db=(
            10 * np.log10(power[targets, None] / threshold[target_indices])
        ).tolist(),
    )
