from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 47
DEFAULTS = {"final_drive_ratio": 4.1, "shift_delay_s": 0.25}
RANGES = {"final_drive_ratio": (3.5, 4.8), "shift_delay_s": (0.05, 0.6)}
BROKEN_TEXT = "Broken mode holds first gear beyond redline and removes every shift interruption, creating a fast but invalid acceleration result."
RECOVERY_TEXT = "Select the largest valid wheel force within the engine-speed band and apply the declared interruption whenever the selected gear changes."


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


def _plot(title: str, x_title: str, y_title: str, traces: list[dict[str, Any]]) -> dict[str, Any]:
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


GEARS = np.array((3.60, 2.20, 1.50, 1.15))


def _engine_torque(rpm: float) -> float:
    return 220.0 - 6.0e-6 * (rpm - 4500.0) ** 2


def _gear_state(speed: float, final_drive: float, broken: bool) -> tuple[int, float, float]:
    rpm_values = speed / 0.31 * GEARS * final_drive * 60.0 / (2.0 * np.pi)
    if broken:
        rpm = rpm_values[0]
        torque = max(120.0, _engine_torque(min(rpm, 7000.0)))
        return 0, rpm, torque * GEARS[0] * final_drive * 0.92 / 0.31
    forces = np.full(4, -np.inf)
    for index, rpm in enumerate(rpm_values):
        if 1500.0 <= rpm <= 7000.0:
            forces[index] = _engine_torque(float(rpm)) * GEARS[index] * final_drive * 0.92 / 0.31
    if not np.any(np.isfinite(forces)):
        valid = int(np.argmin(np.abs(rpm_values - 4250.0)))
        return valid, float(rpm_values[valid]), 0.0
    gear = int(np.argmax(forces))
    return gear, float(rpm_values[gear]), float(forces[gear])


def _simulate(final_drive: float, delay: float, broken: bool) -> tuple[list[float], np.ndarray, np.ndarray, np.ndarray]:
    step, samples = 0.01, 4001
    time = np.arange(samples) * step
    speed = np.zeros(samples)
    speed[0] = 5.0
    gear_trace = np.zeros(samples)
    selected, _, _ = _gear_state(speed[0], final_drive, broken)
    interruption = 0.0
    shift_speeds: list[float] = []
    peak_acceleration = 0.0
    max_redline_excess = 0.0
    finish_time = time[-1]
    for index in range(1, samples):
        desired, rpm, force = _gear_state(speed[index - 1], final_drive, broken)
        max_redline_excess = max(max_redline_excess, rpm - 7000.0)
        if not broken and desired != selected and interruption <= 0.0:
            selected = desired
            interruption = delay
            shift_speeds.append(speed[index - 1])
        if interruption > 0.0:
            force = 0.0
            interruption = max(0.0, interruption - step)
        resistance = 180.0 + 0.38 * speed[index - 1] ** 2
        acceleration = max(0.0, (force - resistance) / 1450.0)
        peak_acceleration = max(peak_acceleration, acceleration)
        speed[index] = speed[index - 1] + acceleration * step
        gear_trace[index] = selected + 1
        if speed[index] >= 27.78 and finish_time == time[-1]:
            finish_time = time[index]
    first = shift_speeds[0] * 3.6 if shift_speeds else 0.0
    second = shift_speeds[1] * 3.6 if len(shift_speeds) > 1 else 0.0
    signature = [finish_time, first, second, peak_acceleration, max(0.0, max_redline_excess)]
    return signature, time, speed, gear_trace


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    signature, time, speed, gear_trace = _simulate(
        p["final_drive_ratio"], p["shift_delay_s"], broken
    )
    return {
        "signature": signature,
        "metrics": [
            ("zero_to_hundred", "Time to 100 km/h", signature[0], "s"),
            ("first_shift", "First shift speed", signature[1], "km/h"),
            ("second_shift", "Second shift speed", signature[2], "km/h"),
            ("strategy_residual", "Redline residual", signature[4], "rpm"),
        ],
        "plots": {
            "response": _plot(
                "Acceleration strategy",
                "Elapsed time (s)",
                "Vehicle speed (m/s)",
                [_trace("Vehicle speed", time, speed, "Elapsed time", "s", "Vehicle speed", "m/s")],
            ),
            "mechanism": _plot(
                "Selected gear",
                "Vehicle speed (m/s)",
                "Gear number (1)",
                [_trace("Selected gear", speed, gear_trace, "Vehicle speed", "m/s", "Gear number", "1")],
            ),
        },
        "observation": "A useful shift strategy maximizes valid wheel force inside the engine-speed band and pays the time cost of each torque interruption.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
