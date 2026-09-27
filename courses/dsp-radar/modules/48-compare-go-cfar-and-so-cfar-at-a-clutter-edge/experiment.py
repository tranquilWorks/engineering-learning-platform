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


def run(parameters):
    contrast, interferer, broken = _controls(
        parameters,
        [
            ("clutter_step_db", 12, [0, 6, 12, 18]),
            ("interferer_power_db", 20, [0, 10, 20]),
        ],
    )
    t = 12
    p = 0.001
    scales = _scales(t, p)
    ago, aso = scales[1:3]
    rng = np.random.default_rng(4801)
    cells = np.arange(1, 241)
    mean = np.where(cells >= 121, 10 ** (contrast / 10), 1.0)
    background = -mean * np.log(rng.random(240))
    power = background.copy()
    targets = np.array([69, 115, 125, 173])
    power[targets] += mean[targets] * 10 ** (np.array([16, 13, 13, 16]) / 10)
    cuts, refs = _refs(240, 12, 2)
    samples = background[refs]
    left = samples[:, :12].mean(axis=1)
    right = samples[:, 12:].mean(axis=1)
    go = ago * np.maximum(left, right)
    so = aso * np.minimum(left, right)
    trials = 25000
    l = -np.log(rng.random((trials, 12)))
    r = -np.log(rng.random((trials, 12)))
    cut = -np.log(rng.random(trials))
    lm = l.mean(axis=1)
    rm = r.mean(axis=1)
    contrasts = np.array([0, 6, 12, 18])
    gp = []
    sp = []
    for db in contrasts:
        q = 10 ** (db / 10)
        gp.append(np.mean(q * cut > ago * np.maximum(lm, q * rm)))
        sp.append(np.mean(q * cut > aso * np.minimum(lm, q * rm)))
    noise = (rng.normal(size=trials) + 1j * rng.normal(size=trials)) / np.sqrt(2)
    target = abs(noise + np.sqrt(10**1.3)) ** 2
    strengths = np.array([-20, 0, 10, 20])
    gpd = []
    spd = []
    for db in strengths:
        contaminated = lm + 10 ** (db / 10) / 12
        gpd.append(np.mean(target > ago * np.maximum(contaminated, rm)))
        spd.append(np.mean(target > aso * np.minimum(contaminated, rm)))
    q = 10 ** (contrast / 10)
    active = aso * np.minimum(lm, q * rm) if broken else ago * np.maximum(lm, q * rm)
    contaminated = lm + 10 ** (interferer / 10) / 12
    values = {
        "go_alpha": (ago, "ratio"),
        "so_alpha": (aso, "ratio"),
        "active_edge_pfa": (np.mean(q * cut > active), "probability"),
        "recovered_go_edge_pfa": (
            np.mean(q * cut > ago * np.maximum(lm, q * rm)),
            "probability",
        ),
        "contaminated_go_pd": (
            np.mean(target > ago * np.maximum(contaminated, rm)),
            "probability",
        ),
        "contaminated_so_pd": (
            np.mean(target > aso * np.minimum(contaminated, rm)),
            "probability",
        ),
        "shared_ca_go_pfa": (_variant_pfa(scales[0], 12, "GO"), "probability"),
        "shared_ca_so_pfa": (_variant_pfa(scales[0], 12, "SO"), "probability"),
        "go_edge_threshold": (go[120 - cuts[0]], "power"),
        "so_edge_threshold": (so[120 - cuts[0]], "power"),
        "model_valid": (not broken, "boolean"),
    }
    plots = {
        "profile": _plot(
            "Individually calibrated GO and SO at a clutter edge",
            "Range cell (index)",
            "Power (relative)",
            [("Observed", cells, power), ("GO", cuts + 1, go), ("SO", cuts + 1, so)],
        ),
        "sides": _plot(
            "The two side means explain the decision",
            "Range cell (index)",
            "Estimated power (relative)",
            [("Leading", cuts + 1, left), ("Lagging", cuts + 1, right)],
        ),
        "edge": _plot(
            "High-side CUT against mixed reference populations",
            "Clutter contrast (dB)",
            "H0 crossings (probability)",
            [("GO", contrasts, gp), ("SO", contrasts, sp)],
        ),
        "interferer": _plot(
            "One contaminated side can make GO mask a weak CUT",
            "Interferer excess power (dB)",
            "Pd (probability)",
            [("GO", strengths, gpd), ("SO", strengths, spd)],
        ),
        "calibration": _plot(
            "A shared CA multiplier is not equal-Pfa calibration",
            "Variant: GO, SO (index)",
            "Homogeneous Pfa (probability)",
            [
                (
                    "Shared CA alpha",
                    [0, 1],
                    [
                        _variant_pfa(scales[0], 12, "GO"),
                        _variant_pfa(scales[0], 12, "SO"),
                    ],
                ),
                ("Variant-specific", [0, 1], [p, p]),
            ],
        ),
    }
    return _finish(
        values,
        plots,
        "GO protects the high side of a clutter edge; SO can preserve a weak target when one reference side is contaminated. Each statistic needs its own homogeneous calibration.",
        "Always choosing SO because it preserved one weak target causes excess high-side edge crossings. A shared CA multiplier also fails to give GO and SO the same nominal Pfa.",
        "Restore statistic-specific calibration and choose GO for the protected edge-false-alarm comparison. Disable the toggle; retain the separate SO advantage under one-sided contamination.",
        4801,
        broken,
        trials=trials,
        edge_go_pfa=gp,
        edge_so_pfa=sp,
        interferer_go_pd=gpd,
        interferer_so_pd=spd,
        baseline_references="background-only isolated probes",
    )
