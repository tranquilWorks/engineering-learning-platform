from __future__ import annotations

import ast
import hashlib
import importlib.util
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from elp_api.catalog import CourseCatalog

ROOT = Path(__file__).resolve().parents[3]
COURSE_ROOT = ROOT / "courses" / "robotics-autonomy"
SOURCE_ROOT = ROOT / "courses" / "robotics-autonomy-learning"
EXPECTED_SOURCE_COMMIT = "f8807640258f1a6c1c77f1dcc9e61734551c585b"
EXPECTED_SOURCE_TREE = "7f8bc62382ca8d7fbe26ff4413cabf7d00d64bb9"
EXPECTED_CURRICULUM_SHA256 = "972eee6b99945f6c2380ba097e443b30c37ca9e4e0acfd2c7f7cde8a7550207d"
EXPECTED_FILE_SET_SHA256 = "f8f2fe6aff1bfa3e63013279b1b2d5e3e8fe86f2c064555183d8e5a8380e7551"
HEX_64 = re.compile(r"^[0-9a-f]{64}$")


def _yaml(path: Path) -> dict[str, Any]:
    value, _ = CourseCatalog._read_yaml(path)
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


SOURCE_MAP = _yaml(COURSE_ROOT / "source-map.yaml")
MANIFEST = _yaml(COURSE_ROOT / "conversion-manifest.yaml")
COVERAGE = _yaml(COURSE_ROOT / "coverage.yaml")


def test_robotics_source_identity_and_exact_24_item_map() -> None:
    source = SOURCE_MAP["source"]
    assert source == {
        "repository": "tranquilWorks/robotics-autonomy-learning",
        "commit": EXPECTED_SOURCE_COMMIT,
        "tree": EXPECTED_SOURCE_TREE,
        "curriculum": {
            "path": "curriculum/modules.json",
            "sha256": EXPECTED_CURRICULUM_SHA256,
        },
        "item_file_policy": "all committed files in each source module folder",
        "aggregate_file_set_sha256": EXPECTED_FILE_SET_SHA256,
    }
    assert [item["id"] for item in SOURCE_MAP["items"]] == [
        f"P{number:02d}" for number in range(1, 25)
    ]
    assert [item["number"] for item in SOURCE_MAP["items"]] == list(range(1, 25))
    assert Counter(item["phase"] for item in SOURCE_MAP["items"]) == {
        1: 4,
        2: 4,
        3: 4,
        4: 4,
        5: 4,
        6: 4,
    }
    assert SOURCE_MAP["items"][0]["source_status"] == "implemented"
    assert all(item["source_status"] == "scaffolded" for item in SOURCE_MAP["items"][1:])
    assert len(SOURCE_MAP["items"][0]["files"]) == 9
    assert all(len(item["files"]) == 6 for item in SOURCE_MAP["items"][1:])
    for item in SOURCE_MAP["items"]:
        for identity in item["files"]:
            assert HEX_64.fullmatch(identity["sha256"])


