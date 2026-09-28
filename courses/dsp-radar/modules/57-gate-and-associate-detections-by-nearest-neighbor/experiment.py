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


def _uniform(seed, count, offset=0.5):
    states = np.empty(count)
    state = int(seed)
    for k in range(count):
        state = (16807 * state) % 2147483647
        states[k] = (state + offset) / 2147483647
    return states


def _normal(seed, count, offset=0.5):
    u = _uniform(seed, 2 * ((count + 1) // 2), offset)
    radius = np.sqrt(-2 * np.log(u[::2]))
    phase = 2 * np.pi * u[1::2]
    return np.column_stack([radius * np.cos(phase), radius * np.sin(phase)]).ravel()[
        :count
    ]


def _greedy(cost, valid):
    working = np.where(valid, cost, np.inf).copy()
    assignment = np.full(cost.shape[0], -1, dtype=int)
    for _ in range(min(cost.shape)):
        flat = int(np.argmin(working.ravel(order="F")))
        i, j = np.unravel_index(flat, working.shape, order="F")
        if not np.isfinite(working[i, j]):
            break
        assignment[i] = j
        working[i, :] = np.inf
        working[:, j] = np.inf
    return assignment


def _scene():
    f = np.kron(np.eye(2), [[1.0, 1.0], [0.0, 1.0]])
    g = np.kron(np.eye(2), np.array([[0.5], [1.0]]))
    h = np.array([[1.0, 0, 0, 0], [0, 0, 1, 0]])
    prior = np.array([[-20, 20, 0, 0], [178, 22, 48, 2], [375, 25, -94, -6]], float)
    ps = [
        np.diag(np.array(d, float) ** 2)
        for d in [[45, 5, 7, 2], [12, 4, 12, 4], [14, 4, 10, 3]]
    ]
    prediction = prior @ f.T
    position = prediction[:, [0, 2]]
    cov = np.array([h @ (f @ p @ f.T + g @ g.T) @ h.T for p in ps])
    targets = (
        position
        + np.array([[44, 0], [4, -5], [-6, 7]])
        + 6 * _normal(5701, 6).reshape(3, 2)
    )
    reports = np.array(
        [targets[1], [0, 30], targets[0], [110, 140], targets[2], [520, 40]]
    )
    return position, cov, reports


def _distances(position, cov, reports, scale):
    innovation = scale * cov + 36 * np.eye(2)
    residual = reports[None, :, :] - position[:, None, :]
    distance = np.array(
        [
            np.einsum(
                "ni,in->n", residual[i], np.linalg.solve(innovation[i], residual[i].T)
            )
            for i in range(3)
        ]
    )
    return distance, innovation


def run(parameters):
    gate, scale, broken = _controls(
        parameters,
        [
            ("gate_d2", 5.991, [0.5, 5.991, 13.816]),
            ("covariance_scale", 1, [0.25, 1, 4]),
        ],
    )
    position, cov, reports = _scene()
    d, s = _distances(position, cov, reports, scale)
    valid = d <= gate
    active_cost = (
        np.sum((reports[None, :, :] - position[:, None, :]) ** 2, axis=2)
        if broken
        else d
    )
    assignment = _greedy(active_cost, np.ones_like(valid) if broken else valid)
    truth = np.array([2, 0, 1, 0, 3, 0])
    correct = sum(j >= 0 and truth[j] == i + 1 for i, j in enumerate(assignment))
    gates = [0.5, 5.991, 13.816]
    scales = [0.25, 1, 4]
    candidate_sweep = [int(np.count_nonzero(d <= g)) for g in gates]
    area_sweep = [
        np.pi
        * gate
        * np.sqrt(np.linalg.det(_distances(position, cov, reports, c)[1][0]))
        for c in scales
    ]
    values = {
        "model_valid": (not broken, "boolean"),
        "assigned_tracks": (np.count_nonzero(assignment >= 0), "tracks"),
        "correct_links": (correct, "links"),
        "candidate_pairs": (valid.sum(), "pairs"),
        "track1_target_d2": (d[0, 2], "ratio"),
        "track1_clutter_d2": (d[0, 1], "ratio"),
        "track1_gate_area": (np.pi * gate * np.sqrt(np.linalg.det(s[0])), "m²"),
        "track1_report": (assignment[0] + 1, "report ID"),
        "track2_report": (assignment[1] + 1, "report ID"),
        "track3_report": (assignment[2] + 1, "report ID"),
    }
    traces = [
        ("Predictions", position[:, 0], position[:, 1]),
        ("Reports", reports[:, 0], reports[:, 1]),
    ]
    phase = np.linspace(0, 2 * np.pi, 73)
    for i, j in enumerate(assignment):
        eigen, rotation = np.linalg.eigh(s[i])
        ellipse = position[i, :, None] + np.sqrt(gate) * rotation @ np.diag(
            np.sqrt(eigen)
        ) @ np.array([np.cos(phase), np.sin(phase)])
        traces.append((f"Track {i + 1} gate", ellipse[0], ellipse[1]))
        if j >= 0:
            traces.append(
                (
                    f"Track {i + 1} link",
                    [position[i, 0], reports[j, 0]],
                    [position[i, 1], reports[j, 1]],
                )
            )
    plots = {
        "association": _plot(
            "Prediction, covariance gates and selected links",
            "Cartesian x (m)",
            "Cartesian y (m)",
            traces,
        ),
        "distance": _heat(
            "Squared Mahalanobis pair distances",
            "Report ID (index)",
            "Track ID (index)",
            np.arange(1, 7),
            np.arange(1, 4),
            d,
            "d²",
        ),
        "valid": _heat(
            "Admissible pairs before assignment",
            "Report ID (index)",
            "Track ID (index)",
            np.arange(1, 7),
            np.arange(1, 4),
            valid.astype(int),
            "valid pair",
        ),
        "gate_sweep": _plot(
            "Gate threshold admits candidates",
            "Gate threshold d² (ratio)",
            "Admissible pairs (count)",
            [("Pairs", gates, candidate_sweep)],
        ),
        "covariance_sweep": _plot(
            "Prediction uncertainty changes physical gate area",
            "Covariance scale (ratio)",
            "Track 1 gate area (m²)",
            [("Ellipse", scales, area_sweep)],
        ),
    }
    for trace in plots["association"]["data"][:2]:
        trace["mode"] = "markers"
    return _finish(
        values,
        plots,
        "Predict each track and form S=H P^- Hᵀ+R. Gate squared Mahalanobis distances, then greedily select the nearest remaining valid pair with row-and-column removal.",
        "Ungated Euclidean matching favors a cross-ellipse clutter report over a plausible residual along the high-uncertainty direction.",
        "Restore track-specific covariance distances and the gate on unchanged reports. Truth IDs audit correctness only and never enter association.",
        5701,
        broken,
        assignment=(assignment + 1).tolist(),
        distance=d.tolist(),
        innovation_covariance=s.tolist(),
        valid_pairs=valid.tolist(),
        candidate_sweep=candidate_sweep,
    )
