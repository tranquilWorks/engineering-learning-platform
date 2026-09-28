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


def _uniform(seed, count):
    state = int(seed)
    out = np.empty(count)
    for i in range(count):
        state = (16807 * state) % 2147483647
        out[i] = state / 2147483647
    return out


def _noise(seed, rows, columns=1, interleaved=False):
    count = rows * columns
    u = _uniform(seed, 2 * count)
    first, second = (u[::2], u[1::2]) if interleaved else (u[:count], u[count:])
    return (np.sqrt(-np.log(first)) * np.exp(2j * np.pi * second)).reshape(
        (rows, columns), order="F"
    )


def _db(power, floor=-80, relative=False):
    x = np.asarray(power)
    if relative:
        x = x / np.max(x)
    return 10 * np.log10(np.maximum(x, 10 ** (floor / 10)))


def _steer(angles, count, sign=1):
    return np.exp(
        sign
        * 1j
        * np.pi
        * np.arange(count)[:, None]
        * np.sin(np.deg2rad(np.atleast_1d(angles)))
    )


def _cov(data):
    r = data @ data.conj().T / data.shape[1]
    return (r + r.conj().T) / 2


def _mvdr(r, a, alpha):
    loaded = r + alpha * np.trace(r).real / len(r) * np.eye(len(r))
    if 1 / np.linalg.cond(loaded, 1).real < 1e-12:
        raise ValueError("Covariance solve refused: insufficient regularization")
    u = np.linalg.solve(loaded, a)
    return u / np.vdot(a, u)


def _peaks(power, angles, count=2, separation=1):
    ix = np.flatnonzero((power[1:-1] > power[:-2]) & (power[1:-1] >= power[2:])) + 1
    selected = []
    for k in sorted(ix, key=lambda k: (-power[k], k)):
        if all(abs(angles[k] - angles[j]) >= separation for j in selected):
            selected.append(k)
            if len(selected) == count:
                break
    return np.sort(angles[selected])


def _width(axis, power):
    i = int(np.argmax(power))
    left = right = i
    level = power[i] / 2
    while left > 0 and power[left] >= level:
        left -= 1
    while right < len(power) - 1 and power[right] >= level:
        right += 1
    if left == 0 or right == len(power) - 1:
        raise ValueError("Half-power crossing is outside the retained axis")
    lo = axis[left] + (level - power[left]) * (axis[left + 1] - axis[left]) / (
        power[left + 1] - power[left]
    )
    hi = axis[right - 1] + (level - power[right - 1]) * (
        axis[right] - axis[right - 1]
    ) / (power[right] - power[right - 1])
    return hi - lo


CONTROLS = [
    ("source_separation_deg", 6, [2, 6, 12]),
    ("source_snr_db", 10, [-10, 0, 10]),
]


def _spectra(x, grid, count=2):
    r = _cov(x)
    e, v = np.linalg.eigh(r)
    a = _steer(grid, len(r))
    en = v[:, : len(r) - count]
    bart = np.real(np.sum(a.conj() * (r @ a), axis=0)) / len(r) ** 2
    music = 1 / np.maximum(np.sum(abs(en.conj().T @ a) ** 2, axis=0), 1e-30)
    return _db(bart, -60, True), _db(music, -60, True), e[::-1]


def _angle_error(peaks, truth):
    # Missing peaks are counted separately; finite scan-span penalty is explicit.
    return (
        float(np.sqrt(np.mean((peaks - truth) ** 2)))
        if len(peaks) == len(truth)
        else 80.0
    )


