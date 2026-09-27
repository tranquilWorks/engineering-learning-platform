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


def _wilson(count, n):
    rate = np.asarray(count) / n
    z = 1.96
    den = 1 + z * z / n
    center = (rate + z * z / (2 * n)) / den
    half = z / den * np.sqrt(rate * (1 - rate) / n + z * z / (4 * n * n))
    return center - half, center + half


def run(parameters):
    training, pfa, broken = _controls(
        parameters,
        [
            ("training_count", 24, [8, 16, 24]),
            ("design_pfa", 0.001, [0.01, 0.003, 0.001]),
        ],
    )
    n = int(training)
    trials = 200000
    block = 2000
    rng = np.random.default_rng(5201)
    ns = np.array([8, 16, 24, 32, 64])
    pfs = np.array([0.01, 0.003, 0.001])
    pc = np.zeros(3, int)
    nc = np.zeros(5, int)
    alarms = np.zeros(trials, bool)
    bad_count = 0
    alpha = _alpha(n, pfa)
    known = -np.log(pfa)
    for start in range(0, trials, block):
        noise = (
            rng.normal(size=(block, 65)) + 1j * rng.normal(size=(block, 65))
        ) / np.sqrt(2)
        power = abs(noise) ** 2
        cut = power[:, 0]
        cumulative = np.cumsum(power[:, 1:], axis=1)
        mean = cumulative[:, n - 1] / n
        pc += np.sum(cut[:, None] > mean[:, None] * _alpha(n, pfs), axis=0)
        nc += np.sum(
            cut[:, None] > (cumulative[:, ns - 1] / ns) * _alpha(ns, pfa), axis=0
        )
        alarms[start : start + block] = cut > alpha * mean
        bad_count += sum(cut > known * mean)
        if start == 0:
            example_cut = cut[:240].copy()
            example_threshold = alpha * mean[:240]
        del noise, power, cut, cumulative, mean
    count = int(sum(alarms))
    checkpoints = np.array(
        [200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000]
    )
    running = np.cumsum(alarms)[checkpoints - 1]
    low, high = _wilson(running, checkpoints)
    correlated = 0
    textured = 0
    for _ in range(0, trials, block):
        common = (
            rng.normal(size=(block, 1)) + 1j * rng.normal(size=(block, 1))
        ) / np.sqrt(2)
        innovation = (
            rng.normal(size=(block, n + 1)) + 1j * rng.normal(size=(block, n + 1))
        ) / np.sqrt(2)
        cp = abs(np.sqrt(0.65) * common + np.sqrt(0.35) * innovation) ** 2
        correlated += sum(cp[:, 0] > alpha * np.mean(cp[:, 1:], axis=1))
        del common, innovation, cp
        carrier = (
            rng.normal(size=(block, n + 1)) + 1j * rng.normal(size=(block, n + 1))
        ) / np.sqrt(2)
        texture = np.exp(0.9 * rng.normal(size=(block, n + 1)) - 0.5 * 0.9**2)
        tp = abs(carrier) ** 2 * texture
        textured += sum(tp[:, 0] > alpha * np.mean(tp[:, 1:], axis=1))
        del carrier, texture, tp
    active_count = bad_count if broken else count
    active_alpha = known if broken else alpha
    lo, hi = _wilson(active_count, trials)
    values = {
        "active_alpha": (active_alpha, "ratio"),
        "active_alarm_count": (active_count, "trials"),
        "active_measured_pfa": (active_count / trials, "probability"),
        "active_theoretical_pfa": ((1 + active_alpha / n) ** (-n), "probability"),
        "wilson_lower": (lo, "probability"),
        "wilson_upper": (hi, "probability"),
        "correlated_pfa": (correlated / trials, "probability"),
        "textured_pfa": (textured / trials, "probability"),
        "recovered_pfa": (count / trials, "probability"),
        "recovered_theory": ((1 + alpha / n) ** (-n), "probability"),
        "model_valid": (not broken, "boolean"),
    }
    pl, pu = _wilson(pc, trials)
    nl, nu = _wilson(nc, trials)
    mc = np.array([count, correlated, textured])
    ml, mu = _wilson(mc, trials)
    plots = {
        "decisions": _plot(
            "Independent square-law CUT and reference estimate",
            "Trial (index)",
            "Power (relative)",
            [
                ("CUT", np.arange(240), example_cut),
                ("Finite-N threshold", np.arange(240), example_threshold),
            ],
        ),
        "running": _plot(
            "Running rate with 95% Wilson interval",
            "Independent trials (count)",
            "Pfa (probability)",
            [
                ("Measured", checkpoints, running / checkpoints),
                ("Wilson lower", checkpoints, low),
                ("Wilson upper", checkpoints, high),
                ("Design", checkpoints, np.full(len(checkpoints), pfa)),
            ],
        ),
        "pfa": _plot(
            "Requested Pfa sweep at fixed N",
            "Requested Pfa (probability)",
            "Measured Pfa (probability)",
            [("Measured", pfs, pc / trials), ("Lower", pfs, pl), ("Upper", pfs, pu)],
        ),
        "training": _plot(
            "Finite-N calibration across reference counts",
            "Total training cells (count)",
            "Pfa (probability)",
            [
                ("Measured", ns, nc / trials),
                ("Lower", ns, nl),
                ("Upper", ns, nu),
                ("Theory", ns, np.full(5, pfa)),
            ],
        ),
        "models": _plot(
            "Calibration assumptions matter",
            "Model: iid, correlated, texture (index)",
            "Pfa (probability)",
            [
                ("Measured", np.arange(3), mc / trials),
                ("Lower", np.arange(3), ml),
                ("Upper", np.arange(3), mu),
            ],
        ),
        "failure": _plot(
            "Known-noise alpha overspends the finite-N budget",
            "Rule: known-noise, finite-N (index)",
            "Pfa (probability)",
            [
                ("Measured", [0, 1], [bad_count / trials, count / trials]),
                ("Theory", [0, 1], [(1 + known / n) ** (-n), pfa]),
            ],
        ),
    }
    return _finish(
        values,
        plots,
        "Count false alarms from independent H0 trials and report a Wilson interval. Finite-N calibration matches iid exponential-power theory; correlated Gaussian and cellwise lognormal texture violate that model.",
        "Using −ln(Pfa) on a finite reference mean raises actual Pfa. A small or zero count is also not evidence of zero operational risk.",
        "Restore N(Pfa^(−1/N)−1), retain all 200000 independent trials and the interval, and disclose the background model. Disable the toggle for exact finite-N replay.",
        5201,
        broken,
        trials=trials,
        block_trials=block,
        training_alarm_counts=nc.tolist(),
        pfa_alarm_counts=pc.tolist(),
        running_counts=running.tolist(),
        model_alarm_counts=mc.tolist(),
        running_wilson_width=(high - low).tolist(),
    )
