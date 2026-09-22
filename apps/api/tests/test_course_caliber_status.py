from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[3]
STATUS_PATH = ROOT / "docs" / "course-caliber-status.yaml"

MATURITY_STATES = [
    "source_authored",
    "platform_converted",
    "numerically_verified",
    "curriculum_covered",
    "capstone_integrated",
    "learner_validated",
]
RUBRIC_DIMENSIONS = [
    "foundations_prerequisites",
    "breadth_sequencing",
    "derivation_physical_meaning",
    "unique_executable_fidelity",
    "sweeps_limits_failure_recovery",
    "independent_evidence",
    "formative_cumulative_assessment",
    "capstones",
    "exclusions_cross_course_handoffs",
]


def _status() -> dict[str, Any]:
    value = yaml.safe_load(STATUS_PATH.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _review_by_id(status: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {review["course_id"]: review for review in status["course_reviews"]}


def _validate_authorization(candidate: dict[str, Any], status: dict[str, Any]) -> None:
    policies = status["policies"]
    conversion = policies["conversion_authorization"]
    evidence = candidate["independent_evidence"]

    if not candidate.get("competency_map_validated"):
        raise ValueError("reviewed competency mapping is required")
    if candidate.get("count_source") != conversion["count_source"]:
        raise ValueError("module count must be derived from the competency matrix")
    if candidate.get("new_lessons", 0) > policies["batching"]["max_new_lessons"]:
        raise ValueError("implementation batch exceeds the ten-lesson limit")
    if not candidate.get("coherent_unit"):
        raise ValueError("implementation batch must be a coherent unit")
    if not evidence.get("origin_metadata"):
        raise ValueError("independent evidence requires origin metadata")
    if evidence.get("imports_production_entrypoint"):
        raise ValueError("independent evidence imports the production entrypoint")
    if evidence.get("derived_from_production_output"):
        raise ValueError("independent evidence derives from production output")
    if evidence.get("perturbs_production_output"):
        raise ValueError("independent evidence perturbs production output")


def _valid_authorization() -> dict[str, Any]:
    return {
        "competency_map_validated": True,
        "count_source": "competency_to_module_matrix",
        "new_lessons": 8,
        "coherent_unit": True,
        "independent_evidence": {
            "origin_metadata": "closed-form conservation-law oracle",
            "imports_production_entrypoint": False,
            "derived_from_production_output": False,
            "perturbs_production_output": False,
        },
    }


def test_status_has_closed_top_level_shape_and_exact_standard_identity() -> None:
    status = _status()
    assert set(status) == {
        "schema_version",
        "standard",
        "count_semantics",
        "maturity_states",
        "rubric_dimensions",
        "policies",
        "course_reviews",
        "holds",
    }
    assert status["schema_version"] == 1
    assert status["standard"] == {
        "id": "ELP-COURSE-CALIBER-1",
        "effective_date": "2026-09-21",
        "control_repository": "tranquilWorks/portfolio-control",
        "control_revision": "755c418c5b4f1fbccae77fa1695ce39a60d68cad",
        "audit_baseline": "1506591946ec8e96fe3201e8893b8ad851a1685a",
    }
    assert status["count_semantics"] == (
        "implementation_inventory_not_curriculum_completeness"
    )


def test_exact_ordered_states_and_nine_dimension_rubric_are_projected() -> None:
    status = _status()
    assert [state["id"] for state in status["maturity_states"]] == MATURITY_STATES
    assert status["rubric_dimensions"] == RUBRIC_DIMENSIONS
    for state in status["maturity_states"]:
        assert set(state) == {"id", "definition", "required_evidence"}
        assert state["definition"].strip()
        assert state["required_evidence"].strip()


def test_reviewed_course_dispositions_keep_inventory_separate_from_maturity() -> None:
    status = _status()
    reviews = _review_by_id(status)
    assert list(reviews) == ["dsp-radar", "controls-gnc", "robotics-autonomy"]
    assert reviews["dsp-radar"]["inventory"] == {
        "source_items": 84,
        "platform_modules": 84,
        "interactive_modules": 84,
    }
    assert reviews["controls-gnc"]["inventory"] == {
        "source_items": 24,
        "platform_modules": 62,
        "interactive_modules": 62,
    }
    assert reviews["robotics-autonomy"]["inventory"] == {
        "source_items": 24,
        "platform_modules": 24,
        "interactive_modules": 24,
    }
    assert status["policies"]["completion_language"] == {
        "module_counts_are_inventory_only": True,
        "curriculum_complete_requires": "curriculum_covered: passed",
    }

    for review in reviews.values():
        assert list(review["maturity"]) == MATURITY_STATES
        assert list(review["rubric"]) == RUBRIC_DIMENSIONS
        assert review["maturity"]["curriculum_covered"]["status"] != "passed"
        for stage in review["maturity"].values():
            assert set(stage) == {"status", "evidence", "limitation"}
            assert stage["evidence"].strip()
            assert stage["limitation"].strip()


def test_follow_up_ownership_is_exact_and_remains_unimplemented_here() -> None:
    reviews = _review_by_id(_status())
    assert reviews["dsp-radar"]["disposition"] == "remediate"
    assert reviews["dsp-radar"]["follow_up_issues"] == [441]
    assert reviews["controls-gnc"]["disposition"] == "expand"
    assert reviews["controls-gnc"]["follow_up_issues"] == [439]
    assert reviews["controls-gnc"]["maturity"]["numerically_verified"]["status"] == (
        "passed"
    )
    assert reviews["controls-gnc"]["maturity"]["curriculum_covered"]["status"] == (
        "partial"
    )
    assert reviews["controls-gnc"]["maturity"]["capstone_integrated"]["status"] == (
        "partial"
    )
    assert reviews["controls-gnc"]["maturity"]["learner_validated"]["status"] == (
        "not_run"
    )
    assert reviews["robotics-autonomy"]["disposition"] == "expand"
    assert reviews["robotics-autonomy"]["follow_up_issues"] == [440]


def test_vehicle_dynamics_hold_is_explicit_and_complete() -> None:
    holds = _status()["holds"]
    assert len(holds) == 1
    hold = holds[0]
    assert hold["course_id"] == "vehicle-dynamics"
    assert hold["implementation_status"] == "not_implemented"
    assert hold["authorization_status"] == "blocked"
    conditions = " ".join(hold["release_conditions"])
    assert "competency-to-module matrix" in conditions
    assert "GR86 CAN/BLE" in conditions
    assert "at most ten new lessons" in conditions


def test_valid_coherent_authorization_passes() -> None:
    status = _status()
    assert status["policies"]["batching"]["max_new_lessons"] == 10
    assert status["policies"]["conversion_authorization"] == {
        "competency_map_required": True,
        "schema": "portfolio-control/contracts/course-competency-map.schema.json",
        "count_source": "competency_to_module_matrix",
        "arbitrary_module_target_allowed": False,
    }
    _validate_authorization(_valid_authorization(), status)


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (lambda item: item.update({"count_source": "arbitrary_target"}), "derived"),
        (lambda item: item.update({"new_lessons": 11}), "ten-lesson"),
        (
            lambda item: item.update({"competency_map_validated": False}),
            "competency mapping",
        ),
        (
            lambda item: item["independent_evidence"].update(
                {"imports_production_entrypoint": True}
            ),
            "imports",
        ),
        (
            lambda item: item["independent_evidence"].update(
                {"derived_from_production_output": True}
            ),
            "derives",
        ),
        (
            lambda item: item["independent_evidence"].update(
                {"perturbs_production_output": True}
            ),
            "perturbs",
        ),
    ],
    ids=[
        "arbitrary-count",
        "eleven-lessons",
        "missing-map",
        "imports-production",
        "derived-from-production",
        "perturbed-production",
    ],
)
def test_invalid_authorization_and_false_independence_are_rejected(
    mutation: Any, message: str
) -> None:
    candidate = deepcopy(_valid_authorization())
    mutation(candidate)
    with pytest.raises(ValueError, match=message):
        _validate_authorization(candidate, _status())
