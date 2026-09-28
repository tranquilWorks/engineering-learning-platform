from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 68
BROKEN_TEXT = (
    "Broken mode suppresses the perceived map update, follows the stale route, freezes the dynamic "
    "obstacle prediction, and records no recovery event. The mission trace violates multiple requirements."
)
RECOVERY_TEXT = (
    "Fuse the obstacle observation into occupancy, replan around the changed cell, predict synchronized "
    "separation, wait until the crossing is safe, and retain dropout recovery in the deterministic replay."
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


def _grid_path(start, occupied):
    # A* ordered by (f, entire path): lexicographically first shortest route.
    goal = (8, 0)
    queue = [(abs(8 - start[0]) + abs(start[1]), (start,))]
    best = {}
    while queue:
        priority, path = min(queue)
        queue.remove((priority, path))
        cell = path[-1]
        cost = len(path) - 1
        if cell in best and best[cell] <= (cost, path):
            continue
        best[cell] = (cost, path)
        if cell == goal:
            return path
        for neighbor in sorted(
            (
                (cell[0] + 1, cell[1]),
                (cell[0] - 1, cell[1]),
                (cell[0], cell[1] + 1),
                (cell[0], cell[1] - 1),
            )
        ):
            if (
                not (0 <= neighbor[0] <= 8 and 0 <= neighbor[1] <= 2)
                or neighbor in occupied
                or neighbor in path
            ):
                continue
            route = path + (neighbor,)
            queue.append((cost + 1 + abs(8 - neighbor[0]) + abs(neighbor[1]), route))
    raise ValueError("No route in bounded grid")


def _separation(start, end, time, speed):
    relative = np.asarray(start, float) - [6.0, -2 + speed * time]
    velocity = np.asarray(end, float) - start - [0.0, speed]
    tau = float(np.clip(-relative @ velocity / max(velocity @ velocity, 1e-15), 0, 1))
    return float(np.linalg.norm(relative + tau * velocity))


def _mission(dropout, speed, broken):
    dropped = set(range(7, 7 + round(125 * dropout / 100)))
    cell = (0, 0)
    next_cell = cell
    segment_start = cell
    occupied = set()
    accepted = -1
    old_observation = None
    segments = []
    observations = []
    routes = []
    stale_moves = order_errors = collisions = 0
    recovered_sources = []
    held = False
    for tick in range(125):
        time = tick * 0.2
        if tick % 5 == 0:
            cell = next_cell
            segment_start = cell
        pose = np.asarray(segment_start, float) + (tick % 5) / 5 * (
            np.asarray(next_cell) - segment_start
        )
        detected = np.linalg.norm(pose - [4, 0]) <= 2.5
        if tick == 3:
            old_observation = (tick, detected)
        packets = [] if tick in dropped else [(tick, detected)]
        if tick == 35:
            packets.append(old_observation)
        for source, seen in packets:
            use = broken or source > accepted
            observations.append([source, tick, int(seen), int(use)])
            if use:
                order_errors += int(source <= accepted)
                accepted = source
                if seen and not broken:
                    occupied.add((4, 0))
        if tick % 5:
            continue
        age = (tick - accepted) * 0.2
        route = _grid_path(cell, set() if broken else occupied)
        routes.append([tick, [list(c) for c in route]])
        candidate = route[1] if len(route) > 1 else cell
        if age > 0.6 + 1e-12 and not broken:
            candidate = cell
            held = True
        predicted = _separation(cell, candidate, time, 0.0 if broken else speed)
        if predicted < 0.85 and not broken:
            candidate = cell
        moving = candidate != cell
        stale_moves += int(moving and age > 0.6 + 1e-12)
        if held and moving and accepted >= max(dropped, default=-1) + 1:
            recovered_sources.append(accepted)
        collisions += int(moving and ((4, 0) == cell or (4, 0) == candidate))
        separation = _separation(cell, candidate, time, speed)
        segments.append([time, *cell, *candidate, age, separation, int(moving)])
        next_cell = candidate
    points = [segments[0][1:3]] + [r[3:5] for r in segments]
    distance = float(np.linalg.norm(np.asarray(next_cell) - [8, 0]))
    # Recovery requires observed post-gap fresh movement, except with no drop gap.
    recovery_missing = int(bool(dropped) and not recovered_sources)
    return {
        "segments": segments,
        "observations": observations,
        "routes": routes,
        "points": points,
        "stale_moves": stale_moves,
        "source_order_errors": order_errors,
        "collisions": collisions,
        "goal_distance_m": distance,
        "recovery_missing": recovery_missing,
        "minimum_separation_m": min(r[6] for r in segments),
        "recovered_sources": recovered_sources,
    }


def _model(p, broken):
    history = _mission(
        float(p["range_dropout_percent"]),
        float(p["dynamic_obstacle_speed_m_s"]),
        broken,
    )
    req = {
        "R68-MAP": _requirement(
            "Executed static-obstacle contacts", history["collisions"], "count", "<=", 0
        ),
        "R68-REPLAN": _requirement(
            "Final goal distance", history["goal_distance_m"], "m", "<=", 0
        ),
        "R68-DYNAMIC": _requirement(
            "Continuous minimum moving-obstacle separation",
            history["minimum_separation_m"],
            "m",
            ">=",
            0.85,
        ),
        "R68-RECOVERY": _requirement(
            "Stale motion decisions plus missing fresh resume",
            history["stale_moves"] + history["recovery_missing"],
            "count",
            "<=",
            0,
        ),
        "R68-REPLAY": _requirement(
            "Accepted source-order inversions",
            history["source_order_errors"],
            "count",
            "<=",
            0,
        ),
    }
    violations = sum(not r["passed"] for r in req.values())
    signature = [
        float(violations == 0),
        history["minimum_separation_m"],
        float(violations),
    ]
    points = np.asarray(history["points"])
    segments = np.asarray(history["segments"])
    return {
        "signature": signature,
        "requirements": req,
        "metrics": [
            ("mission_success", "Mission success", signature[0], "bool"),
            (
                "minimum_dynamic_separation",
                "Minimum dynamic separation",
                signature[1],
                "m",
            ),
            (
                "capstone_requirement_violations",
                "Failed requirements",
                signature[2],
                "count",
            ),
        ],
        "plots": {
            "response": _plot(
                "Executed perception and replanning route",
                "Map x position (m)",
                "Map y position (m)",
                [
                    _trace(
                        "Executed",
                        points[:, 0],
                        points[:, 1],
                        "Map x position",
                        "m",
                        "Map y position",
                        "m",
                    ),
                    _trace(
                        "Static obstacle",
                        [4],
                        [0],
                        "Map x position",
                        "m",
                        "Map y position",
                        "m",
                    ),
                ],
            ),
            "mechanism": _plot(
                "Continuous separation along executed one-second segments",
                "Time (s)",
                "Separation (m)",
                [
                    _trace(
                        "Minimum separation",
                        segments[:, 0],
                        segments[:, 6],
                        "Time",
                        "s",
                        "Separation",
                        "m",
                    ),
                    _trace(
                        "Required",
                        [0, 25],
                        [0.85, 0.85],
                        "Time",
                        "s",
                        "Separation",
                        "m",
                    ),
                ],
            ),
        },
        "history": {**history, "sample_count": 125, "software_only": True},
        "observation": "Range observations arrive at 5 Hz; a 1 Hz decision loop checks source age, updates occupancy and replans. Separation is minimized continuously over each executed segment. Fresh post-dropout movement and accepted timestamps determine recovery and replay validity.",
    }


def run(parameters):
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
