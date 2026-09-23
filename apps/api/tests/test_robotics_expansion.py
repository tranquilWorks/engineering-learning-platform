from __future__ import annotations

import importlib.util
import json
import math
import re
from pathlib import Path
from typing import Any

import numpy as np
import yaml

from elp_api.catalog import CourseCatalog
from elp_api.runtime import ExperimentRuntime

ROOT = Path(__file__).resolve().parents[3]
COURSE_ROOT = ROOT / "courses/robotics-autonomy"


def _yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


MAP = _yaml(COURSE_ROOT / "competency-map.yaml")
DEPTH = _yaml(COURSE_ROOT / "depth-review.yaml")
EXPANSION = _yaml(COURSE_ROOT / "expansion-map.yaml")
NATIVE = EXPANSION["implemented_native_modules"]
REFERENCE = None
if NATIVE:
    reference_spec = importlib.util.spec_from_file_location(
        "robotics_expansion_reference", COURSE_ROOT / "expansion_reference_cases.py"
    )
    assert reference_spec is not None and reference_spec.loader is not None
    REFERENCE = importlib.util.module_from_spec(reference_spec)
    reference_spec.loader.exec_module(REFERENCE)

SCENARIOS = ("baseline", "sweep_1", "sweep_2", "broken", "recovery")
GENERIC_LABELS = {"Independent variable", "Response", "Diagnostic", "output", "units"}


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
    expected_summary = {
        "retained_modules": 24,
        "dispositioned": 24,
        "deepen_in_place": 24,
        "runtime_changes_planned": 0,
        "minimum_additions_per_lesson": 5,
    }
    assert {key: DEPTH["summary"][key] for key in expected_summary} == expected_summary
    assert DEPTH["summary"].get("completed", 0) + DEPTH["summary"].get("remaining", 24) == 24
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


def test_completed_depth_items_have_rigorous_lesson_sections() -> None:
    completed = [item for item in DEPTH["items"] if item.get("status") == "completed"]
    for item in completed:
        module_root = COURSE_ROOT / "modules" / item["target_module_id"]
        lesson = (module_root / "lesson.md").read_text(encoding="utf-8")
        assert item["completed_word_count"] >= 1_250
        assert item["completed_word_count"] > item["baseline_word_count"] + 600
        assert item["runtime_changed"] is False
        for heading in (
            "## Deep derivation and conventions",
            "## Alternative formulation and limiting analysis",
            "## Practical failure analysis and recovery",
            "## Evidence workflow and formative check",
            "## Boundary and onward links",
        ):
            assert heading in lesson


def test_robotics_native_designs_are_schema_valid_distinct_and_rigorous() -> None:
    schema = json.loads((COURSE_ROOT / "native-design.schema.json").read_text(encoding="utf-8"))
    helper_path = ROOT / "apps/api/tests/test_dsp_conversion_framework.py"
    helper_spec = importlib.util.spec_from_file_location("robotics_native_schema", helper_path)
    assert helper_spec is not None and helper_spec.loader is not None
    helper = importlib.util.module_from_spec(helper_spec)
    helper_spec.loader.exec_module(helper)
    expected_ids = [f"P{number:02d}" for number in range(25, 25 + len(NATIVE))]
    assert [item["id"] for item in NATIVE] == expected_ids
    fingerprints: set[tuple[str, ...]] = set()
    for item in NATIVE:
        module_root = COURSE_ROOT / item["folder"]
        design = _yaml(module_root / "design.yaml")
        assert helper._schema_errors(design, schema, schema) == []
        fingerprints.add(tuple(design["governing_equations"]))
        assert design["scenarios"]["baseline"] == design["scenarios"]["recovery"]
        assert design["scenarios"]["broken"]["broken_mode"] is True
        assert design["provenance"] == {
            "kind": "python-first-native",
            "source_equivalence_claimed": False,
            "competency_map": "../../competency-map.yaml",
            "matlab_runtime": "not_run",
        }
        lesson = (module_root / "lesson.md").read_text(encoding="utf-8")
        assert len(lesson.split()) >= 1_000
        for section in (
            "Model, derivation, and conventions",
            "Predict before running",
            "Baseline workflow",
            "Two one-variable sweeps",
            "Intentionally broken case",
            "Recovery",
            "Alternative and limiting cases",
            "Independent evidence and MATLAB-style design boundary",
            "Engineering review checklist",
            "Common mistakes",
            "Focused check and teach-back",
        ):
            assert f"## {section}" in lesson
    assert len(fingerprints) == len(NATIVE)


