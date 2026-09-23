from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 68
BROKEN_TEXT = (
    "Broken mode suppresses the perceived map update, follows the stale route, freezes the dynamic "
    "obstacle prediction, and records no recovery event. The mission trace violates multiple requirements."
)
RECOVERY_TEXT = (
    "Fuse the obstacle observation into occupancy, replan around the changed cell, predict synchronized "
    "separation, wait until the crossing is safe, and retain dropout recovery in the deterministic replay."
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


def _grid_path(occupied: set[tuple[int, int]]) -> list[tuple[int, int]]:
    start, goal = (0, 0), (8, 0)
    queue: list[tuple[int, int, tuple[int, int], list[tuple[int, int]]]] = [(8, 0, start, [start])]
    best = {start: 0}
    actions = ((1, 0), (0, 1), (0, -1), (-1, 0))
    while queue:
        entry = min(queue, key=lambda item: (item[0], item[1], item[2]))
        queue.remove(entry)
        _, cost, state, path = entry
        if state == goal:
            return path
        for dx, dy in actions:
            candidate = (state[0] + dx, state[1] + dy)
            if not (0 <= candidate[0] <= 8 and 0 <= candidate[1] <= 2):
                continue
            if candidate in occupied:
                continue
            next_cost = cost + 1
            if next_cost >= best.get(candidate, 10**9):
                continue
            best[candidate] = next_cost
            heuristic = abs(candidate[0] - goal[0]) + abs(candidate[1] - goal[1])
            queue.append((next_cost + heuristic, next_cost, candidate, path + [candidate]))
    raise RuntimeError("bounded capstone grid has no route")


def _model(parameters: dict[str, Any], broken: bool) -> dict[str, Any]:
    dropout = float(parameters["range_dropout_percent"])
    obstacle_speed = float(parameters["dynamic_obstacle_speed_m_s"])
    discovered = (4, 0)
    path = _grid_path(set() if broken else {discovered})
    collision_cells = int(discovered in path)
    crossing_index = next(index for index, point in enumerate(path) if point[0] == 6 and point[1] == 0)
    crossing_time = float(crossing_index)
    if not broken:
        while abs(-2.0 + obstacle_speed * crossing_time) < 0.85:
            crossing_time += 1.0
    obstacle_y = -2.0 + obstacle_speed * crossing_time
    separation = abs(obstacle_y)
    map_margin = 1.0 if collision_cells == 0 else -1.0
    dynamic_margin = (separation - 0.85) / 0.85
    dropout_margin = (50.0 - dropout) / 50.0
    replay_margin = 1.0 if not broken else -1.0
    recovery_margin = 1.0 if (dropout == 0.0 or not broken) else -1.0
    margins = np.array([map_margin, dynamic_margin, dropout_margin,
                        replay_margin, recovery_margin])
    violations = int(np.sum(margins < -1.0e-12))
    success = float(violations == 0)
    points = np.asarray(path, dtype=float)
    return {"signature": [success, separation, float(violations)],
            "sample_count": len(path) + len(margins),
            "metrics": [("mission_success", "Mission Success", success, "1"),
                        ("minimum_dynamic_separation", "Minimum Dynamic Separation", separation, "m"),
                        ("capstone_requirement_violations", "Capstone Requirement Violations", violations, "count")],
            "plots": {"response": _plot("Perception-updated mission route", "Map x position (m)",
                "Map y position (m)", [
                    _trace("Executed route", points[:, 0], points[:, 1], "Map x position", "m",
                           "Map y position", "m"),
                    _trace("Discovered obstacle", [discovered[0]], [discovered[1]], "Map x position", "m",
                           "Map y position", "m"),
                    _trace("Dynamic crossing", [6.0], [obstacle_y], "Map x position", "m",
                           "Map y position", "m")]),
                "mechanism": _plot("Cumulative requirement margins", "Requirement index (count)",
                "Normalized requirement margin (1)", [
                    _trace("Margin", np.arange(1, 6), margins, "Requirement index", "count",
                           "Normalized requirement margin", "1"),
                    _trace("Pass boundary", np.arange(1, 6), np.zeros(5), "Requirement index", "count",
                           "Normalized requirement margin", "1")])},
            "observation": (f"The cumulative mission records success={int(success)}, {violations} requirement "
                            f"violation(s), and {separation:.3f} m crossing separation after replanning/recovery.")}


def _result(model: dict[str, Any], broken: bool) -> dict[str, Any]:
    return {"metrics": [{"id": key, "label": label, "value": float(value), "unit": unit,
            "emphasis": "primary" if index == 0 else "normal"}
            for index, (key, label, value, unit) in enumerate(model["metrics"])], "plots": model["plots"],
            "explanations": {"observation": model["observation"], "broken": BROKEN_TEXT, "recovery": RECOVERY_TEXT},
            "diagnostics": {"item_number": ITEM_NUMBER, "broken_active": bool(broken),
            "sample_count": int(model["sample_count"]), "signature": [float(v) for v in model["signature"]],
            "software_only": True}}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
