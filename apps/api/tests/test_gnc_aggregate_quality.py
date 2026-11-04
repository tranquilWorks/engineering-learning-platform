"""Actual assessment, mechanism, independence and preservation gates for Controls."""

from __future__ import annotations

import ast
import importlib.util
import itertools
import subprocess
from pathlib import Path

import numpy as np
import pytest
import yaml

from elp_api.catalog import CourseCatalog
from elp_api.runtime import ExperimentRuntime

ROOT = Path(__file__).resolve().parents[3]
COURSE = ROOT / "courses/controls-gnc"
BASELINE = "abe7c49cea2a649354f20ad19dbe8a2e6c78540a"
REPAIRED = (44, 52, 53, 54, 58, 59, 63)


def read(path):
    return yaml.safe_load(path.read_text())


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def runtime():
    return ExperimentRuntime(CourseCatalog([ROOT / "courses"]))


def folder(number):
    return next((COURSE / "modules").glob(f"{number:02}-*"))


def run(runtime, number, parameters=None):
    return runtime.run("controls-gnc", folder(number).name, parameters or {}).model_dump(
        mode="json"
    )


def historical(path):
    return subprocess.check_output(
        ["git", "show", f"{BASELINE}:{path.relative_to(ROOT)}"], cwd=ROOT
    )


def test_exact_curriculum_identity_assessments_and_bidirectional_competency_bindings():
    mapping = read(COURSE / "competency-map.yaml")
    registry = read(COURSE / "assessment-map.json")
    helper = load(ROOT / "apps/api/tests/test_dsp_conversion_framework.py")
    schema = read(COURSE / "competency-map.schema.json")
    assert helper._schema_errors(mapping, schema, schema) == []
    assert registry["baseline"] == mapping["course"]["baseline"] == BASELINE
    assert len(registry["lessons"]) == registry["formative_count"] == 68
    assert len(registry["domains"]) == registry["cumulative_count"] == 22
    assert len(mapping["assessments"]) == 90
    modules = {r["id"]: r for r in mapping["modules"]}
    competencies = {r["id"]: r for r in mapping["competencies"]}
    assessments = {r["id"]: r for r in mapping["assessments"]}
    assert set(modules) == {f"P{n:02}" for n in range(1, 69)}
    for competency in competencies.values():
        for assessment in competency["assessment_ids"]:
            assert competency["id"] in assessments[assessment]["competency_ids"]
        for module in competency["module_ids"]:
            assert competency["id"] in modules[module]["competency_ids"]
    for assessment in assessments.values():
        for competency in assessment["competency_ids"]:
            assert assessment["id"] in competencies[competency]["assessment_ids"]
    assert len({r["expected_reasoning"] for r in registry["lessons"]}) == 68
    for row in registry["lessons"]:
        path = COURSE / "modules" / row["module_id"]
        manifest = read(path / "module.yaml")
        text = (COURSE / row["assessment_file"]).read_text()
        assert row["number"] == manifest["number"]
        assert modules[f"P{row['number']:02}"]["title"] == manifest["title"]
        assert (
            row["task"] in text and row["expected_reasoning"] in text and row["claim_limit"] in text
        )
        assert "Reset parameters" in text and "two one-variable sweeps" in text
        assert row["learner_result"] == "not_recorded"
        assert len(row["expected_reasoning"].split()) >= 20
        assert any(b.get("source") == "assessment.md" for b in manifest["blocks"])
        # Preserve previously reviewed individual reasoning verbatim.
        try:
            old = historical(path / "assessment.md").decode()
        except subprocess.CalledProcessError:
            old = ""
        assert text.startswith(old)
    for domain in registry["domains"]:
        text = (COURSE / domain["assessment_file"]).read_text()
        assert all(f"### {n}." in text for n in range(1, 5))
        assert "Four-criterion rubric" in text
        assert "](#/courses/" not in text
        anchor = COURSE / "modules" / domain["module_id"]
        assert any(
            b.get("source") == Path(domain["assessment_file"]).name
            for b in read(anchor / "module.yaml")["blocks"]
        )


def test_prerequisites_remain_exact_and_acyclic_and_capstones_name_their_actual_scope():
    mapping = read(COURSE / "competency-map.yaml")
    old = yaml.safe_load(historical(COURSE / "competency-map.yaml"))
    assert mapping["scope"]["outcomes"] == old["scope"]["outcomes"]
    assert {c["id"]: c["outcome"] for c in mapping["competencies"]} == {
        c["id"]: c["outcome"] for c in old["competencies"]
    }
    graph = {m["id"]: m["depends_on"] for m in mapping["modules"]}
    assert graph == {m["id"]: m["depends_on"] for m in old["modules"]}
    visited = set()

    def visit(node, active):
        assert node not in active
        if node in visited:
            return
        for predecessor in graph[node]:
            visit(predecessor, active | {node})
        visited.add(node)

    for node in graph:
        visit(node, set())
    assert len(visited) == 68
    claims = " ".join(c["integration_claim"] for c in mapping["capstones"])
    assert "scalar" in claims and "planar" in claims and "not real hardware timing" in claims
    assert "does not import P60" in claims


