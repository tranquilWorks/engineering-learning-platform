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


def run(parameters):
    from scipy.special import ndtr, ndtri

    sigma, pedestal, broken = _controls(
        parameters,
        [("noise_rms", 1, [0.75, 1, 1.5, 2]), ("clutter_pedestal", 0, [0, 0.5, 1, 2])],
    )
    rng = np.random.default_rng(4301)
    z0 = rng.normal(size=20000)
    z1 = rng.normal(size=20000)
    profile = rng.normal(size=256)
    targets = np.array([47, 102, 170, 225])
    profile[targets] += 4
    gamma = float(ndtri(0.99))
    active_gamma = sigma * gamma if broken else gamma
    h0 = pedestal + sigma * z0
    h1 = pedestal + 4 + sigma * z1
    pfa = np.mean(h0 > active_gamma)
    pd = np.mean(h1 > active_gamma)
    ns = np.array([0.75, 1, 1.25, 1.5, 2])
    ps = np.array([0, 0.5, 1, 1.5, 2])
    noise_pfa = [np.mean(v * z0 > gamma) for v in ns]
    noise_pd = [np.mean(4 + v * z1 > gamma) for v in ns]
    pedestal_pfa = [np.mean(v + z0 > gamma) for v in ps]
    pedestal_pd = [np.mean(v + 4 + z1 > gamma) for v in ps]
    values = {
        "fixed_threshold": (gamma, "amplitude"),
        "active_threshold": (active_gamma, "amplitude"),
        "empirical_pfa": (pfa, "probability"),
        "empirical_pd": (pd, "probability"),
        "miss_count": (sum(h1 <= active_gamma), "trials"),
        "analytic_pfa": (ndtr((pedestal - active_gamma) / sigma), "probability"),
        "analytic_pd": (ndtr((pedestal + 4 - active_gamma) / sigma), "probability"),
        "recovered_pfa": (np.mean(h0 > gamma), "probability"),
        "profile_target_detections": (sum(profile[targets] > gamma), "targets"),
        "active_pfa_at_double_noise": (
            np.mean(2 * z0 > (2 * gamma if broken else gamma)),
            "probability",
        ),
        "model_valid": (not broken, "boolean"),
    }
    hist = np.linspace(-6, 10, 65)
    a, _ = np.histogram(h0, hist)
    b, _ = np.histogram(h1, hist)
    centers = (hist[1:] + hist[:-1]) / 2
    plots = {
        "profile": _plot(
            "One reference-noise range profile",
            "Range cell (index)",
            "Signed amplitude (relative)",
            [
                ("Profile", np.arange(1, 257), profile),
                ("Fixed threshold", np.arange(1, 257), np.full(256, gamma)),
            ],
        ),
        "statistics": _plot(
            "Separate target-absent and target-present banks",
            "Signed amplitude (relative)",
            "Probability per bin (ratio)",
            [("H0", centers, a / 20000), ("H1", centers, b / 20000)],
        ),
        "noise": _plot(
            "Fixed threshold as noise RMS changes",
            "Noise RMS (amplitude)",
            "Probability (ratio)",
            [
                ("Measured Pfa", ns, noise_pfa),
                ("Gaussian Pfa", ns, ndtr(-gamma / ns)),
                ("Measured Pd", ns, noise_pd),
                ("Gaussian Pd", ns, ndtr((4 - gamma) / ns)),
            ],
        ),
        "pedestal": _plot(
            "A positive pedestal raises both crossing rates",
            "Pedestal (amplitude)",
            "Probability (ratio)",
            [("Pfa", ps, pedestal_pfa), ("Pd", ps, pedestal_pd)],
        ),
        "failure": _plot(
            "Silent true-RMS adaptation hides the fixed-threshold failure",
            "Noise RMS (amplitude)",
            "H0 crossing probability (ratio)",
            [
                ("Fixed threshold", ns, noise_pfa),
                ("Hidden adaptive threshold", ns, np.full(5, np.mean(z0 > gamma))),
            ],
        ),
    }
    return _finish(
        values,
        plots,
        "One absolute signed-amplitude threshold is calibrated for zero-mean Gaussian noise at RMS 1. Increasing noise or adding a pedestal changes its false-alarm rate; H0 and H1 counts use separate denominators.",
        "Dividing by each true RMS silently changes the detector into an oracle-adaptive threshold. A flat Pfa curve would no longer demonstrate a fixed threshold.",
        "Restore the single threshold in native amplitude units. Disable the toggle to recover the selected noise/pedestal experiment; pedestal and RMS changes remain physically visible.",
        4301,
        broken,
        trials=20000,
        false_alarm_count=int(sum(h0 > active_gamma)),
        detection_count=int(sum(h1 > active_gamma)),
        noise_pfa=noise_pfa,
        pedestal_pfa=pedestal_pfa,
    )
