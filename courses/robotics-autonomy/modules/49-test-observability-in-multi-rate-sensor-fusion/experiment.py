from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 49
BROKEN_TEXT = (
    "Broken mode removes commanded excitation, so repeated high-rate inertial "
    "samples cannot distinguish accelerometer scale from the unexcited model."
)
RECOVERY_TEXT = (
    "Restore a persistently exciting command and preserve the real fast/slow "
    "timestamps; then recheck rank, the smallest information mode, and covariance."
)


def _trace(
    name: str,
    x: Any,
    y: Any,
    x_quantity: str,
    x_unit: str,
    y_quantity: str,
    y_unit: str,
) -> dict[str, Any]:
    return {
        "type": "scattergl",
        "mode": "lines",
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
    title: str,
    x_title: str,
    y_title: str,
    traces: list[dict[str, Any]],
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


def _information_rows(
    rate_ratio: float, excitation: float, broken: bool
) -> tuple[np.ndarray, np.ndarray]:
    duration_s = 6.0
    omega_rad_s = 2.0 * np.pi * 0.35
    effective_excitation = 0.0 if broken else excitation
    fast_times = np.linspace(0.0, duration_s, round(duration_s * rate_ratio) + 1)
    slow_times = np.arange(0.0, duration_s + 0.5, 1.0)

    rows: list[tuple[float, np.ndarray]] = []
    for time_s in fast_times:
        command = effective_excitation * (
            np.sin(omega_rad_s * time_s) + 0.35 * np.cos(0.5 * omega_rad_s * time_s)
        )
        # Fast accelerometer: a_m = scale * u + bias.
        rows.append((time_s, np.array([0.0, 0.0, command / 0.04, 1.0 / 0.04])))
    for time_s in slow_times:
        # Double integral of the commanded acceleration, with zero initial integral.
        integral = effective_excitation * (
            time_s / omega_rad_s
            - np.sin(omega_rad_s * time_s) / omega_rad_s**2
            + 0.35
            * 4.0
            * (1.0 - np.cos(0.5 * omega_rad_s * time_s))
            / omega_rad_s**2
        )
        # Slow position fix: p = p0 + v0*t + scale*int(int(u)) + .5*bias*t^2.
        rows.append(
            (
                time_s,
                np.array([1.0, time_s, integral, 0.5 * time_s**2]) / 0.08,
            )
        )
    rows.sort(key=lambda item: (item[0], 0 if item[1][0] else 1))
    return (
        np.asarray([item[0] for item in rows], dtype=float),
        np.vstack([item[1] for item in rows]),
    )


def _information_signature(rows: np.ndarray) -> tuple[float, float, float]:
    information = rows.T @ rows
    singular = np.linalg.svd(information, compute_uv=False)
    tolerance = singular[0] * 1.0e-9
    rank = int(np.sum(singular > tolerance))
    if rank < information.shape[0]:
        return float(rank), 1.0e12, 1.0e6
    condition = float(singular[0] / singular[-1])
    normalized_variance = float(np.trace(np.linalg.inv(information)))
    return float(rank), condition, normalized_variance


def _model(parameters: dict[str, Any], broken: bool) -> dict[str, Any]:
    rate_ratio = float(parameters["rate_ratio"])
    excitation = float(parameters["excitation_level"])
    times, rows = _information_rows(rate_ratio, excitation, broken)
    signature = list(_information_signature(rows))

    ranks: list[float] = []
    minimum_modes: list[float] = []
    information = np.zeros((4, 4), dtype=float)
    for row in rows:
        information += np.outer(row, row)
        singular = np.linalg.svd(information, compute_uv=False)
        ranks.append(float(np.sum(singular > max(singular[0], 1.0) * 1.0e-9)))
        minimum_modes.append(float(singular[-1]))

    return {
        "signature": signature,
        "sample_count": len(times),
        "metrics": [
            ("observability_rank", "Observable State Rank", signature[0], "count"),
            ("gramian_condition", "Information Condition Number", signature[1], "1"),
            ("state_variance", "Normalized Posterior Variance", signature[2], "1"),
        ],
        "plots": {
            "response": _plot(
                "Rank gained as asynchronous measurements arrive",
                "Elapsed time (s)",
                "Observable rank (count)",
                [
                    _trace("Cumulative rank", times, ranks, "Elapsed time", "s", "Observable rank", "count"),
                    _trace("Four-state target", times, np.full_like(times, 4.0), "Elapsed time", "s", "Observable rank", "count"),
                ],
            ),
            "mechanism": _plot(
                "Weakest information direction",
                "Elapsed time (s)",
                "Minimum information singular value (1)",
                [
                    _trace("Smallest mode", times, minimum_modes, "Elapsed time", "s", "Information singular value", "1"),
                    _trace("Numerical zero", times, np.zeros_like(times), "Elapsed time", "s", "Information singular value", "1"),
                ],
            ),
        },
        "observation": (
            "The rank answers whether every state direction is exposed; the condition "
            "number and posterior variance answer whether that exposure is numerically useful."
        ),
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
            "sample_count": int(model["sample_count"]),
            "signature": [float(value) for value in model["signature"]],
            "software_only": True,
        },
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
