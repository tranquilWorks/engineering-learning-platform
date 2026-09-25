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
from elp_api.runtime import ExperimentRuntime

ROOT = Path(__file__).resolve().parents[3]
COURSE_ROOT = ROOT / "courses/dsp-radar"
MODULES_ROOT = COURSE_ROOT / "modules"
ITEM_IDS = [f"P{number:02d}" for number in range(2, 11)]
GENERIC_CONTROLS = {"primary_scale", "secondary_scale", "noise_db"}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _module_root(number: int) -> Path:
    values = list(MODULES_ROOT.glob(f"{number:02d}-*"))
    assert len(values) == 1
    return values[0]


def _reference_module() -> Any:
    path = COURSE_ROOT / "remediation_reference_cases.py"
    spec = importlib.util.spec_from_file_location("dsp_remediation_references", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def catalog() -> CourseCatalog:
    return CourseCatalog([COURSE_ROOT])


@pytest.fixture(scope="module")
def runtime(catalog: CourseCatalog) -> ExperimentRuntime:
    return ExperimentRuntime(catalog)


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


def test_control_plane_and_immutable_source_identities() -> None:
    contract = _load_yaml(ROOT / "contracts/active-batch.yaml")
    assert contract["batch"]["id"] == "ELP-DSP-FIDELITY-P11-P20"
    assert contract["sources"]["source_pin"] == "5d73667a486df4a7b6c581e4c9406e810ed4f0f6"
    assert contract["sources"]["source_tree"] == "7a3a0f9adce607e10097724c13745eace212f4e1"
    assert _sha256(COURSE_ROOT / "source-map.yaml") == contract["sources"]["source_map_sha256"]
    assert (
        _sha256(COURSE_ROOT / "conversion-manifest.yaml")
        == contract["sources"]["conversion_manifest_sha256"]
    )


def test_remediation_ledger_preserves_prior_batch_membership() -> None:
    ledger = _load_yaml(COURSE_ROOT / "remediation-map.yaml")
    repaired = ledger["scope"]["repaired_in_prior_batches"]["items"]
    current = ledger["scope"]["repaired_in_batch"]["items"]
    pending = ledger["scope"]["pending"]["items"]
    already = ledger["scope"]["already_distinct"]
    assert repaired == ITEM_IDS
    assert current == [f"P{number:02d}" for number in range(11, 21)]
    assert pending == [f"P{number:02d}" for number in range(21, 85)]
    assert already == ["P01"]
    counts = ledger["derived_counts"]
    assert counts["already_distinct"] == len(already) == 1
    assert counts["repaired_in_prior_batches"] == len(repaired) == 9
    assert counts["repaired_in_batch"] == len(current) == 10
    assert counts["pending"] == len(pending) == 64
    assert counts["total_items"] == len(already) + len(repaired) + len(current) + len(pending) == 84
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

    for number, item_id in zip(range(2, 11), ITEM_IDS, strict=True):
        module_root = _module_root(number)
        manifest = json.loads((module_root / "module.yaml").read_text(encoding="utf-8"))
        controls = {control["id"] for control in manifest["controls"]}
        assert controls.isdisjoint(GENERIC_CONTROLS)
        source = (module_root / "experiment.py").read_text(encoding="utf-8")
        assert "PHASE" not in source
        tree = Normalize().visit(ast.parse(source))
        shapes[item_id] = ast.dump(tree, include_attributes=False)
    assert len(set(shapes.values())) == len(shapes)


@pytest.mark.parametrize("number", range(2, 11), ids=ITEM_IDS)
def test_five_independent_scenarios_are_finite_and_within_tolerance(
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
        np.testing.assert_allclose(actual, expected, rtol=1e-8, atol=1e-8)
        assert all(math.isfinite(value) for value in _finite_leaves(first))
        for plot in first["plots"].values():
            assert plot["layout"]["xaxis"]["title"]
            assert plot["layout"]["yaxis"]["title"]
    source = (COURSE_ROOT / "remediation_reference_cases.py").read_text(encoding="utf-8")
    assert "experiment.py" not in source
    assert "from courses" not in source


def test_source_specific_failures_and_exact_recoveries(
    runtime: ExperimentRuntime, catalog: CourseCatalog
) -> None:
    def run(number: int, broken: bool) -> dict[str, Any]:
        module_id = catalog.course("dsp-radar").modules[number - 1].manifest.id
        result = runtime.run("dsp-radar", module_id, {"broken_mode": broken})
        return result.model_dump(mode="json")["diagnostics"]

    baseline = {number: run(number, False) for number in range(2, 11)}
    broken = {number: run(number, True) for number in range(2, 11)}
    assert broken[2]["sample_count"] == 12
    assert broken[2]["alias_family_hz"] == [5.0, 7.0, 19.0]
    assert broken[2]["reflected_alias_error"] < 1e-10
    assert baseline[3]["sample_agreement_error"] < 1e-10 < broken[3]["sample_agreement_error"]
    assert baseline[4]["max_unclipped_error_v"] <= baseline[4]["half_lsb_v"]
    assert broken[4]["signature"][-1] > 0 and broken[4]["code_max"] == 63
    baseline_rms = [value["rms"] for value in baseline[5]["family_metrics"].values()]
    broken_rms = [value["rms"] for value in broken[5]["family_metrics"].values()]
    assert max(baseline_rms) - min(baseline_rms) < 1e-12
    assert max(broken_rms) - min(broken_rms) > 1.0
    assert max(baseline[6]["direct_convolution_errors"].values()) < 1e-12
    assert broken[6]["circular_wrap_error"] > 1.0
    assert baseline[7]["convolution_error"] == baseline[7]["manual_error"] == 0.0
    assert broken[7]["overwrite_error"] > 0.2
    assert baseline[8]["recovered_delay_samples"] == baseline[8]["true_delay_samples"] == 137
    assert broken[8]["reported_delay_samples"] - broken[8]["recovered_delay_samples"] == 25
    assert broken[9]["broken_tail_ratio"] > 1e5 * broken[9]["recovered_tail_ratio"]
    assert broken[10]["folded_amplitude"] > 100 * baseline[10]["folded_amplitude"]
    assert broken[10]["image_amplitude"] > 100 * baseline[10]["image_amplitude"]


def test_conversion_records_capture_retained_omitted_and_claim_boundary() -> None:
    for number in range(2, 11):
        record = _load_yaml(_module_root(number) / "conversion.yaml")
        flow = " ".join(record["content"]["signal_flow"])
        assert "Retained from the pinned source" in flow
        assert "Deliberately omitted" in flow
        assert "software-only" in flow
        assert record["matlab_runtime_parity"]["status"] == "not_run"
        claim_values = (value for value in record["claims"].values() if isinstance(value, dict))
        assert all(value["status"] == "not_run" for value in claim_values)


def test_catalog_count_and_course_status_remain_bounded(catalog: CourseCatalog) -> None:
    course = catalog.course("dsp-radar")
    assert len(course.modules) == 84
    assert all(module.manifest.runtime.kind == "python" for module in course.modules)
    ledger = _load_yaml(COURSE_ROOT / "remediation-map.yaml")
    assert ledger["claim_boundary"]["numerically_verified"] == "blocked"
    assert ledger["claim_boundary"]["curriculum_covered"] == "blocked"
    assert ledger["claim_boundary"]["capstone_integrated"] == "blocked"
