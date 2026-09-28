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


def _amplitude_width(axis, magnitude):
    peak = int(np.argmax(magnitude))
    level = magnitude[peak] / np.sqrt(2)
    left = right = peak
    while left > 0 and magnitude[left] >= level:
        left -= 1
    while right < len(axis) - 1 and magnitude[right] >= level:
        right += 1
    if magnitude[left] >= level or magnitude[right] >= level:
        return float(axis[-1] - axis[0])
    lo = axis[left] + (level - magnitude[left]) * (axis[left + 1] - axis[left]) / (
        magnitude[left + 1] - magnitude[left]
    )
    hi = axis[right - 1] + (level - magnitude[right - 1]) * (
        axis[right] - axis[right - 1]
    ) / (magnitude[right] - magnitude[right - 1])
    return float(hi - lo)


def _linear_row(row, axis, query):
    f = (query - axis[0]) / (axis[1] - axis[0])
    left = np.floor(f).astype(int)
    valid = (left >= 0) & (left < len(axis) - 1)
    j = np.clip(left, 0, len(axis) - 2)
    w = f - left
    return np.where(valid, (1 - w) * row[j] + w * row[j + 1], 0)


from scipy import ndimage as _ndi84
from scipy import signal as _signal84

CONTROLS = [
    ("design_pfa", 0.001, [0.0001, 0.001, 0.01]),
    ("replica_taper", 0, [0, 0.5, 1]),
]


def _pulse84():
    t = (np.arange(32) - 15.5) / 4e6
    return t, np.exp(1j * np.pi * (2e6 / 8e-6) * t * t) / np.sqrt(32)


def _scan84(pulse, scan):
    r = np.array([900, 1650, 2550, 2625]) - np.array([0, 30, -15, -15]) * (scan - 1)
    v = np.array([0, 30, -15, -15])
    idx = np.floor(r / 37.5 + 0.5).astype(int)
    fd = 2 * v / 0.03
    visible = np.array([1, 0 if scan == 4 else 1, 1, 1])
    amp = np.array([1.8, 2.2, 3, 0.22]) * visible
    scale = np.where(np.arange(128) * 37.5 >= 1800, 0.20, 0.015)
    clutter = scale * _noise(8411, 128)[:, 0]
    reflectivity = np.tile(clutter[:, None], (1, 32))
    for k, a in enumerate(amp):
        reflectivity[idx[k]] += a * np.exp(2j * np.pi * fd[k] * np.arange(32) / 31250)
    propagated = _signal84.fftconvolve(
        reflectivity, pulse[:, None], mode="full", axes=0
    )[:128]
    receiver = propagated.copy()
    available = min(32, 128 - 104)
    receiver[104 : 104 + available] += (
        0.85
        * pulse[:available, None]
        * np.exp(2j * np.pi * 5 * np.arange(32) / 32)[None, :]
    )
    preimage = receiver + 0.18 * _noise(8501 + scan, 128, 32)
    measured = preimage + 0.12 * preimage.conj() + (0.04 + 0.03j)
    centered = measured - (0.04 + 0.03j)
    corrected = (centered - 0.12 * centered.conj()) / (1 - 0.12**2)
    truth = {
        "range": r,
        "velocity": v,
        "range_index": idx,
        "doppler_index": np.floor(fd / 31250 * 32 + 0.5).astype(int) + 16,
        "visible": visible,
    }
    return measured, corrected, truth, float(np.max(abs(corrected - preimage)))


def _cfar84(power, pfa):
    # Complete 13-by-9 outer stencil minus the 5-by-3 CUT/guard rectangle.
    padded = np.pad(power, ((1, 0), (1, 0))).cumsum(0).cumsum(1)
    rr = np.arange(6, 122)[:, None]
    dd = np.arange(4, 28)[None, :]

    def box(hr, hd):
        return (
            padded[rr + hr + 1, dd + hd + 1]
            - padded[rr - hr, dd + hd + 1]
            - padded[rr + hr + 1, dd - hd]
            + padded[rr - hr, dd - hd]
        )

    noise = (box(6, 4) - box(2, 1)) / 102
    threshold = np.zeros_like(power)
    eligible = np.zeros(power.shape, bool)
    eligible[6:122, 4:28] = True
    threshold[6:122, 4:28] = 102 * (pfa ** (-1 / 102) - 1) * noise
    detected = eligible & (power > threshold)
    return threshold, eligible, detected


