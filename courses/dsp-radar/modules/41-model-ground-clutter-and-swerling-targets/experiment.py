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


def _field(white, rho, slow=0):
    a = white.copy()
    for j in range(1, a.shape[1]):
        a[:, j] = rho * a[:, j - 1] + np.sqrt(1 - rho * rho) * white[:, j]
    b = a.copy()
    for i in range(1, a.shape[0]):
        b[i] = slow * b[i - 1] + np.sqrt(1 - slow * slow) * a[i]
    return b


def _corr(a, lag, axis):
    if axis == 1:
        left, right = a[:, : a.shape[1] - lag], a[:, lag:]
    else:
        left, right = a[: a.shape[0] - lag], a[lag:]
    return float(
        np.real(np.vdot(left, right))
        / np.sqrt(np.vdot(left, left).real * np.vdot(right, right).real)
    )


def run(parameters):
    rho, snr, broken = _controls(
        parameters,
        [
            ("range_correlation", 0.85, [0, 0.5, 0.85, 0.97]),
            ("target_snr_db", -3, [-6, -3, 0]),
        ],
    )
    rng = np.random.default_rng(4101)
    r = 0.25 + 0.05 * np.arange(96)
    profile = 0.1 + 25 * (r / 0.25) ** -2
    white = (rng.normal(size=(64, 96)) + 1j * rng.normal(size=(64, 96))) / np.sqrt(2)
    field = _field(white, rho, 0.92)
    noise = (rng.normal(size=(64, 96)) + 1j * rng.normal(size=(64, 96))) / np.sqrt(2)
    clutter = field * np.sqrt(profile)
    background = clutter + noise
    lags = np.arange(13)
    rc = np.array([_corr(field, l, 1) for l in lags])
    tc = np.array([_corr(field, l, 0) for l in lags])
    power = 10 ** (snr / 10)
    trials = 2000
    target = np.empty((5, trials, 32))
    target[0] = power
    target[1] = -power * np.log(rng.random((trials, 1)))
    target[2] = -power * np.log(rng.random((trials, 32)))
    target[3] = -power / 2 * np.log(rng.random((trials, 1)) * rng.random((trials, 1)))
    target[4] = -power / 2 * np.log(rng.random((trials, 32)) * rng.random((trials, 32)))
    tn = (rng.normal(size=(trials, 32)) + 1j * rng.normal(size=(trials, 32))) / np.sqrt(
        2
    )
    h0 = (rng.normal(size=(trials, 32)) + 1j * rng.normal(size=(trials, 32))) / np.sqrt(
        2
    )
    observed = abs(np.sqrt(target) * np.exp(1j * np.deg2rad(35)) + tn) ** 2
    counts = np.array([1, 2, 4, 8, 16, 32])
    pd = []
    cv = []
    thresholds = []
    for n in counts:
        threshold = np.sort(np.mean(abs(h0[:, :n]) ** 2, axis=1))[1899]
        clean = np.mean(target[:, :, :n], axis=2)
        thresholds.append(threshold)
        pd.append(np.mean(np.mean(observed[:, :, :n], axis=2) > threshold, axis=1))
        cv.append(np.std(clean, axis=1, ddof=1) / np.mean(clean, axis=1))
    pd, cv = np.array(pd), np.array(cv)
    rho_sweep = np.array([0, 0.5, 0.85, 0.97])
    measured = [_corr(_field(white, v), 1, 1) for v in rho_sweep]
    bw = (rng.normal(size=(1024, 96)) + 1j * rng.normal(size=(1024, 96))) / np.sqrt(2)
    bn = (rng.normal(size=(1024, 96)) + 1j * rng.normal(size=(1024, 96))) / np.sqrt(2)
    bp = abs(_field(bw, rho) * np.sqrt(profile) + bn) ** 2
    global_threshold = -np.mean(profile + 1) * np.log(0.05)
    bad = np.mean(bp > global_threshold, axis=0)
    good = np.mean(bp / (profile + 1) > -np.log(0.05), axis=0)
    active = bad if broken else good
    values = {
        "near_clutter_power": (profile[0], "power"),
        "far_clutter_power": (profile[-1], "power"),
        "range_lag1": (rc[1], "correlation"),
        "slow_time_lag1": (tc[1], "correlation"),
        "swerling_i_cv_16": (cv[4, 1], "ratio"),
        "swerling_ii_cv_16": (cv[4, 2], "ratio"),
        "swerling_iii_cv_16": (cv[4, 3], "ratio"),
        "swerling_iv_cv_16": (cv[4, 4], "ratio"),
        "active_near_pfa": (active[:16].mean(), "probability"),
        "active_far_pfa": (active[-16:].mean(), "probability"),
        "recovered_near_pfa": (good[:16].mean(), "probability"),
        "steady_pd_16": (pd[4, 0], "probability"),
        "swerling_ii_pd_16": (pd[4, 2], "probability"),
        "model_valid": (not broken, "boolean"),
    }
    names = ["Steady", "Swerling I", "Swerling II", "Swerling III", "Swerling IV"]
    plots = {
        "background": _heat(
            "Correlated clutter plus white noise",
            "Range (km)",
            "Pulse (index)",
            r,
            np.arange(64),
            10 * np.log10(abs(background) ** 2 + 1e-15),
            "dB",
        ),
        "profile": _plot(
            "Range-dependent mean power",
            "Range (km)",
            "Power (relative)",
            [
                ("Prescribed clutter", r, profile),
                ("Measured clutter", r, np.mean(abs(clutter) ** 2, axis=0)),
                ("White noise", r, np.mean(abs(noise) ** 2, axis=0)),
            ],
        ),
        "correlation": _plot(
            "Clutter memory in both dimensions",
            "Lag (bins or pulses)",
            "Correlation (ratio)",
            [
                ("Range measured", lags, rc),
                ("Range model", lags, rho**lags),
                ("Pulse measured", lags, tc),
                ("Pulse model", lags, 0.92**lags),
                ("White range", lags, [_corr(noise, l, 1) for l in lags]),
            ],
        ),
        "powers": _plot(
            "Slow versus pulse-to-pulse target fluctuation",
            "Pulse (index)",
            "Target power / mean (ratio)",
            [(names[i], np.arange(32), target[i, 0] / power) for i in range(5)],
        ),
        "integration": _plot(
            "Noncoherent integration at equal average SNR",
            "Integrated pulses (count)",
            "Threshold crossings (probability)",
            [(names[i], counts, pd[:, i]) for i in range(5)],
        ),
        "variation": _plot(
            "Fast fluctuations average within a dwell",
            "Integrated pulses (count)",
            "Clean power CV (ratio)",
            [(names[i], counts, cv[:, i]) for i in range(5)],
        ),
        "rho_sweep": _plot(
            "Change range correlation alone",
            "Prescribed correlation (ratio)",
            "Measured lag-one (ratio)",
            [("Measured", rho_sweep, measured)],
        ),
        "failure": _plot(
            "One global threshold versus known local normalization",
            "Range (km)",
            "H0 crossings (probability)",
            [
                ("Global", r, bad),
                ("Local recovery", r, good),
                ("Design", r, np.full(96, 0.05)),
            ],
        ),
    }
    amplitude_bins = np.linspace(0, 5, 65)
    centers = (amplitude_bins[:-1] + amplitude_bins[1:]) / 2
    traces = []
    for label, samples in [
        ("White noise", abs(noise).ravel()),
        (
            "Range-mixed clutter",
            abs(clutter).ravel() / np.sqrt(np.mean(abs(clutter) ** 2)),
        ),
    ]:
        count, _ = np.histogram(samples, amplitude_bins)
        traces.append((label, centers, count / samples.size / np.diff(amplitude_bins)))
    plots["amplitude_distribution"] = _plot(
        "Range mixing changes the aggregate amplitude distribution",
        "Amplitude / RMS (ratio)",
        "Probability density (per ratio)",
        traces,
    )
    power_bins = np.linspace(0, 6, 65)
    centers = (power_bins[:-1] + power_bins[1:]) / 2
    traces = []
    for index in [0, 1, 2]:
        count, _ = np.histogram(
            np.mean(target[index, :, :16], axis=1) / power, power_bins
        )
        traces.append((names[index], centers, count / trials))
    plots["dwell_distribution"] = _plot(
        "Fast fluctuations narrow dwell-average power",
        "Dwell power / mean (ratio)",
        "Probability per bin (ratio)",
        traces,
    )
    return _finish(
        values,
        plots,
        "Clutter has a range-dependent mean and memory. Swerling I/III hold power through a dwell; II/IV redraw every pulse. Equal average SNR does not imply equal integration stability.",
        "One global white-background threshold overspends false alarms near the radar and underspends them farther away.",
        "Normalize by the known local expected clutter-plus-noise power. This is an oracle-background comparison, not an estimated CFAR algorithm; disable the toggle to replay it.",
        4101,
        broken,
        target_trials=trials,
        background_shape=[64, 96],
        pd_by_count=pd.tolist(),
        cv_by_count=cv.tolist(),
    )
