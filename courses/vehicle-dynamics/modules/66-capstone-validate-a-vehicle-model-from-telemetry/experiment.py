from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

ITEM_NUMBER = 66
DEFAULTS = {"validation_fraction": 0.3, "fault_severity": 1.0}
RANGES = {"validation_fraction": (0.2, 0.4), "fault_severity": (0.5, 2.0)}
BROKEN_TEXT = "Broken mode skips clock and sensor calibration and leaves injected corrupt/duplicate packets unrecovered; the same chronological split is retained."
RECOVERY_TEXT = "Replay deterministically, align and calibrate first, preserve a held-out split, trace every requirement, inject a fault, and sign the recovery evidence."


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
        "mode": "lines+markers",
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


def _decode(records):
    wheel, yaw = {}, {}
    for record in records:
        payload = bytes.fromhex(record["payload_hex"])
        identifier = int.from_bytes(payload[:4], "little")
        data = payload[4:]
        time = record["source_time_us"] / 1e6
        if identifier == 0x139:
            wheel[time] = (
                sum(int.from_bytes(data[j : j + 2], "big") for j in range(0, 8, 2))
                / 4
                / 128
                / 3.6
            )
        elif identifier == 0x2D2:
            yaw[time] = (int.from_bytes(data[:2], "big") - 32768) / 100 * np.pi / 180
    return (
        np.array(sorted(wheel)),
        np.array([wheel[t] for t in sorted(wheel)]),
        np.array(sorted(yaw)),
        np.array([yaw[t] for t in sorted(yaw)]),
    )


def _trajectory(time, speed, yaw):
    dt = np.diff(time)
    heading = np.r_[0.0, np.cumsum(yaw[:-1] * dt)]
    increments = speed[:-1] * dt * np.exp(1j * heading[:-1])
    return np.r_[0j, np.cumsum(increments)]


def _telemetry(validation_fraction, severity, broken):
    fixture = Path(__file__).resolve().parents[2] / "fixtures"
    manifest = json.loads((fixture / "manifest.json").read_text())
    hashes = {entry["path"]: entry["sha256"] for entry in manifest["files"]}
    names = ("gr86-can-replay-v1.jsonl", "racechrono-ble-replay-v1.jsonl")
    hash_failures = sum(
        hashlib.sha256((fixture / name).read_bytes()).hexdigest() != hashes[name]
        for name in names
    )
    can = [json.loads(line) for line in (fixture / names[0]).read_text().splitlines()]
    nominal = [
        json.loads(line) for line in (fixture / names[1]).read_text().splitlines()
    ]
    canonical = {
        r["sequence"]: {
            "sequence": r["sequence"],
            "source_time_us": r["source_time_us"],
            "payload_hex": (
                int(r["can_id"], 16).to_bytes(4, "little")
                + bytes.fromhex(r["data_hex"])
            )
            .hex()
            .upper(),
        }
        for r in can
    }

    def anomalies(records):
        seen = set()
        count = 0
        for r in records:
            expected = canonical[r["sequence"]]
            count += int(
                r["sequence"] in seen
                or r["source_time_us"] != expected["source_time_us"]
                or r["payload_hex"].upper() != expected["payload_hex"]
            )
            seen.add(r["sequence"])
        return count

    provenance = (
        hash_failures
        + anomalies(nominal)
        + int(manifest["measured_vehicle_data"] is not False)
        + int(manifest["provenance_class"] != "synthetic_protocol_fixture")
    )
    working = [dict(r) for r in nominal]
    wheel_indices = [i for i, r in enumerate(can) if r["can_id"] == "0x139"]
    fault_indices = [wheel_indices[10]] + (
        [wheel_indices[50]] if severity > 1.4 else []
    )
    for index in fault_indices:
        payload = bytearray.fromhex(working[index]["payload_hex"])
        payload[4] ^= 4
        working[index]["payload_hex"] = payload.hex()
    working.insert(wheel_indices[20], dict(working[wheel_indices[20]]))
    detected = anomalies(working)
    if not broken:
        # Recovery is possible only because a valid redundant CAN stream is retained.
        working = [dict(canonical[key]) for key in sorted(canonical)]
    unresolved = anomalies(working)
    time, true_speed, yaw_time, true_yaw = _decode(nominal)
    sample_time, sample_speed, sample_yaw_time, sample_yaw = _decode(working)
    clock_scale = 1 + 0.0008 * severity
    offset = 0.02 * severity
    sync = np.array([0.0, 1.0, 2.0])
    sync_logger = clock_scale * sync + offset
    measured_scale, measured_offset = np.linalg.lstsq(
        np.c_[sync, np.ones(3)], sync_logger, rcond=None
    )[0]

    def align(t):
        recorded = clock_scale * t + offset
        return recorded if broken else (recorded - measured_offset) / measured_scale

    clock_error = float(max(abs(align(sync) - sync)))
    speed_scale = 1 + 0.02 * severity
    speed_bias = 0.2 * severity
    yaw_bias = np.deg2rad(0.5 * severity)
    known = np.array([0.0, 30.0])
    readings = speed_scale * known + speed_bias
    calibration = np.polyfit(readings, known, 1)
    raw_speed = speed_scale * sample_speed + speed_bias
    calibrated_speed = raw_speed if broken else np.polyval(calibration, raw_speed)
    calibrated_yaw = (
        sample_yaw + yaw_bias if broken else sample_yaw + yaw_bias - yaw_bias
    )
    check_raw = speed_scale * 15 + speed_bias
    calibration_error = abs(
        (check_raw if broken else np.polyval(calibration, check_raw)) - 15
    )
    velocity = np.interp(time, align(sample_time), calibrated_speed)
    yaw = np.interp(time, align(sample_yaw_time), calibrated_yaw)
    true_yaw_grid = np.interp(time, yaw_time, true_yaw)
    position = _trajectory(time, velocity, yaw)
    truth = _trajectory(time, true_speed, true_yaw_grid)
    # An explicitly synthetic force channel, not the fixture's inconsistent IMU ax.
    true_acceleration = np.r_[0.0, np.diff(true_speed) / np.diff(time)]
    acceleration = np.r_[0.0, np.diff(velocity) / np.diff(time)]
    force = (
        1450 * true_acceleration
        + 0.45 * true_speed**2
        + 2 * np.sin(0.9 * np.arange(len(time)))
    )
    split = int(np.floor((1 - validation_fraction) * len(time)))
    train = np.c_[acceleration[1:split], velocity[1:split] ** 2]
    target = force[1:split]
    parameters = np.linalg.lstsq(train, target, rcond=None)[0]
    predicted = np.c_[acceleration, velocity**2] @ parameters
    residual = target - train @ parameters
    covariance = (residual @ residual / (len(target) - 2)) * np.linalg.inv(
        train.T @ train
    )
    normalized = train / np.linalg.norm(train, axis=0)
    eigenvalues = np.linalg.eigvalsh(normalized.T @ normalized)
    held_error = float(np.sqrt(np.mean((predicted[split:] - force[split:]) ** 2)))
    speed_error = float(np.sqrt(np.mean((velocity - true_speed) ** 2)))
    closure = float(max(abs(velocity - true_speed)))
    req = {
        "TV-01": _requirement(
            "Raw hashes, provenance and CAN/BLE parity failures",
            provenance,
            "count",
            "<=",
            0,
        ),
        "TV-02": _requirement("Clock sync residual", clock_error, "s", "<=", 1e-9),
        "TV-03": _requirement(
            "Unused calibration speed error", calibration_error, "m/s", "<=", 1e-9
        ),
        "TV-04": _requirement(
            "Reconstructed trajectory endpoint error",
            abs(position[-1] - truth[-1]),
            "m",
            "<=",
            0.05,
        ),
        "TV-05": _requirement(
            "Reconstructed speed RMS error", speed_error, "m/s", "<=", 0.01
        ),
        "TV-06": _requirement(
            "Chronological held-out force RMS", held_error, "N", "<=", 20
        ),
        "TV-07": _requirement(
            "Smallest normalized information eigenvalue",
            min(eigenvalues),
            "1",
            ">=",
            0.001,
        ),
        "TV-08": _requirement(
            "Unresolved corrupt/duplicate packets", unresolved, "count", "<=", 0
        ),
        "TV-09": _requirement(
            "Recovered speed maximum error", closure, "m/s", "<=", 0.01
        ),
    }
    passed = sum(r["passed"] for r in req.values())
    signature = [
        float(passed),
        9.0,
        held_error,
        passed / 9,
        float(detected),
        float(9 - passed),
        float(req["TV-09"]["passed"]),
    ]
    return {
        "signature": signature,
        "requirements": req,
        "time": time,
        "speed": velocity,
        "true_speed": true_speed,
        "force": force,
        "predicted_force": predicted,
        "position": position,
        "true_position": truth,
        "parameters": parameters,
        "covariance": covariance,
        "information_eigenvalues": eigenvalues,
        "split": split,
        "record_count": len(can),
        "fault_indices": fault_indices,
        "detected_anomalies": detected,
        "yaw_rad_s": yaw,
        "clock_fit": [float(measured_scale), float(measured_offset)],
    }


