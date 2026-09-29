from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 43
BROKEN_TEXT = "Broken mode negates the selected damping, retaining the selected initial energy. Energy is supplied at +|c|v² rather than dissipated; the growing trajectory is integrated rather than replaced by an exponential sinusoid."
RECOVERY_TEXT = "Restore positive damping and reset both controls. Check energy does not increase and the energy-work residual is small relative to the energy scale."


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

    c = float(p["damping_per_s"]) * (-1 if broken else 1)
    E0 = float(p["initial_energy"])

    def rhs(t, s):
        x, v, _work = s
        return [v, x - x**3 - c * v, -c * v * v]

    t = np.linspace(0.0, 6.0, 401)
    sol = solve_ivp(
        rhs,
        [0.0, 6.0],
        [0.0, np.sqrt(2 * E0), 0.0],
        t_eval=t,
        method="DOP853",
        rtol=2e-12,
        atol=2e-13,
    )
    if not sol.success:
        raise ValueError(sol.message)
    x, v, work = sol.y
    energy = 0.5 * v * v - 0.5 * x * x + 0.25 * x**4
    local = max(np.roots([1.0, c, 2.0]).real)
    distance = min(abs(x[-1] - 1), abs(x[-1] + 1))
    return {
        "signature": [(energy[-1] - energy[0]) / 6, distance, local],
        "metrics": [
            (
                "power",
                "Mean dissipated/supplied power",
                (energy[-1] - energy[0]) / 6,
                "W",
            ),
            ("well", "Final distance to nearest well", distance, "m"),
            ("local", "Well linearization abscissa", local, "1/s"),
            ("balance", "Energy-work residual", max(abs(energy - E0 - work)), "J"),
        ],
        "plots": {
            "response": _plot(
                "Double-well phase portrait",
                "Position (m)",
                "Velocity (m/s)",
                [
                    _trace(
                        "Integrated trajectory",
                        x,
                        v,
                        "Position",
                        "m",
                        "Velocity",
                        "m/s",
                    ),
                    _trace(
                        "Equilibria",
                        [-1, 0, 1],
                        [0, 0, 0],
                        "Position",
                        "m",
                        "Velocity",
                        "m/s",
                        mode="markers",
                    ),
                ],
            ),
            "mechanism": _plot(
                "Mechanical energy balance",
                "Time (s)",
                "Energy (J)",
                [
                    _trace("Mechanical energy", t, energy, "Time", "s", "Energy", "J"),
                    _trace(
                        "Initial energy plus work",
                        t,
                        E0 + work,
                        "Time",
                        "s",
                        "Energy",
                        "J",
                    ),
                ],
            ),
        },
        "details": {
            "time": t,
            "position": x,
            "velocity": v,
            "energy": energy,
            "damping_work": work,
            "damping": c,
        },
        "observation": "This is an integrated double-well trajectory. The origin is a saddle; local decay about either well is not a global guarantee of convergence to that particular well. Negative damping supplies energy.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
