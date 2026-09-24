from __future__ import annotations

import hashlib
import importlib.util
import json
import runpy
import subprocess
from collections import Counter
from itertools import pairwise
from pathlib import Path
from typing import Any

import yaml

from elp_api.catalog import CourseCatalog

ROOT = Path(__file__).resolve().parents[3]
COURSE_ROOT = ROOT / "courses/vehicle-dynamics"
SOURCE_ROOT = ROOT / "courses/vehicle-dynamics-learning"
FIXTURE_ROOT = COURSE_ROOT / "fixtures"

SOURCE_COMMIT = "57264b3ffeb517ee5eb73e8957b9cd190d022457"
SOURCE_TREE = "d9e7267ba02c8d3d836c0ae481b80e91233eb81a"
CURRICULUM_SHA256 = "c452996e5253ec7e547a64cccd4aa8af60dc5f4106311d1dec25ec8d5c48eba6"
SOURCE_FILE_SET_SHA256 = "15de22f8396cf978e80e55f2ed7541234804913c81dbef71cb85c81508472d11"
MAP_SHA256 = "87dae868d7e3a0181062a4fd42ff316513b0f6f35c053cb56b5d73b9c56bde6d"
ACTIVE_CONTRACT_SHA256 = "8aaf80f5f415f152b21812846d49f6d65b41c876164078e83a95a54aa5ce0f34"
FRAMEWORK_SHA256 = {
    "source-map.yaml": "1533c3a5f78447adb3008796530796ade0da18a4c4bda57e565c82548ff4c298",
    "course.yaml": "8b25d17589cb56bf8c1e2501298d092d9db11aeb6a42f5673f956029d15b5681",
}
FIXTURE_SHA256 = {
    "manifest.json": "5727329535dee3906f3c72acc0aed52219ccab0e5db57b688b99025e556a54f8",
    "gr86-can-replay-v1.jsonl": (
        "b4f2239ade6167cbc02331866ea303d2c0abb580f85e068a29527e5e3b712bd3"
    ),
    "racechrono-ble-replay-v1.jsonl": (
        "ac20b5bd3943c5d6d7713617179c57892e5d976e4c5783117971580b4a4de69e"
    ),
    "racechrono-ble-fault-plan-v1.json": (
        "ee278a9360c0b8b38f227b10ea11371b183cfa4c18c7cc984501f4c6b76607d3"
    ),
    "generate_fixture.py": ("b2bd34a621c97dc5d8e7930014ee2d0281166833f43639d621666c230c68015d"),
    "verify_fixture.py": ("508a1a6a73fd4f5af8049eb07abad9f3b11c1a20dc74a9d466ec978db6159b32"),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load(path: Path) -> dict[str, Any]:
    value, _ = CourseCatalog._read_yaml(path)
    return value


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def _git(*args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )


def _decode(can_id: int, data: bytes) -> dict[str, float]:
    def be16(offset: int) -> int:
        return (data[offset] << 8) | data[offset + 1]

    if can_id == 0x118:
        return {
            "engine_speed_rpm": be16(0) * 0.25,
            "accelerator_pedal_percent": data[2] * 0.5,
            "throttle_plate_percent": data[3] * 0.5,
            "coolant_temperature_degC": float(data[4] - 40),
            "intake_air_temperature_degC": float(data[5] - 40),
        }
    if can_id == 0x139:
        return {
            name: be16(2 * index) / 128.0
            for index, name in enumerate(
                (
                    "wheel_speed_fl_kmh",
                    "wheel_speed_fr_kmh",
                    "wheel_speed_rl_kmh",
                    "wheel_speed_rr_kmh",
                )
            )
        }
    if can_id == 0x241:
        return {
            "steering_angle_deg": (be16(0) - 32768) * 0.1,
            "steering_rate_deg_s": (be16(2) - 32768) * 0.1,
        }
    if can_id == 0x2D2:
        return {
            "yaw_rate_deg_s": (be16(0) - 32768) * 0.01,
            "lateral_acceleration_g": (be16(2) - 32768) / 256.0,
            "longitudinal_acceleration_g": (be16(4) - 32768) / 256.0,
        }
    if can_id == 0x390:
        return {"brake_master_pressure_bar": be16(0) * 0.025}
    if can_id == 0x710:
        return {"oil_pressure_psi": be16(0) * 0.1}
    raise AssertionError(f"unexpected CAN identifier {can_id:#x}")


def test_reviewed_map_identity_schema_graph_batches_and_capstones() -> None:
    mapping = _load(COURSE_ROOT / "competency-map.yaml")
    schema = json.loads((COURSE_ROOT / "competency-map.schema.json").read_text(encoding="utf-8"))
    helper_path = ROOT / "apps/api/tests/test_dsp_conversion_framework.py"
    spec = importlib.util.spec_from_file_location("vehicle_schema_helper", helper_path)
    assert spec is not None and spec.loader is not None
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    assert helper._schema_errors(mapping, schema, schema) == []
    assert _sha256(COURSE_ROOT / "competency-map.yaml") == MAP_SHA256

    modules = mapping["modules"]
    module_by_id = {item["id"]: item for item in modules}
    competency_by_id = {item["id"]: item for item in mapping["competencies"]}
    assessment_ids = {item["id"] for item in mapping["assessments"]}
    assert [item["id"] for item in modules] == [f"P{number:02d}" for number in range(1, 68)]
    assert mapping["count_derivation"]["planned_module_count"] == len(modules) == 67
    assert len(competency_by_id) == 15
    assert len(assessment_ids) == 14

    for module in modules:
        number = int(module["id"][1:])
        assert all(int(item[1:]) < number for item in module["depends_on"])
        assert set(module["competency_ids"]) <= set(competency_by_id)
        for competency_id in module["competency_ids"]:
            assert module["id"] in competency_by_id[competency_id]["module_ids"]
    for competency in competency_by_id.values():
        assert set(competency["prerequisite_ids"]) <= set(competency_by_id)
        assert set(competency["module_ids"]) <= set(module_by_id)
        assert set(competency["assessment_ids"]) <= assessment_ids
        for module_id in competency["module_ids"]:
            assert competency["id"] in module_by_id[module_id]["competency_ids"]

    flattened = [module_id for batch in mapping["batch_plan"] for module_id in batch["module_ids"]]
    assert Counter(flattened) == Counter(module_by_id.keys())
    assert [len(item["module_ids"]) for item in mapping["batch_plan"]] == [
        8,
        8,
        8,
        9,
        10,
        9,
        8,
        7,
    ]
    assert [item["id"] for item in mapping["capstones"]] == [
        "CAP-TELEMETRY-VALIDATION",
        "CAP-GR86-DIGITAL-TWIN",
    ]
    assert all(len(item["competency_ids"]) >= 5 for item in mapping["capstones"])


def test_exact_source_map_and_read_only_gitlink() -> None:
    source_map = _load(COURSE_ROOT / "source-map.yaml")
    source = source_map["source"]
    assert source == {
        "repository": "tranquilWorks/vehicle-dynamics-learning",
        "commit": SOURCE_COMMIT,
        "tree": SOURCE_TREE,
        "curriculum": {
            "path": "curriculum/modules.json",
            "sha256": CURRICULUM_SHA256,
        },
        "required_common_files": [
            "README.md",
            "checks.md",
            "experiment.m",
            "lesson.m",
            "lesson.md",
            "walkthrough.md",
        ],
        "implemented_extension_files": ["interactive.m", "model.m", "run_checks.m"],
        "aggregate_file_set_sha256": SOURCE_FILE_SET_SHA256,
        "file_count": 150,
    }
    items = source_map["items"]
    assert [item["id"] for item in items] == [f"P{number:02d}" for number in range(1, 25)]
    assert [item["source_status"] for item in items[:2]] == ["implemented", "implemented"]
    assert {item["source_status"] for item in items[2:]} == {"scaffolded"}
    identities = [identity for item in items for identity in item["files"]]
    assert len(identities) == 150
    assert len({item["path"] for item in identities}) == 150
    framed = "".join(
        f"{item['sha256']}  {item['path']}\n"
        for item in sorted(identities, key=lambda value: value["path"])
    ).encode()
    assert hashlib.sha256(framed).hexdigest() == SOURCE_FILE_SET_SHA256

    staged = _git("ls-files", "--stage", "--", "courses/vehicle-dynamics-learning").stdout
    assert staged.split()[0:2] == ["160000", SOURCE_COMMIT]
    if (SOURCE_ROOT / ".git").exists():
        assert _git("rev-parse", "HEAD", cwd=SOURCE_ROOT).stdout.strip() == SOURCE_COMMIT
        assert _git("rev-parse", "HEAD^{tree}", cwd=SOURCE_ROOT).stdout.strip() == SOURCE_TREE
        assert (
            _git(
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
                cwd=SOURCE_ROOT,
            ).stdout
            == ""
        )
        assert _sha256(SOURCE_ROOT / "curriculum/modules.json") == CURRICULUM_SHA256
        for identity in identities:
            assert _sha256(SOURCE_ROOT / identity["path"]) == identity["sha256"]


def test_conversion_ledgers_record_exact_third_batch_transition() -> None:
    for name, expected in FRAMEWORK_SHA256.items():
        assert _sha256(COURSE_ROOT / name) == expected
    source_map = _load(COURSE_ROOT / "source-map.yaml")
    conversion = _load(COURSE_ROOT / "conversion-manifest.yaml")
    coverage = _load(COURSE_ROOT / "coverage.yaml")
    assert conversion["source_map_sha256"] == FRAMEWORK_SHA256["source-map.yaml"]
    assert coverage["source_map_sha256"] == FRAMEWORK_SHA256["source-map.yaml"]
    assert coverage["summary"] == {
        "total": 24,
        "pending": 0,
        "converted": 24,
        "blocked": 0,
        "placeholder": 0,
    }
    stable_keys = (
        "id",
        "number",
        "source_folder",
        "title",
        "guiding_question",
        "phase",
        "phase_title",
        "source_status",
    )
    for index, (source_item, conversion_item, coverage_item) in enumerate(
        zip(source_map["items"], conversion["items"], coverage["items"], strict=True), 1
    ):
        assert {key: conversion_item[key] for key in stable_keys} == {
            key: source_item[key] for key in stable_keys
        }
        assert coverage_item["status"] == "converted"
        if index <= 8:
            expected_batch = "ELP-VEHICLE-P01-P08"
        elif index <= 16:
            expected_batch = "ELP-VEHICLE-P09-P16"
        else:
            expected_batch = "ELP-VEHICLE-P17-P24"
        assert coverage_item["conversion_record"]["batch_id"] == expected_batch
        assert len(coverage_item["target_content_digest"]) == 64
        assert coverage_item["blocker"] is None
    module_paths = sorted((COURSE_ROOT / "modules").glob("*/module.yaml"))
    assert len([path for path in module_paths if int(path.parent.name[:2]) <= 24]) == 24
    assert len(module_paths) == 52


def test_fixture_identity_provenance_and_privacy_boundary() -> None:
    for name, expected in FIXTURE_SHA256.items():
        assert _sha256(FIXTURE_ROOT / name) == expected
    manifest = json.loads((FIXTURE_ROOT / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["fixture_set_id"] == "gr86-protocol-replay-v1"
    assert manifest["provenance_class"] == "synthetic_protocol_fixture"
    assert manifest["measured_vehicle_data"] is False
    assert manifest["protocol_source"]["repository"] == "tranquilWorks/gr86-cca-telemetry"
    assert manifest["protocol_source"]["commit"] == ("f5d13fce5fcfc23a914f7da39e5bb448c56ed6b7")
    assert manifest["protocol_source"]["tree"] == ("3c4edb0083fa93af8114497c145a7248bafd7ade")
    privacy = manifest["privacy"]
    assert privacy["classification"] == "public synthetic engineering data"
    assert all(value is False for key, value in privacy.items() if key.startswith("contains_"))
    assert manifest["generation"]["randomness"] == "none"
    assert manifest["generation"]["record_count"] == 309


def test_nominal_can_ble_identity_and_independent_raw_decode() -> None:
    can_records = _jsonl(FIXTURE_ROOT / "gr86-can-replay-v1.jsonl")
    ble_records = _jsonl(FIXTURE_ROOT / "racechrono-ble-replay-v1.jsonl")
    assert len(can_records) == len(ble_records) == 309
    assert [item["sequence"] for item in can_records] == list(range(309))
    assert [item["source_time_us"] for item in can_records] == sorted(
        item["source_time_us"] for item in can_records
    )
    decoded: dict[int, dict[str, float]] = {}
    for can_record, ble_record in zip(can_records, ble_records, strict=True):
        can_id = int(can_record["can_id"], 16)
        data = bytes.fromhex(can_record["data_hex"])
        payload = bytes.fromhex(ble_record["payload_hex"])
        assert can_record["sequence"] == ble_record["sequence"]
        assert can_record["source_time_us"] == ble_record["source_time_us"]
        assert can_record["dlc"] == len(data) <= 8
        assert ble_record["service_uuid"] == "0x1FF8"
        assert ble_record["characteristic_uuid"] == "0x0001"
        assert int.from_bytes(payload[:4], "little") == can_id
        assert payload[4:] == data
        decoded[can_record["sequence"]] = _decode(can_id, data)

    # These anchors are decoded from the raw protocol bytes; generated decoded fields
    # are deliberately not consulted by this independent check.
    assert [item["data_hex"] for item in can_records[:6]] == [
        "28A0746883440000",
        "12001200125A125A",
        "8000815A00000000",
        "80008000802E0000",
        "0000000000000000",
        "0230",
    ]
    assert decoded[0] == {
        "engine_speed_rpm": 2600.0,
        "accelerator_pedal_percent": 58.0,
        "throttle_plate_percent": 52.0,
        "coolant_temperature_degC": 91.0,
        "intake_air_temperature_degC": 28.0,
    }
    assert decoded[1] == {
        "wheel_speed_fl_kmh": 36.0,
        "wheel_speed_fr_kmh": 36.0,
        "wheel_speed_rl_kmh": 36.703125,
        "wheel_speed_rr_kmh": 36.703125,
    }
    assert decoded[2] == {"steering_angle_deg": 0.0, "steering_rate_deg_s": 34.6}
    assert decoded[3] == {
        "yaw_rate_deg_s": 0.0,
        "lateral_acceleration_g": 0.0,
        "longitudinal_acceleration_g": 0.1796875,
    }
    assert decoded[4] == {"brake_master_pressure_bar": 0.0}
    assert decoded[5] == {"oil_pressure_psi": 56.0}


def test_fault_plan_has_independently_diagnosed_exact_outcome() -> None:
    can_records = _jsonl(FIXTURE_ROOT / "gr86-can-replay-v1.jsonl")
    corrupted = _jsonl(FIXTURE_ROOT / "racechrono-ble-replay-v1.jsonl")
    fault_plan = json.loads(
        (FIXTURE_ROOT / "racechrono-ble-fault-plan-v1.json").read_text(encoding="utf-8")
    )
    assert fault_plan["operations"] == [
        {"kind": "drop", "sequence": 37},
        {"kind": "duplicate", "sequence": 52},
        {"kind": "swap_adjacent", "sequences": [71, 72]},
        {"kind": "truncate_payload", "sequence": 89, "remove_tail_bytes": 1},
    ]
    corrupted = [item for item in corrupted if item["sequence"] != 37]
    duplicate_index = next(i for i, item in enumerate(corrupted) if item["sequence"] == 52)
    corrupted.insert(duplicate_index + 1, dict(corrupted[duplicate_index]))
    first = next(i for i, item in enumerate(corrupted) if item["sequence"] == 71)
    second = next(i for i, item in enumerate(corrupted) if item["sequence"] == 72)
    corrupted[first], corrupted[second] = corrupted[second], corrupted[first]
    truncated = next(item for item in corrupted if item["sequence"] == 89)
    truncated["payload_hex"] = truncated["payload_hex"][:-2]

    counts = Counter(item["sequence"] for item in corrupted)
    duplicates = sorted(sequence for sequence, count in counts.items() if count > 1)
    out_of_order = [
        [left["sequence"], right["sequence"]]
        for left, right in pairwise(corrupted)
        if left["sequence"] > right["sequence"]
    ]
    can_by_sequence = {item["sequence"]: item for item in can_records}
    malformed = sorted(
        item["sequence"]
        for item in corrupted
        if len(bytes.fromhex(item["payload_hex"])) != 4 + can_by_sequence[item["sequence"]]["dlc"]
    )
    valid_sequences = {item["sequence"] for item in corrupted if item["sequence"] not in malformed}
    missing = sorted(set(range(309)) - valid_sequences)
    assert missing == [37, 89]
    assert duplicates == [52]
    assert out_of_order == [[72, 71]]
    assert malformed == [89]
    assert len(valid_sequences) == 307
    assert fault_plan["expected_diagnostics"] == {
        "missing_sequences": missing,
        "duplicate_sequences": duplicates,
        "out_of_order_pairs": out_of_order,
        "malformed_sequences": malformed,
        "recoverable_valid_record_count": len(valid_sequences),
    }


def test_fixture_verifier_is_generator_independent_and_passes(capsys: Any) -> None:
    verifier = (FIXTURE_ROOT / "verify_fixture.py").read_text(encoding="utf-8")
    assert "import generate_fixture" not in verifier
    assert "from generate_fixture" not in verifier
    runpy.run_path(str(FIXTURE_ROOT / "verify_fixture.py"), run_name="__main__")
    result = json.loads(capsys.readouterr().out)
    assert result == {
        "fault_diagnostics": "passed",
        "fixture_set_id": "gr86-protocol-replay-v1",
        "independent_decode": "passed",
        "nominal_packet_identity": "passed",
        "privacy": "synthetic_no_identifiers",
        "records": 309,
    }


def test_propulsion_depth_catalog_is_six_courses_with_fifty_two_vehicle_modules() -> None:
    catalog = CourseCatalog([ROOT / "courses"])
    summaries = {item.id: item for item in catalog.summaries()}
    assert len(summaries) == 6
    assert sum(len(item.modules) for item in summaries.values()) == 275
    assert (
        sum(module.interactive for course in summaries.values() for module in course.modules) == 275
    )
    assert len(summaries["vehicle-dynamics"].modules) == 52


def test_active_contract_is_exact_merged_propulsion_depth_authorization() -> None:
    contract_path = ROOT / "contracts/active-batch.yaml"
    contract = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    assert _sha256(contract_path) == ACTIVE_CONTRACT_SHA256
    assert contract["batch"]["id"] == "ELP-VEHICLE-PROPULSION-P44-P52"
    assert contract["sources"]["baseline_commit"] == ("e33d1356f15f88c876fb41a482bb3882dcb20783")
    assert contract["sources"]["competency_map_sha256"] == MAP_SHA256
    assert "courses/vehicle-dynamics/modules/44-*/**" in contract["scope"]["allowed_paths"]
    assert "courses/vehicle-dynamics/modules/5[3-9]-*/**" in contract["scope"]["forbidden_paths"]
    assert contract["validation"]["required_ci"] == []