def test_no_source_model_other_course_or_generic_runtime_mutation():
    paths = [
        ".gitmodules",
        "courses/*-learning",
        "courses/dsp-radar",
        "courses/robotics-autonomy",
        "courses/vehicle-dynamics",
        "courses/demo-radar",
        "courses/platform-showcase",
        "apps/api/src",
        "apps/web/src/components",
        "packages",
        ".github",
    ]
    active = yaml.safe_load((ROOT / "contracts/active-batch.yaml").read_text())
    if active["batch"]["id"] == "ELP-ROB-AGGREGATE-QUALITY-01":
        # The succeeding approved batch may edit Robotics. Its own preservation
        # test pins every other course, including all Controls bytes, to PR63.
        assert active["sources"]["baseline_commit"] == "185e966242c889d3f030bab6016139777fcf0f17"
        paths.remove("courses/robotics-autonomy")
    assert not subprocess.check_output(["git", "diff", BASELINE, "--", *paths], cwd=ROOT)
    for number in range(1, 25):
        for name in (
            "experiment.py",
            "lesson.md",
            "evidence/expected-independent.json",
            "evidence/actual-production.json",
        ):
            path = folder(number) / name
            assert path.read_bytes() == historical(path)
        path = folder(number) / "conversion.yaml"
        old, current = yaml.safe_load(historical(path)), read(path)
        assert {k: v for k, v in current.items() if k != "target"} == {
            k: v for k, v in old.items() if k != "target"
        }
    reference_path = COURSE / "expansion_reference_cases.py"
    old_tree, new_tree = (
        ast.parse(historical(reference_path)),
        ast.parse(reference_path.read_text()),
    )
    old_defs = {f.name: ast.dump(f) for f in old_tree.body if isinstance(f, ast.FunctionDef)}
    new_defs = {f.name: ast.dump(f) for f in new_tree.body if isinstance(f, ast.FunctionDef)}
    changed = {f"_p{n}" for n in (34, 35, 37, 39, 40, 41, *REPAIRED)} | {"origin"}
    assert all(
        new_defs[name] == definition for name, definition in old_defs.items() if name not in changed
    )


@pytest.mark.parametrize("number", (34, 35, 37, 39, 40, 41, *REPAIRED))
def test_new_references_compute_unretained_inputs_and_never_lookup_expected_outputs(
    runtime, number
):
    reference = load(COURSE / "expansion_reference_cases.py")
    manifest = read(folder(number) / "module.yaml")
    parameters = {c["id"]: c["default"] for c in manifest["controls"]}
    for control in manifest["controls"]:
        if control["type"] == "slider":
            parameters[control["id"]] = 0.37 * control["minimum"] + 0.63 * control["maximum"]
    expected = reference.reference_signature(number, parameters)
    actual = run(runtime, number, parameters)["diagnostics"]["signature"]
    np.testing.assert_allclose(actual, expected, atol=1e-8, rtol=1e-8)
    function = next(
        f
        for f in ast.parse((COURSE / "expansion_reference_cases.py").read_text()).body
        if isinstance(f, ast.FunctionDef) and f.name == f"_p{number}"
    )
    assert "_NATIVE_FIXTURES" not in ast.unparse(function)


@pytest.mark.parametrize("number", REPAIRED)
def test_all_repaired_control_corners_and_full_independent_mechanisms(runtime, number):
    reference = load(COURSE / "expansion_reference_cases.py")
    manifest = read(folder(number) / "module.yaml")
    controls = manifest["controls"]
    choices = [
        [False, True] if c["type"] == "toggle" else [c["minimum"], c["maximum"]] for c in controls
    ]
    for values in itertools.product(*choices):
        parameters = dict(zip([c["id"] for c in controls], values, strict=True))
        actual = run(runtime, number, parameters)["diagnostics"]
        expected = reference.aggregate_mechanism(number, parameters)
        for key, value in expected.items():
            if value is None:
                assert actual[key] is None
            else:
                np.testing.assert_allclose(
                    actual[key],
                    value,
                    atol=1e-8,
                    rtol=1e-8,
                    err_msg=f"P{number} {key} {parameters}",
                )


