import fnmatch
import importlib.util
import json
import math
import subprocess
from pathlib import Path

import pytest
import yaml

from elp_api.catalog import CourseCatalog
from elp_api.runtime import ExperimentRuntime

ROOT = Path(__file__).resolve().parents[3]
COURSE = ROOT / "courses/dsp-radar"
BASELINE = "b107ac198543e8dfb563c6aae4175cc87da6210d"


def decode(raw):
    if isinstance(raw, bytes):
        raw = raw.decode()
    return json.loads(raw) if raw.lstrip().startswith("{") else yaml.safe_load(raw)


def read(path):
    return decode(path.read_text())


def historical(path):
    return subprocess.check_output(
        ["git", "show", f"{BASELINE}:{path.relative_to(ROOT)}"], cwd=ROOT
    )


def test_reviewed_map_has_exact_identity_binding_and_no_orphaned_assessments():
    mapping = read(COURSE / "competency-map.yaml")
    schema = json.loads((COURSE / "competency-map.schema.json").read_text())
    spec = importlib.util.spec_from_file_location(
        "dsp_aggregate_schema", ROOT / "apps/api/tests/test_dsp_conversion_framework.py"
    )
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    assert helper._schema_errors(mapping, schema, schema) == []
    assert (COURSE / "competency-map.schema.json").read_bytes() == (
        ROOT / "courses/controls-gnc/competency-map.schema.json"
    ).read_bytes()
    registry = read(COURSE / "assessment-map.json")
    assert mapping["course"]["baseline"] == registry["baseline"] == BASELINE
    assert mapping["count_derivation"]["planned_module_count"] == len(mapping["modules"]) == 84
    assert len(mapping["competencies"]) == 84
    assert len(mapping["assessments"]) == 94
    assert registry["formative_count"] == len(registry["lessons"]) == 84
    assert registry["cumulative_count"] == len(registry["domains"]) == 10
    assert registry["retained_independent_case_count"] == 417
    modules = {m["id"]: m for m in mapping["modules"]}
    competencies = {c["id"]: c for c in mapping["competencies"]}
    assessments = {a["id"]: a for a in mapping["assessments"]}
    assert set(modules) == {f"P{n:02}" for n in range(1, 85)}
    for m in modules.values():
        for c in m["competency_ids"]:
            assert m["id"] in competencies[c]["module_ids"]
    for c in competencies.values():
        assert c["assessment_ids"]
        for a in c["assessment_ids"]:
            assert c["id"] in assessments[a]["competency_ids"]
    for a in assessments.values():
        for c in a["competency_ids"]:
            assert a["id"] in competencies[c]["assessment_ids"]
    assert len({r["expected_reasoning"] for r in registry["lessons"]}) == 84
    for row in registry["lessons"]:
        manifest = read(COURSE / "modules" / row["module_id"] / "module.yaml")
        assert manifest["number"] == row["number"]
        assert modules[f"P{row['number']:02}"]["title"] == manifest["title"]
        assert row["learner_result"] == "not_recorded"
        assert competencies[row["competency_id"]]["outcome"] == row["task"]
        text = (COURSE / row["assessment_file"]).read_text()
        assert (
            row["task"] in text and row["expected_reasoning"] in text and row["claim_limit"] in text
        )
        assert len(row["task"].split()) >= 12 and len(row["expected_reasoning"].split()) >= 20
        assert "The pinned source develops this physical relationship" not in text
        assert "**Browser recovery.**" in text and "**Reset parameters**" in text
        assert next(c["label"] for c in manifest["controls"] if c["type"] == "toggle") in text


