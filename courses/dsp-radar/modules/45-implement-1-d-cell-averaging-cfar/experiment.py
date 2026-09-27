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


def _ca(power, t, g, p, geometric=False):
    cuts, refs = _refs(len(power), t, g)
    samples = power[refs]
    estimate = (
        np.exp(np.mean(np.log(np.maximum(samples, 1e-300)), axis=1))
        if geometric
        else np.mean(samples, axis=1)
    )
    threshold = _alpha(2 * t, p) * estimate
    return cuts, threshold, power[cuts] > threshold, estimate


def run(parameters):
    pfa, scale, broken = _controls(
        parameters,
        [
            ("design_pfa", 0.001, [0.01, 0.001, 0.0001]),
            ("scene_power_scale", 1, [0.5, 1, 2]),
        ],
    )
    cells = np.arange(1, 257)
    mean = 0.65 + 0.0045 * cells + 0.32 * (1 + np.sin(2 * np.pi * (cells - 18) / 190))
    rng = np.random.default_rng(4501)
    received = np.sqrt(mean / 2) * (rng.normal(size=256) + 1j * rng.normal(size=256))
    targets = np.array([61, 131, 210])
    received[targets] += np.sqrt(
        mean[targets] * 10 ** (np.array([19, 17, 20]) / 10)
    ) * np.exp(1j * np.array([0.2, -0.8, 1.1]))
    power = scale * abs(received) ** 2
    cuts, threshold, det, estimate = _ca(power, 12, 2, pfa)
    _, bad, _bd, be = _ca(power, 12, 2, pfa, True)
    active = bad if broken else threshold
    active_det = power[cuts] > active
    mask = np.isin(cuts, targets)
    pfs = np.array([0.01, 0.001, 0.0001])
    alphas = _alpha(24, pfs)
    scaling = np.array([0.5, 1, 2])
    ratios = []
    for factor in scaling:
        ratios.append(np.median(_ca(power * factor, 12, 2, pfa)[1] / threshold))
    values = {
        "scale_factor": (_alpha(24, pfa), "ratio"),
        "eligible_cells": (len(cuts), "cells"),
        "excluded_edges": (256 - len(cuts), "cells"),
        "target_detections": (sum(active_det[mask]), "targets"),
        "non_target_crossings": (sum(active_det[~mask]), "cells"),
        "active_noise_at_middle_target": (
            (be if broken else estimate)[131 - cuts[0]],
            "power",
        ),
        "active_threshold_at_middle_target": (active[131 - cuts[0]], "power"),
        "geometric_threshold_ratio": (np.median(bad / threshold), "ratio"),
        "recovered_target_detections": (sum(det[mask]), "targets"),
        "model_valid": (not broken, "boolean"),
    }
    cut = 131
    _, refs = _refs(256, 12, 2)
    example = refs[cut - cuts[0]]
    plots = {
        "profile": _plot(
            "CA-CFAR adapts to local power",
            "Range (m)",
            "Linear power (relative)",
            [
                ("Observed", 15 * (cells - 1), power),
                ("Active threshold", 15 * cuts, active),
                ("Known background", 15 * (cells - 1), scale * mean),
            ],
        ),
        "window": _plot(
            "Reference cells exclude CUT and guards",
            "Offset from middle CUT (cells)",
            "Training power (relative)",
            [("References", example - cut, power[example])],
        ),
        "estimate": _plot(
            "Arithmetic and geometric estimates differ",
            "Range (m)",
            "Estimated noise power (relative)",
            [
                ("Arithmetic", 15 * cuts, estimate),
                ("dB mean converted back", 15 * cuts, be),
            ],
        ),
        "pfa_sweep": _plot(
            "Requested Pfa changes alpha",
            "Requested Pfa (probability)",
            "Scale factor (ratio)",
            [("Finite N=24", pfs, alphas)],
        ),
        "scale_sweep": _plot(
            "Scaling all powers scales the threshold",
            "Whole-scene power scale (ratio)",
            "Threshold scale (ratio)",
            [("Measured", scaling, ratios)],
        ),
        "failure": _plot(
            "A dB average underestimates arithmetic mean power",
            "Range (m)",
            "Threshold power (relative)",
            [
                ("Linear recovery", 15 * cuts, threshold),
                ("Geometric failure", 15 * cuts, bad),
            ],
        ),
    }
    return _finish(
        values,
        plots,
        "CA-CFAR averages 24 linear-power references and uses α=N(Pfa^(−1/N)−1). Only complete windows are eligible; scaling the entire scene preserves decisions.",
        "Averaging dB powers computes a geometric mean, lowers the noise estimate, and breaks the exponential-power calibration.",
        "Restore the arithmetic mean in linear power, retain the guard/CUT exclusion and skip incomplete edge windows. Disable the toggle to replay the selected scene.",
        4501,
        broken,
        eligible_first=int(cuts[0] + 1),
        eligible_last=int(cuts[-1] + 1),
        reference_cells=(example + 1).tolist(),
        target_cells=(targets + 1).tolist(),
        scale_invariant=all(
            np.array_equal(_ca(power * f, 12, 2, pfa)[2], det) for f in scaling
        ),
    )
