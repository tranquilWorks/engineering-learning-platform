from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 3
BROKEN_TEXT = "The broken case reflects a stable pole into the right half-plane, turning decay into exponential growth."
RECOVERY_TEXT = "Disable the broken case and keep the real part negative."

PLOT_SPECS = {
    "response": {
        "title": "Mode response and exponential envelope",
        "axes": {"x": "Time (s)", "y": "Modal amplitude (ratio)"},
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Modal response",
                "y_unit": "ratio",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Positive envelope",
                "y_unit": "ratio",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Negative envelope",
                "y_unit": "ratio",
                "xaxis": "x",
                "yaxis": "y",
            },
        ],
    },
    "mechanism": {
        "title": "Phase portrait and pole location",
        "axes": {
            "x": "Modal amplitude (ratio)",
            "y": "Modal rate (1/s)",
            "x2": "Real pole part (1/s)",
            "y2": "Imaginary pole part (rad/s)",
        },
        "traces": [
            {
                "x_quantity": "Modal amplitude",
                "x_unit": "ratio",
                "y_quantity": "Modal rate",
                "y_unit": "1/s",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Real pole part",
                "x_unit": "1/s",
                "y_quantity": "Imaginary pole part",
                "y_unit": "rad/s",
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
    sigma = float(parameters["pole_real_per_s"])
    omega = float(parameters["pole_imag_rad_s"])
    sigma = abs(sigma) if broken_mode else sigma
    t = np.linspace(0, 12, 601)
    env = np.exp(sigma * t)
    x = env * np.cos(omega * t)
    period = 2 * np.pi / omega if omega > 0 else 0.0
    return result(
        broken_mode,
        t,
        [
            trace("Response", t, x),
            trace("Envelope +", t, env, "dash"),
            trace("Envelope -", t, -env, "dash"),
        ],
        [
            trace("Phase portrait", x, np.gradient(x, t)),
            trace("Pole", [sigma], [omega]),
        ],
        [
            ("decay_rate", "Real part", sigma, "1/s"),
            ("oscillation_rate", "Imaginary part", omega, "rad/s"),
            ("period", "Oscillation period", period, "s"),
        ],
        [sigma, omega, period, x[-1], np.max(np.abs(x))],
        "The pole real part controls the envelope while its imaginary part controls rotation and visible oscillation.",
    )


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
