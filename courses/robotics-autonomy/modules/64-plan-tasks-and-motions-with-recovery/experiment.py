from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 64
BROKEN_TEXT = (
    "Broken mode executes the cheapest symbolic plan once and never feeds the failed corridor "
    "motion edge back into planning. The trace stops with the object outside the goal region."
)
RECOVERY_TEXT = (
    "Monitor geometric clearance during execution, blacklist the failed grasp-carry edge, return "
    "to the last certified state, and search again for the feasible side-grasp branch."
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


def _plan(corridor_width: float, blocked: set[tuple[str, str]]) -> list[tuple[str, str, float]]:
    edges = {"start": [("approach", 2.0)],
             "approach": [("top", 1.0), ("side", 1.6)],
             "top": [("goal", 4.0)], "side": [("goal", 4.5)]}
    required = {("top", "goal"): 0.24, ("side", "goal"): 0.16}
    queue: list[tuple[float, str, list[tuple[str, str, float]]]] = [(0.0, "start", [])]
    best = {"start": 0.0}
    while queue:
        cost, state, path = min(queue, key=lambda item: (item[0], item[1]))
        queue.remove((cost, state, path))
        if state == "goal":
            return path
        if cost > best.get(state, float("inf")) + 1.0e-12:
            continue
        for target, duration in edges.get(state, []):
            edge = (state, target)
            if edge in blocked or corridor_width + 1.0e-12 < required.get(edge, 0.0):
                continue
            candidate = cost + duration
            if candidate < best.get(target, float("inf")) - 1.0e-12:
                best[target] = candidate
                queue.append((candidate, target, path + [(state, target, duration)]))
    raise RuntimeError("task-and-motion search exhausted its bounded graph")


def _model(parameters: dict[str, Any], broken: bool) -> dict[str, Any]:
    corridor = float(parameters["corridor_width_m"])
    model_error = 0.01 * float(parameters["geometry_error_cm"])
    actual_width = corridor - model_error
    blocked: set[tuple[str, str]] = set()
    plan = _plan(corridor, blocked)
    cumulative = [0.0]
    margins: list[float] = []
    replans = 0
    success = False
    total = 0.0
    while True:
        failed_edge: tuple[str, str] | None = None
        for source, target, duration in plan:
            total += duration
            cumulative.append(total)
            if target == "goal":
                required = 0.24 if source == "top" else 0.16
                margin = actual_width - required
                margins.append(margin)
                if margin < -1.0e-12:
                    failed_edge = (source, target)
                    break
                success = True
        if success or failed_edge is None or broken:
            break
        blocked.add(failed_edge)
        replans += 1
        total += 1.0
        cumulative.append(total)
        plan = _plan(corridor, blocked)
        plan = [edge for edge in plan if edge[0] != "start"]
    attempts = np.arange(1, len(margins) + 1, dtype=float)
    signature = [float(success), float(replans), total]
    return {"signature": signature, "sample_count": len(cumulative) + len(margins),
            "metrics": [("task_success", "Task Success", float(success), "1"),
                        ("motion_replans", "Motion Replans", replans, "count"),
                        ("executed_task_time", "Executed Task Time", total, "s")],
            "plots": {"response": _plot("Executed task-and-motion trace", "Executed transition (count)",
                "Cumulative task time (s)", [
                    _trace("Execution", np.arange(len(cumulative)), cumulative, "Executed transition", "count",
                           "Cumulative task time", "s")]),
                "mechanism": _plot("Corridor feasibility at each carry attempt", "Carry attempt (count)",
                "Geometric clearance margin (m)", [
                    _trace("Measured margin", attempts, margins, "Carry attempt", "count",
                           "Geometric clearance margin", "m"),
                    _trace("Feasibility boundary", attempts, np.zeros_like(attempts), "Carry attempt", "count",
                           "Geometric clearance margin", "m")])},
            "observation": (f"Execution observed {len(margins)} carry attempt(s), performed {replans} "
                            f"bounded replan(s), and ended with task success={int(success)}.")}


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
