from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 65
BROKEN_TEXT = (
    "Broken mode gives both robots independent shortest paths. They reserve no vertices or edges, "
    "arrive at the central cell together, and violate the coordination assurance boundary."
)
RECOVERY_TEXT = (
    "Plan the second robot in a bounded space-time graph against the first robot's vertex and "
    "edge reservations, including the selected temporal buffer, then audit synchronized separation."
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


def _at(path: list[tuple[int, int]], time: int) -> tuple[int, int]:
    return path[min(max(time, 0), len(path) - 1)]


def _reserved(first: list[tuple[int, int]], current: tuple[int, int],
              candidate: tuple[int, int], next_time: int, buffer: int) -> bool:
    if any(candidate == _at(first, time)
           for time in range(max(0, next_time - buffer), next_time + buffer + 1)):
        return True
    return candidate == _at(first, next_time - 1) and current == _at(first, next_time)


def _plan_second(first: list[tuple[int, int]], buffer: int,
                 delay: int) -> list[tuple[int, int]]:
    start, goal = (2, 0), (2, 4)
    prefix = [start] * (delay + 1)
    queue: list[tuple[int, int, tuple[int, int], list[tuple[int, int]]]] = [
        (4, delay, start, prefix)
    ]
    best = {(start, delay): delay}
    actions = ((0, 0), (0, 1), (1, 0), (-1, 0), (0, -1))
    while queue:
        _, time, state, path = min(queue, key=lambda item: (item[0], item[1], item[2]))
        queue.remove((_, time, state, path))
        if state == goal:
            return path
        if time >= 18:
            continue
        for dx, dy in actions:
            candidate = (state[0] + dx, state[1] + dy)
            next_time = time + 1
            if not (0 <= candidate[0] <= 4 and 0 <= candidate[1] <= 4):
                continue
            if _reserved(first, state, candidate, next_time, buffer):
                continue
            key = (candidate, next_time)
            if next_time >= best.get(key, 10**9):
                continue
            best[key] = next_time
            heuristic = abs(candidate[0] - goal[0]) + abs(candidate[1] - goal[1])
            queue.append((next_time + heuristic, next_time, candidate, path + [candidate]))
    raise RuntimeError("bounded reservation search found no coordinated path")


def _audit(first: list[tuple[int, int]], second: list[tuple[int, int]]) -> tuple[int, np.ndarray]:
    horizon = max(len(first), len(second))
    conflicts = 0
    separation = []
    for time in range(horizon):
        a, b = _at(first, time), _at(second, time)
        separation.append(float(np.hypot(a[0] - b[0], a[1] - b[1])))
        if a == b:
            conflicts += 1
        if time > 0 and _at(first, time - 1) == b and _at(second, time - 1) == a:
            conflicts += 1
    return conflicts, np.asarray(separation)


def _model(parameters: dict[str, Any], broken: bool) -> dict[str, Any]:
    buffer = round(float(parameters["reservation_buffer_steps"]))
    delay = round(float(parameters["robot_b_start_delay_steps"]))
    first = [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)]
    if broken:
        second = [(2, 0)] * (delay + 1) + [(2, 1), (2, 2), (2, 3), (2, 4)]
    else:
        second = _plan_second(first, buffer, delay)
    conflicts, separation = _audit(first, second)
    makespan = max(len(first), len(second)) - 1
    signature = [float(conflicts), float(makespan), float(np.min(separation))]
    first_array, second_array = np.asarray(first), np.asarray(second)
    return {"signature": signature, "sample_count": len(separation),
            "metrics": [("space_time_conflicts", "Space-Time Conflicts", conflicts, "count"),
                        ("coordinated_makespan", "Coordinated Makespan", makespan, "step"),
                        ("minimum_robot_separation", "Minimum Robot Separation", signature[2], "cell")],
            "plots": {"response": _plot("Reserved multi-robot routes", "Grid x position (cell)",
                "Grid y position (cell)", [
                    _trace("Robot A", first_array[:, 0], first_array[:, 1], "Grid x position", "cell",
                           "Grid y position", "cell"),
                    _trace("Robot B", second_array[:, 0], second_array[:, 1], "Grid x position", "cell",
                           "Grid y position", "cell")]),
                "mechanism": _plot("Synchronized separation audit", "Coordination time (step)",
                "Robot separation (cell)", [
                    _trace("Separation", np.arange(len(separation)), separation, "Coordination time", "step",
                           "Robot separation", "cell"),
                    _trace("Vertex-conflict boundary", np.arange(len(separation)), np.zeros_like(separation),
                           "Coordination time", "step", "Robot separation", "cell")])},
            "observation": (f"The reservation audit found {conflicts} vertex/edge conflict(s) over a "
                            f"{makespan}-step coordinated schedule.")}


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
