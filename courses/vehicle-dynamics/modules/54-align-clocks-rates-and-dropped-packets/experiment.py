from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 54
DEFAULTS = {"clock_offset_ms": 12.0, "drop_period": 7.0}
RANGES = {"clock_offset_ms": (-25.0, 25.0), "drop_period": (4.0, 12.0)}
BROKEN_TEXT = "Broken mode treats offset source timestamps as already aligned, leaving a phase error that masquerades as sensor disagreement."
RECOVERY_TEXT = "Remove the declared source-clock offset, identify missing grid positions, and interpolate only the bounded single-sample gaps onto the reference clock."


def _parameters(supplied: dict[str, Any]) -> dict[str, float]:
    result = {}
    for key, default in DEFAULTS.items():
        value = float(supplied.get(key, default)); minimum, maximum = RANGES[key]
        if not np.isfinite(value) or value < minimum or value > maximum: raise ValueError(f"{key} outside declared finite range [{minimum}, {maximum}]")
        result[key] = value
    return result


def _trace(name: str, x: Any, y: Any, xq: str, xu: str, yq: str, yu: str) -> dict[str, Any]:
    return {"type": "scattergl", "mode": "lines+markers", "name": name, "x": np.asarray(x, dtype=float), "y": np.asarray(y, dtype=float), "meta": {"x_quantity": xq, "x_unit": xu, "y_quantity": yq, "y_unit": yu}}


def _plot(title: str, xt: str, yt: str, traces: list[dict[str, Any]]) -> dict[str, Any]:
    return {"data": traces, "layout": {"title": {"text": title, "x": 0.02}, "xaxis": {"title": {"text": xt}}, "yaxis": {"title": {"text": yt}}, "legend": {"orientation": "h"}, "margin": {"l": 72, "r": 36, "t": 62, "b": 62}, "hovermode": "closest", "uirevision": "keep-view"}, "config": {"responsive": True, "displaylogo": False}}


def _result(model: dict[str, Any], broken: bool) -> dict[str, Any]:
    return {"metrics": [{"id": k, "label": l, "value": float(v), "unit": u, "emphasis": "primary" if i == 0 else "normal"} for i, (k, l, v, u) in enumerate(model["metrics"])], "plots": model["plots"], "explanations": {"observation": model["observation"], "broken": BROKEN_TEXT, "recovery": RECOVERY_TEXT}, "diagnostics": {"item_number": ITEM_NUMBER, "broken_active": bool(broken), "signature": [float(v) for v in model["signature"]]}}


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    offset = p["clock_offset_ms"] / 1000.0
    period = round(p["drop_period"])
    reference_time = np.arange(101, dtype=float) * 0.02
    truth = np.sin(2.0 * np.pi * 0.7 * reference_time) + 0.2 * np.cos(2.0 * np.pi * 1.3 * reference_time)
    source_time = reference_time + offset
    keep = np.ones(reference_time.size, dtype=bool); keep[period::period] = False
    observed_time, observed = source_time[keep], truth[keep]
    aligned_time = observed_time if broken else observed_time - offset
    reconstructed = np.interp(reference_time, aligned_time, observed)
    rmse = float(np.sqrt(np.mean((reconstructed - truth) ** 2)))
    aligned_offset = 0.0 if broken else offset
    max_gap = float(np.max(np.diff(aligned_time)))
    time_residual = abs(aligned_offset - offset)
    signature = [1000.0 * aligned_offset, float(np.count_nonzero(~keep)), float(reference_time.size), 1000.0 * max_gap, rmse, 1000.0 * time_residual]
    return {
        "signature": signature,
        "metrics": [("offset", "Recovered clock offset", signature[0], "ms"), ("drops", "Detected dropped samples", signature[1], "sample"), ("aligned", "Aligned sample count", signature[2], "sample"), ("maximum_gap", "Maximum observed gap", signature[3], "ms"), ("rmse", "Alignment RMSE", rmse, "1"), ("time_residual", "Clock residual", signature[5], "ms")],
        "plots": {"response": _plot("Clock-aligned signal", "Reference time (s)", "Signal amplitude (1)", [_trace("Truth", reference_time, truth, "Reference time", "s", "Signal amplitude", "1"), _trace("Reconstructed", reference_time, reconstructed, "Reference time", "s", "Signal amplitude", "1")]), "mechanism": _plot("Source sample timing", "Sample index (1)", "Timestamp (s)", [_trace("Observed source time", np.arange(observed_time.size), observed_time, "Sample index", "1", "Timestamp", "s"), _trace("Aligned time", np.arange(aligned_time.size), aligned_time, "Sample index", "1", "Timestamp", "s")])},
        "observation": "Rate conversion is trustworthy only after clocks share an epoch and every interpolation spans a declared, bounded gap.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters); broken = bool(parameters.get("broken_mode", False)); return _result(_model(values, broken), broken)
