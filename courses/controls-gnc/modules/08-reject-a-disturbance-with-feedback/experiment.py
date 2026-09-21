from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 8
BROKEN_TEXT = (
    "The broken case injects a 0.5-unit sensor bias with no physical disturbance."
)
RECOVERY_TEXT = "Disable the broken case and validate/calibrate the sensor bias."

PLOT_SPECS = {
    "response": {
        "title": "Disturbance rejection response",
        "axes": {
            "x": "Time (s)",
            "y": "Plant disturbance (normalized input)",
            "y2": "True output (normalized output)",
        },
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Plant disturbance",
                "y_unit": "normalized input",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "True output",
                "y_unit": "normalized output",
                "xaxis": "x",
                "yaxis": "y2",
            },
        ],
    },
    "mechanism": {
        "title": "Measurement and feedback command",
        "axes": {
            "x": "Time (s)",
            "y": "Measured output (normalized output)",
            "y2": "Control command (normalized input)",
        },
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Measured output",
                "y_unit": "normalized output",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Control command",
                "y_unit": "normalized input",
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
    K = float(parameters["feedback_gain"])
    omega = float(parameters["disturbance_frequency_rad_s"])
    bias = 0.5 if broken_mode else 0.0
    dt = 0.005
    t = np.arange(0, 12 + dt / 2, dt)
    y = np.zeros_like(t)
    d = np.where(t >= 1, np.ones_like(t) if omega == 0 else np.sin(omega * (t - 1)), 0)
    u = np.zeros_like(t)
    for i in range(len(t) - 1):
        u[i] = -K * (y[i] + (bias if t[i] >= 1 else 0))
        y[i + 1] = y[i] + dt * (-y[i] + u[i] + d[i])
        u[-1] = -K * (y[-1] + bias)
    atten = 1 / np.sqrt((1 + K) ** 2 + omega**2)
    return result(
        broken_mode,
        t,
        [trace("Disturbance", t, d, "dash"), trace("True output", t, y)],
        [
            trace("Measured output", t, y + bias * (t >= 1)),
            trace("Control effort", t, u),
        ],
        [
            ("attenuation", "Theoretical disturbance gain", atten, "output/input"),
            ("peak_output", "Peak true output", np.max(np.abs(y)), "output"),
            ("peak_control", "Peak control", np.max(np.abs(u)), "actuator"),
        ],
        [K, omega, bias, atten, y[-1], np.max(np.abs(u))],
        "Feedback rejects plant disturbance through sensitivity, but a biased measurement drives a real and costly correction.",
    )


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
