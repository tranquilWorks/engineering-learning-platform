from __future__ import annotations

from typing import Any

import numpy as np


def _layout(title: str, x: str, y: str) -> dict[str, Any]:
    return {
        "title": {"text": title, "x": 0.02},
        "xaxis": {"title": x},
        "yaxis": {"title": y},
        "legend": {"orientation": "h"},
        "margin": {"l": 65, "r": 20, "t": 55, "b": 55},
        "hovermode": "closest",
        "uirevision": "keep-view",
    }


def _trace(name: str, x: Any, y: Any) -> dict[str, Any]:
    return {"type": "scatter", "mode": "lines", "name": name, "x": x, "y": y}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    plant_tau = float(parameters["plant_tau_s"])
    latency_ms = float(parameters["io_latency_ms"])
    fault_start = float(parameters["fault_start_s"])
    fault_duration = float(parameters["fault_duration_s"])
    watchdog = float(parameters["watchdog_ms"]) / 1000.0
    broken = bool(parameters["broken_mode"])
    dt = 0.01
    times = np.arange(0.0, 6.0 + 0.5 * dt, dt)
    output = np.zeros(len(times))
    effort = np.zeros(len(times))
    signal_age = np.zeros(len(times))
    delay_steps = max(0, round(latency_ms / 10.0))
    telemetry_queue = [0.0] * (delay_steps + 1)
    last_measurement = 0.0
    last_update = 0.0
    integral = 0.0
    fault_end = fault_start + fault_duration
    safe_active = np.zeros(len(times), dtype=bool)
    for index in range(len(times) - 1):
        now = times[index]
        telemetry_queue.append(float(output[index]))
        delayed = telemetry_queue.pop(0)
        dropout = fault_start <= now < fault_end
        if not dropout:
            last_measurement = delayed
            last_update = now
        signal_age[index] = now - last_update
        safe = signal_age[index] > watchdog and not broken
        safe_active[index] = safe
        error = 1.0 - last_measurement
        if safe:
            command = 0.0
        else:
            integral += error * dt
            command = float(np.clip(2.0 * error + integral, -2.0, 2.0))
        effort[index] = command
        output[index + 1] = output[index] + dt * (-output[index] + command) / plant_tau
    signal_age[-1] = times[-1] - last_update
    effort[-1] = effort[-2]
    safe_active[-1] = signal_age[-1] > watchdog and not broken
    detections = np.flatnonzero(signal_age > watchdog)
    detection_time = (
        times[detections[0]] if len(detections) and not broken else times[-1]
    )
    safe_duration = np.sum(safe_active) * dt
    error = 1.0 - output
    verdict = bool(len(detections) > 0 and not broken and np.all(np.isfinite(output)))
    signature = [
        np.max(np.abs(error)),
        np.max(output),
        detection_time,
        safe_duration,
        output[-1],
        float(verdict),
    ]
    return {
        "metrics": [
            {
                "id": "test_verdict",
                "label": "Dropout-monitor verdict",
                "value": "pass" if verdict else "fail",
                "unit": None,
                "emphasis": "primary",
            },
            {
                "id": "fault_detection_time",
                "label": "Watchdog detection time",
                "value": detection_time,
                "unit": "s",
            },
            {
                "id": "safe_command_duration",
                "label": "Safe-command duration",
                "value": safe_duration,
                "unit": "s",
            },
            {
                "id": "maximum_output",
                "label": "Maximum virtual-plant output",
                "value": np.max(output),
                "unit": "normalized",
            },
        ],
        "plots": {
            "response": {
                "data": [
                    _trace("Reference command", times, np.ones_like(times)),
                    _trace("Virtual plant output", times, output),
                    _trace("Controller effort", times, effort),
                ],
                "layout": _layout(
                    "Software-HIL closed-loop response",
                    "Time (s)",
                    "Normalized signal (-)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
            "mechanism": {
                "data": [
                    _trace("Telemetry age", times, 1000.0 * signal_age),
                    _trace(
                        "Watchdog threshold",
                        times,
                        np.full_like(times, 1000.0 * watchdog),
                    ),
                    _trace("Safe state x100", times, 100.0 * safe_active.astype(float)),
                ],
                "layout": _layout(
                    "Interface freshness and monitor action",
                    "Time (s)",
                    "Age or state scale (ms)",
                ),
                "config": {"responsive": True, "displaylogo": False},
            },
        },
        "explanations": {
            "observation": "The deterministic harness closes a controller around a first-order virtual plant, delays telemetry, injects a dropout, and records a verdict from explicit freshness and finite-response criteria.",
            "broken": "Broken mode disables the freshness watchdog. Control continues from stale telemetry throughout the dropout, so the required fault-detection and safe-command evidence is absent.",
            "recovery": "Enable the watchdog, freeze integral growth, command the virtual plant safe when telemetry age exceeds its bound, and retain the exact fault/detection/verdict trace.",
        },
        "diagnostics": {
            "item_id": "P24",
            "reference_basis": "independent discrete virtual-plant, delayed-telemetry, and watchdog recurrence",
            "broken_active": broken,
            "sample_count": len(times),
            "software_hil_only": True,
            "signature": [float(value) for value in signature],
        },
    }
