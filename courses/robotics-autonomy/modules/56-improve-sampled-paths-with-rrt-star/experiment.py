from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 56
BROKEN_TEXT = (
    "Broken mode grows a collision-free RRT but never chooses a lower-cost parent and never "
    "rewires descendants. Feasibility survives while the first-found detour remains unnecessarily long."
)
RECOVERY_TEXT = (
    "Restore near-neighbor parent selection, collision-check every candidate edge, and propagate "
    "lower costs through rewired descendants before comparing incumbent goal connections."
)
OBSTACLES = ((4.2, 2.7, 1.15), (6.5, 3.5, 1.0))
START = np.array([0.5, 0.5])
GOAL = np.array([9.5, 5.5])


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


def _segment_distance(a: np.ndarray, b: np.ndarray, center: np.ndarray) -> float:
    delta = b - a
    fraction = np.clip(np.dot(center - a, delta) / max(np.dot(delta, delta), 1.0e-12), 0.0, 1.0)
    return float(np.linalg.norm(a + fraction * delta - center))


def _clear(a: np.ndarray, b: np.ndarray) -> bool:
    return all(_segment_distance(a, b, np.array([cx, cy])) > radius + 0.2
               for cx, cy, radius in OBSTACLES)


def _descendants(parent: list[int], root: int) -> list[int]:
    result = [root]
    for node in result:
        result.extend(index for index, ancestor in enumerate(parent) if ancestor == node and index != node)
    return result


def _plan(sample_count: int, rewire_radius: float, broken: bool) -> tuple[np.ndarray, float, int, list[float]]:
    nodes = [START.copy()]
    parent = [0]
    cost = [0.0]
    rewires = 0
    incumbent: list[float] = []
    step = 0.68
    for sample_index in range(1, sample_count + 1):
        sample = GOAL if sample_index % 12 == 0 else np.array([
            10.0 * _vdc(sample_index, 2), 6.0 * _vdc(sample_index, 3)
        ])
        distances = np.asarray([np.linalg.norm(node - sample) for node in nodes])
        nearest = int(np.argmin(distances))
        direction = sample - nodes[nearest]
        length = float(np.linalg.norm(direction))
        new = sample.copy() if length <= step else nodes[nearest] + step * direction / length
        if not (0.0 <= new[0] <= 10.0 and 0.0 <= new[1] <= 6.0) or not _clear(nodes[nearest], new):
            incumbent.append(incumbent[-1] if incumbent else 20.0)
            continue
        near = [index for index, node in enumerate(nodes) if np.linalg.norm(node - new) <= rewire_radius]
        chosen = nearest
        chosen_cost = cost[nearest] + float(np.linalg.norm(nodes[nearest] - new))
        if not broken:
            for candidate in near:
                candidate_cost = cost[candidate] + float(np.linalg.norm(nodes[candidate] - new))
                if candidate_cost < chosen_cost and _clear(nodes[candidate], new):
                    chosen, chosen_cost = candidate, candidate_cost
        nodes.append(new)
        parent.append(chosen)
        cost.append(chosen_cost)
        new_index = len(nodes) - 1
        if not broken:
            for candidate in near:
                through_new = chosen_cost + float(np.linalg.norm(nodes[candidate] - new))
                if candidate != chosen and through_new + 1.0e-12 < cost[candidate] and _clear(new, nodes[candidate]):
                    delta = through_new - cost[candidate]
                    parent[candidate] = new_index
                    for descendant in _descendants(parent, candidate):
                        cost[descendant] += delta
                    rewires += 1
        goal_options = [index for index, node in enumerate(nodes)
                        if np.linalg.norm(node - GOAL) <= 2.2 and _clear(node, GOAL)]
        best_goal = min((cost[index] + float(np.linalg.norm(nodes[index] - GOAL))
                         for index in goal_options), default=20.0)
        incumbent.append(best_goal)
    options = [(cost[index] + float(np.linalg.norm(node - GOAL)), index)
               for index, node in enumerate(nodes) if np.linalg.norm(node - GOAL) <= 2.2 and _clear(node, GOAL)]
    if not options:
        return np.asarray([START]), 1.0e6, rewires, incumbent
    path_cost, node = min(options)
    path = [GOAL]
    while node != 0:
        path.append(nodes[node])
        node = parent[node]
    path.append(START)
    return np.asarray(list(reversed(path))), float(path_cost), rewires, incumbent


def _model(parameters: dict[str, Any], broken: bool) -> dict[str, Any]:
    sample_count = round(float(parameters["sample_count"]))
    rewire_radius = float(parameters["rewire_radius_m"])
    path, cost, rewires, incumbent = _plan(sample_count, rewire_radius, broken)
    lower_bound = float(np.linalg.norm(GOAL - START))
    excess = cost / lower_bound - 1.0
    signature = [cost, float(rewires), float(excess)]
    angles = np.linspace(0.0, 2.0 * np.pi, 80)
    obstacle_x = np.concatenate([cx + (radius + 0.2) * np.cos(angles) for cx, _, radius in OBSTACLES])
    obstacle_y = np.concatenate([cy + (radius + 0.2) * np.sin(angles) for _, cy, radius in OBSTACLES])
    return {"signature": signature, "sample_count": sample_count,
            "metrics": [("best_path_cost", "Best Path Cost", signature[0], "m"),
                        ("rewire_count", "Successful Rewires", signature[1], "count"),
                        ("lower_bound_excess", "Excess over Straight-Line Bound", signature[2], "1")],
            "plots": {"response": _plot("RRT* incumbent path", "Workspace x position (m)", "Workspace y position (m)", [
                _trace("Best path", path[:, 0], path[:, 1], "Workspace x position", "m", "Workspace y position", "m"),
                _trace("Inflated obstacles", obstacle_x, obstacle_y, "Workspace x position", "m", "Workspace y position", "m"),
            ]), "mechanism": _plot("Anytime path improvement", "Accepted sample index (count)", "Incumbent goal cost (m)", [
                _trace("Incumbent cost", np.arange(len(incumbent)), incumbent, "Accepted sample index", "count", "Incumbent goal cost", "m"),
                _trace("Euclidean lower bound", np.arange(len(incumbent)), np.full(len(incumbent), lower_bound), "Accepted sample index", "count", "Incumbent goal cost", "m"),
            ])},
            "observation": ("RRT* retains RRT feasibility while parent selection and rewiring monotonically "
                            "improve the incumbent cost toward, but never below, the geometric lower bound.")}


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
