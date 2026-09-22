from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 39
BROKEN_TEXT = 'Broken mode bypasses the passivity observer/controller and replays delayed force without energy limiting.'
RECOVERY_TEXT = 'Restore the energy tank, include saturation in the observer, and reduce gain or delay until energy remains bounded.'


def _trace(name: str, x: Any, y: Any, x_quantity: str, x_unit: str,
           y_quantity: str, y_unit: str) -> dict[str, Any]:
    return {
        "type": "scattergl", "mode": "lines", "name": name,
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
            "sample_count": int(model["sample_count"]),
            "signature": [float(value) for value in model["signature"]],
            "software_only": True,
        },
    }

def _model(p: dict[str, Any], broken: bool) -> dict[str, Any]:
    a = float(p["round_trip_delay_ms"])
    b = float(p["force_limit_n"])
    if broken:
        a, b = (110.0, 5.0)
    x = np.linspace(0.0, 1.0, 181)
    signature = [float(value) for value in [(-.002*a*b if broken else .0005*b*max(0.,40-a)), min(1.,20/max(2.,b)), max(0.,80-a)*(0.5 if broken else 1.)]]
    y1 = np.asarray((.02*b-a*.002)*x if broken else .0005*b*(1-np.exp(-4*x)), dtype=float)
    y2 = np.asarray(np.zeros_like(x), dtype=float)
    z1 = np.asarray(np.minimum(1.,20/max(2.,b))*np.ones_like(x), dtype=float)
    z2 = np.asarray(np.zeros_like(x), dtype=float)
    if y1.ndim == 0:
        y1 = np.full_like(x, float(y1))
    if y2.ndim == 0:
        y2 = np.full_like(x, float(y2))
    if z1.ndim == 0:
        z1 = np.full_like(x, float(z1))
    if z2.ndim == 0:
        z2 = np.full_like(x, float(z2))
    return {
        "signature": signature,
        "sample_count": len(x),
        "metrics": [("passivity_energy", "Passivity Energy", signature[0], "J"), ("saturation_fraction", "Saturation Fraction", signature[1], "1"), ("delay_margin", "Delay Margin", signature[2], "ms")],
        "plots": {
            "response": _plot("Passivity-observer energy", "Time fraction (1)", "Observed energy (J)", [
                _trace("Model response", x, y1, "Time fraction", "1", "Observed energy", "J"),
                _trace("Reference or bound", x, y2, "Time fraction", "1", "Observed energy", "J"),
            ]),
            "mechanism": _plot("Force saturation occupancy", "Time fraction (1)", "Saturation fraction (1)", [
                _trace("Governing mechanism", x, z1, "Time fraction", "1", "Saturation fraction", "1"),
                _trace("Requirement or reference", x, z2, "Time fraction", "1", "Saturation fraction", "1"),
            ]),
        },
        "observation": "A delayed saturated interaction remains within this lesson's claim only when observed net energy and the energy tank stay nonnegative.",
    }



def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
