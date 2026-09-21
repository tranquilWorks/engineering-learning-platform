from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 20
BROKEN_TEXT = "The broken case reverses actuator sign, which lies outside the declared positive gain/drag family used for this two-gain comparison."
RECOVERY_TEXT = "Disable the broken case to restore positive actuator polarity. The comparison is empirical over the displayed family; it is not a synthesis or certification result."

PLOT_SPECS = {
    "response": {
        "title": "Two fixed-gain speed responses",
        "axes": {"x": "Time (s)", "y": "Speed (m/s)"},
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Gain-2 speed",
                "y_unit": "m/s",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Gain-4 speed",
                "y_unit": "m/s",
                "xaxis": "x",
                "yaxis": "y",
            },
        ],
    },
    "mechanism": {
        "title": "Two fixed-gain commands",
        "axes": {"x": "Time (s)", "y": "Commanded acceleration (m/s²)"},
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Gain-2 command",
                "y_unit": "m/s²",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Gain-4 command",
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
    ga = float(parameters["actuator_gain_ratio"])
    drag = float(parameters["drag_ratio"])
    sign = -1 if broken_mode else 1
    dt = 0.02
    t = np.arange(0, 12 + dt / 2, dt)
    yn = np.zeros_like(t)
    yr = np.zeros_like(t)
    un = np.zeros_like(t)
    ur = np.zeros_like(t)
    for i in range(len(t) - 1):
        un[i] = 2 * (1 - yn[i])
        ur[i] = 4 * (1 - yr[i])
        yn[i + 1] = yn[i] + dt * (-drag * yn[i] + sign * ga * un[i])
        yr[i + 1] = yr[i] + dt * (-drag * yr[i] + sign * ga * ur[i])
    jn = np.trapezoid((1 - yn) ** 2 + 0.05 * un**2, t)
    jr = np.trapezoid((1 - yr) ** 2 + 0.05 * ur**2, t)
    return result(
        broken_mode,
        t,
        [trace("Fixed gain K=2", t, yn), trace("Fixed gain K=4", t, yr)],
        [trace("K=2 command", t, un), trace("K=4 command", t, ur)],
        [
            ("gain_2_objective", "K=2 finite-horizon objective", jn, "s"),
            ("gain_4_objective", "K=4 finite-horizon objective", jr, "s"),
            ("gain_4_final_error", "K=4 final speed error", 1 - yr[-1], "m/s"),
        ],
        [ga, drag, sign, jn, jr, yr[-1]],
        "These are two preselected proportional gains evaluated at the selected gain/drag point. The result builds robustness intuition only; it is not the source's finite minimax PI selection, a general robust-control synthesis, or a certification.",
    )


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
