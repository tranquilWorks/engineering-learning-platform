from __future__ import annotations

import math
from typing import Any

PRIMARY = "gps_weight"
SECONDARY = "imu_bias_m_s2"
PRIMARY_RANGE = (0.0, 1.0)
SECONDARY_RANGE = (-0.30, 0.30)
FIELDS = [
    "final_position_error_m",
    "final_velocity_error_m_s",
    "position_rmse_m",
    "mean_abs_innovation_m",
    "final_gps_residual_m",
    "maximum_time_skew_s",
    "samples",
    "invalid",
]


def _simulate(weight: float, bias: float, broken: bool) -> tuple[list[float], list[float], list[float]]:
    dt = 0.5
    acceleration = 0.4
    times = [index * dt for index in range(21)]
    truth = [0.5 * acceleration * time * time for time in times]
    gps = [value + 0.6 * math.sin(0.7 * time) for value, time in zip(truth, times, strict=True)]
    fused = 0.0
    velocity = 0.0
    estimates = [fused]
    innovations: list[float] = []
    for index in range(1, len(times)):
        measured_acceleration = acceleration + bias
        predicted = fused + velocity * dt + 0.5 * measured_acceleration * dt * dt
        velocity += measured_acceleration * dt
        gps_index = max(0, index - 2) if broken else index
        innovation = gps[gps_index] - predicted
        fused = predicted + weight * innovation
        innovations.append(abs(innovation))
        estimates.append(fused)
    errors = [estimate - actual for estimate, actual in zip(estimates, truth, strict=True)]
    rmse = math.sqrt(sum(error * error for error in errors) / len(errors))
    signature = [
        errors[-1],
        velocity - acceleration * times[-1],
        rmse,
        sum(innovations) / len(innovations),
        estimates[-1] - gps[-1],
        1.0 if broken else 0.0,
        float(len(times)),
        float(broken),
    ]
    return signature, times, estimates


def _plot(name: str, x: list[float], y: list[float], x_title: str, y_title: str) -> dict[str, Any]:
    return {
        "data": [{"type": "scatter", "mode": "lines+markers", "name": name, "x": x, "y": y}],
        "layout": {"title": {"text": "Fuse GPS and IMU Motion"}, "xaxis": {"title": x_title}, "yaxis": {"title": y_title}, "uirevision": "keep-view"},
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
    signature, times, estimates = _simulate(primary, secondary, broken)
    if len(signature) != len(FIELDS) or not all(math.isfinite(value) for value in signature):
        raise ValueError("fusion model produced an invalid signature")
    primary_values = [0.0, 0.25, 1.0]
    secondary_values = [-0.30, 0.05, 0.30]
    failed = _simulate(primary, secondary, True)[0]
    recovered = _simulate(0.25, 0.05, False)[0]
    return _present_result({
        "metrics": [
            {"id": "rmse", "label": "Position RMSE", "value": signature[2], "unit": "m", "emphasis": "primary"},
            {"id": "innovation", "label": "Mean absolute innovation", "value": signature[3], "unit": "m"},
            {"id": "valid", "label": "Time alignment valid", "value": not bool(signature[-1]), "unit": "boolean"},
        ],
        "plots": {
            "response": _plot("fused position", times, estimates, "time (s)", "position (m)"),
            "primary_sweep": _plot(PRIMARY, primary_values, [_simulate(value, secondary, False)[0][2] for value in primary_values], "GPS correction weight", "position RMSE (m)"),
            "secondary_sweep": _plot(SECONDARY, secondary_values, [_simulate(primary, value, False)[0][2] for value in secondary_values], "IMU bias (m/s²)", "position RMSE (m)"),
            "broken_recovery": {
                "data": [
                    {"type": "bar", "name": "misaligned", "x": FIELDS[:-1], "y": failed[:-1]},
                    {"type": "bar", "name": "aligned baseline", "x": FIELDS[:-1], "y": recovered[:-1]},
                ],
                "layout": {"barmode": "group", "xaxis": {"title": "fusion diagnostic"}, "yaxis": {"title": "SI value"}},
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "GPS corrections bound position drift while the IMU supplies motion between the half-second fixes.",
            "broken": "Broken mode associates each prediction with GPS from one second earlier and reports the time skew explicitly.",
            "recovery": "Align sensor timestamps before computing innovations, then restore the 0.25 correction weight and 0.05 m/s² bias case.",
        },
        "diagnostics": {"item_id": "P18", "signature": signature, "fields": FIELDS, "broken_active": broken, "bounded_points": len(times)},
    })


def _present_result(result):
    """Present unchanged calculations with readable, dimensionless comparison axes."""
    from textwrap import fill
    for plot in result["plots"].values():
        layout = plot["layout"]
        title = layout.get("title", {}).get("text", "")
        layout["title"] = {"text": fill(title, width=30).replace("\n", "<br>"), "font": {"size": 14}, "x": 0.02}
        layout["legend"] = {"orientation": "h"}
        layout["margin"] = {"l": 72, "r": 36, "t": 80, "b": 110}
        for axis in ("xaxis", "yaxis"):
            layout[axis]["automargin"] = True
    comparison = result["plots"]["broken_recovery"]
    fields = comparison["data"][0]["x"]
    baseline = comparison["data"][1]["y"]
    scales = [max(1.0, abs(value)) for value in baseline]
    for trace in comparison["data"]:
        raw = trace["y"]
        trace["x"] = [f"D{i+1}" for i in range(len(fields))]
        trace["y"] = [value / scale for value, scale in zip(raw, scales, strict=True)]
        trace["customdata"] = [f"{field}: {value:.5g}; scale {scale:.5g} in the field's unit" for field, value, scale in zip(fields, raw, scales, strict=True)]
        trace["hovertemplate"] = "%{customdata}<br>Normalized value: %{y:.5g}<extra>%{fullData.name}</extra>"
    comparison["layout"]["title"] = {"text": "Per-field normalized<br>fault and recovery", "font": {"size": 14}, "x": 0.02}
    comparison["layout"]["xaxis"]["title"] = "Diagnostic index (see key)"
    comparison["layout"]["yaxis"]["title"] = "Normalized value (1)"
    return result
