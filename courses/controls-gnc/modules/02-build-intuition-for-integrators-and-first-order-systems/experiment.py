from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 2
BROKEN_TEXT = "The broken case uses forward Euler with dt/tau greater than two, creating a discrete pole outside the unit circle."
RECOVERY_TEXT = "Disable the broken case to use the exact first-order transition."

PLOT_SPECS = {
    "response": {
        "title": "Integrator and first-order step responses",
        "axes": {"x": "Time (s)", "y": "Normalized response (ratio)"},
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Integrator response",
                "y_unit": "ratio",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "First-order response",
                "y_unit": "ratio",
                "xaxis": "x",
                "yaxis": "y",
            },
        ],
    },
    "mechanism": {
        "title": "First-order tracking mechanism",
        "axes": {"x": "Time (s)", "y": "Normalized signal (ratio)"},
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "First-order error",
                "y_unit": "ratio",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Input amplitude",
                "y_unit": "ratio",
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
    a = float(parameters["input_amplitude"])
    tau = float(parameters["time_constant_s"])
    t = np.linspace(0, 10, 501)
    integ = a * t
    if broken_mode:
        dt = 3 * tau
        tb = np.arange(0, 10 + dt / 2, dt)
        y = np.zeros_like(tb)
        for i in range(len(tb) - 1):
            y[i + 1] = y[i] + dt * (a - y[i]) / tau
        y = np.interp(t, tb, y)
    else:
        y = a * (1 - np.exp(-t / tau))
    return result(
        broken_mode,
        t,
        [trace("Integrator", t, integ), trace("First order", t, y)],
        [trace("First-order error", t, a - y), trace("Input", t, np.full_like(t, a))],
        [
            ("ramp_slope", "Integrator slope", a, "input/s"),
            ("time_constant", "Time constant", tau, "s"),
            ("final_first_order", "Final first-order output", y[-1], "output"),
        ],
        [a, tau, integ[-1], y[-1], np.max(np.abs(y))],
        "The same step becomes an unbounded ramp through an integrator and a bounded exponential through a first-order state.",
    )


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
