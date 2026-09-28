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
        if len(x) <= 512:
            ix = np.arange(len(x))
        else:
            peaks = np.flatnonzero((y[1:-1] >= y[:-2]) & (y[1:-1] > y[2:])) + 1
            selected = peaks[np.argsort(y[peaks])[-12:]]
            keep = np.unique(
                np.r_[
                    0,
                    len(x) - 1,
                    np.argmin(abs(x)),
                    np.argmin(y),
                    np.argmax(y),
                    selected,
                ]
            )
            grid = np.linspace(0, len(x) - 1, 512 - len(keep)).astype(int)
            ix = np.unique(np.r_[keep, grid])
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


def _scene():
    r = np.arange(72) * 15.0
    v = (np.arange(65) - 32) * 0.5
    vv, rr = np.meshgrid(v, r)
    texture = abs(np.random.default_rng(5301).standard_normal((72, 65)))
    score = 0.25 + 0.20 * texture / texture.max()
    for rt, vt, a, sr, sv in [
        (365.25, 4.20, 5, 1.35, 1.10),
        (742.50, -6.25, 3.6, 1.05, 1.30),
    ]:
        score += a * np.exp(
            -0.5 * (((rr - rt) / (15 * sr)) ** 2 + ((vv - vt) / (0.5 * sv)) ** 2)
        )
    score += 1.8 * np.exp(
        -0.5 * (((rr - 392.25) / 10.5) ** 2 + ((vv - 4.60) / 0.325) ** 2)
    )
    for row, col, value in [
        (22, 17, 1.42),
        (22, 18, 1.24),
        (55, 52, 1.38),
        (56, 52, 1.20),
        (10, 55, 1.31),
        (35, 9, 1.27),
        (64, 31, 1.34),
    ]:
        score[row - 1, col - 1] = value
    return r, v, score


def _components(mask):
    labels = np.zeros(mask.shape, dtype=int)
    groups = []
    for row, col in np.argwhere(mask):
        if labels[row, col]:
            continue
        queue = [(int(row), int(col))]
        labels[row, col] = len(groups) + 1
        for a, b in queue:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    i, j = a + dr, b + dc
                    if (
                        0 <= i < mask.shape[0]
                        and 0 <= j < mask.shape[1]
                        and mask[i, j]
                        and not labels[i, j]
                    ):
                        labels[i, j] = len(groups) + 1
                        queue.append((i, j))
        groups.append(np.array(queue))
    return labels, groups


def _peaks(score):
    visited = np.zeros(score.shape, bool)
    peaks = []
    for row, col in np.argwhere(score > 1):
        if visited[row, col]:
            continue
        value = score[row, col]
        queue = [(int(row), int(col))]
        visited[row, col] = True
        maximum = True
        for a, b in queue:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    i, j = a + dr, b + dc
                    if (
                        0 <= i < score.shape[0]
                        and 0 <= j < score.shape[1]
                        and score[i, j] > 1
                    ):
                        if score[i, j] > value:
                            maximum = False
                        elif score[i, j] == value and not visited[i, j]:
                            visited[i, j] = True
                            queue.append((i, j))
        if maximum:
            peaks.append((row, col))
    return np.array(peaks, dtype=int)


def _reports(score, groups, r, v, minimum, exponent):
    reports = []
    for label, coords in enumerate(groups, 1):
        if len(coords) < minimum:
            continue
        rows, cols = coords.T
        excess = score[rows, cols] - 1
        w = excess**exponent
        w /= w.sum()
        center = np.array([w @ r[rows], w @ v[cols]])
        neff = 1 / (w @ w)
        variance = np.array(
            [w @ (r[rows] - center[0]) ** 2, w @ (v[cols] - center[1]) ** 2]
        )
        peak = coords[np.argmax(score[rows, cols])]
        reports.append(
            {
                "component": label,
                "cells": len(coords),
                "range_m": float(center[0]),
                "velocity_mps": float(center[1]),
                "peak_range_m": float(r[peak[0]]),
                "peak_velocity_mps": float(v[peak[1]]),
                "integrated_excess": float(excess.sum()),
                "range_extent_m": float(np.ptp(r[rows]) + 15),
                "velocity_extent_mps": float(np.ptp(v[cols]) + 0.5),
                "effective_cells": float(neff),
                "range_proxy_m": float(np.sqrt(variance[0] / neff + 15**2 / 12)),
                "velocity_proxy_mps": float(np.sqrt(variance[1] / neff + 0.5**2 / 12)),
            }
        )
    return reports


