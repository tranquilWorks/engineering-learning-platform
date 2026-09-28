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
    velocity = np.where(np.arange(81) >= 40, 32.0, 20.0)
    position = np.r_[1000.0, 1000.0 + np.cumsum(velocity[:-1])]
    z = position + 30 * np.random.default_rng(5401).standard_normal(81)
    available = np.ones(81, bool)
    available[np.array([18, 19, 20, 66, 67, 68]) - 1] = False
    return position, velocity, z, available


def _track(z, available, alpha, beta):
    state = np.zeros((81, 2))
    state[0] = [z[0], 0]
    prediction = state.copy()
    innovation = np.zeros(81)
    for k in range(1, 81):
        prediction[k] = [state[k - 1, 0] + state[k - 1, 1], state[k - 1, 1]]
        if available[k]:
            innovation[k] = z[k] - prediction[k, 0]
            state[k] = prediction[k] + np.array([alpha, beta]) * innovation[k]
        else:
            state[k] = prediction[k]
    return state, prediction, innovation


def run(parameters):
    alpha, beta, broken = _controls(
        parameters,
        [
            ("alpha_gain", 0.35, [0.1, 0.35, 0.85]),
            ("beta_gain", 0.08, [0.01, 0.08, 0.30]),
        ],
    )
    position, velocity, z, available = _scene()
    track, pred, innovation = _track(z, available, alpha, 0 if broken else beta)
    base, _, _ = _track(z, available, alpha, beta)
    wrong, _, _ = _track(z, available, alpha, 0)
    rms = lambda x: float(np.sqrt(np.mean(x * x)))
    sweep_a = [
        rms(_track(z, available, a, beta)[0][10:, 0] - position[10:])
        for a in [0.1, 0.35, 0.85]
    ]
    sweep_b = [
        rms(_track(z, available, alpha, b)[0][10:, 1] - velocity[10:])
        for b in [0.01, 0.08, 0.30]
    ]
    values = {
        "model_valid": (not broken, "boolean"),
        "position_rmse": (rms(track[10:, 0] - position[10:]), "m"),
        "velocity_rmse": (rms(track[10:, 1] - velocity[10:]), "m/s"),
        "steady_position_rmse": (rms(track[10:40, 0] - position[10:40]), "m"),
        "final_velocity": (track[-1, 1], "m/s"),
        "coast_scans": (np.count_nonzero(~available), "scans"),
        "final_position": (track[-1, 0], "m"),
        "innovation_rms": (rms(innovation[available & (np.arange(81) >= 10)]), "m"),
    }
    t = np.arange(81)
    plots = {
        "position": _plot(
            "Prediction and correction through missing reports",
            "Time (s)",
            "Position (m)",
            [
                ("Truth", t, position),
                ("Reports", t[available], z[available]),
                ("Prediction", t, pred[:, 0]),
                ("Active estimate", t, track[:, 0]),
            ],
        ),
        "velocity": _plot(
            "Velocity learning and maneuver lag",
            "Time (s)",
            "Velocity (m/s)",
            [
                ("Truth", t, velocity),
                ("Active", t, track[:, 1]),
                ("Beta zero", t, wrong[:, 1]),
                ("Recovery", t, base[:, 1]),
            ],
        ),
        "innovation": _plot(
            "Available-scan innovations; gaps are coast intervals",
            "Time (s)",
            "Innovation (m)",
            [("Available reports", t[available], innovation[available])],
        ),
        "alpha_sweep": _plot(
            "Alpha changes position response",
            "Alpha (ratio)",
            "Position RMSE (m)",
            [("Same reports", [0.1, 0.35, 0.85], sweep_a)],
        ),
        "beta_sweep": _plot(
            "Beta changes velocity learning",
            "Beta (ratio)",
            "Velocity RMSE (m/s)",
            [("Same reports", [0.01, 0.08, 0.30], sweep_b)],
        ),
    }
    plots["position"]["data"][1]["mode"] = "markers"
    plots["innovation"]["data"][0]["mode"] = "markers"
    return _finish(
        values,
        plots,
        "Predict x+=T v, form the available-report innovation, and correct position by alpha r and velocity by beta r/T. Missing reports coast without invented measurements.",
        "Setting beta to zero leaves the initially zero velocity unlearned, causing persistent position lag.",
        "Restore positive beta on the same measurements; reset the controls and disable the failure for exact recovery.",
        5401,
        broken,
        available=available.tolist(),
        state=track.tolist(),
        prediction=pred.tolist(),
        innovation=innovation.tolist(),
        innovation_valid=available.tolist(),
        alpha_sweep_rmse=sweep_a,
        beta_sweep_rmse=sweep_b,
    )
