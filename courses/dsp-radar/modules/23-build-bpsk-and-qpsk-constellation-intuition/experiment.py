from __future__ import annotations

from typing import Any

import numpy as np


def _plot(title, xlabel, ylabel, traces):
    data = []
    for name, x, y in traces:
        x, y = np.asarray(x), np.asarray(y)
        indices = np.unique(np.linspace(0, len(x) - 1, min(len(x), 512)).astype(int))
        data.append(
            {
                "type": "scatter",
                "mode": "lines",
                "name": name,
                "x": x[indices].tolist(),
                "y": y[indices].tolist(),
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


def _result(signature, fields, plots, explanations, seed, broken, extra=None):
    return {
        "metrics": [
            {
                "id": fields[i][0],
                "label": fields[i][0].replace("_", " "),
                "value": float(v),
                "unit": fields[i][1],
            }
            for i, v in enumerate(signature)
        ],
        "plots": plots,
        "explanations": explanations,
        "diagnostics": {
            "signature": [float(v) for v in signature],
            "signature_fields": [f[0] for f in fields],
            "seed": seed,
            "broken_active": broken,
            **(extra or {}),
        },
    }


def _symbols():
    rng = np.random.default_rng(1023)
    b = (rng.random(400) >= 0.5).astype(int)
    q = (rng.random((2, 400)) >= 0.5).astype(int)
    bn = rng.standard_normal(400) + 1j * rng.standard_normal(400)
    qn = rng.standard_normal(400) + 1j * rng.standard_normal(400)
    return b, q, bn, qn


def _receive(ebn0, phase):
    b, q, bn, qn = _symbols()
    bs = 2 * b - 1
    qs = ((2 * q[0] - 1) + 1j * (2 * q[1] - 1)) / np.sqrt(2)
    rotation = np.exp(1j * np.deg2rad(phase))
    br = bs * rotation + bn / np.sqrt(2 * 10 ** (ebn0 / 10))
    qr = qs * rotation + qn / np.sqrt(4 * 10 ** (ebn0 / 10))
    corrected = qr / rotation
    ber_b = np.mean((br.real >= 0) != b)
    ber_q = np.mean(np.array([qr.real >= 0, qr.imag >= 0]) != q)
    ber_corrected = np.mean(np.array([corrected.real >= 0, corrected.imag >= 0]) != q)
    return bs, qs, br, qr, corrected, ber_b, ber_q, ber_corrected


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    snr = float(parameters.get("ebn0_db", 6))
    phase = float(parameters.get("phase_error_deg", 12))
    broken = bool(parameters.get("broken_mode", False))
    if snr not in {-4, 0, 4, 6, 8, 16} or phase not in {0, 12, 15, 30, 50, 55}:
        raise ValueError("Choose a retained constellation Eb/N0 and phase")
    active_snr, active_phase = (16, 55) if broken else (snr, phase)
    bs, qs, br, qr, corrected, bb, qb, cb = _receive(active_snr, active_phase)
    signature = [
        active_snr,
        active_phase,
        np.mean(abs(bs) ** 2),
        np.mean(abs(qs) ** 2),
        1 / np.sqrt(2 * 10 ** (active_snr / 10)),
        1 / np.sqrt(4 * 10 ** (active_snr / 10)),
        bb,
        qb,
        cb,
    ]
    fields = [
        ("ebn0", "dB"),
        ("phase_error", "deg"),
        ("bpsk_symbol_energy", "normalized energy"),
        ("qpsk_symbol_energy", "normalized energy"),
        ("bpsk_noise_sigma", "normalized amplitude"),
        ("qpsk_noise_sigma", "normalized amplitude"),
        ("bpsk_ber", "ratio"),
        ("qpsk_ber", "ratio"),
        ("inverse_rotation_ber", "ratio"),
    ]
    snrs, phases = [-4, 0, 4, 8], [0, 15, 30, 50]
    plots = {
        "bit_mapping": _plot(
            "Input bits before symbol mapping",
            "Symbol index (integer)",
            "Bit value (0 or 1)",
            [
                ("BPSK bit", np.arange(24), _symbols()[0][:24]),
                ("QPSK I bit", np.arange(24), _symbols()[1][0, :24]),
                ("QPSK Q bit", np.arange(24), _symbols()[1][1, :24]),
            ],
        ),
        "symbol_mapping": _plot(
            "First 24 mapped QPSK symbols",
            "Symbol index (integer)",
            "Coordinate (normalized amplitude)",
            [("I", np.arange(24), qs.real[:24]), ("Q", np.arange(24), qs.imag[:24])],
        ),
        "constellation": _plot(
            "Noisy QPSK and exact inverse rotation",
            "In-phase (normalized amplitude)",
            "Quadrature (normalized amplitude)",
            [
                ("received", qr.real, qr.imag),
                ("recovered", corrected.real, corrected.imag),
                ("I decision boundary", [0, 0], [-2, 2]),
                ("Q decision boundary", [-2, 2], [0, 0]),
            ],
        ),
        "bpsk": _plot(
            "BPSK uses the I sign",
            "In-phase (normalized amplitude)",
            "Quadrature (normalized amplitude)",
            [("BPSK received", br.real, br.imag), ("I=0", [0, 0], [-2, 2])],
        ),
        "noise_sweep": _plot(
            "Eb/N0 sweep at selected phase",
            "Eb/N0 (dB)",
            "Bit error rate (ratio)",
            [
                ("BPSK", snrs, [_receive(s, phase)[5] for s in snrs]),
                ("QPSK", snrs, [_receive(s, phase)[6] for s in snrs]),
            ],
        ),
        "phase_sweep": _plot(
            "Phase sweep at 8 dB Eb/N0",
            "Phase error (deg)",
            "Bit error rate (ratio)",
            [
                ("BPSK", phases, [_receive(8, p)[5] for p in phases]),
                ("QPSK", phases, [_receive(8, p)[6] for p in phases]),
            ],
        ),
    }
    for key in ["constellation", "bpsk"]:
        for trace in plots[key]["data"][: 2 if key == "constellation" else 1]:
            trace["mode"] = "markers"
    return _result(
        signature,
        fields,
        plots,
        {
            "observation": "Both maps have unit symbol energy, but QPSK carries two bits per symbol. At equal Eb/N0 its noise standard deviation per coordinate is smaller by sqrt(2).",
            "broken": "At 55 degrees and 16 dB, QPSK clusters are tight but cross the fixed receiver sign boundaries. More SNR does not fix the wrong phase reference.",
            "recovery": "Multiply the received QPSK samples by the exact inverse carrier rotation before sign decisions. This demonstration assumes the phase error is known; it does not implement carrier acquisition.",
        },
        1023,
        broken,
        {
            "symbol_count": 400,
            "bpsk_bits": _symbols()[0][:24].tolist(),
            "qpsk_bits": _symbols()[1][:, :24].tolist(),
        },
    )
