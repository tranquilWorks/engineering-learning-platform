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


def _normal_bank(seeds):
    states = np.asarray(seeds, dtype=np.int64).copy()
    u = np.empty((len(states), 200))
    for k in range(200):
        states = (16807 * states) % 2147483647
        u[:, k] = (states + 0.5) / 2147483647
    radius = np.sqrt(-2 * np.log(u[:, ::2]))
    phase = 2 * np.pi * u[:, 1::2]
    z = np.empty_like(u)
    z[:, ::2] = radius * np.cos(phase)
    z[:, 1::2] = radius * np.sin(phase)
    return z.reshape(-1, 25, 2, 4)


def _scene(noise, sigma, dt, miss=0):
    t = (np.arange(25) - 12) * dt
    velocity = np.array([[20.0, 5.0], [20.0, -5.0]])
    truth = t[:, None, None] * velocity[None, :, :]
    truth[:, 0, 0] -= miss / 2
    truth[:, 1, 0] += miss / 2
    position = truth[None, :, :, :] + sigma * noise[:, :, :, :2]
    vreports = velocity[None, None, :, :] + 3 * noise[:, :, :, 2:]
    position[:, 1::2] = position[:, 1::2, ::-1].copy()
    vreports[:, 1::2] = vreports[:, 1::2, ::-1].copy()
    return truth, position, vreports


def _track(truth, reports, vreports, sigma, dt, feature, reuse=False):
    b = len(reports)
    x = np.broadcast_to(truth[0], (b, 2, 2)).copy()
    v = np.broadcast_to([[20.0, 5.0], [20.0, -5.0]], (b, 2, 2)).copy()
    xs = []
    vs = []
    links = []
    costs = []
    pcosts = []
    vcosts = []
    batch = np.arange(b)
    for k in range(25):
        pred = x if k == 0 else x + dt * v
        pc = (
            np.sum((reports[:, k, None, :, :] - pred[:, :, None, :]) ** 2, axis=-1)
            / sigma**2
        )
        vc = np.sum((vreports[:, k, None, :, :] - v[:, :, None, :]) ** 2, axis=-1) / 9
        cost = pc + feature * vc
        if reuse:
            chosen = np.argmin(cost, axis=2)
        else:
            # Column-major tie order matches source: report index, then track index.
            flat = np.argmin(cost.transpose(0, 2, 1).reshape(b, 4), axis=1)
            i = flat % 2
            j = flat // 2
            chosen = np.empty((b, 2), int)
            chosen[batch, i] = j
            chosen[batch, 1 - i] = 1 - j
        residual = reports[batch[:, None], k, chosen] - pred
        x = pred + 0.6 * residual
        v = v + 0.25 / dt * residual
        xs.append(x.copy())
        vs.append(v.copy())
        links.append(chosen)
        costs.append(cost)
        pcosts.append(pc)
        vcosts.append(vc)
    links = np.stack(links, axis=1)
    assigned_truth = links.copy()
    assigned_truth[:, 1::2] = 1 - assigned_truth[:, 1::2]
    wrong = np.sum(assigned_truth != np.array([0, 1]), axis=(1, 2))
    transitions = np.count_nonzero(np.diff(assigned_truth, axis=1), axis=(1, 2))
    duplicates = np.sum(links[:, :, 0] == links[:, :, 1], axis=1)
    return {
        "state": np.stack(xs, axis=1),
        "velocity": np.stack(vs, axis=1),
        "assignment": links,
        "truth_links": assigned_truth,
        "wrong": wrong,
        "transitions": transitions,
        "duplicates": duplicates,
        "cost": np.stack(costs, axis=1),
        "position_cost": np.stack(pcosts, axis=1),
        "velocity_cost": np.stack(vcosts, axis=1),
    }


def _sweep(bank, kind, values, sigma, dt):
    failure = [[], []]
    wrong = [[], []]
    for value in values:
        sp = value if kind == "noise" else sigma
        interval = value if kind == "interval" else dt
        miss = value if kind == "miss" else 0
        truth, p, v = _scene(bank, sp, interval, miss)
        for mode in [0, 1]:
            result = _track(truth, p, v, sp, interval, mode)
            failure[mode].append(float(np.mean(result["wrong"] > 0)))
            wrong[mode].append(float(np.mean(result["wrong"])))
    return failure, wrong