def test_robotics_native_reference_has_no_production_execution_path() -> None:
    assert REFERENCE is not None
    tree = __import__("ast").parse(
        (COURSE_ROOT / "expansion_reference_cases.py").read_text(encoding="utf-8")
    )
    allowed_imports = {"json", "typing", "numpy", "__future__"}
    forbidden_calls = {"eval", "exec", "compile", "__import__", "run", "import_module"}
    ast = __import__("ast")
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            assert all(alias.name.split(".")[0] in allowed_imports for alias in node.names)
        if isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".")[0] in allowed_imports
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in forbidden_calls
    doc = ast.get_docstring(tree, clean=True) or ""
    assert "imports no production experiment" in doc
    assert "consumes no production result" in doc
    assert "perturbs no production value" in " ".join(doc.split())


def _approx(expected: list[float], tolerance: dict[str, float]) -> Any:
    import pytest

    return pytest.approx(expected, abs=tolerance["absolute"], rel=tolerance["relative"])


def test_robotics_native_five_scenario_evidence_and_runtime() -> None:
    assert REFERENCE is not None
    runtime = ExperimentRuntime(CourseCatalog([ROOT / "courses"]))
    for item in NATIVE:
        number = int(item["id"][1:])
        module_root = COURSE_ROOT / item["folder"]
        design = _yaml(module_root / "design.yaml")
        module_id = _yaml(module_root / "module.yaml")["id"]
        expected = json.loads((module_root / "evidence/expected-independent.json").read_text())
        actual = json.loads((module_root / "evidence/actual-production.json").read_text())
        assert expected["origin"] == REFERENCE.origin(number)
        assert actual["origin"]["independent"] is False
        assert expected["signature_fields"] == actual["signature_fields"] == design["signature"]
        assert tuple(expected["cases"]) == tuple(actual["cases"]) == SCENARIOS
        for scenario in SCENARIOS:
            parameters = design["scenarios"][scenario]
            reference = REFERENCE.reference_signature(number, parameters)
            first = runtime.run("robotics-autonomy", module_id, parameters)
            second = runtime.run("robotics-autonomy", module_id, parameters)
            production = first.diagnostics["signature"]
            assert first.model_dump(mode="json") == second.model_dump(mode="json")
            assert first.diagnostics["sample_count"] <= 500
            assert reference == expected["cases"][scenario]["signature"]
            assert production == _approx(
                actual["cases"][scenario]["signature"], design["tolerance"]
            )
            assert len(reference) == len(production) == len(design["signature"])
            assert np.all(np.isfinite(reference)) and np.all(np.isfinite(production))
            assert production == _approx(reference, design["tolerance"])
        assert expected["cases"]["baseline"] == expected["cases"]["recovery"]
        assert actual["cases"]["baseline"] == actual["cases"]["recovery"]
        assert actual["cases"]["broken"]["signature"] != actual["cases"]["recovery"]["signature"]


def test_robotics_native_plots_retain_domain_quantities_and_units() -> None:
    runtime = ExperimentRuntime(CourseCatalog([ROOT / "courses"]))
    for item in NATIVE:
        module_root = COURSE_ROOT / item["folder"]
        module_id = _yaml(module_root / "module.yaml")["id"]
        result = runtime.run("robotics-autonomy", module_id, {}).model_dump(mode="json")
        assert set(result["plots"]) == {"response", "mechanism"}
        assert len(result["metrics"]) == 3
        for plot in result["plots"].values():
            for axis in ("xaxis", "yaxis"):
                title = plot["layout"][axis]["title"]["text"]
                assert title not in GENERIC_LABELS
                assert re.search(r"\([^()]+\)$", title), title
            for trace in plot["data"]:
                assert set(trace["meta"]) == {
                    "x_quantity",
                    "x_unit",
                    "y_quantity",
                    "y_unit",
                }
                assert all(str(value).strip() for value in trace["meta"].values())


