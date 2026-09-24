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
FIDELITY_BATCH = "ELP-GNC-FIDELITY-P01-P24"
REQUIRED_SOURCE_FILES = (
    "README.md",
    "lesson.md",
    "walkthrough.md",
    "checks.md",
    "experiment.m",
    "interactive.m",
    "lesson.m",
    "model.m",
)
HEX_64 = re.compile(r"^[0-9a-f]{64}$")
GENERIC_AXIS_TITLES = {"Independent variable", "Response", "Diagnostic"}


def _yaml(path: Path) -> dict[str, Any]:
    value, _ = CourseCatalog._read_yaml(path)
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _schema_helper() -> Any:
    helper_path = ROOT / "apps/api/tests/test_dsp_conversion_framework.py"
    spec = importlib.util.spec_from_file_location("elp_gnc_schema_helper", helper_path)
    assert spec is not None and spec.loader is not None
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    return helper


def test_gnc_framework_source_identity_and_exact_map() -> None:
    source_map = _yaml(COURSE_ROOT / "source-map.yaml")
    source = source_map["source"]
    assert source["repository"] == "tranquilWorks/controls-gnc-learning"
    assert source["commit"] == EXPECTED_SOURCE_COMMIT
    assert source["tree"] == EXPECTED_SOURCE_TREE
    assert source["curriculum"] == {
        "path": "curriculum/modules.json",
        "sha256": EXPECTED_CURRICULUM_SHA256,
    }
    assert tuple(source["required_files"]) == REQUIRED_SOURCE_FILES
    assert source["aggregate_file_set_sha256"] == EXPECTED_FILE_SET_SHA256
    assert len(source_map["items"]) == 24
    assert [item["id"] for item in source_map["items"]] == [
        f"P{number:02d}" for number in range(1, 25)
    ]
    assert Counter(item["phase"] for item in source_map["items"]) == {
        1: 4,
        2: 4,
        3: 4,
        4: 4,
        5: 4,
        6: 4,
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


def test_gnc_manifest_and_coverage_are_ordered_complete_inventory() -> None:
    source_map = _yaml(COURSE_ROOT / "source-map.yaml")
    manifest = _yaml(COURSE_ROOT / "conversion-manifest.yaml")
    coverage = _yaml(COURSE_ROOT / "coverage.yaml")
    assert manifest["course_id"] == coverage["course_id"] == "controls-gnc"
    assert (
        manifest["source_map_sha256"]
        == coverage["source_map_sha256"]
        == _sha256(COURSE_ROOT / "source-map.yaml")
    )
    assert coverage["conversion_manifest_sha256"] == _sha256(
        COURSE_ROOT / "conversion-manifest.yaml"
    )
    assert coverage["summary"] == {
        "total": 24,
        "pending": 0,
        "converted": 24,
        "blocked": 0,
        "placeholder": 0,
    }
    assert len(manifest["items"]) == len(coverage["items"]) == 24
    for index, (source, mapped, item) in enumerate(
        zip(source_map["items"], manifest["items"], coverage["items"], strict=True),
        start=1,
    ):
        assert source["number"] == mapped["number"] == item["number"] == index
        assert source["id"] == mapped["id"] == item["id"]
        assert source["source_folder"] == mapped["source_folder"] == item["source_folder"]
        assert item["status"] == "converted"
        assert (COURSE_ROOT / item["conversion_record"]).is_file()
        assert HEX_64.fullmatch(item["target_content_digest"])


def test_gnc_fidelity_map_is_closed_source_bound_and_semantically_distinct() -> None:
    source_map = _yaml(COURSE_ROOT / "source-map.yaml")
    fidelity = _yaml(COURSE_ROOT / "fidelity-map.yaml")
    assert fidelity["source"] == {
        "repository": "tranquilWorks/controls-gnc-learning",
        "commit": EXPECTED_SOURCE_COMMIT,
        "tree": EXPECTED_SOURCE_TREE,
        "curriculum": {
            "path": "curriculum/modules.json",
            "sha256": EXPECTED_CURRICULUM_SHA256,
        },
    }
    assert [item["id"] for item in fidelity["items"]] == [
        f"P{number:02d}" for number in range(1, 25)
    ]
    equation_fingerprints: set[tuple[str, ...]] = set()
    for source, item in zip(source_map["items"], fidelity["items"], strict=True):
        module = _yaml(COURSE_ROOT / item["target_folder"] / "module.yaml")
        source_model = next(
            identity for identity in source["files"] if identity["path"].endswith("/model.m")
        )
        assert item["source_model"] == source_model
        assert item["source_folder"] == item["target_folder"] == source["source_folder"]
        assert [control["platform_control"] for control in item["controls"]] == [
            control["id"] for control in module["controls"]
        ]
        assert [sweep["evidence_case"] for sweep in item["sweeps"]] == [
            "sweep_1",
            "sweep_2",
        ]
        assert all(sweep["one_variable"] is True for sweep in item["sweeps"])
        assert item["broken_case"]["trigger"] == "broken_mode=true"
        assert len(item["limiting_cases"]) >= 2
        assert item["omissions"]
        assert item["reference"]["independent"] is True
        assert item["reference"]["imports_production_entrypoint"] is False
        assert item["reference"]["derived_from_production_output"] is False
        assert item["reference"]["perturbs_production_output"] is False
        assert [plot["key"] for plot in item["plots"]] == ["response", "mechanism"]
        for plot in item["plots"]:
            assert len(plot["axes"]) >= 2
            assert not (GENERIC_AXIS_TITLES & {axis["title"] for axis in plot["axes"]})
        equation_fingerprints.add(tuple(item["state_equations"]))
    assert len(equation_fingerprints) == 24

    p20 = fidelity["items"][19]
    assert "two fixed gains" in p20["teaching_invariant"]
    assert "12 PI candidates" in " ".join(p20["omissions"])
    p24 = fidelity["items"][23]
    assert "cancellation" in " ".join(p24["omissions"]).lower()
    assert "not a capstone" in " ".join(p24["omissions"]).lower()


def test_gnc_independent_reference_has_no_production_execution_path() -> None:
    path = COURSE_ROOT / "reference_cases.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    allowed_imports = {"collections", "typing", "numpy", "scipy", "__future__"}
    forbidden_calls = {"eval", "exec", "compile", "__import__", "run", "import_module"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            assert all(alias.name.split(".")[0] in allowed_imports for alias in node.names)
        if isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".")[0] in allowed_imports
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in forbidden_calls
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            assert not (
                {"actual", "production", "production_result"}
                & {argument.arg for argument in node.args.args}
            )
    assert "experiment.py" in ast.get_docstring(tree, clean=True)


def test_gnc_records_are_schema_valid_bounded_and_fidelity_linked() -> None:
    helper = _schema_helper()
    conversion_schema = helper._load_json(COURSE_ROOT / "conversion.schema.json")
    fidelity_schema = helper._load_json(COURSE_ROOT / "fidelity-map.schema.json")
    fidelity = _yaml(COURSE_ROOT / "fidelity-map.yaml")
    assert conversion_schema["$id"].endswith("controls-gnc-conversion-v2.json")
    assert helper._schema_errors(fidelity, fidelity_schema, fidelity_schema) == []

    coverage = _yaml(COURSE_ROOT / "coverage.yaml")
    forbidden_calls = {"eval", "exec", "compile", "__import__"}
    forbidden_imports = {"subprocess", "socket", "requests", "urllib", "httpx", "pip"}
    for item in coverage["items"]:
        root = COURSE_ROOT / item["target_folder"]
        record = _yaml(root / "conversion.yaml")
        assert helper._schema_errors(record, conversion_schema, conversion_schema) == []
        assert record["schema_version"] == 2
        assert record["target"]["content_digest"] == item["target_content_digest"]
        assert record["fidelity"]["batch_id"] == FIDELITY_BATCH
        assert record["fidelity"]["item_id"] == item["id"]
        assert record["fidelity"]["map"] == {
            "path": "fidelity-map.yaml",
            "sha256": _sha256(COURSE_ROOT / "fidelity-map.yaml"),
        }
        assert record["python_source_equivalence"]["status"] == "passed"
        assert len(record["python_source_equivalence"]["cases"]) == 5
        assert record["matlab_runtime_parity"]["status"] == "not_run"
        assert record["claims"]["learner_effectiveness"]["status"] == "not_run"
        tree = ast.parse((root / "experiment.py").read_text())
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [alias.name.split(".")[0] for alias in node.names]
                assert not (set(names) & forbidden_imports)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                assert node.func.id not in forbidden_calls


def test_gnc_final_catalog_shape() -> None:
    catalog = CourseCatalog([ROOT / "courses"])
    courses = catalog.summaries()
    assert len(courses) == 6
    modules = sum(len(course.modules) for course in courses)
    interactive = sum(module.interactive for course in courses for module in course.modules)
    robotics_expansion = _yaml(ROOT / "courses/robotics-autonomy/expansion-map.yaml")
    robotics_native = len(robotics_expansion["implemented_native_modules"])
    assert (modules, interactive) == (221 + robotics_native, 221 + robotics_native)
    gnc = next(course for course in courses if course.id == "controls-gnc")
    assert len(gnc.modules) == 68


def test_p24_is_explicitly_software_only_and_not_a_capstone() -> None:
    root = COURSE_ROOT / "modules/24-close-the-loop-through-a-hardware-in-the-loop-plant"
    combined = ((root / "lesson.md").read_text() + (root / "conversion.yaml").read_text()).lower()
    assert "software-only" in combined
    assert "does not claim physical hil" in combined or "no physical hil is claimed" in combined
    assert "not a capstone" in combined
