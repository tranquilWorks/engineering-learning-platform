from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 59
BROKEN_TEXT = "Omit the declared 95-percent bias correction while keeping the same sensor bias and coast duration."
RECOVERY_TEXT = (
    "Restore correction and compare both paths over the same selected coast interval."
)


def _trace(
    name: str,
    x: Any,
    y: Any,
    x_quantity: str,
    x_unit: str,
    y_quantity: str,
    y_unit: str,
    *,
    mode: str = "lines",
) -> dict[str, Any]:
    return {
        "type": "scattergl",
        "mode": mode,
        "name": name,
        "x": np.asarray(x, dtype=float),
        "y": np.asarray(y, dtype=float),
        "meta": {
            "x_quantity": x_quantity,
            "x_unit": x_unit,
            "y_quantity": y_quantity,
            "y_unit": y_unit,
        },
    }


def _plot(
    title: str, x_title: str, y_title: str, traces: list[dict[str, Any]]
) -> dict[str, Any]:
    return {
        "data": traces,
        "layout": {
            "title": {"text": title, "x": 0.02},
            "xaxis": {"title": {"text": x_title}},
            "yaxis": {"title": {"text": y_title}},
            "legend": {"orientation": "h"},
            "margin": {"l": 72, "r": 36, "t": 62, "b": 62},
            "hovermode": "closest",
            "uirevision": "keep-view",
        },
        "config": {"responsive": True, "displaylogo": False},
    }


def _result(model: dict[str, Any], broken: bool) -> dict[str, Any]:
    return {
        "metrics": [
            {
                "id": key,
                "label": label,
                "value": float(value),
                "unit": unit,
                "emphasis": "primary" if index == 0 else "normal",
            }
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
            **model.get("history", {}),
        },
    }


def _model(p, broken):
    bias = float(p["accelerometer_bias_m_s2"])
    duration = float(p["coast_duration_s"])
    time = np.linspace(0, duration, 241)
    dt = duration / 240
    residual = bias if broken else 0.05 * bias
    velocity = np.zeros(241)
    position = np.zeros(241)
    corrected_v = np.zeros(241)
    corrected_p = np.zeros(241)
    for k in range(240):
        position[k + 1] = position[k] + velocity[k] * dt + 0.5 * bias * dt * dt
        velocity[k + 1] = velocity[k] + bias * dt
        corrected_p[k + 1] = (
            corrected_p[k] + corrected_v[k] * dt + 0.5 * residual * dt * dt
        )
        corrected_v[k + 1] = corrected_v[k] + residual * dt
    return {
        "signature": [velocity[-1], position[-1], corrected_p[-1]],
        "metrics": [
            ("velocity_error", "Uncorrected velocity error", velocity[-1], "m/s"),
            ("position_error", "Uncorrected position error", position[-1], "m"),
            (
                "corrected_position_error",
                "Residual-bias position error",
                corrected_p[-1],
                "m",
            ),
        ],
        "history": {
            "time": time,
            "velocity": velocity,
            "position": position,
            "corrected_velocity": corrected_v,
            "corrected_position": corrected_p,
            "residual_bias": residual,
        },
        "plots": {
            "response": _plot(
                "Velocity bias error",
                "Coast time (s)",
                "Velocity error (m/s)",
                [
                    _trace(
                        "Uncorrected",
                        time,
                        velocity,
                        "Coast time",
                        "s",
                        "Velocity error",
                        "m/s",
                    ),
                    _trace(
                        "Bias corrected",
                        time,
                        corrected_v,
                        "Coast time",
                        "s",
                        "Velocity error",
                        "m/s",
                    ),
                ],
            ),
            "mechanism": _plot(
                "Position bias error",
                "Coast time (s)",
                "Position error (m)",
                [
                    _trace(
                        "Uncorrected",
                        time,
                        position,
                        "Coast time",
                        "s",
                        "Position error",
                        "m",
                    ),
                    _trace(
                        "Bias corrected",
                        time,
                        corrected_p,
                        "Coast time",
                        "s",
                        "Position error",
                        "m",
                    ),
                ],
            ),
        },
        "observation": f"Both paths integrate the same {bias:g} m/s^2 bias over {duration:g} s. The declared correction leaves {residual:g} m/s^2; fault mode omits that correction. This one-axis bias propagation assumes known fixed attitude and zero true acceleration; no quaternion, Earth rotation, gravity compensation or full strapdown mechanization is executed.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
