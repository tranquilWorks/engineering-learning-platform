from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 57
BROKEN_TEXT = (
    "Broken mode tests shortcut endpoints only and treats the robot as a point. It accepts the "
    "start-to-goal chord even though the swept disk intersects both configuration-space obstacles."
)
RECOVERY_TEXT = (
    "Inflate every obstacle by the robot footprint, compute the closest point on each complete "
    "segment, and accept a shortcut only when its signed swept clearance is nonnegative."
)
OBSTACLES = ((4.0, 0.45, 1.0), (6.3, -0.35, 0.9))


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


def _segment_clearance(a: np.ndarray, b: np.ndarray, robot_radius: float) -> float:
    delta = b - a
    denominator = max(float(np.dot(delta, delta)), 1.0e-12)
    clearances = []
    for cx, cy, obstacle_radius in OBSTACLES:
        center = np.array([cx, cy])
        fraction = np.clip(float(np.dot(center - a, delta)) / denominator, 0.0, 1.0)
        distance = float(np.linalg.norm(a + fraction * delta - center))
        clearances.append(distance - obstacle_radius - robot_radius)
    return min(clearances)


def _path_metrics(path: list[np.ndarray], robot_radius: float) -> tuple[float, float, int]:
    segment_clearances = [_segment_clearance(path[i], path[i + 1], robot_radius)
                          for i in range(len(path) - 1)]
    length = sum(float(np.linalg.norm(path[i + 1] - path[i])) for i in range(len(path) - 1))
    return length, min(segment_clearances), sum(value < 0.0 for value in segment_clearances)


def _smooth(robot_radius: float, iterations: int, broken: bool) -> tuple[list[np.ndarray], list[float]]:
    path = [np.array(point, dtype=float) for point in (
        (0.0, 0.0), (2.2, 0.0), (3.0, 2.15), (5.2, 2.55),
        (7.3, 2.0), (8.3, 0.1), (10.0, 0.0)
    )]
    history = [_path_metrics(path, robot_radius)[0]]
    for attempt in range(iterations):
        if len(path) <= 2:
            history.append(history[-1])
            continue
        span = len(path) - 1
        left = attempt % (len(path) - 2)
        right = min(len(path) - 1, left + 2 + (attempt // max(len(path) - 2, 1)) % max(span - left - 1, 1))
        if right <= left + 1:
            history.append(history[-1])
            continue
        if broken:
            endpoints_clear = _segment_clearance(path[left], path[left], 0.0) >= 0.0 and _segment_clearance(path[right], path[right], 0.0) >= 0.0
            acceptable = endpoints_clear
        else:
            acceptable = _segment_clearance(path[left], path[right], robot_radius) >= 0.0
        if acceptable:
            path = path[: left + 1] + path[right:]
        history.append(_path_metrics(path, robot_radius)[0])
    return path, history


def _model(parameters: dict[str, Any], broken: bool) -> dict[str, Any]:
    robot_radius = float(parameters["robot_radius_m"])
    iterations = round(float(parameters["smoothing_iterations"]))
    path, history = _smooth(robot_radius, iterations, broken)
    length, clearance, collisions = _path_metrics(path, robot_radius)
    coordinates = np.asarray(path)
    signature = [float(length), float(clearance), float(collisions)]
    angles = np.linspace(0.0, 2.0 * np.pi, 80)
    obstacle_x = np.concatenate([cx + (radius + robot_radius) * np.cos(angles) for cx, _, radius in OBSTACLES])
    obstacle_y = np.concatenate([cy + (radius + robot_radius) * np.sin(angles) for _, cy, radius in OBSTACLES])
    return {"signature": signature, "sample_count": len(history),
            "metrics": [("smoothed_path_length", "Smoothed Path Length", signature[0], "m"),
                        ("minimum_swept_clearance", "Minimum Swept Clearance", signature[1], "m"),
                        ("colliding_segments", "Colliding Segments", signature[2], "count")],
            "plots": {"response": _plot("Footprint-aware shortcut path", "Workspace x position (m)", "Workspace y position (m)", [
                _trace("Smoothed path", coordinates[:, 0], coordinates[:, 1], "Workspace x position", "m", "Workspace y position", "m"),
                _trace("Inflated obstacle boundaries", obstacle_x, obstacle_y, "Workspace x position", "m", "Workspace y position", "m"),
            ]), "mechanism": _plot("Accepted shortcuts shorten monotonically", "Shortcut attempt (count)", "Path length (m)", [
                _trace("Current path length", np.arange(len(history)), history, "Shortcut attempt", "count", "Path length", "m"),
                _trace("Straight-line lower bound", np.arange(len(history)), np.full(len(history), 10.0), "Shortcut attempt", "count", "Path length", "m"),
            ])},
            "observation": ("Exact segment-to-obstacle distance lets shortcut smoothing reduce length monotonically "
                            "without confusing waypoint safety with swept-volume safety.")}


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
