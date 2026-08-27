from __future__ import annotations

import hashlib
import json
import math
import os
import re
from pathlib import Path
from typing import Any

import pytest

from elp_api.catalog import CourseCatalog
from elp_api.runtime import ExperimentRuntime, RuntimeContractError

ROOT = Path(__file__).resolve().parents[3]
COURSE_ROOT = ROOT / "courses" / "controls-gnc"


def _yaml(path: Path) -> dict[str, Any]:
    value, _ = CourseCatalog._read_yaml(path)
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _numeric_leaves(value: Any) -> list[float]:
    if type(value) in {int, float}:
        number = float(value)
        assert math.isfinite(number)
        return [number]
    if isinstance(value, list):
        return [number for item in value for number in _numeric_leaves(item)]
    if isinstance(value, dict):
        return [number for key in sorted(value) for number in _numeric_leaves(value[key])]
    raise AssertionError(f"nonnumeric evidence leaf: {value!r}")


SOURCE_MAP = _yaml(COURSE_ROOT / "source-map.yaml")
MANIFEST = _yaml(COURSE_ROOT / "conversion-manifest.yaml")
COVERAGE = _yaml(COURSE_ROOT / "coverage.yaml")
CONVERTED = [item for item in COVERAGE["items"] if item["status"] == "converted"]
REQUESTED_ITEM = os.environ.get("ELP_GNC_ITEM")
if REQUESTED_ITEM:
    SELECTED = [item for item in CONVERTED if item["id"] == REQUESTED_ITEM]
    if not SELECTED:
        raise RuntimeError(f"{REQUESTED_ITEM} is not in the retained converted prefix")
else:
    SELECTED = CONVERTED


@pytest.fixture(scope="module")
def catalog() -> CourseCatalog:
    return CourseCatalog([ROOT / "courses"])


@pytest.fixture(scope="module")
def runtime(catalog: CourseCatalog) -> ExperimentRuntime:
    return ExperimentRuntime(catalog)


@pytest.mark.parametrize("item", SELECTED, ids=lambda item: item["id"])
def test_gnc_item_source_content_and_catalog_contract(
    item: dict[str, Any], catalog: CourseCatalog
) -> None:
    index = item["number"] - 1
    source = SOURCE_MAP["items"][index]
    mapped = MANIFEST["items"][index]
    module_root = COURSE_ROOT / item["target_folder"]
    record = _yaml(module_root / "conversion.yaml")
    course, module = catalog.module_record("controls-gnc", item["target_module_id"])

    assert course.manifest.id == "controls-gnc"
    assert module.manifest.id == mapped["target_module_id"]
    assert module.manifest.number == source["number"]
    assert module.manifest.title == source["title"]
    assert module.manifest.guiding_question == source["guiding_question"]
    assert module.revision.content_digest == item["target_content_digest"]
    assert record["target"]["content_digest"] == module.revision.content_digest
    assert record["item"]["source_inputs"] == source["files"]
    assert record["content"]["guiding_question"] == source["guiding_question"]
    assert len(record["content"]["sweeps"]) >= 2
    assert record["content"]["equation_order"] == "before_toolbox_shortcuts"

    expected_hashes = {
        identity["path"]: identity["sha256"] for identity in record["target"]["files"]
    }
    assert expected_hashes == {
        f"{item['target_folder']}/{path}": digest for path, digest in module.input_hashes
    }
    for relative, digest in expected_hashes.items():
        assert _sha256(COURSE_ROOT / relative) == digest

    lesson = (module_root / "lesson.md").read_text(encoding="utf-8")
    assert source["title"] in lesson
    assert source["guiding_question"] in lesson
    for concept in ("equation", "sweep", "broken", "recovery", "mistake", "teach-back"):
        assert re.search(concept, lesson, re.IGNORECASE), f"{item['id']} omits {concept}"

    source_root_value = os.environ.get("ELP_GNC_SOURCE_ROOT")
    if source_root_value:
        source_root = Path(source_root_value)
        for identity in source["files"]:
            assert _sha256(source_root / identity["path"]) == identity["sha256"]


