from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 47
BROKEN_TEXT = "Broken mode adds the estimated drift instead of subtracting it, so delta=2−mismatch. It retains both selected controls. At the default gain it decays slowly; at lower gain it can reach the departure threshold."
RECOVERY_TEXT = "Restore the cancellation sign and default controls. Verify the observed duration returns to four seconds and terminal error decreases. Do not interpret a stopped trajectory as a clipped stable plant."


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
    from scipy.integrate import solve_ivp

    mismatch = float(p["model_mismatch"])
    k = float(p["tracking_gain_per_s"])
    chat = 1 - mismatch
    cancellation = chat if broken else -chat
    delta = 1 + cancellation

    def rhs(t, x):
        return delta * x * x - k * x

    def escape(t, x):
        return x[0] - 10.0

    escape.terminal = True
    escape.direction = 1
    sol = solve_ivp(
        rhs,
        [0.0, 4.0],
        [1.0],
        events=escape,
        dense_output=True,
        rtol=2e-12,
        atol=2e-13,
        method="DOP853",
    )
    if not sol.success:
        raise ValueError(sol.message)
    end = sol.t[-1]
    t = np.linspace(0.0, end, 241)
    x = sol.sol(t)[0]
    u = cancellation * x * x - k * x
    escaped = bool(len(sol.t_events[0]))
    return {
        "signature": [delta, delta - k, abs(x[-1])],
        "metrics": [
            ("drift", "Initial uncancelled drift", delta, "1/s"),
            ("rate", "Initial error rate", delta - k, "1/s"),
            ("terminal", "Observed terminal error", abs(x[-1]), "1"),
            ("horizon", "Observed duration", end, "s"),
            ("escape", "Departure threshold reached", escaped, "1"),
        ],
        "plots": {
            "response": _plot(
                "Nonlinear cancellation dynamics",
                "Time (s)",
                "Normalized state (1)",
                [
                    _trace("Actual state", t, x, "Time", "s", "Normalized state", "1"),
                    _trace(
                        "Exact-cancellation comparison",
                        t,
                        np.exp(-k * t),
                        "Time",
                        "s",
                        "Normalized state",
                        "1",
                    ),
                ],
            ),
            "mechanism": _plot(
                "Cancellation and applied input",
                "Time (s)",
                "Normalized state rate (1/s)",
                [
                    _trace(
                        "Applied input",
                        t,
                        u,
                        "Time",
                        "s",
                        "Normalized state rate",
                        "1/s",
                    ),
                    _trace(
                        "Plant drift",
                        t,
                        x * x,
                        "Time",
                        "s",
                        "Normalized state rate",
                        "1/s",
                    ),
                ],
            ),
        },
        "details": {
            "time": t,
            "state": x,
            "input": u,
            "residual_coefficient": delta,
            "escape_observed": escaped,
        },
        "observation": (
            "Trajectory terminated at x=10; its last error is a departure event, not a four-second tracking score."
            if escaped
            else "The actual nonlinear trajectory reaches the four-second horizon. Cancellation mismatch remains state dependent; a decaying nominal linear law alone cannot establish nonlinear stability."
        ),
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
