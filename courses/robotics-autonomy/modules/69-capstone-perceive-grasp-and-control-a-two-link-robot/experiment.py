from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 69
BROKEN_TEXT = (
    "Broken mode skips the camera extrinsic, reverses the closure interpretation, applies positive "
    "contact feedback without the energy tank, and bypasses timed-interface recovery."
)
RECOVERY_TEXT = (
    "Restore the calibrated pose chain, verify reach and positive grasp margin, regulate contact with "
    "passivity energy accounting, and require the replayed interface fault to recover before success."
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


def _model(parameters: dict[str, Any], broken: bool) -> dict[str, Any]:
    noise = 0.01 * float(parameters["vision_noise_cm"])
    friction = float(parameters["contact_friction_coefficient"])
    camera_point = np.array([0.72, 0.18])
    true_point = np.array([0.28, 0.12]) + _rotation(np.deg2rad(25.0)) @ camera_point
    measured = camera_point + noise * np.array([0.5, -0.25])
    estimate = measured if broken else np.array([0.28, 0.12]) + _rotation(np.deg2rad(25.0)) @ measured
    first, second = 0.75, 0.55
    cosine = (float(estimate @ estimate) - first**2 - second**2) / (2.0 * first * second)
    reachable = abs(cosine) <= 1.0
    elbow_angle = -float(np.arccos(np.clip(cosine, -1.0, 1.0)))
    shoulder = float(np.arctan2(estimate[1], estimate[0])
                     - np.arctan2(second * np.sin(elbow_angle), first + second * np.cos(elbow_angle)))
    endpoint = np.array([first * np.cos(shoulder) + second * np.cos(shoulder + elbow_angle),
                         first * np.sin(shoulder) + second * np.sin(shoulder + elbow_angle)])
    pickup_error = float(np.linalg.norm(endpoint - true_point))
    closure_margin = -friction if broken else friction - 0.22
    dt, stiffness, desired_force = 0.01, 600.0, 10.0
    penetration, tank = 0.0, 0.18
    minimum_tank = tank
    delay = [0.0] * (7 if broken else 3)
    force_history = []
    for _ in range(200):
        force = stiffness * penetration
        error = desired_force - force
        if broken:
            command_velocity = float(np.clip(0.08 * (desired_force + force), -0.15, 0.15))
        else:
            command_velocity = float(np.clip(0.012 * error, -0.025, 0.025))
        delay.append(command_velocity)
        velocity = delay.pop(0)
        requested_work = max(force * velocity, 0.0) * dt
        if not broken and requested_work > tank and force > 1.0e-12:
            velocity = tank / (force * dt)
            requested_work = tank
        tank -= requested_work
        penetration = float(np.clip(penetration + velocity * dt, 0.0, 0.05))
        minimum_tank = min(minimum_tank, tank)
        force_history.append(stiffness * penetration)
    final_force_error = abs(force_history[-1] - desired_force)
    interface_recovered = not broken
    reach_margin = first + second - float(np.linalg.norm(estimate))
    margins = np.array([(0.055 - pickup_error) / 0.055, reach_margin / 0.20,
                        closure_margin / 0.20, (3.0 - final_force_error) / 3.0,
                        minimum_tank / 0.10, 1.0 if interface_recovered else -1.0])
    violations = int(np.sum(margins < -1.0e-12)) + int(not reachable)
    success = float(violations == 0)
    fractions = np.linspace(0.0, 1.0, 31)
    approach = fractions[:, None] * endpoint
    return {"signature": [success, pickup_error, minimum_tank],
            "sample_count": len(force_history),
            "metrics": [("capstone_success", "Capstone Success", success, "1"),
                        ("pickup_position_error", "Pickup Position Error", pickup_error, "m"),
                        ("minimum_passivity_energy", "Minimum Passivity Energy", minimum_tank, "J")],
            "plots": {"response": _plot("Perception-to-contact manipulation approach",
                "Base-frame x position (m)", "Base-frame y position (m)", [
                    _trace("End-effector approach", approach[:, 0], approach[:, 1],
                           "Base-frame x position", "m", "Base-frame y position", "m"),
                    _trace("True object", [true_point[0]], [true_point[1]],
                           "Base-frame x position", "m", "Base-frame y position", "m"),
                    _trace("Estimated grasp", [estimate[0]], [estimate[1]],
                           "Base-frame x position", "m", "Base-frame y position", "m")]),
                "mechanism": _plot("Cumulative manipulation requirement margins",
                "Requirement index (count)", "Normalized requirement margin (1)", [
                    _trace("Margin", np.arange(1, 7), margins, "Requirement index", "count",
                           "Normalized requirement margin", "1"),
                    _trace("Pass boundary", np.arange(1, 7), np.zeros(6),
                           "Requirement index", "count", "Normalized requirement margin", "1")])},
            "observation": (f"The cumulative manipulation run records success={int(success)}, "
                            f"pickup error {pickup_error:.3f} m, final force error {final_force_error:.2f} N, "
                            f"and minimum tank energy {minimum_tank:.3f} J.")}


def _result(model: dict[str, Any], broken: bool) -> dict[str, Any]:
    return {"metrics": [{"id": key, "label": label, "value": float(value), "unit": unit,
            "emphasis": "primary" if index == 0 else "normal"}
            for index, (key, label, value, unit) in enumerate(model["metrics"])], "plots": model["plots"],
            "explanations": {"observation": model["observation"], "broken": BROKEN_TEXT, "recovery": RECOVERY_TEXT},
            "diagnostics": {"item_number": ITEM_NUMBER, "broken_active": bool(broken),
            "sample_count": int(model["sample_count"]), "signature": [float(v) for v in model["signature"]],
            "software_only": True}}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
