from __future__ import annotations

import ast
import hashlib
import importlib.util
import os
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from elp_api.catalog import CourseCatalog

ROOT = Path(__file__).resolve().parents[3]
COURSE_ROOT = ROOT / "courses" / "controls-gnc"
SOURCE_ROOT = ROOT / "courses" / "controls-gnc-learning"

EXPECTED_SOURCE_COMMIT = "ffd6623ee2cf8ccd8599fffd935ef07370750fa3"
EXPECTED_SOURCE_TREE = "471a0afead6f44e875627e7ffe9c088c23f784db"
EXPECTED_CURRICULUM_SHA256 = "8763981e20d02a88450956682b4daff9ee0d74bfed5f0ad91b08715f16aea930"
EXPECTED_FILE_SET_SHA256 = "020ab18235d933cad94aa1c19b2d107b0f3a7ef409458b64f8ed38a9f408afbe"
REQUIRED_SOURCE_FILES = (
    "README.md", "lesson.md", "walkthrough.md", "checks.md",
    "experiment.m", "interactive.m", "lesson.m", "model.m",
)
HEX_64 = re.compile(r"^[0-9a-f]{64}$")


def _yaml(path: Path) -> dict[str, Any]:
    value, _ = CourseCatalog._read_yaml(path)
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_gnc_framework_source_identity_and_exact_map() -> None:
    source_map = _yaml(COURSE_ROOT / "source-map.yaml")
    source = source_map["source"]
    assert source["repository"] == "kpbianco/controls-gnc-learning"
    assert source["commit"] == EXPECTED_SOURCE_COMMIT
    assert source["tree"] == EXPECTED_SOURCE_TREE
    assert source["curriculum"] == {
        "path": "curriculum/modules.json", "sha256": EXPECTED_CURRICULUM_SHA256
    }
    assert tuple(source["required_files"]) == REQUIRED_SOURCE_FILES
    assert source["aggregate_file_set_sha256"] == EXPECTED_FILE_SET_SHA256
    assert len(source_map["items"]) == 24
    assert [item["id"] for item in source_map["items"]] == [
        f"P{number:02d}" for number in range(1, 25)
    ]
    assert Counter(item["phase"] for item in source_map["items"]) == {
        1: 4, 2: 4, 3: 4, 4: 4, 5: 4, 6: 4
    }

    for item in source_map["items"]:
        assert len(item["files"]) == 8
        assert [Path(identity["path"]).name for identity in item["files"]] == list(
            REQUIRED_SOURCE_FILES
        )
        for identity in item["files"]:
            assert HEX_64.fullmatch(identity["sha256"])


def test_gnc_source_attestation_when_requested() -> None:
    configured = os.environ.get("ELP_GNC_SOURCE_ROOT")
    if not configured:
        return
    source_root = Path(configured)
    source_map = _yaml(COURSE_ROOT / "source-map.yaml")
    assert _sha256(source_root / "curriculum/modules.json") == EXPECTED_CURRICULUM_SHA256
    for item in source_map["items"]:
        for identity in item["files"]:
            assert _sha256(source_root / identity["path"]) == identity["sha256"]


def test_gnc_gitlink_is_exact_and_source_checkout_is_clean() -> None:
    listing = subprocess.run(
        ["git", "ls-files", "-s", "courses/controls-gnc-learning"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.split()
    assert listing[:3] == ["160000", EXPECTED_SOURCE_COMMIT, "0"]

    if (SOURCE_ROOT / ".git").exists():
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=SOURCE_ROOT,
            check=True,
            text=True,
            capture_output=True,
        ).stdout.strip()
        dirty = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=SOURCE_ROOT,
            check=True,
            text=True,
            capture_output=True,
        ).stdout
        assert head == EXPECTED_SOURCE_COMMIT
        assert dirty == ""