def run(parameters):
    minimum, exponent, broken = _controls(
        parameters,
        [("minimum_cells", 3, [1, 3, 18]), ("weight_exponent", 1, [0, 1, 2])],
    )
    r, v, score = _scene()
    labels, groups = _components(score > 1)
    peaks = _peaks(score)
    reports = _reports(score, groups, r, v, minimum, exponent)
    truth_labels = [
        int(labels[round(365.25 / 15), round(4.2 / 0.5 + 32)]),
        int(labels[round(742.5 / 15), round(-6.25 / 0.5 + 32)]),
    ]
    # Truth is used only to audit component survival, never to construct reports.
    target1 = next(x for x in reports if x["component"] == truth_labels[0])
    size_counts = [len(_reports(score, groups, r, v, k, exponent)) for k in [1, 3, 18]]
    centroids = [
        next(
            x
            for x in _reports(score, groups, r, v, minimum, p)
            if x["component"] == truth_labels[0]
        )
        for p in [0, 1, 2]
    ]
    active_r = r[peaks[:, 0]] if broken else np.array([x["range_m"] for x in reports])
    active_v = (
        v[peaks[:, 1]] if broken else np.array([x["velocity_mps"] for x in reports])
    )
    values = {
        "model_valid": (not broken, "boolean"),
        "threshold_cells": (np.count_nonzero(score > 1), "cells"),
        "local_peaks": (len(peaks), "peaks"),
        "components": (len(groups), "components"),
        "active_reports": (len(active_r), "reports"),
        "retained_truth_components": (
            sum(any(x["component"] == t for x in reports) for t in truth_labels),
            "targets",
        ),
        "target1_range": (target1["range_m"], "m"),
        "target1_velocity": (target1["velocity_mps"], "m/s"),
        "target1_shape_proxy": (target1["range_proxy_m"], "m"),
        "target1_effective_cells": (target1["effective_cells"], "cells"),
    }
    plots = {
        "score": _heat(
            "Normalized detector score",
            "Velocity (m/s; positive approaching)",
            "Range (m)",
            v,
            r,
            score,
            "CUT / threshold",
        ),
        "components": _heat(
            "Eight-connected component labels",
            "Velocity (m/s)",
            "Range (m)",
            v,
            r,
            labels,
            "component ID",
        ),
        "reports": _plot(
            "Selected report locations: peaks or grouped centroids",
            "Velocity (m/s)",
            "Range (m)",
            [
                ("Active reports", active_v, active_r),
                ("Truth", np.array([4.2, -6.25]), np.array([365.25, 742.5])),
            ],
        ),
        "size_sweep": _plot(
            "Minimum-size filtering",
            "Minimum size (cells)",
            "Accepted reports (count)",
            [("Reports", [1, 3, 18], size_counts)],
        ),
        "weight_sweep": _plot(
            "Asymmetric target centroid shift",
            "Weight exponent (ratio)",
            "Target 1 range error (m)",
            [
                (
                    "Weighted centroid",
                    [0, 1, 2],
                    [x["range_m"] - 365.25 for x in centroids],
                )
            ],
        ),
    }
    for trace in plots["reports"]["data"]:
        trace["mode"] = "markers"
    plots["weight_velocity"] = _plot(
        "Weighting also changes signed velocity",
        "Weight exponent (ratio)",
        "Target 1 velocity error (m/s)",
        [
            (
                "Weighted centroid",
                [0, 1, 2],
                [x["velocity_mps"] - 4.2 for x in centroids],
            )
        ],
    )
    retained = [
        sum(
            any(
                report["component"] == label
                for report in _reports(score, groups, r, v, k, exponent)
            )
            for label in truth_labels
        )
        for k in [1, 3, 18]
    ]
    plots["size_sweep"]["data"].append(
        {
            "type": "scatter",
            "mode": "lines+markers",
            "name": "Known target components retained",
            "x": [1, 3, 18],
            "y": retained,
        }
    )
    return _finish(
        values,
        plots,
        "Eight-connected detection groups retain excess-power weighted centroids, extent and effective cell count. Morphology uncertainty proxies are not calibrated tracker measurement covariance.",
        "Peak-only reporting promotes disconnected sidelobes and false cells and quantizes position to cell centers.",
        "Restore grouping and minimum-size filtering on the identical score map; disable the toggle for exact selected-control recovery.",
        5301,
        broken,
        reports=reports,
        truth_component_ids=truth_labels,
        peak_cells=(peaks + 1).tolist(),
        size_sweep_report_counts=size_counts,
    )
