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


def _scene(acceleration):
    truth = np.zeros((60, 6))
    state = np.array([0.0, 20, 0, 0, 5, 0])
    maneuver = np.zeros(60, bool)
    for k in range(60):
        a = (
            np.array([0.0, acceleration])
            if 15 <= k <= 24
            else (np.array([-acceleration, 0.0]) if 38 <= k <= 47 else np.zeros(2))
        )
        maneuver[k] = bool(np.any(a))
        state[[2, 5]] = a
        state[[0, 3]] += state[[1, 4]] + 0.5 * a
        state[[1, 4]] += a
        truth[k] = state
    reports = truth[:, [0, 3]] + 10 * _normal(6007, 120).reshape(60, 2)
    return truth, reports, maneuver


def _bank():
    f = np.array(
        [
            np.kron(np.eye(2), [[1.0, 1, 0], [0, 1, 0], [0, 0, 0]]),
            np.kron(np.eye(2), [[1.0, 1, 0.5], [0, 1, 1], [0, 0, 1]]),
        ]
    )
    steady = np.array([0.5, 1, 1])
    jerk = np.array([1 / 6, 0.5, 1])
    q = np.array(
        [
            np.kron(np.eye(2), 0.35**2 * np.outer(steady, steady)),
            np.kron(np.eye(2), 0.8**2 * np.outer(jerk, jerk)),
        ]
    )
    h = np.array([[1.0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0]])
    return f, q, h, 100 * np.eye(2)


def _step(x, p, z, f, q, h, r):
    xp = f @ x
    pp = f @ p @ f.T + q
    nu = z - h @ xp
    s = h @ pp @ h.T + r
    k = np.linalg.solve(s, h @ pp).T
    xn = xp + k @ nu
    j = np.eye(6) - k @ h
    pn = j @ pp @ j.T + k @ r @ k.T
    nis = nu @ np.linalg.solve(s, nu)
    ll = -0.5 * (2 * np.log(2 * np.pi) + np.linalg.slogdet(s)[1] + nis)
    return xn, (pn + pn.T) / 2, ll, nis


def _imm(reports, stay, broken=False):
    f, q, h, r = _bank()
    transition = np.eye(2) if broken else np.array([[stay, 1 - stay], [1 - stay, stay]])
    mu = np.array([1.0, 0.0]) if broken else np.array([0.85, 0.15])
    x = np.tile([0.0, 20, 0, 0, 5, 0], (2, 1))
    p = np.tile(np.diag([100.0, 100, 16, 100, 100, 16]), (2, 1, 1))
    states = []
    covariances = []
    probabilities = []
    models = []
    likelihoods = []
    mixing_log = []
    for z in reports:
        prior = mu @ transition
        mixed_x = np.empty_like(x)
        mixed_p = np.zeros_like(p)
        mixing = np.zeros((2, 2))
        for j in range(2):
            w = mu * transition[:, j] / prior[j] if prior[j] > 0 else np.eye(2)[j]
            mixing[:, j] = w
            mixed_x[j] = w @ x
            for i in range(2):
                delta = x[i] - mixed_x[j]
                mixed_p[j] += w[i] * (p[i] + np.outer(delta, delta))
        logweight = np.full(2, -np.inf)
        lls = []
        for j in range(2):
            x[j], p[j], ll, _ = _step(mixed_x[j], mixed_p[j], z, f[j], q[j], h, r)
            lls.append(ll)
            if prior[j] > 0:
                logweight[j] = np.log(prior[j]) + ll
        weights = np.exp(logweight - np.max(logweight))
        mu = weights / weights.sum()
        combined = mu @ x
        cov = np.zeros((6, 6))
        for j in range(2):
            delta = x[j] - combined
            cov += mu[j] * (p[j] + np.outer(delta, delta))
        states.append(combined)
        covariances.append((cov + cov.T) / 2)
        probabilities.append(mu.copy())
        models.append(x.copy())
        likelihoods.append(lls)
        mixing_log.append(mixing)
    return {
        "state": np.array(states),
        "covariance": np.array(covariances),
        "probability": np.array(probabilities),
        "models": np.array(models),
        "likelihood": np.array(likelihoods),
        "mixing": np.array(mixing_log),
    }


def _fixed(reports):
    f, q, h, r = _bank()
    x = np.array([0.0, 20, 0, 0, 5, 0])
    p = np.diag([100.0, 100, 16, 100, 100, 16])
    states = []
    for z in reports:
        x, p, _, _ = _step(x, p, z, f[0], q[0], h, r)
        states.append(x.copy())
    return np.array(states)


