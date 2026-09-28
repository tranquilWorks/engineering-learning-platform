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


def run(parameters):
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
