from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[3]
COURSE_ROOT = ROOT / "courses/robotics-autonomy"


def _yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


MAP = _yaml(COURSE_ROOT / "competency-map.yaml")
DEPTH = _yaml(COURSE_ROOT / "depth-review.yaml")


def test_robotics_competency_map_schema_count_and_order() -> None:
    schema = json.loads((COURSE_ROOT / "competency-map.schema.json").read_text(encoding="utf-8"))
    helper_path = ROOT / "apps/api/tests/test_dsp_conversion_framework.py"
    spec = importlib.util.spec_from_file_location("elp_schema_helper", helper_path)
    assert spec is not None and spec.loader is not None
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    assert helper._schema_errors(MAP, schema, schema) == []
    modules = MAP["modules"]
    assert [item["id"] for item in modules] == [f"P{number:02d}" for number in range(1, 70)]
    assert MAP["count_derivation"]["planned_module_count"] == len(modules) == 69
    assert "not normalized" in MAP["count_derivation"]["rationale"]


def test_robotics_competency_references_close() -> None:
    modules = {item["id"] for item in MAP["modules"]}
    competencies = {item["id"] for item in MAP["competencies"]}
    assessments = {item["id"] for item in MAP["assessments"]}
    for item in MAP["modules"]:
        assert set(item["depends_on"]) < modules | {item["id"]}
        assert set(item["competency_ids"]) <= competencies
    for item in MAP["competencies"]:
        assert set(item["prerequisite_ids"]) <= competencies
        assert set(item["module_ids"]) <= modules
        assert set(item["assessment_ids"]) <= assessments


def test_robotics_batches_are_bounded_and_cover_the_reviewed_map() -> None:
    flattened = [module_id for batch in MAP["batch_plan"] for module_id in batch["module_ids"]]
    assert set(flattened) == {item["id"] for item in MAP["modules"]}
    assert all(1 <= len(batch["module_ids"]) <= 10 for batch in MAP["batch_plan"])
    retained = {f"P{number:02d}" for number in range(1, 25)}
    assert len([module_id for module_id in flattened if module_id in retained]) == 24


def test_robotics_capstones_integrate_multiple_prior_competencies() -> None:
    assert [item["id"] for item in MAP["capstones"]] == [
        "CAP-MOBILE-AUTONOMY",
        "CAP-TWO-LINK-MANIPULATION",
    ]
    for capstone in MAP["capstones"]:
        assert len(capstone["competency_ids"]) >= 5
        assert len(capstone["integration_claim"].split()) >= 20


def test_every_retained_module_has_a_specific_depth_disposition() -> None:
    assert DEPTH["summary"] == {
        "retained_modules": 24,
        "dispositioned": 24,
        "deepen_in_place": 24,
        "runtime_changes_planned": 0,
        "minimum_additions_per_lesson": 5,
    }
    assert [item["id"] for item in DEPTH["items"]] == [f"P{number:02d}" for number in range(1, 25)]
    derivations: set[str] = set()
    failures: set[str] = set()
    for item in DEPTH["items"]:
        assert item["disposition"] == "deepen_in_place"
        assert item["baseline_word_count"] >= 350
        assert len(item["baseline_lesson_sha256"]) == 64
        additions = item["required_additions"]
        assert set(additions) == {
            "derivation_and_conventions",
            "alternative_or_limiting_comparison",
            "practical_failure_analysis",
            "formative_check",
            "cross_course_boundary",
        }
        assert all(len(value.split()) >= 4 for value in additions.values())
        derivations.add(additions["derivation_and_conventions"])
        failures.add(additions["practical_failure_analysis"])
    assert len(derivations) == len(failures) == 24