def test_gnc_manifest_and_coverage_are_ordered_retained_prefix() -> None:
    source_map = _yaml(COURSE_ROOT / "source-map.yaml")
    manifest = _yaml(COURSE_ROOT / "conversion-manifest.yaml")
    coverage = _yaml(COURSE_ROOT / "coverage.yaml")
    assert manifest["course_id"] == coverage["course_id"] == "controls-gnc"
    assert manifest["source_map_sha256"] == coverage["source_map_sha256"] == _sha256(
        COURSE_ROOT / "source-map.yaml"
    )
    assert coverage["conversion_manifest_sha256"] == _sha256(
        COURSE_ROOT / "conversion-manifest.yaml"
    )
    assert len(manifest["items"]) == len(coverage["items"]) == 24
    statuses = [item["status"] for item in coverage["items"]]
    converted = statuses.count("converted")
    assert statuses == ["converted"] * converted + ["pending"] * (24 - converted)
    assert coverage["summary"] == {
        "total": 24, "pending": 24 - converted, "converted": converted,
        "blocked": 0, "placeholder": 0,
    }
    for index, (source, mapped, item) in enumerate(
        zip(source_map["items"], manifest["items"], coverage["items"], strict=True), start=1
    ):
        assert source["number"] == mapped["number"] == item["number"] == index
        assert source["id"] == mapped["id"] == item["id"]
        assert source["source_folder"] == mapped["source_folder"] == item["source_folder"]
        if item["status"] == "converted":
            assert (COURSE_ROOT / item["conversion_record"]).is_file()
            assert HEX_64.fullmatch(item["target_content_digest"])


def test_gnc_converted_records_and_runtime_sources_are_bounded() -> None:
    coverage = _yaml(COURSE_ROOT / "coverage.yaml")
    forbidden_calls = {"eval", "exec", "compile", "__import__"}
    forbidden_imports = {"subprocess", "socket", "requests", "urllib", "httpx", "pip"}
    for item in coverage["items"]:
        if item["status"] != "converted":
            continue
        root = COURSE_ROOT / item["target_folder"]
        record = _yaml(root / "conversion.yaml")
        assert record["schema_version"] == 1
        assert record["course_id"] == "controls-gnc"
        assert record["item"]["id"] == item["id"]
        assert record["target"]["content_digest"] == item["target_content_digest"]
        assert record["python_source_equivalence"]["status"] == "passed"
        assert record["matlab_runtime_parity"]["status"] == "not_run"
        assert record["claims"]["learner_effectiveness"]["status"] == "not_run"
        tree = ast.parse((root / "experiment.py").read_text())
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [alias.name.split(".")[0] for alias in node.names]
                assert not (set(names) & forbidden_imports)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                assert node.func.id not in forbidden_calls


def test_gnc_closed_schema_accepts_every_converted_record() -> None:
    helper_path = ROOT / "apps/api/tests/test_dsp_conversion_framework.py"
    helper_spec = importlib.util.spec_from_file_location("elp_schema_test_helper", helper_path)
    assert helper_spec is not None and helper_spec.loader is not None
    helper = importlib.util.module_from_spec(helper_spec)
    helper_spec.loader.exec_module(helper)

    schema = helper._load_json(COURSE_ROOT / "conversion.schema.json")
    assert schema["$id"].endswith("controls-gnc-conversion-v1.json")
    assert schema["properties"]["course_id"]["const"] == "controls-gnc"
    assert schema["$defs"]["itemIdentity"]["properties"]["source_inputs"]["minItems"] == 8
    assert schema["$defs"]["claims"]["properties"]["profile"]["const"] == "elp-gnc-item-software-v1"

    coverage = _yaml(COURSE_ROOT / "coverage.yaml")
    for item in coverage["items"]:
        if item["status"] != "converted":
            continue
        record = _yaml(COURSE_ROOT / item["conversion_record"])
        assert helper._schema_errors(record, schema, schema) == []


def test_gnc_final_catalog_shape_when_complete() -> None:
    coverage = _yaml(COURSE_ROOT / "coverage.yaml")
    if coverage["summary"]["converted"] != 24:
        return
    catalog = CourseCatalog([ROOT / "courses"])
    courses = catalog.summaries()
    assert len(courses) == 4
    modules = sum(len(course.modules) for course in courses)
    interactive = sum(module.interactive for course in courses for module in course.modules)
    assert (modules, interactive) == (110, 110)
    gnc = next(course for course in courses if course.id == "controls-gnc")
    assert len(gnc.modules) == 24


def test_p24_is_explicitly_software_only() -> None:
    coverage = _yaml(COURSE_ROOT / "coverage.yaml")
    p24 = coverage["items"][23]
    if p24["status"] != "converted":
        return
    root = COURSE_ROOT / p24["target_folder"]
    combined = (
        (root / "lesson.md").read_text().lower()
        + (root / "conversion.yaml").read_text().lower()
    )
    assert "software-only" in combined
    assert (
        "does not claim physical hil" in combined
        or "no physical hardware execution is claimed" in combined
    )
