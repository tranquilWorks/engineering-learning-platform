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


def _trace(
    name: str,
    x: Any,
    y: Any,
    x_quantity: str,
    x_unit: str,
    y_quantity: str,
    y_unit: str,
) -> dict[str, Any]:
    return {
        "type": "scattergl",
        "mode": "lines+markers",
        "name": name,
        "x": np.asarray(x, dtype=float),
        "y": np.asarray(y, dtype=float),
        "meta": {
            "x_quantity": x_quantity,
            "x_unit": x_unit,
            "y_quantity": y_quantity,
            "y_unit": y_unit,
        },
    }


def _plot(
    title: str, x_title: str, y_title: str, traces: list[dict[str, Any]]
) -> dict[str, Any]:
    return {
        "data": traces,
        "layout": {
            "title": {"text": title, "x": 0.02},
            "xaxis": {"title": {"text": x_title}},
            "yaxis": {"title": {"text": y_title}},
            "legend": {"orientation": "h"},
            "margin": {"l": 72, "r": 36, "t": 62, "b": 62},
            "hovermode": "closest",
            "uirevision": "keep-view",
        },
        "config": {"responsive": True, "displaylogo": False},
    }


def _rotation(angle: float) -> np.ndarray:
    return np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])


def _ik(point: np.ndarray) -> tuple[np.ndarray, bool, float]:
    first, second = 0.75, 0.55
    radius_squared = float(point @ point)
    cosine = (radius_squared - first**2 - second**2) / (2.0 * first * second)
    reachable = abs(cosine) <= 1.0
    clipped = float(np.clip(cosine, -1.0, 1.0))
    elbow = -float(np.arccos(clipped))
    shoulder = float(
        np.arctan2(point[1], point[0])
        - np.arctan2(second * np.sin(elbow), first + second * np.cos(elbow))
    )
    reach_margin = first + second - float(np.linalg.norm(point))
    return np.array([shoulder, elbow]), reachable, reach_margin


def _fk(joints: np.ndarray) -> np.ndarray:
    first, second = 0.75, 0.55
    return np.array(
        [
            first * np.cos(joints[0]) + second * np.cos(np.sum(joints)),
            first * np.sin(joints[0]) + second * np.sin(np.sum(joints)),
        ]
    )


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
        estimated_object = (
            translation + _rotation(true_yaw + yaw_error) @ measured_camera
        )
    joints, reachable, reach_margin = _ik(estimated_object)
    endpoint = _fk(joints)
    pickup_error = float(np.linalg.norm(endpoint - true_object))
    tolerance = 0.055
    completed_states = 9 if reachable and pickup_error <= tolerance else 4
    fractions = np.linspace(0.0, 1.0, 31)
    joint_path = fractions[:, None] * joints
    endpoint_path = np.asarray([_fk(joint) for joint in joint_path])
    phase_error = np.array(
        [float(np.linalg.norm(point - true_object)) for point in endpoint_path]
    )
    signature = [pickup_error, reach_margin, float(completed_states)]
    return {
        "signature": signature,
        "sample_count": len(fractions),
        "metrics": [
            ("pickup_position_error", "Pickup Position Error", pickup_error, "m"),
            ("reachability_margin", "Reachability Margin", reach_margin, "m"),
            (
                "completed_task_states",
                "Preflight predicted task states",
                completed_states,
                "count",
            ),
        ],
        "plots": {
            "response": _plot(
                "Perception-guided approach in the base frame",
                "Base-frame x position (m)",
                "Base-frame y position (m)",
                [
                    _trace(
                        "End-effector approach",
                        endpoint_path[:, 0],
                        endpoint_path[:, 1],
                        "Base-frame x position",
                        "m",
                        "Base-frame y position",
                        "m",
                    ),
                    _trace(
                        "True object",
                        [true_object[0]],
                        [true_object[1]],
                        "Base-frame x position",
                        "m",
                        "Base-frame y position",
                        "m",
                    ),
                    _trace(
                        "Estimated object",
                        [estimated_object[0]],
                        [estimated_object[1]],
                        "Base-frame x position",
                        "m",
                        "Base-frame y position",
                        "m",
                    ),
                ],
            ),
            "mechanism": _plot(
                "Pickup tolerance through the approach",
                "Approach fraction (1)",
                "Object-position error (m)",
                [
                    _trace(
                        "Position error",
                        fractions,
                        phase_error,
                        "Approach fraction",
                        "1",
                        "Object-position error",
                        "m",
                    ),
                    _trace(
                        "Grasp tolerance",
                        fractions,
                        np.full_like(fractions, tolerance),
                        "Approach fraction",
                        "1",
                        "Object-position error",
                        "m",
                    ),
                ],
            ),
        },
        "observation": (
            f"Geometric preflight predicts {completed_states} of 9 conceptual states; this is not an execution count. "
            f"The final visual-to-contact error is {pickup_error:.3f} m against a "
            f"{tolerance:.3f} m gripper tolerance."
        ),
    }