def _reports84(detected, power, threshold):
    labels, count = _ndi84.label(detected, structure=np.ones((3, 3), int))
    reports = []
    velocity = (np.arange(32) - 16) * 31250 / 32 * 0.03 / 2
    for label in range(1, count + 1):
        rows, cols = np.where(labels == label)
        excess = np.maximum(power[rows, cols] / threshold[rows, cols] - 1, 0)
        if not np.any(excess):
            excess = np.ones(len(rows))
        peak = int(np.argmax(power[rows, cols]))
        reports.append(
            {
                "range": float(np.dot(excess, rows * 37.5) / sum(excess)),
                "velocity": float(np.dot(excess, velocity[cols]) / sum(excess)),
                "peak": float(power[rows[peak], cols[peak]]),
                "cells": len(rows),
                "range_index": int(rows[peak]),
                "doppler_index": int(cols[peak]),
            }
        )
    return reports


def _process84(cube, pulse, pfa, taper, wrong=False):
    replica = pulse * ((1 - taper) + taper * np.hanning(32))
    replica /= np.linalg.norm(replica)
    kernel = replica[::-1] if wrong else replica[::-1].conj()
    matched = _signal84.fftconvolve(cube, kernel[:, None], mode="full", axes=0)[31:159]
    window = np.hanning(32)
    rd = np.fft.fftshift(np.fft.fft(matched * window[None, :], axis=1), axes=1) / sum(
        window
    )
    power = abs(rd) ** 2
    threshold, eligible, detected = _cfar84(power, pfa)
    return {
        "matched": matched,
        "rd": rd,
        "power": power,
        "threshold": threshold,
        "eligible": eligible,
        "detected": detected,
        "reports": _reports84(detected, power, threshold),
    }


def _score84(product, truth):
    reports = product["reports"]
    adj = []
    for r, v in zip(truth["range"], truth["velocity"]):
        adj.append(
            [
                j
                for j, a in enumerate(reports)
                if abs(a["range"] - r) <= 75
                and abs(a["velocity"] - v) <= 1.5 * 14.6484375
            ]
        )
    assigned = {}

    def augment(i, seen):
        for j in adj[i]:
            if j in seen:
                continue
            seen.add(j)
            if j not in assigned or augment(assigned[j], seen):
                assigned[j] = i
                return True
        return False

    matches = sum(augment(i, set()) for i in range(4))
    mask = product["eligible"].copy()
    for r, d in zip(truth["range_index"], truth["doppler_index"]):
        mask[max(0, r - 2) : min(128, r + 3), max(0, d - 1) : min(32, d + 2)] = False
    return {
        "matches": int(matches),
        "false_reports": len(reports) - len(assigned),
        "false_cells": int(np.sum(product["detected"] & mask)),
        "background_cells": int(np.sum(mask)),
    }


def _track84(history):
    candidates = [
        r for r in history[0] if 1300 < r["range"] < 2000 and r["velocity"] > 0
    ]
    if not candidates:
        raise ValueError(
            "Reviewed baseline surveillance sector contains no initiating report"
        )
    first = max(candidates, key=lambda r: r["peak"])
    ranges = [first["range"]]
    rates = [-first["velocity"]]
    updates = [True]
    coasts = [0]
    for reports in history[1:]:
        prediction = ranges[-1] + rates[-1]
        rate = rates[-1]
        gated = [
            r
            for r in reports
            if abs(r["range"] - prediction) <= 225 and abs(r["velocity"] + rate) <= 35
        ]
        if gated:
            chosen = min(
                gated,
                key=lambda r: (
                    abs(r["range"] - prediction) / 225 + abs(r["velocity"] + rate) / 35
                ),
            )
            innovation = chosen["range"] - prediction
            ranges.append(prediction + 0.65 * innovation)
            rates.append(rate + 0.18 * innovation)
            updates.append(True)
            coasts.append(0)
        else:
            ranges.append(prediction)
            rates.append(rate)
            updates.append(False)
            coasts.append(coasts[-1] + 1)
    return np.array(ranges), np.array(rates), updates, coasts


