from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 18
BROKEN_TEXT = "The broken case reverses feedforward sign, commanding acceleration away from the plan."
RECOVERY_TEXT = "Disable the broken case and verify inverse-model sign conventions."

PLOT_SPECS = {
    "response": {
        "title": "Feedforward-plus-feedback tracking",
        "axes": {"x": "Time (s)", "y": "Position (m)"},
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Desired position",
                "y_unit": "m",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Actual position",
                "y_unit": "m",
                "xaxis": "x",
                "yaxis": "y",
            },
        ],
    },
    "mechanism": {
        "title": "Acceleration-command decomposition",
        "axes": {"x": "Time (s)", "y": "Acceleration (m/s²)"},
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Feedforward acceleration",
                "y_unit": "m/s²",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Feedback acceleration",
                "y_unit": "m/s²",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Disturbance acceleration",
                "y_unit": "m/s²",
                "xaxis": "x",
                "yaxis": "y",
            },
        ],
    },
}


def layout(spec: dict[str, Any]) -> dict[str, Any]:
    value: dict[str, Any] = {
        "title": {"text": spec["title"], "x": 0.02},
        "legend": {"orientation": "h"},
        "margin": {"l": 72, "r": 90, "t": 62, "b": 62},
        "hovermode": "closest",
        "uirevision": "keep-view",
    }
    for axis_id, title in spec["axes"].items():
        axis_key = f"{axis_id[0]}axis{axis_id[1:]}"
        axis: dict[str, Any] = {"title": {"text": title}}
        if axis_id.startswith("x") and axis_id != "x":
            axis.update({"overlaying": "x", "side": "top"})
        if axis_id.startswith("y") and axis_id != "y":
            axis.update({"overlaying": "y", "side": "right"})
            if axis_id == "y3":
                axis.update({"anchor": "free", "position": 0.88})
        value[axis_key] = axis
    return value


def trace(name: str, x: Any, y: Any, dash: str | None = None) -> dict[str, Any]:
    item = {"type": "scattergl", "mode": "lines", "name": name, "x": x, "y": y}
    if dash:
        item["line"] = {"dash": dash}
    return item


def make_plot(key: str, traces: list[dict[str, Any]]) -> dict[str, Any]:
    spec = PLOT_SPECS[key]
    if len(traces) != len(spec["traces"]):
        raise ValueError(f"{key} trace metadata does not match the plotted traces")
    data: list[dict[str, Any]] = []
    for item, metadata in zip(traces, spec["traces"], strict=True):
        plotted = dict(item)
        plotted["meta"] = {
            "x_quantity": metadata["x_quantity"],
            "x_unit": metadata["x_unit"],
            "y_quantity": metadata["y_quantity"],
            "y_unit": metadata["y_unit"],
        }
        if metadata["xaxis"] != "x":
            plotted["xaxis"] = metadata["xaxis"]
        if metadata["yaxis"] != "y":
            plotted["yaxis"] = metadata["yaxis"]
        data.append(plotted)
    return {
        "data": data,
        "layout": layout(spec),
        "config": {"responsive": True, "displaylogo": False},
    }


def result(
    broken_active: bool,
    t: np.ndarray,
    response: list[dict[str, Any]],
    mechanism: list[dict[str, Any]],
    metrics: list[tuple[str, str, float, str]],
    signature: list[float],
    observation: str,
) -> dict[str, Any]:
    del t
    return {
        "metrics": [
            {
                "id": key,
                "label": label,
                "value": float(value),
                "unit": unit,
                "emphasis": "primary" if i == 0 else "normal",
            }
            for i, (key, label, value, unit) in enumerate(metrics)
        ],
        "plots": {
            "response": make_plot("response", response),
            "mechanism": make_plot("mechanism", mechanism),
        },
        "explanations": {
            "observation": observation,
            "broken": BROKEN_TEXT,
            "recovery": RECOVERY_TEXT,
        },
        "diagnostics": {
            "item_number": ITEM_NUMBER,
            "broken_active": bool(broken_active),
            "signature": [float(v) for v in signature],
        },
    }


def _simulate(parameters: dict[str, Any], broken_mode: bool) -> dict[str, Any]:
    ff = float(parameters["feedforward_scale"])
    fb = float(parameters["feedback_scale"])
    sign = -1 if broken_mode else 1
    dt = 0.02
    t = np.arange(0, 12 + dt / 2, dt)
    xd = np.sin(0.5 * t)
    vd = 0.5 * np.cos(0.5 * t)
    ad = -0.25 * np.sin(0.5 * t)
    x = np.zeros_like(t)
    v = np.zeros_like(t)
    u = np.zeros_like(t)
    d = np.where(t >= 6, -0.4, 0.0)
    for i in range(len(t) - 1):
        u[i] = sign * ff * ad[i] + fb * (4 * (xd[i] - x[i]) + 3 * (vd[i] - v[i]))
        v[i + 1] = v[i] + dt * (u[i] + d[i])
        x[i + 1] = x[i] + dt * v[i + 1]
    err = xd - x
    rms = np.sqrt(np.mean(err * err))
    return result(
        broken_mode,
        t,
        [trace("Desired position", t, xd, "dash"), trace("Actual position", t, x)],
        [
            trace("Feedforward term", t, sign * ff * ad),
            trace("Feedback correction", t, u - sign * ff * ad),
            trace("Disturbance", t, d),
        ],
        [
            ("tracking_rmse", "Tracking RMSE", rms, "m"),
            ("peak_control", "Peak command", np.max(np.abs(u)), "m/s²"),
            ("final_error", "Final tracking error", err[-1], "m"),
        ],
        [ff, fb, sign, rms, np.max(np.abs(u))],
        "Feedforward handles modeled demand before error appears; feedback remains the channel for mismatch and disturbance.",
    )


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
