from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 67
BROKEN_TEXT = "Broken mode disables the monitor and commands unconstrained turns during the longest dropout."
RECOVERY_TEXT = "Restore uncertainty-aware guidance, enforce the turn-rate limit, and require the monitor to alarm on the injected dropout fault."


def _trace(
    name: str,
    x: Any,
    y: Any,
    x_quantity: str,
    x_unit: str,
    y_quantity: str,
    y_unit: str,
    *,
    mode: str = "lines",
) -> dict[str, Any]:
    return {
        "type": "scatter",
        "mode": mode,
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


def _arc(pose, speed, turn, dt):
    x, y, heading = pose
    angle = turn * dt
    distance = speed * dt * np.sinc(angle / (2 * np.pi))
    return np.array(
        [
            x + distance * np.cos(heading + angle / 2),
            y + distance * np.sin(heading + angle / 2),
            heading + angle,
        ]
    )


def _survey(dropout, limit, broken):
    dt = 0.05
    waypoints = np.array([[0.0, 0.0], [30.0, 0.0], [30.0, 20.0], [0.0, 20.0]])
    actual = np.array([0.0, 1.0, 0.0])
    estimated = actual.copy()
    leg = 0
    last_fix = 0.0
    rows = []
    for k in range(600):
        t = k * dt
        if k % 10 == 0 and not (5 <= t < 5 + dropout):
            estimated = actual + np.array(
                [0.05 * np.sin(t), 0.05 * np.cos(t), 0.002 * np.sin(2 * t)]
            )
            last_fix = t
        age = t - last_fix
        start, finish = waypoints[leg : leg + 2]
        tangent = finish - start
        length = np.linalg.norm(tangent)
        tangent /= length
        along = float((estimated[:2] - start) @ tangent)
        if along >= length - 1 and leg < 2:
            leg += 1
            start, finish = waypoints[leg : leg + 2]
            tangent = finish - start
            length = np.linalg.norm(tangent)
            tangent /= length
            along = float((estimated[:2] - start) @ tangent)
        target = start + np.clip(along + 4, 0, length) * tangent
        wanted = np.arctan2(target[1] - estimated[1], target[0] - estimated[0])
        error = np.arctan2(np.sin(wanted - estimated[2]), np.cos(wanted - estimated[2]))
        demanded = 1.5 * error
        turn = (
            demanded
            if broken
            else float(np.clip(demanded, -np.deg2rad(limit), np.deg2rad(limit)))
        )
        alarm = age > 3 and not broken
        speed = (
            0.0
            if alarm or (leg == 2 and np.linalg.norm(actual[:2] - finish) < 1)
            else 2.0
        )
        actual = _arc(actual, speed, turn, dt)
        estimated = _arc(estimated, speed, turn + np.deg2rad(0.3), dt)
        displacement = actual[:2] - start
        cross = abs(tangent[0] * displacement[1] - tangent[1] * displacement[0])
        rows.append(
            [
                *actual,
                *estimated,
                age,
                speed,
                np.rad2deg(turn),
                cross,
                float(alarm),
                leg,
            ]
        )
    return np.array(rows)


def _model(p, broken):
    limit = float(p["turn_rate_limit_deg_s"])
    h = _survey(float(p["gnss_dropout_s"]), limit, broken)
    cross = float(max(h[:, 9]))
    violation = float(max(0, max(abs(h[:, 8])) - limit))
    alarm = float(max(h[:, 10]))
    expired_motion = float(np.count_nonzero((h[:, 6] > 3) & (h[:, 7] > 0)))
    req = {
        "NAV-1": _requirement("Maximum cross-track distance", cross, "m", "<=", 12),
        "TURN-1": _requirement("Applied turn-rate excess", violation, "deg/s", "<=", 0),
        "MON-1": _requirement(
            "Moving samples with GNSS age above 3 s", expired_motion, "count", "<=", 0
        ),
    }
    req["SURVEY-PASS"] = _requirement(
        "Failed navigation/turn/monitor requirements",
        sum(not r["passed"] for r in req.values()),
        "count",
        "<=",
        0,
    )
    return {
        "signature": [cross, violation, alarm],
        "requirements": req,
        "metrics": [
            ("maximum_cross_track_error", "Maximum cross-track error", cross, "m"),
            ("turn_rate_violation", "Turn-rate excess", violation, "deg/s"),
            ("monitor_alarm", "Freshness hold activated", alarm, "bool"),
        ],
        "plots": {
            "response": _plot(
                "Actual and inertial/GNSS survey paths",
                "East position (m)",
                "North position (m)",
                [
                    _trace(
                        "Actual",
                        h[:, 0],
                        h[:, 1],
                        "East position",
                        "m",
                        "North position",
                        "m",
                    ),
                    _trace(
                        "Estimated",
                        h[:, 3],
                        h[:, 4],
                        "East position",
                        "m",
                        "North position",
                        "m",
                    ),
                    _trace(
                        "Waypoint corridor",
                        [0, 30, 30, 0],
                        [0, 0, 20, 20],
                        "East position",
                        "m",
                        "North position",
                        "m",
                    ),
                ],
            ),
            "mechanism": _plot(
                "GNSS outage and safe-hold threshold",
                "Time (s)",
                "GNSS age (s)",
                [
                    _trace(
                        "GNSS age",
                        0.05 * np.arange(600),
                        h[:, 6],
                        "Time",
                        "s",
                        "GNSS age",
                        "s",
                    ),
                    _trace(
                        "Hold threshold", [0, 30], [3, 3], "Time", "s", "GNSS age", "s"
                    ),
                ],
            ),
        },
        "history": {
            "survey_columns": [
                "x",
                "y",
                "heading",
                "estimated_x",
                "estimated_y",
                "estimated_heading",
                "gnss_age_s",
                "speed_m_s",
                "turn_deg_s",
                "cross_track_m",
                "hold",
                "leg",
            ],
            "survey": h.tolist(),
            "dt_s": 0.05,
        },
        "observation": "GNSS updates correct the inertial trajectory; a timed outage ages the last fix. Holding after 3 s trades mission progress for bounded motion without fresh navigation. The 30 s run is a corridor demonstration, not proof the full survey finishes.",
    }


def run(parameters):
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
