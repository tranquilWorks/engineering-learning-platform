from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 44
BROKEN_TEXT = "Reverse the linear damping sign in the actual cubic vector field while retaining the selected radius and cubic coefficient."
RECOVERY_TEXT = "Restore negative linear feedback and choose a strict sublevel inside the nominal equilibrium boundary."


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
        "type": "scattergl",
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
            "broken_active": bool(broken),
            "signature": [float(value) for value in model["signature"]],
            **model.get("history", {}),
        },
    }


def _model(p, broken):
    radius = float(p["sublevel_radius"])
    cubic = float(p["cubic_coefficient"])
    damping = -1.0 if broken else 1.0
    x = np.linspace(
        -max(1.4 * radius, 1.2 / np.sqrt(cubic)),
        max(1.4 * radius, 1.2 / np.sqrt(cubic)),
        241,
    )
    velocity = -damping * x + cubic * x**3
    derivative = x * velocity
    margin = damping - cubic * radius**2
    boundary = -margin * radius**2
    return {
        "signature": [margin, boundary, 1 / np.sqrt(cubic)],
        "metrics": [
            ("minimum_decay_margin", "Boundary decay margin", margin, "1/s"),
            ("boundary_vdot", "Boundary Vdot", boundary, "1/s"),
            ("roa_radius", "Nominal strict-decay radius", 1 / np.sqrt(cubic), "1"),
        ],
        "history": {
            "state": x,
            "vector_field": velocity,
            "vdot": derivative,
            "candidate_radius": radius,
            "certified": bool(margin > 0 and not broken),
        },
        "plots": {
            "response": _plot(
                "Candidate sublevel",
                "State x (1)",
                "V(x) (1)",
                [
                    _trace(
                        "V = x squared / 2", x, 0.5 * x * x, "State x", "1", "V(x)", "1"
                    ),
                    _trace(
                        "Selected sublevel",
                        x,
                        np.full_like(x, 0.5 * radius**2),
                        "State x",
                        "1",
                        "V(x)",
                        "1",
                    ),
                ],
            ),
            "mechanism": _plot(
                "Lyapunov derivative",
                "State x (1)",
                "V-dot (1/s)",
                [
                    _trace(
                        "x times x-dot", x, derivative, "State x", "1", "V-dot", "1/s"
                    ),
                    _trace(
                        "Zero derivative",
                        x,
                        np.zeros_like(x),
                        "State x",
                        "1",
                        "V-dot",
                        "1/s",
                    ),
                ],
            ),
        },
        "observation": f"The selected sublevel has boundary V-dot={boundary:.6g}/s and margin {margin:.6g}/s. Strict positivity of the margin certifies decay for all 0<|x|<=radius only in the nominal cubic model. The origin and equality boundary require separate reasoning.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
