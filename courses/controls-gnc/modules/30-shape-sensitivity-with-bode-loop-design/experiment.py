from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 30
BROKEN_TEXT = 'Broken mode closes the same loop with the wrong feedback sign, replacing 1+L by 1-L and producing a near-singular sensitivity peak.'
RECOVERY_TEXT = 'Restore negative feedback and select crossover only after checking all four maps: S, T, PS, and CS.'


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
    gain = float(p["loop_gain"])
    zero = float(p["lead_zero_rad_s"])
    pole = 10*zero
    w = np.geomspace(0.02, 200.0, 360)
    s = 1j*w
    P = 1/(s*(s+1))
    C = gain*(1+s/zero)/(1+s/pole)
    L = P*C
    denominator = 1-L if broken else 1+L
    S = 1/denominator
    T = L/denominator
    PS = P*S
    CS = C*S
    db = lambda value: 20*np.log10(np.maximum(np.abs(value), 1e-12))
    peak_s, peak_t, peak_cs = map(float, (np.max(abs(S)), np.max(abs(T)), np.max(abs(CS))))
    return {
        "signature": [peak_s, peak_t, peak_cs, float(np.max(np.abs(S+T-1)))],
        "metrics": [("peak_s", "Peak sensitivity", peak_s, "1"),
                    ("peak_t", "Peak complementary sensitivity", peak_t, "1"),
                    ("peak_cs", "Peak control sensitivity", peak_cs, "1")],
        "plots": {
            "response": _plot("Sensitivity and complementary-sensitivity magnitude", "Angular frequency (rad/s)", "Magnitude (dB)", [
                _trace("Sensitivity S", w, db(S), "Angular frequency", "rad/s", "Magnitude", "dB"),
                _trace("Complementary sensitivity T", w, db(T), "Angular frequency", "rad/s", "Magnitude", "dB")]),
            "mechanism": _plot("Disturbance and control-effort maps", "Angular frequency (rad/s)", "Magnitude (dB)", [
                _trace("Plant disturbance map PS", w, db(PS), "Angular frequency", "rad/s", "Magnitude", "dB"),
                _trace("Control sensitivity CS", w, db(CS), "Angular frequency", "rad/s", "Magnitude", "dB")]),
        },
        "observation": "Reading S alone hides the noise and actuator price. The identity S+T=1 makes the trade explicit at every frequency."
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
