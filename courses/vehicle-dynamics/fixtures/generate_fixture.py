from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent

PROTOCOL_SOURCE = {
    "repository": "tranquilWorks/gr86-cca-telemetry",
    "commit": "f5d13fce5fcfc23a914f7da39e5bb448c56ed6b7",
    "tree": "3c4edb0083fa93af8114497c145a7248bafd7ade",
    "files": [
        {
            "path": "firmware/cca_telemetry.ino",
            "sha256": "bd7597f6c6bdcc5f3eff8519d1429d856ab4c2ca3cb6495b8a5cb3d02a686a0b",
            "retained_behavior": "RaceChrono UUIDs and four-byte little-endian CAN identifier followed by zero to eight CAN data bytes",
        },
        {
            "path": "firmware/pidmaps/gr86_2022.h",
            "sha256": "d318c65b3a0d1a381b19ba514fdc43eac974f1420869ea7579d24acba7e4144f",
            "retained_behavior": "GR86 identifier allow-list and forwarding-rate policy",
        },
        {
            "path": "docs/racechrono_preset.md",
            "sha256": "3c3e0aa7c730e46e931249ec9dc5c9b49a967bd19707b98fa2c90893cffc007a",
            "retained_behavior": "Documented big-endian signal byte ranges, scale equations, units, and virtual oil-pressure frame",
        },
    ],
}


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def u16(value: int) -> bytes:
    if not 0 <= value <= 0xFFFF:
        raise ValueError(value)
    return value.to_bytes(2, "big")


def clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


def encode_118(time_s: float) -> bytes:
    accelerating = time_s <= 1.15
    rpm = 2600.0 + 900.0 * time_s if accelerating else 3635.0 - 700.0 * (time_s - 1.15)
    pedal = 58.0 if accelerating else 7.0
    throttle = 52.0 if accelerating else 5.0
    coolant_c = 91.0 + 0.5 * time_s
    intake_c = 28.0 + 0.25 * time_s
    return b"".join(
        [
            u16(round(clamp(rpm, 0.0, 16000.0) * 4.0)),
            bytes(
                [
                    round(clamp(pedal, 0.0, 100.0) * 2.0),
                    round(clamp(throttle, 0.0, 100.0) * 2.0),
                    round(clamp(coolant_c + 40.0, 0.0, 255.0)),
                    round(clamp(intake_c + 40.0, 0.0, 255.0)),
                    0,
                    0,
                ]
            ),
        ]
    )


def speed_profile_kmh(time_s: float) -> float:
    if time_s <= 1.2:
        return 36.0 + 15.0 * time_s
    return 54.0 - 10.0 * (time_s - 1.2)


def encode_139(time_s: float) -> bytes:
    center = speed_profile_kmh(time_s)
    turn = math.sin(math.pi * time_s / 2.0)
    acceleration_slip = 0.7 if time_s < 1.0 else 0.0
    wheel_speeds = [
        center - 0.35 * turn,
        center + 0.35 * turn,
        center - 0.45 * turn + acceleration_slip,
        center + 0.45 * turn + acceleration_slip,
    ]
    return b"".join(u16(round(clamp(speed, 0.0, 511.99) * 128.0)) for speed in wheel_speeds)


def encode_241(time_s: float) -> bytes:
    steer_deg = 22.0 * math.sin(math.pi * time_s / 2.0)
    steer_rate_dps = 11.0 * math.pi * math.cos(math.pi * time_s / 2.0)
    return b"".join(
        [
            u16(round(clamp(steer_deg * 10.0 + 32768.0, 0.0, 65535.0))),
            u16(round(clamp(steer_rate_dps * 10.0 + 32768.0, 0.0, 65535.0))),
            bytes(4),
        ]
    )


