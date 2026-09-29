from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 38
BROKEN_TEXT = "Broken mode reverses the observer injection L. The error subsystem then has a positive pole, and its growing error drives the physical plant through BK e."
RECOVERY_TEXT = "Restore the observer sign and reset controls. Verify both abscissae are negative and the CARE and separation residuals are near roundoff."


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


def _model(p, broken):
    from scipy.linalg import expm, solve_continuous_are

    bw = float(p["regulator_bandwidth_per_s"])
    ow = bw * float(p["observer_speed_ratio"])
    A = np.array([[0.0, 1.0], [0.0, 0.0]])
    B = np.array([[0.0], [1.0]])
    C = np.array([[1.0, 0.0]])
    Q = np.diag([bw**4, bw**2])
    P = solve_continuous_are(A, B, Q, np.ones((1, 1)))
    K = B.T @ P
    L = np.array([[3 * ow], [2 * ow**2]]) * (-1 if broken else 1)
    reg = A - B @ K
    obs = A - L @ C
    aug = np.block([[reg, B @ K], [np.zeros((2, 2)), obs]])
    rp = np.linalg.eigvals(reg)
    op = np.linalg.eigvals(obs)
    separation = np.max(
        abs(np.sort_complex(np.linalg.eigvals(aug)) - np.sort_complex(np.r_[rp, op]))
    )
    # Fixed observer-normalized horizon bounds the unstable demonstration at every control corner.
    t = np.linspace(0.0, 3 / ow, 201)
    dt = t[1]
    transition = expm(aug * dt)
    history = [np.array([1.0, 0.0, 0.1, 0.0])]
    for _ in t[1:]:
        history.append(transition @ history[-1])
    h = np.array(history)
    residual = np.max(abs(A.T @ P + P @ A - P @ B @ B.T @ P + Q))
    return {
        "signature": [max(rp.real), max(op.real), separation, residual],
        "metrics": [
            ("regulator", "LQR spectral abscissa", max(rp.real), "1/s"),
            ("observer", "Observer spectral abscissa", max(op.real), "1/s"),
            ("separation", "Separation spectrum residual", separation, "1/s"),
            ("care", "Normalized CARE residual", residual, "1"),
            ("position_gain", "Normalized LQR position gain", K[0, 0], "1"),
            ("velocity_gain", "Normalized LQR velocity gain", K[0, 1], "1"),
        ],
        "plots": {
            "response": _plot(
                "Plant and estimate",
                "Time (s)",
                "Normalized position (1)",
                [
                    _trace(
                        "True position",
                        t,
                        h[:, 0],
                        "Time",
                        "s",
                        "Normalized position",
                        "1",
                    ),
                    _trace(
                        "Estimated position",
                        t,
                        h[:, 0] - h[:, 2],
                        "Time",
                        "s",
                        "Normalized position",
                        "1",
                    ),
                ],
            ),
            "mechanism": _plot(
                "Actual observer error",
                "Time (s)",
                "Normalized state error (1)",
                [
                    _trace(
                        "Position error",
                        t,
                        h[:, 2],
                        "Time",
                        "s",
                        "Normalized error",
                        "1",
                    ),
                    _trace(
                        "Velocity error (1 s scale)",
                        t,
                        h[:, 3],
                        "Time",
                        "s",
                        "Normalized error",
                        "1",
                    ),
                ],
            ),
        },
        "details": {
            "time": t,
            "augmented_state": h,
            "augmented_matrix": aug,
            "Q": Q,
            "P": P,
            "K": K,
            "L": L,
        },
        "observation": "K comes from the stated normalized quadratic cost, not pole placement. Curves propagate the coupled plant and estimation error; the finite observer-scaled window is not a settling-time claim.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
