from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 56
DEFAULTS = {"initial_heading_deg": 15.0, "gps_blend": 0.12}
RANGES = {"initial_heading_deg": (-30.0, 30.0), "gps_blend": (0.0, 0.30)}
BROKEN_TEXT = "Broken mode uses degree-valued heading directly in trigonometric functions and integrates degree-per-second yaw as radians per second."
RECOVERY_TEXT = "Convert heading and yaw rate to radians once, integrate body-forward speed on the timestamp grid, and apply the bounded position correction without changing heading units."


def _parameters(supplied: dict[str, Any]) -> dict[str, float]:
    result = {}
    for key, default in DEFAULTS.items():
        value = float(supplied.get(key, default)); minimum, maximum = RANGES[key]
        if not np.isfinite(value) or value < minimum or value > maximum: raise ValueError(f"{key} outside declared finite range [{minimum}, {maximum}]")
        result[key] = value
    return result


def _trace(name: str, x: Any, y: Any, xq: str, xu: str, yq: str, yu: str) -> dict[str, Any]:
    return {"type": "scattergl", "mode": "lines", "name": name, "x": np.asarray(x, dtype=float), "y": np.asarray(y, dtype=float), "meta": {"x_quantity": xq, "x_unit": xu, "y_quantity": yq, "y_unit": yu}}


def _plot(title: str, xt: str, yt: str, traces: list[dict[str, Any]]) -> dict[str, Any]:
    return {"data": traces, "layout": {"title": {"text": title, "x": 0.02}, "xaxis": {"title": {"text": xt}}, "yaxis": {"title": {"text": yt}}, "legend": {"orientation": "h"}, "margin": {"l": 72, "r": 36, "t": 62, "b": 62}, "hovermode": "closest", "uirevision": "keep-view"}, "config": {"responsive": True, "displaylogo": False}}


def _result(model: dict[str, Any], broken: bool) -> dict[str, Any]:
    return {"metrics": [{"id": k, "label": l, "value": float(v), "unit": u, "emphasis": "primary" if i == 0 else "normal"} for i, (k, l, v, u) in enumerate(model["metrics"])], "plots": model["plots"], "explanations": {"observation": model["observation"], "broken": BROKEN_TEXT, "recovery": RECOVERY_TEXT}, "diagnostics": {"item_number": ITEM_NUMBER, "broken_active": bool(broken), "signature": [float(v) for v in model["signature"]]}}


def _integrate(initial_deg: float, blend: float, broken: bool) -> tuple[list[float], np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    step, samples = 0.05, 241
    time = np.arange(samples, dtype=float) * step
    speed = 15.0 + 2.0 * np.sin(0.35 * time)
    yaw_deg_s = 8.0 * np.sin(0.28 * time) + 1.5
    truth_x = np.zeros(samples); truth_y = np.zeros(samples); truth_heading = np.zeros(samples); truth_heading[0] = np.deg2rad(initial_deg)
    for index in range(1, samples):
        truth_heading[index] = truth_heading[index - 1] + np.deg2rad(yaw_deg_s[index - 1]) * step
        truth_x[index] = truth_x[index - 1] + speed[index - 1] * np.cos(truth_heading[index - 1]) * step
        truth_y[index] = truth_y[index - 1] + speed[index - 1] * np.sin(truth_heading[index - 1]) * step
    gps_x = truth_x + 0.40 * np.sin(0.9 * time); gps_y = truth_y + 0.35 * np.cos(0.7 * time)
    x = np.zeros(samples); y = np.zeros(samples); heading = np.zeros(samples); heading[0] = initial_deg if broken else np.deg2rad(initial_deg)
    for index in range(1, samples):
        yaw = yaw_deg_s[index - 1] if broken else np.deg2rad(yaw_deg_s[index - 1])
        heading[index] = heading[index - 1] + yaw * step
        x_predict = x[index - 1] + speed[index - 1] * np.cos(heading[index - 1]) * step
        y_predict = y[index - 1] + speed[index - 1] * np.sin(heading[index - 1]) * step
        x[index] = x_predict + blend * (gps_x[index] - x_predict) * step
        y[index] = y_predict + blend * (gps_y[index] - y_predict) * step
    endpoint_error = float(np.hypot(x[-1] - truth_x[-1], y[-1] - truth_y[-1]))
    path_length = float(np.sum(speed[:-1]) * step)
    closure = float(np.sqrt(np.mean((x - truth_x) ** 2 + (y - truth_y) ** 2)))
    heading_deg = float(np.rad2deg(heading[-1]) if not broken else heading[-1])
    return [float(x[-1]), float(y[-1]), heading_deg, path_length, endpoint_error, closure], x, y, truth_x, truth_y, time


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    signature, x, y, truth_x, truth_y, time = _integrate(p["initial_heading_deg"], p["gps_blend"], broken)
    position_error = np.hypot(x - truth_x, y - truth_y)
    return {
        "signature": signature,
        "metrics": [("final_x", "Final east position", signature[0], "m"), ("final_y", "Final north position", signature[1], "m"), ("heading", "Final heading", signature[2], "deg"), ("path_length", "Integrated path length", signature[3], "m"), ("endpoint_error", "Endpoint error", signature[4], "m"), ("closure", "Trajectory closure RMS", signature[5], "m")],
        "plots": {"response": _plot("Reconstructed trajectory", "East position (m)", "North position (m)", [_trace("Reconstruction", x, y, "East position", "m", "North position", "m"), _trace("Reference", truth_x, truth_y, "East position", "m", "North position", "m")]), "mechanism": _plot("Position error history", "Elapsed time (s)", "Position error (m)", [_trace("Position error", time, position_error, "Elapsed time", "s", "Position error", "m")])},
        "observation": "Trajectory reconstruction closes only when timestamp spacing, yaw units, heading convention, and body-to-inertial rotation are applied consistently.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters); broken = bool(parameters.get("broken_mode", False)); return _result(_model(values, broken), broken)