def run(parameters):
    pfa, taper, broken = _controls(parameters, CONTROLS)
    t, pulse = _pulse84()
    measured, cube, truth, cal_error = _scan84(pulse, 1)
    correct = _process84(cube, pulse, pfa, taper)
    active = _process84(cube, pulse, pfa, taper, True) if broken else correct
    score = _score84(active, truth)
    # As in the source, the eight-scan tracking demonstration retains the reviewed
    # Pfa/taper/replica baseline. Selected controls compare the retained first scan.
    history = []
    truth_track = []
    matches = 0
    false_reports = 0
    for scan in range(1, 9):
        _, h, tr, _ = _scan84(pulse, scan)
        out = _process84(h, pulse, 0.001, 0)
        sc = _score84(out, tr)
        history.append(out["reports"])
        truth_track.append(tr["range"][1])
        matches += sc["matches"]
        false_reports += sc["false_reports"]
    track, rates, updates, coasts = _track84(history)
    rmse = np.sqrt(np.mean((track - truth_track) ** 2))
    quiet = correct["power"][
        (np.arange(128) * 37.5 > 300) & (np.arange(128) * 37.5 < 1500)
    ]
    fixed_threshold = -np.log(pfa) * np.median(quiet) / np.log(2)
    fixed_detection = correct["eligible"] & (correct["power"] > fixed_threshold)
    edge = correct["eligible"] & (np.arange(128)[:, None] * 37.5 >= 1800)
    pfas = [0.0001, 0.001, 0.01]
    pfa_cells = []
    pfa_false = []
    pfa_reports = []
    for q in pfas:
        th, eligible, detection = _cfar84(correct["power"], q)
        pr = {
            "power": correct["power"],
            "threshold": th,
            "eligible": eligible,
            "detected": detection,
            "reports": _reports84(detection, correct["power"], th),
        }
        sc = _score84(pr, truth)
        pfa_cells.append(int(sum(detection.ravel())))
        pfa_false.append(sc["false_cells"])
        pfa_reports.append(len(pr["reports"]))
    tapers = [0, 0.5, 1]
    widths = []
    weak = []
    for a in tapers:
        out = _process84(cube, pulse, pfa, a)
        cut = out["power"][:, truth["doppler_index"][2]]
        i = int(truth["range_index"][2])
        left = right = i
        half = cut[i] / 2
        while left > 0 and cut[left - 1] >= half:
            left -= 1
        while right < 127 and cut[right + 1] >= half:
            right += 1
        widths.append(right - left + 1)
        weak.append(
            float(
                10
                * np.log10(
                    out["power"][truth["range_index"][3], truth["doppler_index"][3]]
                    / out["power"][truth["range_index"][2], truth["doppler_index"][2]]
                )
            )
        )
    peak = float(np.max(active["power"]))
    goodpeak = float(np.max(correct["power"]))
    values = {
        "active_peak_power": (peak, "V^2"),
        "compression_peak_ratio": (peak / goodpeak, "ratio"),
        "detected_cells": (np.sum(active["detected"]), "count"),
        "clustered_reports": (len(active["reports"]), "count"),
        "matched_truth_reports": (score["matches"], "count"),
        "false_reports": (score["false_reports"], "count"),
        "empirical_false_cell_rate": (
            score["false_cells"] / score["background_cells"],
            "ratio",
        ),
        "baseline_sequence_pd": (matches / 32, "ratio"),
        "baseline_track_rmse": (rmse, "m"),
        "scan_four_coast_count": (coasts[3], "count"),
        "receiver_reconstruction_error": (cal_error, "V"),
        "model_valid": (not broken, "boolean"),
    }
    ranges = np.arange(128) * 37.5
    velocity = (np.arange(32) - 16) * 14.6484375
    norm = goodpeak
    plots = {
        "waveform": _plot(
            "Unit-energy LFM transmit waveform",
            "Centered fast time (us)",
            "Voltage (V)",
            [("I", t * 1e6, pulse.real), ("Q", t * 1e6, pulse.imag)],
        ),
        "receiver": _plot(
            "Receiver calibration before matched filtering",
            "Fast-time range sample (m)",
            "Voltage (V)",
            [
                ("Measured I", ranges, measured[:, 0].real),
                ("Calibrated I", ranges, cube[:, 0].real),
            ],
        ),
        "matched": _plot(
            "Selected replica: delay-corrected range compression",
            "Monostatic range (m)",
            "Magnitude (V)",
            [
                ("Selected", ranges, abs(active["matched"][:, 0])),
                ("Correct conjugation", ranges, abs(correct["matched"][:, 0])),
            ],
        ),
        "range_doppler": _heat(
            "Selected coherent range-Doppler power",
            "Approach speed (m/s)",
            "Monostatic range (m)",
            velocity,
            ranges,
            _db(active["power"] / norm),
            "dB relative to correct peak",
        ),
        "detections": _heat(
            "Complete-stencil CA-CFAR threshold crossings",
            "Approach speed (m/s)",
            "Monostatic range (m)",
            velocity,
            ranges,
            active["detected"].astype(float),
            "detection (boolean)",
        ),
        "threshold": _plot(
            "Adaptive threshold along moving-target Doppler bin",
            "Range (m)",
            "Power (V^2)",
            [
                ("CUT power", ranges[6:122], active["power"][6:122, 18]),
                ("CA-CFAR threshold", ranges[6:122], active["threshold"][6:122, 18]),
            ],
        ),
        "reports": _plot(
            "Eight-connected excess-weighted reports",
            "Approach speed (m/s)",
            "Monostatic range (m)",
            [
                (
                    "Reports",
                    [a["velocity"] for a in active["reports"]],
                    [a["range"] for a in active["reports"]],
                )
            ],
        ),
        "track": _plot(
            "Reviewed baseline eight-scan track and physical fade",
            "Scan (count)",
            "Monostatic range (m)",
            [
                ("Truth for scoring", np.arange(1, 9), truth_track),
                ("Gated alpha-beta track", np.arange(1, 9), track),
            ],
        ),
        "coast": _plot(
            "Baseline update/coast decisions from detections",
            "Scan (count)",
            "Update flag / coast count (count)",
            [
                ("Measurement update", np.arange(1, 9), np.array(updates, int)),
                ("Consecutive coasts", np.arange(1, 9), coasts),
            ],
        ),
        "pfa": _plot(
            "Threshold nesting on the same corrected power map",
            "Requested homogeneous-cell Pfa (ratio)",
            "Count (count)",
            [
                ("Detection cells", pfas, pfa_cells),
                ("False cells", pfas, pfa_false),
                ("Reports", pfas, pfa_reports),
            ],
        ),
        "taper_width": _plot(
            "Replica taper trades range width",
            "Cosine taper fraction (ratio)",
            "Strong-target half-power width (samples)",
            [("Measured", tapers, widths)],
        ),
        "taper_visibility": _plot(
            "Replica taper changes nearby weak-target visibility",
            "Cosine taper fraction (ratio)",
            "Weak/strong cell power (dB)",
            [("Measured", tapers, weak)],
        ),
    }
    plots["reports"]["data"][0]["mode"] = "markers"
    return _finish(
        values,
        plots,
        "Trace unit-energy LFM through echoes, receiver correction, conjugate matched filtering, coherent Doppler, complete-stencil CA-CFAR, connected reports and gated tracking. Controls affect the retained first scan; the explicitly labeled eight-scan baseline shows a real scan-4 fade and coast.",
        "Removing conjugation from the matched replica loses coherent compression gain and changes downstream detections. A fixed threshold also overreacts to the clutter edge; a report near the injected receiver spur is a false report, not target truth.",
        "Disable the failure to rerun the conjugate time-reversed replica on the identical calibrated cube. Reports drive tracking; truth is used only for offline scoring. Requested Pfa is not a guarantee for these correlated, nonhomogeneous cells.",
        8401,
        broken,
        pfa_detection_cells=pfa_cells,
        pfa_false_cells=pfa_false,
        pfa_report_counts=pfa_reports,
        taper_width_samples=widths,
        taper_weak_strong_db=weak,
        track_updated=updates,
        track_coast_counts=coasts,
        track_ranges_m=track.tolist(),
        track_range_rates_mps=rates.tolist(),
        baseline_sequence_false_reports=false_reports,
        tracking_configuration={"pfa": 0.001, "taper": 0, "correct_replica": True},
        cfar_training_cells=102,
        testable_cells=int(np.sum(active["eligible"])),
        fixed_edge_detections=int(np.sum(fixed_detection & edge)),
        adaptive_edge_detections=int(np.sum(correct["detected"] & edge)),
        calibrated_cube_shape=list(cube.shape),
        reports=active["reports"],
    )
