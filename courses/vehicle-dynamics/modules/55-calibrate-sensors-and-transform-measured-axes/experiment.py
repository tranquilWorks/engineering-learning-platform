from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 55
DEFAULTS = {"yaw_bias_deg_s": 1.5, "mounting_yaw_deg": 8.0}
RANGES = {"yaw_bias_deg_s": (-3.0, 3.0), "mounting_yaw_deg": (-15.0, 15.0)}
BROKEN_TEXT = "Broken mode sends the mounting angle in degrees directly into sine and cosine and leaves yaw-rate bias in the calibrated channel."
RECOVERY_TEXT = "Remove sensor bias in native units, convert the mounting angle to radians once, and rotate the calibrated sensor vector into the declared body axes."


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


def _rotation(angle: float) -> np.ndarray:
    return np.array(((np.cos(angle), -np.sin(angle)), (np.sin(angle), np.cos(angle))))


def _state(bias: float, mounting_deg: float, broken: bool) -> list[float]:
    truth = np.array((1.20, 4.50)); sensor_bias = np.array((0.15, -0.10)); sensor_scale = np.array((1.04, 0.97))
    physical_angle = np.deg2rad(mounting_deg)
    measured = sensor_scale * _rotation(-physical_angle).dot(truth) + sensor_bias
    used_angle = mounting_deg if broken else physical_angle
    used_vector = measured if broken else (measured - sensor_bias) / sensor_scale
    body = _rotation(used_angle).dot(used_vector)
    yaw_measured = 12.0 + bias
    yaw = yaw_measured if broken else yaw_measured - bias
    norm_closure = abs(np.linalg.norm(body) - np.linalg.norm(used_vector))
    residual = float(np.linalg.norm(body - truth) + abs(yaw - 12.0))
    return [float(body[0]), float(body[1]), float(yaw), float(norm_closure), residual]


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    signature = _state(p["yaw_bias_deg_s"], p["mounting_yaw_deg"], broken)
    angles = np.linspace(-15.0, 15.0, 61); ax, ay = [], []
    for angle in angles:
        state = _state(p["yaw_bias_deg_s"], float(angle), broken); ax.append(state[0]); ay.append(state[1])
    biases = np.linspace(-3.0, 3.0, 61); yaw = [_state(float(value), p["mounting_yaw_deg"], broken)[2] for value in biases]
    return {
        "signature": signature,
        "metrics": [("body_ax", "Body longitudinal acceleration", signature[0], "m/s^2"), ("body_ay", "Body lateral acceleration", signature[1], "m/s^2"), ("yaw_rate", "Calibrated yaw rate", signature[2], "deg/s"), ("norm_closure", "Rotation norm closure", signature[3], "m/s^2"), ("calibration_residual", "Calibration residual", signature[4], "mixed")],
        "plots": {"response": _plot("Mounting-angle calibration", "Mounting yaw (deg)", "Body acceleration (m/s^2)", [_trace("Longitudinal", angles, ax, "Mounting yaw", "deg", "Body acceleration", "m/s^2"), _trace("Lateral", angles, ay, "Mounting yaw", "deg", "Body acceleration", "m/s^2")]), "mechanism": _plot("Yaw-bias removal", "Declared yaw bias (deg/s)", "Calibrated yaw rate (deg/s)", [_trace("Calibrated yaw rate", biases, yaw, "Declared yaw bias", "deg/s", "Calibrated yaw rate", "deg/s")])},
        "observation": "Calibration removes bias and scale in sensor coordinates before a norm-preserving rotation maps the measurement into forward-left body axes.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters); broken = bool(parameters.get("broken_mode", False)); return _result(_model(values, broken), broken)
