from __future__ import annotations

import hashlib
import importlib.util
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
COURSE_ROOT = ROOT / "courses" / "robotics-autonomy"


def _yaml(path: Path) -> dict[str, Any]:
    value, _ = CourseCatalog._read_yaml(path)
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _assert_finite(value: Any) -> None:
    if isinstance(value, bool) or value is None or isinstance(value, str):
        return
    if type(value) in {int, float}:
        assert math.isfinite(float(value))
        return
    if isinstance(value, list):
        for item in value:
            _assert_finite(item)
        return
    if isinstance(value, dict):
        for item in value.values():
            _assert_finite(item)
        return
    raise AssertionError(f"unsupported serialized value {type(value)!r}")


def _load_reference() -> Any:
    path = COURSE_ROOT / "reference_cases.py"
    spec = importlib.util.spec_from_file_location("robotics_reference_cases", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SOURCE_MAP = _yaml(COURSE_ROOT / "source-map.yaml")
MANIFEST = _yaml(COURSE_ROOT / "conversion-manifest.yaml")
COVERAGE = _yaml(COURSE_ROOT / "coverage.yaml")
AUTHORED = [item for item in COVERAGE["items"] if item["status"] == "authored"]
REQUESTED_ITEM = os.environ.get("ELP_ROBOTICS_ITEM")
if REQUESTED_ITEM:
    SELECTED = [item for item in AUTHORED if item["id"] == REQUESTED_ITEM]
    if not SELECTED:
        raise RuntimeError(f"{REQUESTED_ITEM} is not in the authored Robotics prefix")
else:
    SELECTED = AUTHORED
REFERENCE = _load_reference()


@pytest.fixture(scope="module")
def catalog() -> CourseCatalog:
    return CourseCatalog([ROOT / "courses"])


@pytest.fixture(scope="module")
def runtime(catalog: CourseCatalog) -> ExperimentRuntime:
    return ExperimentRuntime(catalog)


@pytest.mark.parametrize("item", SELECTED, ids=lambda item: item["id"])
def test_robotics_item_identity_lesson_and_content_digest(
    item: dict[str, Any],
    catalog: CourseCatalog,
) -> None:
    source = SOURCE_MAP["items"][item["number"] - 1]
    module_root = COURSE_ROOT / item["target_folder"]
    record = _yaml(module_root / "verification.yaml")
    course, module = catalog.module_record("robotics-autonomy", item["target_module_id"])

    assert course.manifest.id == "robotics-autonomy"
    assert module.manifest.number == source["number"]
    assert module.manifest.title == source["title"]
    assert module.manifest.guiding_question == source["guiding_question"]
    assert module.revision.content_digest == item["target_content_digest"]
    assert record["target"]["content_digest"] == module.revision.content_digest
    expected_hashes = {
        identity["path"]: identity["sha256"] for identity in record["target"]["files"]
    }
    actual_hashes = {
        str(module.path.relative_to(COURSE_ROOT) / relative): digest
        for relative, digest in module.input_hashes
    }
    assert expected_hashes == actual_hashes
    for relative, digest in expected_hashes.items():
        assert _sha256(COURSE_ROOT / relative) == digest

    lesson = (module_root / "lesson.md").read_text(encoding="utf-8")
    assert source["title"] in lesson
    assert source["guiding_question"] in lesson
    for concept in (
        "equation",
        "sweep",
        "broken",
        "recovery",
        "mistake",
        "limiting",
        "teach-back",
        "unit",
    ):
        assert re.search(concept, lesson, re.IGNORECASE), f"{item['id']} omits {concept}"
    for sweep in record["learning"]["sweeps"]:
        assert f"`{sweep['control']}`" in lesson


@pytest.mark.parametrize("item", SELECTED, ids=lambda item: item["id"])
def test_robotics_runtime_is_deterministic_bounded_and_interpretable(
    item: dict[str, Any],
    catalog: CourseCatalog,
    runtime: ExperimentRuntime,
) -> None:
    module_root = COURSE_ROOT / item["target_folder"]
    record = _yaml(module_root / "verification.yaml")
    _, module = catalog.module_record("robotics-autonomy", item["target_module_id"])
    first = runtime.run("robotics-autonomy", item["target_module_id"], {}).model_dump(mode="json")
    second = runtime.run("robotics-autonomy", item["target_module_id"], {}).model_dump(mode="json")
    assert _canonical(first) == _canonical(second)
    assert set(first["plots"]) == {"response", "mechanism"}
    assert len(first["metrics"]) >= 3
    assert first["explanations"]["observation"]
    assert first["explanations"]["broken"]
    assert first["explanations"]["recovery"]
    assert first["diagnostics"]["sample_count"] <= record["runtime"]["max_samples"]
    assert len(_canonical(first).encode()) <= record["runtime"]["max_output_bytes"]
    _assert_finite(first)

    for plot in first["plots"].values():
        x_title = plot["layout"]["xaxis"]["title"]
        y_title = plot["layout"]["yaxis"]["title"]
        assert "(" in x_title and ")" in x_title
        assert "(" in y_title and ")" in y_title

    controls = {control.id: control for control in module.manifest.controls}
    for sweep in record["learning"]["sweeps"]:
        control = controls[sweep["control"]]
        low = runtime.run(
            "robotics-autonomy",
            item["target_module_id"],
            {control.id: sweep["values"][0]},
        ).model_dump(mode="json")
        high = runtime.run(
            "robotics-autonomy",
            item["target_module_id"],
            {control.id: sweep["values"][-1]},
        ).model_dump(mode="json")
        assert _canonical(low["diagnostics"]) != _canonical(high["diagnostics"])

    recovered = runtime.run(
        "robotics-autonomy", item["target_module_id"], {"broken_mode": False}
    ).model_dump(mode="json")
    broken = runtime.run(
        "robotics-autonomy", item["target_module_id"], {"broken_mode": True}
    ).model_dump(mode="json")
    assert _canonical(recovered["diagnostics"]) != _canonical(broken["diagnostics"])

    with pytest.raises(RuntimeContractError, match="unknown parameters"):
        runtime.run("robotics-autonomy", item["target_module_id"], {"unreviewed": 1})
    numeric = next(control for control in module.manifest.controls if control.type == "slider")
    with pytest.raises(RuntimeContractError, match="outside"):
        runtime.run(
            "robotics-autonomy",
            item["target_module_id"],
            {numeric.id: numeric.maximum + (numeric.step or 1.0)},
        )


@pytest.mark.parametrize("item", SELECTED, ids=lambda item: item["id"])
def test_robotics_independent_expected_and_actual_evidence(
    item: dict[str, Any],
    runtime: ExperimentRuntime,
) -> None:
    record = _yaml(COURSE_ROOT / item["verification_record"])
    verification = record["python_verification"]
    assert verification["status"] == "passed"
    assert len(verification["cases"]) == 2
    if item["id"] == "P01":
        assert verification["basis"] == "source_design"
    else:
        assert verification["basis"] == "native_python_reference"

    for case in verification["cases"]:
        broken = case["name"] == "broken"
        expected_path = COURSE_ROOT / case["expected"]["path"]
        actual_path = COURSE_ROOT / case["actual"]["path"]
        assert expected_path.read_bytes() != actual_path.read_bytes()
        assert _sha256(expected_path) == case["expected"]["sha256"]
        assert _sha256(actual_path) == case["actual"]["sha256"]
        expected_document = json.loads(expected_path.read_text(encoding="utf-8"))
        actual_document = json.loads(actual_path.read_text(encoding="utf-8"))
        assert expected_document["origin"] == "independent_reference_cases.py"
        assert actual_document["origin"] == "production_experiment.py"

        independent = REFERENCE.expected_signature(item["id"], broken)
        actual = runtime.run(
            "robotics-autonomy",
            item["target_module_id"],
            {"broken_mode": broken},
        ).diagnostics["signature"]
        assert expected_document["signature"] == pytest.approx(independent, abs=1e-9, rel=1e-9)
        assert actual_document["signature"] == pytest.approx(actual, abs=1e-9, rel=1e-9)

        retained_expected = expected_document["signature"]
        retained_actual = actual_document["signature"]
        retained_absolute = max(
            abs(left - right)
            for left, right in zip(retained_expected, retained_actual, strict=True)
        )
        retained_relative = max(
            abs(left - right) / max(abs(left), abs(right), 1.0)
            for left, right in zip(retained_expected, retained_actual, strict=True)
        )
        assert retained_absolute == pytest.approx(case["max_absolute_error"], abs=1e-15)
        assert retained_relative == pytest.approx(case["max_relative_error"], abs=1e-15)

        live_absolute = max(
            abs(left - right) for left, right in zip(independent, actual, strict=True)
        )
        live_relative = max(
            abs(left - right) / max(abs(left), abs(right), 1.0)
            for left, right in zip(independent, actual, strict=True)
        )
        assert live_absolute <= case["tolerance"]["absolute"]
        assert live_relative <= case["tolerance"]["relative"]
        assert case["passed"] is True


def test_robotics_resource_extremes_and_unreachable_ik_remain_bounded(
    runtime: ExperimentRuntime,
) -> None:
    imu = runtime.run(
        "robotics-autonomy",
        "10-integrate-an-imu-and-observe-drift",
        {"duration_s": 60, "sample_rate_hz": 200},
    ).model_dump(mode="json")
    assert imu["diagnostics"]["sample_count"] == 3001
    assert len(_canonical(imu).encode()) < 1_000_000
    _assert_finite(imu)

    ik = runtime.run(
        "robotics-autonomy",
        "04-solve-inverse-kinematics",
        {"target_x_m": 1.5, "target_y_m": 1.5, "link1_m": 0.2, "link2_m": 0.2},
    ).model_dump(mode="json")
    metrics = {metric["id"]: metric for metric in ik["metrics"]}
    assert metrics["reachable"]["value"] == "no"
    assert metrics["target_residual"]["value"] > 0
    _assert_finite(ik)

    bounded_cases = [
        (
            "15-localize-with-a-particle-filter",
            {"particle_count": 1000, "steps": 30},
            1000,
        ),
        (
            "17-search-a-grid-with-a-star",
            {"grid_size": 35, "gap_offset": 7},
            1225,
        ),
        (
            "18-plan-with-random-samples",
            {"sample_budget": 1200, "step_size_m": 0.25, "goal_bias": 0.05},
            1202,
        ),
        (
            "22-meet-real-time-perception-and-control-deadlines",
            {"horizon_ms": 1000},
            1000,
        ),
        (
            "24-validate-autonomy-in-hil",
            {"io_latency_ms": 100, "fault_duration_s": 2, "watchdog_ms": 500},
            601,
        ),
    ]
    for module_id, parameters, sample_limit in bounded_cases:
        result = runtime.run("robotics-autonomy", module_id, parameters).model_dump(mode="json")
        assert result["diagnostics"]["sample_count"] <= sample_limit
        assert len(_canonical(result).encode()) < 1_000_000
        _assert_finite(result)

    software_hil = runtime.run("robotics-autonomy", "24-validate-autonomy-in-hil", {}).model_dump(
        mode="json"
    )
    assert software_hil["diagnostics"]["software_hil_only"] is True
