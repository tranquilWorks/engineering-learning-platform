from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 13
BROKEN_TEXT = "The broken case removes coupling between rate and position, dropping controllability rank."
RECOVERY_TEXT = "Disable the broken case to restore the state-to-state path."

PLOT_SPECS = {
    "response": {
        "title": "Reachable position under unit command",
        "axes": {"x": "Time (s)", "y": "Position (m)"},
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Reachable position",
                "y_unit": "m",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Target position",
                "y_unit": "m",
                "xaxis": "x",
                "yaxis": "y",
            },
        ],
    },
    "mechanism": {
        "title": "Controllability conditioning and energy map",
        "axes": {
            "x": "Ordered direction (index)",
            "y": "Controllability singular value (state/input)",
            "y2": "Gramian eigenvalue (state²/input²)",
        },
        "traces": [
            {
                "x_quantity": "Ordered direction",
                "x_unit": "index",
                "y_quantity": "Controllability singular value",
                "y_unit": "state/input",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Ordered direction",
                "x_unit": "index",
                "y_quantity": "Gramian eigenvalue",
                "y_unit": "state²/input²",
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
    b = float(parameters["input_gain"])
    coupling = 0.0 if broken_mode else float(parameters["coupling"])
    A = np.array([[1.0, 0.05 * coupling], [0.0, 1.0]])
    B = np.array([[0.5 * 0.05**2 * b], [0.05 * b]])
    C = np.hstack([B, A @ B])
    rank = float(np.linalg.matrix_rank(C))
    gram = sum(
        (np.linalg.matrix_power(A, k) @ B) @ (np.linalg.matrix_power(A, k) @ B).T
        for k in range(40)
    )
    eig = np.linalg.eigvalsh(gram)
    t = np.arange(41) * 0.05
    reachable = b * coupling * 0.5 * t * t
    return result(
        broken_mode,
        t,
        [
            trace("Reachable position under unit command", t, reachable),
            trace("Target", t, np.ones_like(t), "dash"),
        ],
        [
            trace(
                "Controllability singular values",
                [1, 2],
                np.linalg.svd(C, compute_uv=False),
            ),
            trace("Gramian eigenvalues", [1, 2], eig),
        ],
        [
            ("rank", "Controllability rank", rank, "states"),
            (
                "minimum_gramian_eigenvalue",
                "Minimum Gramian eigenvalue",
                eig[0],
                "energy map",
            ),
            ("final_reachable_position", "Unit-command position", reachable[-1], "m"),
        ],
        [b, coupling, rank, eig[0], reachable[-1]],
        "Rank answers possible or impossible; Gramian eigenvalues reveal whether a possible direction is still expensive.",
    )


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
