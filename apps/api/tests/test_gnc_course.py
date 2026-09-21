from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import os
import re
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from elp_api.catalog import CourseCatalog
from elp_api.runtime import ExperimentRuntime, RuntimeContractError

ROOT = Path(__file__).resolve().parents[3]
COURSE_ROOT = ROOT / "courses" / "controls-gnc"
SCENARIOS = ("baseline", "sweep_1", "sweep_2", "broken", "recovery")
GENERIC_LABELS = {
    "Independent variable",
    "Response",
    "Diagnostic",
    "source units",
    "output",
    "actuator",
    "measurement",
    "units",
    "cost",
}


def _yaml(path: Path) -> dict[str, Any]:
    value, _ = CourseCatalog._read_yaml(path)
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


REFERENCE = _load_module(COURSE_ROOT / "reference_cases.py", "gnc_independent_references")
SOURCE_MAP = _yaml(COURSE_ROOT / "source-map.yaml")
MANIFEST = _yaml(COURSE_ROOT / "conversion-manifest.yaml")
COVERAGE = _yaml(COURSE_ROOT / "coverage.yaml")
CONVERTED = [item for item in COVERAGE["items"] if item["status"] == "converted"]
REQUESTED_ITEM = os.environ.get("ELP_GNC_ITEM")
if REQUESTED_ITEM:
    SELECTED = [item for item in CONVERTED if item["id"] == REQUESTED_ITEM]
    if not SELECTED:
        raise RuntimeError(f"{REQUESTED_ITEM} is not in the converted P01-P24 inventory")
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
    assert len(record["content"]["sweeps"]) == 2
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
    for sweep in record["content"]["sweeps"]:
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
def test_gnc_item_five_scenario_independent_equivalence(
    item: dict[str, Any], runtime: ExperimentRuntime
) -> None:
    module_root = COURSE_ROOT / item["target_folder"]
    record = _yaml(module_root / "conversion.yaml")
    equivalence = record["python_source_equivalence"]
    assert equivalence["status"] == "passed"
    assert equivalence["reference_origin"] == {
        **REFERENCE.origin(item["number"]),
        "package": {
            "path": "reference_cases.py",
            "sha256": _sha256(COURSE_ROOT / "reference_cases.py"),
        },
    }
    assert equivalence["production_origin"]["independent"] is False
    assert equivalence["production_origin"]["imports_production_entrypoint"] is True
    assert equivalence["production_origin"]["derived_from_production_output"] is True
    assert equivalence["production_origin"]["perturbs_production_output"] is False
    assert [case["scenario"] for case in equivalence["cases"]] == list(SCENARIOS)

    expected_path = COURSE_ROOT / equivalence["cases"][0]["expected"]["path"]
    actual_path = COURSE_ROOT / equivalence["cases"][0]["actual"]["path"]
    assert expected_path.name == "expected-independent.json"
    assert actual_path.name == "actual-production.json"
    assert sorted(path.name for path in (module_root / "evidence").glob("*.json")) == [
        "actual-production.json",
        "expected-independent.json",
    ]
    expected = json.loads(expected_path.read_text())
    actual = json.loads(actual_path.read_text())
    assert expected["origin"] == equivalence["reference_origin"]
    assert actual["origin"] == equivalence["production_origin"]
    assert expected["signature_fields"] == actual["signature_fields"]
    assert expected_path.read_bytes() != actual_path.read_bytes()

    for case in equivalence["cases"]:
        scenario = case["scenario"]
        assert case["evidence_key"] == scenario
        assert case["parameters"] == expected["cases"][scenario]["parameters"]
        assert case["parameters"] == actual["cases"][scenario]["parameters"]
        assert _sha256(expected_path) == case["expected"]["sha256"]
        assert _sha256(actual_path) == case["actual"]["sha256"]

        regenerated_expected = REFERENCE.reference_signature(item["number"], case["parameters"])
        regenerated_actual = runtime.run(
            "controls-gnc", item["target_module_id"], case["parameters"]
        ).diagnostics["signature"]
        assert regenerated_expected == pytest.approx(
            expected["cases"][scenario]["signature"], abs=0, rel=0
        )
        assert regenerated_actual == pytest.approx(
            actual["cases"][scenario]["signature"], abs=0, rel=0
        )

        expected_values = np.asarray(regenerated_expected, dtype=float)
        actual_values = np.asarray(regenerated_actual, dtype=float)
        assert len(expected_values) == len(actual_values) == len(expected["signature_fields"])
        assert np.all(np.isfinite(expected_values))
        assert np.all(np.isfinite(actual_values))
        difference = np.abs(expected_values - actual_values)
        scale = float(max(np.max(np.abs(expected_values)), np.max(np.abs(actual_values)), 1.0))
        absolute = float(np.max(difference))
        relative = float(
            np.max(
                difference
                / np.maximum.reduce(
                    [np.abs(expected_values), np.abs(actual_values), np.ones_like(difference)]
                )
            )
        )
        allowed_absolute = max(case["tolerance"]["absolute"], case["tolerance"]["relative"] * scale)
        assert scale == pytest.approx(case["comparison_scale"], abs=1e-15, rel=1e-15)
        assert allowed_absolute == pytest.approx(
            case["allowed_absolute_error"], abs=1e-15, rel=1e-15
        )
        assert absolute == pytest.approx(case["max_absolute_error"], abs=1e-15, rel=1e-15)
        assert relative == pytest.approx(case["max_relative_error"], abs=1e-15, rel=1e-15)
        assert absolute <= allowed_absolute
        assert relative <= case["tolerance"]["relative"]

        description, expected_invariant = REFERENCE.teaching_invariant(
            item["number"], case["parameters"], regenerated_expected
        )
        _, actual_invariant = REFERENCE.teaching_invariant(
            item["number"], case["parameters"], regenerated_actual
        )
        assert case["teaching_invariant"] == {
            "description": description,
            "reference_passed": expected_invariant,
            "production_passed": actual_invariant,
        }
        assert expected_invariant and actual_invariant and case["passed"]

    assert expected["cases"]["baseline"] == expected["cases"]["recovery"]
    assert actual["cases"]["baseline"] == actual["cases"]["recovery"]
    assert expected["cases"]["broken"]["signature"] != expected["cases"]["recovery"]["signature"]


