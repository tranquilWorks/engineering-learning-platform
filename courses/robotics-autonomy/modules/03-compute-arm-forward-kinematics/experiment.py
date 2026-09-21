from __future__ import annotations

from typing import Any

import numpy as np


def _layout(title: str, x: str, y: str, equal: bool = False) -> dict[str, Any]:
    layout: dict[str, Any] = {"title": {"text": title, "x": 0.02}, "xaxis": {"title": x}, "yaxis": {"title": y}, "legend": {"orientation": "h"}, "margin": {"l": 65, "r": 20, "t": 55, "b": 55}, "hovermode": "closest", "uirevision": "keep-view"}
    if equal:
        layout["yaxis"]["scaleanchor"] = "x"
    return layout


def _trace(name: str, x: Any, y: Any, mode: str = "lines") -> dict[str, Any]:
    return {"type": "scatter", "mode": mode, "name": name, "x": x, "y": y}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    q1 = np.radians(float(parameters["joint1_deg"]))
    q2 = np.radians(float(parameters["joint2_deg"]))
    link1 = float(parameters["link1_m"])
    link2 = float(parameters["link2_m"])
    broken = bool(parameters["broken_mode"])
    elbow = np.array([link1 * np.cos(q1), link1 * np.sin(q1)])
    second_angle = q2 if broken else q1 + q2
    tool = elbow + link2 * np.array([np.cos(second_angle), np.sin(second_angle)])
    q2_sweep = np.linspace(-np.pi, np.pi, 361)
    sweep_x = elbow[0] + link2 * np.cos(q1 + q2_sweep)
    sweep_y = elbow[1] + link2 * np.sin(q1 + q2_sweep)
    reach = float(np.linalg.norm(tool))
    signature = [elbow[0], elbow[1], tool[0], tool[1], reach]
    return {
        "metrics": [
            {"id": "tool_x", "label": "Tool x", "value": tool[0], "unit": "m", "emphasis": "primary"},
            {"id": "tool_y", "label": "Tool y", "value": tool[1], "unit": "m"},
            {"id": "base_reach", "label": "Tool radius", "value": reach, "unit": "m"},
        ],
        "plots": {
            "response": {
                "data": [_trace("Arm configuration", [0.0, elbow[0], tool[0]], [0.0, elbow[1], tool[1]], "lines+markers")],
                "layout": _layout("Two-link arm configuration", "Base x (m)", "Base y (m)", True),
                "config": {"responsive": True, "displaylogo": False},
            },
            "mechanism": {
                "data": [_trace("Joint-2 locus", sweep_x, sweep_y), _trace("Current tool", [tool[0]], [tool[1]], "markers")],
                "layout": _layout("Relative-joint sweep", "Base x (m)", "Base y (m)", True),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "The second link inherits the first joint angle, so its world angle is q1 + q2.",
            "broken": "Broken mode treats relative q2 as an absolute world angle and breaks serial rotation composition.",
            "recovery": "Accumulate upstream joint angles before projecting each link.",
        },
        "diagnostics": {"item_id": "P03", "reference_basis": "closed-form forward kinematics", "broken_active": broken, "sample_count": len(q2_sweep), "signature": [float(v) for v in signature]},
    }

