from __future__ import annotations

import heapq
from typing import Any

import numpy as np

ITEM_NUMBER = 55
BROKEN_TEXT = (
    "Broken mode accepts every short roadmap edge without a local collision query. The graph "
    "is richly connected, yet its shortest route cuts through an inflated obstacle."
)
RECOVERY_TEXT = (
    "Reject samples inside configuration-space obstacles and validate the entire swept segment "
    "before inserting each undirected roadmap edge, then run the same shortest-path query."
)
OBSTACLES = ((4.1, 3.1, 1.05), (6.4, 2.35, 0.95))
ROBOT_RADIUS = 0.25


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


def _vdc(index: int, base: int) -> float:
    value, denominator = 0.0, 1.0
    while index:
        index, remainder = divmod(index, base)
        denominator *= base
        value += remainder / denominator
    return value


def _point_clear(point: np.ndarray) -> bool:
    return all(np.linalg.norm(point - np.array([cx, cy])) > radius + ROBOT_RADIUS
               for cx, cy, radius in OBSTACLES)


def _segment_distance(a: np.ndarray, b: np.ndarray, center: np.ndarray) -> float:
    delta = b - a
    fraction = np.clip(np.dot(center - a, delta) / max(np.dot(delta, delta), 1.0e-12), 0.0, 1.0)
    return float(np.linalg.norm(a + fraction * delta - center))


def _edge_clear(a: np.ndarray, b: np.ndarray) -> bool:
    return all(_segment_distance(a, b, np.array([cx, cy])) > radius + ROBOT_RADIUS
               for cx, cy, radius in OBSTACLES)


def _roadmap(sample_count: int, radius: float, broken: bool) -> tuple[np.ndarray, list[list[tuple[int, float]]], int]:
    points = [np.array([0.5, 0.5]), np.array([9.5, 5.5])]
    index = 1
    while len(points) < sample_count + 2:
        point = np.array([10.0 * _vdc(index, 2), 6.0 * _vdc(index, 3)])
        index += 1
        if _point_clear(point):
            points.append(point)
    nodes = np.asarray(points)
    adjacency: list[list[tuple[int, float]]] = [[] for _ in nodes]
    candidate_edges = 0
    for left in range(len(nodes)):
        for right in range(left + 1, len(nodes)):
            distance = float(np.linalg.norm(nodes[left] - nodes[right]))
            if distance > radius:
                continue
            candidate_edges += 1
            if broken or _edge_clear(nodes[left], nodes[right]):
                adjacency[left].append((right, distance))
                adjacency[right].append((left, distance))
    return nodes, adjacency, candidate_edges


def _query(adjacency: list[list[tuple[int, float]]]) -> tuple[list[int], float, int]:
    queue = [(0.0, 0)]
    best = {0: 0.0}
    parent: dict[int, int] = {}
    settled: set[int] = set()
    while queue:
        cost, node = heapq.heappop(queue)
        if node in settled:
            continue
        settled.add(node)
        if node == 1:
            break
        for neighbor, length in adjacency[node]:
            candidate = cost + length
            if candidate < best.get(neighbor, float("inf")):
                best[neighbor] = candidate
                parent[neighbor] = node
                heapq.heappush(queue, (candidate, neighbor))
    if 1 not in best:
        return [], float("inf"), len(settled)
    path = [1]
    while path[-1] != 0:
        path.append(parent[path[-1]])
    return list(reversed(path)), best[1], len(settled)


def _model(parameters: dict[str, Any], broken: bool) -> dict[str, Any]:
    requested = round(float(parameters["sample_count"]))
    connection_radius = float(parameters["connection_radius_m"])
    nodes, adjacency, candidate_edges = _roadmap(requested, connection_radius, broken)
    indices, path_length, reached = _query(adjacency)
    if not indices:
        path = np.asarray([nodes[0]])
        collision_count = 0
        path_length = 1.0e6
    else:
        path = nodes[indices]
        collision_count = sum(not _edge_clear(path[i], path[i + 1]) for i in range(len(path) - 1))
    reachability = reached / len(nodes)
    signature = [float(path_length), float(collision_count), float(reachability)]
    angles = np.linspace(0.0, 2.0 * np.pi, 80)
    obstacle_x = np.concatenate([cx + (radius + ROBOT_RADIUS) * np.cos(angles) for cx, _, radius in OBSTACLES])
    obstacle_y = np.concatenate([cy + (radius + ROBOT_RADIUS) * np.sin(angles) for _, cy, radius in OBSTACLES])
    edge_count = sum(len(edges) for edges in adjacency) // 2
    return {
        "signature": signature, "sample_count": len(nodes),
        "metrics": [
            ("roadmap_path_length", "Roadmap Path Length", signature[0], "m"),
            ("colliding_path_edges", "Colliding Path Edges", signature[1], "count"),
            ("query_reachability", "Settled Vertex Fraction", signature[2], "1"),
        ],
        "plots": {
            "response": _plot("PRM query in configuration space", "Workspace x position (m)", "Workspace y position (m)", [
                _trace("Roadmap samples", nodes[:, 0], nodes[:, 1], "Workspace x position", "m", "Workspace y position", "m"),
                _trace("Shortest path", path[:, 0], path[:, 1], "Workspace x position", "m", "Workspace y position", "m"),
                _trace("Inflated obstacles", obstacle_x, obstacle_y, "Workspace x position", "m", "Workspace y position", "m"),
            ]),
            "mechanism": _plot("Roadmap edge filtering", "Edge-filter stage (count)", "Roadmap edges (count)", [
                _trace("Candidate versus retained", [0, 1], [candidate_edges, edge_count], "Edge-filter stage", "count", "Roadmap edges", "count"),
                _trace("Query-settled vertices", [0, 1], [0, reached], "Edge-filter stage", "count", "Roadmap edges", "count"),
            ]),
        },
        "observation": (
            "A PRM separates expensive offline connectivity construction from a cheap online "
            "query, but only collision-validated edges make graph reachability physically meaningful."
        ),
    }


def _result(model: dict[str, Any], broken: bool) -> dict[str, Any]:
    return {"metrics": [{"id": key, "label": label, "value": float(value), "unit": unit,
            "emphasis": "primary" if index == 0 else "normal"}
            for index, (key, label, value, unit) in enumerate(model["metrics"])],
            "plots": model["plots"], "explanations": {"observation": model["observation"],
            "broken": BROKEN_TEXT, "recovery": RECOVERY_TEXT}, "diagnostics": {
            "item_number": ITEM_NUMBER, "broken_active": bool(broken),
            "sample_count": int(model["sample_count"]),
            "signature": [float(value) for value in model["signature"]], "software_only": True}}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
