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
    heading_deg = float(parameters["heading_deg"])
    origin = np.array([float(parameters["robot_x_m"]), float(parameters["robot_y_m"])])
    body = np.array([float(parameters["point_x_m"]), float(parameters["point_y_m"])])
    broken = bool(parameters["broken_mode"])
    theta = np.radians(heading_deg)
    c = np.cos(theta)
    s = np.sin(theta)
    rotation = np.array([[c, -s], [s, c]])
    used_rotation = rotation.T if broken else rotation
    world = origin + used_rotation @ body
    recovered_body = rotation.T @ (world - origin)
    roundtrip_error = float(np.linalg.norm(recovered_body - body))
    angles = np.radians(np.linspace(-180.0, 180.0, 361))
    sweep_x = origin[0] + body[0] * np.cos(angles) - body[1] * np.sin(angles)
    sweep_y = origin[1] + body[0] * np.sin(angles) + body[1] * np.cos(angles)
    signature = [world[0], world[1], recovered_body[0], recovered_body[1], roundtrip_error]
    return {
        "metrics": [
            {"id": "world_x", "label": "World point x", "value": world[0], "unit": "m", "emphasis": "primary"},
            {"id": "world_y", "label": "World point y", "value": world[1], "unit": "m"},
            {"id": "roundtrip_error", "label": "Round-trip error", "value": roundtrip_error, "unit": "m"},
        ],
        "plots": {
            "response": {
                "data": [_trace("Robot to transformed point", [origin[0], world[0]], [origin[1], world[1]], "lines+markers"), _trace("Heading sweep", sweep_x, sweep_y)],
                "layout": _layout("Body point expressed in world frame", "World x (m)", "World y (m)", True),
                "config": {"responsive": True, "displaylogo": False},
            },
            "mechanism": {
                "data": [_trace("Original body point", [0.0, body[0]], [0.0, body[1]], "lines+markers"), _trace("Inverse-recovered body point", [0.0, recovered_body[0]], [0.0, recovered_body[1]], "lines+markers")],
                "layout": _layout("Forward/inverse consistency", "Body x (m)", "Body y (m)", True),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "Rotate the body-frame vector, then add the robot origin in world coordinates.",
            "broken": "Broken mode reverses the forward rotation sign while retaining the declared inverse, so the round trip fails.",
            "recovery": "Use one positive-counterclockwise rotation convention in both forward and inverse transforms.",
        },
        "diagnostics": {"item_id": "P02", "reference_basis": "SE(2) matrix invariant", "broken_active": broken, "sample_count": len(angles), "signature": [float(v) for v in signature]},
    }

