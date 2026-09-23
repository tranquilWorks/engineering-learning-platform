from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 58
BROKEN_TEXT = (
    "Broken mode minimizes smoothness while omitting the signed-distance constraint. The optimizer "
    "correctly converges to a straight, low-curvature trajectory that passes through the obstacle."
)
RECOVERY_TEXT = (
    "Restore the obstacle hinge penalty and feasibility projection, evaluate clearance over complete "
    "segments, and retain the fixed endpoint constraints during every accepted descent step."
)
CENTER = np.array([5.0, 0.0])
OBSTACLE_RADIUS = 1.1


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


def _segment_clearance(a: np.ndarray, b: np.ndarray, safety_radius: float) -> float:
    delta = b - a
    fraction = np.clip(np.dot(CENTER - a, delta) / max(np.dot(delta, delta), 1.0e-12), 0.0, 1.0)
    return float(np.linalg.norm(a + fraction * delta - CENTER) - safety_radius)


def _objective(points: np.ndarray, safety_radius: float, smoothness_weight: float,
               obstacle_weight: float) -> float:
    second = points[:-2] - 2.0 * points[1:-1] + points[2:]
    smooth = smoothness_weight * float(np.sum(second**2))
    length = 0.03 * float(np.sum((points[1:] - points[:-1]) ** 2))
    distance = np.linalg.norm(points[1:-1] - CENTER, axis=1)
    violation = np.maximum(safety_radius - distance, 0.0)
    return smooth + length + obstacle_weight * float(np.sum(violation**2))


def _gradient(points: np.ndarray, safety_radius: float, smoothness_weight: float,
              obstacle_weight: float) -> np.ndarray:
    gradient = np.zeros_like(points)
    for index in range(1, len(points) - 1):
        second = points[index - 1] - 2.0 * points[index] + points[index + 1]
        gradient[index - 1] += 2.0 * smoothness_weight * second
        gradient[index] -= 4.0 * smoothness_weight * second
        gradient[index + 1] += 2.0 * smoothness_weight * second
    for index in range(1, len(points) - 1):
        gradient[index] += 0.06 * (2.0 * points[index] - points[index - 1] - points[index + 1])
        offset = points[index] - CENTER
        distance = float(np.linalg.norm(offset))
        if distance < safety_radius:
            direction = offset / max(distance, 1.0e-9)
            gradient[index] -= 2.0 * obstacle_weight * (safety_radius - distance) * direction
    gradient[[0, -1]] = 0.0
    return gradient


def _restore_segment_feasibility(points: np.ndarray, safety_radius: float) -> np.ndarray:
    restored = points.copy()
    for _ in range(12):
        changed = False
        for index in range(len(restored) - 1):
            clearance = _segment_clearance(restored[index], restored[index + 1], safety_radius)
            if clearance >= -1.0e-9:
                continue
            midpoint = 0.5 * (restored[index] + restored[index + 1])
            direction = midpoint - CENTER
            direction = direction / max(float(np.linalg.norm(direction)), 1.0e-9)
            correction = (-clearance + 1.0e-6) * direction
            if index > 0:
                restored[index] += correction
            if index + 1 < len(restored) - 1:
                restored[index + 1] += correction
            changed = True
        if not changed:
            break
    return restored


def _optimize(clearance: float, smoothness_weight: float, broken: bool) -> tuple[np.ndarray, list[float]]:
    time_fraction = np.linspace(0.0, 1.0, 31)
    height = 0.0 if broken else OBSTACLE_RADIUS + clearance + 0.65
    points = np.column_stack((10.0 * time_fraction, height * np.sin(np.pi * time_fraction)))
    safety_radius = OBSTACLE_RADIUS + clearance
    obstacle_weight = 0.0 if broken else 80.0
    history = [_objective(points, safety_radius, smoothness_weight, obstacle_weight)]
    for _ in range(1200):
        gradient = _gradient(points, safety_radius, smoothness_weight, obstacle_weight)
        step = 0.01
        current = history[-1]
        candidate = points.copy()
        for _ in range(12):
            candidate = points - step * gradient
            candidate[[0, -1]] = points[[0, -1]]
            if not broken:
                candidate = _restore_segment_feasibility(candidate, safety_radius)
            value = _objective(candidate, safety_radius, smoothness_weight, obstacle_weight)
            if value <= current + 1.0e-12:
                break
            step *= 0.5
        points = candidate
        history.append(value)
    return points, history


def _model(parameters: dict[str, Any], broken: bool) -> dict[str, Any]:
    clearance = float(parameters["required_clearance_m"])
    smoothness_weight = float(parameters["smoothness_weight"])
    points, history = _optimize(clearance, smoothness_weight, broken)
    safety_radius = OBSTACLE_RADIUS + clearance
    segment_clearances = [_segment_clearance(points[i], points[i + 1], safety_radius)
                          for i in range(len(points) - 1)]
    path_length = float(np.sum(np.linalg.norm(points[1:] - points[:-1], axis=1)))
    min_clearance = min(segment_clearances)
    violations = sum(value < -1.0e-7 for value in segment_clearances)
    signature = [path_length, float(min_clearance), float(violations)]
    angles = np.linspace(0.0, 2.0 * np.pi, 100)
    return {"signature": signature, "sample_count": len(points),
            "metrics": [("optimized_length", "Optimized Trajectory Length", signature[0], "m"),
                        ("minimum_constraint_margin", "Minimum Clearance Margin", signature[1], "m"),
                        ("violated_segments", "Violated Obstacle Segments", signature[2], "count")],
            "plots": {"response": _plot("Obstacle-constrained trajectory", "Workspace x position (m)", "Workspace y position (m)", [
                _trace("Optimized trajectory", points[:, 0], points[:, 1], "Workspace x position", "m", "Workspace y position", "m"),
                _trace("Required-clearance boundary", CENTER[0] + safety_radius * np.cos(angles), CENTER[1] + safety_radius * np.sin(angles), "Workspace x position", "m", "Workspace y position", "m"),
            ]), "mechanism": _plot("Constrained objective convergence", "Optimization iteration (count)", "Trajectory objective (1)", [
                _trace("Objective", np.arange(len(history)), history, "Optimization iteration", "count", "Trajectory objective", "1"),
                _trace("Final objective", np.arange(len(history)), np.full(len(history), history[-1]), "Optimization iteration", "count", "Trajectory objective", "1"),
            ])},
            "observation": ("Smoothness has no knowledge of obstacles. A valid trajectory optimizer must couple "
                            "its descent objective to explicit signed-distance feasibility over swept segments.")}


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