def encode_2d2(time_s: float) -> bytes:
    yaw_rate_dps = 9.0 * math.sin(math.pi * time_s / 2.0)
    lateral_g = 0.21 * math.sin(math.pi * time_s / 2.0)
    longitudinal_g = 0.18 if time_s <= 1.15 else -0.14
    return b"".join(
        [
            u16(round(clamp(yaw_rate_dps * 100.0 + 32768.0, 0.0, 65535.0))),
            u16(round(clamp(lateral_g * 256.0 + 32768.0, 0.0, 65535.0))),
            u16(round(clamp(longitudinal_g * 256.0 + 32768.0, 0.0, 65535.0))),
            bytes(2),
        ]
    )


def encode_390(time_s: float) -> bytes:
    pressure_bar = 0.0 if time_s <= 1.15 else min(42.0, 52.0 * (time_s - 1.15))
    return u16(round(pressure_bar * 40.0)) + bytes(6)


def encode_710(time_s: float) -> bytes:
    oil_pressure_psi = 56.0 + 4.0 * math.sin(math.pi * time_s / 2.0)
    return u16(round(oil_pressure_psi * 10.0))


ENCODERS = {
    0x118: encode_118,
    0x139: encode_139,
    0x241: encode_241,
    0x2D2: encode_2d2,
    0x390: encode_390,
    0x710: encode_710,
}


def decode(can_id: int, data: bytes) -> dict[str, dict[str, float | str]]:
    be16 = lambda start: int.from_bytes(data[start : start + 2], "big")
    if can_id == 0x118:
        return {
            "engine_speed": {"value": be16(0) / 4.0, "unit": "rpm"},
            "accelerator_pedal": {"value": data[2] / 2.0, "unit": "%"},
            "throttle_plate": {"value": data[3] / 2.0, "unit": "%"},
            "coolant_temperature": {"value": data[4] - 40.0, "unit": "degC"},
            "intake_air_temperature": {"value": data[5] - 40.0, "unit": "degC"},
        }
    if can_id == 0x139:
        names = ["wheel_speed_fl", "wheel_speed_fr", "wheel_speed_rl", "wheel_speed_rr"]
        return {
            name: {"value": be16(2 * index) / 128.0, "unit": "km/h"}
            for index, name in enumerate(names)
        }
    if can_id == 0x241:
        return {
            "steering_angle": {"value": (be16(0) - 32768.0) / 10.0, "unit": "deg"},
            "steering_rate": {"value": (be16(2) - 32768.0) / 10.0, "unit": "deg/s"},
        }
    if can_id == 0x2D2:
        return {
            "yaw_rate": {"value": (be16(0) - 32768.0) / 100.0, "unit": "deg/s"},
            "lateral_acceleration": {"value": (be16(2) - 32768.0) / 256.0, "unit": "g"},
            "longitudinal_acceleration": {"value": (be16(4) - 32768.0) / 256.0, "unit": "g"},
        }
    if can_id == 0x390:
        return {"brake_master_pressure": {"value": be16(0) / 40.0, "unit": "bar"}}
    if can_id == 0x710:
        return {"oil_pressure": {"value": be16(0) / 10.0, "unit": "psi"}}
    raise ValueError(hex(can_id))


SCHEDULE_DIVISORS = {0x118: 2, 0x139: 1, 0x241: 2, 0x2D2: 3, 0x390: 5, 0x710: 2}
frames: list[dict[str, Any]] = []
for tick in range(101):
    source_time_us = tick * 20_000
    time_s = source_time_us / 1_000_000.0
    for can_id in sorted(ENCODERS):
        if tick % SCHEDULE_DIVISORS[can_id] != 0:
            continue
        data = ENCODERS[can_id](time_s)
        frames.append(
            {
                "sequence": len(frames),
                "source_time_us": source_time_us,
                "can_id": f"0x{can_id:03X}",
                "extended": False,
                "dlc": len(data),
                "data_hex": data.hex().upper(),
                "decoded": decode(can_id, data),
            }
        )

can_path = ROOT / "gr86-can-replay-v1.jsonl"
can_path.write_text("".join(canonical(frame) + "\n" for frame in frames), encoding="utf-8")

