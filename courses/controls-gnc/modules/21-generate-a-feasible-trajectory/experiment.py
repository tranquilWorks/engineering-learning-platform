from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 21
BROKEN_TEXT = "The broken case forces the 20 m move into 4 s, exceeding the declared speed/acceleration limits."
RECOVERY_TEXT = (
    "Disable the broken case and lengthen the move until both constraints pass."
)

PLOT_SPECS = {
    "response": {
        "title": "Quintic trajectory and derivatives",
        "axes": {
            "x": "Time (s)",
            "y": "Position (m)",
            "y2": "Velocity (m/s)",
            "y3": "Acceleration (m/s²)",
        },
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Position",
                "y_unit": "m",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Velocity",
                "y_unit": "m/s",
                "xaxis": "x",
                "yaxis": "y2",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Acceleration",
                "y_unit": "m/s²",
                "xaxis": "x",
                "yaxis": "y3",
            },
        ],
    },
    "mechanism": {
        "title": "Declared trajectory limits",
        "axes": {
            "x": "Time (s)",
            "y": "Speed limit (m/s)",
            "y2": "Acceleration limit (m/s²)",
        },
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Speed limit",
                "y_unit": "m/s",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Acceleration limit",
                "y_unit": "m/s²",
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
    target = 20.0 if broken_mode else float(parameters["target_position_m"])
    T = 4.0 if broken_mode else float(parameters["move_duration_s"])
    t = np.linspace(0, T, 501)
    s = t / T
    x = target * (10 * s**3 - 15 * s**4 + 6 * s**5)
    v = target / T * (30 * s**2 - 60 * s**3 + 30 * s**4)
    a = target / T**2 * (60 * s - 180 * s**2 + 120 * s**3)
    feasible = bool(np.max(np.abs(v)) <= 5 and np.max(np.abs(a)) <= 2)
    return result(
        broken_mode,
        t,
        [trace("Position", t, x), trace("Velocity", t, v), trace("Acceleration", t, a)],
        [
            trace("Speed limit", t, np.full_like(t, 5), "dash"),
            trace("Acceleration limit", t, np.full_like(t, 2), "dash"),
        ],
        [
            ("peak_speed", "Peak speed", np.max(np.abs(v)), "m/s"),
            ("peak_acceleration", "Peak acceleration", np.max(np.abs(a)), "m/s²"),
            ("feasible", "Feasible (1=yes)", float(feasible), "flag"),
        ],
        [target, T, np.max(np.abs(v)), np.max(np.abs(a)), float(feasible)],
        "The quintic guarantees smooth endpoints, but only explicit derivative checks establish actuator feasibility.",
    )


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
