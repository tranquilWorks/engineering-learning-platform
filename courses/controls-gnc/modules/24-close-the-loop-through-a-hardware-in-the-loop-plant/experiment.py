from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 24
BROKEN_TEXT = "The broken case drops every second command with a 0.1 s controller period, 0.04 s one-way latency, and 0.12 s watchdog."
RECOVERY_TEXT = "Disable the broken case to restore fresh commands. This is a software-only virtual protocol/plant lesson; it does not claim physical HIL execution."

PLOT_SPECS = {
    "response": {
        "title": "Software-only virtual-plant tracking",
        "axes": {"x": "Time (s)", "y": "Position (m)"},
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Virtual plant position",
                "y_unit": "m",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Reference position",
                "y_unit": "m",
                "xaxis": "x",
                "yaxis": "y",
            },
        ],
    },
    "mechanism": {
        "title": "Packet-driven force and freshness",
        "axes": {"x": "Time (s)", "y": "Force (N)", "y2": "Packet age (s)"},
        "traces": [
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Controller force",
                "y_unit": "N",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Applied force",
                "y_unit": "N",
                "xaxis": "x",
                "yaxis": "y",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Measurement age",
                "y_unit": "s",
                "xaxis": "x",
                "yaxis": "y2",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Command age",
                "y_unit": "s",
                "xaxis": "x",
                "yaxis": "y2",
            },
            {
                "x_quantity": "Time",
                "x_unit": "s",
                "y_quantity": "Watchdog timeout",
                "y_unit": "s",
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
    period = 0.1 if broken_mode else float(parameters["controller_period_s"])
    latency = 0.04 if broken_mode else float(parameters["one_way_latency_s"])
    watchdog = 0.12 if broken_mode else 0.2
    drop_interval = 2 if broken_mode else 0
    dt = 0.01
    time = np.arange(0.0, 8.0 + dt / 2, dt)
    period_ticks = round(period / dt)
    latency_ticks = round(latency / dt)
    watchdog_ticks = round(watchdog / dt)

    reference = np.where(time < 4.0, 1.0, -0.5)
    position = np.zeros_like(time)
    velocity = np.zeros_like(time)
    controller_force = np.zeros_like(time)
    applied_force = np.zeros_like(time)
    command_age = np.full_like(time, watchdog + dt)
    measurement_age = np.full_like(time, latency + period)
    watchdog_active = np.zeros(len(time), dtype=bool)

    sensor_queue: dict[int, tuple[float, float, int]] = {}
    command_queue: dict[int, tuple[float, int]] = {}
    latest_measurement = (0.0, 0.0)
    latest_measurement_tick = 0
    latest_controller_force = 0.0
    latest_delivered_force = 0.0
    latest_delivery_tick = 0
    has_measurement = False
    has_delivered_command = False
    command_sequence = 0

    mass = 1.5
    damping = 1.2
    velocity_decay = np.exp(-damping * dt / mass)
    velocity_from_force = (1 - velocity_decay) / damping
    position_from_velocity = mass / damping * (1 - velocity_decay)
    position_from_force = dt / damping - mass / damping**2 * (1 - velocity_decay)

    for tick in range(len(time)):
        controller_event = tick % period_ticks == 0
        if controller_event:
            delivery_tick = tick + latency_ticks
            if delivery_tick < len(time):
                sensor_queue[delivery_tick] = (position[tick], velocity[tick], tick)

        if tick in sensor_queue:
            measured_position, measured_velocity, source_tick = sensor_queue.pop(tick)
            latest_measurement = (measured_position, measured_velocity)
            latest_measurement_tick = source_tick
            has_measurement = True

        if controller_event and has_measurement:
            measured_position, measured_velocity = latest_measurement
            raw_force = (
                18 * (reference[tick] - measured_position) - 8 * measured_velocity
            )
            latest_controller_force = float(np.clip(raw_force, -30, 30))
            command_sequence += 1
            should_drop = drop_interval > 0 and command_sequence % drop_interval == 0
            delivery_tick = tick + latency_ticks
            if not should_drop and delivery_tick < len(time):
                command_queue[delivery_tick] = (latest_controller_force, tick)

        if tick in command_queue:
            latest_delivered_force, _ = command_queue.pop(tick)
            latest_delivery_tick = tick
            has_delivered_command = True

        controller_force[tick] = latest_controller_force
        if has_measurement:
            measurement_age[tick] = (tick - latest_measurement_tick) * dt
        if has_delivered_command:
            command_age[tick] = (tick - latest_delivery_tick) * dt
        watchdog_active[tick] = (
            has_delivered_command and tick - latest_delivery_tick >= watchdog_ticks
        )
        startup_safe = not has_delivered_command
        applied_force[tick] = (
            0.0 if startup_safe or watchdog_active[tick] else latest_delivered_force
        )

        if tick < len(time) - 1:
            velocity[tick + 1] = (
                velocity_decay * velocity[tick]
                + velocity_from_force * applied_force[tick]
            )
            position[tick + 1] = (
                position[tick]
                + position_from_velocity * velocity[tick]
                + position_from_force * applied_force[tick]
            )

    watchdog_fraction = float(np.mean(watchdog_active[:-1]))
    signature = [
        period,
        latency,
        watchdog,
        float(drop_interval),
        position[-1],
        watchdog_fraction,
    ]
    return result(
        broken_mode,
        time,
        [
            trace("Virtual plant position", time, position),
            trace("Reference position", time, reference, "dash"),
        ],
        [
            trace("Controller force", time, controller_force, "dash"),
            trace("Applied force", time, applied_force),
            trace("Measurement age", time, measurement_age),
            trace("Command age", time, command_age),
            trace("Watchdog timeout", time, np.full_like(time, watchdog), "dash"),
        ],
        [
            (
                "final_error",
                "Final virtual-plant error",
                reference[-1] - position[-1],
                "m",
            ),
            ("maximum_command_age", "Maximum command age", np.max(command_age), "s"),
            (
                "watchdog_fraction",
                "Watchdog-active samples",
                watchdog_fraction,
                "ratio",
            ),
        ],
        signature,
        "A timestamped sensor packet travels to the controller before a timestamped command returns to the exact damped virtual plant. Same-tick deliveries precede control and watchdog decisions. This is entirely software-only; no physical hardware execution is claimed.",
    )


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    return _simulate(parameters, bool(parameters["broken_mode"]))
