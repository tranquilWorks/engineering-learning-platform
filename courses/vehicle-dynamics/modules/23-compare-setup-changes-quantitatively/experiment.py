from __future__ import annotations

import math
from typing import Any

PRIMARY = "aero_change_percent"
SECONDARY = "tire_mu_change_percent"
PRIMARY_RANGE = (-20.0, 30.0)
SECONDARY_RANGE = (-10.0, 15.0)
FIELDS = [
    "baseline_lap_s",
    "candidate_lap_s",
    "paired_delta_s",
    "aero_main_effect_s",
    "tire_main_effect_s",
    "interaction_effect_s",
    "paired_standard_error_s",
    "decision_margin_s",
    "worthwhile",
    "invalid",
]

BASELINE = [28.0, 35.0, 22.0, 31.0]
AERO_SENSITIVITY = [1.0, 0.4, 1.2, 0.6]
TIRE_SENSITIVITY = [0.8, 1.2, 0.7, 1.1]


def _compare(aero: float, tire: float, broken: bool) -> tuple[list[float], list[str], list[float], list[float]]:
    candidates = [
        base * (1.0 - 0.0008 * aero * aero_sensitivity - 0.002 * tire * tire_sensitivity - 0.00001 * aero * tire)
        for base, aero_sensitivity, tire_sensitivity in zip(BASELINE, AERO_SENSITIVITY, TIRE_SENSITIVITY, strict=True)
    ]
    compared = candidates[1:] + candidates[:1] if broken else candidates
    paired = [candidate - base for candidate, base in zip(compared, BASELINE, strict=True)]
    mean_delta = sum(paired) / len(paired)
    standard_error = math.sqrt(sum((value - mean_delta) ** 2 for value in paired) / (len(paired) - 1)) / math.sqrt(len(paired))
    baseline_lap = sum(BASELINE)
    candidate_lap = sum(candidates)
    delta = candidate_lap - baseline_lap
    aero_effect = sum(-base * 0.0008 * aero * sensitivity for base, sensitivity in zip(BASELINE, AERO_SENSITIVITY, strict=True))
    tire_effect = sum(-base * 0.002 * tire * sensitivity for base, sensitivity in zip(BASELINE, TIRE_SENSITIVITY, strict=True))
    interaction = sum(-base * 0.00001 * aero * tire for base in BASELINE)
    threshold = -0.20
    worthwhile = delta < threshold and not broken
    signature = [baseline_lap, candidate_lap, delta, aero_effect, tire_effect, interaction, standard_error, threshold - delta, float(worthwhile), float(broken)]
    return signature, ["sector 1", "sector 2", "sector 3", "sector 4"], list(BASELINE), compared


def _plot(name: str, x: list[float], y: list[float], x_title: str, y_title: str) -> dict[str, Any]:
    return {
        "data": [{"type": "scatter", "mode": "lines+markers", "name": name, "x": x, "y": y}],
        "layout": {"title": {"text": "Compare Setup Changes Quantitatively"}, "xaxis": {"title": x_title}, "yaxis": {"title": y_title}, "uirevision": "keep-view"},
        "config": {"responsive": True, "displaylogo": False},
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    primary = float(parameters[PRIMARY])
    secondary = float(parameters[SECONDARY])
    broken = bool(parameters["broken_mode"])
    if not math.isfinite(primary) or not PRIMARY_RANGE[0] <= primary <= PRIMARY_RANGE[1]:
        raise ValueError(f"{PRIMARY} outside declared finite range")
    if not math.isfinite(secondary) or not SECONDARY_RANGE[0] <= secondary <= SECONDARY_RANGE[1]:
        raise ValueError(f"{SECONDARY} outside declared finite range")
    signature, sectors, baseline, candidate = _compare(primary, secondary, broken)
    if len(signature) != len(FIELDS) or not all(math.isfinite(value) for value in signature):
        raise ValueError("setup comparison produced an invalid signature")
    primary_values = [-20.0, 10.0, 30.0]
    secondary_values = [-10.0, 5.0, 15.0]
    failed = _compare(primary, secondary, True)[0]
    recovered = _compare(10.0, 5.0, False)[0]
    response = _plot("baseline", [1.0, 2.0, 3.0, 4.0], baseline, "paired sector", "sector time (s)")
    response["data"].append({"type": "scatter", "mode": "lines+markers", "name": "candidate", "x": [1.0, 2.0, 3.0, 4.0], "y": candidate, "text": sectors})
    return {
        "metrics": [
            {"id": "delta", "label": "Paired lap delta", "value": signature[2], "unit": "s", "emphasis": "primary"},
            {"id": "uncertainty", "label": "Paired standard error", "value": signature[6], "unit": "s"},
            {"id": "valid", "label": "Pairing valid", "value": not bool(signature[-1]), "unit": "boolean"},
        ],
        "plots": {
            "response": response,
            "primary_sweep": _plot(PRIMARY, primary_values, [_compare(value, secondary, False)[0][2] for value in primary_values], "aero change (%)", "paired lap delta (s)"),
            "secondary_sweep": _plot(SECONDARY, secondary_values, [_compare(primary, value, False)[0][2] for value in secondary_values], "tire μ change (%)", "paired lap delta (s)"),
            "broken_recovery": {
                "data": [
                    {"type": "bar", "name": "unpaired sectors", "x": FIELDS[:-1], "y": failed[:-1]},
                    {"type": "bar", "name": "recovered pairing", "x": FIELDS[:-1], "y": recovered[:-1]},
                ],
                "layout": {"barmode": "group", "xaxis": {"title": "comparison quantity"}, "yaxis": {"title": "reported value"}},
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "Paired sectors preserve like-for-like comparisons and separate aero, tire, and interaction contributions.",
            "broken": "Broken mode rotates candidate sectors before pairing, inflating scatter and invalidating the quantitative verdict.",
            "recovery": "Match each candidate sector to its baseline sector, retain the interaction term, and apply the declared 0.20 s threshold.",
        },
        "diagnostics": {"item_id": "P23", "signature": signature, "fields": FIELDS, "broken_active": broken, "bounded_points": len(sectors)},
    }
