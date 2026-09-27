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


def _heat(title, xlabel, ylabel, x, y, z, unit):
    x, y, z = np.asarray(x), np.asarray(y), np.asarray(z)

    def indices(axis, scores, limit):
        peaks = np.flatnonzero(
            (scores >= np.r_[-np.inf, scores[:-1]])
            & (scores >= np.r_[scores[1:], -np.inf])
        )
        keep = list(peaks[np.argsort(scores[peaks])[-12:]]) + [
            int(np.argmin(abs(axis))),
            0,
            len(axis) - 1,
        ]
        keep = np.unique(keep)
        grid = np.linspace(
            0, len(axis) - 1, min(len(axis), max(2, limit - len(keep)))
        ).astype(int)
        return np.unique(np.r_[keep, grid])

    ix = indices(x, np.max(z, axis=0), 128)
    iy = indices(y, np.max(z, axis=1), 64)
    return {
        "data": [
            {
                "type": "heatmap",
                "x": x[ix].tolist(),
                "y": y[iy].tolist(),
                "z": z[np.ix_(iy, ix)].tolist(),
                "colorbar": {"title": unit},
            }
        ],
        "layout": {
            "title": {"text": title},
            "xaxis": {"title": xlabel},
            "yaxis": {"title": ylabel},
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


def _ring(power, tr, td, p=0.001):
    from scipy.signal import convolve2d

    hr, hd = tr + 2, td + 2
    mask = np.ones((2 * hr + 1, 2 * hd + 1))
    mask[hr - 2 : hr + 3, hd - 2 : hd + 3] = 0
    n = int(mask.sum())
    estimate = convolve2d(power, mask, mode="same", boundary="fill") / n
    threshold = _alpha(n, p) * estimate
    eligible = np.zeros(power.shape, bool)
    eligible[hr:-hr, hd:-hd] = True
    return threshold, eligible, n, estimate, mask


def run(parameters):
    tr, td, broken = _controls(
        parameters,
        [
            ("range_training_half_width", 6, [3, 6, 12]),
            ("doppler_training_half_width", 4, [2, 4, 8]),
        ],
    )
    tr, td = int(tr), int(td)
    rng = np.random.default_rng(5001)
    r = np.arange(96) * 30.0
    v = np.arange(-32, 32) * 0.625
    mean = (0.8 + 1.2 * (r / r[-1]) ** 2)[:, None] * (
        1 + 2.5 * np.exp(-((v / 2.5) ** 2))
    )
    power = (
        abs(
            np.sqrt(mean / 2)
            * (rng.normal(size=(96, 64)) + 1j * rng.normal(size=(96, 64)))
        )
        ** 2
    )
    rows = np.array([27, 52, 75, 3])
    cols = np.array([44, 21, 34, 7])
    snrs = [24, 20, 18, 20]
    rw = np.array([0.015, 0.05, 0.2, 0.55, 1, 0.55, 0.2, 0.05, 0.015])
    dw = np.array([0.01, 0.04, 0.18, 0.5, 1, 0.5, 0.18, 0.04, 0.01])
    support = np.zeros((96, 64), bool)
    for row, col, snr in zip(rows, cols, snrs):
        rr = np.arange(max(0, row - 4), min(96, row + 5))
        cc = np.arange(max(0, col - 4), min(64, col + 5))
        power[np.ix_(rr, cc)] += (
            mean[row, col]
            * 10 ** (snr / 10)
            * rw[rr - row + 4, None]
            * dw[None, cc - col + 4]
        )
        support[np.ix_(rr, cc)] = True
    threshold, eligible, n, _estimate, mask = _ring(power, tr, td)
    det = (power > threshold) & eligible
    bad = power > threshold
    active = bad if broken else det

    def sweep(values, axis):
        result = []
        for size in values:
            tt, ee, nn, est, _ = _ring(
                power, int(size) if axis == 0 else tr, int(size) if axis == 1 else td
            )
            analysis = ee & ~support
            dd = (power > tt) & ee
            result.append(
                [
                    nn,
                    np.mean(ee),
                    np.sqrt(np.mean((est[analysis] / mean[analysis] - 1) ** 2)),
                    sum(dd[rows[:3], cols[:3]]),
                    sum(dd[~support]),
                ]
            )
        return np.array(result)

    rs = np.array([3, 6, 12])
    ds = np.array([2, 4, 8])
    rstats = sweep(rs, 0)
    dstats = sweep(ds, 1)
    values = {
        "training_cells": (n, "cells"),
        "scale_factor": (_alpha(n, 0.001), "ratio"),
        "eligible_cells": (sum(eligible.ravel()), "cells"),
        "eligible_fraction": (np.mean(eligible), "ratio"),
        "interior_targets_detected": (sum(det[rows[:3], cols[:3]]), "targets"),
        "active_edge_target_detected": (active[3, 7], "boolean"),
        "active_border_crossings": (sum(active[~eligible]), "cells"),
        "recovered_edge_testable": (eligible[3, 7], "boolean"),
        "first_target_margin": (power[27, 44] / threshold[27, 44], "ratio"),
        "h0_crossings": (sum(det[~support]), "cells"),
        "model_valid": (not broken, "boolean"),
    }
    # Display eligibility separately; no fabricated zero threshold denotes an untested border.
    ir = np.arange(tr + 2, 96 - tr - 2)
    ic = np.arange(td + 2, 64 - td - 2)
    plots = {
        "power": _heat(
            "Synthetic square-law range–Doppler scene",
            "Velocity (m/s)",
            "Range (m)",
            v,
            r,
            10 * np.log10(power),
            "dB power",
        ),
        "stencil": _heat(
            "Rectangular training ring excludes guard rectangle and CUT",
            "Doppler offset (bins)",
            "Range offset (bins)",
            np.arange(-td - 2, td + 3),
            np.arange(-tr - 2, tr + 3),
            mask,
            "training=1",
        ),
        "threshold": _heat(
            "Threshold only where every reference exists",
            "Velocity (m/s)",
            "Range (m)",
            v[ic],
            r[ir],
            10 * np.log10(threshold[np.ix_(ir, ic)]),
            "dB power",
        ),
        "eligibility": _heat(
            "Border cells are untested",
            "Velocity (m/s)",
            "Range (m)",
            v,
            r,
            eligible.astype(int),
            "eligible=1",
        ),
        "decisions": _heat(
            "Active detection mask",
            "Velocity (m/s)",
            "Range (m)",
            v,
            r,
            active.astype(int),
            "detection=1",
        ),
        "range_sweep": _plot(
            "Range-window size trades coverage and locality",
            "Range training half-width (bins)",
            "Fraction or normalized RMSE (ratio)",
            [("Eligible", rs, rstats[:, 1]), ("Estimate RMSE", rs, rstats[:, 2])],
        ),
        "doppler_sweep": _plot(
            "Doppler-window size crosses a clutter ridge",
            "Doppler training half-width (bins)",
            "Fraction or normalized RMSE (ratio)",
            [("Eligible", ds, dstats[:, 1]), ("Estimate RMSE", ds, dstats[:, 2])],
        ),
    }
    return _finish(
        values,
        plots,
        "The two-dimensional CA stencil is the outer rectangle minus the full guard rectangle. The exact training count sets alpha; only complete windows define calibrated tests.",
        "Zero-padding missing border powers while retaining the full N produces artificially low finite thresholds and makes an edge target appear testable.",
        "Retain decisions only inside the complete-stencil eligibility mask. The border target remains untested rather than missed. Disable the toggle to restore that policy.",
        5001,
        broken,
        shape=[96, 64],
        range_sweep=rstats.tolist(),
        doppler_sweep=dstats.tolist(),
        target_eligibility=eligible[rows, cols].tolist(),
        target_detections=det[rows, cols].tolist(),
    )