def test_prerequisite_graph_is_closed_acyclic_and_domain_coverage_is_exact():
    mapping = read(COURSE / "competency-map.yaml")
    graph = {m["id"]: m["depends_on"] for m in mapping["modules"]}
    visited, active = set(), set()

    def visit(node):
        assert node in graph
        assert node not in active, f"prerequisite cycle at {node}"
        if node in visited:
            return
        active.add(node)
        for parent in graph[node]:
            visit(parent)
        active.remove(node)
        visited.add(node)

    for node in graph:
        visit(node)
    registry = read(COURSE / "assessment-map.json")
    assert [n for d in registry["domains"] for n in range(d["start"], d["end"] + 1)] == list(
        range(1, 85)
    )
    assert [m for b in mapping["batch_plan"] for m in b["module_ids"]] == [
        f"P{n:02}" for n in range(1, 85)
    ]
    assert all(len(b["module_ids"]) <= 10 for b in mapping["batch_plan"])
    capstone = mapping["capstones"][0]
    assert capstone["module_ids"] == ["P84"]
    assert not {f"DSP-C{n:02}" for n in range(61, 84)} & set(capstone["competency_ids"])
    assert "fixed baseline" in capstone["integration_claim"]


def test_assessment_revision_preserves_models_source_pins_and_all_other_courses():
    changed = subprocess.check_output(
        [
            "git",
            "diff",
            "--name-only",
            BASELINE,
            "00983cab0599b1ce3a613a2cc8ef42eb7b45f0b4",
            "--",
            "courses",
            ".gitmodules",
        ],
        cwd=ROOT,
        text=True,
    ).splitlines()
    allowed = [
        "courses/dsp-radar/competency-map.yaml",
        "courses/dsp-radar/competency-map.schema.json",
        "courses/dsp-radar/assessment-map.json",
        "courses/dsp-radar/coverage.yaml",
        "courses/dsp-radar/remediation-map.yaml",
        "courses/dsp-radar/modules/*/module.yaml",
        "courses/dsp-radar/modules/*/conversion.yaml",
        "courses/dsp-radar/modules/*/assessment.md",
        "courses/robotics-autonomy/modules/58-optimize-a-trajectory-through-obstacle-constraints/experiment.py",
    ]
    assert changed
    assert all(any(fnmatch.fnmatch(p, pattern) for pattern in allowed) for p in changed)
    assert not subprocess.check_output(
        [
            "git",
            "diff",
            BASELINE,
            "--",
            ".gitmodules",
            "courses/*-learning",
            "courses/dsp-radar/remediation_reference_cases.py",
            "courses/dsp-radar/modules/*/experiment.py",
            "courses/dsp-radar/modules/*/lesson.md",
            "courses/dsp-radar/modules/*/evidence",
        ],
        cwd=ROOT,
    )


def test_append_only_blocks_and_target_identity_reconciliation_preserve_provenance():
    catalog = CourseCatalog([ROOT / "courses"])
    old_coverage = decode(historical(COURSE / "coverage.yaml"))
    coverage = read(COURSE / "coverage.yaml")
    assert {k: v for k, v in coverage.items() if k != "items"} == {
        k: v for k, v in old_coverage.items() if k != "items"
    }
    old_remediation = decode(historical(COURSE / "remediation-map.yaml"))
    remediation = read(COURSE / "remediation-map.yaml")
    assert {k: v for k, v in remediation.items() if k != "claim_boundary"} == {
        k: v for k, v in old_remediation.items() if k != "claim_boundary"
    }
    for old_item, item in zip(old_coverage["items"], coverage["items"], strict=True):
        assert {k: v for k, v in old_item.items() if k != "target_content_digest"} == {
            k: v for k, v in item.items() if k != "target_content_digest"
        }
        folder = COURSE / item["target_folder"]
        old_manifest = decode(historical(folder / "module.yaml"))
        manifest = read(folder / "module.yaml")
        assert manifest["blocks"] == old_manifest["blocks"] + [
            {"type": "markdown", "title": "Course checkpoint", "source": "assessment.md"}
        ]
        assert {k: v for k, v in manifest.items() if k != "blocks"} == {
            k: v for k, v in old_manifest.items() if k != "blocks"
        }
        old_conversion = decode(historical(folder / "conversion.yaml"))
        conversion = read(folder / "conversion.yaml")
        assert CourseCatalog._read_yaml(folder / "conversion.yaml")[0] == conversion
        assert CourseCatalog._read_yaml(folder / "module.yaml")[0] == manifest
        assert {k: v for k, v in conversion.items() if k != "target"} == {
            k: v for k, v in old_conversion.items() if k != "target"
        }
        _, record = catalog.module_record("dsp-radar", manifest["id"])
        assert (
            record.revision.content_digest
            == item["target_content_digest"]
            == conversion["target"]["content_digest"]
        )
        assert "assessment.md" in dict(record.input_hashes)
        assert {f"{item['target_folder']}/{k}": v for k, v in record.input_hashes} == {
            r["path"]: r["sha256"] for r in conversion["target"]["files"]
        }


