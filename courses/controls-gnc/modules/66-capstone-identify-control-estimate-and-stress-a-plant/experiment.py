from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 66
BROKEN_TEXT = "Broken mode reuses a stale nominal model and underreports estimator covariance under the same uncertainty/noise stress."
RECOVERY_TEXT = "Re-identify, redesign, and rerun the exact stress family; do not waive a failed upstream requirement."


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


def _requirement(quantity, value, unit, operator, threshold):
    value = float(value)
    passed = (
        value <= threshold + 1e-10 if operator == "<=" else value >= threshold - 1e-10
    )
    return {
        "quantity": quantity,
        "value": value,
        "unit": unit,
        "operator": operator,
        "threshold": threshold,
        "passed": bool(passed),
    }


def _result(model, broken):
    requirements = model["requirements"]
    columns = ["Requirement", "Quantity", "Value", "Unit", "Rule", "Verdict"]
    rows = [
        {
            "Requirement": key,
            "Quantity": r["quantity"],
            "Value": round(r["value"], 7),
            "Unit": r["unit"],
            "Rule": f"{r['operator']} {r['threshold']}",
            "Verdict": "pass" if r["passed"] else "fail",
        }
        for key, r in requirements.items()
    ]
    return {
        "metrics": [
            {"id": key, "label": label, "value": float(value), "unit": unit}
            for key, label, value, unit in model["metrics"]
        ],
        "plots": model["plots"],
        "tables": {"requirements": {"columns": columns, "rows": rows}},
        "explanations": {
            "observation": model["observation"],
            "broken": BROKEN_TEXT,
            "recovery": RECOVERY_TEXT,
        },
        "diagnostics": {
            "item_number": ITEM_NUMBER,
            "broken_active": broken,
            "signature": model["signature"],
            "requirements": requirements,
            **model["history"],
        },
    }


def _simulate(uncertainty, noise, broken):
    dt = 0.02
    a0, b0 = np.exp(-dt), -np.expm1(-dt)
    drive = (
        np.ones(400)
        if broken
        else np.sin(np.arange(400) * 0.17) + 0.6 * np.cos(np.arange(400) * 0.071)
    )
    states = [1.0 if broken else 0.0]
    for u in drive:
        states.append(a0 * states[-1] + b0 * u)
    matrix = np.column_stack((states[:-1], drive))
    rank = int(np.linalg.matrix_rank(matrix))
    identified = np.linalg.lstsq(matrix, states[1:], rcond=None)[0]
    # A rank-deficient calibration cannot identify two coefficients. This explicit
    # stale fallback is operationally runnable but does not pass identification.
    ah, bh = (np.exp(-0.4 * dt), -np.expm1(-0.4 * dt) * 0.5) if rank < 2 else identified
    gain = (ah - np.exp(-2 * dt)) / bh
    prefilter = (1 - ah + bh * gain) / bh
    histories = []
    for stress in (-uncertainty, 0.0, uncertainty):
        aa = np.exp(-(1 + stress) * dt)
        bb = (1 - stress / 2) / (1 + stress) * (1 - aa)
        state = estimate = 0.0
        covariance = 0.1
        rows = []
        for k in range(600):
            command = float(np.clip(prefilter - gain * estimate, -3, 3))
            state = aa * state + bb * command
            measured = state + noise * (np.sin(0.73 * k) + np.cos(1.17 * k))
            prior = ah * estimate + bh * command
            predicted_cov = ah * ah * covariance + (
                1e-7 if broken else 1e-5 + (0.1 * uncertainty) ** 2
            )
            variance = max(noise * noise * (0.01 if broken else 1), 1e-12)
            kalman_gain = predicted_cov / (predicted_cov + variance)
            estimate = prior + kalman_gain * (measured - prior)
            covariance = (1 - kalman_gain) * predicted_cov
            nees = (state - estimate) ** 2 / max(covariance, 1e-15)
            rows.append([state, estimate, covariance, command, nees])
        histories.append(rows)
    return rank, [float(ah), float(bh)], np.asarray(histories)


def _model(p, broken):
    rank, identified, h = _simulate(
        float(p["plant_uncertainty"]), float(p["measurement_noise"]), broken
    )
    tracking = float(np.max(np.sqrt(np.mean((h[:, 300:, 0] - 1) ** 2, axis=1))))
    nees = np.mean(h[:, 300:, 4], axis=1)
    effort = float(np.max(np.abs(h[:, :, 3])))
    req = {
        "ID-1": _requirement("Calibration regressor rank", rank, "count", ">=", 2),
        "CTRL-1": _requirement("Worst settled tracking RMS", tracking, "1", "<=", 0.35),
        "ACT-1": _requirement("Peak applied command", effort, "1", "<=", 3),
        "EST-1": _requirement(
            "Maximum mean normalized estimation error", max(nees), "1", "<=", 6
        ),
    }
    sig = [tracking, float(max(nees)), float(all(r["passed"] for r in req.values()))]
    t = 0.02 * np.arange(1, 601)
    return {
        "signature": sig,
        "requirements": req,
        "metrics": [
            ("worst_tracking_error", "Worst settled tracking RMS", sig[0], "1"),
            ("maximum_nees", "Maximum mean NEES", sig[1], "1"),
            ("requirements_passed", "Requirements passed", sig[2], "bool"),
        ],
        "plots": {
            "response": _plot(
                "Executed closed-loop stress trajectories",
                "Time (s)",
                "Plant state (1)",
                [
                    _trace(
                        f"Stress {i - 1}",
                        t,
                        h[i, :, 0],
                        "Time",
                        "s",
                        "Plant state",
                        "1",
                    )
                    for i in range(3)
                ]
                + [_trace("Target", t, np.ones(600), "Time", "s", "Plant state", "1")],
            ),
            "mechanism": _plot(
                "Estimator error measured over the settled record",
                "Stress case (count)",
                "Mean NEES (1)",
                [
                    _trace(
                        "Mean NEES",
                        [-1, 0, 1],
                        nees,
                        "Stress case",
                        "count",
                        "Mean NEES",
                        "1",
                    ),
                    _trace(
                        "Requirement",
                        [-1, 0, 1],
                        [6] * 3,
                        "Stress case",
                        "count",
                        "Mean NEES",
                        "1",
                    ),
                ],
            ),
        },
        "history": {
            "identified_coefficients": identified,
            "calibration_rank": rank,
            "state_estimate_covariance_command_nees": h.tolist(),
            "dt_s": 0.02,
        },
        "observation": "Identification, feedback, scalar filtering and three stressed plants execute in sequence. Rank and measured state/estimator errors determine the verdict. NEES is a diagnostic for deterministic noise, not a coverage certificate.",
    }


def run(parameters):
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