def test_robotics_geometry_and_dynamics_teaching_invariants() -> None:
    runtime = ExperimentRuntime(CourseCatalog([ROOT / "courses"]))

    def signature(number: int, supplied: dict[str, Any]) -> list[float]:
        item = NATIVE[number - 25]
        module_id = _yaml(COURSE_ROOT / item["folder"] / "module.yaml")["id"]
        return runtime.run("robotics-autonomy", module_id, supplied).diagnostics["signature"]

    assert signature(25, {"broken_mode": False})[0] == 0
    assert signature(25, {"broken_mode": True})[0] > 0
    assert signature(26, {"broken_mode": False})[0] < 1e-10
    assert signature(26, {"broken_mode": True})[1] > 0
    assert signature(27, {"broken_mode": False})[0] == 0
    assert signature(27, {"broken_mode": True})[0] > 0
    singular = signature(28, {"elbow_angle_deg": 175.0})
    nonsingular = signature(28, {"elbow_angle_deg": 70.0})
    assert singular[0] < nonsingular[0]
    assert signature(29, {"broken_mode": True})[1] > signature(29, {"broken_mode": False})[1]
    assert signature(30, {"broken_mode": False})[1] == 0
    assert signature(30, {"broken_mode": True})[1] > 0
    inertia = signature(31, {"broken_mode": False})
    assert inertia[0] > 0 and math.isfinite(inertia[2])
    identification = signature(32, {"broken_mode": False})
    assert identification[0] < signature(32, {"broken_mode": True})[0]
    assert identification[2] < signature(32, {"broken_mode": True})[2]
    assert signature(33, {"broken_mode": False})[2] == 0
    assert signature(33, {"broken_mode": True})[2] > 0


def test_robotics_control_and_interaction_teaching_invariants() -> None:
    runtime = ExperimentRuntime(CourseCatalog([ROOT / "courses"]))

    def signature(number: int, supplied: dict[str, Any]) -> list[float]:
        item = NATIVE[number - 25]
        module_id = _yaml(COURSE_ROOT / item["folder"] / "module.yaml")["id"]
        return runtime.run("robotics-autonomy", module_id, supplied).diagnostics["signature"]

    for number in (34, 35, 36, 37):
        nominal = signature(number, {"broken_mode": False})
        broken = signature(number, {"broken_mode": True})
        assert broken[0] > nominal[0]
    hybrid = signature(38, {"broken_mode": False})
    hybrid_broken = signature(38, {"broken_mode": True})
    assert hybrid[2] == 0 < hybrid_broken[2]
    passive = signature(39, {"broken_mode": False})
    active = signature(39, {"broken_mode": True})
    assert passive[0] > 0 > active[0]
    swing_up = signature(40, {"broken_mode": False})
    wrong_energy_sign = signature(40, {"broken_mode": True})
    assert wrong_energy_sign[0] > swing_up[0]
    assert wrong_energy_sign[1] > swing_up[1]


def test_robotics_perception_teaching_invariants() -> None:
    runtime = ExperimentRuntime(CourseCatalog([ROOT / "courses"]))

    def signature(number: int, supplied: dict[str, Any]) -> list[float]:
        item = NATIVE[number - 25]
        module_id = _yaml(COURSE_ROOT / item["folder"] / "module.yaml")["id"]
        return runtime.run("robotics-autonomy", module_id, supplied).diagnostics["signature"]

    pinhole = signature(41, {"broken_mode": False})
    wrong_frame = signature(41, {"broken_mode": True})
    assert pinhole[2] == 0 < wrong_frame[2]
    calibration = signature(42, {"broken_mode": False})
    pinhole_only = signature(42, {"broken_mode": True})
    assert pinhole_only[0] > calibration[0]
    features = signature(43, {"broken_mode": False})
    unnormalized = signature(43, {"broken_mode": True})
    assert features[0] > unnormalized[0] and features[1] < unnormalized[1]
    robust_match = signature(44, {"broken_mode": False})
    least_squares = signature(44, {"broken_mode": True})
    assert robust_match[0] > least_squares[0] and robust_match[1] < least_squares[1]
    for number in (45, 46, 48):
        nominal = signature(number, {"broken_mode": False})
        broken = signature(number, {"broken_mode": True})
        assert nominal[0] < broken[0] and nominal[1] < broken[1]
    occupancy = signature(47, {"broken_mode": False})
    endpoint_only = signature(47, {"broken_mode": True})
    assert occupancy[2] < endpoint_only[2]