def _result(model: dict[str, Any], broken: bool) -> dict[str, Any]:
    return {
        "metrics": [
            {
                "id": key,
                "label": label,
                "value": float(value),
                "unit": unit,
                "emphasis": "primary" if index == 0 else "normal",
            }
            for index, (key, label, value, unit) in enumerate(model["metrics"])
        ],
        "plots": model["plots"],
        "explanations": {
            "observation": model["observation"],
            "broken": BROKEN_TEXT,
            "recovery": RECOVERY_TEXT,
        },
        "diagnostics": {
            "item_number": ITEM_NUMBER,
            "broken_active": bool(broken),
            "sample_count": int(model["sample_count"]),
            "signature": [float(value) for value in model["signature"]],
            "software_only": True,
        },
    }


def _manipulation(noise_cm, yaw_error_deg=0.8, friction=0.5, broken=False):
    """Executed planar arm/gripper/object sequence; point-mass rigid links."""
    import math

    def rotate(a):
        return np.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]])

    def ik(point):
        c = (point @ point - 0.75**2 - 0.55**2) / (2 * 0.75 * 0.55)
        if abs(c) > 1:
            return None
        q2 = -math.acos(c)
        return np.array(
            [
                math.atan2(point[1], point[0])
                - math.atan2(0.55 * math.sin(q2), 0.75 + 0.55 * math.cos(q2)),
                q2,
            ]
        )

    def fk(q):
        return np.array(
            [
                0.75 * math.cos(q[0]) + 0.55 * math.cos(q.sum()),
                0.75 * math.sin(q[0]) + 0.55 * math.sin(q.sum()),
            ]
        )

    def dynamics(q, v, payload):
        m1, m2 = 1.0, 0.7 + payload
        cross = m2 * 0.75 * 0.55
        h = cross * math.sin(q[1])
        c = math.cos(q[1])
        M = np.array(
            [
                [
                    (m1 + m2) * 0.75**2 + m2 * 0.55**2 + 2 * cross * c,
                    m2 * 0.55**2 + cross * c,
                ],
                [m2 * 0.55**2 + cross * c, m2 * 0.55**2],
            ]
        )
        coriolis = np.array([-h * (2 * v[0] * v[1] + v[1] ** 2), h * v[0] ** 2])
        gravity = 9.81 * np.array(
            [
                (m1 + m2) * 0.75 * math.cos(q[0]) + m2 * 0.55 * math.cos(q.sum()),
                m2 * 0.55 * math.cos(q.sum()),
            ]
        )
        return M, coriolis, gravity

    object_true = np.array([0.28, 0.12]) + rotate(math.radians(25)) @ np.array(
        [0.72, 0.18]
    )
    measured = np.array([0.72, 0.18]) + 0.01 * noise_cm * np.array([0.6, -0.35])
    estimate = (
        measured
        if broken
        else np.array([0.28, 0.12])
        + rotate(math.radians(25 + yaw_error_deg)) @ measured
    )
    drop = np.array([0.50, 0.55])
    state = np.array([0.2, -1.2, 0.0, 0.0])
    object_position = object_true.copy()
    stage = 0
    entered = 0.0
    force = 0.0
    attached = False
    offset = np.zeros(2)
    target = state[:2].copy()
    events = []
    history = []
    success = False
    failure = ""
    grasp_error = None
    max_torque = 0.0
    dt = 0.01

    def derivative(y, goal, payload):
        q, v = y[:2], y[2:]
        M, C, g = dynamics(q, v, payload)
        demand = M @ (36 * (goal - q) - 12 * v) + C + g + 0.025 * v
        applied = np.clip(demand, -25.0, 25.0)
        acceleration = np.linalg.solve(M, applied - C - g - 0.025 * v)
        return np.r_[v, acceleration], applied

    for k in range(2401):
        t = k * dt
        tip = fk(state[:2])
        speed = np.linalg.norm(state[2:])
        error = np.linalg.norm(state[:2] - target)
        prior = stage
        if stage == 0:
            stage = 1
        elif stage == 1:
            target = ik(estimate)
            if target is None:
                failure = "unreachable estimated pickup"
                stage = 9
                target = state[:2].copy()
            else:
                stage = 2
        elif stage == 2 and error < 0.005 and speed < 0.015:
            stage = 3
        elif stage == 3:
            force = min(10.0, force + 30 * dt)
            if force >= 10.0:
                stage = 4
        elif stage == 4:
            grasp_error = float(np.linalg.norm(tip - object_true))
            if grasp_error > 0.055:
                failure = "gripper missed object"
                stage = 9
            elif 2 * friction * force < 0.45 * 9.81:
                failure = "insufficient vertical grasp support"
                stage = 9
            else:
                attached = True
                offset = object_true - tip
                target = ik(estimate + np.array([0, 0.12]))
                stage = 5
                if target is None:
                    failure = "unreachable lift"
                    stage = 9
                    attached = False
                    target = state[:2].copy()
        elif stage == 5 and error < 0.005 and speed < 0.015:
            target = ik(drop - offset)
            stage = 6
            if target is None:
                failure = "unreachable transfer"
                stage = 9
                target = state[:2].copy()
        elif stage == 6 and error < 0.005 and speed < 0.015:
            stage = 7
        elif stage == 7:
            attached = False
            force = max(0.0, force - 30 * dt)
            if force <= 0.0:
                target = ik(drop + np.array([0, 0.15]))
                stage = 8
        elif stage == 8 and error < 0.005 and speed < 0.015:
            success = bool(np.linalg.norm(object_position - drop) < 0.02)
            stage = 10
            if not success:
                failure = "placement outside tolerance"
        if stage not in (9, 10) and t - entered > 5.0:
            failure = "phase timeout"
            stage = 9
        if stage != prior:
            events.append(
                [
                    float(t),
                    int(prior),
                    int(stage),
                    float(np.linalg.norm(tip - object_true)),
                    float(2 * friction * force - 0.45 * 9.81),
                ]
            )
            entered = t
        if k % 5 == 0 or stage in (9, 10):
            history.append(
                [
                    t,
                    stage,
                    *state,
                    *tip,
                    *object_position,
                    force,
                    float(attached),
                    float(np.linalg.norm(object_position - drop)),
                ]
            )
        if stage in (9, 10):
            break
        payload = 0.45 if attached else 0.0
        # Resolve torque saturation crossings within each 10 ms task tick.
        step = dt / 8
        for _ in range(8):
            a, u = derivative(state, target, payload)
            b, ub = derivative(state + 0.5 * step * a, target, payload)
            c, uc = derivative(state + 0.5 * step * b, target, payload)
            d, ud = derivative(state + step * c, target, payload)
            state += step * (a + 2 * b + 2 * c + d) / 6
            max_torque = max(max_torque, float(np.max(np.abs([u, ub, uc, ud]))))
        if attached:
            object_position = fk(state[:2]) + offset
    return {
        "history": np.asarray(history),
        "events": np.asarray(events),
        "success": success,
        "failure": failure,
        "placement_error_m": float(np.linalg.norm(object_position - drop)),
        "grasp_error_m": float(
            grasp_error
            if grasp_error is not None
            else np.linalg.norm(fk(state[:2]) - object_true)
        ),
        "max_torque_nm": max_torque,
        "terminal_stage": int(stage),
        "true_object": object_true,
        "estimated_object": estimate,
        "drop_target": drop,
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    result = _result(_model(parameters, broken), broken)
    motion = _manipulation(
        float(parameters["vision_noise_cm"]),
        float(parameters.get("camera_yaw_error_deg", 0.8)),
        float(parameters.get("contact_friction_coefficient", 0.5)),
        broken,
    )
    result["diagnostics"]["manipulation"] = motion
    h = motion["history"]
    result["plots"]["executed_manipulation"] = _plot(
        "Executed arm and carried-object trajectory",
        "East position (m)",
        "North position (m)",
        [
            _trace("Arm endpoint", h[:, 6], h[:, 7], "East", "m", "North", "m"),
            _trace("Object", h[:, 8], h[:, 9], "East", "m", "North", "m"),
        ],
    )
    result["plots"]["execution_phases"] = _plot(
        "Actual task phase",
        "Elapsed time (s)",
        "Phase index (count)",
        [
            _trace(
                "Task phase",
                h[:, 0],
                h[:, 1],
                "Elapsed time",
                "s",
                "Phase index",
                "count",
            )
        ],
    )
    result.setdefault("tables", {})["execution_events"] = {
        "columns": [
            "Time (s)",
            "From phase",
            "To phase",
            "Tip to original object (m)",
            "Support margin (N)",
        ],
        "rows": [
            dict(
                zip(
                    [
                        "Time (s)",
                        "From phase",
                        "To phase",
                        "Tip to original object (m)",
                        "Support margin (N)",
                    ],
                    map(float, row),
                )
            )
            for row in motion["events"]
        ],
    }
    result["metrics"].extend(
        [
            {
                "id": "executed_placement_error",
                "label": "Executed object placement error",
                "value": motion["placement_error_m"],
                "unit": "m",
            },
            {
                "id": "executed_task_success",
                "label": "Executed task completed",
                "value": float(motion["success"]),
                "unit": "boolean",
            },
        ]
    )
    return result
