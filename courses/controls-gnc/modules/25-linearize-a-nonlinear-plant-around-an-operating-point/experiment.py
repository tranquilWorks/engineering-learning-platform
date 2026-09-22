from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 25
BROKEN_TEXT = 'Broken mode omits the equilibrium torque, so the supposedly linearized origin accelerates before any perturbation is applied.'
RECOVERY_TEXT = 'Restore the balancing torque, recompute the Jacobian at the same angle, and shrink the perturbation until the nonlinear and tangent torques agree.'


def _trace(name: str, x: Any, y: Any, x_quantity: str, x_unit: str,
           y_quantity: str, y_unit: str, *, mode: str = "lines") -> dict[str, Any]:
    return {
        "type": "scattergl", "mode": mode, "name": name,
        "x": np.asarray(x, dtype=float), "y": np.asarray(y, dtype=float),
        "meta": {"x_quantity": x_quantity, "x_unit": x_unit,
                 "y_quantity": y_quantity, "y_unit": y_unit},
    }


def _plot(title: str, x_title: str, y_title: str,
          traces: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "data": traces,
        "layout": {
            "title": {"text": title, "x": 0.02},
            "xaxis": {"title": {"text": x_title}},
            "yaxis": {"title": {"text": y_title}},
            "legend": {"orientation": "h"},
            "margin": {"l": 72, "r": 36, "t": 62, "b": 62},
            "hovermode": "closest", "uirevision": "keep-view",
        },
        "config": {"responsive": True, "displaylogo": False},
    }


def _result(model: dict[str, Any], broken: bool) -> dict[str, Any]:
    return {
        "metrics": [
            {"id": key, "label": label, "value": float(value), "unit": unit,
              "emphasis": "primary" if index == 0 else "normal"}
            for index, (key, label, value, unit) in enumerate(model["metrics"])
        ],
        "plots": model["plots"],
        "explanations": {
            "observation": model["observation"],
            "broken": BROKEN_TEXT,
            "recovery": RECOVERY_TEXT,
        },
        "diagnostics": {
            "item_number": ITEM_NUMBER,
            "broken_active": bool(broken),
            "signature": [float(value) for value in model["signature"]],
        },
    }

def _model(p: dict[str, Any], broken: bool) -> dict[str, Any]:
    theta0 = float(p["operating_angle_rad"])
    radius = float(p["perturbation_rad"])
    mass, gravity, length = 2.0, 9.81, 0.7
    angles = theta0 + np.linspace(-radius, radius, 161)
    exact = mass * gravity * length * np.sin(angles)
    tangent = mass * gravity * length * (np.sin(theta0) + np.cos(theta0) * (angles - theta0))
    balance = 0.0 if broken else mass * gravity * length * np.sin(theta0)
    residual = mass * gravity * length * np.sin(theta0) - balance
    acceleration = -(gravity / length) * (np.sin(angles) - balance / (mass * gravity * length))
    local_acceleration = -(gravity / length) * np.cos(theta0) * (angles - theta0)
    error = float(np.max(np.abs(exact - tangent)))
    a21 = -(gravity / length) * np.cos(theta0)
    return {
        "signature": [abs(residual), error, a21],
        "metrics": [("residual", "Operating-point residual", abs(residual), "N*m"),
                    ("local_error", "Maximum Taylor torque error", error, "N*m"),
                    ("jacobian", "Local angular stiffness A21", a21, "1/s^2")],
        "plots": {
            "response": _plot("Nonlinear gravity torque and first-order tangent", "Pendulum angle (rad)", "Gravity torque (N*m)", [
                _trace("Nonlinear torque", angles, exact, "Pendulum angle", "rad", "Gravity torque", "N*m"),
                _trace("Tangent model", angles, tangent, "Pendulum angle", "rad", "Gravity torque", "N*m")]),
            "mechanism": _plot("Local angular acceleration about the operating point", "Angle perturbation (rad)", "Angular acceleration (rad/s^2)", [
                _trace("Nonlinear acceleration", angles-theta0, acceleration, "Angle perturbation", "rad", "Angular acceleration", "rad/s^2"),
                _trace("Jacobian prediction", angles-theta0, local_acceleration, "Angle perturbation", "rad", "Angular acceleration", "rad/s^2")]),
        },
        "observation": "Residual diagnoses whether the nominal state is an equilibrium; the curvature gap diagnoses whether the Jacobian is local enough."
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
