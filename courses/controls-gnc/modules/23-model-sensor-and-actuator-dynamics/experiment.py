from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 23
BROKEN_TEXT = "The broken case combines slow actuator/sensor dynamics with a command that reverses every 0.1 s."
RECOVERY_TEXT = (
    "Disable the broken case and slow the command or increase component bandwidth."
)

PLOT_SPECS = {
    "response": {
        "title": "Actuator and sensor acceleration dynamics",
        "axes": {"x": "Time (s)", "y": "Acceleration (m/s²)"},
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Commanded acceleration",
                "y_unit": "m/s²",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Actual acceleration",
                "y_unit": "m/s²",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Measured acceleration",
                "y_unit": "m/s²",
                "xaxis": "x",
                "yaxis": "y",
            },
        ],
    },
    "mechanism": {
        "title": "Actuator and sensor lag errors",
        "axes": {"x": "Time (s)", "y": "Acceleration error (m/s²)"},
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Actuator tracking error",
                "y_unit": "m/s²",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Sensor dynamic error",
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
    ta = 0.8 if broken_mode else float(parameters["actuator_time_constant_s"])
    ts = 0.6 if broken_mode else float(parameters["sensor_time_constant_s"])
    half = 0.1 if broken_mode else 2.0
    dt = 0.01
    t = np.arange(0, 8 + dt / 2, dt)
    cmd = 20 * np.where((np.floor(t / half) % 2) == 0, 1, -1)
    act = np.zeros_like(t)
    sense = np.zeros_like(t)
    for i in range(len(t) - 1):
        act[i + 1] = act[i] + (1 - np.exp(-dt / ta)) * (
            np.clip(cmd[i], -30, 30) - act[i]
        )
        sense[i + 1] = sense[i] + (1 - np.exp(-dt / ts)) * (act[i] - sense[i])
    lag = np.sqrt(np.mean((cmd - sense) ** 2))
    return result(
        broken_mode,
        t,
        [
            trace("Command", t, cmd, "dash"),
            trace("Actuator", t, act),
            trace("Sensor", t, sense),
        ],
        [
            trace("Actuator error", t, cmd - act),
            trace("Sensor lag error", t, act - sense),
        ],
        [
            ("chain_rmse", "Command-to-sensor RMSE", lag, "m/s²"),
            ("actuator_bandwidth", "Actuator bandwidth", 1 / ta, "rad/s"),
            ("sensor_bandwidth", "Sensor bandwidth", 1 / ts, "rad/s"),
        ],
        [ta, ts, half, lag, act[-1], sense[-1]],
        "Two first-order acceleration states create distinct actuator and sensor lag; plotting both prevents sensor dynamics from being mistaken for actuator failure.",
    )


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
