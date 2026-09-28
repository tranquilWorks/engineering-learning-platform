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


def _uniform(seed, count, offset=0.5):
    states = np.empty(count)
    state = int(seed)
    for k in range(count):
        state = (16807 * state) % 2147483647
        states[k] = (state + offset) / 2147483647
    return states


def _normal(seed, count, offset=0.5):
    u = _uniform(seed, 2 * ((count + 1) // 2), offset)
    radius = np.sqrt(-2 * np.log(u[::2]))
    phase = 2 * np.pi * u[1::2]
    return np.column_stack([radius * np.cos(phase), radius * np.sin(phase)]).ravel()[
        :count
    ]


def _greedy(cost, valid):
    working = np.where(valid, cost, np.inf).copy()
    assignment = np.full(cost.shape[0], -1, dtype=int)
    for _ in range(min(cost.shape)):
        flat = int(np.argmin(working.ravel(order="F")))
        i, j = np.unravel_index(flat, working.shape, order="F")
        if not np.isfinite(working[i, j]):
            break
        assignment[i] = j
        working[i, :] = np.inf
        working[:, j] = np.inf
    return assignment


def _complex_noise(seed, rows, columns):
    u = _uniform(seed, 2 * rows * columns)
    z = np.sqrt(-np.log(u[::2])) * np.exp(2j * np.pi * u[1::2])
    return z.reshape(columns, rows).T


def _weights(squint):
    m = np.arange(12)
    weights = (
        np.exp(1j * np.pi * m[:, None] * np.sin(np.deg2rad([-squint, squint]))) / 12
    )
    phase = np.exp(-1j * np.angle(weights.conj().sum(axis=0)))
    return weights, phase


def _patterns(squint, angles):
    weights, phase = _weights(squint)
    a = np.exp(1j * np.pi * np.arange(12)[:, None] * np.sin(np.deg2rad(angles)))
    return (weights.conj().T @ a) * phase[:, None]


def _estimate(squint, snr, angles, noise):
    left, right = _patterns(squint, angles)
    summed = (right + left) / 2
    ratio = np.real((right - left) / (right + left))
    mask = abs(angles) <= 4 + 1e-10
    grid = angles[mask]
    calibration = ratio[mask]
    if not np.all(np.diff(calibration) > 0):
        raise ValueError("Monopulse calibration must be strictly monotonic")
    if min(abs(summed[mask])) <= 0.15:
        raise ValueError("Calibration leaves the reviewed sum-channel guard")
    signal = np.exp(1j * np.pi * np.arange(12) * np.sin(np.deg2rad(2)) + 0.4j)
    data = signal[:, None] + 10 ** (-snr / 20) * noise[:12]
    weights, phase = _weights(squint)
    l, r = (weights.conj().T @ data) * phase[:, None]
    sigma = (r + l) / 2
    delta = (r - l) / 2
    valid = abs(sigma) >= 0.15
    samples = np.real(delta / sigma)
    estimates = np.interp(samples[valid], calibration, grid)
    mean_ratio = float(np.real(delta.mean() / sigma.mean()))
    if abs(sigma.mean()) < 0.15 or not np.any(valid):
        raise ValueError("Insufficient sum-channel support")
    estimate = float(np.interp(mean_ratio, calibration, grid))
    rmse = float(np.sqrt(np.mean((estimates - 2) ** 2)))
    clipped = int(
        np.sum((samples[valid] < calibration[0]) | (samples[valid] > calibration[-1]))
    )
    return {
        "left": left,
        "right": right,
        "ratio": ratio,
        "calibration": calibration,
        "grid": grid,
        "estimate": estimate,
        "rmse": rmse,
        "valid": valid,
        "samples": samples,
        "estimates": estimates,
        "clipped": clipped,
        "mean_ratio": mean_ratio,
        "sum_magnitude": abs(sigma),
    }


def run(parameters):
    squint, snr, broken = _controls(
        parameters,
        [("beam_squint_deg", 3, [1.5, 3, 5]), ("receiver_snr_db", 15, [-5, 5, 15, 25])],
    )
    angles = np.linspace(-10, 10, 401)
    noise = _complex_noise(6401, 16, 256)
    baseline = _estimate(squint, snr, angles, noise)
    left, right = baseline["left"], baseline["right"]
    sum_pattern = (right + left) / 2
    difference = (right - left) / 2
    zero = 200
    ratio_bad = float(
        np.real((1.12 * right[zero] - left[zero]) / (1.12 * right[zero] + left[zero]))
    )
    bad_estimate = float(
        np.interp(ratio_bad, baseline["calibration"], baseline["grid"])
    )
    fixed_ratio = float(
        np.real(
            (1.12 * right[zero] / 1.12 - left[zero])
            / (1.12 * right[zero] / 1.12 + left[zero])
        )
    )
    fixed_estimate = float(
        np.interp(fixed_ratio, baseline["calibration"], baseline["grid"])
    )
    slopes = []
    strengths = []
    for q in [1.5, 3, 5]:
        l, r = _patterns(q, np.array([-1.0, 0, 1.0]))
        ratio = np.real((r - l) / (r + l))
        slopes.append(float((ratio[2] - ratio[0]) / 2))
        strengths.append(float(abs((r[1] + l[1]) / 2)))
    snr_results = [_estimate(squint, s, angles, noise) for s in [-5, 5, 15, 25]]
    active_estimate = bad_estimate if broken else baseline["estimate"]
    active_truth = 0 if broken else 2
    values = {
        "model_valid": (not broken, "boolean"),
        "active_angle_estimate": (active_estimate, "deg"),
        "active_angle_error": (active_estimate - active_truth, "deg"),
        "snapshot_rmse": (baseline["rmse"], "deg"),
        "valid_snapshots": (np.sum(baseline["valid"]), "snapshots"),
        "clipped_valid_snapshots": (baseline["clipped"], "snapshots"),
        "coherent_ratio": (baseline["mean_ratio"], "ratio"),
        "gain_mismatch_boresight_bias": (bad_estimate, "deg"),
        "calibrated_boresight_error": (fixed_estimate, "deg"),
        "local_comparator_slope": (
            (baseline["ratio"][220] - baseline["ratio"][180]) / 2,
            "1/deg",
        ),
        "boresight_sum": (abs(sum_pattern[zero]), "voltage"),
    }
    corrupted = np.real((1.12 * right - left) / (1.12 * right + left))
    calmask = abs(angles) <= 4 + 1e-10
    plots = {
        "beams": _plot(
            "Phase-aligned left/right beams and sum/difference",
            "Angle from boresight (deg)",
            "Normalized voltage magnitude (ratio)",
            [
                ("|L|", angles, abs(left)),
                ("|R|", angles, abs(right)),
                ("|Sigma|", angles, abs(sum_pattern)),
                ("|Delta|", angles, abs(difference)),
            ],
        ),
        "calibration": _plot(
            "Signed comparator within the calibrated sector",
            "Angle from boresight (deg)",
            "Real Delta/Sigma (ratio)",
            [
                ("Nominal", angles[calmask], baseline["ratio"][calmask]),
                ("1.12 right gain", angles[calmask], corrupted[calmask]),
                ("Inverse-gain recovery", angles[calmask], baseline["ratio"][calmask]),
            ],
        ),
        "estimates": _plot(
            "Guarded snapshots: estimates clip at calibration limits",
            "Snapshot (index)",
            "Estimated target angle (deg)",
            [
                (
                    "Valid snapshots",
                    np.flatnonzero(baseline["valid"]) + 1,
                    baseline["estimates"],
                )
            ],
        ),
        "sum_guard": _plot(
            "Snapshot validity depends on sum-channel magnitude",
            "Snapshot (index)",
            "Sum voltage magnitude (ratio)",
            [
                ("|Sigma|", np.arange(1, 257), baseline["sum_magnitude"]),
                ("Guard", np.arange(1, 257), np.full(256, 0.15)),
            ],
        ),
        "squint_slope": _plot(
            "Larger squint steepens the comparator",
            "Beam squint (deg)",
            "Local comparator slope (1/deg)",
            [("Finite +/-1 degree slope", [1.5, 3, 5], slopes)],
        ),
        "squint_sum": _plot(
            "Larger squint reduces boresight sum",
            "Beam squint (deg)",
            "Boresight sum voltage (ratio)",
            [("|Sigma(0)|", [1.5, 3, 5], strengths)],
        ),
        "snr": _plot(
            "Same receiver-noise samples at each SNR",
            "Receiver SNR (dB)",
            "Valid-snapshot angle RMSE (deg)",
            [
                (
                    "Clipped calibrated estimates",
                    [-5, 5, 15, 25],
                    [x["rmse"] for x in snr_results],
                )
            ],
        ),
    }
    plots["estimates"]["data"][0]["mode"] = "markers"
    return _finish(
        values,
        plots,
        "Phase-align squinted receive beams at boresight, form Sigma and Delta, and invert a monotone local ratio calibration. The sum guard, valid count and clipping count expose the estimator limits.",
        "Unknown right-channel gain 1.12 gives a nonzero angle for a noiseless boresight target. This named mismatch scene is separate from the selected noisy 2-degree target.",
        "Divide the right channel by the measured gain on unchanged boresight data. Disable the toggle for exact selected noisy-scene recovery. Calibration is local to +/-4 degrees; clipping is not evidence of accuracy outside that sector.",
        6401,
        broken,
        valid_samples=baseline["valid"].tolist(),
        squint_slopes=slopes,
        squint_boresight_sum=strengths,
        snr_sweep_rmse=[x["rmse"] for x in snr_results],
        snr_sweep_valid=[int(x["valid"].sum()) for x in snr_results],
        snr_sweep_clipped=[x["clipped"] for x in snr_results],
        snapshots=256,
        calibration_limit_deg=4,
        sum_guard=0.15,
    )
