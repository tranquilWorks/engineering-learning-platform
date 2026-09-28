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


def _wrap(angle):
    return np.arctan2(np.sin(angle), np.cos(angle))


def _scene():
    rng = np.random.default_rng(5601)
    f = np.kron(np.eye(2), [[1.0, 1.0], [0.0, 1.0]])
    g = np.kron(np.eye(2), np.array([[0.5], [1.0]]))
    acc = 0.25 * rng.standard_normal((2, 100))
    truth = np.zeros((101, 4))
    truth[0] = [-1600, 4, 600, -12]
    for k in range(1, 101):
        truth[k] = f @ truth[k - 1] + g @ acc[:, k - 1]
    radius = np.hypot(truth[:, 0], truth[:, 2])
    bearing = np.arctan2(truth[:, 2], truth[:, 0])
    z = np.column_stack(
        [
            radius + 18 * rng.standard_normal(101),
            _wrap(bearing + np.deg2rad(0.8) * rng.standard_normal(101)),
        ]
    )
    return truth, z


def _filter(z, bearing_sigma, wrap=True):
    f = np.kron(np.eye(2), [[1.0, 1.0], [0.0, 1.0]])
    g = np.kron(np.eye(2), np.array([[0.5], [1.0]]))
    q = 0.25**2 * g @ g.T
    r = np.diag([18**2, np.deg2rad(bearing_sigma) ** 2])
    x = np.zeros((101, 4))
    p = np.zeros((101, 4, 4))
    nu = np.zeros((101, 2))
    s = np.zeros((101, 2, 2))
    nis = np.zeros(101)
    hlog = np.zeros((101, 2, 4))
    pred = x.copy()
    radius, theta = z[0]
    c, si = np.cos(theta), np.sin(theta)
    x[0] = [radius * c, 0, radius * si, 0]
    j = np.array([[c, -radius * si], [si, radius * c]])
    # Source sweeps retain the reviewed initial covariance; only subsequent R changes.
    p[0][np.ix_([0, 2], [0, 2])] = j @ np.diag([18**2, np.deg2rad(0.8) ** 2]) @ j.T
    p[0, 1, 1] = p[0, 3, 3] = 400
    pred[0] = x[0]
    for k in range(1, 101):
        pred[k] = f @ x[k - 1]
        pp = f @ p[k - 1] @ f.T + q
        px, py = pred[k, [0, 2]]
        rr = px * px + py * py
        if rr <= 25**2:
            raise ValueError(
                "EKF linearization is undefined inside the reviewed 25 m guard"
            )
        radius = np.sqrt(rr)
        h = np.array([[px / radius, 0, py / radius, 0], [-py / rr, 0, px / rr, 0]])
        nu[k] = z[k] - [radius, np.arctan2(py, px)]
        if wrap:
            nu[k, 1] = _wrap(nu[k, 1])
        s[k] = h @ pp @ h.T + r
        gain = np.linalg.solve(s[k], h @ pp).T
        x[k] = pred[k] + gain @ nu[k]
        j = np.eye(4) - gain @ h
        p[k] = j @ pp @ j.T + gain @ r @ gain.T
        p[k] = (p[k] + p[k].T) / 2
        nis[k] = nu[k] @ np.linalg.solve(s[k], nu[k])
        hlog[k] = h
    return x, p, nu, s, nis, hlog, pred


