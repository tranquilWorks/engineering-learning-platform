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
    rcs, power, broken = _controls(
        parameters,
        [("rcs_m2", 1, [0.1, 1, 10]), ("transmit_power_kw", 100, [25, 100, 400])],
    )
    ranges = np.arange(1, 120.5, 0.5)
    noise = 1.380649e-23 * 290 * 1e6 * 10**0.4
    numerator = (
        power * 1000 * 10**7 * (C / 1e10) ** 2 * rcs / ((4 * np.pi) ** 3 * 10**0.6)
    )
    received = numerator / (ranges * 1000) ** 4
    reference = numerator / (40000**4)
    wrong = reference * (40 / ranges) ** 2
    active = wrong if broken else received
    threshold = noise * 10**1.3
    rng = np.random.default_rng(2901)
    samples = np.sqrt(noise / 2) * (rng.normal(size=4096) + 1j * rng.normal(size=4096))
    max_range = (numerator / threshold) ** 0.25 / 1000
    dbm = lambda x: 10 * np.log10(x) + 30
    gains = np.array([1, 2, 10**0.3, 10**0.3, 4, 2, 2])
    values = {
        "reference_echo": (dbm(reference), "dBm"),
        "noise_floor": (dbm(noise), "dBm"),
        "measured_noise": (dbm(np.mean(abs(samples) ** 2)), "dBm"),
        "reference_margin": (dbm(reference) - dbm(threshold), "dB"),
        "threshold_range": (max_range, "km"),
        "active_decade_slope": ((-20 if broken else -40), "dB/decade"),
        "range_doubling_cost": (10 * np.log10(16), "dB"),
        "power_required_to_double_range": (16, "ratio"),
        "active_power_at_100km": (dbm(active[198]), "dBm"),
        "model_valid": (not broken, "boolean"),
    }
    plots = {
        "power": _plot(
            "Two spreading trips",
            "Range (km)",
            "Received power (dBm)",
            [
                ("R^-4", ranges, dbm(received)),
                ("Active model", ranges, dbm(active)),
                ("Threshold", ranges, np.full(len(ranges), dbm(threshold))),
            ],
        ),
        "margin": _plot(
            "Detection margin is a power criterion",
            "Range (km)",
            "Margin (dB)",
            [("Selected", ranges, dbm(received) - dbm(threshold))],
        ),
        "rcs_sweep": _plot(
            "Change only RCS",
            "Range (km)",
            "Power (dBm)",
            [(f"RCS {v} m²", ranges, dbm(received * v / rcs)) for v in [0.1, 1, 10]],
        ),
        "frequency_sweep": _plot(
            "Frequency at fixed antenna gains",
            "Range (km)",
            "Power (dBm)",
            [(f"{f} GHz", ranges, dbm(received * (10 / f) ** 2)) for f in [3, 10, 30]],
        ),
        "power_sweep": _plot(
            "Fourth-root range growth",
            "Transmit power (kW)",
            "Threshold range (km)",
            [
                (
                    "Range",
                    [25, 100, 400],
                    max_range * (np.array([25, 100, 400]) / power) ** 0.25,
                )
            ],
        ),
        "sensitivity": _plot(
            "0 baseline; 1 Pt×2; 2 Gt+3; 3 Gr+3; 4 wavelength×2; 5 loss/2; 6 RCS×2",
            "Budget case (index)",
            "Margin change (dB)",
            [("One variable", np.arange(7), 10 * np.log10(gains))],
        ),
    }
    return _finish(
        values,
        plots,
        "Echo power follows Pt Gt Gr λ² σ / ((4π)³ R⁴ L); noise follows kTBF. Positive margin is not detection probability.",
        "The anchored R^-2 model agrees at 40 km but loses only 20 dB per decade. It omits one propagation trip.",
        "Disable the failure to restore R^-4 and the same private noise bank.",
        2901,
        broken,
        noise_sample_count=4096,
    )
