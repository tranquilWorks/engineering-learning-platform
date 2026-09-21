from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 7
BROKEN_TEXT = "The broken case keeps K=4 while exposing a 0.5 s actuator lag omitted by the optimistic design."
RECOVERY_TEXT = (
    "Disable the broken case or lower loop gain until both margins are positive."
)

PLOT_SPECS = {
    "response": {
        "title": "Closed-loop stability-margin response",
        "axes": {"x": "Time (s)", "y": "Normalized plant output (ratio)"},
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Plant output",
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
        "title": "Open-loop frequency response",
        "axes": {
            "x": "Angular frequency (rad/s)",
            "y": "Magnitude (dB)",
            "y2": "Phase (deg)",
        },
        "traces": [
            {
                "x_quantity": "Angular frequency",
                "x_unit": "rad/s",
                "y_quantity": "Open-loop magnitude",
                "y_unit": "dB",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Angular frequency",
                "x_unit": "rad/s",
                "y_quantity": "Open-loop phase",
                "y_unit": "deg",
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
    K = 4.0 if broken_mode else float(parameters["loop_gain"])
    tau = 0.5 if broken_mode else float(parameters["actuator_lag_s"])
    dt = 0.005
    t = np.arange(0, 20 + dt / 2, dt)
    y = np.zeros_like(t)
    v = np.zeros_like(t)
    a = np.zeros_like(t)
    for i in range(len(t) - 1):
        cmd = K * (1 - y[i])
        da = (cmd - a[i]) / max(tau, dt / 10) if tau > 0 else 0
        a[i + 1] = cmd if tau == 0 else a[i] + dt * da
        v[i + 1] = v[i] + dt * (a[i] - v[i])
        y[i + 1] = y[i] + dt * v[i]
    w = np.logspace(-2, 2, 300)
    mag = K / (w * np.sqrt(1 + w * w) * np.sqrt(1 + (tau * w) ** 2))
    phase = -90 - np.degrees(np.arctan(w)) - np.degrees(np.arctan(tau * w))
    idx = int(np.argmin(np.abs(20 * np.log10(mag))))
    pm = 180 + phase[idx]
    return result(
        broken_mode,
        t,
        [trace("Output", t, y), trace("Reference", t, np.ones_like(t), "dash")],
        [
            trace("Open-loop magnitude", w, 20 * np.log10(mag)),
            trace("Open-loop phase", w, phase),
        ],
        [
            ("phase_margin", "Approx. phase margin", pm, "deg"),
            ("crossover", "Gain crossover", w[idx], "rad/s"),
            ("peak_output", "Peak output", np.max(np.abs(y)), "output"),
        ],
        [K, tau, pm, w[idx], np.max(np.abs(y))],
        "The same actuator pole that adds time-domain ringing removes phase reserve near gain crossover.",
    )


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
