from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 1
BROKEN_TEXT = "The broken case uses an explicit integration step too large for the fastest mode, so numerical energy grows even though the physical system is damped."
RECOVERY_TEXT = (
    "Disable the broken case to restore a time step that resolves the natural period."
)

PLOT_SPECS = {
    "response": {
        "title": "Mass–spring–damper displacement",
        "axes": {"x": "Time (s)", "y": "Position (m)"},
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Displacement",
                "y_unit": "m",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Static equilibrium",
                "y_unit": "m",
                "xaxis": "x",
                "yaxis": "y",
            },
        ],
    },
    "mechanism": {
        "title": "Phase state and mechanical energy",
        "axes": {
            "x": "Position (m)",
            "y": "Velocity (m/s)",
            "x2": "Time (s)",
            "y2": "Mechanical energy (J)",
        },
        "traces": [
            {
                "x_quantity": "Position",
                "x_unit": "m",
                "y_quantity": "Velocity",
                "y_unit": "m/s",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Mechanical energy",
                "y_unit": "J",
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
    m = float(parameters["mass_kg"])
    c = float(parameters["damping_ns_m"])
    k = float(parameters["stiffness_n_m"])
    dt = 1.0 if broken_mode else 0.01
    t = np.arange(0.0, 12.0 + dt / 2, dt)
    x = np.zeros_like(t)
    v = np.zeros_like(t)
    force = 1.0
    for i in range(len(t) - 1):
        a = (force - c * v[i] - k * x[i]) / m
        if broken_mode:
            x[i + 1] = x[i] + dt * v[i]
            v[i + 1] = v[i] + dt * a
        else:
            v[i + 1] = v[i] + dt * a
            x[i + 1] = x[i] + dt * v[i + 1]
    energy = 0.5 * m * v * v + 0.5 * k * x * x
    wn = np.sqrt(k / m)
    zeta = c / (2 * np.sqrt(k * m))
    return result(
        broken_mode,
        t,
        [
            trace("Displacement", t, x),
            trace("Steady F/k", t, np.full_like(t, force / k), "dash"),
        ],
        [trace("Velocity", x, v), trace("Energy", t, energy)],
        [
            ("natural_frequency", "Natural frequency", wn, "rad/s"),
            ("damping_ratio", "Damping ratio", zeta, "ratio"),
            ("final_displacement", "Final displacement", x[-1], "m"),
        ],
        [wn, zeta, x[-1], np.max(np.abs(x)), energy[-1]],
        "Mass slows acceleration, stiffness sets equilibrium and frequency, and damping removes mechanical energy.",
    )


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
