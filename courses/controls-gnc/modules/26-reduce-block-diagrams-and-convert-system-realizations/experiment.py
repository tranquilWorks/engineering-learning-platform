from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 26
BROKEN_TEXT = 'Broken mode performs the cancellation regardless of pole offset and presents the reduced response as exact.'
RECOVERY_TEXT = 'Retain the third state whenever the pole-zero distance is nonzero, then compare frequency responses before accepting a reduced realization.'


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
    offset = float(p["pole_offset_per_s"])
    wmax = float(p["max_frequency_rad_s"])
    if broken and offset < 0.6:
        offset = 0.6
    poles = np.array([-1.0, -(2.0 + offset), -4.0])
    den = np.poly(poles).real
    num = np.array([1.0, 2.0])
    w = np.geomspace(0.05, wmax, 180)
    s = 1j*w
    full = np.polyval(num, s) / np.polyval(den, s)
    # Independent state evaluation of the same controllable canonical realization.
    a1, a2, a3 = den[1:]
    A = np.array([[-a1, -a2, -a3], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
    B = np.array([1.0, 0.0, 0.0])
    C = np.array([0.0, 1.0, 2.0])
    state = np.array([C @ np.linalg.solve(z*np.eye(3)-A, B) for z in s])
    reduced = 1.0 / ((s+1.0)*(s+4.0))
    realization_error = float(np.max(np.abs(full-state)))
    reduction_error = float(np.max(np.abs(full-reduced)))
    distance = abs(offset)
    return {
        "signature": [realization_error, reduction_error, distance],
        "metrics": [("realization_error", "Transfer/state mismatch", realization_error, "1"),
                    ("reduction_error", "Naive reduction mismatch", reduction_error, "1"),
                    ("pole_zero_distance", "Pole-zero distance", distance, "1/s")],
        "plots": {
            "response": _plot("Transfer and state-space frequency-response magnitude", "Angular frequency (rad/s)", "Magnitude (1)", [
                _trace("Transfer polynomial", w, np.abs(full), "Angular frequency", "rad/s", "Magnitude", "1"),
                _trace("State realization", w, np.abs(state), "Angular frequency", "rad/s", "Magnitude", "1")]),
            "mechanism": _plot("Full and naively reduced model mismatch", "Angular frequency (rad/s)", "Magnitude (1)", [
                _trace("Full model", w, np.abs(full), "Angular frequency", "rad/s", "Magnitude", "1"),
                _trace("Naively reduced", w, np.abs(reduced), "Angular frequency", "rad/s", "Magnitude", "1")]),
        },
        "observation": "The state realization follows the full polynomial model to numerical precision; cancellation quality is a separate model-reduction question."
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
