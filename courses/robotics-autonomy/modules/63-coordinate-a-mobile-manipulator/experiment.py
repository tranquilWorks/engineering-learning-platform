from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 63
BROKEN_TEXT = (
    "Broken mode fixes the base at its initial pose and clips an unreachable arm target onto the "
    "workspace boundary. The apparent IK solution is singular and leaves a Cartesian residual."
)
RECOVERY_TEXT = (
    "Search bounded base placements, retain only reachable arm configurations, penalize weak "
    "manipulability, and execute synchronized base and joint trajectories to the composite target."
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


def _arm_solution(relative: np.ndarray) -> tuple[np.ndarray, float] | None:
    first, second = 0.75, 0.55
    cosine = (float(relative @ relative) - first**2 - second**2) / (2.0 * first * second)
    if abs(cosine) > 1.0:
        return None
    elbow = -float(np.arccos(np.clip(cosine, -1.0, 1.0)))
    shoulder = float(np.arctan2(relative[1], relative[0])
                     - np.arctan2(second * np.sin(elbow), first + second * np.cos(elbow)))
    manipulability = first * second * abs(float(np.sin(elbow)))
    return np.array([shoulder, elbow]), manipulability


def _arm_points(base: float, joints: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    first, second = 0.75, 0.55
    elbow = np.array([base + first * np.cos(joints[0]), first * np.sin(joints[0])])
    endpoint = elbow + second * np.array([np.cos(np.sum(joints)), np.sin(np.sum(joints))])
    return elbow, endpoint


def _model(parameters: dict[str, Any], broken: bool) -> dict[str, Any]:
    target = np.array([float(parameters["target_distance_m"]), 0.35])
    base_weight = float(parameters["base_motion_weight"])
    if broken:
        base = 0.0
        direction = target / float(np.linalg.norm(target))
        clipped = 1.30 * direction
        solution = _arm_solution(clipped)
        assert solution is not None
        joints, manipulability = solution
    else:
        candidates: list[tuple[float, float, np.ndarray, float]] = []
        for base_candidate in np.linspace(0.0, 1.45, 59):
            solution = _arm_solution(target - np.array([base_candidate, 0.0]))
            if solution is None:
                continue
            candidate_joints, candidate_manipulability = solution
            score = (base_weight * base_candidate
                     + 0.18 / max(candidate_manipulability + 0.025, 1.0e-9))
            candidates.append((score, base_candidate, candidate_joints, candidate_manipulability))
        _, base, joints, manipulability = min(candidates, key=lambda item: (item[0], item[1]))
    fractions = np.linspace(0.0, 1.0, 41)
    base_path = base * fractions
    joint_path = fractions[:, None] * joints
    endpoints = []
    for base_state, joint_state in zip(base_path, joint_path, strict=True):
        endpoints.append(_arm_points(float(base_state), joint_state)[1])
    endpoints_array = np.asarray(endpoints)
    elbow, endpoint = _arm_points(base, joints)
    error = float(np.linalg.norm(endpoint - target))
    signature = [error, manipulability, abs(base)]
    return {"signature": signature, "sample_count": len(fractions),
            "metrics": [("composite_endpoint_error", "Composite Endpoint Error", error, "m"),
                        ("arm_manipulability", "Arm Manipulability", manipulability, "m^2"),
                        ("base_travel", "Base Travel", abs(base), "m")],
            "plots": {"response": _plot("Coordinated base-arm reach",
                "World-frame x position (m)", "World-frame y position (m)", [
                    _trace("End-effector path", endpoints_array[:, 0], endpoints_array[:, 1],
                           "World-frame x position", "m", "World-frame y position", "m"),
                    _trace("Final mechanism", [base, elbow[0], endpoint[0]], [0.0, elbow[1], endpoint[1]],
                           "World-frame x position", "m", "World-frame y position", "m"),
                    _trace("Target", [target[0]], [target[1]], "World-frame x position", "m",
                           "World-frame y position", "m")]),
                "mechanism": _plot("Synchronized subsystem progress", "Execution time (s)",
                "Normalized progress (1)", [
                    _trace("Base progress", 4.0 * fractions, fractions, "Execution time", "s",
                           "Normalized progress", "1"),
                    _trace("Arm progress", 4.0 * fractions, np.linalg.norm(joint_path, axis=1)
                           / max(float(np.linalg.norm(joints)), 1.0e-9), "Execution time", "s",
                           "Normalized progress", "1")])},
            "observation": (f"The placement search selected base x={base:.3f} m and retained "
                            f"{manipulability:.3f} m^2 of arm manipulability.")}


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
