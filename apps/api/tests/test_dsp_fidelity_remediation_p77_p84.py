from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np
import pytest
import yaml

from elp_api.catalog import CourseCatalog
from elp_api.runtime import ExperimentRuntime, RuntimeContractError

ROOT = Path(__file__).resolve().parents[3]
COURSE = ROOT / "courses/dsp-radar"
SOURCE = ROOT / "courses/dsp-radar-learning"


def _load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _folder(number):
    return next((COURSE / "modules").glob(f"{number}-*"))


def _sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture(scope="module")
def references():
    return _load(COURSE / "remediation_reference_cases.py")


@pytest.fixture(scope="module")
def runtime():
    return ExperimentRuntime(CourseCatalog([ROOT / "courses"]))


@pytest.fixture(scope="module")
def scenarios(runtime, references):
    return {
        n: {
            name: runtime.run("dsp-radar", _folder(n).name, p).model_dump(mode="json")
            for name, p in references.SCENARIOS[f"P{n}"].items()
        }
        for n in range(77, 85)
    }


@pytest.mark.parametrize("number", range(77, 85))
def test_source_bound_identity_content_and_stage_wiring(number, references):
    folder = _folder(number)
    manifest = yaml.safe_load((folder / "module.yaml").read_text())
    record = json.loads((folder / "conversion.yaml").read_text())
    assert (
        yaml.safe_load((folder / "conversion.yaml").read_text())["content"]["sweeps"]
        == record["content"]["sweeps"]
    )
    source_folder = SOURCE / "modules" / folder.name
    assert (
        (folder / "lesson.md")
        .read_text()
        .startswith((source_folder / "lesson.md").read_text().rstrip())
    )
    for source_input in record["item"]["source_inputs"]:
        assert _sha(SOURCE / source_input["path"]) == source_input["sha256"]
    assert manifest["guiding_question"] == record["content"]["guiding_question"]
    controls = {c["id"] for c in manifest["controls"]}
    assert controls == set(references.SCENARIOS[f"P{number}"]["baseline"])
    assert controls.isdisjoint({"primary_scale", "secondary_scale", "noise_db"})
    assert "PHASE" not in (folder / "experiment.py").read_text()
    assert record["matlab_runtime_parity"]["status"] == "not_run"
    assert all(
        record["claims"][key]["status"] == "not_run"
        for key in ["browser_visual_review", "accessibility_review", "learner_effectiveness"]
    )
    assert [c["name"] for c in record["python_source_equivalence"]["cases"]] == list(
        references.SCENARIOS[f"P{number}"]
    )


@pytest.mark.parametrize("number", range(77, 85))
@pytest.mark.parametrize("name", ["baseline", "sweep_1", "sweep_2", "broken", "recovery"])
def test_independent_saved_live_evidence_and_determinism(
    number, name, references, runtime, scenarios
):
    result = scenarios[number][name]
    repeat = runtime.run(
        "dsp-radar", _folder(number).name, references.SCENARIOS[f"P{number}"][name]
    ).model_dump(mode="json")
    assert result == repeat
    encoded = json.dumps(result, allow_nan=False)
    assert len(encoded.encode()) < 1_000_000
    expected = references.expected_signature(f"P{number}", name)
    actual = result["diagnostics"]["signature"]
    assert len(expected) == len(actual) == len(result["metrics"])
    np.testing.assert_allclose(actual, expected, atol=1e-8, rtol=1e-8)
    record = json.loads((_folder(number) / "conversion.yaml").read_text())
    case = next(c for c in record["python_source_equivalence"]["cases"] if c["name"] == name)
    for label, live in [("expected", expected), ("actual", actual)]:
        path = COURSE / case[label]["path"]
        assert _sha(path) == case[label]["sha256"]
        np.testing.assert_allclose(live, json.loads(path.read_text()), atol=1e-8, rtol=1e-8)
    difference = np.abs(np.array(expected) - actual)
    assert np.max(difference) <= case["tolerance"]["absolute"] == 1e-8
    assert np.max(difference / np.maximum(1, np.abs(expected))) <= 1e-8
    # Historical error metadata is checked using its retained pair, not fresh roundoff extrema.
    saved_expected = np.array(json.loads((COURSE / case["expected"]["path"]).read_text()))
    saved_actual = np.array(json.loads((COURSE / case["actual"]["path"]).read_text()))
    saved_error = abs(saved_expected - saved_actual)
    assert max(saved_error) == pytest.approx(case["max_absolute_error"], abs=1e-15)
    assert max(saved_error / np.maximum(1, abs(saved_expected))) == pytest.approx(
        case["max_relative_error"], abs=1e-15
    )
    for plot in result["plots"].values():
        assert "(" in plot["layout"]["xaxis"]["title"]
        assert "(" in plot["layout"]["yaxis"]["title"]
        for trace in plot["data"]:
            if trace["type"] == "heatmap":
                assert 0 < len(trace["x"]) <= 128 and 0 < len(trace["y"]) <= 64
                assert np.asarray(trace["z"]).shape == (len(trace["y"]), len(trace["x"]))
            else:
                assert 0 < len(trace["x"]) == len(trace["y"]) <= 512
    manifest = yaml.safe_load((_folder(number) / "module.yaml").read_text())
    wired = {block["plot"] for block in manifest["blocks"] if block["type"] == "plot"}
    assert wired == set(result["plots"])


