from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 26
DEFAULTS = {"normal_load_n": 3500, "load_exponent": 0.88}
RANGES = {"normal_load_n": (1000, 7000), "load_exponent": (0.7, 1)}
BROKEN_TEXT = "Broken mode replaces the reviewed sublinear exponent with one and erases the load-transfer penalty."
RECOVERY_TEXT = "Restore the reviewed exponent and compare even and split tire pairs at identical total normal load."


def _parameters(supplied: dict[str, Any]) -> dict[str, float]:
    result: dict[str, float] = {}
    for key, default in DEFAULTS.items():
        value = float(supplied.get(key, default))
        minimum, maximum = RANGES[key]
        if not np.isfinite(value) or value < minimum or value > maximum:
            raise ValueError(f"{key} outside declared finite range [{minimum}, {maximum}]")
        result[key] = value
    return result


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
        },
    }


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    load = p["normal_load_n"]
    exponent = p["load_exponent"]
    used_exponent = 1.0 if broken else exponent
    reference_load = 3500.0
    reference_mu = 1.25

    def peak_force(value: np.ndarray | float) -> np.ndarray | float:
        return reference_mu * reference_load * (np.asarray(value) / reference_load) ** used_exponent

    peak = float(peak_force(load))
    effective_mu = peak / load
    transfer_fraction = 0.25
    even_capacity = 2.0 * peak
    split_capacity = float(
        peak_force(load * (1.0 - transfer_fraction))
        + peak_force(load * (1.0 + transfer_fraction))
    )
    loss = even_capacity - split_capacity
    scaling = float(peak_force(2.0 * load) / peak)
    scaling_residual = abs(scaling - 2.0**exponent)

    loads = np.linspace(500.0, 8000.0, 151)
    forces = np.asarray(peak_force(loads), dtype=float)
    mus = forces / loads
    transfer = np.linspace(0.0, 0.45, 91)
    losses = [
        2.0 * peak
        - float(peak_force(load * (1.0 - fraction)) + peak_force(load * (1.0 + fraction)))
        for fraction in transfer
    ]
    signature = [peak, effective_mu, loss, scaling_residual, float(broken)]
    return {
        "signature": signature,
        "metrics": [
            ("peak_force", "Peak tire force", peak, "N"),
            ("effective_mu", "Effective friction coefficient", effective_mu, "1"),
            ("pair_loss", "Load-transfer capacity loss", loss, "N"),
            ("scaling_residual", "Power-law scaling residual", scaling_residual, "1"),
        ],
        "plots": {
            "response": _plot("Peak force and load-sensitive friction", "Normal load (N)", "Peak force (N)", [
                _trace("Peak force", loads, forces, "Normal load", "N", "Peak force", "N"),
            ]),
            "mechanism": _plot("Paired capacity penalty", "Load-transfer fraction (1)", "Capacity loss (N)", [
                _trace("Pair loss", transfer, losses, "Load-transfer fraction", "1", "Capacity loss", "N"),
                _trace("Effective friction", loads / 8000.0, mus, "Normalized load", "1", "Effective friction", "1"),
            ]),
        },
        "observation": "Sublinear peak-force growth makes the more-loaded tire less efficient, so unequal sharing loses total capacity at fixed total load.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
