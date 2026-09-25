from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pytest
import yaml

from elp_api.catalog import CourseCatalog
from elp_api.runtime import ExperimentRuntime, RuntimeContractError

ROOT = Path(__file__).resolve().parents[3]
COURSE_ROOT = ROOT / "courses/dsp-radar"
SOURCE_ROOT = ROOT / "courses/dsp-radar-learning"
MODULES_ROOT = COURSE_ROOT / "modules"
ITEM_IDS = [f"P{number:02d}" for number in range(11, 21)]
GENERIC_CONTROLS = {"primary_scale", "secondary_scale", "noise_db"}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _module_root(number: int, root: Path = MODULES_ROOT) -> Path:
    values = list(root.glob(f"{number:02d}-*"))
    assert len(values) == 1
    return values[0]


def _reference_module() -> Any:
    path = COURSE_ROOT / "remediation_reference_cases.py"
    spec = importlib.util.spec_from_file_location("dsp_p11_p20_references", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _finite_leaves(value: Any) -> list[float]:
    if isinstance(value, bool) or value is None or isinstance(value, str):
        return []
    if isinstance(value, (int, float)):
        return [float(value)]
    if isinstance(value, list):
        return [number for item in value for number in _finite_leaves(item)]
    if isinstance(value, dict):
        return [number for item in value.values() for number in _finite_leaves(item)]
    raise AssertionError(f"unexpected runtime value {type(value)!r}")


@pytest.fixture(scope="module")
def catalog() -> CourseCatalog:
    return CourseCatalog([COURSE_ROOT])


@pytest.fixture(scope="module")
def runtime(catalog: CourseCatalog) -> ExperimentRuntime:
    return ExperimentRuntime(catalog)


def _run_scenario(
    number: int,
    scenario: str,
    runtime: ExperimentRuntime,
    catalog: CourseCatalog,
) -> dict[str, Any]:
    references = _reference_module()
    item_id = f"P{number:02d}"
    module_id = catalog.course("dsp-radar").modules[number - 1].manifest.id
    result = runtime.run("dsp-radar", module_id, references.SCENARIOS[item_id][scenario])
    return result.model_dump(mode="json")


def test_exact_control_source_and_immutable_framework_identities() -> None:
    contract = _load_yaml(ROOT / "contracts/active-batch.yaml")
    assert contract["batch"]["id"] == "ELP-DSP-FIDELITY-P11-P20"
    assert contract["sources"]["baseline_commit"] == "a24818f42ff267394ee4ec97727ddb7d1978e3f4"
    assert contract["sources"]["baseline_tree"] == "1b5f62cc0adaa1796c459e7def317405cea4fe37"
    assert contract["sources"]["source_pin"] == "5d73667a486df4a7b6c581e4c9406e810ed4f0f6"
    assert contract["sources"]["source_tree"] == "7a3a0f9adce607e10097724c13745eace212f4e1"
    assert _sha256(COURSE_ROOT / "source-map.yaml") == contract["sources"]["source_map_sha256"]
    assert (
        _sha256(COURSE_ROOT / "conversion-manifest.yaml")
        == contract["sources"]["conversion_manifest_sha256"]
    )
    assert (
        _sha256(COURSE_ROOT / "course.yaml")
        == "9950220969a64e5c7faed96ae1f8a2395339c7dbd292a9471c89001a2a5d0228"
    )


def test_titles_questions_and_source_lessons_remain_bound_to_the_pin() -> None:
    manifest = _load_yaml(COURSE_ROOT / "conversion-manifest.yaml")
    for number in range(11, 21):
        target_root = _module_root(number)
        source_root = _module_root(number, SOURCE_ROOT / "modules")
        module = json.loads((target_root / "module.yaml").read_text(encoding="utf-8"))
        mapped = manifest["items"][number - 1]
        assert module["title"] == mapped["title"]
        assert module["guiding_question"] == mapped["guiding_question"]
        source_lesson = (source_root / "lesson.md").read_text(encoding="utf-8").rstrip()
        target_lesson = (target_root / "lesson.md").read_text(encoding="utf-8")
        assert target_lesson.startswith(source_lesson)


def test_remediation_ledger_distinguishes_prior_current_and_pending() -> None:
    ledger = _load_yaml(COURSE_ROOT / "remediation-map.yaml")
    scope = ledger["scope"]
    assert scope["already_distinct"] == ["P01"]
    assert scope["repaired_in_prior_batches"]["items"] == [
        f"P{number:02d}" for number in range(2, 11)
    ]
    assert scope["repaired_in_batch"]["batch_id"] == "ELP-DSP-FIDELITY-P11-P20"
    assert scope["repaired_in_batch"]["items"] == ITEM_IDS
    assert scope["pending"]["items"] == [f"P{number:02d}" for number in range(21, 85)]
    assert ledger["derived_counts"] == {
        "rule": (
            "total_items = already_distinct + repaired_in_prior_batches + "
            "repaired_in_batch + pending"
        ),
        "total_items": 84,
        "already_distinct": 1,
        "repaired_in_prior_batches": 9,
        "repaired_in_batch": 10,
        "pending": 64,
    }
    assert ledger["claim_boundary"]["numerically_verified"] == "blocked"
    assert ledger["claim_boundary"]["curriculum_covered"] == "blocked"
    assert ledger["claim_boundary"]["capstone_integrated"] == "blocked"


def test_repaired_controls_and_normalized_program_shapes_are_distinct() -> None:
    shapes: dict[str, str] = {}

    class Normalize(ast.NodeTransformer):
        def visit_Name(self, node: ast.Name) -> ast.AST:
            return ast.copy_location(ast.Name(id="name", ctx=node.ctx), node)

        def visit_arg(self, node: ast.arg) -> ast.AST:
            return ast.copy_location(ast.arg(arg="argument", annotation=None), node)

        def visit_Constant(self, node: ast.Constant) -> ast.AST:
            value: object = "text" if isinstance(node.value, str) else 0
            return ast.copy_location(ast.Constant(value=value), node)

    for number in range(2, 21):
        module_root = _module_root(number)
        module = json.loads((module_root / "module.yaml").read_text(encoding="utf-8"))
        controls = {control["id"] for control in module["controls"]}
        if number >= 11:
            assert controls.isdisjoint(GENERIC_CONTROLS)
        source = (module_root / "experiment.py").read_text(encoding="utf-8")
        assert "PHASE" not in source
        normalized = Normalize().visit(ast.parse(source))
        shapes[f"P{number:02d}"] = ast.dump(normalized, include_attributes=False)
    assert len(set(shapes.values())) == len(shapes)


@pytest.mark.parametrize("number", range(11, 21), ids=ITEM_IDS)
def test_five_independent_scenarios_are_deterministic_finite_and_within_tolerance(
    number: int, runtime: ExperimentRuntime, catalog: CourseCatalog
) -> None:
    references = _reference_module()
    item_id = f"P{number:02d}"
    module_id = catalog.course("dsp-radar").modules[number - 1].manifest.id
    record = _load_yaml(_module_root(number) / "conversion.yaml")
    assert [case["name"] for case in record["python_source_equivalence"]["cases"]] == [
        "baseline",
        "sweep_1",
        "sweep_2",
        "broken",
        "recovery",
    ]
    for scenario, parameters in references.SCENARIOS[item_id].items():
        first = runtime.run("dsp-radar", module_id, parameters).model_dump(mode="json")
        second = runtime.run("dsp-radar", module_id, parameters).model_dump(mode="json")
        assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)
        actual = np.asarray(first["diagnostics"]["signature"], dtype=float)
        expected = np.asarray(references.expected_signature(item_id, scenario), dtype=float)
        np.testing.assert_allclose(actual, expected, rtol=0.0001, atol=0.0001)
        assert all(math.isfinite(value) for value in _finite_leaves(first))
        for plot in first["plots"].values():
            assert plot["layout"]["xaxis"]["title"]
            assert plot["layout"]["yaxis"]["title"]
    source = (COURSE_ROOT / "remediation_reference_cases.py").read_text(encoding="utf-8")
    assert "experiment.py" not in source
    assert "from courses" not in source


