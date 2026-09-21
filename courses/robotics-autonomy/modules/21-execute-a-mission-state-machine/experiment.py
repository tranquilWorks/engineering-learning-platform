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
    return {"type": "scatter", "mode": "lines", "name": name, "x": x, "y": y}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    target_detect = float(parameters["target_detect_s"])
    execute_duration = float(parameters["execute_duration_s"])
    watchdog = float(parameters["watchdog_s"])
    fault_time = float(parameters["fault_time_s"])
    broken = bool(parameters["broken_mode"])
    dt = 0.1
    times = np.arange(0.0, 12.0 + 0.5 * dt, dt)
    states = np.zeros(len(times), dtype=int)
    state = 0
    entered = 0.0
    transition_times: list[float] = []
    for index in range(1, len(times)):
        now = times[index]
        previous = state
        if not broken and now >= fault_time and state not in {4, 5}:
            state = 4
        elif state == 0 and now >= 0.2:
            state, entered = 1, now
        elif state == 1:
            if now >= target_detect:
                state, entered = 2, now
            elif now - entered >= watchdog:
                state, entered = 4, now
        elif state == 2 and now - entered >= 1.0:
            state, entered = 3, now
        elif state == 3 and now - entered >= execute_duration:
            state, entered = 5, now
        states[index] = state
        if state != previous:
            transition_times.append(now)
        if state in {4, 5} and previous == state:
            states[index:] = state
            break
    terminal = np.flatnonzero(np.isin(states, [4, 5]))
    terminal_time = times[terminal[0]] if len(terminal) else times[-1]
    fault_index = int(np.searchsorted(times, fault_time, side="left"))
    unsafe = int(np.sum(np.isin(states[fault_index:], [1, 2, 3])))
    event_fault = (times >= fault_time).astype(float)
    event_detect = (times >= target_detect).astype(float)
    signature = [
        float(states[-1]),
        terminal_time,
        float(unsafe),
        float(np.count_nonzero(np.diff(states))),
        float(states[-1] == 5),
    ]
    names = {0: "INIT", 1: "SEARCH", 2: "TRACK", 3: "EXECUTE", 4: "SAFE", 5: "COMPLETE"}
    return {
        "metrics": [
            {
                "id": "final_state",
                "label": "Final mission state",
                "value": names[int(states[-1])],
                "unit": None,
                "emphasis": "primary",
            },
            {
                "id": "terminal_time",
                "label": "Terminal-state time",
                "value": terminal_time,
                "unit": "s",
            },
            {
                "id": "unsafe_ticks",
                "label": "Active ticks after fault",
                "value": unsafe,
                "unit": "ticks",
            },
            {
                "id": "transition_count",
                "label": "State transitions",
                "value": np.count_nonzero(np.diff(states)),
                "unit": "transitions",
            },
        ],
        "plots": {
            "response": {
                "data": [_trace("Mission state code", times, states)],
                "layout": _layout(
                    "Mission state execution", "Time (s)", "State code (-)"
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "mechanism": {
                "data": [
                    _trace("Target detected", times, event_detect),
                    _trace("Fault active", times, event_fault),
                ],
                "layout": _layout(
                    "Guard-event timeline", "Time (s)", "Event active (0/1)"
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "The nominal mission advances INIT to SEARCH, TRACK, and EXECUTE, while timeout and global fault guards route execution to a terminal SAFE state.",
            "broken": "Broken mode omits the global fault guard. The mission remains active for twenty ticks after the injected fault and reaches COMPLETE despite unsafe state.",
            "recovery": "Evaluate the global fault guard before local progress transitions in every nonterminal state and make SAFE terminal until an explicit reset policy runs.",
        },
        "diagnostics": {
            "item_id": "P21",
            "reference_basis": "independent table-driven mission transition schedule",
            "broken_active": broken,
            "sample_count": len(times),
            "transition_times_s": transition_times,
            "signature": [float(value) for value in signature],
        },
    }
