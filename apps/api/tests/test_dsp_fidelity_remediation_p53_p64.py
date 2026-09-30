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
        for n in range(53, 65)
    }


@pytest.mark.parametrize("number", range(53, 65))
def test_source_bound_identity_content_and_stage_wiring(number, references):
    folder = _folder(number)
    manifest = yaml.safe_load((folder / "module.yaml").read_text())
    record = json.loads((folder / "conversion.yaml").read_text())
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


@pytest.mark.parametrize("number", range(53, 65))
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
    for number in range(53, 65):
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
    for number in range(53, 65):
        assert scenarios[number]["baseline"] == scenarios[number]["recovery"]
        base = _values(scenarios, number)
        assert base["model_valid"] == 1
        for name in ["sweep_1", "sweep_2", "broken"]:
            assert base != _values(scenarios, number, name)
        assert _values(scenarios, number, "broken")["model_valid"] == 0


def test_p53_topology_filtering_weighting_and_plateau_ties(scenarios):
    a = _values(scenarios, 53)
    broken = _values(scenarios, 53, "broken")
    assert a["active_reports"] == 2 and broken["active_reports"] == 7
    assert scenarios[53]["baseline"]["diagnostics"]["size_sweep_report_counts"] == [7, 2, 1]
    assert abs(a["target1_range"] - 365.25) < 15 and abs(a["target1_velocity"] - 4.2) < 0.5
    module = _load(_folder(53) / "experiment.py")
    score = np.array([[2.0, 2.0, 0.0], [0.0, 0.0, 2.0], [0.0, 0.0, 2.0]])
    assert len(module._components(score > 1)[1]) == 1  # diagonal connection joins all four cells
    np.testing.assert_array_equal(module._peaks(score), [[0, 0]])
    score[2, 2] = 3
    np.testing.assert_array_equal(module._peaks(score), [[2, 2]])  # no partial plateau maxima


def test_p54_coasting_and_velocity_learning(scenarios):
    a = _values(scenarios, 54)
    b = _values(scenarios, 54, "broken")
    assert b["final_velocity"] == 0 and b["position_rmse"] > 3 * a["position_rmse"]
    d = scenarios[54]["baseline"]["diagnostics"]
    state = np.array(d["state"])
    pred = np.array(d["prediction"])
    available = np.array(d["available"])
    assert np.count_nonzero(~available) == 6
    np.testing.assert_array_equal(state[~available], pred[~available])
    np.testing.assert_allclose(pred[1:, 0], state[:-1, 0] + state[:-1, 1])
    np.testing.assert_allclose(pred[1:, 1], state[:-1, 1])


def test_p55_covariance_gain_and_mismatch(scenarios):
    a = _values(scenarios, 55)
    b = _values(scenarios, 55, "broken")
    d = scenarios[55]["baseline"]["diagnostics"]
    assert a["position_rmse"] < 25 and b["position_rmse"] > a["position_rmse"]
    assert a["low_r_position_rmse"] > a["position_rmse"]
    covariance = np.array(d["covariance"])
    np.testing.assert_allclose(covariance, covariance.transpose(0, 2, 1), atol=1e-12)
    assert np.linalg.eigvalsh(covariance).min() > 0
    assert np.all(np.diff(d["r_sweep_gain"]) < 0)
    assert 0.4 < a["mean_nis"] < 1.6  # single fixed record; not an ensemble consistency claim


def test_p56_wrap_jacobian_and_geometry(scenarios):
    a = _values(scenarios, 56)
    b = _values(scenarios, 56, "broken")
    s = _values(scenarios, 56, "sweep_2")
    assert a["maximum_bearing_innovation"] < 10 and b["maximum_bearing_innovation"] > 300
    assert b["position_rmse"] > 10 * a["position_rmse"]
    assert s["geometry_tangential_sigma"] == 2 * a["geometry_tangential_sigma"]
    d = scenarios[56]["baseline"]["diagnostics"]
    states = np.array(d["state"])
    jacobians = np.array(d["jacobian"])
    for k in [1, 25, 50, 75, 100]:
        prior = states[k - 1]
        prediction = prior + np.array([prior[1], 0, prior[3], 0])
        numeric = np.zeros((2, 4))

        def measurement(x):
            return np.array([np.hypot(x[0], x[2]), np.arctan2(x[2], x[0])])

        for j in range(4):
            offset = np.eye(4)[j] * 1e-3
            numeric[:, j] = (
                measurement(prediction + offset) - measurement(prediction - offset)
            ) / (2e-3)
        np.testing.assert_allclose(jacobians[k], numeric, atol=2e-7, rtol=2e-7)
    assert np.linalg.eigvalsh(d["covariance"]).min() > 0


