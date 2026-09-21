from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 17
BROKEN_TEXT = "The broken case sets actuator effectiveness to zero, so a valid design model cannot move the plant."
RECOVERY_TEXT = (
    "Disable the broken case and verify actuator authority before applying the gain."
)

PLOT_SPECS = {
    "response": {
        "title": "LQR state trajectory",
        "axes": {"x": "Time (s)", "y": "Position (m)", "y2": "Velocity (m/s)"},
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
        ],
    },
    "mechanism": {
        "title": "LQR authority and position decay",
        "axes": {
            "x": "Time (s)",
            "y": "Control command (N)",
            "y2": "Absolute position (m)",
        },
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Control command",
                "y_unit": "N",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Absolute position",
                "y_unit": "m",
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
    qw = float(parameters["position_weight"])
    rw = float(parameters["control_weight"])
    eff = 0.0 if broken_mode else 1.0
    dt = 0.02
    A = np.array([[1, dt], [0, 1 - 0.4 * dt]])
    B = np.array([[0.5 * dt * dt * eff], [dt * eff]])
    Q = np.diag([qw, 1.0])
    R = np.array([[rw]])
    if eff == 0:
        K = np.zeros((1, 2))
    else:
        P = Q.copy()
        for _ in range(500):
            Pn = (
                A.T @ P @ A
                - A.T @ P @ B @ np.linalg.solve(R + B.T @ P @ B, B.T @ P @ A)
                + Q
            )
            if np.max(np.abs(Pn - P)) < 1e-12:
                P = Pn
                break
            P = Pn
        K = np.linalg.solve(R + B.T @ P @ B, B.T @ P @ A)
    t = np.arange(0, 12 + dt / 2, dt)
    x = np.zeros((len(t), 2))
    x[0] = [1, 0]
    u = np.zeros(len(t))
    for i in range(len(t) - 1):
        u[i] = (-K @ x[i]).item()
        x[i + 1] = A @ x[i] + B[:, 0] * u[i]
    cost = np.trapezoid(qw * x[:, 0] ** 2 + x[:, 1] ** 2 + rw * u * u, t)
    return result(
        broken_mode,
        t,
        [trace("Position", t, x[:, 0]), trace("Velocity", t, x[:, 1])],
        [trace("Control effort", t, u), trace("Absolute position", t, np.abs(x[:, 0]))],
        [
            ("gain_position", "Position gain", K[0, 0], "N/m"),
            ("peak_control", "Peak command", np.max(np.abs(u)), "N"),
            (
                "quadratic_cost",
                "Realized weighted cost",
                cost,
                "weighted state integral",
            ),
        ],
        [qw, rw, eff, K[0, 0], np.max(np.abs(u)), cost],
        "LQR does not mean aggressive by default; Q and R explicitly declare what the optimum should value. Position and velocity remain on separate axes so a dimensionally invalid state norm is never implied.",
    )


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
