from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 22
BROKEN_TEXT = "The broken case limits lateral acceleration to 5 m/s², preventing intercept in the modeled engagement."
RECOVERY_TEXT = (
    "Disable the broken case and restore the 80 m/s² authority used by the baseline."
)

PLOT_SPECS = {
    "response": {
        "title": "Proportional-navigation engagement geometry",
        "axes": {"x": "Time (s)", "y": "Range (m)", "y2": "Line-of-sight angle (deg)"},
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Range",
                "y_unit": "m",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Line-of-sight angle",
                "y_unit": "deg",
                "xaxis": "x",
                "yaxis": "y2",
            },
        ],
    },
    "mechanism": {
        "title": "Lateral-acceleration authority",
        "axes": {"x": "Time (s)", "y": "Lateral acceleration (m/s²)"},
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Lateral acceleration",
                "y_unit": "m/s²",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Acceleration limit",
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
    N = float(parameters["navigation_constant"])
    limit = 5.0 if broken_mode else float(parameters["maximum_acceleration_m_s2"])
    dt = 0.02
    steps = int(25 / dt) + 1
    t = np.arange(steps) * dt
    p = np.array([0.0, 0.0])
    heading = 0.0
    speed = 300.0
    target = np.array([5000.0, 600.0])
    tv = np.array([-60.0, 0.0])
    rng = np.zeros(steps)
    accel = np.zeros(steps)
    los = np.zeros(steps)
    hit = False
    end = steps
    for i in range(steps):
        rel = target - p
        rng[i] = np.linalg.norm(rel)
        los[i] = np.arctan2(rel[1], rel[0])
        if rng[i] < 5:
            hit = True
            end = i + 1
            break
        iv = speed * np.array([np.cos(heading), np.sin(heading)])
        rv = tv - iv
        closing = -np.dot(rel, rv) / max(rng[i], 1e-9)
        rate = (rel[0] * rv[1] - rel[1] * rv[0]) / max(rng[i] ** 2, 1e-9)
        accel[i] = np.clip(N * closing * rate, -limit, limit)
        heading += dt * accel[i] / speed
        p += dt * speed * np.array([np.cos(heading), np.sin(heading)])
        target += dt * tv
    t = t[:end]
    rng = rng[:end]
    accel = accel[:end]
    los = los[:end]
    miss = np.min(rng)
    return result(
        broken_mode,
        t,
        [trace("Range", t, rng), trace("LOS angle", t, np.degrees(los))],
        [
            trace("Lateral acceleration", t, accel),
            trace("Acceleration limit", t, np.full_like(t, limit), "dash"),
        ],
        [
            ("miss_distance", "Minimum range", miss, "m"),
            ("intercept", "Intercept (1=yes)", float(hit), "flag"),
            (
                "peak_acceleration",
                "Peak lateral acceleration",
                np.max(np.abs(accel)),
                "m/s²",
            ),
        ],
        [N, limit, miss, float(hit), np.max(np.abs(accel))],
        "PN steers by cancelling line-of-sight rotation; acceleration clipping reveals whether the geometry is physically achievable.",
    )


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