@pytest.mark.parametrize(
    "overrides",
    [
        {},
        {"frequency_hz": -5.0},
        {"phase_rad": math.pi / 2, "amplitude": 1.7},
        {"alias_mode": True},
        {"frequency_hz": 0.0},
    ],
)
def test_p01_analytic_limits_use_phasor_identities_not_production_outputs(overrides):
    catalog = CourseCatalog([ROOT / "courses"])
    module_id = "01-build-a-sinusoid-and-a-complex-phasor"
    _, record = catalog.module_record("dsp-radar", module_id)
    parameters = {c.id: c.default for c in record.manifest.controls} | overrides
    result = ExperimentRuntime(catalog).run("dsp-radar", module_id, overrides)
    metrics = {m.id: m.value for m in result.metrics}
    a, phase = parameters["amplitude"], parameters["phase_rad"]
    f = 5.0 if parameters["alias_mode"] else parameters["frequency_hz"]
    fs = 8.0 if parameters["alias_mode"] else parameters["sample_rate_hz"]
    expected_step = math.atan2(math.sin(2 * math.pi * f / fs), math.cos(2 * math.pi * f / fs))
    assert metrics["initial_i"] == pytest.approx(a * math.cos(phase), abs=1e-12)
    assert metrics["initial_q"] == pytest.approx(a * math.sin(phase), abs=1e-12)
    assert metrics["phase_step"] == pytest.approx(expected_step, abs=1e-12)
    assert result.diagnostics["radius_error"] < 1e-12
    assert result.diagnostics["projection_error"] < 1e-12
    if not f:
        assert "no cycle exists" in (COURSE / "modules" / module_id / "assessment.md").read_text()


def test_software_assessment_acceptance_does_not_promote_other_curricula_or_learners():
    status = read(ROOT / "docs/course-caliber-status.yaml")
    for course in status["course_reviews"]:
        assert course["maturity"]["learner_validated"]["status"] == "not_run"
        if course["course_id"] != "dsp-radar":
            assert all(
                course["maturity"][stage]["status"] == "blocked"
                for stage in ["numerically_verified", "curriculum_covered", "capstone_integrated"]
            )
    audit = read(ROOT / "docs/course-quality/lesson-audit.json")
    assert sum(r["semantic_review"] == "blocked" for r in audit["lessons"]) == 48


def test_checkpoint_named_controls_and_quantities_exist_in_retained_labs():
    import ast
    import re

    registry = read(COURSE / "assessment-map.json")
    for row in registry["lessons"]:
        folder = COURSE / "modules" / row["module_id"]
        manifest = read(folder / "module.yaml")
        tree = ast.parse((folder / "experiment.py").read_text())
        quantities = {
            n.value
            for n in ast.walk(tree)
            if isinstance(n, ast.Constant) and isinstance(n.value, str)
        }
        controls = {c["id"] for c in manifest["controls"]}
        named = set(re.findall(r"\b[a-z][a-z0-9]+_[a-z0-9_]+\b", row["task"]))
        assert named <= quantities | controls, (row["number"], named - quantities - controls)