def test_independent_reference_provenance_and_no_production_imports(references):
    text = (COURSE / "remediation_reference_cases.py").read_text()
    assert "experiment.py" not in text
    assert "importlib" not in text and "elp_api" not in text
    for number in range(77, 85):
        provenance = json.loads((_folder(number) / "evidence/provenance.json").read_text())
        assert provenance["reference"]["independent"] is True
        assert provenance["reference"]["imports_production"] is False
        # Historical provenance binds the exact append-only prefix for this batch.
        prior_bytes = (COURSE / "remediation_reference_cases.py").read_bytes()
        assert (
            provenance["reference"]["sha256"]
            == hashlib.sha256(prior_bytes[: provenance["reference"]["byte_count"]]).hexdigest()
        )
        assert provenance["production"]["sha256"] == _sha(_folder(number) / "experiment.py")
        assert provenance["scenarios"] == references.SCENARIOS[f"P{number}"]


def _values(scenarios, number, name="baseline"):
    return {m["id"]: m["value"] for m in scenarios[number][name]["metrics"]}


def test_distinct_sweeps_named_failures_and_exact_recovery(scenarios):
    for number in range(77, 85):
        assert scenarios[number]["baseline"] == scenarios[number]["recovery"]
        base = _values(scenarios, number)
        assert base["model_valid"] == 1
        for name in ["sweep_1", "sweep_2", "broken"]:
            assert base != _values(scenarios, number, name)
        assert _values(scenarios, number, "broken")["model_valid"] == 0


@pytest.mark.parametrize("number", range(77, 85))
def test_source_specific_physical_invariants(number, scenarios):
    a = _values(scenarios, number)
    b = _values(scenarios, number, "broken")
    d = scenarios[number]["baseline"]["diagnostics"]
    module = _load(_folder(number) / "experiment.py")
    if number == 77:
        assert a["phase_coherence"] > 0.99 and b["phase_coherence"] < 0.2
        assert a["max_x_error"] == a["max_y_error"] == 0
        assert b["active_true_voltage"] < 0.2 * a["active_true_voltage"]
        # Complex interpolation preserves quadrature and zeros unsupported endpoints.
        row = np.array([1 + 2j, 3 + 4j, 5 + 6j])
        np.testing.assert_allclose(
            module._linear_row(row, np.arange(3), np.array([-0.1, 0.5, 2, 2.1])), [0, 2 + 3j, 0, 0]
        )
    elif number == 78:
        assert a["geometric_migration"] > 33 and a["active_ridge_span"] <= 0.5
        assert b["active_ridge_span"] > 1.9 * a["measured_migration"]
        assert a["profile_peak_gain"] > 3 and b["profile_peak_gain"] < 1
        assert a["fixed_true_pixel_ratio"] < 0.25
    elif number == 79:
        assert a["hamming_half_power_width"] > a["cross_range_half_power_width"]
        assert a["hamming_peak_sidelobe"] < a["cross_range_peak_sidelobe"] - 20
        assert a["far_cross_range_peak"] < 0.1 and b["far_cross_range_peak"] > 0.99
        assert np.all(np.diff(d["bandwidth_widths"]) < 0)
        assert np.all(np.diff(d["aperture_widths"]) < 0)
    elif number == 80:
        assert a["phase_error_rms"] == pytest.approx(np.pi / 2)
        assert a["active_peak_retention"] > 0.99 and a["blurred_peak_retention"] < 0.6
        assert a["centered_phase_rmse"] < 0.02 and b["centered_phase_rmse"] > 0.4
        assert b["active_entropy"] > a["active_entropy"] + 0.4
    elif number == 81:
        assert a["truth_neighborhood_capture"] > 0.95 and b["truth_neighborhood_capture"] < 0.15
        assert max(d["rate_image_max_magnitude_differences"]) < 1e-10
        assert np.all(np.diff(d["cross_range_axis_m"]) > 0)
        assert a["coherent_processing_interval"] == 1
        # A known projected scatterer must land at positive cross-range with this sign.
        theta = np.linspace(-0.05, 0.05, 65)
        freq = 1e10 + np.linspace(-3e8, 3e8, 129)
        history = np.exp(-4j * np.pi * np.sin(theta[:, None]) * freq[None, :] / 3e8)
        ranges, x, _, image = module._isar_focus81(history, theta)
        i, j = np.unravel_index(np.argmax(abs(image)), image.shape)
        assert abs(x[j] - 1) < 0.15 and ranges[i] == 0
    elif number == 82:
        assert a["peak_delay"] == 24 and a["peak_doppler"] == 500
        assert a["peak_excess_path"] == 36
        assert b["peak_delay"] == b["peak_doppler"] == 0
        assert a["origin_coherence"] < 1e-12 and b["origin_coherence"] > 0.99
        assert a["target_contrast"] > b["target_contrast"] + 20
        ref, surv = module._channels82(24, 500, 35)
        residual, _ = module._cancel82(ref, surv)
        assert abs(np.vdot(ref, residual)) / np.vdot(ref, ref).real < 1e-12
    elif number == 83:
        assert a["active_scnr"] > a["fixed_scnr"] + 25
        assert b["active_scnr"] < a["active_scnr"] - 20
        assert b["interference_output_change"] > 20 and b["target_output_change"] > -1
        assert a["distortionless_error"] < 1e-12 and b["distortionless_error"] < 1e-12
        assert a["peak_range_cell"] == 25 and b["contaminated_cells"] == 9
        assert len(d["training_indices"]) == len(set(d["training_indices"])) == 36
        assert set(d["training_indices"]).isdisjoint(range(23, 28))
        assert d["support_ranks"][:3] == [8, 16, 24]
    elif number == 84:
        assert a["compression_peak_ratio"] == 1 and b["compression_peak_ratio"] < 0.1
        assert a["receiver_reconstruction_error"] < 1e-14
        assert a["scan_four_coast_count"] == 1 and a["baseline_track_rmse"] < 10
        assert d["track_updated"] == [True, True, True, False, True, True, True, True]
        assert d["cfar_training_cells"] == 102 and d["testable_cells"] == 116 * 24
        assert d["fixed_edge_detections"] > 3 * d["adaptive_edge_detections"]
        assert np.all(np.diff(d["pfa_detection_cells"]) >= 0)
        assert d["tracking_configuration"] == {"pfa": 0.001, "taper": 0, "correct_replica": True}
        # Flat power fixes the independent CFAR scale and complete-stencil border.
        threshold, eligible, detected = module._cfar84(np.ones((128, 32)), 0.001)
        np.testing.assert_allclose(threshold[eligible], 102 * (0.001 ** (-1 / 102) - 1))
        assert not np.any(detected) and not np.any(eligible[:6])