@pytest.mark.parametrize("item", SELECTED, ids=lambda item: item["id"])
def test_gnc_plot_axes_are_quantity_and_unit_specific(
    item: dict[str, Any], runtime: ExperimentRuntime
) -> None:
    result = runtime.run("controls-gnc", item["target_module_id"], {}).model_dump(mode="json")
    for plot in result["plots"].values():
        layout = plot["layout"]
        for key, value in layout.items():
            if not re.fullmatch(r"[xy]axis[1-9]?", key):
                continue
            title = value["title"]["text"]
            assert title not in GENERIC_LABELS
            assert re.search(r"\([^()]+\)$", title), title

        axis_units: dict[tuple[str, str], set[str]] = {}
        for trace in plot["data"]:
            meta = trace["meta"]
            assert set(meta) == {"x_quantity", "x_unit", "y_quantity", "y_unit"}
            assert all(str(value).strip() for value in meta.values())
            assert meta["x_unit"] not in GENERIC_LABELS
            assert meta["y_unit"] not in GENERIC_LABELS
            xaxis = trace.get("xaxis", "x")
            yaxis = trace.get("yaxis", "y")
            assert f"xaxis{xaxis[1:]}" in layout
            assert f"yaxis{yaxis[1:]}" in layout
            axis_units.setdefault(("x", xaxis), set()).add(meta["x_unit"])
            axis_units.setdefault(("y", yaxis), set()).add(meta["y_unit"])
        assert all(len(units) == 1 for units in axis_units.values())


def test_gnc_focused_control_and_guidance_invariants(runtime: ExperimentRuntime) -> None:
    def signature(number: int, supplied: dict[str, Any]) -> list[float]:
        item = CONVERTED[number - 1]
        return runtime.run("controls-gnc", item["target_module_id"], supplied).diagnostics[
            "signature"
        ]

    p03 = signature(3, {"broken_mode": False})
    p03_broken = signature(3, {"broken_mode": True})
    assert p03[0] < 0 < p03_broken[0]
    assert p03[2] * p03[1] == pytest.approx(2 * math.pi)

    assert signature(7, {"broken_mode": False})[2] > 0
    assert signature(7, {"broken_mode": True})[2] < 0
    assert signature(9, {"broken_mode": True})[0] == pytest.approx(0.3)
    p10 = signature(10, {"sample_period_s": 0.1, "delay_fraction": 0.4})
    assert p10[2] == pytest.approx(p10[0] * p10[1])

    assert 0 < signature(11, {"broken_mode": True})[2] <= 1
    assert signature(12, {"broken_mode": True})[2] == -1
    assert signature(13, {"broken_mode": False})[2] == 2
    assert signature(13, {"broken_mode": True})[2] == 1
    assert signature(14, {"broken_mode": False})[3] == 2
    assert signature(14, {"broken_mode": True})[3] == 1

    assert abs(signature(15, {"broken_mode": False})[-2]) < 0.02
    assert np.isfinite(signature(16, {"broken_mode": True})[3])
    assert signature(17, {"broken_mode": True})[2:5] == pytest.approx([0, 0, 0])
    assert signature(19, {"broken_mode": False})[2] == 1
    assert signature(19, {"broken_mode": True})[2] == -1

    p20_lesson = (
        (COURSE_ROOT / "modules/20-compare-nominal-and-robust-designs/lesson.md")
        .read_text()
        .lower()
    )
    assert "two preselected proportional gains" in p20_lesson
    assert "not robust-control synthesis" in p20_lesson
    assert "12 candidates and 25 positive plant points" in p20_lesson

    assert signature(21, {"broken_mode": False})[-1] == 1
    assert signature(21, {"broken_mode": True})[-1] == 0
    p22_broken = signature(22, {"broken_mode": True})
    assert p22_broken[-1] <= p22_broken[1] + 1e-12
    assert p22_broken[3] == 0
    p23_broken = signature(23, {"broken_mode": True})
    assert p23_broken[0:3] == pytest.approx([0.8, 0.6, 0.1])

    p24_zero_latency = signature(24, {"one_way_latency_s": 0.0})
    p24_broken = signature(24, {"broken_mode": True})
    assert p24_zero_latency[1] == 0
    assert p24_zero_latency[-1] == 0
    assert p24_broken[3] == 2
    assert p24_broken[-1] > 0
