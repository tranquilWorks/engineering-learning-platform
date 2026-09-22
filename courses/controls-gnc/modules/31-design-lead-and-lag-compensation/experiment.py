from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 31
BROKEN_TEXT = 'Broken mode swaps the lead pole and zero, turning the intended phase lead into phase lag.'
RECOVERY_TEXT = 'Restore p_lead greater than z_lead, confirm positive phase at the target frequency, then add lag below crossover.'


def _trace(name: str, x: Any, y: Any, x_quantity: str, x_unit: str,
           y_quantity: str, y_unit: str, *, mode: str = "lines") -> dict[str, Any]:
    return {
        "type": "scattergl", "mode": mode, "name": name,
        "x": np.asarray(x, dtype=float), "y": np.asarray(y, dtype=float),
        "meta": {"x_quantity": x_quantity, "x_unit": x_unit,
                 "y_quantity": y_quantity, "y_unit": y_unit},
    }


def _plot(title: str, x_title: str, y_title: str,
          traces: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "data": traces,
        "layout": {
            "title": {"text": title, "x": 0.02},
            "xaxis": {"title": {"text": x_title}},
            "yaxis": {"title": {"text": y_title}},
            "legend": {"orientation": "h"},
            "margin": {"l": 72, "r": 36, "t": 62, "b": 62},
            "hovermode": "closest", "uirevision": "keep-view",
        },
        "config": {"responsive": True, "displaylogo": False},
    }


def _result(model: dict[str, Any], broken: bool) -> dict[str, Any]:
    return {
        "metrics": [
            {"id": key, "label": label, "value": float(value), "unit": unit,
              "emphasis": "primary" if index == 0 else "normal"}
            for index, (key, label, value, unit) in enumerate(model["metrics"])
        ],
        "plots": model["plots"],
        "explanations": {
            "observation": model["observation"],
            "broken": BROKEN_TEXT,
            "recovery": RECOVERY_TEXT,
        },
        "diagnostics": {
            "item_number": ITEM_NUMBER,
            "broken_active": bool(broken),
            "signature": [float(value) for value in model["signature"]],
        },
    }

def _model(p: dict[str, Any], broken: bool) -> dict[str, Any]:
    alpha = float(p["lead_alpha"])
    beta = float(p["lag_beta"])
    wm = 3.0
    zlead, plead = wm*np.sqrt(alpha), wm/np.sqrt(alpha)
    if broken:
        zlead, plead = plead, zlead
    zlag, plag = 0.3, 0.3/beta
    w = np.geomspace(0.01, 100, 360)
    s = 1j*w
    lead = (1+s/zlead)/(1+s/plead)
    lag = beta*(1+s/zlag)/(1+s/plag)
    total = lead*lag
    phase = np.unwrap(np.angle(lead))*180/np.pi
    peak_phase = float(np.max(phase))
    low_gain = float(abs(total[0]))
    target_gain = float(20*np.log10(abs(np.interp(wm, w, abs(total)))))
    return {
        "signature": [peak_phase, low_gain, target_gain],
        "metrics": [("lead_phase", "Peak lead phase", peak_phase, "deg"),
                    ("low_gain", "Low-frequency compensator gain", low_gain, "1"),
                    ("target_gain", "Target-frequency gain", target_gain, "dB")],
        "plots": {
            "response": _plot("Lead, lag, and combined magnitude", "Angular frequency (rad/s)", "Magnitude (dB)", [
                _trace("Lead", w, 20*np.log10(abs(lead)), "Angular frequency", "rad/s", "Magnitude", "dB"),
                _trace("Lag", w, 20*np.log10(abs(lag)), "Angular frequency", "rad/s", "Magnitude", "dB"),
                _trace("Combined", w, 20*np.log10(abs(total)), "Angular frequency", "rad/s", "Magnitude", "dB")]),
            "mechanism": _plot("Compensator phase contributions", "Angular frequency (rad/s)", "Phase (deg)", [
                _trace("Lead phase", w, np.angle(lead, deg=True), "Angular frequency", "rad/s", "Phase", "deg"),
                _trace("Lag phase", w, np.angle(lag, deg=True), "Angular frequency", "rad/s", "Phase", "deg")]),
        },
        "observation": "Pole-zero order determines the sign of phase contribution; low-frequency gain and crossover phase must be checked as separate requirements."
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
