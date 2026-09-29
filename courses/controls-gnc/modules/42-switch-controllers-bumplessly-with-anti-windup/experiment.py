from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 42
BROKEN_TEXT = "Broken mode starts z at zero on switching and disables back-calculation. It still obeys actuator limits, so the integrator can accumulate error that the actuator cannot realize."
RECOVERY_TEXT = "Disable broken mode, restore gain 4/s and limit 1.2, and verify a zero applied bump plus the actual integral history. Check the recovery-observed indicator before quoting a settling time."


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
    dt = 0.01
    t = np.arange(1201) * dt
    limit = float(p["actuator_limit"])
    kaw = 0.0 if broken else float(p["antiwindup_gain_per_s"])
    manual = min(0.7, limit)
    x = np.zeros(len(t))
    z = np.zeros(len(t))
    u = np.zeros(len(t))
    raw = np.zeros(len(t))
    ref = np.where(t < 7.0, 2.0, 0.2)
    for j in range(len(t)):
        e = ref[j] - x[j]
        if j == 300:
            z[j] = 0.0 if broken else manual - 2 * e
        raw[j] = manual if j < 300 else 2 * e + z[j]
        u[j] = np.clip(raw[j], -limit, limit)
        if j < len(t) - 1:
            x[j + 1] = x[j] + dt * (-x[j] + u[j])
            z[j + 1] = (
                z[j] if j < 300 else z[j] + dt * (1.2 * e + kaw * (u[j] - raw[j]))
            )
    # A recovery must stay inside the band for the remainder of the observation window.
    outside = np.flatnonzero(abs(x[700:] - 0.2) > 0.04)
    start = 700 if len(outside) == 0 else 701 + int(outside[-1])
    observed = start < len(t)
    recovery = float(t[start] - 7) if observed else 5.0
    bump = abs(u[300] - u[299])
    peak = max(abs(z))
    return {
        "signature": [bump, recovery, peak, float(observed)],
        "metrics": [
            ("bump", "Applied switch bump", bump, "1"),
            (
                "recovery",
                "Recovery time" if observed else "Recovery lower bound (censored)",
                recovery,
                "s",
            ),
            ("integrator", "Peak absolute integral state", peak, "1"),
            ("observed", "Recovery observed", observed, "1"),
        ],
        "plots": {
            "response": _plot(
                "Switch and reference drop",
                "Time (s)",
                "Normalized output (1)",
                [
                    _trace("Plant output", t, x, "Time", "s", "Normalized output", "1"),
                    _trace("Reference", t, ref, "Time", "s", "Normalized output", "1"),
                ],
            ),
            "mechanism": _plot(
                "Integrator and actuator",
                "Time (s)",
                "Normalized command (1)",
                [
                    _trace(
                        "Integral state", t, z, "Time", "s", "Normalized command", "1"
                    ),
                    _trace(
                        "Requested command",
                        t,
                        raw,
                        "Time",
                        "s",
                        "Normalized command",
                        "1",
                    ),
                    _trace(
                        "Applied command", t, u, "Time", "s", "Normalized command", "1"
                    ),
                ],
            ),
        },
        "details": {
            "time": t,
            "state": x,
            "integral": z,
            "requested": raw,
            "applied": u,
            "reference": ref,
            "recovery_observed": observed,
        },
        "observation": "The same integral-state history defines the peak in both modes. Manual and automatic commands obey the selected limit. A censored recovery is a lower bound, not successful settling.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
