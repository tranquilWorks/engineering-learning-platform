from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 49
BROKEN_TEXT = "Broken mode solves the same horizon objective without bounds and applies that unconstrained move. Constraint violation is measured from applied inputs; at sufficiently large limits this fault need not cause a violation."
RECOVERY_TEXT = "Reenable optimization bounds and reset the controls. Check every applied move against the limits and require a near-zero box KKT residual, not merely a clipped-looking first command."


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


def _result(model: dict[str, Any], broken: bool) -> dict[str, Any]:
    return {
        "metrics": [
            {
                "id": key,
                "label": label,
                "value": float(value),
                "unit": unit,
                "emphasis": "primary" if index == 0 else "normal",
            }
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
            **model.get("details", {}),
            "broken_active": bool(broken),
            "signature": [float(value) for value in model["signature"]],
        },
    }


def solve_plan(state, horizon, limit, broken=False):
    from scipy.optimize import lsq_linear

    G = np.tril(np.ones((horizon, horizon)))
    D = np.vstack([G, np.sqrt(0.1) * np.eye(horizon)])
    target = np.r_[-state * np.ones(horizon), np.zeros(horizon)]
    if broken:
        inputs = np.linalg.lstsq(D, target, rcond=None)[0]
    else:
        fit = lsq_linear(
            D, target, bounds=(-limit, limit), method="bvls", tol=1e-12, max_iter=100
        )
        if not fit.success:
            raise ValueError("Constrained plan did not converge")
        inputs = fit.x
    states = state + G @ inputs
    gradient = 2 * (G.T @ states + 0.1 * inputs)
    # Projected-gradient KKT residual uses the declared feasible box even in fault mode.
    residual = max(abs(inputs - np.clip(inputs - gradient, -limit, limit)))
    return (
        inputs,
        states,
        float(states @ states + 0.1 * (inputs @ inputs)),
        float(residual),
    )


def _model(p, broken):
    horizon = int(p["prediction_horizon"])
    limit = float(p["input_limit"])
    states = [1.5]
    inputs = []
    costs = []
    residuals = []
    first, prediction, initial_cost, initial_kkt = solve_plan(
        states[0], horizon, limit, broken
    )
    for _ in range(16):
        plan, _predicted, cost, residual = solve_plan(states[-1], horizon, limit, broken)
        inputs.append(plan[0])
        states.append(states[-1] + plan[0])
        costs.append(cost)
        residuals.append(residual)
    violation = max(0.0, max(abs(np.array(inputs))) - limit)
    return {
        "signature": [first[0], violation, abs(prediction[-1])],
        "metrics": [
            ("first", "First optimized move", first[0], "1"),
            ("violation", "Applied constraint violation", violation, "1"),
            ("terminal", "First-plan terminal error", abs(prediction[-1]), "1"),
            ("objective", "First-plan quadratic objective", initial_cost, "1"),
            ("kkt", "First-plan box KKT residual", initial_kkt, "1"),
        ],
        "plots": {
            "response": _plot(
                "Prediction and receding horizon",
                "Sample index (1)",
                "Normalized state (1)",
                [
                    _trace(
                        "Executed state",
                        np.arange(17),
                        states,
                        "Sample index",
                        "1",
                        "Normalized state",
                        "1",
                    ),
                    _trace(
                        "Initial optimized prediction",
                        np.arange(horizon + 1),
                        np.r_[1.5, prediction],
                        "Sample index",
                        "1",
                        "Normalized state",
                        "1",
                    ),
                ],
            ),
            "mechanism": _plot(
                "Executed control moves",
                "Sample index (1)",
                "Normalized input (1)",
                [
                    _trace(
                        "Applied input",
                        np.arange(16),
                        inputs,
                        "Sample index",
                        "1",
                        "Normalized input",
                        "1",
                    ),
                    _trace(
                        "Upper limit",
                        np.arange(16),
                        np.full(16, limit),
                        "Sample index",
                        "1",
                        "Normalized input",
                        "1",
                    ),
                    _trace(
                        "Lower limit",
                        np.arange(16),
                        np.full(16, -limit),
                        "Sample index",
                        "1",
                        "Normalized input",
                        "1",
                    ),
                ],
            ),
        },
        "details": {
            "state": states,
            "input": inputs,
            "first_plan": first,
            "first_prediction": prediction,
            "costs": costs,
            "kkt_residuals": residuals,
        },
        "observation": "Each displayed move is the first input of a newly solved finite-horizon quadratic problem. The fault removes optimization bounds and exposes measured violations. A feasible input does not by itself prove model robustness or recursive feasibility for other plants.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
