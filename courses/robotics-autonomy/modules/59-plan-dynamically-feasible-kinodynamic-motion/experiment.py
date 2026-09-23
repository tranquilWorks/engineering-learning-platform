from __future__ import annotations

import heapq
from typing import Any

import numpy as np

ITEM_NUMBER = 59
BROKEN_TEXT = (
    "Broken mode time-parameterizes a geometric line at the speed limit and commands an instantaneous "
    "start and stop. Position is feasible, but the implied acceleration exceeds the plant limit."
)
RECOVERY_TEXT = (
    "Search a state lattice whose edges apply bounded acceleration through the discrete dynamics, "
    "and require the goal node to satisfy both position and terminal-velocity tolerances."
)


def _trace(name: str, x: Any, y: Any, x_quantity: str, x_unit: str,
           y_quantity: str, y_unit: str) -> dict[str, Any]:
    return {"type": "scattergl", "mode": "lines+markers", "name": name,
            "x": np.asarray(x, dtype=float), "y": np.asarray(y, dtype=float),
            "meta": {"x_quantity": x_quantity, "x_unit": x_unit,
                     "y_quantity": y_quantity, "y_unit": y_unit}}


def _plot(title: str, x_title: str, y_title: str,
          traces: list[dict[str, Any]]) -> dict[str, Any]:
    return {"data": traces, "layout": {"title": {"text": title, "x": 0.02},
            "xaxis": {"title": {"text": x_title}}, "yaxis": {"title": {"text": y_title}},
            "legend": {"orientation": "h"}, "margin": {"l": 72, "r": 36, "t": 62, "b": 62},
            "hovermode": "closest", "uirevision": "keep-view"},
            "config": {"responsive": True, "displaylogo": False}}


def _search(acceleration_limit: float, speed_limit: float) -> tuple[np.ndarray, np.ndarray, np.ndarray, int]:
    dt, target = 0.5, 8.0
    start = (0.0, 0.0)
    queue: list[tuple[float, float, tuple[float, float]]] = [(target / speed_limit, 0.0, start)]
    best = {start: 0.0}
    parent: dict[tuple[float, float], tuple[tuple[float, float], float]] = {}
    settled: set[tuple[float, float]] = set()
    goal: tuple[float, float] | None = None
    while queue:
        _, elapsed, state = heapq.heappop(queue)
        if state in settled:
            continue
        settled.add(state)
        position, speed = state
        if abs(position - target) <= 0.13 and abs(speed) <= 1.0e-9:
            goal = state
            break
        if elapsed >= 20.0:
            continue
        for acceleration in (-acceleration_limit, 0.0, acceleration_limit):
            next_speed = speed + acceleration * dt
            if next_speed < -1.0e-9 or next_speed > speed_limit + 1.0e-9:
                continue
            next_position = position + speed * dt + 0.5 * acceleration * dt**2
            if next_position < -0.01 or next_position > target + 0.13:
                continue
            next_state = (round(next_position, 6), round(next_speed, 6))
            candidate = elapsed + dt
            if candidate + 1.0e-12 < best.get(next_state, float("inf")):
                best[next_state] = candidate
                parent[next_state] = (state, acceleration)
                remaining = max(target - next_position, 0.0)
                heuristic = remaining / max(speed_limit, 1.0e-9)
                heapq.heappush(queue, (candidate + heuristic, candidate, next_state))
    if goal is None:
        raise RuntimeError("bounded kinodynamic lattice has no terminal-rest solution")
    states = [goal]
    actions: list[float] = []
    while states[-1] != start:
        previous, action = parent[states[-1]]
        actions.append(action)
        states.append(previous)
    states.reverse()
    actions.reverse()
    trajectory = np.asarray(states)
    return np.arange(len(states)) * dt, trajectory, np.asarray(actions), len(settled)


def _model(parameters: dict[str, Any], broken: bool) -> dict[str, Any]:
    acceleration_limit = float(parameters["acceleration_limit_m_s2"])
    speed_limit = float(parameters["speed_limit_m_s"])
    if broken:
        travel_time = 8.0 / speed_limit
        time_s = np.array([0.0, 0.5, max(travel_time - 0.5, 0.5), travel_time])
        position = np.array([0.0, 0.5 * speed_limit, 8.0 - 0.5 * speed_limit, 8.0])
        speed = np.array([0.0, speed_limit, speed_limit, 0.0])
        peak_acceleration = speed_limit / 0.5
        violation = max(peak_acceleration - acceleration_limit, 0.0)
        terminal_error = speed_limit
        expanded = 4
        actions = np.array([peak_acceleration, 0.0, -peak_acceleration])
    else:
        time_s, trajectory, actions, expanded = _search(acceleration_limit, speed_limit)
        position, speed = trajectory[:, 0], trajectory[:, 1]
        travel_time = float(time_s[-1])
        peak_acceleration = float(np.max(np.abs(actions)))
        violation = max(peak_acceleration - acceleration_limit, 0.0)
        terminal_error = abs(float(speed[-1]))
    signature = [float(travel_time), float(violation), float(terminal_error)]
    return {"signature": signature, "sample_count": len(time_s),
            "metrics": [("arrival_time", "Arrival Time", signature[0], "s"),
                        ("acceleration_violation", "Peak Acceleration Violation", signature[1], "m/s^2"),
                        ("terminal_speed_error", "Terminal Speed Error", signature[2], "m/s")],
            "plots": {"response": _plot("Kinodynamic state-lattice trajectory", "Elapsed time (s)", "Position (m)", [
                _trace("Planned position", time_s, position, "Elapsed time", "s", "Position", "m"),
                _trace("Goal position", time_s, np.full_like(time_s, 8.0), "Elapsed time", "s", "Position", "m"),
            ]), "mechanism": _plot("Velocity-state feasibility", "Elapsed time (s)", "Speed (m/s)", [
                _trace("Planned speed", time_s, speed, "Elapsed time", "s", "Speed", "m/s"),
                _trace("Speed limit", time_s, np.full_like(time_s, speed_limit), "Elapsed time", "s", "Speed", "m/s"),
            ])},
            "observation": (f"The lattice settled {expanded} states and reached the positional goal at rest; "
                            "each edge is executable because acceleration is part of the transition model.")}


def _result(model: dict[str, Any], broken: bool) -> dict[str, Any]:
    return {"metrics": [{"id": key, "label": label, "value": float(value), "unit": unit,
            "emphasis": "primary" if index == 0 else "normal"}
            for index, (key, label, value, unit) in enumerate(model["metrics"])], "plots": model["plots"],
            "explanations": {"observation": model["observation"], "broken": BROKEN_TEXT, "recovery": RECOVERY_TEXT},
            "diagnostics": {"item_number": ITEM_NUMBER, "broken_active": bool(broken),
            "sample_count": int(model["sample_count"]), "signature": [float(value) for value in model["signature"]],
            "software_only": True}}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
