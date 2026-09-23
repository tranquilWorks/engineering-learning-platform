from __future__ import annotations

import heapq
from typing import Any

import numpy as np

ITEM_NUMBER = 54
BROKEN_TEXT = (
    "Broken mode reuses the path cached before the occupancy change. Its search cost is zero, "
    "but the path crosses the newly occupied cell and is therefore not executable."
)
RECOVERY_TEXT = (
    "Notify LPA* of every changed vertex, update the inconsistent one-step lookahead values, "
    "and process the priority queue until the goal is locally consistent again."
)


def _trace(name: str, x: Any, y: Any, x_quantity: str, x_unit: str,
           y_quantity: str, y_unit: str) -> dict[str, Any]:
    return {
        "type": "scattergl", "mode": "lines+markers", "name": name,
        "x": np.asarray(x, dtype=float), "y": np.asarray(y, dtype=float),
        "meta": {"x_quantity": x_quantity, "x_unit": x_unit,
                 "y_quantity": y_quantity, "y_unit": y_unit},
    }


def _plot(title: str, x_title: str, y_title: str,
          traces: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "data": traces,
        "layout": {
            "title": {"text": title, "x": 0.02},
            "xaxis": {"title": {"text": x_title}},
            "yaxis": {"title": {"text": y_title}},
            "legend": {"orientation": "h"},
            "margin": {"l": 72, "r": 36, "t": 62, "b": 62},
            "hovermode": "closest", "uirevision": "keep-view",
        },
        "config": {"responsive": True, "displaylogo": False},
    }


def _neighbors(node: tuple[int, int], occupied: set[tuple[int, int]]) -> list[tuple[int, int]]:
    if node in occupied:
        return []
    x, y = node
    return [
        candidate for candidate in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))
        if 0 <= candidate[0] < 24 and 0 <= candidate[1] < 16 and candidate not in occupied
    ]


class _LPAStar:
    def __init__(self, start: tuple[int, int], goal: tuple[int, int],
                 occupied: set[tuple[int, int]], heuristic_weight: float) -> None:
        self.start = start
        self.goal = goal
        self.occupied = occupied
        self.weight = heuristic_weight
        self.g: dict[tuple[int, int], float] = {}
        self.rhs: dict[tuple[int, int], float] = {start: 0.0}
        self.queue: list[tuple[float, float, int, tuple[int, int]]] = []
        self.version: dict[tuple[int, int], int] = {}
        self._push(start)

    def _value(self, table: dict[tuple[int, int], float], node: tuple[int, int]) -> float:
        return table.get(node, float("inf"))

    def _key(self, node: tuple[int, int]) -> tuple[float, float]:
        value = min(self._value(self.g, node), self._value(self.rhs, node))
        heuristic = abs(node[0] - self.goal[0]) + abs(node[1] - self.goal[1])
        return value + self.weight * heuristic, value

    def _push(self, node: tuple[int, int]) -> None:
        version = self.version.get(node, 0) + 1
        self.version[node] = version
        first, second = self._key(node)
        heapq.heappush(self.queue, (first, second, version, node))

    def _top(self) -> tuple[tuple[float, float], tuple[int, int] | None]:
        while self.queue:
            first, second, version, node = self.queue[0]
            if version != self.version.get(node) or (first, second) != self._key(node):
                heapq.heappop(self.queue)
                continue
            return (first, second), node
        return (float("inf"), float("inf")), None

    def update_vertex(self, node: tuple[int, int]) -> None:
        if node != self.start:
            predecessors = _neighbors(node, self.occupied)
            self.rhs[node] = min(
                (self._value(self.g, predecessor) + 1.0 for predecessor in predecessors),
                default=float("inf"),
            )
        self.version[node] = self.version.get(node, 0) + 1
        if self._value(self.g, node) != self._value(self.rhs, node):
            self._push(node)

    def compute(self) -> int:
        expansions = 0
        while True:
            top_key, node = self._top()
            goal_key = self._key(self.goal)
            if node is None or (top_key >= goal_key and self._value(self.rhs, self.goal) == self._value(self.g, self.goal)):
                break
            heapq.heappop(self.queue)
            if self._value(self.g, node) > self._value(self.rhs, node):
                self.g[node] = self._value(self.rhs, node)
                for successor in _neighbors(node, self.occupied):
                    self.update_vertex(successor)
            else:
                self.g[node] = float("inf")
                self.update_vertex(node)
                for successor in _neighbors(node, self.occupied):
                    self.update_vertex(successor)
            expansions += 1
            if expansions > 2500:
                raise RuntimeError("bounded LPA* search did not converge")
        return expansions

    def path(self) -> list[tuple[int, int]]:
        if not np.isfinite(self._value(self.g, self.goal)):
            return []
        path = [self.goal]
        while path[-1] != self.start:
            predecessors = _neighbors(path[-1], self.occupied)
            predecessor = min(
                predecessors,
                key=lambda node: (self._value(self.g, node) + 1.0, node),
            )
            if not np.isfinite(self._value(self.g, predecessor)):
                return []
            path.append(predecessor)
        return list(reversed(path))


