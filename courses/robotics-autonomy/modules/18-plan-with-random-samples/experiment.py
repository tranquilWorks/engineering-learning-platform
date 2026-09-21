from __future__ import annotations

from itertools import pairwise
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


def _vdc(index: int, base: int) -> float:
    value = 0.0
    factor = 1.0 / base
    while index:
        value += factor * (index % base)
        index //= base
        factor /= base
    return value


def _clearance(
    start: np.ndarray, end: np.ndarray, center: np.ndarray, radius: float
) -> float:
    delta = end - start
    denominator = float(delta @ delta)
    fraction = (
        0.0
        if denominator == 0.0
        else float(np.clip((center - start) @ delta / denominator, 0.0, 1.0))
    )
    return float(np.linalg.norm(start + fraction * delta - center) - radius)


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    budget = round(float(parameters["sample_budget"]))
    step_size = float(parameters["step_size_m"])
    goal_bias = float(parameters["goal_bias"])
    radius = float(parameters["obstacle_radius_m"])
    broken = bool(parameters["broken_mode"])
    start = np.array([0.5, 0.5])
    goal = np.array([9.5, 9.5])
    center = np.array([5.0, 5.0])
    nodes = [start]
    parents = [-1]
    goal_index = -1
    for iteration in range(1, budget + 1):
        sample = (
            goal
            if _vdc(iteration, 5) < goal_bias
            else np.array([10.0 * _vdc(iteration, 2), 10.0 * _vdc(iteration, 3)])
        )
        array = np.vstack(nodes)
        nearest = int(np.argmin(np.linalg.norm(array - sample, axis=1)))
        direction = sample - nodes[nearest]
        norm = np.linalg.norm(direction)
        if norm < 1e-12:
            continue
        candidate = nodes[nearest] + direction / norm * min(step_size, norm)
        if not broken and _clearance(nodes[nearest], candidate, center, radius) < 0.1:
            continue
        nodes.append(candidate)
        parents.append(nearest)
        new_index = len(nodes) - 1
        if np.linalg.norm(candidate - goal) <= step_size and (
            broken or _clearance(candidate, goal, center, radius) >= 0.1
        ):
            nodes.append(goal.copy())
            parents.append(new_index)
            goal_index = len(nodes) - 1
            break
    path: list[int] = []
    if goal_index >= 0:
        cursor = goal_index
        while cursor >= 0:
            path.append(cursor)
            cursor = parents[cursor]
        path.reverse()
    path_length = 0.0
    collision_edges = 0
    clearances: list[float] = []
    for left, right in pairwise(path):
        path_length += np.linalg.norm(nodes[right] - nodes[left])
        edge_clearance = _clearance(nodes[left], nodes[right], center, radius)
        clearances.append(edge_clearance)
        collision_edges += edge_clearance < 0.0
    minimum_clearance = (
        min(clearances)
        if clearances
        else min(float(np.linalg.norm(node - center) - radius) for node in nodes)
    )
    tree_x: list[float | None] = []
    tree_y: list[float | None] = []
    for index in range(1, len(nodes)):
        parent = parents[index]
        tree_x.extend([float(nodes[parent][0]), float(nodes[index][0]), None])
        tree_y.extend([float(nodes[parent][1]), float(nodes[index][1]), None])
    circle = np.linspace(0.0, 2.0 * np.pi, 101)
    path_points = (
        np.vstack([nodes[index] for index in path]) if path else np.empty((0, 2))
    )
    signature = [
        float(goal_index >= 0),
        path_length,
        float(len(nodes)),
        float(collision_edges),
        minimum_clearance,
    ]
    return {
        "metrics": [
            {
                "id": "goal_reached",
                "label": "Goal reached",
                "value": "yes" if goal_index >= 0 else "no",
                "unit": None,
                "emphasis": "primary",
            },
            {
                "id": "path_length",
                "label": "Path length",
                "value": path_length,
                "unit": "m",
            },
            {
                "id": "minimum_clearance",
                "label": "Minimum edge clearance",
                "value": minimum_clearance,
                "unit": "m",
            },
            {
                "id": "collision_edges",
                "label": "Colliding path edges",
                "value": collision_edges,
                "unit": "edges",
            },
        ],
        "plots": {
            "response": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "RRT edges",
                        "x": tree_x,
                        "y": tree_y,
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "Obstacle boundary",
                        "x": center[0] + radius * np.cos(circle),
                        "y": center[1] + radius * np.sin(circle),
                    },
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "Returned path",
                        "x": path_points[:, 0] if len(path_points) else [],
                        "y": path_points[:, 1] if len(path_points) else [],
                    },
                ],
                "layout": _layout("Low-discrepancy RRT", "World x (m)", "World y (m)"),
                "config": {"responsive": True, "displaylogo": False},
            },
            "mechanism": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "Path-edge clearance",
                        "x": list(range(len(clearances))),
                        "y": clearances,
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "Collision boundary",
                        "x": [0, max(1, len(clearances) - 1)],
                        "y": [0.0, 0.0],
                    },
                ],
                "layout": _layout(
                    "Continuous collision audit",
                    "Path edge index (-)",
                    "Obstacle clearance (m)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "Low-discrepancy samples grow the tree toward unexplored states while goal bias accelerates connection; validity still depends on every continuous edge.",
            "broken": "Broken mode accepts all extensions without segment collision tests. It reaches the goal with a shorter path whose negative clearance and collision-edge count expose the invalid shortcut.",
            "recovery": "Reject any extension whose segment-to-obstacle clearance is below the safety margin and audit the final parent chain independently.",
        },
        "diagnostics": {
            "item_id": "P18",
            "reference_basis": "independent deterministic RRT recurrence with analytic segment-circle audit",
            "broken_active": broken,
            "sample_count": len(nodes),
            "requested_sample_budget": budget,
            "goal_bias": goal_bias,
            "signature": [float(value) for value in signature],
        },
    }