def run(parameters):
    separation, snr, broken = _controls(parameters, CONTROLS)
    grid = np.linspace(-40, 40, 801)
    truth = np.array([-separation / 2, separation / 2])
    a = _steer(truth, 10)
    waves = np.array([np.exp(2j * np.pi * _uniform(s, 512)) for s in [6601, 6602]])
    noise = _noise(6603, 10, 512)
    x = 10 ** (snr / 20) * a @ waves + noise
    bart, music, eig = _spectra(x, grid)
    coherent = (
        10 ** (snr / 20) * a @ np.array([waves[0], np.exp(0.7j) * waves[0]]) + noise
    )
    _cb, cm, ce = _spectra(coherent, grid)
    # Concatenating the four overlapping subarrays gives their mean covariance.
    smoothed = np.concatenate([coherent[k : k + 7] for k in range(4)], axis=1)
    _, sm, se = _spectra(smoothed, grid)
    active = cm if broken else music
    peaks = _peaks(active, grid)
    recpeaks = _peaks(sm, grid)
    midpoint = np.argmin(abs(grid))
    ti = np.array([np.argmin(abs(grid - t)) for t in truth])
    sep = np.array([2, 3, 4, 5, 6, 8, 10, 12])
    sepcontrast = []
    seperror = []
    for d in sep:
        _, m, _ = _spectra(
            10 ** (snr / 20) * _steer([-d / 2, d / 2], 10) @ waves + noise, grid
        )
        sepcontrast.append(
            float(min(np.interp([-d / 2, d / 2], grid, m)) - m[midpoint])
        )
        seperror.append(_angle_error(_peaks(m, grid), np.array([-d / 2, d / 2])))
    snrs = np.array([-10, -5, 0, 5, 10, 15])
    snrerror = [
        _angle_error(
            _peaks(_spectra(10 ** (s / 20) * a @ waves + noise, grid)[1], grid), truth
        )
        for s in snrs
    ]
    ns = np.array([16, 32, 64, 128, 256, 512])
    prefix = a @ waves + noise
    nerror = [
        _angle_error(_peaks(_spectra(prefix[:, :n], grid)[1], grid), truth) for n in ns
    ]
    counts = [1, 2, 3, 4]
    countcurves = [_spectra(x, grid, k)[1] for k in counts]
    values = {
        "angle_rmse": (_angle_error(peaks, truth), "deg"),
        "detected_peaks": (len(peaks), "count"),
        "first_peak": (peaks[0] if len(peaks) else 0, "deg"),
        "second_peak": (peaks[-1] if len(peaks) else 0, "deg"),
        "music_contrast": (min(music[ti]) - music[midpoint], "dB"),
        "bartlett_contrast": (min(bart[ti]) - bart[midpoint], "dB"),
        "coherent_gap": (10 * np.log10(ce[1] / ce[2]), "dB"),
        "smoothed_gap": (10 * np.log10(se[1] / se[2]), "dB"),
        "smoothed_rmse": (_angle_error(recpeaks, truth), "deg"),
        "low_snr_rmse": (snrerror[0], "deg"),
        "short_record_rmse": (nerror[0], "deg"),
        "model_valid": (not broken, "boolean"),
    }
    plots = {
        "eigenvalues": _plot(
            "Signal/noise eigenvalue split",
            "Descending mode (index)",
            "Eigenvalue (dB)",
            [
                (label, np.arange(len(e)), _db(e))
                for label, e in [
                    ("Independent", eig),
                    ("Coherent", ce),
                    ("Smoothed", se),
                ]
            ],
        ),
        "spectrum": _plot(
            "Conventional beam versus MUSIC",
            "Angle (deg)",
            "Normalized power (dB)",
            [
                ("Bartlett", grid, bart),
                ("Selected MUSIC", grid, active),
                ("Smoothed coherent record", grid, sm),
            ],
        ),
        "separation": _plot(
            "Two-source contrast at fixed noise",
            "Source separation (deg)",
            "Truth-to-midpoint contrast (dB)",
            [("MUSIC", sep, sepcontrast)],
        ),
        "snr": _plot(
            "Fixed scene SNR sweep",
            "SNR (dB)",
            "Matched angle RMSE (deg)",
            [("MUSIC", snrs, snrerror)],
        ),
        "snapshots": _plot(
            "Nested prefixes of a 0 dB record",
            "Snapshots (count)",
            "Matched angle RMSE (deg)",
            [("MUSIC", ns, nerror)],
        ),
        "count": _plot(
            "Assumed source count changes the noise subspace",
            "Angle (deg)",
            "Normalized MUSIC power (dB)",
            [(str(k) + " assumed", grid, m) for k, m in zip(counts, countcurves)],
        ),
    }
    return _finish(
        values,
        plots,
        "Ten sensors estimate R, split its Hermitian eigenspaces, and scan 1/||E_n^H a||². The independent sources share fixed private waveforms/noise across sweeps; two separated local peaks are selected without truth.",
        "Coherent sources collapse the second signal eigenvalue; assuming two independent sources can create false MUSIC directions.",
        "Average four overlapping seven-element subarray covariances on unchanged coherent data. This restores rank at the cost of aperture. Missing peak sets use an explicit 80-degree penalty; counts expose incompleteness. Toggle off restores selected independent-source data.",
        6601,
        broken,
        detected_angles=peaks.tolist(),
        smoothed_angles=recpeaks.tolist(),
        eigenvalues=eig.tolist(),
        spacing_contrast=sepcontrast,
        spacing_rmse=seperror,
        snapshot_rmse=nerror,
        snr_rmse=snrerror,
        missing_peak_penalty_deg=80,
    )
