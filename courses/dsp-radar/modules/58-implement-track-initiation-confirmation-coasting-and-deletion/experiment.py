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
    scans = np.arange(1, 31)
    available = (scans >= 4) & (scans <= 24) & ~np.isin(scans, [6, 12, 13])
    noise = 3 * _normal(5802, int(available.sum()), 0)
    target = dict(zip(scans[available], 1000 + 12 * (scans[available] - 4) + noise))
    false_scans = [2, 5, 8, 11, 15, 18, 22, 26]
    false = dict(
        zip(false_scans, 100 + 100 * np.arange(8) + 20 * (_uniform(5801, 8, 0) - 0.5))
    )
    records = []
    labels = []
    for scan in scans:
        pairs = sorted(
            ([(target[scan], 1)] if scan in target else [])
            + ([(false[scan], 0)] if scan in false else [])
        )
        records.append(np.array([x for x, _ in pairs]))
        labels.append([label for _, label in pairs])
    return records, labels


def _manager(records, m, n, coasts):
    active = np.zeros(20, bool)
    confirmed = active.copy()
    x = np.zeros(20)
    v = x.copy()
    age = np.zeros(20, int)
    miss = age.copy()
    history = np.zeros((20, n), bool)
    birth = age.copy()
    confirmation = age.copy()
    deletion = age.copy()
    life = np.zeros((20, 30), int)
    hits = life.copy()
    misses = life.copy()
    assign = np.full((20, 30), -1, int)
    positions = np.zeros((20, 30))
    count = 0
    events = []
    for k, reports in enumerate(records):
        ids = np.flatnonzero(active)
        prediction = x.copy()
        prediction[ids] += v[ids]
        costs = abs(prediction[ids, None] - reports[None, :])
        chosen = (
            _greedy(costs, costs <= 40)
            if len(ids) and len(reports)
            else np.full(len(ids), -1, int)
        )
        used = set(chosen[chosen >= 0].tolist())
        for i, j in zip(ids, chosen):
            age[i] += 1
            history[i, :-1] = history[i, 1:]
            history[i, -1] = j >= 0
            if j >= 0:
                residual = reports[j] - prediction[i]
                x[i] = prediction[i] + 0.7 * residual
                v[i] += 0.2 * residual
                miss[i] = 0
                assign[i, k] = j
            else:
                x[i] = prediction[i]
                miss[i] += 1
            hit_score = int(history[i].sum())
            if not confirmed[i] and hit_score >= m:
                confirmed[i] = True
                confirmation[i] = k + 1
                events.append([k + 1, int(i + 1), "confirmed: M-of-N hits"])
            if not confirmed[i] and age[i] >= n and hit_score < m:
                active[i] = False
                deletion[i] = k + 1
                events.append(
                    [k + 1, int(i + 1), "deleted: failed confirmation window"]
                )
            elif confirmed[i] and miss[i] > coasts:
                active[i] = False
                deletion[i] = k + 1
                events.append([k + 1, int(i + 1), "deleted: coast budget exceeded"])
            life[i, k] = (
                4
                if not active[i]
                else (1 if not confirmed[i] else (3 if miss[i] else 2))
            )
            hits[i, k] = hit_score
            misses[i, k] = miss[i]
            positions[i, k] = x[i]
        for j, report in enumerate(reports):
            if j in used:
                continue
            if count >= 20:
                raise ValueError("Track allocation ceiling exceeded")
            i = count
            count += 1
            active[i] = True
            confirmed[i] = m <= 1
            x[i] = report
            age[i] = 1
            history[i, -1] = True
            birth[i] = k + 1
            assign[i, k] = j
            hits[i, k] = 1
            positions[i, k] = report
            life[i, k] = 2 if confirmed[i] else 1
            confirmation[i] = k + 1 if confirmed[i] else 0
            events.append(
                [k + 1, i + 1, "born confirmed" if confirmed[i] else "born tentative"]
            )
    return {
        "life": life[:count],
        "hits": hits[:count],
        "misses": misses[:count],
        "assignment": assign[:count],
        "positions": positions[:count],
        "birth": birth[:count],
        "confirmation": confirmation[:count],
        "deletion": deletion[:count],
        "active": active[:count],
        "events": events,
    }