ble_records = []
for frame in frames:
    can_id = int(frame["can_id"], 16)
    data = bytes.fromhex(frame["data_hex"])
    payload = can_id.to_bytes(4, "little") + data
    ble_records.append(
        {
            "sequence": frame["sequence"],
            "source_time_us": frame["source_time_us"],
            "service_uuid": "0x1FF8",
            "characteristic_uuid": "0x0001",
            "payload_hex": payload.hex().upper(),
        }
    )

ble_path = ROOT / "racechrono-ble-replay-v1.jsonl"
ble_path.write_text("".join(canonical(record) + "\n" for record in ble_records), encoding="utf-8")

fault_plan = {
    "schema_version": 1,
    "fixture_set_id": "gr86-protocol-replay-v1",
    "operations": [
        {"kind": "drop", "sequence": 37},
        {"kind": "duplicate", "sequence": 52},
        {"kind": "swap_adjacent", "sequences": [71, 72]},
        {"kind": "truncate_payload", "sequence": 89, "remove_tail_bytes": 1},
    ],
    "expected_diagnostics": {
        "missing_sequences": [37, 89],
        "duplicate_sequences": [52],
        "out_of_order_pairs": [[72, 71]],
        "malformed_sequences": [89],
        "recoverable_valid_record_count": len(frames) - 2,
    },
}
fault_path = ROOT / "racechrono-ble-fault-plan-v1.json"
fault_path.write_text(json.dumps(fault_plan, indent=2) + "\n", encoding="utf-8")

generator_path = Path(__file__).resolve()
manifest = {
    "schema_version": 1,
    "fixture_set_id": "gr86-protocol-replay-v1",
    "provenance_class": "synthetic_protocol_fixture",
    "measured_vehicle_data": False,
    "protocol_source": PROTOCOL_SOURCE,
    "generation": {
        "script": generator_path.name,
        "script_sha256": sha256(generator_path),
        "method": "Deterministic analytic two-second acceleration, cornering, and braking profile encoded with documented GR86 signal equations and the firmware CAN-to-BLE packet layout.",
        "randomness": "none",
        "base_tick_us": 20_000,
        "duration_us": 2_000_000,
        "record_count": len(frames),
    },
    "privacy": {
        "classification": "public synthetic engineering data",
        "contains_vin": False,
        "contains_driver_identity": False,
        "contains_real_location": False,
        "contains_precise_route": False,
        "contains_vehicle_capture": False,
    },
    "transport": {
        "can_byte_order": "big-endian per documented signal",
        "ble_service_uuid": "0x1FF8",
        "ble_can_characteristic_uuid": "0x0001",
        "ble_packet": "four-byte little-endian CAN identifier followed by dlc CAN data bytes",
    },
    "files": [
        {"path": can_path.name, "sha256": sha256(can_path), "records": len(frames)},
        {"path": ble_path.name, "sha256": sha256(ble_path), "records": len(ble_records)},
        {"path": fault_path.name, "sha256": sha256(fault_path), "records": 4},
    ],
    "invariants": [
        "CAN and BLE nominal records have identical sequence and source-time order",
        "Each BLE payload equals the CAN identifier encoded little-endian in four bytes followed by the exact CAN data bytes",
        "Every decoded signal uses the documented GR86 RaceChrono byte range, scale, offset, and unit",
        "Nominal source timestamps are monotonic and replay is deterministic",
        "The fault plan deterministically exposes one drop, one duplicate, one adjacent inversion, and one malformed packet",
    ],
    "limitations": [
        "The fixture is generated from protocol documentation and analytic profiles; it is not a captured drive and cannot validate actual vehicle signal identity, timing, calibration, noise, or operating range",
        "No GNSS position or personal/vehicle identifier is present",
        "Firmware execution, BLE radio behavior, CAN electrical behavior, RaceChrono application behavior, bench hardware, and vehicle behavior are not validated",
    ],
}

(ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

print(canonical({"fixture_set_id": manifest["fixture_set_id"], "records": len(frames)}))
