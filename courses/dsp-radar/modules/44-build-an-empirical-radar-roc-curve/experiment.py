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
    from scipy.special import ndtr

    snr, threshold, broken = _controls(
        parameters,
        [
            ("matched_snr_db", 6, [-6, 0, 6, 12]),
            ("threshold_sigma", 3.090232306, [2, 3.090232306, 4]),
        ],
    )
    rng = np.random.default_rng(4401)
    template = np.array([1, 1, 1, -1, 1, -1, -1, 1, -1, 1, -1, -1, -1, 1, 1, -1])
    energy = np.dot(template, template)
    n0 = rng.normal(size=(16, 60000))
    z0 = np.sum(template[:, None] * n0, axis=0) / np.sqrt(energy)
    example0 = n0[:, 0].copy()
    del n0
    n1 = rng.normal(size=(16, 60000))
    z1 = np.sum(template[:, None] * n1, axis=0) / np.sqrt(energy)
    example1 = n1[:, 0].copy()
    del n1
    dp = 10 ** (snr / 20)
    sigma = np.sqrt(energy) / dp
    gammas = np.array([-1, 0, 1, 2, 2.5, 3.090232306, 3.5, 4, 5])
    snrs = np.array([-6, 0, 6, 12])
    pfa = np.array([np.mean(z0 > g) for g in gammas])
    pd = np.array([[np.mean(10 ** (s / 20) + z1 > g) for g in gammas] for s in snrs])
    tuned = np.sort(z0)[249]
    active = tuned if broken else threshold
    active_pfa = np.mean(z0 > active)
    active_pd = np.mean(dp + z1 > active)
    counts = np.array([500, 2000, 10000, 60000])
    trial_pfa = np.array([np.mean(z0[:n] > threshold) for n in counts])
    trial_pd = np.array([np.mean(dp + z1[:n] > threshold) for n in counts])
    se = np.sqrt(trial_pd * (1 - trial_pd) / counts)
    values = {
        "template_energy": (energy, "amplitude² samples"),
        "active_threshold": (active, "noise RMS"),
        "empirical_pfa": (active_pfa, "probability"),
        "empirical_pd": (active_pd, "probability"),
        "analytic_design_pfa": (ndtr(-threshold), "probability"),
        "analytic_design_pd": (ndtr(dp - threshold), "probability"),
        "false_alarms_per_million": (1e6 * active_pfa, "crossings"),
        "tuning_bank_pfa": (0, "probability"),
        "held_out_pfa": (np.mean(np.sort(z0)[250:] > tuned), "probability"),
        "recovered_pfa": (np.mean(z0 > threshold), "probability"),
        "model_valid": (not broken, "boolean"),
    }
    plots = {
        "formation": _plot(
            "A signed matched sum forms each score",
            "Fast-time sample (index)",
            "Amplitude (relative)",
            [
                ("Template", np.arange(16), template),
                ("H0 record", np.arange(16), sigma * example0),
                ("H1 record", np.arange(16), template + sigma * example1),
            ],
        ),
        "roc": _plot(
            "Threshold sweeps at several matched-filter SNRs",
            "False-alarm probability (ratio)",
            "Detection probability (ratio)",
            [
                (f"{s:g} dB", np.r_[1, pfa, 0], np.r_[1, pd[i], 0])
                for i, s in enumerate(snrs)
            ],
        ),
        "threshold": _plot(
            "Same threshold: detections and false alarms",
            "Threshold (noise RMS)",
            "Probability (ratio)",
            [
                ("Empirical Pfa", gammas, pfa),
                ("Gaussian Pfa", gammas, ndtr(-gammas)),
                ("Selected SNR Pd", gammas, [np.mean(dp + z1 > g) for g in gammas]),
                ("Gaussian Pd", gammas, ndtr(dp - gammas)),
            ],
        ),
        "trial_pfa": _plot(
            "Rare events require enough opportunities",
            "Independent trials (count)",
            "Probability (ratio)",
            [
                ("Pfa", counts, trial_pfa),
                ("One-count resolution", counts, 1 / counts),
                ("Design", counts, np.full(4, ndtr(-threshold))),
            ],
        ),
        "trial_pd": _plot(
            "Finite-trial Pd with approximate 95% limits",
            "Independent trials (count)",
            "Detection probability (ratio)",
            [
                ("Measured", counts, trial_pd),
                ("Lower", counts, np.maximum(0, trial_pd - 1.96 * se)),
                ("Upper", counts, np.minimum(1, trial_pd + 1.96 * se)),
            ],
        ),
        "failure": _plot(
            "Cherry-picked tuning data cannot validate operational Pfa",
            "Bank: tuning, remaining, recovered (index)",
            "Pfa (ratio)",
            [("Crossings", [0, 1, 2], [0, 1, np.mean(z0 > threshold)])],
        ),
    }
    return _finish(
        values,
        plots,
        "The normalized signed matched-filter score is Gaussian: H0 has mean zero and H1 shifts by √SNR. Threshold sweeps trade Pd against Pfa, while trial count sets rare-event resolution.",
        "Selecting the 250 lowest H0 scores and placing a threshold at their maximum guarantees zero tuning crossings. The remaining bank crosses it: this selection-biased result cannot establish zero operational Pfa.",
        "Use the predetermined threshold and full independently generated H0/H1 banks. Disable the toggle for exact replay; finite Monte Carlo counts remain estimates.",
        4401,
        broken,
        trials=60000,
        pfa=pfa.tolist(),
        pd=pd.tolist(),
        trial_counts=counts.tolist(),
        trial_pfa=trial_pfa.tolist(),
        trial_pd=trial_pd.tolist(),
    )
