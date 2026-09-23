from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 66
BROKEN_TEXT = (
    "Broken mode feeds degree-valued joint coordinates to radian trigonometry and bypasses "
    "timestamp/unit contract checks. Every matrix remains finite while the integrated endpoint is wrong."
)
RECOVERY_TEXT = (
    "Validate interface units and age before use, convert encoder counts once into radians, compose "
    "the declared frame chain in order, and audit the result against an independently measured tool pose."
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


def _transform(x: float, y: float, angle: float) -> np.ndarray:
    return np.array([[np.cos(angle), -np.sin(angle), x],
                     [np.sin(angle), np.cos(angle), y], [0.0, 0.0, 1.0]])


def _chain(joints: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    base_shoulder = _transform(0.20, 0.10, 0.15)
    shoulder_elbow = _transform(0.0, 0.0, joints[0]) @ _transform(0.70, 0.0, 0.0)
    elbow_tool = _transform(0.0, 0.0, joints[1]) @ _transform(0.50, 0.0, 0.0)
    elbow = base_shoulder @ shoulder_elbow @ np.array([0.0, 0.0, 1.0])
    return base_shoulder @ shoulder_elbow @ elbow_tool, elbow[:2]


def _model(parameters: dict[str, Any], broken: bool) -> dict[str, Any]:
    scale_error = 0.01 * float(parameters["encoder_scale_error_percent"])
    skew_ms = float(parameters["timestamp_skew_ms"])
    true_joints = np.array([0.55, -0.85])
    radians_per_count = 2.0 * np.pi / 4096.0
    counts = true_joints / radians_per_count
    decoded = counts * radians_per_count * (1.0 + scale_error)
    integrated_joints = np.rad2deg(decoded) if broken else decoded
    true_tool, _true_elbow = _chain(true_joints)
    integrated_tool, integrated_elbow = _chain(integrated_joints)
    endpoint_error = float(np.linalg.norm(integrated_tool[:2, 2] - true_tool[:2, 2]))
    inverse_residual = float(np.linalg.norm(integrated_tool @ np.linalg.inv(integrated_tool)
                                            - np.eye(3)))
    violations = int(abs(skew_ms) > 20.0)
    if broken:
        violations += 2
    ages = np.array([0.0, 0.5 * skew_ms, skew_ms])
    return {"signature": [endpoint_error, inverse_residual, float(violations)],
            "sample_count": len(ages),
            "metrics": [("integrated_endpoint_error", "Integrated Endpoint Error", endpoint_error, "m"),
                        ("frame_inverse_residual", "Frame Inverse Residual", inverse_residual, "1"),
                        ("interface_contract_violations", "Interface Contract Violations", violations, "count")],
            "plots": {"response": _plot("Integrated model and measured tool pose",
                "Base-frame x position (m)", "Base-frame y position (m)", [
                    _trace("Integrated chain", [0.20, integrated_elbow[0], integrated_tool[0, 2]],
                           [0.10, integrated_elbow[1], integrated_tool[1, 2]],
                           "Base-frame x position", "m", "Base-frame y position", "m"),
                    _trace("Measured tool", [true_tool[0, 2]], [true_tool[1, 2]],
                           "Base-frame x position", "m", "Base-frame y position", "m")]),
                "mechanism": _plot("Interface timestamp-age audit", "Interface stage (count)",
                "Message age (ms)", [
                    _trace("Observed age", np.arange(3), ages, "Interface stage", "count",
                           "Message age", "ms"),
                    _trace("Freshness limit", np.arange(3), np.full(3, 20.0),
                           "Interface stage", "count", "Message age", "ms")])},
            "observation": (f"The integrated tool differs from the measured pose by {endpoint_error:.4f} m "
                            f"and the interface audit reports {violations} contract violation(s).")}


def _result(model: dict[str, Any], broken: bool) -> dict[str, Any]:
    return {"metrics": [{"id": key, "label": label, "value": float(value), "unit": unit,
            "emphasis": "primary" if index == 0 else "normal"}
            for index, (key, label, value, unit) in enumerate(model["metrics"])], "plots": model["plots"],
            "explanations": {"observation": model["observation"], "broken": BROKEN_TEXT, "recovery": RECOVERY_TEXT},
            "diagnostics": {"item_number": ITEM_NUMBER, "broken_active": bool(broken),
            "sample_count": int(model["sample_count"]), "signature": [float(v) for v in model["signature"]],
            "software_only": True}}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
