from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 67
BROKEN_TEXT = (
    "Broken mode replays arrival order, integrates arrival-time deltas, weakly blends measurements, "
    "and never declares the source-time gap. The log is readable but not causally reproducible."
)
RECOVERY_TEXT = (
    "Order by monotonic source time, audit clock residual and missing intervals, enter safe hold at "
    "the gap, reset from the next valid checkpoint, and retain the replay/fault decision trace."
)


def _trace(name: str, x: Any, y: Any, x_quantity: str, x_unit: str,
           y_quantity: str, y_unit: str) -> dict[str, Any]:
    return {"type": "scattergl", "mode": "lines+markers", "name": name,
            "x": np.asarray(x, dtype=float), "y": np.asarray(y, dtype=float),
            "meta": {"x_quantity": x_quantity, "x_unit": x_unit,
                     "y_quantity": y_quantity, "y_unit": y_unit}}


def _plot(title: str, x_title: str, y_title: str,
          traces: list[dict[str, Any]]) -> dict[str, Any]:
    return {"data": traces, "layout": {"title": {"text": title, "x": 0.02},
            "xaxis": {"title": {"text": x_title}}, "yaxis": {"title": {"text": y_title}},
            "legend": {"orientation": "h"}, "margin": {"l": 72, "r": 36, "t": 62, "b": 62},
            "hovermode": "closest", "uirevision": "keep-view"},
            "config": {"responsive": True, "displaylogo": False}}


def _model(parameters: dict[str, Any], broken: bool) -> dict[str, Any]:
    dropout = 0.001 * float(parameters["dropout_duration_ms"])
    drift = 1.0e-6 * float(parameters["clock_drift_ppm"])
    times = np.arange(0.0, 2.0001, 0.02)
    truth = np.sin(1.4 * times)
    velocity = 1.4 * np.cos(1.4 * times)
    present = ~((times >= 0.80) & (times < 0.80 + dropout))
    indices = np.flatnonzero(present)
    remote = times[indices] * (1.0 + drift)
    arrival = remote + 0.018 * np.sin(1.7 * indices)
    faults = 0
    recovery_latency_ms = 0.0
    replay_times: list[float] = []
    replay_values: list[float] = []
    if broken:
        order = indices[np.argsort(arrival)]
        estimate = 0.0
        previous_arrival = 0.0
        last_velocity = velocity[0]
        for index in order:
            event_arrival = times[index] * (1.0 + drift) + 0.018 * np.sin(1.7 * index)
            delta = max(event_arrival - previous_arrival, 0.0)
            estimate += last_velocity * delta
            estimate = 0.92 * estimate + 0.08 * truth[index]
            last_velocity = velocity[index]
            previous_arrival = event_arrival
            replay_times.append(float(times[index]))
            replay_values.append(estimate)
        recovery_latency_ms = 1000.0
        reference = np.sin(1.4 * np.asarray(replay_times))
    else:
        estimate = truth[0]
        last_velocity = velocity[0]
        last_measurement = 0.0
        gap_seen = False
        for index, time_s in enumerate(times):
            if index > 0:
                estimate += last_velocity * 0.02
            if present[index]:
                gap = time_s - last_measurement
                if gap > 0.060001:
                    faults += 1
                    gap_seen = True
                    estimate = truth[index]
                    recovery_latency_ms = 20.0
                else:
                    estimate = 0.35 * estimate + 0.65 * truth[index]
                last_velocity = velocity[index]
                last_measurement = time_s
            replay_times.append(float(time_s))
            replay_values.append(float(estimate))
        if abs(float(parameters["clock_drift_ppm"])) > 150.0:
            faults += 1
        if not gap_seen:
            recovery_latency_ms = 0.0
        reference = truth
    replay_array = np.asarray(replay_values)
    rms_error = float(np.sqrt(np.mean((replay_array - reference) ** 2)))
    clock_residual_ms = 1000.0 * (remote - times[indices])
    return {"signature": [rms_error, float(faults), recovery_latency_ms],
            "sample_count": len(replay_array),
            "metrics": [("replay_state_rms_error", "Replay State RMS Error", rms_error, "m"),
                        ("diagnosed_timing_faults", "Diagnosed Timing Faults", faults, "count"),
                        ("safe_recovery_latency", "Safe Recovery Latency", recovery_latency_ms, "ms")],
            "plots": {"response": _plot("Deterministic state replay", "Source time (s)",
                "Replayed position (m)", [
                    _trace("Reference", replay_times, reference, "Source time", "s", "Replayed position", "m"),
                    _trace("Replay", replay_times, replay_array, "Source time", "s", "Replayed position", "m")]),
                "mechanism": _plot("Remote-clock residual", "Source time (s)",
                "Clock residual (ms)", [
                    _trace("Clock residual", times[indices], clock_residual_ms, "Source time", "s",
                           "Clock residual", "ms"),
                    _trace("Drift review limit", times[indices], np.full(len(indices), 0.30),
                           "Source time", "s", "Clock residual", "ms")])},
            "observation": (f"Replay RMS error is {rms_error:.4f} m; the diagnostic trace reports "
                            f"{faults} timing fault(s) and {recovery_latency_ms:.1f} ms recovery latency.")}


def _result(model: dict[str, Any], broken: bool) -> dict[str, Any]:
    return {"metrics": [{"id": key, "label": label, "value": float(value), "unit": unit,
            "emphasis": "primary" if index == 0 else "normal"}
            for index, (key, label, value, unit) in enumerate(model["metrics"])], "plots": model["plots"],
            "explanations": {"observation": model["observation"], "broken": BROKEN_TEXT, "recovery": RECOVERY_TEXT},
            "diagnostics": {"item_number": ITEM_NUMBER, "broken_active": bool(broken),
            "sample_count": int(model["sample_count"]), "signature": [float(v) for v in model["signature"]],
            "software_only": True}}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
