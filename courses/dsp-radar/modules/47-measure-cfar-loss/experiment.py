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


def _crossing(snr, raw, pd):
    curve = np.maximum.accumulate(raw)
    j = int(np.flatnonzero(curve >= pd)[0])
    if j == 0:
        raise ValueError("Pd crossing is not bracketed")
    value = snr[j - 1] + (pd - curve[j - 1]) * (snr[j] - snr[j - 1]) / (
        curve[j] - curve[j - 1]
    )
    return float(value), float(np.max(curve - raw))


def _pd_curve(scores, threshold):
    return np.array([np.mean(scores[:, j] > threshold) for j in range(scores.shape[1])])


def run(parameters):
    training, pfa, broken = _controls(
        parameters,
        [
            ("training_count", 16, [8, 16, 32, 64]),
            ("design_pfa", 0.001, [0.01, 0.001, 0.0001]),
        ],
    )
    n = int(training)
    trials = 50000
    rng = np.random.default_rng(4701)
    noise = (rng.normal(size=trials) + 1j * rng.normal(size=trials)) / np.sqrt(2)
    phase = np.exp(2j * np.pi * rng.random(trials))
    ns = np.array([8, 16, 32, 64])
    means = np.empty((trials, 4))
    for start in range(0, trials, 2000):
        ref = (
            rng.normal(size=(2000, 64)) + 1j * rng.normal(size=(2000, 64))
        ) / np.sqrt(2)
        acc = np.cumsum(abs(ref) ** 2, axis=1)
        means[start : start + 2000] = acc[:, ns - 1] / ns
        del ref, acc
    snrs = np.arange(3, 17.01, 0.5)
    h0 = abs(noise) ** 2
    h1 = np.empty((trials, len(snrs)))
    for index, snr in enumerate(snrs):
        h1[:, index] = abs(noise + phase * 10 ** (snr / 20)) ** 2
    del noise, phase
    known = -np.log(pfa)
    known_curve = _pd_curve(h1, known)
    known_snr, adjust = _crossing(snrs, known_curve, 0.8)
    curves = []
    loss = []
    measured_pfa = []
    adjustments = [adjust]
    for j, num in enumerate(ns):
        threshold = _alpha(num, pfa) * means[:, j]
        curve = _pd_curve(h1, threshold)
        cross, adj = _crossing(snrs, curve, 0.8)
        curves.append(curve)
        loss.append(cross - known_snr)
        adjustments.append(adj)
        measured_pfa.append(np.mean(h0 > threshold))
    index = int(np.flatnonzero(ns == n)[0])
    mean = means[:, index]
    alpha = known if broken else _alpha(n, pfa)
    threshold = alpha * mean
    active_curve = _pd_curve(h1, threshold)
    active_snr, active_adjust = _crossing(snrs, active_curve, 0.8)
    pfs = np.array([0.01, 0.001, 0.0001])
    pfa_loss = []
    for p in pfs:
        kcurve = _pd_curve(h1, -np.log(p))
        acurve = _pd_curve(h1, _alpha(n, p) * mean)
        pfa_loss.append(
            _crossing(snrs, acurve, 0.8)[0] - _crossing(snrs, kcurve, 0.8)[0]
        )
    values = {
        "known_noise_threshold": (known, "power"),
        "active_alpha": (alpha, "ratio"),
        "known_snr_at_pd80": (known_snr, "dB"),
        "active_snr_at_pd80": (active_snr, "dB"),
        "active_cfar_loss": (active_snr - known_snr, "dB"),
        "active_empirical_pfa": (np.mean(h0 > threshold), "probability"),
        "active_theoretical_pfa": ((1 + alpha / n) ** (-n), "probability"),
        "recovered_cfar_loss": (loss[index], "dB"),
        "reference_std": (np.std(mean), "power"),
        "maximum_monotone_adjustment": (
            max(adjustments + [active_adjust]),
            "probability",
        ),
        "model_valid": (not broken, "boolean"),
    }
    plots = {
        "thresholds": _plot(
            "Known background versus estimated threshold",
            "Trial (index)",
            "Power (relative)",
            [
                ("Known", np.arange(240), np.full(240, known)),
                ("Active CA", np.arange(240), threshold[:240]),
                ("10 dB CUT", np.arange(240), h1[:240, 14]),
            ],
        ),
        "pd": _plot(
            "Horizontal SNR cost at equal Pd and requested Pfa",
            "Input SNR (dB)",
            "Detection probability (ratio)",
            [
                ("Known background", snrs, known_curve),
                ("Selected detector", snrs, active_curve),
            ]
            + [(f"N={num}", snrs, curves[i]) for i, num in enumerate(ns)],
        ),
        "n_loss": _plot(
            "Finite reference-count loss",
            "Total training cells (count)",
            "Extra SNR at Pd=.8 (dB)",
            [("Measured", ns, loss)],
        ),
        "pfa_loss": _plot(
            "Pfa also changes the estimation cost",
            "Requested Pfa (probability)",
            "Extra SNR at Pd=.8 (dB)",
            [("Measured", pfs, pfa_loss)],
        ),
        "calibration": _plot(
            "The apparent free gain spends false alarms",
            "Total training cells (count)",
            "Actual homogeneous Pfa (probability)",
            [
                ("Finite-N design", ns, np.full(4, pfa)),
                ("Known-noise multiplier reused", ns, (1 + known / ns) ** (-ns)),
                ("Measured proper calibration", ns, measured_pfa),
            ],
        ),
    }
    plots["estimate_spread"] = _plot(
        "More independent references reduce mean-power uncertainty",
        "Total training cells (count)",
        "Reference-mean standard deviation (power)",
        [
            ("Measured", ns, np.std(means, axis=0)),
            ("IID exponential model", ns, 1 / np.sqrt(ns)),
        ],
    )
    return _finish(
        values,
        plots,
        "CFAR loss is a horizontal SNR difference at the same Pd and Pfa. Finite reference counts make the threshold uncertain; the disclosed monotone envelope only permits inversion of finite-trial curves.",
        "Reusing −ln(Pfa) on an estimated mean gives a smaller apparent SNR penalty by increasing actual false alarms. It is not an equal-Pfa comparison.",
        "Restore N(Pfa^(−1/N)−1), keep paired CUT trials and independent references, and compare at Pd=.8. Disable the toggle to reproduce the properly calibrated selected curve.",
        4701,
        broken,
        trials=trials,
        raw_pd=active_curve.tolist(),
        known_raw_pd=known_curve.tolist(),
        training_loss_db=loss,
        pfa_loss_db=pfa_loss,
        monotone_adjustment=max(adjustments + [active_adjust]),
    )