@pytest.mark.parametrize("item", SELECTED, ids=lambda item: item["id"])
def test_gnc_item_runtime_sweeps_and_failure_recovery(
    item: dict[str, Any], catalog: CourseCatalog, runtime: ExperimentRuntime
) -> None:
    module_root = COURSE_ROOT / item["target_folder"]
    record = _yaml(module_root / "conversion.yaml")
    _, module = catalog.module_record("controls-gnc", item["target_module_id"])

    first = runtime.run("controls-gnc", item["target_module_id"], {}).model_dump(mode="json")
    second = runtime.run("controls-gnc", item["target_module_id"], {}).model_dump(mode="json")
    assert _canonical(first) == _canonical(second)
    assert set(first["plots"]) == {"response", "mechanism"}
    assert len(first["metrics"]) >= 3
    assert first["explanations"].get("broken")
    assert first["explanations"].get("recovery")

    controls = {control.id: control for control in module.manifest.controls}
    for sweep in record["content"]["sweeps"][:2]:
        control = controls[sweep["control"]]
        low = runtime.run(
            "controls-gnc", item["target_module_id"], {control.id: sweep["values"][0]}
        ).model_dump(mode="json")
        high = runtime.run(
            "controls-gnc", item["target_module_id"], {control.id: sweep["values"][-1]}
        ).model_dump(mode="json")
        assert _canonical(low["diagnostics"]) != _canonical(high["diagnostics"])

    recovered = runtime.run(
        "controls-gnc", item["target_module_id"], {"broken_mode": False}
    ).model_dump(mode="json")
    broken = runtime.run(
        "controls-gnc", item["target_module_id"], {"broken_mode": True}
    ).model_dump(mode="json")
    assert _canonical(recovered["diagnostics"]) != _canonical(broken["diagnostics"])

    with pytest.raises(RuntimeContractError, match="unknown parameters"):
        runtime.run("controls-gnc", item["target_module_id"], {"unreviewed_parameter": 1})
    numeric = next(control for control in module.manifest.controls if control.type == "slider")
    with pytest.raises(RuntimeContractError, match="outside"):
        runtime.run(
            "controls-gnc",
            item["target_module_id"],
            {numeric.id: numeric.maximum + (numeric.step or 1.0)},
        )


@pytest.mark.parametrize("item", SELECTED, ids=lambda item: item["id"])
def test_gnc_item_retained_numeric_equivalence(item: dict[str, Any]) -> None:
    record = _yaml(COURSE_ROOT / item["conversion_record"])
    equivalence = record["python_source_equivalence"]
    assert equivalence["status"] == "passed"
    assert len(equivalence["cases"]) == 2
    for case in equivalence["cases"]:
        expected_path = COURSE_ROOT / case["expected"]["path"]
        actual_path = COURSE_ROOT / case["actual"]["path"]
        assert expected_path.read_bytes() != actual_path.read_bytes()
        assert _sha256(expected_path) == case["expected"]["sha256"]
        assert _sha256(actual_path) == case["actual"]["sha256"]
        expected = _numeric_leaves(json.loads(expected_path.read_text()))
        actual = _numeric_leaves(json.loads(actual_path.read_text()))
        assert len(expected) == len(actual) > 0
        absolute = max(abs(left - right) for left, right in zip(expected, actual, strict=True))
        relative = max(
            abs(left - right) / max(abs(left), abs(right), 1.0)
            for left, right in zip(expected, actual, strict=True)
        )
        assert absolute == pytest.approx(case["max_absolute_error"], abs=1e-18)
        assert relative == pytest.approx(case["max_relative_error"], abs=1e-18)
        assert absolute <= case["tolerance"]["absolute"]
        assert relative <= case["tolerance"]["relative"]
        assert case["passed"] is True
