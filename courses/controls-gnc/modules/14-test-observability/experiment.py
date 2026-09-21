from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 14
BROKEN_TEXT = "The broken case measures rate only, so initial position never appears in the output."
RECOVERY_TEXT = (
    "Disable the broken case to measure position and restore full observability."
)

PLOT_SPECS = {
    "response": {
        "title": "Measurement history and position truth",
        "axes": {"x": "Time (s)", "y": "Position-equivalent measurement (m)"},
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Measurement",
                "y_unit": "m",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Position truth",
                "y_unit": "m",
                "xaxis": "x",
                "yaxis": "y",
            },
        ],
    },
    "mechanism": {
        "title": "Observability conditioning and reconstructed rate",
        "axes": {
            "x": "Ordered direction (index)",
            "y": "Observability singular value (measurement/state)",
            "x2": "Time (s)",
            "y2": "Reconstructed rate (m/s)",
        },
        "traces": [
            {
                "x_quantity": "Ordered direction",
                "x_unit": "index",
                "y_quantity": "Observability singular value",
                "y_unit": "measurement/state",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Reconstructed rate",
                "y_unit": "m/s",
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
    g = float(parameters["sensor_gain"])
    window = float(parameters["observation_window_s"])
    rate_only = broken_mode
    dt = 0.05
    t = np.arange(0, window + dt / 2, dt)
    x0 = 0.8
    v0 = 0.6
    y = g * (np.full_like(t, v0) if rate_only else x0 + v0 * t)
    O = np.array([[0, g], [0, g]]) if rate_only else np.array([[g, 0], [g, g * dt]])
    rank = float(np.linalg.matrix_rank(O))
    fit = np.polyfit(t, y, 1) if len(t) > 1 else [0, y[0]]
    inferred_v = 0.0 if rate_only else fit[0] / max(g, 1e-12)
    return result(
        broken_mode,
        t,
        [
            trace("Measurement history", t, y),
            trace("Position truth", t, x0 + v0 * t, "dash"),
        ],
        [
            trace(
                "Observability singular values",
                [1, 2],
                np.linalg.svd(O, compute_uv=False),
            ),
            trace("Reconstructed rate", t, np.full_like(t, inferred_v)),
        ],
        [
            ("rank", "Observability rank", rank, "states"),
            ("inferred_rate", "Inferred initial rate", inferred_v, "m/s"),
            ("measurement_span", "Measurement span", np.ptp(y), "measurement"),
        ],
        [g, window, float(rate_only), rank, inferred_v, np.ptp(y)],
        "A measurement must vary with each state direction over time; sensor gain alone cannot create a missing direction.",
    )


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
