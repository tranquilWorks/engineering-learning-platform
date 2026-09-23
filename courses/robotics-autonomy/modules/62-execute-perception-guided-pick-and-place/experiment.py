from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 62
BROKEN_TEXT = (
    "Broken mode treats camera-frame coordinates as base-frame coordinates and discards the "
    "pickup tolerance check. The arm reaches a mathematically valid but physically wrong point."
)
RECOVERY_TEXT = (
    "Transform the visual estimate through the calibrated camera extrinsic, solve a reachable IK "
    "branch, and gate the grasp transition on true pose-error tolerance before lift and transfer."
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


def _rotation(angle: float) -> np.ndarray:
    return np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])


def _ik(point: np.ndarray) -> tuple[np.ndarray, bool, float]:
    first, second = 0.75, 0.55
    radius_squared = float(point @ point)
    cosine = (radius_squared - first**2 - second**2) / (2.0 * first * second)
    reachable = abs(cosine) <= 1.0
    clipped = float(np.clip(cosine, -1.0, 1.0))
    elbow = -float(np.arccos(clipped))
    shoulder = float(np.arctan2(point[1], point[0])
                     - np.arctan2(second * np.sin(elbow), first + second * np.cos(elbow)))
    reach_margin = first + second - float(np.linalg.norm(point))
    return np.array([shoulder, elbow]), reachable, reach_margin


def _fk(joints: np.ndarray) -> np.ndarray:
    first, second = 0.75, 0.55
    return np.array([first * np.cos(joints[0]) + second * np.cos(np.sum(joints)),
                     first * np.sin(joints[0]) + second * np.sin(np.sum(joints))])


def _model(parameters: dict[str, Any], broken: bool) -> dict[str, Any]:
    noise = 0.01 * float(parameters["vision_noise_cm"])
    yaw_error = np.deg2rad(float(parameters["camera_yaw_error_deg"]))
    translation = np.array([0.28, 0.12])
    true_yaw = np.deg2rad(25.0)
    object_camera = np.array([0.72, 0.18])
    true_object = translation + _rotation(true_yaw) @ object_camera
    measured_camera = object_camera + noise * np.array([0.60, -0.35])
    if broken:
        estimated_object = measured_camera
    else:
        estimated_object = translation + _rotation(true_yaw + yaw_error) @ measured_camera
    joints, reachable, reach_margin = _ik(estimated_object)
    endpoint = _fk(joints)
    pickup_error = float(np.linalg.norm(endpoint - true_object))
    tolerance = 0.055
    completed_states = 9 if reachable and pickup_error <= tolerance else 4
    fractions = np.linspace(0.0, 1.0, 31)
    joint_path = fractions[:, None] * joints
    endpoint_path = np.asarray([_fk(joint) for joint in joint_path])
    phase_error = np.array([float(np.linalg.norm(point - true_object)) for point in endpoint_path])
    signature = [pickup_error, reach_margin, float(completed_states)]
    return {"signature": signature, "sample_count": len(fractions),
            "metrics": [("pickup_position_error", "Pickup Position Error", pickup_error, "m"),
                        ("reachability_margin", "Reachability Margin", reach_margin, "m"),
                        ("completed_task_states", "Completed Task States", completed_states, "count")],
            "plots": {"response": _plot("Perception-guided approach in the base frame",
                "Base-frame x position (m)", "Base-frame y position (m)", [
                    _trace("End-effector approach", endpoint_path[:, 0], endpoint_path[:, 1],
                           "Base-frame x position", "m", "Base-frame y position", "m"),
                    _trace("True object", [true_object[0]], [true_object[1]],
                           "Base-frame x position", "m", "Base-frame y position", "m"),
                    _trace("Estimated object", [estimated_object[0]], [estimated_object[1]],
                           "Base-frame x position", "m", "Base-frame y position", "m")]),
                "mechanism": _plot("Pickup tolerance through the approach", "Approach fraction (1)",
                "Object-position error (m)", [
                    _trace("Position error", fractions, phase_error, "Approach fraction", "1",
                           "Object-position error", "m"),
                    _trace("Grasp tolerance", fractions, np.full_like(fractions, tolerance),
                           "Approach fraction", "1", "Object-position error", "m")])},
            "observation": (f"The calibrated pipeline completed {completed_states} of 9 states. "
                            f"The final visual-to-contact error is {pickup_error:.3f} m against a "
                            f"{tolerance:.3f} m gripper tolerance.")}


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
