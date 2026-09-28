import importlib.util
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def _audit():
    spec = importlib.util.spec_from_file_location(
        "quality_audit", ROOT / "scripts/audit_course_quality.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.audit()


def test_lesson_ledger_matches_actual_payloads_and_does_not_certify_presence():
    actual = _audit()
    assert actual == json.loads((ROOT / "docs/course-quality/lesson-audit.json").read_text())
    assert len(actual["lessons"]) == 288
    assert len({(r["course"], r["module"]) for r in actual["lessons"]}) == 288
    assert sum(r["delivery"] == "source_only" for r in actual["source_repositories"]) == 9
    assert all(r["semantic_review"] != "passed" for r in actual["lessons"])
    assert all(r["manual_learner_validation"] == "not_run" for r in actual["lessons"])
    blocked = {
        (r["course"], r["number"]) for r in actual["lessons"] if r["semantic_review"] == "blocked"
    }
    assert len(blocked) == 72
    assert {("controls-gnc", n) for n in (36, 43, 49, 55, 56, 60, 61, 66, 67, 68)} <= blocked
    assert {("robotics-autonomy", n) for n in (*range(25, 49), 52, 68, 69)} <= blocked
    assert {("vehicle-dynamics", n) for n in range(61, 68)} <= blocked
    assert {("vehicle-dynamics", n) for n in range(1, 17)} <= blocked


def test_browser_projection_keeps_confirmed_limitations_attached_to_lesson():
    audit = _audit()
    projection = json.loads((ROOT / "apps/web/src/lesson-quality.json").read_text())
    assert len(projection) == 288
    assert [(r["course"], r["module"], r["known_issue"]) for r in projection] == [
        (r["course"], r["module"], r["known_issue"]) for r in audit["lessons"]
    ]


def test_delivery_batch_preserves_every_course_and_source_pin():
    changed = subprocess.check_output(
        [
            "git",
            "diff",
            "--name-only",
            "b8d760e6721ae0b94aaa503f4ca1599592266442",
            "--",
            "courses",
            ".gitmodules",
        ],
        cwd=ROOT,
        text=True,
    )
    assert not changed
