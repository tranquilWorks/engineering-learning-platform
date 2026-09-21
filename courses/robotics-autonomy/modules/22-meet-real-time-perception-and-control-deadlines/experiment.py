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


def _response_time(
    wcet: float, period: float, higher: list[tuple[float, float]]
) -> float:
    response = wcet
    for _ in range(100):
        updated = wcet + sum(
            np.ceil(response / hp_period) * hp_wcet for hp_period, hp_wcet in higher
        )
        if updated == response or updated > 10_000.0:
            return float(updated)
        response = updated
    return float(response)


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    horizon = round(float(parameters["horizon_ms"]))
    tasks = [
        (20, round(float(parameters["control_wcet_ms"]))),
        (50, round(float(parameters["perception_wcet_ms"]))),
        (100, round(float(parameters["planning_wcet_ms"]))),
    ]
    broken = bool(parameters["broken_mode"])
    order = [2, 1, 0] if broken else [0, 1, 2]
    priority = {task_index: rank for rank, task_index in enumerate(order)}
    jobs: list[dict[str, int]] = []
    responses: list[list[int]] = [[], [], []]
    running = np.full(horizon, -1, dtype=int)
    misses = 0
    total_jobs = 0
    for now in range(horizon):
        for task_index, (period, wcet) in enumerate(tasks):
            if now % period == 0:
                jobs.append(
                    {
                        "task": task_index,
                        "release": now,
                        "deadline": now + period,
                        "remaining": wcet,
                    }
                )
                total_jobs += 1
        for job in jobs:
            if job["deadline"] == now and job["remaining"] > 0:
                misses += 1
        ready = [job for job in jobs if job["release"] <= now and job["remaining"] > 0]
        if ready:
            active = min(ready, key=lambda job: (priority[job["task"]], job["release"]))
            running[now] = active["task"]
            active["remaining"] -= 1
            if active["remaining"] == 0:
                responses[active["task"]].append(now + 1 - active["release"])
    analytic = np.zeros(3)
    for rank, task_index in enumerate(order):
        higher = [
            (float(tasks[index][0]), float(tasks[index][1])) for index in order[:rank]
        ]
        analytic[task_index] = _response_time(
            float(tasks[task_index][1]), float(tasks[task_index][0]), higher
        )
    observed = np.array(
        [max(values) if values else horizon for values in responses], dtype=float
    )
    utilization = sum(wcet / period for period, wcet in tasks)
    schedulable = float(all(analytic[index] <= tasks[index][0] for index in range(3)))
    signature = [
        utilization,
        observed[0],
        observed[1],
        observed[2],
        schedulable,
        float(total_jobs),
    ]
    task_names = ["Control", "Perception", "Planning"]
    return {
        "metrics": [
            {
                "id": "utilization",
                "label": "Total utilization",
                "value": utilization,
                "unit": "ratio",
                "emphasis": "primary",
            },
            {
                "id": "deadline_misses",
                "label": "Observed deadline misses",
                "value": misses,
                "unit": "jobs",
            },
            {
                "id": "control_response",
                "label": "Worst control response",
                "value": observed[0],
                "unit": "ms",
            },
            {
                "id": "schedulable",
                "label": "Analytically schedulable",
                "value": "yes" if schedulable else "no",
                "unit": None,
            },
        ],
        "plots": {
            "response": {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "Running task code",
                        "x": np.arange(horizon),
                        "y": running,
                    }
                ],
                "layout": _layout(
                    "Preemptive fixed-priority schedule", "Time (ms)", "Task code (-)"
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "mechanism": {
                "data": [
                    {
                        "type": "bar",
                        "name": "Observed response",
                        "x": task_names,
                        "y": observed,
                    },
                    {
                        "type": "bar",
                        "name": "Deadline",
                        "x": task_names,
                        "y": [task[0] for task in tasks],
                    },
                ],
                "layout": _layout(
                    "Worst response versus deadline", "Periodic task (-)", "Time (ms)"
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "Synchronous event simulation matches fixed-point response-time analysis: short-period control preempts longer work and remains within its 20 ms deadline.",
            "broken": "Broken mode reverses priorities. The critical-instant bound is already 48 ms, and queued control work reaches a 51 ms observed response within the default horizon even though total utilization remains below one.",
            "recovery": "Restore rate-monotonic priority, use WCET rather than average execution time, and verify each response time against its own deadline.",
        },
        "diagnostics": {
            "item_id": "P22",
            "reference_basis": "independent event-driven schedule plus fixed-point response-time analysis",
            "broken_active": broken,
            "sample_count": horizon,
            "analytic_response_ms": analytic.tolist(),
            "signature": [float(value) for value in signature],
        },
    }
