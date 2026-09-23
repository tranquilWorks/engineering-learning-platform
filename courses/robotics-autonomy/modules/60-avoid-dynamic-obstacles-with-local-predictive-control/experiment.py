from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 60
BROKEN_TEXT = (
    "Broken mode reduces the horizon to one step and freezes the obstacle at its current position. "
    "The controller detects the crossing only after bounded lateral acceleration can no longer avoid it."
)
RECOVERY_TEXT = (
    "Propagate both robot and obstacle over the full receding horizon, score separation at every "
    "prediction step, apply only the first bounded action, and repeat from the next observation."
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


def _candidate_cost(x: float, y: float, lateral_speed: float, obstacle_y: float,
                    obstacle_speed: float, acceleration: float, horizon: int,
                    broken: bool) -> float:
    dt, forward_speed, safety = 0.2, 1.25, 0.9
    predicted_y, predicted_speed = y, lateral_speed
    cost = 0.0
    for step in range(1, horizon + 1):
        predicted_speed = float(np.clip(predicted_speed + acceleration * dt, -1.1, 1.1))
        predicted_y += predicted_speed * dt
        robot_x = x + forward_speed * dt * step
        moving_y = obstacle_y if broken else obstacle_y + obstacle_speed * dt * step
        separation = float(np.hypot(robot_x - 5.0, predicted_y - moving_y))
        cost += 1200.0 * max(safety - separation, 0.0) ** 2
        if separation < safety:
            cost += 80.0
        cost += 0.035 * predicted_y**2 + 0.01 * predicted_speed**2
    cost += 0.12 * acceleration**2 + 0.4 * predicted_y**2
    return cost


def _simulate(horizon: int, obstacle_speed: float, broken: bool) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    dt, forward_speed = 0.2, 1.25
    x, y, lateral_speed = 0.0, 0.0, 0.0
    obstacle_y = -2.0
    robot = [[x, y]]
    obstacle = [[5.0, obstacle_y]]
    separation = [float(np.hypot(x - 5.0, y - obstacle_y))]
    controls: list[float] = []
    effective_horizon = 1 if broken else horizon
    for _ in range(40):
        candidates = (-1.2, -0.6, 0.0, 0.6, 1.2)
        acceleration = min(candidates, key=lambda action: (
            _candidate_cost(x, y, lateral_speed, obstacle_y, obstacle_speed,
                            action, effective_horizon, broken), abs(action), action
        ))
        lateral_speed = float(np.clip(lateral_speed + acceleration * dt, -1.1, 1.1))
        x += forward_speed * dt
        y += lateral_speed * dt
        obstacle_y += obstacle_speed * dt
        robot.append([x, y])
        obstacle.append([5.0, obstacle_y])
        separation.append(float(np.hypot(x - 5.0, y - obstacle_y)))
        controls.append(acceleration)
    return np.asarray(robot), np.asarray(obstacle), np.asarray(separation), np.asarray(controls)


def _model(parameters: dict[str, Any], broken: bool) -> dict[str, Any]:
    horizon = round(float(parameters["prediction_horizon_steps"]))
    obstacle_speed = float(parameters["obstacle_speed_m_s"])
    robot, obstacle, separation, controls = _simulate(horizon, obstacle_speed, broken)
    safety = 0.9
    min_separation = float(np.min(separation))
    violations = int(np.sum(separation < safety))
    path_length = float(np.sum(np.linalg.norm(robot[1:] - robot[:-1], axis=1)))
    signature = [min_separation, float(violations), path_length]
    time_s = np.arange(len(separation)) * 0.2
    return {"signature": signature, "sample_count": len(time_s),
            "metrics": [("minimum_dynamic_separation", "Minimum Dynamic Separation", signature[0], "m"),
                        ("safety_violation_steps", "Safety-Violation Steps", signature[1], "count"),
                        ("executed_path_length", "Executed Path Length", signature[2], "m")],
            "plots": {"response": _plot("Receding-horizon avoidance trajectory", "Workspace x position (m)", "Workspace y position (m)", [
                _trace("Robot", robot[:, 0], robot[:, 1], "Workspace x position", "m", "Workspace y position", "m"),
                _trace("Moving obstacle", obstacle[:, 0], obstacle[:, 1], "Workspace x position", "m", "Workspace y position", "m"),
            ]), "mechanism": _plot("Predicted-separation safety audit", "Elapsed time (s)", "Robot-obstacle separation (m)", [
                _trace("Executed separation", time_s, separation, "Elapsed time", "s", "Robot-obstacle separation", "m"),
                _trace("Safety radius", time_s, np.full_like(time_s, safety), "Elapsed time", "s", "Robot-obstacle separation", "m"),
            ])},
            "observation": (f"The controller applied {len(controls)} bounded first actions. Safety depends on "
                            "predicting where the obstacle will be, not only measuring where it is now.")}


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
