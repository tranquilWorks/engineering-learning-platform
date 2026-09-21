from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 15
BROKEN_TEXT = "The broken case introduces a persistent 0.15 m measurement bias."
RECOVERY_TEXT = "Disable the broken case and correct the sensor bias before trusting the state estimate."

PLOT_SPECS = {
    "response": {
        "title": "True and observed position",
        "axes": {"x": "Time (s)", "y": "Position (m)"},
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "True position",
                "y_unit": "m",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Estimated position",
                "y_unit": "m",
                "xaxis": "x",
                "yaxis": "y",
            },
        ],
    },
    "mechanism": {
        "title": "Observer error components",
        "axes": {"x": "Time (s)", "y": "Position error (m)", "y2": "Rate error (m/s)"},
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Position error",
                "y_unit": "m",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Rate error",
                "y_unit": "m/s",
                "xaxis": "x",
                "yaxis": "y2",
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
    speed = float(parameters["observer_speed_per_s"])
    bias = 0.15 if broken_mode else float(parameters["sensor_bias_m"])
    dt = 0.02
    t = np.arange(0, 8 + dt / 2, dt)
    x = np.zeros((len(t), 2))
    x[0] = [0.8, -0.1]
    xh = np.zeros_like(x)
    xh[0] = [-0.4, 0.4]
    L = np.array([2 * speed, speed**2])
    for i in range(len(t) - 1):
        u = 0.4
        x[i + 1] = x[i] + dt * np.array([x[i, 1], u])
        innovation = x[i, 0] + bias - xh[i, 0]
        xh[i + 1] = xh[i] + dt * (np.array([xh[i, 1], u]) + L * innovation)
    err = x - xh
    rms = np.sqrt(np.mean(err[:, 0] ** 2))
    return result(
        broken_mode,
        t,
        [
            trace("True position", t, x[:, 0]),
            trace("Estimated position", t, xh[:, 0], "dash"),
        ],
        [trace("Position error", t, err[:, 0]), trace("Rate error", t, err[:, 1])],
        [
            ("position_rmse", "Position RMSE", rms, "m"),
            ("final_position_error", "Final position error", err[-1, 0], "m"),
            ("final_rate_error", "Final rate error", err[-1, 1], "m/s"),
        ],
        [speed, bias, rms, err[-1, 0], err[-1, 1]],
        "The innovation drives both estimated states; persistent sensor bias therefore becomes persistent state-estimate bias.",
    )


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