def test_p57_uncertainty_gating_and_one_to_one(scenarios):
    a = _values(scenarios, 57)
    b = _values(scenarios, 57, "broken")
    d = scenarios[57]["baseline"]["diagnostics"]
    assert d["assignment"] == [3, 1, 5] and a["correct_links"] == 3
    assert b["track1_report"] == 2 and b["correct_links"] == 2
    assert a["track1_target_d2"] < 5.991 < a["track1_clutter_d2"]
    assert _values(scenarios, 57, "sweep_1")["assigned_tracks"] < 3
    assert _values(scenarios, 57, "sweep_2")["track1_gate_area"] > a["track1_gate_area"]
    module = _load(_folder(57) / "experiment.py")
    result = module._greedy(np.ones((3, 2)), np.ones((3, 2), bool))
    assert result.tolist() == [0, 1, -1]  # source column-major tie order and no reuse
    assert module._greedy(np.ones((3, 2)), np.zeros((3, 2), bool)).tolist() == [-1, -1, -1]


def test_p58_lifecycle_thresholds_and_stable_ids(scenarios):
    a = _values(scenarios, 58)
    b = _values(scenarios, 58, "broken")
    assert a["target_confirmation_scan"] == 7 and a["target_last_deletion_scan"] == 27
    assert (
        a["short_gap_same_id_survived"] == 1
        and a["false_confirmed"] == 0
        and a["final_active_tracks"] == 0
    )
    assert b["false_confirmed"] == 8 and b["final_active_tracks"] == 9
    assert _values(scenarios, 58, "sweep_2")["short_gap_same_id_survived"] == 0
    events = scenarios[58]["baseline"]["diagnostics"]["events"]
    assert any("failed confirmation" in event[2] for event in events)
    assert any("coast budget" in event[2] for event in events)
    births = [event[1] for event in events if event[2].startswith("born")]
    assert births == list(range(1, 10))


def test_p59_crossing_truth_is_audit_only_and_report_reuse_fails(scenarios):
    a = _values(scenarios, 59)
    b = _values(scenarios, 59, "broken")
    assert a["active_wrong_links"] == 0 and a["position_only_wrong_links"] == 24
    assert b["duplicate_report_scans"] == 12 and a["duplicate_report_scans"] == 0
    assert b["position_rmse"] > a["position_rmse"]
    assert a["noise_sweep_high_velocity_failure"] < a["noise_sweep_high_position_failure"]
    assert a["wide_separation_position_failure"] < 0.2
    module = _load(_folder(59) / "experiment.py")
    truth, p, v = module._scene(module._normal_bank([5908]), 6, 1)
    first = module._track(truth, p, v, 6, 1, 1)
    changed_truth = truth.copy()
    changed_truth[1:] += 1e6
    second = module._track(changed_truth, p, v, 6, 1, 1)
    np.testing.assert_array_equal(first["assignment"], second["assignment"])
    np.testing.assert_array_equal(
        first["state"], second["state"]
    )  # only disclosed initial state uses truth


def test_p60_mixing_support_covariance_and_likelihood(scenarios):
    a = _values(scenarios, 60)
    b = _values(scenarios, 60, "broken")
    d = scenarios[60]["baseline"]["diagnostics"]
    assert a["position_rmse"] < 0.5 * a["fixed_cv_rmse"]
    assert b["maximum_maneuver_probability"] == 0 and b["position_rmse"] == pytest.approx(
        b["fixed_cv_rmse"]
    )
    assert a["maximum_maneuver_probability"] > 0.9
    np.testing.assert_allclose(np.sum(d["mode_probability"], axis=1), 1, atol=1e-14)
    np.testing.assert_allclose(np.sum(d["mixing_probability"], axis=1), 1, atol=1e-14)
    assert np.linalg.eigvalsh(d["covariance"]).min() > 0
    assert np.isfinite(d["log_likelihood"]).all()


def test_p61_phase_sign_and_unresolvable_alias(scenarios):
    a = _values(scenarios, 61)
    b = _values(scenarios, 61, "broken")
    assert a["theoretical_phase_slope"] == pytest.approx(np.pi / 2)
    assert a["last_sensor_delay"] < 0 and abs(a["angle_error"]) < 1
    assert b["alias_snapshot_mismatch"] < 1e-12 and abs(b["angle_error"]) > 50
    assert b["recovered_alias_angle"] == pytest.approx(np.rad2deg(np.arcsin(0.6)))
    assert _values(scenarios, 61, "sweep_1")["theoretical_phase_slope"] < 0
    assert _values(scenarios, 61, "sweep_2")["theoretical_phase_slope"] == pytest.approx(np.pi / 4)


