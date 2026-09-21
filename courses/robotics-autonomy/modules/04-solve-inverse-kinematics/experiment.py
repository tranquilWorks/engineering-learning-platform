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
    target = np.array([float(parameters["target_x_m"]), float(parameters["target_y_m"])])
    link1 = float(parameters["link1_m"])
    link2 = float(parameters["link2_m"])
    elbow_up = bool(parameters["elbow_up"])
    broken = bool(parameters["broken_mode"])
    radius_sq = float(target @ target)
    raw_c2 = (radius_sq - link1**2 - link2**2) / (2.0 * link1 * link2)
    reachable = abs(raw_c2) <= 1.0
    c2 = float(np.clip(raw_c2, -1.0, 1.0))
    s2_mag = float(np.sqrt(max(0.0, 1.0 - c2**2)))
    s2 = -s2_mag if elbow_up else s2_mag
    q2 = float(np.arctan2(s2, c2))
    bearing = float(np.arctan2(target[1], target[0]))
    correction = float(np.arctan2(link2 * s2, link1 + link2 * c2))
    q1 = bearing if broken else bearing - correction
    elbow = link1 * np.array([np.cos(q1), np.sin(q1)])
    tool = elbow + link2 * np.array([np.cos(q1 + q2), np.sin(q1 + q2)])
    residual = float(np.linalg.norm(tool - target))
    theta = np.linspace(0.0, 2.0 * np.pi, 361)
    outer_x = (link1 + link2) * np.cos(theta)
    outer_y = (link1 + link2) * np.sin(theta)
    inner = abs(link1 - link2)
    inner_x = inner * np.cos(theta)
    inner_y = inner * np.sin(theta)
    signature = [np.degrees(q1), np.degrees(q2), tool[0], tool[1], residual, float(reachable)]
    return {
        "metrics": [
            {"id": "shoulder_angle", "label": "Shoulder angle", "value": np.degrees(q1), "unit": "deg", "emphasis": "primary"},
            {"id": "elbow_angle", "label": "Elbow angle", "value": np.degrees(q2), "unit": "deg"},
            {"id": "target_residual", "label": "Target residual", "value": residual, "unit": "m", "emphasis": "warning" if residual > 1e-6 else "normal"},
            {"id": "reachable", "label": "Reachable", "value": "yes" if reachable else "no", "unit": "state"},
        ],
        "plots": {
            "response": {
                "data": [_trace("Solved arm", [0.0, elbow[0], tool[0]], [0.0, elbow[1], tool[1]], "lines+markers"), _trace("Requested target", [target[0]], [target[1]], "markers")],
                "layout": _layout("Inverse-kinematics solution", "Base x (m)", "Base y (m)", True),
                "config": {"responsive": True, "displaylogo": False},
            },
            "mechanism": {
                "data": [_trace("Outer reach", outer_x, outer_y), _trace("Inner reach", inner_x, inner_y), _trace("Target", [target[0]], [target[1]], "markers")],
                "layout": _layout("Reachable annulus", "Base x (m)", "Base y (m)", True),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "The law of cosines chooses an elbow branch; the shoulder correction closes the link triangle.",
            "broken": "Broken mode omits the shoulder correction, so forward kinematics misses a reachable target.",
            "recovery": "Restore the triangle correction and verify the solution with a forward-kinematics round trip.",
        },
        "diagnostics": {"item_id": "P04", "reference_basis": "law of cosines plus FK invariant", "broken_active": broken, "sample_count": len(theta), "signature": [float(v) for v in signature]},
    }

