from __future__ import annotations

import numpy as np

ITEM_NUMBER = 67
DEFAULTS = {"setup_delta": 0.08, "uncertainty_fraction": 0.05}
RANGES = {"setup_delta": (0.02, 0.15), "uncertainty_fraction": (0.02, 0.1)}
BROKEN_TEXT = "Broken mode counts aerodynamic downforce twice in the grip model. The physical normal-load ledger counts it once and measures the discrepancy."
RECOVERY_TEXT = "Restore one aerodynamic load contribution and rerun tire, chassis, gearing, braking, line, lap and uncertainty checks with the same controls."


def _parameters(s):
    r = {}
    for k, d in DEFAULTS.items():
        v = float(s.get(k, d))
        lo, hi = RANGES[k]
        if not np.isfinite(v) or v < lo or v > hi:
            raise ValueError(f"{k} outside declared finite range [{lo}, {hi}]")
        r[k] = v
    return r


def _tr(n, x, y, xq, xu, yq, yu):
    return {
        "type": "scatter",
        "mode": "lines",
        "name": n,
        "x": np.asarray(x),
        "y": np.asarray(y),
        "meta": {"x_quantity": xq, "x_unit": xu, "y_quantity": yq, "y_unit": yu},
    }


def _pl(t, xt, yt, d):
    return {
        "data": d,
        "layout": {
            "title": {"text": t},
            "xaxis": {"title": {"text": xt}},
            "yaxis": {"title": {"text": yt}},
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


def _tire_calibration():
    normal = 1450 * 9.81 / 4
    slip = np.array([0.005, 0.01, 0.02, 0.03, 0.12, 0.16])
    force = np.minimum(70000 * slip, 1.15 * normal)
    stiffness = float(np.linalg.lstsq(slip[:4, None], force[:4], rcond=None)[0][0])
    friction = float(np.mean(force[4:]) / normal)
    unseen = np.array([0.04, 0.07])
    error = float(
        max(
            abs(
                np.minimum(stiffness * unseen, friction * normal)
                - np.minimum(70000 * unseen, 1.15 * normal)
            )
        )
    )
    return stiffness, friction, error


def _gear_force(speed):
    ratios = np.array([3.63, 2.19, 1.54, 1.21, 1.0, 0.77]) * 4.1
    rpm = np.asarray(speed)[..., None] / 0.31 * ratios * 60 / (2 * np.pi)
    torque = np.interp(
        rpm,
        [2000, 3000, 4000, 5000, 6000, 7000, 7400],
        [170, 205, 225, 230, 225, 200, 180],
    )
    force = np.where((rpm >= 2000) & (rpm <= 7400), torque * ratios * 0.9 / 0.31, 0.0)
    return np.max(force, axis=-1), np.argmax(force, axis=-1) + 1


def _loads(square, curvature, setup, broken=False):
    down = 0.5 * 1.225 * 2.5 * (1 + 2 * setup) * square
    used_down = down * (2 if broken else 1)
    transfer = 1450 * square * curvature * 0.5 / 1.52
    front_split = 0.55 + 0.1 * setup
    front = (0.53 * 1450 * 9.81 + 0.5 * used_down) / 2
    rear = (0.47 * 1450 * 9.81 + 0.5 * used_down) / 2
    loads = np.stack(
        (
            front + front_split * transfer,
            front - front_split * transfer,
            rear + (1 - front_split) * transfer,
            rear - (1 - front_split) * transfer,
        ),
        axis=-1,
    )
    return loads, down


def _lap(setup, friction_factor=1.0, broken=False, count=96):
    _, mu, _ = _tire_calibration()
    mu *= (1 + 0.3 * setup) * friction_factor
    theta = (np.arange(count) + 0.5) * 2 * np.pi / count
    tangent = np.hypot(180 * np.sin(theta), 110 * np.cos(theta))
    center_k = 19800 / tangent**3
    center_ds = tangent * 2 * np.pi / count
    offsets = np.linspace(-1.5, 1.5, 9)
    scale = 1 - offsets[:, None] * center_k
    curvature = center_k / scale
    ds = center_ds * scale
    normal = 1450 * 9.81 / 4

    def grip(square, physical=False):
        loads, down = _loads(square, curvature, setup, broken and not physical)
        capacity = mu * normal * np.sum((np.maximum(loads, 0) / normal) ** 0.9, axis=-1)
        return capacity, loads, down

    lower = np.full_like(curvature, 25.0)
    upper = np.full_like(curvature, 70.0**2)
    for _ in range(42):
        middle = (lower + upper) / 2
        capacity, loads, _ = grip(middle)
        okay = (1450 * middle * curvature <= 0.8 * capacity) & (
            np.min(loads, axis=-1) >= 200
        )
        lower = np.where(okay, middle, lower)
        upper = np.where(okay, upper, middle)
    square = lower
    drag = 0.5 * 1.225 * 0.72 * (1 + setup)
    rolling = 0.012 * 1450 * 9.81
    for iteration in range(512):
        capacity, _, _ = grip(square)
        propulsion, _ = _gear_force(np.sqrt(square))
        drive = np.minimum(0.6 * capacity, propulsion)
        brake = np.minimum(0.6 * capacity, 7500 * (1 + setup))
        forward = square + 2 * ds * (drive - drag * square - rolling) / 1450
        backward = (np.roll(square, -1, axis=1) + 2 * ds * (brake + rolling) / 1450) / (
            1 - 2 * ds * drag / 1450
        )
        updated = np.minimum(square, np.minimum(np.roll(forward, 1, axis=1), backward))
        if np.max(abs(updated - square)) < 1e-9:
            square = updated
            break
        square = updated
    else:
        raise ValueError("Coupled lap solver did not converge")
    speed = np.sqrt(square)
    time = np.sum(ds / speed, axis=1)
    chosen = int(np.argmin(time))
    capacity, used_loads, down = grip(square)
    physical_capacity, physical_loads, _ = grip(square, True)
    propulsion, gears = _gear_force(speed)
    force = (
        1450 * (np.roll(square, -1, axis=1) - square) / (2 * ds)
        + drag * square
        + rolling
    )
    drive = np.minimum(0.6 * capacity, propulsion)
    brake = np.minimum(0.6 * capacity, 7500 * (1 + setup))
    excess = np.maximum(0, np.maximum(force - drive, -force - brake))
    utilization = np.hypot(force, 1450 * square * curvature) / physical_capacity
    temperature = 20 + np.sum(np.maximum(-force * ds, 0), axis=1) / (32 * 500)
    ledger = abs(np.sum(used_loads, axis=-1) - (1450 * 9.81 + down)) / (
        1450 * 9.81 + down
    )
    take = lambda value: value[chosen]
    return {
        "lap_s": float(time[chosen]),
        "offset_m": float(offsets[chosen]),
        "candidate_times_s": time,
        "distance_m": take(np.cumsum(ds, axis=1) - ds),
        "segment_lengths_m": take(ds),
        "curvature_per_m": take(curvature),
        "speed_m_s": take(speed),
        "force_n": take(force),
        "gears": take(gears),
        "physical_loads_n": take(physical_loads),
        "grip_utilization": take(utilization),
        "minimum_wheel_load_n": float(np.min(take(physical_loads))),
        "peak_roll_rad": float(
            max(1450 * take(square) * take(curvature) * 0.5 / (100000 * (1 + setup)))
        ),
        "propulsion_excess_n": float(max(0, max(take(force - propulsion)))),
        "temperature_c": float(temperature[chosen]),
        "load_ledger_residual": float(max(take(ledger))),
        "geometry_residual_rad": float(abs(sum(take(ds * curvature)) - 2 * np.pi)),
        "reachability_excess_n": float(max(take(excess))),
        "iterations": iteration + 1,
    }


def _model(setup, uncertainty, broken):
    stiffness, mu, calibration_error = _tire_calibration()
    current = _lap(setup, 1.0, broken)
    baseline = _lap(0.0, 1.0, False)
    low = _lap(setup, 1 - uncertainty, broken)
    high = _lap(setup, 1 + uncertainty, broken)
    clean = _lap(setup, 1.0, False)
    replay = _lap(setup, 1.0, False)
    lower = min(low["lap_s"], high["lap_s"])
    upper = max(low["lap_s"], high["lap_s"])
    coverage = max(0, lower - current["lap_s"], current["lap_s"] - upper)
    recovery_error = abs(clean["lap_s"] - replay["lap_s"])
    req = {
        "DT-01": _requirement(
            "Unused tire calibration force error", calibration_error, "N", "<=", 1e-8
        ),
        "DT-02": _requirement(
            "Maximum physical combined-grip utilization",
            max(current["grip_utilization"]),
            "1",
            "<=",
            1.000001,
        ),
        "DT-03": _requirement(
            "Minimum physical wheel normal load",
            current["minimum_wheel_load_n"],
            "N",
            ">=",
            200,
        ),
        "DT-04": _requirement(
            "Selected-gear propulsion force excess",
            current["propulsion_excess_n"],
            "N",
            "<=",
            1e-5,
        ),
        "DT-05": _requirement(
            "One-lap adiabatic brake temperature",
            current["temperature_c"],
            "degC",
            "<=",
            450,
        ),
        "DT-06": _requirement(
            "Used/physical normal-load ledger residual",
            current["load_ledger_residual"],
            "fraction",
            "<=",
            1e-10,
        ),
        "DT-07": _requirement(
            "Closed-track total-curvature residual",
            current["geometry_residual_rad"],
            "rad",
            "<=",
            1e-6,
        ),
        "DT-08": _requirement(
            "Selected line offset magnitude", abs(current["offset_m"]), "m", "<=", 1.5
        ),
        "DT-09": _requirement(
            "Cyclic segment reachability excess",
            current["reachability_excess_n"],
            "N",
            "<=",
            1e-5,
        ),
        "DT-10": _requirement(
            "Nominal time outside friction endpoint envelope", coverage, "s", "<=", 1e-8
        ),
        "DT-11": _requirement(
            "Internal clean replay discrepancy", recovery_error, "s", "<=", 1e-10
        ),
    }
    passed = sum(r["passed"] for r in req.values())
    signature = [
        float(passed),
        11.0,
        current["lap_s"],
        upper - lower,
        baseline["lap_s"] - current["lap_s"],
        current["load_ledger_residual"],
        float(req["DT-11"]["passed"]),
    ]
    return {
        "signature": signature,
        "requirements": req,
        "current": current,
        "baseline": baseline,
        "friction_lap_endpoints_s": [low["lap_s"], high["lap_s"]],
        "tire_fit": [stiffness, mu],
        "clean_lap_s": clean["lap_s"],
    }


def run(parameters):
    p = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    r = _model(p["setup_delta"], p["uncertainty_fraction"], broken)
    current = r["current"]
    baseline = r["baseline"]
    labels = [
        "Requirements passed",
        "Requirements total",
        "Selected lap time",
        "Friction scenario time width",
        "Setup time improvement",
        "Normal-load ledger residual",
        "Internal clean replay check",
    ]
    units = ["count", "count", "s", "s", "s", "fraction", "bool"]
    columns = ["Requirement", "Quantity", "Value", "Unit", "Rule", "Verdict"]
    rows = [
        {
            "Requirement": key,
            "Quantity": v["quantity"],
            "Value": round(v["value"], 8),
            "Unit": v["unit"],
            "Rule": f"{v['operator']} {v['threshold']}",
            "Verdict": "pass" if v["passed"] else "fail",
        }
        for key, v in r["requirements"].items()
    ]
    return {
        "metrics": [
            {"id": f"m{i}", "label": label, "unit": unit, "value": r["signature"][i]}
            for i, (label, unit) in enumerate(zip(labels, units))
        ],
        "tables": {"requirements": {"columns": columns, "rows": rows}},
        "plots": {
            "response": _pl(
                "Executed baseline and changed-setup laps",
                "Line distance (m)",
                "Speed (m/s)",
                [
                    _tr(
                        "Setup",
                        current["distance_m"],
                        current["speed_m_s"],
                        "Line distance",
                        "m",
                        "Speed",
                        "m/s",
                    ),
                    _tr(
                        "Baseline",
                        baseline["distance_m"],
                        baseline["speed_m_s"],
                        "Line distance",
                        "m",
                        "Speed",
                        "m/s",
                    ),
                ],
            ),
            "mechanism": _pl(
                "Combined grip against the physical load ledger",
                "Line distance (m)",
                "Tire utilization (1)",
                [
                    _tr(
                        "Utilization",
                        current["distance_m"],
                        current["grip_utilization"],
                        "Line distance",
                        "m",
                        "Tire utilization",
                        "1",
                    ),
                    _tr(
                        "Boundary",
                        [0, max(current["distance_m"])],
                        [1, 1],
                        "Line distance",
                        "m",
                        "Tire utilization",
                        "1",
                    ),
                ],
            ),
        },
        "explanations": {
            "observation": "An illustrative, synthetic GR86-sized model fits tire data, computes four wheel loads, gears, brakes and aero, then solves nine closed-track line candidates. Friction endpoints form a scenario envelope, not a confidence interval. An internal clean replay does not validate the currently broken run.",
            "broken": BROKEN_TEXT,
            "recovery": RECOVERY_TEXT,
        },
        "diagnostics": {
            "item_number": 67,
            "broken_active": broken,
            "signature": r["signature"],
            "requirements": r["requirements"],
            "current": {
                k: v.tolist() if isinstance(v, np.ndarray) else v
                for k, v in current.items()
            },
            "baseline_lap_s": baseline["lap_s"],
            "clean_lap_s": r["clean_lap_s"],
            "friction_lap_endpoints_s": r["friction_lap_endpoints_s"],
            "tire_fit": r["tire_fit"],
            "measured_vehicle_data": False,
        },
    }
