from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 4
BROKEN_TEXT = "The broken case forces a 120 degree release while interpreting the small-angle trace as truth."
RECOVERY_TEXT = "Disable the broken case or reduce the release angle until the approximation error is acceptable."

PLOT_SPECS = {
    "response": {
        "title": "Linear and nonlinear pendulum angles",
        "axes": {"x": "Time (s)", "y": "Angular displacement (deg)"},
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Nonlinear angle",
                "y_unit": "deg",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Linear angle",
                "y_unit": "deg",
                "xaxis": "x",
                "yaxis": "y",
            },
        ],
    },
    "mechanism": {
        "title": "Approximation error and nonlinear phase state",
        "axes": {
            "x": "Time (s)",
            "y": "Angular model gap (deg)",
            "x2": "Angular displacement (deg)",
            "y2": "Angular rate (deg/s)",
        },
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Angular model gap",
                "y_unit": "deg",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Angular displacement",
                "x_unit": "deg",
                "y_quantity": "Angular rate",
                "y_unit": "deg/s",
                "xaxis": "x2",
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
    angle = np.deg2rad(120.0 if broken_mode else float(parameters["initial_angle_deg"]))
    length = float(parameters["length_m"])
    dt = 0.01
    t = np.arange(0, 12 + dt / 2, dt)
    nl = np.zeros_like(t)
    nv = np.zeros_like(t)
    li = np.zeros_like(t)
    lv = np.zeros_like(t)
    nl[0] = li[0] = angle
    w2 = 9.81 / length
    z = 0.02
    for i in range(len(t) - 1):
        nv[i + 1] = nv[i] + dt * (-2 * z * np.sqrt(w2) * nv[i] - w2 * np.sin(nl[i]))
        nl[i + 1] = nl[i] + dt * nv[i + 1]
        lv[i + 1] = lv[i] + dt * (-2 * z * np.sqrt(w2) * lv[i] - w2 * li[i])
        li[i + 1] = li[i] + dt * lv[i + 1]
    gap = np.max(np.abs(nl - li))
    return result(
        broken_mode,
        t,
        [
            trace("Nonlinear sin(theta)", t, np.rad2deg(nl)),
            trace("Linear theta", t, np.rad2deg(li), "dash"),
        ],
        [
            trace("Model gap", t, np.rad2deg(nl - li)),
            trace("Phase portrait", np.rad2deg(nl), np.rad2deg(nv)),
        ],
        [
            ("small_angle_gap", "Maximum model gap", np.rad2deg(gap), "deg"),
            ("linear_period", "Linear period", 2 * np.pi / np.sqrt(w2), "s"),
            ("release_angle", "Release angle", np.rad2deg(angle), "deg"),
        ],
        [angle, length, gap, nl[-1], li[-1]],
        "The linear and nonlinear plants share their initial state; their divergence isolates the small-angle assumption.",
    )


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
