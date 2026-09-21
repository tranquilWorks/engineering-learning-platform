from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 10
BROKEN_TEXT = "The broken case uses a 0.2 s period with 90 percent computation delay."
RECOVERY_TEXT = (
    "Disable the broken case and schedule computation early in the sample interval."
)

PLOT_SPECS = {
    "response": {
        "title": "Sampled response with computation delay",
        "axes": {"x": "Time (s)", "y": "Normalized plant output (ratio)"},
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Sampled output",
                "y_unit": "ratio",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Continuous equilibrium",
                "y_unit": "ratio",
                "xaxis": "x",
                "yaxis": "y",
            },
        ],
    },
    "mechanism": {
        "title": "Delayed command and equilibrium error",
        "axes": {
            "x": "Time (s)",
            "y": "Applied command (normalized input)",
            "y2": "Equilibrium error (ratio)",
        },
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Applied command",
                "y_unit": "normalized input",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Equilibrium error",
                "y_unit": "ratio",
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
    Ts = 0.2 if broken_mode else float(parameters["sample_period_s"])
    frac = 0.9 if broken_mode else float(parameters["delay_fraction"])
    delay = Ts * frac
    dt = 0.005
    t = np.arange(0, 4 + dt / 2, dt)
    y = np.zeros_like(t)
    u = np.zeros_like(t)
    computed = 0.0
    previous = 0.0
    next_sample = 0.0
    switch = 0.0
    for i in range(len(t) - 1):
        if t[i] + 1e-12 >= next_sample:
            previous = u[i - 1] if i else 0.0
            computed = 8 * (1 - y[i])
            switch = t[i] + delay
            next_sample += Ts
        u[i] = previous if t[i] < switch else computed
        y[i + 1] = y[i] + dt * (-y[i] + u[i])
    u[-1] = u[-2]
    eq = 8 / 9
    return result(
        broken_mode,
        t,
        [
            trace("Sampled output", t, y),
            trace("Continuous equilibrium", t, np.full_like(t, eq), "dash"),
        ],
        [trace("Applied command", t, u), trace("Equilibrium error", t, y - eq)],
        [
            ("sample_rate", "Sample rate", 1 / Ts, "Hz"),
            ("delay", "Computation delay", delay, "s"),
            ("peak_output", "Peak output", np.max(y), "output"),
        ],
        [Ts, frac, delay, y[-1], np.max(y)],
        "The plant sees old command during computation; coarse sampling and latency therefore combine rather than act independently.",
    )


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