def _score(result, labels):
    origins = np.array(
        [
            labels[b - 1][result["assignment"][i, b - 1]]
            for i, b in enumerate(result["birth"])
        ]
    )
    target = np.flatnonzero((origins == 1) & (result["confirmation"] > 0))
    first = target[0] if len(target) else None
    return {
        "false_confirmed": int(np.sum((origins == 0) & (result["confirmation"] > 0))),
        "target_tracks": len(target),
        "confirmation_scan": int(result["confirmation"][target].min())
        if len(target)
        else 0,
        "deletion_scan": int(result["deletion"][target].max()) if len(target) else 0,
        "gap_survived": int(
            first is not None
            and np.array_equal(result["life"][first, 11:14], [3, 3, 2])
        ),
    }


def run(parameters):
    m, coasts, broken = _controls(
        parameters,
        [("confirmation_hits", 3, [1, 3, 4]), ("coast_limit_scans", 2, [0, 2, 5])],
    )
    m = int(m)
    coasts = int(coasts)
    records, labels = _scene()
    baseline = _manager(records, m, 4, coasts)
    wrong = _manager(records, 1, 1, 30)
    active = wrong if broken else baseline
    score = _score(active, labels)
    life = active["life"]
    counts = np.sum((life > 0) & (life < 4), axis=0)
    ms = [_score(_manager(records, i, 4, coasts), labels) for i in [1, 3, 4]]
    ls = [_score(_manager(records, m, 4, i), labels) for i in [0, 2, 5]]
    values = {
        "model_valid": (not broken, "boolean"),
        "allocated_tracks": (len(life), "tracks"),
        "false_confirmed": (score["false_confirmed"], "tracks"),
        "confirmed_target_tracks": (score["target_tracks"], "tracks"),
        "target_confirmation_scan": (score["confirmation_scan"], "scan"),
        "target_last_deletion_scan": (score["deletion_scan"], "scan"),
        "short_gap_same_id_survived": (score["gap_survived"], "boolean"),
        "peak_active_tracks": (max(counts), "tracks"),
        "final_active_tracks": (counts[-1], "tracks"),
    }
    scans = np.arange(1, 31)
    traces = [("Target truth", np.arange(4, 25), 1000 + 12 * np.arange(21))]
    for i in range(len(life)):
        valid = (life[i] > 0) & (life[i] < 4)
        traces.append((f"Track {i + 1}", scans[valid], active["positions"][i, valid]))
    plots = {
        "tracks": _plot(
            "Reports earn a persistent track identity",
            "Scan (index)",
            "Position (m)",
            traces,
        ),
        "lifecycle": _heat(
            "Lifecycle: 0 absent, 1 tentative, 2 confirmed, 3 coast, 4 deleted",
            "Scan (index)",
            "Track ID (index)",
            scans,
            np.arange(1, len(life) + 1),
            life,
            "state code",
        ),
        "counts": _plot(
            "Managed versus bypassed persistence",
            "Scan (index)",
            "Active tracks (count)",
            [
                (
                    "Selected policy",
                    scans,
                    np.sum((baseline["life"] > 0) & (baseline["life"] < 4), axis=0),
                ),
                (
                    "Immediate immortal policy",
                    scans,
                    np.sum((wrong["life"] > 0) & (wrong["life"] < 4), axis=0),
                ),
            ],
        ),
        "confirmation_sweep": _plot(
            "Confirmation evidence requirement",
            "Required hits M of 4 (count)",
            "Confirmed tracks (count)",
            [
                ("False tracks", [1, 3, 4], [s["false_confirmed"] for s in ms]),
                ("Target tracks", [1, 3, 4], [s["target_tracks"] for s in ms]),
            ],
        ),
        "coast_sweep": _plot(
            "Missing-scan budget changes target deletion",
            "Allowed consecutive coasts (scans)",
            "Last target deletion (scan)",
            [("Target history", [0, 2, 5], [s["deletion_scan"] for s in ls])],
        ),
    }
    return _finish(
        values,
        plots,
        "Predict and associate reports before updating an explicit M-of-N lifecycle. Stable IDs record birth, tentative confirmation, coasting and deletion; truth labels enter only the final audit.",
        "The 1-of-1 policy with a 30-scan coast allowance confirms eight isolated false tracks and keeps them active through this record.",
        "Restore the selected M-of-4 and coast policy on identical reports; disabling the toggle reproduces the selected managed history exactly.",
        5801,
        broken,
        lifecycle=life.tolist(),
        hit_scores=active["hits"].tolist(),
        consecutive_misses=active["misses"].tolist(),
        assignment=(active["assignment"] + 1).tolist(),
        events=active["events"],
        birth=active["birth"].tolist(),
        confirmation=active["confirmation"].tolist(),
        deletion=active["deletion"].tolist(),
        noise_seed=5802,
    )
