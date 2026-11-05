from __future__ import annotations

import math
from typing import Any

PRIMARY = "raw_count"
SECONDARY = "frame_age_ms"
PRIMARY_RANGE = (0.0, 65535.0)
SECONDARY_RANGE = (0.0, 250.0)
FIELDS = [
    "wheel_speed_kmh",
    "wheel_speed_m_s",
    "round_trip_count_error",
    "frame_age_ms",
    "freshness_limit_ms",
    "can_identifier_decimal",
    "dlc_bytes",
    "trace_points",
    "invalid",
]


def _decode(raw_count: float, frame_age_ms: float, broken: bool) -> list[float]:
    count = round(raw_count)
    high = (count >> 8) & 0xFF
    low = count & 0xFF
    decoded_count = low * 256 + high if broken else high * 256 + low
    speed_kmh = decoded_count / 128.0
    speed_m_s = speed_kmh / 3.6
    round_trip_error = speed_kmh * 128.0 - count
    invalid = broken or frame_age_ms > 100.0
    return [
        speed_kmh,
        speed_m_s,
        round_trip_error,
        frame_age_ms,
        100.0,
        313.0,
        8.0,
        9.0,
        float(invalid),
    ]


def _plot(name: str, x: list[float], y: list[float], x_unit: str, y_unit: str) -> dict[str, Any]:
    return {
        "data": [{"type": "scatter", "mode": "lines+markers", "name": name, "x": x, "y": y}],
        "layout": {
            "title": {"text": "Decode and Plot CAN Signals"},
            "xaxis": {"title": x_unit},
            "yaxis": {"title": y_unit},
            "uirevision": "keep-view",
        },
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
    if abs(primary - round(primary)) > 1e-9:
        raise ValueError("raw_count must be an integer CAN field")

    signature = _decode(primary, secondary, broken)
    if len(signature) != len(FIELDS) or not all(math.isfinite(value) for value in signature):
        raise ValueError("decoder produced an invalid signature")

    center = round(primary)
    raw_trace = [min(65535, max(0, center + offset)) for offset in (-256, -192, -128, -64, 0, 64, 128, 192, 256)]
    time_ms = [20.0 * index for index in range(len(raw_trace))]
    decoded_trace = [_decode(value, secondary, broken)[0] for value in raw_trace]
    primary_values = [0.0, 4608.0, 65535.0]
    secondary_values = [0.0, 100.0, 250.0]
    failed = _decode(primary, secondary, True)
    recovered = _decode(4608.0, 40.0, False)
    return _present_result({
        "metrics": [
            {"id": "speed", "label": "Decoded wheel speed", "value": signature[0], "unit": "km/h", "emphasis": "primary"},
            {"id": "age", "label": "Frame age", "value": secondary, "unit": "ms"},
            {"id": "valid", "label": "Frame and decode valid", "value": not bool(signature[-1]), "unit": "boolean"},
        ],
        "plots": {
            "response": _plot("decoded wheel speed", time_ms, decoded_trace, "timestamp (ms)", "wheel speed (km/h)"),
            "primary_sweep": _plot(PRIMARY, primary_values, [_decode(value, secondary, False)[0] for value in primary_values], "raw count", "wheel speed (km/h)"),
            "secondary_sweep": _plot(SECONDARY, secondary_values, [_decode(primary, value, False)[-1] for value in secondary_values], "frame age (ms)", "invalid flag"),
            "broken_recovery": {
                "data": [
                    {"type": "bar", "name": "broken endian", "x": FIELDS[:-1], "y": failed[:-1]},
                    {"type": "bar", "name": "recovered baseline", "x": FIELDS[:-1], "y": recovered[:-1]},
                ],
                "layout": {"barmode": "group", "xaxis": {"title": "decoded field"}, "yaxis": {"title": "reported value"}},
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "The documented big-endian 0x1200 field decodes to 36 km/h at 1/128 km/h per count.",
            "broken": "Broken mode reverses the two bytes, so the count no longer round-trips and the decode is explicitly invalid.",
            "recovery": "Restore big-endian byte order, DLC 8, the documented scale, and a frame age no greater than 100 ms.",
        },
        "diagnostics": {"item_id": "P17", "signature": signature, "fields": FIELDS, "broken_active": broken, "bounded_points": 9},
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
