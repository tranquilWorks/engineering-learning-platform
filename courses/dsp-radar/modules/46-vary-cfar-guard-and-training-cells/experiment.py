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


def _refs(length, t, g):
    cuts = np.arange(t + g, length - t - g)
    offsets = np.r_[np.arange(-t - g, -g), np.arange(g + 1, g + t + 1)]
    return cuts, cuts[:, None] + offsets


def _ca(power, t, g, p, geometric=False):
    cuts, refs = _refs(len(power), t, g)
    samples = power[refs]
    estimate = (
        np.exp(np.mean(np.log(np.maximum(samples, 1e-300)), axis=1))
        if geometric
        else np.mean(samples, axis=1)
    )
    threshold = _alpha(2 * t, p) * estimate
    return cuts, threshold, power[cuts] > threshold, estimate


def run(parameters):
    guard, training, broken = _controls(
        parameters,
        [("guard_cells", 4, [0, 4, 10]), ("training_cells", 12, [4, 12, 36])],
    )
    g, t = int(guard), int(training)
    cells = np.arange(1, 257)
    mean = 0.75 + 0.003 * cells + 2.8 / (1 + np.exp(-(cells - 178) / 5.5))
    rng = np.random.default_rng(4601)
    noise = np.sqrt(mean / 2) * (rng.normal(size=256) + 1j * rng.normal(size=256))
    received = noise.copy()
    offsets = np.arange(-18, 19)
    response = np.sinc(offsets / 5)
    strong = 87
    weak = 137
    signal = np.sqrt(mean[strong] * 10**3.5) * np.exp(0.4j) * response
    received[strong + offsets] += signal
    received[weak] += np.sqrt(mean[weak] * 10**1.8) * np.exp(-0.7j)
    power = abs(received) ** 2
    target_power = np.zeros(256)
    target_power[strong + offsets] = abs(signal) ** 2
    target_power[weak] = mean[weak] * 10**1.8
    cuts, threshold, _det, _ = _ca(power, t, g, 0.001)
    guards = np.array([0, 4, 10])
    margins = []
    leak = []
    for v in guards:
        cc, tt, _, _ = _ca(power, 12, int(v), 0.001)
        _, refs = _refs(256, 12, int(v))
        margins.append(power[strong] / tt[strong - cc[0]])
        leak.append(np.mean(target_power[refs[strong - cc[0]]]))
    trains = np.array([4, 12, 36])
    rough = []
    locality = []
    for v in trains:
        cc, _, _, est = _ca(abs(noise) ** 2, int(v), 6, 0.001)
        _, refs = _refs(256, int(v), 6)
        expected = mean[refs].mean(axis=1)
        quiet = np.arange(69, 100) - cc[0]
        edge = np.arange(164, 190) - cc[0]
        rough.append(np.mean(abs(np.diff(est[quiet]))) / np.mean(mean[69:100]))
        locality.append(np.mean(abs(expected[edge] / mean[164:190] - 1)))
    contaminated = received.copy()
    contaminated[125] += np.sqrt(mean[125] * 10**3.2) * np.exp(1.1j)
    bad_power = abs(contaminated) ** 2
    bc, bt, bd, _ = _ca(bad_power, 12, 4, 0.001)
    rc, rt, rd, _ = _ca(bad_power, 12, 12, 0.001)
    active_weak = (
        (bad_power[weak] / bt[weak - bc[0]])
        if broken
        else power[weak] / threshold[weak - cuts[0]]
    )
    values = {
        "window_span": ((2 * (t + g) + 1) * 15, "m"),
        "excluded_edges": (2 * (t + g), "cells"),
        "strong_target_margin": (power[strong] / threshold[strong - cuts[0]], "ratio"),
        "active_weak_margin": (active_weak, "ratio"),
        "contaminated_weak_margin": (bad_power[weak] / bt[weak - bc[0]], "ratio"),
        "recovered_weak_margin": (bad_power[weak] / rt[weak - rc[0]], "ratio"),
        "weak_power_change": (bad_power[weak] - power[weak], "power"),
        "small_guard_leakage": (leak[0], "power"),
        "large_guard_leakage": (leak[-1], "power"),
        "small_window_locality_error": (locality[0], "ratio"),
        "large_window_locality_error": (locality[-1], "ratio"),
        "model_valid": (not broken, "boolean"),
    }
    plots = {
        "profile": _plot(
            "Guard and training geometry in a changing background",
            "Range (m)",
            "Power (relative)",
            [
                ("Observed", 15 * (cells - 1), power),
                ("Selected threshold", 15 * cuts, threshold),
            ],
        ),
        "response": _plot(
            "Sampled-sinc mainlobe and sidelobes",
            "Offset (cells)",
            "Target amplitude (normalized)",
            [("Response", offsets, response)],
        ),
        "guards": _plot(
            "Guard width reduces target leakage into references",
            "Guard cells per side (count)",
            "Power or margin (relative)",
            [
                ("Reference target power", guards, leak),
                ("CUT / threshold", guards, margins),
            ],
        ),
        "training": _plot(
            "Larger training windows trade variance for locality",
            "Training cells per side (count)",
            "Normalized error (ratio)",
            [
                ("Estimate roughness", trains, rough),
                ("Expected locality error", trains, locality),
            ],
        ),
        "contamination": _plot(
            "The same weak CUT can be masked by its neighbor",
            "Range (m)",
            "Power (relative)",
            [
                ("Contaminated scene", 15 * (cells - 1), bad_power),
                ("G=4 masked", 15 * bc, bt),
                ("G=12 recovery", 15 * rc, rt),
            ],
        ),
    }
    return _finish(
        values,
        plots,
        "Guards exclude target response; training cells estimate background. Larger windows can smooth fluctuations while mixing different background powers. Inspect leakage, locality and excluded edges together.",
        "The named failure injects the source neighbor at cell 126 into the weak cell 138 reference window (T=12,G=4). Its CUT power is unchanged while its threshold rises.",
        "At the same contaminated scene, use G=12 and T=12 to exclude that neighbor and recover the weak target. This consumes more edge cells. Disable the toggle to restore the selected uncontaminated baseline.",
        4601,
        broken,
        guard_margins=margins,
        guard_leakage=leak,
        training_roughness=rough,
        training_locality_error=locality,
        recovered_weak_detected=bool(rd[weak - rc[0]]),
        broken_weak_detected=bool(bd[weak - bc[0]]),
    )
