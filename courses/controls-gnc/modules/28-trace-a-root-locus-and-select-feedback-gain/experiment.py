from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 28
BROKEN_TEXT = 'Broken mode applies the gain with the wrong feedback sign, moving one characteristic root into the right half-plane.'
RECOVERY_TEXT = 'Move the gain marker back into the left-half-plane segment and verify dominant damping before accepting the time-domain design.'


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

def _roots(gain: float, zero: float) -> np.ndarray:
    return np.roots([1.0, 7.0, 10.0+gain, gain*zero])


def _model(p: dict[str, Any], broken: bool) -> dict[str, Any]:
    gain = -4.0 if broken else float(p["loop_gain"])
    zero = float(p["zero_location_per_s"])
    gains = np.geomspace(1e-4, 100.0, 220)
    locus = np.array([_roots(k, zero) for k in gains])
    roots = _roots(gain, zero)
    dominant = roots[np.argmax(roots.real)]
    damping = float(-dominant.real/max(abs(dominant), 1e-12))
    centroid = (-7.0 + zero)/2.0
    rightmost = float(np.max(roots.real))
    return {
        "signature": [rightmost, damping, centroid],
        "metrics": [("rightmost", "Rightmost closed-loop pole", rightmost, "1/s"),
                    ("damping", "Dominant modal damping", damping, "1"),
                    ("centroid", "Asymptote centroid", centroid, "1/s")],
        "plots": {
            "response": _plot("Three-branch root locus", "Pole real part (1/s)", "Pole imaginary part (1/s)", [
                _trace(f"Branch {i+1}", locus[:, i].real, locus[:, i].imag, "Pole real part", "1/s", "Pole imaginary part", "1/s") for i in range(3)]),
            "mechanism": _plot("Rightmost pole versus loop gain", "Loop gain (1)", "Rightmost pole real part (1/s)", [
                _trace("Stability margin", gains, [np.max(_roots(k, zero).real) for k in gains], "Loop gain", "1", "Rightmost pole real part", "1/s"),
                _trace("Imaginary-axis boundary", gains, np.zeros_like(gains), "Loop gain", "1", "Rightmost pole real part", "1/s")]),
        },
        "observation": "The selected gain is meaningful only when its marked poles are read against branch origin, asymptotes, stability, and damping."
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