def test_robotics_source_attestation_when_available_and_clean_gitlink() -> None:
    listing = subprocess.run(
        ["git", "ls-files", "-s", "courses/robotics-autonomy-learning"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.split()
    assert listing[:3] == ["160000", EXPECTED_SOURCE_COMMIT, "0"]
    if not (SOURCE_ROOT / "curriculum/modules.json").is_file():
        return

    assert _sha256(SOURCE_ROOT / "curriculum/modules.json") == EXPECTED_CURRICULUM_SHA256
    for item in SOURCE_MAP["items"]:
        for identity in item["files"]:
            assert _sha256(SOURCE_ROOT / identity["path"]) == identity["sha256"]
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=SOURCE_ROOT,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()
    dirty = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=SOURCE_ROOT,
        check=True,
        text=True,
        capture_output=True,
    ).stdout
    assert head == EXPECTED_SOURCE_COMMIT
    assert dirty == ""


def test_robotics_manifest_and_coverage_are_one_ordered_authored_prefix() -> None:
    source_hash = _sha256(COURSE_ROOT / "source-map.yaml")
    manifest_hash = _sha256(COURSE_ROOT / "conversion-manifest.yaml")
    schema_hash = _sha256(COURSE_ROOT / "verification.schema.json")
    assert MANIFEST["source_map_sha256"] == COVERAGE["source_map_sha256"] == source_hash
    assert MANIFEST["verification_schema_sha256"] == schema_hash
    assert COVERAGE["conversion_manifest_sha256"] == manifest_hash
    assert MANIFEST["authored_prefix"] == [f"P{number:02d}" for number in range(1, 25)]
    assert COVERAGE["summary"] == {
        "total": 24,
        "authored": 24,
        "remaining": 0,
        "blocked": 0,
        "placeholder": 0,
    }
    assert [item["status"] for item in COVERAGE["items"]] == ["authored"] * 24
    for number, (source, mapped, covered) in enumerate(
        zip(SOURCE_MAP["items"], MANIFEST["items"], COVERAGE["items"], strict=True),
        start=1,
    ):
        assert source["id"] == mapped["id"] == covered["id"] == f"P{number:02d}"
        assert source["source_folder"] == mapped["source_folder"] == covered["source_folder"]
        assert mapped["target_module_id"] and mapped["verification_record"]
        assert HEX_64.fullmatch(mapped["target_content_digest"])
        assert mapped["target_content_digest"] == covered["target_content_digest"]
        assert mapped["verification_sha256"] == _sha256(COURSE_ROOT / mapped["verification_record"])


def test_robotics_records_are_closed_honest_and_runtime_bounded() -> None:
    helper_path = ROOT / "apps/api/tests/test_dsp_conversion_framework.py"
    spec = importlib.util.spec_from_file_location("elp_schema_helper", helper_path)
    assert spec is not None and spec.loader is not None
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    schema = helper._load_json(COURSE_ROOT / "verification.schema.json")
    forbidden_imports = {"httpx", "pip", "requests", "socket", "subprocess", "urllib"}
    forbidden_calls = {"__import__", "compile", "eval", "exec"}

    for number, mapped in enumerate(MANIFEST["items"], start=1):
        module_root = COURSE_ROOT / mapped["target_folder"]
        record = _yaml(module_root / "verification.yaml")
        assert helper._schema_errors(record, schema, schema) == []
        assert record["item"]["source_inputs"] == SOURCE_MAP["items"][number - 1]["files"]
        assert record["target"]["content_digest"] == mapped["target_content_digest"]
        assert record["matlab_runtime_parity"]["status"] == "not_run"
        if number == 1:
            assert record["item"]["design_basis"] == "implemented_source_design"
            assert record["python_verification"]["basis"] == "source_design"
        else:
            assert record["item"]["design_basis"] == "native_python_design"
            assert record["python_verification"]["basis"] == "native_python_reference"
        assert len(record["python_verification"]["cases"]) == 2
        assert record["runtime"]["max_samples"] <= 12001
        assert record["runtime"]["max_output_bytes"] <= 1_000_000

        tree = ast.parse((module_root / "experiment.py").read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = {alias.name.split(".")[0] for alias in node.names}
                assert not (names & forbidden_imports)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                assert node.func.id not in forbidden_calls


def test_reference_oracle_is_independent_and_native_lessons_are_not_placeholders() -> None:
    oracle_tree = ast.parse((COURSE_ROOT / "reference_cases.py").read_text(encoding="utf-8"))
    imported = {
        alias.name
        for node in ast.walk(oracle_tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    assert not any("experiment" in name for name in imported)
    for mapped in MANIFEST["items"]:
        lesson = (COURSE_ROOT / mapped["target_folder"] / "lesson.md").read_text().lower()
        experiment = (COURSE_ROOT / mapped["target_folder"] / "experiment.py").read_text().lower()
        assert "todo" not in lesson
        assert "scaffolded and intentionally refuses" not in lesson
        assert "not implemented" not in experiment


def test_robotics_final_catalog_shape() -> None:
    catalog = CourseCatalog([ROOT / "courses"])
    courses = catalog.summaries()
    assert len(courses) == 5
    modules = sum(len(course.modules) for course in courses)
    interactive = sum(module.interactive for course in courses for module in course.modules)
    assert (modules, interactive) == (178, 178)
    robotics = next(course for course in courses if course.id == "robotics-autonomy")
    assert [module.number for module in robotics.modules] == list(range(1, 25))
