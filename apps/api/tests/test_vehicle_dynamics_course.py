from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path
from typing import Any

import pytest

from elp_api.catalog import CourseCatalog

ROOT = Path(__file__).resolve().parents[3]
COURSE = ROOT / "courses/vehicle-dynamics"
IDS = [
    "01-turn-steering-and-speed-into-a-vehicle-path",
    "02-relate-acceleration-to-tire-force",
    "03-see-longitudinal-weight-transfer",
    "04-use-the-friction-circle",
    "05-build-slip-ratio-intuition",
    "06-build-slip-angle-intuition",
    "07-use-the-bicycle-model",
    "08-separate-understeer-from-oversteer",
]


def _load(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


REFERENCE = _load(COURSE / "reference_cases.py", "vehicle_reference")


def test_exact_membership_provenance_evidence_and_digests() -> None:
    roots = sorted(path.parent for path in (COURSE / "modules").glob("*/module.yaml"))
    assert [path.name for path in roots] == IDS
    coverage, _ = CourseCatalog._read_yaml(COURSE / "coverage.yaml")
    catalog = CourseCatalog([ROOT / "courses"]).course("vehicle-dynamics")
    digests = {item.manifest.number: item.revision.content_digest for item in catalog.modules}
    for number, root in enumerate(roots, 1):
        manifest, _ = CourseCatalog._read_yaml(root / "module.yaml")
        verification, _ = CourseCatalog._read_yaml(root / "verification.yaml")
        expected = json.loads((root / "expected.json").read_text())
        actual = json.loads((root / "actual.json").read_text())
        assert manifest["number"] == number and manifest["status"] == "implemented"
        provenance = "implemented-source comparison" if number <= 2 else "Python-first native"
        assert verification["provenance"] == provenance
        assert not verification["reference"]["imports_production"]
        assert not verification["reference"]["consumes_production_output"]
        assert expected == actual
        assert list(expected) == ["baseline", "sweep_1", "sweep_2", "broken", "recovery"]
        assert expected["baseline"] == expected["recovery"]
        assert coverage["items"][number - 1]["target_content_digest"] == digests[number]


@pytest.mark.parametrize(("number", "module_id"), list(enumerate(IDS, 1)))
def test_scenarios_reference_determinism_limits_and_outputs(number: int, module_id: str) -> None:
    root = COURSE / "modules" / module_id
    manifest, _ = CourseCatalog._read_yaml(root / "module.yaml")
    experiment = _load(root / "experiment.py", f"vehicle_{number}")
    primary, secondary = manifest["controls"][:2]
    cases = [
        (primary["default"], secondary["default"], False),
        (primary["minimum"], secondary["default"], False),
        (primary["default"], secondary["maximum"], False),
        (primary["default"], secondary["default"], True),
    ]
    for p_value, s_value, broken in cases:
        inputs = {primary["id"]: p_value, secondary["id"]: s_value, "broken_mode": broken}
        first = experiment.run(inputs)
        assert first == experiment.run(inputs)
        signature = first["diagnostics"]["signature"]
        assert signature == pytest.approx(
            REFERENCE.evaluate(f"P{number:02d}", p_value, s_value, broken), abs=1e-10, rel=1e-10
        )
        assert all(math.isfinite(value) for value in signature)
        assert set(first["plots"]) == {
            "response",
            "primary_sweep",
            "secondary_sweep",
            "broken_recovery",
        }
    with pytest.raises(ValueError, match="outside declared finite range"):
        experiment.run(
            {
                primary["id"]: primary["maximum"] + abs(primary["step"]),
                secondary["id"]: secondary["default"],
                "broken_mode": False,
            }
        )


def test_lessons_and_catalog_boundary() -> None:
    for root in sorted((COURSE / "modules").glob("*")):
        lesson = (root / "lesson.md").read_text().lower()
        for phrase in (
            "physical model",
            "predict and sweep",
            "named broken behavior",
            "exact recovery",
            "limits and limiting cases",
            "common mistakes",
            "formative checks",
            "teach-back checklist",
            "not measured-vehicle",
        ):
            assert phrase in lesson
    summaries = CourseCatalog([ROOT / "courses"]).summaries()
    assert len(summaries) == 6
    assert sum(len(course.modules) for course in summaries) == 231
    assert sum(module.interactive for course in summaries for module in course.modules) == 231
