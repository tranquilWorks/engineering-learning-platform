from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 69
BROKEN_TEXT = (
    "Broken mode skips the camera extrinsic, applies positive "
    "contact feedback without the energy tank, and bypasses timed-interface recovery."
)
RECOVERY_TEXT = (
    "Restore the calibrated pose chain, verify reach and positive grasp margin, regulate contact with "
    "passivity energy accounting, and require the replayed interface fault to recover before success."
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
        "type": "scatter",
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


def _requirement(quantity, value, unit, operator, threshold):
    value = float(value)
    passed = (
        value <= threshold + 1e-10 if operator == "<=" else value >= threshold - 1e-10
    )
    return {
        "quantity": quantity,
        "value": value,
        "unit": unit,
        "operator": operator,
        "threshold": threshold,
        "passed": bool(passed),
    }


def _result(model, broken):
    requirements = model["requirements"]
    columns = ["Requirement", "Quantity", "Value", "Unit", "Rule", "Verdict"]
    rows = [
        {
            "Requirement": key,
            "Quantity": r["quantity"],
            "Value": round(r["value"], 7),
            "Unit": r["unit"],
            "Rule": f"{r['operator']} {r['threshold']}",
            "Verdict": "pass" if r["passed"] else "fail",
        }
        for key, r in requirements.items()
    ]
    return {
        "metrics": [
            {"id": key, "label": label, "value": float(value), "unit": unit}
            for key, label, value, unit in model["metrics"]
        ],
        "plots": model["plots"],
        "tables": {"requirements": {"columns": columns, "rows": rows}},
        "explanations": {
            "observation": model["observation"],
            "broken": BROKEN_TEXT,
            "recovery": RECOVERY_TEXT,
        },
        "diagnostics": {
            "item_number": ITEM_NUMBER,
            "broken_active": broken,
            "signature": model["signature"],
            "requirements": requirements,
            **model["history"],
        },
    }


def _contact(broken, initial_tank=0.18):
    penetration = 0.0
    tank = initial_tank
    commands = []
    source = -1
    applied = 0.0
    rows = []
    for tick in range(200):
        force = 600 * penetration
        demand = (
            float(np.clip(0.08 * (10 + force), -0.15, 0.15))
            if broken
            else float(np.clip(0.012 * (10 - force), -0.025, 0.025))
        )
        commands.append(demand)
        arrivals = []
        if tick >= 3 and not 80 <= tick - 3 <= 95:
            arrivals.append(tick - 3)
        if tick == 120:
            arrivals.append(50)
        old_accepted = 0
        for stamp in arrivals:
            if broken or stamp > source:
                old_accepted += int(stamp <= source)
                source = stamp
                applied = commands[stamp]
        age = (tick - source) * 0.01 if source >= 0 else (tick + 1) * 0.01
        if not broken and (source < 0 or age > 0.04 + 1e-12):
            applied = 0.0
        requested = float(np.clip(penetration + applied * 0.01, 0, 0.05))
        if not broken:
            requested = min(
                requested, float(np.sqrt(penetration**2 + 2 * max(tank, 0) / 600))
            )
        work = max(0.0, 300 * (requested**2 - penetration**2))
        tank -= work
        penetration = requested
        rows.append(
            [
                (tick + 1) * 0.01,
                600 * penetration,
                float(tank),
                applied,
                source,
                age,
                old_accepted,
            ]
        )
    return rows


def _model(parameters: dict[str, Any], broken: bool) -> dict[str, Any]:
    noise = 0.01 * float(parameters["vision_noise_cm"])
    friction = float(parameters["contact_friction_coefficient"])
    camera_point = np.array([0.72, 0.18])
    true_point = np.array([0.28, 0.12]) + _rotation(np.deg2rad(25.0)) @ camera_point
    measured = camera_point + noise * np.array([0.5, -0.25])
    estimate = (
        measured
        if broken
        else np.array([0.28, 0.12]) + _rotation(np.deg2rad(25.0)) @ measured
    )
    first, second = 0.75, 0.55
    cosine = (float(estimate @ estimate) - first**2 - second**2) / (
        2.0 * first * second
    )
    elbow_angle = -float(np.arccos(np.clip(cosine, -1.0, 1.0)))
    shoulder = float(
        np.arctan2(estimate[1], estimate[0])
        - np.arctan2(second * np.sin(elbow_angle), first + second * np.cos(elbow_angle))
    )
    endpoint = np.array(
        [
            first * np.cos(shoulder) + second * np.cos(shoulder + elbow_angle),
            first * np.sin(shoulder) + second * np.sin(shoulder + elbow_angle),
        ]
    )
    pickup_error = float(np.linalg.norm(endpoint - true_point))
    support_margin = 2 * friction * 10 - 4.4
    contact = _contact(broken)
    final_force_error = abs(contact[-1][1] - 10)
    minimum_tank = min(row[2] for row in contact)
    expired_nonzero = sum(
        row[5] > 0.04 + 1e-12 and abs(row[3]) > 1e-12 for row in contact
    )
    stale_accepts = sum(row[6] for row in contact)
    recovery_error = final_force_error if contact[-1][4] >= 96 else 10.0
    req = {
        "R69-PERCEPTION": _requirement(
            "Pickup position error", pickup_error, "m", "<=", 0.055
        ),
        "R69-KINEMATICS": _requirement(
            "Reach cosine magnitude", abs(cosine), "1", "<=", 1
        ),
        "R69-GRASP": _requirement(
            "Two-contact vertical support margin", support_margin, "N", ">=", 0
        ),
        "R69-CONTACT": _requirement(
            "Final force error", final_force_error, "N", "<=", 3
        ),
        "R69-ENERGY": _requirement("Minimum tank energy", minimum_tank, "J", ">=", 0),
        "R69-INTERFACE": _requirement(
            "Expired nonzero commands plus source-order inversions",
            expired_nonzero + stale_accepts,
            "count",
            "<=",
            0,
        ),
        "R69-RECOVERY": _requirement(
            "Post-gap fresh-command force error", recovery_error, "N", "<=", 3
        ),
    }
    success = float(all(r["passed"] for r in req.values()))
    signature = [success, pickup_error, float(minimum_tank)]
    approach = np.linspace(0, 1, 31)[:, None] * endpoint
    history = np.asarray(contact)
    return {
        "signature": signature,
        "requirements": req,
        "metrics": [
            ("capstone_success", "Capstone success", success, "bool"),
            ("pickup_position_error", "Pickup position error", pickup_error, "m"),
            ("minimum_passivity_energy", "Minimum tank energy", minimum_tank, "J"),
        ],
        "plots": {
            "response": _plot(
                "Calibrated two-link approach",
                "Base-frame x position (m)",
                "Base-frame y position (m)",
                [
                    _trace(
                        "Approach",
                        approach[:, 0],
                        approach[:, 1],
                        "Base-frame x position",
                        "m",
                        "Base-frame y position",
                        "m",
                    ),
                    _trace(
                        "True object",
                        [true_point[0]],
                        [true_point[1]],
                        "Base-frame x position",
                        "m",
                        "Base-frame y position",
                        "m",
                    ),
                ],
            ),
            "mechanism": _plot(
                "Force through delayed commands and a timed dropout",
                "Time (s)",
                "Contact force (N)",
                [
                    _trace(
                        "Force",
                        history[:, 0],
                        history[:, 1],
                        "Time",
                        "s",
                        "Contact force",
                        "N",
                    ),
                    _trace(
                        "Target", [0, 2], [10, 10], "Time", "s", "Contact force", "N"
                    ),
                ],
            ),
        },
        "history": {
            "contact": contact,
            "contact_columns": [
                "time_s",
                "force_n",
                "tank_j",
                "applied_velocity_command_m_s",
                "source_tick",
                "age_s",
                "accepted_old_source",
            ],
            "sample_count": 200,
            "software_only": True,
            "endpoint_m": endpoint.tolist(),
            "support_margin_n": support_margin,
        },
        "observation": "The calibrated reach feeds a timed force controller. Exact spring work debits the energy tank, including first contact. The requirement table measures stale-command handling and fresh-command recovery; it does not preassign a recovery flag.",
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


def run(parameters):
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
