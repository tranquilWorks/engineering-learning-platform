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


def _trace(name: str, x: Any, y: Any) -> dict[str, Any]:
    return {"type": "scatter", "mode": "lines+markers", "name": name, "x": x, "y": y}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    navigate_needed = round(float(parameters["navigate_ticks"]))
    failures = round(float(parameters["grasp_failures"]))
    retry_limit = round(float(parameters["retry_limit"]))
    ticks = round(float(parameters["mission_ticks"]))
    broken = bool(parameters["broken_mode"])
    state = 0
    navigate_progress = 0
    attempts = 0
    deliver_progress = 0
    transitions = 0
    completion = ticks
    history: list[int] = []
    progress_history: list[float] = []
    for tick in range(ticks):
        previous = state
        if state == 0:
            navigate_progress = 1 if broken else navigate_progress + 1
            if navigate_progress >= navigate_needed:
                state = 1
        elif state == 1:
            attempts += 1
            if attempts <= failures:
                if attempts > retry_limit:
                    state = 4
            else:
                state = 2
        elif state == 2:
            deliver_progress += 1
            if deliver_progress >= 3:
                state = 3
        if state != previous:
            transitions += 1
        history.append(state)
        progress_history.append(
            float(
                navigate_progress
                if state == 0
                else attempts
                if state == 1
                else deliver_progress
            )
        )
        if state in {3, 4}:
            completion = tick + 1
            history.extend([state] * (ticks - tick - 1))
            progress_history.extend([progress_history[-1]] * (ticks - tick - 1))
            break
    signature = [
        float(state),
        float(completion),
        float(attempts),
        float(transitions),
        float(state == 3),
    ]
    labels = {0: "Navigate", 1: "Grasp", 2: "Deliver", 3: "Done", 4: "Failed"}
    return {
        "metrics": [
            {
                "id": "final_status",
                "label": "Final tree status",
                "value": labels[state],
                "unit": None,
                "emphasis": "primary",
            },
            {
                "id": "completion_tick",
                "label": "Terminal tick or budget",
                "value": completion,
                "unit": "ticks",
            },
            {
                "id": "grasp_attempts",
                "label": "Grasp attempts",
                "value": attempts,
                "unit": "attempts",
            },
            {
                "id": "node_transitions",
                "label": "Active-node transitions",
                "value": transitions,
                "unit": "transitions",
            },
        ],
        "plots": {
            "response": {
                "data": [_trace("Active node code", np.arange(len(history)), history)],
                "layout": _layout(
                    "Behavior-tree execution", "Mission tick (-)", "Node code (-)"
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "mechanism": {
                "data": [
                    _trace(
                        "Active child progress",
                        np.arange(len(progress_history)),
                        progress_history,
                    ),
                    _trace(
                        "Grasp attempts",
                        np.arange(len(history)),
                        np.minimum(np.arange(len(history)) + 1, attempts),
                    ),
                ],
                "layout": _layout(
                    "Stateful child progress", "Mission tick (-)", "Progress count (-)"
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "The sequence remembers its RUNNING child, advances only after SUCCESS, and lets the retry decorator absorb a bounded number of grasp failures.",
            "broken": "Broken mode resets navigation progress every tick, so a multi-tick RUNNING action can never finish and downstream grasp/delivery nodes are never reached.",
            "recovery": "Preserve node-local progress and propagate RUNNING distinctly from FAILURE; bound retries so persistent grasp faults terminate explicitly.",
        },
        "diagnostics": {
            "item_id": "P20",
            "reference_basis": "independent closed-form behavior-tree tick schedule",
            "broken_active": broken,
            "sample_count": len(history),
            "signature": [float(value) for value in signature],
        },
    }
