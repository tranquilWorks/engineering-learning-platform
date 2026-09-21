from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 11
BROKEN_TEXT = "The broken case restricts a 1.5-unit request to 0.6 actuator units."
RECOVERY_TEXT = (
    "Disable the broken case or reduce the command to fit available authority."
)

PLOT_SPECS = {
    "response": {
        "title": "Actuator-limited plant response",
        "axes": {"x": "Time (s)", "y": "Normalized plant output (ratio)"},
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Limited output",
                "y_unit": "ratio",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Reference",
                "y_unit": "ratio",
                "xaxis": "x",
                "yaxis": "y",
            },
        ],
    },
    "mechanism": {
        "title": "Requested versus applied actuator command",
        "axes": {"x": "Time (s)", "y": "Normalized actuator command (ratio)"},
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Requested command",
                "y_unit": "ratio",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Applied command",
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
    r = 1.5 if broken_mode else float(parameters["reference"])
    limit = 0.6 if broken_mode else float(parameters["actuator_limit"])
    dt = 0.01
    t = np.arange(0, 6 + dt / 2, dt)
    y = np.zeros_like(t)
    req = np.zeros_like(t)
    applied = np.zeros_like(t)
    for i in range(len(t) - 1):
        req[i] = 4 * (r - y[i])
        applied[i] = np.clip(req[i], -limit, limit)
        y[i + 1] = y[i] + dt * (-y[i] + applied[i])
    req[-1] = 4 * (r - y[-1])
    applied[-1] = np.clip(req[-1], -limit, limit)
    sat = np.mean(np.abs(req - applied) > 1e-12)
    return result(
        broken_mode,
        t,
        [
            trace("Limited output", t, y),
            trace("Reference", t, np.full_like(t, r), "dash"),
        ],
        [trace("Requested", t, req, "dash"), trace("Applied", t, applied)],
        [
            ("saturation_fraction", "Time saturated", 100 * sat, "%"),
            ("final_error", "Final error", r - y[-1], "output"),
            ("peak_request", "Peak requested command", np.max(np.abs(req)), "actuator"),
        ],
        [r, limit, sat, y[-1], np.max(np.abs(req))],
        "The clipping gap is a physical statement: requested control is not applied control.",
    )


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
