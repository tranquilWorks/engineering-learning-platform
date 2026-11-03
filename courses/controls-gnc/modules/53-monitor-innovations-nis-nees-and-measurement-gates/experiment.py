from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 53
BROKEN_TEXT = "Bypass the innovation gate while retaining the identical injected innovation at update 20."
RECOVERY_TEXT = "Restore gating, reset, and verify the original measurement is rejected when its NIS exceeds the selected threshold."


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
    gate = float(p["nis_gate"])
    magnitude = float(p["outlier_sigma"])
    estimate = 0.0
    covariance = 1.0
    rows = []
    for k in range(40):
        truth = 0.2 * np.sin(0.3 * k)
        prior = covariance + 0.02
        innovation_variance = prior + 0.25
        measurement = truth + 0.3 * np.cos(0.71 * k)
        if k == 20:
            measurement = estimate + magnitude * np.sqrt(innovation_variance)
        innovation = measurement - estimate
        nis = innovation**2 / innovation_variance
        accept = broken or nis <= gate
        gain = prior / innovation_variance if accept else 0.0
        estimate += gain * innovation
        covariance = (1 - gain) ** 2 * prior + gain**2 * 0.25
        nees = (estimate - truth) ** 2 / covariance
        rows.append(
            [
                truth,
                measurement,
                estimate,
                covariance,
                nis,
                nees,
                float(accept),
                innovation_variance,
                innovation,
            ]
        )
    h = np.asarray(rows)
    nis = float(h[20, 4])
    return {
        "signature": [nis, max(nis - gate, 0), h[20, 6]],
        "metrics": [
            ("normalized_innovation_squared", "Injected measurement NIS", nis, "1"),
            ("gate_exceedance", "NIS exceedance", max(nis - gate, 0), "1"),
            ("accepted_outlier", "Injected measurement accepted", h[20, 6], "bool"),
            (
                "mean_nees",
                "Mean posterior NEES (deterministic example)",
                np.mean(h[:, 5]),
                "1",
            ),
        ],
        "history": {
            "filter_history": h,
            "columns": [
                "truth",
                "measurement",
                "estimate",
                "P",
                "NIS",
                "NEES",
                "accepted",
                "S",
                "innovation",
            ],
            "outlier_index": 20,
        },
        "plots": {
            "response": _plot(
                "Gated state estimate",
                "Update index (step)",
                "Normalized state (1)",
                [
                    _trace(
                        "Truth",
                        np.arange(40),
                        h[:, 0],
                        "Update index",
                        "step",
                        "State",
                        "1",
                    ),
                    _trace(
                        "Measurement",
                        np.arange(40),
                        h[:, 1],
                        "Update index",
                        "step",
                        "State",
                        "1",
                    ),
                    _trace(
                        "Estimate",
                        np.arange(40),
                        h[:, 2],
                        "Update index",
                        "step",
                        "State",
                        "1",
                    ),
                ],
            ),
            "mechanism": _plot(
                "NIS and posterior NEES",
                "Update index (step)",
                "Squared normalized error (1)",
                [
                    _trace(
                        "NIS",
                        np.arange(40),
                        h[:, 4],
                        "Update index",
                        "step",
                        "NIS",
                        "1",
                    ),
                    _trace(
                        "Posterior NEES",
                        np.arange(40),
                        h[:, 5],
                        "Update index",
                        "step",
                        "NEES",
                        "1",
                    ),
                    _trace(
                        "NIS gate",
                        np.arange(40),
                        np.full(40, gate),
                        "Update index",
                        "step",
                        "NIS gate",
                        "1",
                    ),
                ],
            ),
        },
        "observation": "NIS normalizes the innovation by its predicted variance BEFORE the update; NEES normalizes posterior truth error by posterior P. The same injected innovation is gated or forcibly accepted. Deterministic time samples are not an independent chi-square consistency study.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