def run(parameters):
    sigma, dt, broken = _controls(
        parameters,
        [("position_sigma_m", 6, [2, 6, 10]), ("scan_interval_s", 1, [0.5, 1, 2])],
    )
    truth, reports, vreports = _scene(_normal_bank([5908]), sigma, dt)
    position = _track(truth, reports, vreports, sigma, dt, 0)
    recovery = _track(truth, reports, vreports, sigma, dt, 1)
    bad = _track(truth, reports, vreports, sigma, dt, 0, True)
    active = bad if broken else recovery
    bank = _normal_bank(np.arange(5901, 6101))
    ns = _sweep(bank, "noise", [2, 6, 10], sigma, dt)
    ts = _sweep(bank, "interval", [0.5, 1, 2], sigma, dt)
    ms = _sweep(bank, "miss", [0, 12, 24], sigma, dt)
    rmse = lambda result: float(
        np.sqrt(np.mean(np.sum((result["state"][0] - truth) ** 2, axis=2)))
    )
    values = {
        "model_valid": (not broken, "boolean"),
        "active_wrong_links": (active["wrong"][0], "links"),
        "position_only_wrong_links": (position["wrong"][0], "links"),
        "active_identity_transitions": (active["transitions"][0], "transitions"),
        "duplicate_report_scans": (active["duplicates"][0], "scans"),
        "position_rmse": (rmse(active), "m"),
        "noise_sweep_high_position_failure": (ns[0][0][-1], "probability"),
        "noise_sweep_high_velocity_failure": (ns[0][1][-1], "probability"),
        "wide_separation_position_failure": (ms[0][0][-1], "probability"),
    }
    time = (np.arange(25) - 12) * dt
    trajectory = []
    for i in range(2):
        trajectory.extend(
            [
                (f"Truth {i + 1}", truth[:, i, 0], truth[:, i, 1]),
                (
                    f"Position-only track {i + 1}",
                    position["state"][0, :, i, 0],
                    position["state"][0, :, i, 1],
                ),
                (
                    f"Active track {i + 1}",
                    active["state"][0, :, i, 0],
                    active["state"][0, :, i, 1],
                ),
            ]
        )
    plots = {
        "trajectory": _plot(
            "Crossing geometry and identity-sensitive estimates",
            "Cartesian x (m)",
            "Cartesian y (m)",
            trajectory,
        ),
        "identity": _plot(
            "Truth audit of selected report identities",
            "Time from crossing (s)",
            "Assigned truth ID (index)",
            [
                (f"Track {i + 1}", time, active["truth_links"][0, :, i] + 1)
                for i in range(2)
            ],
        ),
        "position_cost": _heat(
            "Normalized position costs at crossing scan 13",
            "Report ID (index)",
            "Track ID (index)",
            [1, 2],
            [1, 2],
            active["position_cost"][0, 12],
            "position residual² / sigma_p²",
        ),
        "velocity_cost": _heat(
            "Normalized auxiliary velocity costs at crossing",
            "Report ID (index)",
            "Track ID (index)",
            [1, 2],
            [1, 2],
            recovery["velocity_cost"][0, 12],
            "velocity residual² / sigma_v²",
        ),
    }
    for key, title, xlabel, x, results in [
        ("noise", "Position uncertainty", "Position sigma (m)", [2, 6, 10], ns),
        ("interval", "Update interval", "Scan interval (s)", [0.5, 1, 2], ts),
        ("separation", "Closest approach", "Closest approach (m)", [0, 12, 24], ms),
    ]:
        plots[key + "_sweep"] = _plot(
            title + ": 200 paired trials",
            xlabel,
            "At least one wrong link (probability)",
            [
                ("Position only", x, results[0][0]),
                ("Velocity assisted", x, results[0][1]),
            ],
        )
    return _finish(
        values,
        plots,
        "Two existing tracks cross with alternating report order. Position and idealized Cartesian velocity residuals are normalized by their own uncertainties; 200 paired records measure identity failures.",
        "Independent row minima allow both tracks to consume the same report. Even valid one-to-one position-only assignment can swap identities near a crossing.",
        "Restore row-and-column removal plus normalized velocity evidence on unchanged reports. Truth identities are used only for audit; auxiliary Cartesian velocity is an idealized feature.",
        5908,
        broken,
        assignment=(active["assignment"][0] + 1).tolist(),
        state=active["state"][0].tolist(),
        velocity=active["velocity"][0].tolist(),
        noise_sweep=ns,
        interval_sweep=ts,
        separation_sweep=ms,
        trials=200,
    )
