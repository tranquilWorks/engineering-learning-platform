from __future__ import annotations

import math
from typing import Any

PRIMARY = "friction_coefficient"
SECONDARY = "track_half_width_m"
PRIMARY_RANGE = (0.70, 1.40)
SECONDARY_RANGE = (2.0, 6.0)
FIELDS = [
    "best_offset_m",
    "effective_radius_m",
    "corner_path_length_m",
    "grip_speed_limit_m_s",
    "lap_time_proxy_s",
    "gain_from_center_s",
    "constraint_margin_m",
    "evaluated_candidates",
    "invalid",
]


def _score(offset: float, friction: float) -> tuple[float, float, float, float]:
    radius = 45.0 + offset
    path_length = 0.5 * math.pi * 45.0 + 0.08 * offset * offset
    speed_limit = math.sqrt(friction * 9.81 * radius)
    lap_time = path_length / speed_limit + 200.0 / 45.0
    return radius, path_length, speed_limit, lap_time


def _optimize(friction: float, half_width: float, broken: bool) -> tuple[list[float], list[float], list[float]]:
    offsets = [-half_width + 2.0 * half_width * index / 40.0 for index in range(41)]
    times = [_score(offset, friction)[3] for offset in offsets]
    if broken:
        best_offset = half_width + 1.0
        radius, length, speed, best_time = _score(best_offset, friction)
    else:
        best_index = min(range(len(offsets)), key=times.__getitem__)
        best_offset = offsets[best_index]
        radius, length, speed, best_time = _score(best_offset, friction)
    center_time = _score(0.0, friction)[3]
    margin = half_width - abs(best_offset)
    invalid = broken or margin < -1e-12
    signature = [best_offset, radius, length, speed, best_time, center_time - best_time, margin, 41.0, float(invalid)]
    return signature, offsets, times


def _plot(name: str, x: list[float], y: list[float], x_title: str, y_title: str) -> dict[str, Any]:
    return {
        "data": [{"type": "scatter", "mode": "lines+markers", "name": name, "x": x, "y": y}],
        "layout": {"title": {"text": "Optimize a Racing Line"}, "xaxis": {"title": x_title}, "yaxis": {"title": y_title}, "uirevision": "keep-view"},
        "config": {"responsive": True, "displaylogo": False},
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    primary = float(parameters[PRIMARY])
    secondary = float(parameters[SECONDARY])
    broken = bool(parameters["broken_mode"])
    if not math.isfinite(primary) or not PRIMARY_RANGE[0] <= primary <= PRIMARY_RANGE[1]:
        raise ValueError(f"{PRIMARY} outside declared finite range")
    if not math.isfinite(secondary) or not SECONDARY_RANGE[0] <= secondary <= SECONDARY_RANGE[1]:
        raise ValueError(f"{SECONDARY} outside declared finite range")
    signature, offsets, times = _optimize(primary, secondary, broken)
    if len(signature) != len(FIELDS) or not all(math.isfinite(value) for value in signature):
        raise ValueError("racing-line search produced an invalid signature")
    primary_values = [0.70, 1.05, 1.40]
    secondary_values = [2.0, 4.0, 6.0]
    failed = _optimize(primary, secondary, True)[0]
    recovered = _optimize(1.05, 4.0, False)[0]
    return {
        "metrics": [
            {"id": "offset", "label": "Best path offset", "value": signature[0], "unit": "m", "emphasis": "primary"},
            {"id": "time", "label": "Lap-time proxy", "value": signature[4], "unit": "s"},
            {"id": "valid", "label": "Line feasible", "value": not bool(signature[-1]), "unit": "boolean"},
        ],
        "plots": {
            "response": _plot("feasible candidates", offsets, times, "lateral offset (m)", "lap-time proxy (s)"),
            "primary_sweep": _plot(PRIMARY, primary_values, [_optimize(value, secondary, False)[0][4] for value in primary_values], "friction coefficient", "best lap-time proxy (s)"),
            "secondary_sweep": _plot(SECONDARY, secondary_values, [_optimize(primary, value, False)[0][5] for value in secondary_values], "track half-width (m)", "gain from center (s)"),
            "broken_recovery": {
                "data": [
                    {"type": "bar", "name": "infeasible selection", "x": FIELDS[:-1], "y": failed[:-1]},
                    {"type": "bar", "name": "recovered optimum", "x": FIELDS[:-1], "y": recovered[:-1]},
                ],
                "layout": {"barmode": "group", "xaxis": {"title": "optimization quantity"}, "yaxis": {"title": "reported value"}},
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "A wider radius raises the grip-limited speed, but the offset-squared distance penalty prevents radius from being free.",
            "broken": "Broken mode scores a line one metre outside the declared track boundary and reports a negative feasibility margin.",
            "recovery": "Search only the 41 bounded offsets, include both distance and grip speed, and choose the minimum feasible time.",
        },
        "diagnostics": {"item_id": "P21", "signature": signature, "fields": FIELDS, "broken_active": broken, "bounded_points": len(offsets)},
    }