def run(parameters):
    strength, stay, broken = _controls(
        parameters,
        [
            ("maneuver_acceleration_mps2", 2, [0.8, 2, 3.2]),
            ("mode_stay_probability", 0.94, [0.8, 0.94, 0.99]),
        ],
    )
    truth, reports, maneuver = _scene(strength)
    active = _imm(reports, stay, broken)
    recovery = _imm(reports, stay)
    fixed = _fixed(reports)
    x = active["state"]
    rmse = lambda state, actual: float(
        np.sqrt(np.mean(np.sum((state[:, [0, 3]] - actual[:, [0, 3]]) ** 2, axis=1)))
    )
    amplitude = []
    for a in [0.8, 2, 3.2]:
        tr, z, _ = _scene(a)
        amplitude.append([rmse(_imm(z, stay)["state"], tr), rmse(_fixed(z), tr)])
    persistence = [rmse(_imm(reports, p)["state"], truth) for p in [0.8, 0.94, 0.99]]
    values = {
        "model_valid": (not broken, "boolean"),
        "position_rmse": (rmse(x, truth), "m"),
        "fixed_cv_rmse": (rmse(fixed, truth), "m"),
        "maneuver_probability_mean": (
            active["probability"][maneuver, 1].mean(),
            "probability",
        ),
        "maximum_maneuver_probability": (
            active["probability"][:, 1].max(),
            "probability",
        ),
        "final_x": (x[-1, 0], "m"),
        "final_y": (x[-1, 3], "m"),
        "probability_sum_error": (
            abs(active["probability"].sum(axis=1) - 1).max(),
            "ratio",
        ),
        "minimum_covariance_eigenvalue": (
            np.linalg.eigvalsh(active["covariance"]).min(),
            "mixed state units",
        ),
    }
    time = np.arange(1, 61)
    error = lambda state: np.linalg.norm(state[:, [0, 3]] - truth[:, [0, 3]], axis=1)
    plots = {
        "trajectory": _plot(
            "Fixed CV versus interacting motion models",
            "East position (m)",
            "North position (m)",
            [
                ("Truth", truth[:, 0], truth[:, 3]),
                ("Reports", reports[:, 0], reports[:, 1]),
                ("Fixed CV", fixed[:, 0], fixed[:, 3]),
                ("Active IMM", x[:, 0], x[:, 3]),
            ],
        ),
        "probability": _plot(
            "Likelihood updates the two mode probabilities",
            "Time (s)",
            "Mode probability (ratio)",
            [
                ("Straight", time, active["probability"][:, 0]),
                ("Maneuver", time, active["probability"][:, 1]),
                ("Maneuver schedule", time, maneuver.astype(float)),
            ],
        ),
        "error": _plot(
            "Model support changes maneuver error",
            "Time (s)",
            "Position error (m)",
            [
                ("Active IMM", time, error(x)),
                ("Fixed CV", time, error(fixed)),
                ("Recovery", time, error(recovery["state"])),
            ],
        ),
        "models": _plot(
            "Inspect model-conditioned acceleration before mixing",
            "Time (s)",
            "North acceleration (m/s²)",
            [
                ("Truth", time, truth[:, 5]),
                ("Straight model", time, active["models"][:, 0, 5]),
                ("Maneuver model", time, active["models"][:, 1, 5]),
                ("Combined", time, x[:, 5]),
            ],
        ),
        "strength_sweep": _plot(
            "Maneuver strength on paired reports",
            "Acceleration magnitude (m/s²)",
            "Position RMSE (m)",
            [
                ("IMM", [0.8, 2, 3.2], np.array(amplitude)[:, 0]),
                ("Fixed CV", [0.8, 2, 3.2], np.array(amplitude)[:, 1]),
            ],
        ),
        "persistence_sweep": _plot(
            "Transition persistence changes adaptation",
            "Mode stay probability (ratio)",
            "Position RMSE (m)",
            [("IMM", [0.8, 0.94, 0.99], persistence)],
        ),
    }
    plots["trajectory"]["data"][1]["mode"] = "markers"
    return _finish(
        values,
        plots,
        "A shared six-state CV/CA model bank mixes states and covariances, including between-mean spread, before prediction. Log likelihoods normalize posterior mode probabilities; the blended covariance includes model disagreement.",
        "Identity transition probabilities and initial [1,0] make the maneuver mode unreachable even when its likelihood would fit better.",
        "Restore nonzero transition support and the [.85,.15] prior on the same measurements; disable the toggle to reproduce the selected IMM exactly.",
        6007,
        broken,
        state=x.tolist(),
        covariance=active["covariance"].tolist(),
        mode_probability=active["probability"].tolist(),
        mixing_probability=active["mixing"].tolist(),
        model_state=active["models"].tolist(),
        log_likelihood=active["likelihood"].tolist(),
        strength_sweep=amplitude,
        persistence_sweep=persistence,
    )