def run(parameters):
    p = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    r = _telemetry(p["validation_fraction"], p["fault_severity"], broken)
    labels = [
        "Requirements passed",
        "Requirements total",
        "Held-out force RMS",
        "Requirement pass fraction",
        "Detected packet anomalies",
        "Failed requirements",
        "Recovery verdict",
    ]
    units = ["count", "count", "N", "fraction", "count", "count", "bool"]
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
                "Reconstructed speed from the protocol replay",
                "Source time (s)",
                "Speed (m/s)",
                [
                    _tr(
                        "Processed",
                        r["time"],
                        r["speed"],
                        "Source time",
                        "s",
                        "Speed",
                        "m/s",
                    ),
                    _tr(
                        "Decoded truth",
                        r["time"],
                        r["true_speed"],
                        "Source time",
                        "s",
                        "Speed",
                        "m/s",
                    ),
                ],
            ),
            "mechanism": _pl(
                "Unseen chronological force prediction",
                "Source time (s)",
                "Force residual (N)",
                [
                    _tr(
                        "Held-out residual",
                        r["time"][r["split"] :],
                        (r["predicted_force"] - r["force"])[r["split"] :],
                        "Source time",
                        "s",
                        "Force residual",
                        "N",
                    )
                ],
            ),
        },
        "explanations": {
            "observation": "The retained synthetic CAN/BLE bytes feed timing, calibration, trajectory, chronological identification, covariance and corruption recovery. The added force channel is explicitly synthetic; no measured-car calibration is claimed.",
            "broken": BROKEN_TEXT,
            "recovery": RECOVERY_TEXT,
        },
        "diagnostics": {
            "item_number": 66,
            "broken_active": broken,
            "signature": r["signature"],
            "requirements": r["requirements"],
            "mass_drag_estimate": r["parameters"].tolist(),
            "parameter_covariance": r["covariance"].tolist(),
            "information_eigenvalues": r["information_eigenvalues"].tolist(),
            "training_stop": r["split"],
            "held_out_start": r["split"],
            "samples": len(r["time"]),
            "record_count": r["record_count"],
            "clock_fit": r["clock_fit"],
            "synthetic_force_channel": True,
            "trajectory_xy_m": np.c_[r["position"].real, r["position"].imag].tolist(),
        },
    }