def test_gating_ekf_singular_geometry_bias_and_nonlinear_los_have_discriminating_physics(runtime):
    nominal, fault = run(runtime, 53), run(runtime, 53, {"broken_mode": True})
    n, f = (
        np.array(nominal["diagnostics"]["filter_history"]),
        np.array(fault["diagnostics"]["filter_history"]),
    )
    assert n[20, 4] == pytest.approx(16) and f[20, 4] == pytest.approx(16)
    assert n[20, 6] == 0 and f[20, 6] == 1 and n[20, 2] != f[20, 2]
    np.testing.assert_allclose(n[:, 4], n[:, 8] ** 2 / n[:, 7], atol=1e-12)
    np.testing.assert_allclose(n[:, 5], (n[:, 2] - n[:, 0]) ** 2 / n[:, 3], atol=1e-12)
    ekf = run(runtime, 54)["diagnostics"]
    assert ekf["posterior_state"] == pytest.approx(1.3125)
    assert ekf["posterior_variance"] == pytest.approx(0.125)
    assert ekf["signature"][2] == pytest.approx(0.09765625)
    assert run(runtime, 54, {"broken_mode": True})["diagnostics"]["posterior_state"] == 1.0
    singular = run(runtime, 58, {"maneuver_span_deg": 0.0})
    assert singular["diagnostics"]["rank"] == 1 and singular["diagnostics"]["covariance"] is None
    assert (
        next(m for m in singular["metrics"] if m["id"] == "bias_standard_deviation")["value"]
        is None
    )
    valid = run(runtime, 58)["diagnostics"]
    np.testing.assert_allclose(
        np.array(valid["information"]) @ valid["covariance"], np.eye(2), atol=1e-10
    )
    bias = run(runtime, 59)["diagnostics"]
    assert bias["time"][-1] == 30 and bias["position"][-1] == pytest.approx(13.5)
    assert bias["corrected_position"][-1] == pytest.approx(0.675)
    assert run(runtime, 59, {"broken_mode": True})["diagnostics"]["corrected_position"][
        -1
    ] == pytest.approx(13.5)
    los = run(runtime, 63)["diagnostics"]
    assert los["signature"][1] != pytest.approx(10 * np.exp(-8 / 15 * 12), rel=1e-3)
    assert np.all(np.diff(np.array(los["path"])[:, 1]) < 0)
    assert np.all(
        np.diff(np.array(run(runtime, 63, {"broken_mode": True})["diagnostics"]["path"])[:, 1]) > 0
    )


def test_capstone_verdicts_are_bound_to_actual_histories_not_authored_pass_claims(runtime):
    for number in (66, 67, 68):
        for broken in (False, True):
            result = run(runtime, number, {"broken_mode": broken})
            requirements = result["diagnostics"]["requirements"]
            assert requirements
            for row in requirements.values():
                expected = (
                    row["value"] <= row["threshold"] + 1e-10
                    if row["operator"] == "<="
                    else row["value"] >= row["threshold"] - 1e-10
                )
                assert row["passed"] is expected
            assert result["tables"]["requirements"]["rows"]


def test_open_curriculum_gaps_cannot_be_closed_by_renaming_component_lessons():
    gaps = read(ROOT / "docs/course-quality/gnc-aggregate-open-gaps.json")
    assert {g["id"] for g in gaps["gaps"]} == {
        "GNC-AGG-NONLINEAR-FILTER",
        "GNC-AGG-STRAPDOWN-FUSION",
    }
    status = read(ROOT / "docs/course-caliber-status.yaml")
    controls = next(c for c in status["course_reviews"] if c["course_id"] == "controls-gnc")
    if any(g["status"] == "open" for g in gaps["gaps"]):
        assert gaps["status"] == "course_acceptance_blocked"
        assert all(
            controls["maturity"][stage]["status"] == "blocked"
            for stage in ("numerically_verified", "curriculum_covered", "capstone_integrated")
        )
    assert all(g["status"] in {"open", "closed_synthetic"} for g in gaps["gaps"])
    if all(g["status"] == "closed_synthetic" for g in gaps["gaps"]):
        import hashlib

        report = read(ROOT / "docs/course-quality/gnc-aggregate-http.json")
        comparisons = report["recursive_integration_comparisons"]
        assert len(comparisons) == 25
        assert {row["number"] for row in comparisons} == {54, 55, 59, 61, 67}
        assert all(row["status"] == "passed" for row in comparisons)
        assert (
            report["integration_reference_sha256"]
            == hashlib.sha256(
                (COURSE / "recursive_navigation_references.py").read_bytes()
            ).hexdigest()
        )
        catalog = CourseCatalog([ROOT / "courses"])
        for binding in report["bindings"]:
            _, record = catalog.module_record("controls-gnc", binding["module_id"])
            assert binding["content_digest"] == record.revision.content_digest
        assert all(g.get("evidence") for g in gaps["gaps"])
    assert controls["maturity"]["learner_validated"]["status"] == "not_run"
