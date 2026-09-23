from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def decode(can_id: int, data: bytes) -> dict[str, dict[str, float | str]]:
    def be16(offset: int) -> int:
        return (data[offset] << 8) | data[offset + 1]

    if can_id == 0x118:
        return {
            "engine_speed": {"value": be16(0) * 0.25, "unit": "rpm"},
            "accelerator_pedal": {"value": data[2] * 0.5, "unit": "%"},
            "throttle_plate": {"value": data[3] * 0.5, "unit": "%"},
            "coolant_temperature": {"value": float(data[4] - 40), "unit": "degC"},
            "intake_air_temperature": {"value": float(data[5] - 40), "unit": "degC"},
        }
    if can_id == 0x139:
        names = ["wheel_speed_fl", "wheel_speed_fr", "wheel_speed_rl", "wheel_speed_rr"]
        return {
            name: {"value": be16(2 * index) * (1.0 / 128.0), "unit": "km/h"}
            for index, name in enumerate(names)
        }
    if can_id == 0x241:
        return {
            "steering_angle": {"value": (be16(0) - 32768) * 0.1, "unit": "deg"},
            "steering_rate": {"value": (be16(2) - 32768) * 0.1, "unit": "deg/s"},
        }
    if can_id == 0x2D2:
        return {
            "yaw_rate": {"value": (be16(0) - 32768) * 0.01, "unit": "deg/s"},
            "lateral_acceleration": {"value": (be16(2) - 32768) * (1.0 / 256.0), "unit": "g"},
            "longitudinal_acceleration": {"value": (be16(4) - 32768) * (1.0 / 256.0), "unit": "g"},
        }
    if can_id == 0x390:
        return {"brake_master_pressure": {"value": be16(0) * 0.025, "unit": "bar"}}
    if can_id == 0x710:
        return {"oil_pressure": {"value": be16(0) * 0.1, "unit": "psi"}}
    raise AssertionError(hex(can_id))


manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
assert manifest["schema_version"] == 1
assert manifest["fixture_set_id"] == "gr86-protocol-replay-v1"
assert manifest["provenance_class"] == "synthetic_protocol_fixture"
assert manifest["measured_vehicle_data"] is False
assert manifest["protocol_source"]["commit"] == "f5d13fce5fcfc23a914f7da39e5bb448c56ed6b7"
assert manifest["protocol_source"]["tree"] == "3c4edb0083fa93af8114497c145a7248bafd7ade"
assert manifest["generation"]["script_sha256"] == sha256(ROOT / "generate_fixture.py")
assert all(value is False for key, value in manifest["privacy"].items() if key.startswith("contains_"))
for item in manifest["files"]:
    assert item["sha256"] == sha256(ROOT / item["path"])

can = read_jsonl(ROOT / "gr86-can-replay-v1.jsonl")
ble = read_jsonl(ROOT / "racechrono-ble-replay-v1.jsonl")
assert len(can) == len(ble) == manifest["generation"]["record_count"] == 309
assert [item["sequence"] for item in can] == list(range(309))
assert [item["sequence"] for item in ble] == list(range(309))
assert [item["source_time_us"] for item in can] == sorted(item["source_time_us"] for item in can)

for can_record, ble_record in zip(can, ble, strict=True):
    assert can_record["sequence"] == ble_record["sequence"]
    assert can_record["source_time_us"] == ble_record["source_time_us"]
    assert ble_record["service_uuid"] == "0x1FF8"
    assert ble_record["characteristic_uuid"] == "0x0001"
    can_id = int(can_record["can_id"], 16)
    data = bytes.fromhex(can_record["data_hex"])
    assert can_record["dlc"] == len(data) <= 8
    payload = bytes.fromhex(ble_record["payload_hex"])
    assert len(payload) == 4 + len(data)
    assert int.from_bytes(payload[:4], "little") == can_id
    assert payload[4:] == data
    actual = decode(can_id, data)
    assert actual.keys() == can_record["decoded"].keys()
    for signal, measured in actual.items():
        expected = can_record["decoded"][signal]
        assert measured["unit"] == expected["unit"]
        assert abs(float(measured["value"]) - float(expected["value"])) <= 1.0e-12

fault_plan = json.loads((ROOT / "racechrono-ble-fault-plan-v1.json").read_text(encoding="utf-8"))
corrupted = list(ble)
for operation in fault_plan["operations"]:
    if operation["kind"] == "drop":
        corrupted = [item for item in corrupted if item["sequence"] != operation["sequence"]]
    elif operation["kind"] == "duplicate":
        index = next(i for i, item in enumerate(corrupted) if item["sequence"] == operation["sequence"])
        corrupted.insert(index + 1, dict(corrupted[index]))
    elif operation["kind"] == "swap_adjacent":
        first, second = operation["sequences"]
        first_index = next(i for i, item in enumerate(corrupted) if item["sequence"] == first)
        second_index = next(i for i, item in enumerate(corrupted) if item["sequence"] == second)
        corrupted[first_index], corrupted[second_index] = corrupted[second_index], corrupted[first_index]
    elif operation["kind"] == "truncate_payload":
        record = next(item for item in corrupted if item["sequence"] == operation["sequence"])
        remove_hex = 2 * operation["remove_tail_bytes"]
        record["payload_hex"] = record["payload_hex"][:-remove_hex]
    else:
        raise AssertionError(operation)

duplicates = sorted(
    sequence for sequence in {item["sequence"] for item in corrupted}
    if sum(item["sequence"] == sequence for item in corrupted) > 1
)
out_of_order = [
    [first["sequence"], second["sequence"]]
    for first, second in zip(corrupted, corrupted[1:])
    if first["sequence"] > second["sequence"]
]
malformed = []
valid_by_sequence: dict[int, dict[str, Any]] = {}
can_by_sequence = {item["sequence"]: item for item in can}
for item in corrupted:
    expected_dlc = can_by_sequence[item["sequence"]]["dlc"]
    if len(bytes.fromhex(item["payload_hex"])) != 4 + expected_dlc:
        malformed.append(item["sequence"])
        continue
    valid_by_sequence.setdefault(item["sequence"], item)
missing = sorted(set(range(309)) - set(valid_by_sequence))
expected = fault_plan["expected_diagnostics"]
assert missing == expected["missing_sequences"]
assert duplicates == expected["duplicate_sequences"]
assert out_of_order == expected["out_of_order_pairs"]
assert sorted(malformed) == expected["malformed_sequences"]
assert len(valid_by_sequence) == expected["recoverable_valid_record_count"]
assert [item["sequence"] for item in sorted(valid_by_sequence.values(), key=lambda row: row["sequence"])] == [
    sequence for sequence in range(309) if sequence not in expected["missing_sequences"]
]

print(
    json.dumps(
        {
            "fixture_set_id": manifest["fixture_set_id"],
            "records": len(can),
            "nominal_packet_identity": "passed",
            "independent_decode": "passed",
            "fault_diagnostics": "passed",
            "privacy": "synthetic_no_identifiers",
        },
        sort_keys=True,
    )
)
