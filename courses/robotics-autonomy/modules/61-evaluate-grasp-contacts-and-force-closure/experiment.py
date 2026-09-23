from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 61
BROKEN_TEXT = (
    "Broken mode reverses the second contact normal. The resulting wrench generators can no "
    "longer form a positive self-equilibrating combination, so rank alone is not force closure."
)
RECOVERY_TEXT = (
    "Restore inward-facing normals, construct both friction-cone edge wrenches in one object "
    "frame, and require a strictly positive null-space equilibrium before testing external loads."
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


def _grasp_matrix(friction: float, misalignment_deg: float,
                  broken: bool) -> tuple[np.ndarray, np.ndarray]:
    radius = 0.06
    angles = (np.pi, np.deg2rad(misalignment_deg))
    contacts: list[np.ndarray] = []
    columns: list[np.ndarray] = []
    for index, angle in enumerate(angles):
        position = radius * np.array([np.cos(angle), np.sin(angle)])
        normal = -position / radius
        if broken and index == 1:
            normal = -normal
        tangent = np.array([-normal[1], normal[0]])
        contacts.append(position)
        for sign in (-1.0, 1.0):
            force = normal + sign * friction * tangent
            moment = position[0] * force[1] - position[1] * force[0]
            columns.append(np.array([force[0], force[1], moment / radius]))
    return np.column_stack(columns), np.asarray(contacts)


def _closure_margin(matrix: np.ndarray) -> tuple[float, int]:
    _, singular, right = np.linalg.svd(matrix)
    rank = int(np.sum(singular > singular[0] * 1.0e-10))
    candidate = right[-1]
    if np.min(-candidate) > np.min(candidate):
        candidate = -candidate
    if abs(float(np.sum(candidate))) < 1.0e-12:
        return -float(np.linalg.norm(matrix @ candidate)), rank
    weights = candidate / float(np.sum(candidate))
    equilibrium = float(np.linalg.norm(matrix @ weights))
    if rank == 3 and np.min(weights) > 1.0e-9 and equilibrium < 1.0e-8:
        return float(np.min(weights)), rank
    return -max(equilibrium, float(max(-np.min(weights), 0.0))), rank


def _nonnegative_load(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    target = np.array([0.0, 7.5, -2.0])
    coefficients = np.zeros(matrix.shape[1])
    step = 0.8 / max(float(np.linalg.norm(matrix, 2) ** 2), 1.0e-9)
    history = []
    for _ in range(240):
        residual = matrix @ coefficients - target
        history.append(float(np.linalg.norm(residual)))
        coefficients = np.maximum(coefficients - step * matrix.T @ residual, 0.0)
    history.append(float(np.linalg.norm(matrix @ coefficients - target)))
    return coefficients, np.asarray(history)


def _model(parameters: dict[str, Any], broken: bool) -> dict[str, Any]:
    friction = float(parameters["friction_coefficient"])
    misalignment = float(parameters["contact_misalignment_deg"])
    matrix, contacts = _grasp_matrix(friction, misalignment, broken)
    margin, rank = _closure_margin(matrix)
    coefficients, residual_history = _nonnegative_load(matrix)
    residual = float(residual_history[-1])
    effort = float(np.sum(coefficients))
    signature = [margin, residual, effort]
    return {"signature": signature, "sample_count": len(residual_history),
            "metrics": [("force_closure_margin", "Force-Closure Margin", margin, "1"),
                        ("equivalent_load_residual", "Equivalent Load Residual", residual, "N"),
                        ("contact_normal_effort", "Contact Normal Effort", effort, "N")],
            "plots": {"response": _plot("Planar friction-cone force generators",
                "Object-frame force x (N)", "Object-frame force y (N)",
                [_trace(f"Cone edge {index + 1}", [0.0, matrix[0, index], 0.0],
                        [0.0, matrix[1, index], 0.0],
                        "Object-frame force x", "N", "Object-frame force y", "N")
                 for index in range(4)]),
                "mechanism": _plot("Projected nonnegative load solve", "Projected-gradient iteration (count)",
                "Equivalent wrench residual (N)", [
                    _trace("Residual", np.arange(len(residual_history)), residual_history,
                           "Projected-gradient iteration", "count", "Equivalent wrench residual", "N")])},
            "observation": (f"The grasp matrix has rank {rank}; its signed positive-equilibrium margin is "
                            f"{margin:.4f}. The contacts are separated by "
                            f"{np.linalg.norm(contacts[1] - contacts[0]):.3f} m.")}


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