def test_robotics_slam_teaching_invariants() -> None:
    runtime = ExperimentRuntime(CourseCatalog([ROOT / "courses"]))

    def signature(number: int, supplied: dict[str, Any]) -> list[float]:
        item = NATIVE[number - 25]
        module_id = _yaml(COURSE_ROOT / item["folder"] / "module.yaml")["id"]
        return runtime.run("robotics-autonomy", module_id, supplied).diagnostics["signature"]

    observable = signature(49, {"broken_mode": False})
    synchronized_badly = signature(49, {"broken_mode": True})
    assert observable[0] > synchronized_badly[0]
    assert observable[1] < synchronized_badly[1]
    gated = signature(50, {"broken_mode": False})
    ungated = signature(50, {"broken_mode": True})
    assert gated[1] > ungated[1] and gated[2] < ungated[2]
    for number in (51, 53):
        nominal = signature(number, {"broken_mode": False})
        broken = signature(number, {"broken_mode": True})
        assert nominal[0] < broken[0]
    verified_loop = signature(52, {"broken_mode": False})
    false_loop = signature(52, {"broken_mode": True})
    assert false_loop[0] > 0
    assert verified_loop[1] < false_loop[1]
    assert verified_loop[2] < false_loop[2]
    consistent = signature(53, {"broken_mode": False})
    inconsistent = signature(53, {"broken_mode": True})
    assert consistent[1] > inconsistent[1] and consistent[2] < inconsistent[2]


def test_robotics_planning_teaching_invariants() -> None:
    runtime = ExperimentRuntime(CourseCatalog([ROOT / "courses"]))

    def signature(number: int, supplied: dict[str, Any]) -> list[float]:
        item = NATIVE[number - 25]
        module_id = _yaml(COURSE_ROOT / item["folder"] / "module.yaml")["id"]
        return runtime.run("robotics-autonomy", module_id, supplied).diagnostics["signature"]

    repaired = signature(54, {"broken_mode": False})
    stale = signature(54, {"broken_mode": True})
    assert repaired[1] == 0 < stale[1]

    roadmap = signature(55, {"broken_mode": False})
    unchecked = signature(55, {"broken_mode": True})
    assert roadmap[1] == 0 < unchecked[1]

    rewired = signature(56, {"broken_mode": False})
    unrewired = signature(56, {"broken_mode": True})
    assert rewired[0] < unrewired[0]
    assert rewired[1] > unrewired[1] == 0

    swept = signature(57, {"broken_mode": False})
    endpoints_only = signature(57, {"broken_mode": True})
    assert swept[1] >= 0 and swept[2] == 0
    assert endpoints_only[1] < 0 and endpoints_only[2] > 0

    constrained = signature(58, {"broken_mode": False})
    unconstrained = signature(58, {"broken_mode": True})
    assert constrained[1] >= 0 and constrained[2] == 0
    assert unconstrained[1] < 0 and unconstrained[2] > 0

    kinodynamic = signature(59, {"broken_mode": False})
    geometric = signature(59, {"broken_mode": True})
    assert kinodynamic[1:] == [0.0, 0.0]
    assert geometric[1] > 0 and geometric[2] > 0

    predictive = signature(60, {"broken_mode": False})
    frozen = signature(60, {"broken_mode": True})
    assert predictive[0] >= 0.9 and predictive[1] == 0
    assert frozen[0] < 0.9 and frozen[1] > 0