def test_active_contract_ledger_and_prior_source_prefix():
    raw = (COURSE / "remediation_reference_cases.py").read_bytes()
    assert (
        hashlib.sha256(raw[:185460]).hexdigest()
        == "41ad296232898f8d5b353261df02064ed52ad6d9c1d757e93703868455c6b9fd"
    )
    assert raw[185460:].lstrip().startswith(b"# P77-P84: alternate numerical formulations")
    contract = yaml.safe_load((ROOT / "contracts/active-batch.yaml").read_text())
    assert contract["batch"]["id"] == "ELP-GNC-SEMANTIC-QUALITY-12"
    assert contract["sources"]["baseline_commit"] == "00983cab0599b1ce3a613a2cc8ef42eb7b45f0b4"
    ledger = yaml.safe_load((COURSE / "remediation-map.yaml").read_text())
    assert ledger["derived_counts"]["repaired_in_prior_batches"] == 75
    assert ledger["derived_counts"]["repaired_in_batch"] == 8
    assert ledger["derived_counts"]["pending"] == 0
    assert ledger["claim_boundary"]["numerically_verified"] == "passed"


@pytest.mark.parametrize("number", range(77, 85))
def test_controls_and_all_retained_combinations(number, runtime):
    manifest = yaml.safe_load((_folder(number) / "module.yaml").read_text())
    a, b, _ = manifest["controls"]
    for bad in [float("nan"), -99999, True]:
        with pytest.raises(RuntimeContractError):
            runtime.run("dsp-radar", _folder(number).name, {a["id"]: bad})
    module = _load(_folder(number) / "experiment.py")
    with pytest.raises(TypeError):
        module.run({"broken_mode": "false"})
    for first in a["options"]:
        for second in b["options"]:
            for broken in [False, True]:
                result = module.run(
                    {a["id"]: first["value"], b["id"]: second["value"], "broken_mode": broken}
                )
                assert len(json.dumps(result, allow_nan=False).encode()) < 1_000_000


def test_aggregate_maturity_requires_separate_review_beyond_item_inventory():
    ledger = yaml.safe_load((COURSE / "remediation-map.yaml").read_text())
    assert ledger["scope"]["pending"]["items"] == []
    status = yaml.safe_load((ROOT / "docs/course-caliber-status.yaml").read_text())
    dsp = next(r for r in status["course_reviews"] if r["course_id"] == "dsp-radar")
    assert dsp["follow_up_issues"] == [441]
    for stage in ["numerically_verified", "curriculum_covered", "capstone_integrated"]:
        assert dsp["maturity"][stage]["status"] == "passed"
    assert "aggregate" in dsp["maturity"]["numerically_verified"]["limitation"].lower()


def test_aggregate_review_retains_all_independent_cases_and_no_learner_claim():
    report = json.loads((ROOT / "docs/course-quality/dsp-aggregate-review.json").read_text())
    assert len(report["comparisons"]) == 417
    assert all(c["status"] == "passed" for c in report["comparisons"])
    assert len(report["checkpoint_bindings"]) == 84
    assert len(report["cumulative_probes"]) == 10
    assert report["learner_validation"] == "not_run"
