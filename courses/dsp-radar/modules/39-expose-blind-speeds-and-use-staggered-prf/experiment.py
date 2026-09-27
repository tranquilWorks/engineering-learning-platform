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
    secondary, velocity_multiple, broken = _controls(
        parameters,
        [
            ("secondary_prf_khz", 5.3, [4, 4.2, 4.5, 4.9, 5.3, 5.7, 6.2]),
            ("primary_blind_speed_multiple", 1, [0, 0.5, 1, 1.5, 2]),
        ],
    )
    wavelength = C / 1e10
    velocity = velocity_multiple * wavelength * 4000 / 2
    fd = 2 * velocity / wavelength
    k = np.arange(32)
    active_secondary = 4000 if broken else secondary * 1000
    rng = np.random.default_rng(3901)
    clean = []
    observed = []
    gains = []
    for prf in [4000, active_secondary]:
        s = np.exp(1j * (np.deg2rad(20) + 2 * np.pi * fd * k / prf))
        noise = 0.02 / np.sqrt(2) * (rng.normal(size=32) + 1j * rng.normal(size=32))
        clean.append(s)
        observed.append(s + noise)
        gains.append(np.sqrt(np.mean(abs(np.diff(s)) ** 2)) / 2)
    velocity_axis = np.linspace(-150, 150, 2401)
    doppler = 2 * velocity_axis / wavelength
    response1 = abs(1 - np.exp(-2j * np.pi * doppler / 4000)) / 2
    response2 = abs(1 - np.exp(-2j * np.pi * doppler / active_secondary)) / 2
    fused = np.maximum(response1, response2)
    recovered = max(abs(np.sin(np.pi * fd / 4000)), abs(np.sin(np.pi * fd / 5300)))
    values = {
        "target_velocity": (velocity, "m/s"),
        "target_doppler": (fd, "Hz"),
        "primary_normalized_gain": (gains[0], "ratio"),
        "active_secondary_gain": (gains[1], "ratio"),
        "active_fused_gain": (max(gains), "ratio"),
        "diverse_5300_gain": (recovered, "ratio"),
        "active_detection": (max(gains) >= 0.3, "boolean"),
        "active_secondary_prf": (active_secondary, "Hz"),
        "stationary_fused_gain": (0, "ratio"),
        "observed_secondary_rms": (
            np.sqrt(np.mean(abs(np.diff(observed[1])) ** 2)) / 2,
            "relative",
        ),
        "model_valid": (not broken, "boolean"),
    }
    ps = np.array([4, 4.2, 4.5, 4.9, 5.3, 5.7, 6.2])
    pg = abs(np.sin(np.pi * fd / (ps * 1000)))
    plots = {
        "phasors": _plot(
            "Separate coherent dwells use different pulse intervals",
            "Pulse (index)",
            "Phase modulo one turn (rad)",
            [
                ("Primary", k, np.angle(clean[0])),
                ("Active secondary", k, np.angle(clean[1])),
            ],
        ),
        "differences": _plot(
            "A blind target repeats its phasor",
            "Difference (index)",
            "Canceller magnitude (relative)",
            [
                ("Primary", k[1:], abs(np.diff(observed[0]))),
                ("Secondary", k[1:], abs(np.diff(observed[1]))),
            ],
        ),
        "velocity_response": _plot(
            "Noncoherent maximum combines two normalized gains",
            "Velocity (m/s)",
            "Normalized amplitude (ratio)",
            [
                ("Primary", velocity_axis, response1),
                ("Secondary", velocity_axis, response2),
                ("Fused", velocity_axis, fused),
            ],
        ),
        "coverage": _plot(
            "Illustrative threshold 0.30",
            "Velocity (m/s)",
            "Threshold decision (boolean)",
            [
                ("Primary", velocity_axis, (response1 >= 0.3).astype(float)),
                ("Fused OR", velocity_axis, (fused >= 0.3).astype(float)),
            ],
        ),
        "prf_sweep": _plot(
            "Diversity moves a blind-speed null",
            "Secondary PRF (kHz)",
            "Normalized amplitude (ratio)",
            [("Target", ps, pg)],
        ),
    }
    return _finish(
        values,
        plots,
        "A two-pulse canceller nulls fd=m PRF. Separate 4.0 and 5.3 kHz dwells move nonzero blind speeds; their normalized magnitudes are fused by maximum, not complex addition.",
        "Using 4.0 kHz twice duplicates the same blind-speed holes. A repeated observation supplies no PRF diversity.",
        "Disable the failure and select 5.3 kHz for the primary first-blind-speed target. The zero-velocity null and possible shared nonzero nulls remain.",
        3901,
        broken,
        pulse_count=32,
    )