def _cold_astar(start: tuple[int, int], goal: tuple[int, int],
                occupied: set[tuple[int, int]], weight: float) -> int:
    queue = [(0.0, 0.0, start)]
    best = {start: 0.0}
    expanded: set[tuple[int, int]] = set()
    while queue:
        _, cost, node = heapq.heappop(queue)
        if node in expanded:
            continue
        expanded.add(node)
        if node == goal:
            return len(expanded)
        for neighbor in _neighbors(node, occupied):
            candidate = cost + 1.0
            if candidate < best.get(neighbor, float("inf")):
                best[neighbor] = candidate
                heuristic = abs(neighbor[0] - goal[0]) + abs(neighbor[1] - goal[1])
                heapq.heappush(queue, (candidate + weight * heuristic, candidate, neighbor))
    return len(expanded)


def _model(parameters: dict[str, Any], broken: bool) -> dict[str, Any]:
    resolution = float(parameters["grid_resolution_m"])
    weight = float(parameters["heuristic_weight"])
    start, goal = (2, 4), (21, 4)
    occupied = {(11, y) for y in range(16) if y not in {4, 12}}
    planner = _LPAStar(start, goal, occupied, weight)
    initial_expansions = planner.compute()
    initial_path = planner.path()

    changed = (11, 4)
    occupied.add(changed)
    planner.update_vertex(changed)
    for neighbor in ((10, 4), (12, 4), (11, 3), (11, 5)):
        planner.update_vertex(neighbor)
    repair_expansions = 0 if broken else planner.compute()
    path = initial_path if broken else planner.path()
    cold_expansions = _cold_astar(start, goal, occupied, 0.0)
    collision_count = sum(node in occupied for node in path)
    path_cost = max(len(path) - 1, 0) * resolution
    expansion_ratio = repair_expansions / max(cold_expansions, 1)
    coordinates = np.asarray(path, dtype=float) * resolution
    wall = np.asarray(sorted(occupied), dtype=float) * resolution
    signature = [path_cost, float(collision_count), float(expansion_ratio)]
    return {
        "signature": signature,
        "sample_count": 24 * 16,
        "metrics": [
            ("replanned_path_length", "Replanned Path Length", signature[0], "m"),
            ("occupied_path_cells", "Occupied Cells on Path", signature[1], "count"),
            ("repair_expansion_ratio", "Repair/Cold Expansion Ratio", signature[2], "1"),
        ],
        "plots": {
            "response": _plot(
                "Path after a local map change", "Map x position (m)", "Map y position (m)",
                [
                    _trace("Replanned path", coordinates[:, 0], coordinates[:, 1], "Map x position", "m", "Map y position", "m"),
                    _trace("Occupied wall cells", wall[:, 0], wall[:, 1], "Map x position", "m", "Map y position", "m"),
                ],
            ),
            "mechanism": _plot(
                "Incremental repair versus cold replanning", "Planning method index (count)", "Expanded vertices (count)",
                [
                    _trace("LPA* repair", [0, 1], [initial_expansions, repair_expansions], "Planning method index", "count", "Expanded vertices", "count"),
                    _trace("Cold uniform-cost search", [0, 1], [initial_expansions, cold_expansions], "Planning method index", "count", "Expanded vertices", "count"),
                ],
            ),
        },
        "observation": (
            "LPA* preserves consistent values away from the changed cell and repairs only the "
            "affected dependency cone; validity still dominates a superficially cheap stale path."
        ),
    }


def _result(model: dict[str, Any], broken: bool) -> dict[str, Any]:
    return {
        "metrics": [
            {"id": key, "label": label, "value": float(value), "unit": unit,
             "emphasis": "primary" if index == 0 else "normal"}
            for index, (key, label, value, unit) in enumerate(model["metrics"])
        ],
        "plots": model["plots"],
        "explanations": {"observation": model["observation"], "broken": BROKEN_TEXT,
                         "recovery": RECOVERY_TEXT},
        "diagnostics": {
            "item_number": ITEM_NUMBER, "broken_active": bool(broken),
            "sample_count": int(model["sample_count"]),
            "signature": [float(value) for value in model["signature"]],
            "software_only": True,
        },
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