def run(parameters):
    sigma, geometry_range, broken = _controls(
        parameters,
        [
            ("bearing_sigma_deg", 0.8, [0.2, 0.8, 3.2]),
            ("geometry_range_m", 1500, [500, 1500, 3000]),
        ],
    )
    truth, z = _scene()
    active = _filter(z, sigma, not broken)
    correct = _filter(z, sigma, True)
    wrong = _filter(z, sigma, False)
    x, p, nu, s, nis, h, _pred = active
    t = np.arange(101)
    raw = z[:, 0, None] * np.column_stack([np.cos(z[:, 1]), np.sin(z[:, 1])])
    err = np.linalg.norm(x[:, [0, 2]] - truth[:, [0, 2]], axis=1)
    rms = lambda v: float(np.sqrt(np.mean(v * v)))
    sweeps = [_filter(z, bs, True) for bs in [0.2, 0.8, 3.2]]
    sweep_rmse = [
        rms(a[0][15:, [0, 2]] - truth[15:, [0, 2]]) * np.sqrt(2) for a in sweeps
    ]
    values = {
        "model_valid": (not broken, "boolean"),
        "position_rmse": (rms(err[15:]), "m"),
        "mean_nis": (np.mean(nis[15:]), "ratio"),
        "maximum_bearing_innovation": (np.rad2deg(abs(nu[:, 1]).max()), "deg"),
        "final_x": (x[-1, 0], "m"),
        "final_y": (x[-1, 2], "m"),
        "final_position_sigma": (np.sqrt(p[-1, 0, 0] + p[-1, 2, 2]), "m"),
        "geometry_tangential_sigma": (geometry_range * np.deg2rad(sigma), "m"),
        "geometry_major_sigma": (max(18, geometry_range * np.deg2rad(sigma)), "m"),
        "minimum_covariance_eigenvalue": (
            np.linalg.eigvalsh(p).min(),
            "mixed state units",
        ),
    }
    trajectory = [
        ("Truth", truth[:, 0], truth[:, 2]),
        ("Raw reports", raw[:, 0], raw[:, 1]),
        ("Active EKF", x[:, 0], x[:, 2]),
    ]
    for scan in [0, 25, 50, 75, 100]:
        eigen, rotation = np.linalg.eigh(p[scan][np.ix_([0, 2], [0, 2])])
        phase = np.linspace(0, 2 * np.pi, 73)
        ellipse = x[scan, [0, 2], None] + np.sqrt(5.991) * rotation @ np.diag(
            np.sqrt(np.maximum(0, eigen))
        ) @ np.array([np.cos(phase), np.sin(phase)])
        trajectory.append((f"95% ellipse scan {scan + 1}", ellipse[0], ellipse[1]))
    plots = {
        "trajectory": _plot(
            "Cartesian state and local covariance ellipses",
            "Cartesian x (m)",
            "Cartesian y (m)",
            trajectory,
        ),
        "range_innovation": _plot(
            "Range innovation and its two-sigma scale",
            "Time (s)",
            "Range innovation (m)",
            [
                ("Innovation", t[1:], nu[1:, 0]),
                ("+2 sigma", t[1:], 2 * np.sqrt(s[1:, 0, 0])),
                ("-2 sigma", t[1:], -2 * np.sqrt(s[1:, 0, 0])),
            ],
        ),
        "bearing_innovation": _plot(
            "Bearing branch cut: identical polar reports",
            "Time (s)",
            "Bearing innovation (deg)",
            [
                ("Active", t[1:], np.rad2deg(nu[1:, 1])),
                ("Unwrapped subtraction", t[1:], np.rad2deg(wrong[2][1:, 1])),
                ("Wrapped recovery", t[1:], np.rad2deg(correct[2][1:, 1])),
            ],
        ),
        "bearing_sweep": _plot(
            "Assumed bearing accuracy on identical reports",
            "Assumed bearing sigma (deg)",
            "Position RMSE (m)",
            [("EKF", [0.2, 0.8, 3.2], sweep_rmse)],
        ),
        "geometry_sweep": _plot(
            "The same angular error grows with range",
            "Range (m)",
            "Local uncertainty sigma (m)",
            [
                ("Radial", [500, 1500, 3000], [18] * 3),
                (
                    "Tangential",
                    [500, 1500, 3000],
                    np.array([500, 1500, 3000]) * np.deg2rad(sigma),
                ),
            ],
        ),
    }
    plots["trajectory"]["data"][1]["mode"] = "markers"
    plots["normalized_innovation"] = _plot(
        "Each innovation uses its own uncertainty scale",
        "Time (s)",
        "Innovation / marginal sigma (ratio)",
        [
            ("Range", t[1:], nu[1:, 0] / np.sqrt(s[1:, 0, 0])),
            ("Bearing", t[1:], nu[1:, 1] / np.sqrt(s[1:, 1, 1])),
        ],
    )
    return _finish(
        values,
        plots,
        "Cartesian CV prediction meets nonlinear range/bearing through an explicit Jacobian. Bearing innovations are wrapped, covariance uses Joseph form, and r sigma_theta exposes increasing tangential uncertainty.",
        "Subtracting angles across +/-180 degrees without wrapping creates a near-full-turn innovation and a spurious Cartesian correction.",
        "Wrap only the angular innovation with atan2(sin(delta),cos(delta)); preserve the same polar data and restore the selected assumptions.",
        5601,
        broken,
        state=x.tolist(),
        covariance=p.tolist(),
        innovation=nu.tolist(),
        innovation_valid=([False] + [True] * 100),
        nis=nis.tolist(),
        jacobian=h.tolist(),
        bearing_sweep_rmse=sweep_rmse,
    )
