from __future__ import annotations

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


def _candidate_clearance(
    headings: np.ndarray, robot_speed: float, obstacle_speed: float, horizon: float
) -> tuple[np.ndarray, np.ndarray]:
    robot_velocity = robot_speed * np.column_stack((np.cos(headings), np.sin(headings)))
    relative_position = np.array([5.0, -5.0])
    relative_velocity = np.array([0.0, obstacle_speed]) - robot_velocity
    speed_squared = np.sum(relative_velocity**2, axis=1)
    cpa_time = np.clip(
        -np.sum(relative_position * relative_velocity, axis=1) / speed_squared,
        0.0,
        horizon,
    )
    separation = np.linalg.norm(
        relative_position + relative_velocity * cpa_time[:, None], axis=1
    )
    return separation, cpa_time


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    robot_speed = float(parameters["robot_speed_m_s"])
    obstacle_speed = float(parameters["obstacle_speed_m_s"])
    horizon = float(parameters["prediction_horizon_s"])
    safety_radius = float(parameters["safety_radius_m"])
    broken = bool(parameters["broken_mode"])
    headings = np.radians(np.arange(-60.0, 61.0, 5.0))
    predicted_speed = 0.0 if broken else obstacle_speed
    predicted_separation, _ = _candidate_clearance(
        headings, robot_speed, predicted_speed, horizon
    )
    cost = np.abs(headings) + 0.1 * (1.0 - np.cos(headings))
    safe = predicted_separation >= safety_radius
    if np.any(safe):
        masked = np.where(safe, cost, np.inf)
        chosen_index = int(np.argmin(masked))
    else:
        chosen_index = int(np.argmax(predicted_separation))
    heading = headings[chosen_index]
    times = np.linspace(0.0, horizon, 401)
    robot = robot_speed * times[:, None] * np.array([np.cos(heading), np.sin(heading)])
    obstacle = np.column_stack(
        (np.full_like(times, 5.0), -5.0 + obstacle_speed * times)
    )
    separation = np.linalg.norm(robot - obstacle, axis=1)
    minimum_index = int(np.argmin(separation))
    minimum = separation[minimum_index]
    signature = [
        np.degrees(heading),
        minimum,
        robot[-1, 0],
        float(minimum < safety_radius),
        times[minimum_index],
    ]
    return {
        "metrics": [
            {
                "id": "selected_heading",
                "label": "Selected heading",
                "value": np.degrees(heading),
                "unit": "deg",
                "emphasis": "primary",
            },
            {
                "id": "minimum_separation",
                "label": "Actual minimum separation",
                "value": minimum,
                "unit": "m",
            },
            {
                "id": "time_of_closest_approach",
                "label": "Closest-approach time",
                "value": times[minimum_index],
                "unit": "s",
            },
            {
                "id": "collision",
                "label": "Safety-radius violation",
                "value": "yes" if minimum < safety_radius else "no",
                "unit": None,
            },
        ],
        "plots": {
            "response": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "Robot trajectory",
                        "x": robot[:, 0],
                        "y": robot[:, 1],
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "Moving obstacle",
                        "x": obstacle[:, 0],
                        "y": obstacle[:, 1],
                    },
                ],
                "layout": _layout("Crossing encounter", "World x (m)", "World y (m)"),
                "config": {"responsive": True, "displaylogo": False},
            },
            "mechanism": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": "Predicted closest separation",
                        "x": np.degrees(headings),
                        "y": predicted_separation,
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "Required separation",
                        "x": [-60, 60],
                        "y": [safety_radius, safety_radius],
                    },
                ],
                "layout": _layout(
                    "Heading-candidate safety prediction",
                    "Candidate heading (deg)",
                    "Predicted separation (m)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "Relative velocity predicts when robot and obstacle are closest; the planner selects the smallest heading deviation that stays outside the safety radius.",
            "broken": "Broken mode freezes the obstacle during prediction, selects the straight route, and collides with the obstacle when its actual crossing motion is simulated.",
            "recovery": "Use the observed obstacle velocity in closest-point-of-approach calculations and validate the selected trajectory against actual moving geometry.",
        },
        "diagnostics": {
            "item_id": "P19",
            "reference_basis": "independent scalar closest-point-of-approach candidate enumeration",
            "broken_active": broken,
            "sample_count": len(times),
            "candidate_count": len(headings),
            "signature": [float(value) for value in signature],
        },
    }
