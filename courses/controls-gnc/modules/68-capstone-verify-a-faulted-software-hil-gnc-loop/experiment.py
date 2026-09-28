from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 68
BROKEN_TEXT = "Broken mode holds the last command through stale/drop intervals and suppresses the watchdog, violating fail-zero behavior."
RECOVERY_TEXT = "Restore timestamp checks and fail-zero watchdog, rerun the deterministic fault schedule, and retain the physical-HIL gap."


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


def _loop(latency, fraction, broken):
    dt, count = 0.02, 500
    delay = int(np.ceil(latency / 1000 / dt - 1e-12))
    dropped = set(range(150, min(count, 150 + round(count * fraction))))
    queue = {}
    state = 0.0
    applied = 0.0
    source = -1
    rows = []
    events = []
    for k in range(count):
        command = float(np.clip(2 * (1 - state), -3, 3))
        if k not in dropped:
            arrival = k + delay
            queue.setdefault(arrival, []).append((k, command))
            if k == 50 and fraction > 0:
                queue.setdefault(k + 50 + delay, []).append((k, command))
        for stamp, value in queue.get(k, []):
            accepted = broken or stamp > source
            events.append([stamp, k, value, float(accepted)])
            if accepted:
                source, applied = stamp, value
        age = (k - source) * dt if source >= 0 else (k + 1) * dt
        expired = source < 0 or age > 0.05 + 1e-12
        watchdog = expired and not broken
        if watchdog:
            applied = 0.0
        state = np.exp(-dt) * state - np.expm1(-dt) * applied
        rows.append(
            [state, command, applied, age, float(watchdog), float(expired), source]
        )
    return np.array(rows), np.array(events), len(dropped)


def _model(p, broken):
    h, events, drops = _loop(
        float(p["one_way_latency_ms"]), float(p["packet_drop_fraction"]), broken
    )
    late = (
        float(np.mean((events[:, 1] - events[:, 0]) * 0.02 > 0.03))
        if len(events)
        else 1.0
    )
    watch = float(np.mean(h[:, 4]))
    unsafe = int(np.count_nonzero((h[:, 5] > 0) & (abs(h[:, 2]) > 1e-12)))
    tracking = float(np.sqrt(np.mean((h[250:, 0] - 2 / 3) ** 2)))
    req = {
        "TIME-1": _requirement("Late delivered packets", late, "fraction", "<=", 0.01),
        "LOSS-1": _requirement(
            "Dropped source commands", drops / 500, "fraction", "<=", 0.2
        ),
        "SAFE-1": _requirement(
            "Expired nonzero actuator samples", unsafe, "count", "<=", 0
        ),
        "TRACK-1": _requirement(
            "Settled error from proportional-loop equilibrium", tracking, "1", "<=", 0.4
        ),
    }
    sig = [late, watch, float(all(r["passed"] for r in req.values()))]
    return {
        "signature": sig,
        "requirements": req,
        "metrics": [
            ("deadline_miss_fraction", "Late delivered packets", late, "fraction"),
            (
                "watchdog_activation_fraction",
                "Watchdog-active samples",
                watch,
                "fraction",
            ),
            ("requirements_passed", "Requirements passed", sig[2], "bool"),
        ],
        "plots": {
            "response": _plot(
                "Plant driven by delivered commands",
                "Time (s)",
                "Plant state (1)",
                [
                    _trace(
                        "Plant state",
                        0.02 * np.arange(1, 501),
                        h[:, 0],
                        "Time",
                        "s",
                        "Plant state",
                        "1",
                    ),
                    _trace(
                        "No-fault equilibrium",
                        [0, 10],
                        [2 / 3, 2 / 3],
                        "Time",
                        "s",
                        "Plant state",
                        "1",
                    ),
                ],
            ),
            "mechanism": _plot(
                "Source timestamp age at the actuator",
                "Time (s)",
                "Command age (s)",
                [
                    _trace(
                        "Age",
                        0.02 * np.arange(500),
                        h[:, 3],
                        "Time",
                        "s",
                        "Command age",
                        "s",
                    ),
                    _trace(
                        "Fail-zero threshold",
                        [0, 10],
                        [0.05, 0.05],
                        "Time",
                        "s",
                        "Command age",
                        "s",
                    ),
                ],
            ),
        },
        "history": {
            "loop": h.tolist(),
            "loop_columns": [
                "state",
                "source_command",
                "applied_command",
                "age_s",
                "watchdog",
                "expired",
                "accepted_source_tick",
            ],
            "events": events.tolist(),
            "event_columns": ["source_tick", "arrival_tick", "command", "accepted"],
            "dropped_commands": drops,
            "dt_s": 0.02,
        },
        "observation": "Virtual source/arrival events drive the closed-loop plant. The contiguous drop burst and delayed old packet test source ordering and fail-zero behavior. This is software timing, not physical HIL or an operating-system deadline benchmark.",
    }


def run(parameters):
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
