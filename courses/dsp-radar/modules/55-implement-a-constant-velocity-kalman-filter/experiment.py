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
    rng = np.random.default_rng(5501)
    acc = 0.8 * rng.standard_normal(100)
    truth = np.zeros((101, 2))
    truth[0] = [1000, 20]
    for k in range(1, 101):
        truth[k] = [
            truth[k - 1, 0] + truth[k - 1, 1] + 0.5 * acc[k - 1],
            truth[k - 1, 1] + acc[k - 1],
        ]
    return truth, truth[:, 0] + 25 * rng.standard_normal(101)


def _filter(z, acceleration_sigma, report_sigma):
    f = np.array([[1.0, 1.0], [0.0, 1.0]])
    g = np.array([0.5, 1.0])
    q = acceleration_sigma**2 * np.outer(g, g)
    r = report_sigma**2
    state = np.zeros((101, 2))
    state[0] = [z[0], 0]
    cov = np.zeros((101, 2, 2))
    cov[0] = np.diag([625.0, 225.0])
    gain = np.zeros((101, 2))
    innovation = np.zeros(101)
    s = np.zeros(101)
    prediction = state.copy()
    for k in range(1, 101):
        prediction[k] = f @ state[k - 1]
        p = f @ cov[k - 1] @ f.T + q
        innovation[k] = z[k] - prediction[k, 0]
        s[k] = p[0, 0] + r
        gain[k] = p[:, 0] / s[k]
        state[k] = prediction[k] + gain[k] * innovation[k]
        j = np.eye(2) - np.outer(gain[k], [1.0, 0.0])
        cov[k] = j @ p @ j.T + r * np.outer(gain[k], gain[k])
        cov[k] = (cov[k] + cov[k].T) / 2
    return state, cov, gain, innovation, s, prediction


def run(parameters):
    qs, rs, broken = _controls(
        parameters,
        [
            ("acceleration_sigma_mps2", 0.8, [0.1, 0.8, 3.2]),
            ("report_sigma_m", 25, [5, 25, 100]),
        ],
    )
    truth, z = _scene()
    active = _filter(z, 0 if broken else qs, rs)
    lowr = _filter(z, qs, 0.5)
    recovery = _filter(z, qs, rs)
    x, p, k, nu, s, pred = active
    rms = lambda v: float(np.sqrt(np.mean(v * v)))
    time = np.arange(101)
    q_sweep = [
        rms(_filter(z, q, rs)[0][15:, 0] - truth[15:, 0]) for q in [0.1, 0.8, 3.2]
    ]
    r_sweep = [np.mean(_filter(z, qs, r)[2][15:, 0]) for r in [5, 25, 100]]
    values = {
        "model_valid": (not broken, "boolean"),
        "position_rmse": (rms(x[15:, 0] - truth[15:, 0]), "m"),
        "velocity_rmse": (rms(x[15:, 1] - truth[15:, 1]), "m/s"),
        "mean_nis": (np.mean(nu[15:] ** 2 / s[15:]), "ratio"),
        "final_position_sigma": (np.sqrt(p[-1, 0, 0]), "m"),
        "final_velocity_sigma": (np.sqrt(p[-1, 1, 1]), "m/s"),
        "mean_position_gain": (np.mean(k[15:, 0]), "ratio"),
        "low_r_position_rmse": (rms(lowr[0][15:, 0] - truth[15:, 0]), "m"),
        "minimum_covariance_eigenvalue": (
            np.linalg.eigvalsh(p).min(),
            "mixed state units",
        ),
    }
    plots = {
        "position": _plot(
            "CV prediction and covariance-weighted update",
            "Time (s)",
            "Position (m)",
            [
                ("Truth", time, truth[:, 0]),
                ("Reports", time, z),
                ("Prediction", time, pred[:, 0]),
                ("Active estimate", time, x[:, 0]),
            ],
        ),
        "error": _plot(
            "Position error and posterior two-sigma bounds",
            "Time (s)",
            "Position error (m)",
            [
                ("Active error", time, x[:, 0] - truth[:, 0]),
                ("+2 sigma", time, 2 * np.sqrt(p[:, 0, 0])),
                ("-2 sigma", time, -2 * np.sqrt(p[:, 0, 0])),
                ("Recovery error", time, recovery[0][:, 0] - truth[:, 0]),
            ],
        ),
        "gain": _plot(
            "Trust evolves from covariance",
            "Time (s)",
            "Position gain (ratio)",
            [
                ("Active", time[1:], k[1:, 0]),
                ("Underestimated R", time[1:], lowr[2][1:, 0]),
            ],
        ),
        "nis": _plot(
            "Normalized innovation squared",
            "Time (s)",
            "NIS (ratio)",
            [
                ("Active", time[1:], nu[1:] ** 2 / s[1:]),
                ("Underestimated R", time[1:], lowr[3][1:] ** 2 / lowr[4][1:]),
            ],
        ),
        "q_sweep": _plot(
            "Q assumption on identical reports",
            "Assumed acceleration sigma (m/s²)",
            "Position RMSE (m)",
            [("CV estimate", [0.1, 0.8, 3.2], q_sweep)],
        ),
        "r_sweep": _plot(
            "R assumption changes report trust",
            "Assumed report sigma (m)",
            "Mean position gain (ratio)",
            [("CV estimate", [5, 25, 100], r_sweep)],
        ),
    }
    plots["position"]["data"][1]["mode"] = "markers"
    plots["velocity"] = _plot(
        "Velocity state and its posterior uncertainty",
        "Time (s)",
        "Velocity (m/s)",
        [
            ("Truth", time, truth[:, 1]),
            ("Active estimate", time, x[:, 1]),
            ("Estimate +2 sigma", time, x[:, 1] + 2 * np.sqrt(p[:, 1, 1])),
            ("Estimate -2 sigma", time, x[:, 1] - 2 * np.sqrt(p[:, 1, 1])),
        ],
    )
    return _finish(
        values,
        plots,
        "Q=sigma_a² G Gᵀ admits interval acceleration; R=sigma_z² describes report noise. The Kalman gain and Joseph covariance update expose evolving trust and single-record NIS.",
        "Zero process noise over-trusts the constant-velocity model. A separate sigma_z=.5 m comparison over-trusts noisy reports; neither mismatch changes the actual data.",
        "Restore the selected Q and R assumptions on the identical seeded record; disable the toggle for exact recovery. A single NIS record does not establish ensemble consistency.",
        5501,
        broken,
        state=x.tolist(),
        covariance=p.tolist(),
        gain=k.tolist(),
        innovation=nu.tolist(),
        innovation_variance=s.tolist(),
        innovation_valid=([False] + [True] * 100),
        q_sweep_rmse=q_sweep,
        r_sweep_gain=r_sweep,
    )
