from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 9
BROKEN_TEXT = "The broken case combines coarse sampling with the less forgiving forward-error integral update."
RECOVERY_TEXT = "Disable the broken case and reduce the controller sample period."

PLOT_SPECS = {
    "response": {
        "title": "Sampled PI response versus continuous target",
        "axes": {"x": "Time (s)", "y": "Normalized plant output (ratio)"},
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Digital PI output",
                "y_unit": "ratio",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Continuous target output",
                "y_unit": "ratio",
                "xaxis": "x",
                "yaxis": "y",
            },
        ],
    },
    "mechanism": {
        "title": "Held command and discrete integral state",
        "axes": {
            "x": "Time (s)",
            "y": "Held command (normalized input)",
            "y2": "Integral state (ratio·s)",
        },
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Held command",
                "y_unit": "normalized input",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Integral state",
                "y_unit": "ratio·s",
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
    Ts = 0.3 if broken_mode else float(parameters["sample_period_s"])
    ki = float(parameters["integral_gain"])
    kp = 2.0
    t = np.arange(0, 12 + Ts / 2, Ts)
    y = np.zeros_like(t)
    q = np.zeros_like(t)
    u = np.zeros_like(t)
    a = np.exp(-Ts)
    for k in range(len(t) - 1):
        e = 1 - y[k]
        q[k + 1] = q[k] + Ts * (q[k - 1] if broken_mode and k > 0 else e)
        u[k] = kp * e + ki * q[k]
        y[k + 1] = a * y[k] + (1 - a) * u[k]
    u[-1] = kp * (1 - y[-1]) + ki * q[-1]
    fine = np.linspace(0, 12, 1201)
    target = 1 - np.exp(-2 * fine) * (np.cos(2 * fine) + np.sin(2 * fine))
    return result(
        broken_mode,
        t,
        [trace("Digital PI", t, y), trace("Continuous target", fine, target, "dash")],
        [trace("Held command", t, u), trace("Integral state", t, q)],
        [
            ("sample_rate", "Controller sample rate", 1 / Ts, "Hz"),
            ("final_error", "Final digital error", 1 - y[-1], "output"),
            ("peak_output", "Peak digital output", np.max(np.abs(y)), "output"),
        ],
        [Ts, ki, y[-1], np.max(np.abs(y)), np.max(np.abs(u))],
        "Exact plant holds do not remove controller discretization: the integral rule and sample period still move closed-loop poles.",
    )


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
