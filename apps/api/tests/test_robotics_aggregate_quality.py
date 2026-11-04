"""Whole-course identity, assessment and isolation gates for Robotics qualification."""

import json
import subprocess
from pathlib import Path

import pytest
import yaml

from elp_api.catalog import CourseCatalog

ROOT = Path(__file__).resolve().parents[3]
COURSE = ROOT / "courses/robotics-autonomy"
BASELINE = "185e966242c889d3f030bab6016139777fcf0f17"


@pytest.fixture(scope="module")
def catalog():
    return CourseCatalog([COURSE])


def test_all_actual_lessons_have_unique_bound_assessments(catalog):
    registry = json.loads((COURSE / "assessment-map.json").read_text())
    assert len(registry["lessons"]) == registry["formative_count"] == 69
    assert len(registry["portfolios"]) == registry["cumulative_count"] == 13
    assert len({r["task"] for r in registry["lessons"]}) == 69
    mapping = yaml.safe_load((COURSE / "competency-map.yaml").read_text())
    assessments = {a["id"]: a for a in mapping["assessments"]}
    for n, row in enumerate(registry["lessons"], 1):
        assert row["number"] == n and row["id"] == f"ROB-F{n:02d}"
        assert row["id"] in assessments
        _, record = catalog.module_record("robotics-autonomy", row["module_id"])
        manifest = yaml.safe_load((record.path / "module.yaml").read_text())
        assert row["plot_keys"] == [
            p for b in manifest["blocks"] if b["type"] == "plot_grid" for p in b["plots"]
        ]
        text = (COURSE / row["assessment_file"]).read_text()
        for section in [
            "Predict and derive",
            "Controlled comparison",
            "Diagnose and recover",
            "Expected reasoning",
            "Limits and handoff",
        ]:
            assert section in text
        assert row["task"] in text and row["expected_reasoning"] in text
    generated = list((COURSE / "modules").glob("*/portfolio-a-*.md"))
    assert {str(p.relative_to(COURSE)) for p in generated} == {
        p["assessment_file"] for p in registry["portfolios"]
    }
    for p in registry["portfolios"]:
        text = (COURSE / p["assessment_file"]).read_text()
        assert "Four-criterion rubric" in text and "Diagnose and recover" in text
        assert all(c in {x["id"] for x in mapping["competencies"]} for c in p["competency_ids"])


def test_forbidden_sources_other_courses_and_runtime_preserved():
    paths = [
        ".gitmodules",
        "courses/*-learning",
        "courses/dsp-radar",
        "courses/controls-gnc",
        "courses/vehicle-dynamics",
        "courses/demo-radar",
        "courses/platform-showcase",
        "apps/api/src",
        "apps/web/src/components",
        "packages",
        ".github",
    ]
    paths += [
        f"courses/robotics-autonomy/{p}"
        for p in ["course.yaml", "source-map.yaml", "fidelity-map.yaml", "conversion-manifest.yaml"]
    ]
    assert not subprocess.check_output(["git", "diff", BASELINE, "--", *paths], cwd=ROOT)
    for n in range(1, 25):
        folder = next((COURSE / "modules").glob(f"{n:02d}-*"))
        relative = str(folder.relative_to(ROOT))
        for name in ["experiment.py", "lesson.md"]:
            before = subprocess.check_output(
                ["git", "show", f"{BASELINE}:{relative}/{name}"], cwd=ROOT
            )
            assert before == (folder / name).read_bytes()
        before = json.loads(
            subprocess.check_output(
                ["git", "show", f"{BASELINE}:{relative}/verification.yaml"], cwd=ROOT
            )
        )
        current = json.loads((folder / "verification.yaml").read_text())
        before.pop("target")
        current.pop("target")
        assert before == current


def test_retained_replay_has_five_cases_per_actual_lesson():
    report = json.loads((ROOT / "docs/course-quality/robotics-aggregate-replay.json").read_text())
    assert report["status"] == "passed" and len(report["comparisons"]) == 345
    for n in range(1, 70):
        cases = [r for r in report["comparisons"] if r["number"] == n]
        assert {r["scenario"] for r in cases} == {
            "baseline",
            "sweep_1",
            "sweep_2",
            "broken",
            "recovery",
        }
        assert all(r["status"] == "passed" for r in cases)
    assert report["learner_validation"] == "not_run"


def test_prior_reviewed_assessments_are_preserved_verbatim():
    paths = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", BASELINE, "courses/robotics-autonomy"],
        cwd=ROOT,
        text=True,
    ).splitlines()
    previous = [p for p in paths if p.endswith("/assessment.md")]
    assert len(previous) == 25
    for relative in previous:
        old = subprocess.check_output(
            ["git", "show", f"{BASELINE}:{relative}"], cwd=ROOT, text=True
        )
        current = ROOT / relative
        assert current.with_name("prior-assessment.md").read_text() == old
        assert old in current.read_text()


def test_existing_manifest_controls_and_blocks_are_preserved():
    for folder in (COURSE / "modules").iterdir():
        path = folder / "module.yaml"
        if not path.exists():
            continue
        original = yaml.safe_load(
            subprocess.check_output(
                ["git", "show", f"{BASELINE}:{path.relative_to(ROOT)}"], cwd=ROOT, text=True
            )
        )
        current = yaml.safe_load(path.read_text())
        assert {k: v for k, v in original.items() if k != "blocks"} == {
            k: v for k, v in current.items() if k != "blocks"
        }
        assert all(block in current["blocks"] for block in original["blocks"])
