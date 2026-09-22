from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 32
BROKEN_TEXT = 'Broken mode moves the notch to half the selected frequency, leaving the actual flexible resonance exposed.'
RECOVERY_TEXT = 'Align the notch with the measured resonance and tune the prefilter independently from command rise-time requirements.'


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
    selected = float(p["notch_frequency_rad_s"])
    notch_w = 0.5*selected if broken else selected
    pre_w = float(p["prefilter_bandwidth_rad_s"])
    plant_w, plant_zeta = 12.0, 0.035
    w = np.geomspace(0.2, 100.0, 360)
    s = 1j*w
    plant = plant_w**2/(s*s+2*plant_zeta*plant_w*s+plant_w**2)
    notch = (s*s+2*0.025*notch_w*s+notch_w**2)/(s*s+2*0.25*notch_w*s+notch_w**2)
    prefilter = pre_w/(s+pre_w)
    shaped = plant*notch
    at_res = int(np.argmin(abs(w-plant_w)))
    attenuation = float(20*np.log10(abs(shaped[at_res])/abs(plant[at_res])))
    high_prefilter = float(20*np.log10(abs(prefilter[-1])))
    dc_gain = 1.0
    return {
        "signature": [attenuation, high_prefilter, dc_gain],
        "metrics": [("notch_attenuation", "Attenuation at plant resonance", attenuation, "dB"),
                    ("prefilter_high", "Prefilter gain at 100 rad/s", high_prefilter, "dB"),
                    ("dc_gain", "Reference prefilter DC gain", dc_gain, "1")],
        "plots": {
            "response": _plot("Flexible-mode response before and after notch", "Angular frequency (rad/s)", "Magnitude (dB)", [
                _trace("Flexible plant", w, 20*np.log10(abs(plant)), "Angular frequency", "rad/s", "Magnitude", "dB"),
                _trace("Plant with notch", w, 20*np.log10(abs(shaped)), "Angular frequency", "rad/s", "Magnitude", "dB")]),
            "mechanism": _plot("Reference-prefilter bandwidth", "Angular frequency (rad/s)", "Reference-path magnitude (dB)", [
                _trace("Unity command path", w, np.zeros_like(w), "Angular frequency", "rad/s", "Reference-path magnitude", "dB"),
                _trace("Filtered command path", w, 20*np.log10(abs(prefilter)), "Angular frequency", "rad/s", "Reference-path magnitude", "dB")]),
        },
        "observation": "The notch attacks a localized plant mechanism; the prefilter moderates commanded content without pretending to improve disturbance rejection."
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