def test_p62_full_grid_beamwidth_taper_and_visible_grating_lobe(scenarios):
    a = _values(scenarios, 62)
    b = _values(scenarios, 62, "broken")
    assert 12.7 < a["half_power_beamwidth"] < 12.9
    assert a["taper8_half_power_beamwidth"] > a["half_power_beamwidth"] + 5
    assert a["taper8_sidelobe_level"] < a["peak_sidelobe_level"] - 15
    assert b["visible_grating_lobes"] == 1 and b["alias_response_at_minus30"] == pytest.approx(1)
    assert b["recovered_alias_response"] < 1e-12
    d = scenarios[62]["baseline"]["diagnostics"]
    assert d["calculation_angle_samples"] == 7201 and np.all(np.diff(d["element_sweep_hpbw"]) < 0)
    trace = scenarios[62]["broken"]["plots"]["pattern"]["data"][0]
    assert -30 in trace["x"] and 30 in trace["x"] and 0 in trace["x"]


def test_p63_conjugate_steering_resolution_and_noise_averaging(scenarios):
    a = _values(scenarios, 63)
    b = _values(scenarios, 63, "broken")
    d = scenarios[63]["baseline"]["diagnostics"]
    assert abs(a["first_peak_angle"] + 20) < 0.5 and abs(a["second_peak_angle"] - 25) < 0.5
    assert abs(b["first_peak_angle"] + 30) < 0.5 and abs(b["second_peak_angle"] - 20) < 0.5
    assert a["wrong_sign_mirror_error"] < 1e-12
    assert d["separation_resolved"][0] is False and d["separation_resolved"][-1] is True
    assert d["aperture_resolved"] == [False, True, True]
    assert np.all(np.diff(d["snr_sweep_floor"]) < 0)
    assert d["snapshot_sweep_ripple"][-1] < d["snapshot_sweep_ripple"][0]
    module = _load(_folder(63) / "experiment.py")
    ones = np.ones((8, 4), complex)
    assert module._scan(ones, np.array([0.0]))[0] == pytest.approx(1.0)  # coherent normalization


def test_p64_local_calibration_guard_clipping_and_gain_recovery(scenarios):
    a = _values(scenarios, 64)
    b = _values(scenarios, 64, "broken")
    low = _values(scenarios, 64, "sweep_2")
    d = scenarios[64]["baseline"]["diagnostics"]
    assert abs(a["active_angle_error"]) < 0.15 and a["valid_snapshots"] == 256
    assert abs(b["active_angle_error"]) > 0.3 and abs(a["calibrated_boresight_error"]) < 1e-12
    assert low["snapshot_rmse"] > a["snapshot_rmse"] and low["clipped_valid_snapshots"] > 0
    assert np.all(np.diff(d["squint_slopes"]) > 0) and np.all(
        np.diff(d["squint_boresight_sum"]) < 0
    )
    assert np.all(np.diff(d["snr_sweep_rmse"]) < 0)
    assert d["calibration_limit_deg"] == 4 and d["sum_guard"] == 0.15


def test_active_contract_ledger_and_prior_source_prefix():
    raw = (COURSE / "remediation_reference_cases.py").read_bytes()
    assert (
        hashlib.sha256(raw[:118814]).hexdigest()
        == "eee1c963fa051806d29581553be723bc8580ccbccdd1b7f00ea8492a776fac5c"
    )
    assert raw[118814:].lstrip().startswith(b"# P53-P64 independent references.")
    contract = yaml.safe_load((ROOT / "contracts/active-batch.yaml").read_text())
    assert contract["batch"]["id"] == "ELP-ROBOTICS-DYNAMICS-QUALITY-12"
    assert "ELP-NAV-GEOMETRY-QUALITY-12" in contract["dependencies"]
    ledger = yaml.safe_load((COURSE / "remediation-map.yaml").read_text())
    prior = ledger["scope"]["repaired_in_prior_batches"]
    assert "ELP-DSP-FIDELITY-P53-P64" in prior["batch_ids"]
    assert prior["items"][51:63] == [f"P{n}" for n in range(53, 65)]
    assert ledger["claim_boundary"]["numerically_verified"] == "passed"


@pytest.mark.parametrize("number", range(53, 65))
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