def test_invalid_and_resource_exceeding_controls_fail_before_execution(
    runtime: ExperimentRuntime, catalog: CourseCatalog
) -> None:
    invalid = {
        11: {"record_sample_count": 1_000_000},
        12: {"window_name": "Kaiser"},
        13: {"padding_factor": 1_000_000},
        14: {"segment_length": 4096},
        15: {"window_length": 4096},
        16: {"envelope_depth": 1.0},
        17: {"lo_frequency_hz": 1_000_000.0},
        18: {"sample_rate_hz": 1_000_000.0},
        19: {"i_gain": 100.0},
        20: {"record_sample_count": 1_000_000},
    }
    for number, parameters in invalid.items():
        module_id = catalog.course("dsp-radar").modules[number - 1].manifest.id
        with pytest.raises(RuntimeContractError):
            runtime.run("dsp-radar", module_id, parameters)


def test_source_specific_failures_and_recoveries(
    runtime: ExperimentRuntime, catalog: CourseCatalog
) -> None:
    results = {
        number: {
            scenario: _run_scenario(number, scenario, runtime, catalog)["diagnostics"]["signature"]
            for scenario in ("baseline", "broken", "recovery")
        }
        for number in range(11, 21)
    }
    assert results[11]["baseline"][7] < 1e-10
    assert results[11]["broken"][6] - results[11]["broken"][5] == results[11]["broken"][2]
    assert results[12]["broken"][8] != results[12]["broken"][7]
    assert results[12]["recovery"][8] == results[12]["recovery"][7]
    assert results[13]["broken"][7] == results[13]["broken"][4]
    assert results[13]["recovery"][7] == results[13]["recovery"][5]
    assert results[14]["baseline"][3] <= results[14]["baseline"][2]
    assert results[14]["baseline"][7] < results[14]["baseline"][6]
    assert results[14]["broken"][10] == results[14]["broken"][9] < results[14]["broken"][8]
    assert results[15]["broken"][8] == 2.0
    assert results[15]["recovery"][8] == results[15]["recovery"][5] == 64.0
    assert results[15]["baseline"][9] < 10.0
    assert results[16]["broken"][5] < 0.05
    assert results[16]["broken"][6] > 100 and results[16]["broken"][7] > 0
    assert results[16]["recovery"][7] == 0
    assert results[17]["broken"][2] > 0 > results[17]["broken"][3]
    assert results[17]["recovery"][2] == pytest.approx(results[17]["recovery"][3], abs=0.01)
    assert abs(results[17]["baseline"][4] - 1.0) < 0.01
    assert abs(results[18]["broken"][4]) < 1e-12 and abs(results[18]["broken"][5]) < 1e-12
    assert results[18]["recovery"][4] == pytest.approx(160.0, abs=0.01)
    assert results[18]["recovery"][5] == pytest.approx(-160.0, abs=0.01)
    assert results[18]["baseline"][11] == pytest.approx(160.0, abs=0.01)
    assert results[18]["baseline"][12] == pytest.approx(-160.0, abs=0.01)
    assert results[18]["baseline"][13] < 0.001
    assert results[19]["broken"][6] < results[19]["recovery"][6] - 30
    assert results[19]["recovery"][8] == pytest.approx(1.0, abs=0.01)
    assert results[19]["baseline"][14] > results[19]["baseline"][2] - 1.0
    assert results[19]["baseline"][15] != results[19]["baseline"][16]
    assert abs(results[20]["broken"][13] - 123.25) > 100
    assert results[20]["recovery"][10] == pytest.approx(123.25, abs=1e-10)
    assert abs(results[20]["recovery"][13] - 123.25) < 2.0
    assert results[20]["recovery"][11] < 0.20 and results[20]["recovery"][12] == 0.0
    assert results[20]["baseline"][15] > 0
    assert results[20]["baseline"][16] > 0
    assert results[20]["baseline"][17] > 0.20


def test_conversion_records_capture_retained_omitted_and_claim_boundary() -> None:
    for number in range(11, 21):
        record = _load_yaml(_module_root(number) / "conversion.yaml")
        flow = " ".join(record["content"]["signal_flow"])
        assert "Retained from the pinned source" in flow
        assert "Deliberately omitted" in flow
        assert "software-only" in flow
        assert record["matlab_runtime_parity"]["status"] == "not_run"
        claim_values = (value for value in record["claims"].values() if isinstance(value, dict))
        assert all(value["status"] == "not_run" for value in claim_values)


def test_six_course_290_module_catalog_and_claim_blocks_remain_exact() -> None:
    catalog = CourseCatalog([ROOT / "courses"])
    courses = catalog.summaries()
    assert len(courses) == 6
    modules = [module for course in courses for module in course.modules]
    assert len(modules) == 290
    assert sum(module.interactive for module in modules) == 290
    ledger = _load_yaml(COURSE_ROOT / "remediation-map.yaml")
    assert ledger["claim_boundary"]["numerically_verified"] == "blocked"
    assert ledger["claim_boundary"]["curriculum_covered"] == "blocked"
    assert ledger["claim_boundary"]["capstone_integrated"] == "blocked"
