from __future__ import annotations

import numpy as np

C = 299792458.0


def _plot(title, x_label, y_label, traces):
    data = []
    for name, x, y in traces:
        x, y = np.asarray(x), np.asarray(y)
        i = np.unique(np.linspace(0, len(x) - 1, min(512, len(x))).astype(int))
        data.append(
            {
                "type": "scatter",
                "mode": "lines",
                "name": name,
                "x": x[i].tolist(),
                "y": y[i].tolist(),
            }
        )
    return {
        "data": data,
        "layout": {
            "title": {"text": title},
            "xaxis": {"title": x_label},
            "yaxis": {"title": y_label},
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


def run(parameters):
    prf_khz, true_km, broken = _controls(
        parameters,
        [("prf_khz", 20, [10, 15, 20, 25]), ("true_range_km", 18, [3, 8, 18])],
    )
    prf = prf_khz * 1000
    true = true_km * 1000
    ru = C / (2 * prf)
    order = int(np.floor(true / ru))
    apparent = true - order * ru
    samples = round(20e6 / prf)
    count = 6 * samples
    delay = round(2 * true / C * 20e6)
    rng = np.random.default_rng(3501)
    noise = 0.004 / np.sqrt(2) * (rng.normal(size=count) + 1j * rng.normal(size=count))
    receive = noise.copy()
    transmit = np.zeros(count)
    for pulse in range(6):
        start = pulse * samples
        transmit[start : start + 40] = 1
        start += delay
        if start < count:
            receive[start : min(start + 40, count)] += 0.7
    measured = (delay - order * samples) * C / 40e6
    active = true if broken else apparent
    ps = np.array([10, 15, 20, 25])
    r = np.linspace(0, 3 * ru, 601)
    curve = np.linspace(8, 30, 221)
    values = {
        "unambiguous_range": (ru / 1000, "km"),
        "ambiguity_order": (order, "count"),
        "apparent_range": (apparent / 1000, "km"),
        "active_reported_range": (active / 1000, "km"),
        "sampled_apparent_range": (measured / 1000, "km"),
        "round_trip_delay": (2 * true / C * 1e6, "µs"),
        "below_boundary": ((ru - 25) / 1000, "km"),
        "above_boundary": (0.025, "km"),
        "receiver_noise_power": (np.mean(abs(noise) ** 2), "relative power"),
        "model_valid": (not broken, "boolean"),
    }
    start = order * samples
    fast = np.arange(samples) * C / 40e6 / 1000
    plots = {
        "timeline": _plot(
            "Echoes arrive after later transmissions",
            "Time (µs)",
            "Amplitude (relative)",
            [
                ("Transmit", np.arange(count) / 20, transmit),
                ("Received", np.arange(count) / 20, abs(receive)),
            ],
        ),
        "folded": _plot(
            "The listening interval lacks the original pulse label",
            "Apparent range (km)",
            "Received magnitude (relative)",
            [("Listening interval", fast, abs(receive[start : start + samples]))],
        ),
        "prf_sweep": _plot(
            "PRF changes both folding interval and apparent range",
            "PRF (kHz)",
            "Range (km)",
            [
                ("Unambiguous", curve, C / (2 * curve * 1000) / 1000),
                ("Apparent", curve, np.mod(true, C / (2 * curve * 1000)) / 1000),
                ("Probes", ps, np.mod(true, C / (2 * ps * 1000)) / 1000),
            ],
        ),
        "range_sweep": _plot(
            "True range folds modulo the unambiguous interval",
            "True range (km)",
            "Apparent range (km)",
            [("Folded", r / 1000, np.mod(r, ru) / 1000)],
        ),
        "report": _plot(
            "Pulse identity assumption changes the answer",
            "Method: true, apparent, active (index)",
            "Range (km)",
            [("Report", [0, 1, 2], [true_km, apparent / 1000, active / 1000])],
        ),
    }
    return _finish(
        values,
        plots,
        "PRI=1/PRF and Ru=c/(2 PRF). Six explicit pulses show how a distant echo is assigned to the current listening interval.",
        "The failure uses the transmitted pulse's true identity even though this receiver cannot observe it, reporting true range as unambiguous.",
        "Disable the failure to restore delay modulo PRI and the same seeded receive train. This diagnoses ambiguity; it does not recover true range.",
        3501,
        broken,
        timeline_samples=count,
    )
