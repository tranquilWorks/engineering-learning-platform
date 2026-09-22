from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 40
BROKEN_TEXT = 'Broken mode forces three bits and 0.45-sample deterministic jitter, making both staircase and phase displacement visible.'
RECOVERY_TEXT = 'Restore adequate resolution and clock stability, then budget quantization and jitter as separate mechanisms before combining them.'


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
    bits=int(3 if broken else round(float(p["converter_bits"]))); jf=.45 if broken else float(p["jitter_fraction"]); fs=100.; n=np.arange(300); t=n/fs; jitter=jf/fs*np.sin(2*np.pi*n/37); f=17.; ideal=np.sin(2*np.pi*f*t); timed=np.sin(2*np.pi*f*(t+jitter)); step=2/(2**bits-1); quant=np.clip(np.round(timed/step)*step,-1,1)
    qe=float(np.sqrt(np.mean((quant-timed)**2))); je=float(np.sqrt(np.mean((timed-ideal)**2))); total=np.sqrt(np.mean((quant-ideal)**2)); snr=float(20*np.log10(np.sqrt(np.mean(ideal**2))/max(total,1e-15)))
    return {"signature":[qe,je,snr],"metrics":[("quantization","Quantization RMS error",qe,"V"),("jitter","Jitter RMS error",je,"V"),("snr","Combined sampled SNR",snr,"dB")],
      "plots":{"response":_plot("Ideal and digitized sensor waveform","Time (s)","Sensor voltage (V)",[_trace("Ideal signal",t,ideal,"Time","s","Sensor voltage","V"),_trace("Jittered and quantized",t,quant,"Time","s","Sensor voltage","V",mode="lines+markers")]),
      "mechanism":_plot("Separated digitization errors","Time (s)","Voltage error (V)",[_trace("Quantization error",t,quant-timed,"Time","s","Voltage error","V"),_trace("Jitter error",t,timed-ideal,"Time","s","Voltage error","V")])},"observation":"The separated error traces prevent a higher bit count from being mistaken for a clock-jitter cure."}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
