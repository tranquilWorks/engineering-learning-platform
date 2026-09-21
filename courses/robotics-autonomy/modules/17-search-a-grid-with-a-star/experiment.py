from __future__ import annotations

import heapq
from typing import Any

import numpy as np


def _layout(title: str, x: str, y: str) -> dict[str, Any]:
    return {
        "title": {"text": title, "x": 0.02},
        "xaxis": {"title": x},
        "yaxis": {"title": y},
        "legend": {"orientation": "h"},
        "margin": {"l": 65, "r": 20, "t": 55, "b": 55},
        "hovermode": "closest",
        "uirevision": "keep-view",
    }


def _neighbors(node: tuple[int, int], size: int) -> list[tuple[int, int]]:
    x, y = node
    return [
        (nx, ny)
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))
        if 0 <= nx < size and 0 <= ny < size
    ]


def _search(
    size: int, gap: int, weight: float, ignore_obstacles: bool
) -> tuple[list[tuple[int, int]], list[float]]:
    start = (1, size // 2)
    goal = (size - 2, size // 2)
    wall_x = size // 2
    frontier: list[tuple[float, float, tuple[int, int]]] = [(0.0, 0.0, start)]
    cost = {start: 0.0}
    parent: dict[tuple[int, int], tuple[int, int]] = {}
    expanded_scores: list[float] = []
    while frontier:
        score, distance, current = heapq.heappop(frontier)
        if distance != cost[current]:
            continue
        expanded_scores.append(score)
        if current == goal:
            break
        for neighbor in _neighbors(current, size):
            if not ignore_obstacles and neighbor[0] == wall_x and neighbor[1] != gap:
                continue
            candidate = distance + 1.0
            if candidate < cost.get(neighbor, float("inf")):
                cost[neighbor] = candidate
                parent[neighbor] = current
                heuristic = abs(goal[0] - neighbor[0]) + abs(goal[1] - neighbor[1])
                heapq.heappush(
                    frontier, (candidate + weight * heuristic, candidate, neighbor)
                )
    path = [goal]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path, expanded_scores


def _optimal_cost(size: int, gap: int) -> float:
    path, _ = _search(size, gap, 0.0, False)
    return float(len(path) - 1)


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    size = round(float(parameters["grid_size"]))
    offset = round(float(parameters["gap_offset"]))
    weight = float(parameters["heuristic_weight"])
    broken = bool(parameters["broken_mode"])
    center = size // 2
    gap = int(np.clip(center + offset, 1, size - 2))
    path, scores = _search(size, gap, weight, broken)
    safe_cost = _optimal_cost(size, gap)
    collisions = sum(node[0] == center and node[1] != gap for node in path)
    obstacles = [(center, y) for y in range(size) if y != gap]
    path_array = np.asarray(path)
    obstacle_array = np.asarray(obstacles)
    path_cost = float(len(path) - 1)
    signature = [path_cost, safe_cost, float(collisions), float(len(path)), 1.0]
    return {
        "metrics": [
            {
                "id": "path_cost",
                "label": "Returned path cost",
                "value": path_cost,
                "unit": "cell steps",
                "emphasis": "primary",
            },
            {
                "id": "optimal_safe_cost",
                "label": "Dijkstra safe optimum",
                "value": safe_cost,
                "unit": "cell steps",
            },
            {
                "id": "collision_cells",
                "label": "Obstacle cells on path",
                "value": collisions,
                "unit": "cells",
            },
            {
                "id": "expanded_nodes",
                "label": "Expanded nodes",
                "value": len(scores),
                "unit": "nodes",
            },
        ],
        "plots": {
            "response": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "markers",
                        "name": "Blocked cells",
                        "x": obstacle_array[:, 0],
                        "y": obstacle_array[:, 1],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "Returned path",
                        "x": path_array[:, 0],
                        "y": path_array[:, 1],
                    },
                ],
                "layout": _layout(
                    "Four-connected grid path", "Grid x (cells)", "Grid y (cells)"
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "mechanism": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "Expanded f score",
                        "x": list(range(len(scores))),
                        "y": scores,
                    }
                ],
                "layout": _layout(
                    "Search-priority evolution",
                    "Expansion index (-)",
                    "Priority score (cell cost)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "A-star combines accumulated path cost with a Manhattan estimate of remaining cost; at weight one the heuristic is admissible for four-connected unit-cost motion.",
            "broken": "Broken mode expands through blocked cells, so it reports a deceptively short path whose independent collision count is nonzero.",
            "recovery": "Reject occupied neighbors during expansion and validate the reconstructed path against the same immutable occupancy map.",
        },
        "diagnostics": {
            "item_id": "P17",
            "reference_basis": "independent Dijkstra shortest-path cost and collision audit",
            "broken_active": broken,
            "sample_count": len(scores),
            "expanded_nodes": len(scores),
            "gap_y": gap,
            "heuristic_weight": weight,
            "signature": [float(value) for value in signature],
        },
    }