def test_robotics_manipulation_and_task_autonomy_teaching_invariants() -> None:
    runtime = ExperimentRuntime(CourseCatalog([ROOT / "courses"]))

    def signature(number: int, supplied: dict[str, Any]) -> list[float]:
        item = NATIVE[number - 25]
        module_id = _yaml(COURSE_ROOT / item["folder"] / "module.yaml")["id"]
        return runtime.run("robotics-autonomy", module_id, supplied).diagnostics["signature"]

    closed = signature(61, {"broken_mode": False})
    reversed_normal = signature(61, {"broken_mode": True})
    assert closed[0] > 0 >= reversed_normal[0]
    assert closed[1] < reversed_normal[1]

    calibrated_pick = signature(62, {"broken_mode": False})
    wrong_frame_pick = signature(62, {"broken_mode": True})
    assert calibrated_pick[0] < 0.055 < wrong_frame_pick[0]
    assert calibrated_pick[2] == 9 > wrong_frame_pick[2]

    coordinated_reach = signature(63, {"broken_mode": False})
    frozen_base = signature(63, {"broken_mode": True})
    assert coordinated_reach[0] < 1.0e-9 < frozen_base[0]
    assert coordinated_reach[1] > frozen_base[1]

    recovered_task = signature(64, {"broken_mode": False})
    abandoned_task = signature(64, {"broken_mode": True})
    assert recovered_task[:2] == [1.0, 1.0]
    assert abandoned_task[:2] == [0.0, 0.0]

    reserved = signature(65, {"broken_mode": False})
    independent = signature(65, {"broken_mode": True})
    assert reserved[0] == 0 < independent[0]
    assert reserved[2] > 0 == independent[2]


def test_robotics_systems_and_capstone_teaching_invariants() -> None:
    runtime = ExperimentRuntime(CourseCatalog([ROOT / "courses"]))

    def signature(number: int, supplied: dict[str, Any]) -> list[float]:
        item = NATIVE[number - 25]
        module_id = _yaml(COURSE_ROOT / item["folder"] / "module.yaml")["id"]
        return runtime.run("robotics-autonomy", module_id, supplied).diagnostics["signature"]

    integrated = signature(66, {"broken_mode": False})
    wrong_units = signature(66, {"broken_mode": True})
    assert integrated[0] < wrong_units[0]
    assert integrated[2] == 0 < wrong_units[2]

    recovered_replay = signature(67, {"broken_mode": False})
    arrival_replay = signature(67, {"broken_mode": True})
    assert recovered_replay[0] < arrival_replay[0]
    assert recovered_replay[1] == 1 > arrival_replay[1]
    assert recovered_replay[2] < arrival_replay[2]

    mobile_capstone = signature(68, {"broken_mode": False})
    stale_mobile = signature(68, {"broken_mode": True})
    assert mobile_capstone[0] == 1 and mobile_capstone[1] >= 0.85
    assert mobile_capstone[2] == 0 < stale_mobile[2]
    assert stale_mobile[0] == 0 and stale_mobile[1] < 0.85

    manipulation_capstone = signature(69, {"broken_mode": False})
    broken_manipulation = signature(69, {"broken_mode": True})
    assert manipulation_capstone[0] == 1 and manipulation_capstone[1] < 0.055
    assert manipulation_capstone[2] >= 0
    assert broken_manipulation[0] == 0 and broken_manipulation[2] < 0


def test_robotics_capstone_requirement_traces_close_over_reviewed_dependencies() -> None:
    mapped = {item["id"]: item for item in MAP["modules"]}
    capstones = {
        "P68": ("CAP-MOBILE-AUTONOMY", "68-capstone-navigate-and-replan-with-perception"),
        "P69": (
            "CAP-TWO-LINK-MANIPULATION",
            "69-capstone-perceive-grasp-and-control-a-two-link-robot",
        ),
    }
    for item_id, (capstone_id, folder) in capstones.items():
        trace = _yaml(COURSE_ROOT / "modules" / folder / "requirements-trace.yaml")
        assert trace["schema_version"] == 1
        assert trace["capstone_id"] == capstone_id
        assert trace["module_id"] == item_id
        assert len(trace["requirements"]) >= 5
        prerequisites = {
            prerequisite
            for requirement in trace["requirements"]
            for prerequisite in requirement["prerequisite_modules"]
        }
        assert set(mapped[item_id]["depends_on"]) <= prerequisites
        assert len({requirement["id"] for requirement in trace["requirements"]}) == len(
            trace["requirements"]
        )
        assert all(requirement["mechanism"] and requirement["evidence"]
                   for requirement in trace["requirements"])
