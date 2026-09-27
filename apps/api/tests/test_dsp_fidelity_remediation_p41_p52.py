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
        for n in range(41, 53)
    }


@pytest.mark.parametrize("number", range(41, 53))
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


@pytest.mark.parametrize("number", range(41, 53))
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
    for number in range(41, 53):
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


def test_failures_recoveries_and_physical_limits(scenarios):
    def values(n, name="baseline"):
        return {m["id"]: m["value"] for m in scenarios[n][name]["metrics"]}

    for n in range(41, 53):
        assert scenarios[n]["baseline"] == scenarios[n]["recovery"]
        base = values(n)
        for name in ["sweep_1", "sweep_2", "broken"]:
            assert base != values(n, name)
        assert base["model_valid"] == 1 and values(n, "broken")["model_valid"] == 0
    a = values(41)
    assert a["swerling_i_cv_16"] > 3 * a["swerling_ii_cv_16"]
    assert a["swerling_iii_cv_16"] > 3 * a["swerling_iv_cv_16"]
    assert abs(a["range_lag1"] - 0.85) < 0.06 and abs(a["slow_time_lag1"] - 0.92) < 0.06
    assert values(41, "sweep_2")["steady_pd_16"] > a["steady_pd_16"]
    assert abs(a["active_near_pfa"] - 0.05) < 0.02 and abs(a["active_far_pfa"] - 0.05) < 0.02
    assert values(41, "broken")["active_near_pfa"] > 3 * values(41, "broken")["active_far_pfa"]
    a = values(42)
    assert a["first_range"] == pytest.approx(1200, abs=a["range_spacing"] / 2)
    assert a["third_range"] == pytest.approx(2400, abs=a["range_spacing"] / 2)
    assert a["first_velocity"] < 0 < a["second_velocity"]
    assert a["hann_sidelobe"] < a["rectangular_sidelobe"] - 10
    assert values(42, "sweep_1")["velocity_spacing"] == pytest.approx(2 * a["velocity_spacing"])
    a = values(43)
    assert a["empirical_pd"] == pytest.approx(a["analytic_pd"], abs=0.01)
    assert values(43, "sweep_1")["empirical_pfa"] > 8 * a["empirical_pfa"]
    assert values(43, "broken")["active_pfa_at_double_noise"] < a["active_pfa_at_double_noise"] / 8
    a = values(44)
    assert a["template_energy"] == 16 and a["tuning_bank_pfa"] == 0 and a["held_out_pfa"] == 1
    assert values(44, "broken")["empirical_pfa"] > 0.99
    d = scenarios[44]["baseline"]["diagnostics"]
    assert np.all(np.diff(d["pfa"]) <= 0) and np.all(np.diff(d["pd"], axis=1) <= 0)
    assert a["false_alarms_per_million"] == 1e6 * a["empirical_pfa"]
    a = values(45)
    assert a["eligible_cells"] + a["excluded_edges"] == 256
    assert a["target_detections"] == 3 and a["geometric_threshold_ratio"] < 1
    assert scenarios[45]["baseline"]["diagnostics"]["scale_invariant"]
    assert values(45, "sweep_2")["active_threshold_at_middle_target"] == pytest.approx(
        2 * a["active_threshold_at_middle_target"]
    )
    a = values(46)
    assert (
        a["contaminated_weak_margin"] < 1 < a["recovered_weak_margin"]
        and a["weak_power_change"] == 0
    )
    assert a["small_guard_leakage"] > a["large_guard_leakage"]
    assert a["small_window_locality_error"] < a["large_window_locality_error"]
    d = scenarios[46]["baseline"]["diagnostics"]
    assert d["guard_margins"][0] < 1 < d["guard_margins"][1]
    assert d["training_roughness"][0] > d["training_roughness"][-1]
    a = values(47)
    assert 0 < a["active_cfar_loss"] < 2
    assert values(47, "sweep_1")["active_cfar_loss"] < a["active_cfar_loss"]
    assert values(47, "broken")["active_theoretical_pfa"] > a["active_theoretical_pfa"]
    assert a["maximum_monotone_adjustment"] <= 0.01
    a = values(48)
    assert a["go_alpha"] < a["so_alpha"]
    assert a["contaminated_so_pd"] > a["contaminated_go_pd"] + 0.5
    assert values(48, "broken")["active_edge_pfa"] > 10 * a["active_edge_pfa"]
    assert a["shared_ca_go_pfa"] < 0.001 < a["shared_ca_so_pfa"]
    a = values(49)
    assert a["outlier_capacity"] == 6 and a["primary_ca_margin"] < 1 < a["primary_os_margin"]
    d = scenarios[49]["baseline"]["diagnostics"]
    assert d["count_pd"][3][1] > 0.2 and d["count_pd"][4][1] < 0.01
    assert abs(values(49, "broken")["active_homogeneous_pfa"] - 0.001) > 0.0005
    a = values(50)
    assert a["training_cells"] == 17 * 13 - 25
    assert a["eligible_cells"] == 80 * 52 and a["interior_targets_detected"] == 3
    assert a["active_border_crossings"] == a["recovered_edge_testable"] == 0
    assert values(50, "broken")["active_edge_target_detected"] == 1
    assert values(50, "sweep_1")["eligible_fraction"] < a["eligible_fraction"]
    a = values(51)
    assert a["active_ca_pfa"] == pytest.approx(0.001, abs=1e-12)
    assert a["active_go_pfa"] == pytest.approx(0.001, abs=1e-12)
    assert a["active_so_pfa"] == pytest.approx(0.001, abs=1e-12)
    assert a["active_os_pfa"] == pytest.approx(0.001, abs=1e-12)
    assert a["disagreement_cells"] > 0 and a["ca_response_artifacts"] > 0
    d = scenarios[51]["baseline"]["diagnostics"]
    assert all(row["cause"] and len(row["thresholds"]) == 4 for row in d["disagreements"])
    assert sum(d["h0_category_counts"][0]) == a["ca_h0_crossings"]
    assert sum(d["artifact_owner_counts"][0]) == a["ca_response_artifacts"]
    a = values(52)
    assert a["wilson_lower"] < a["active_measured_pfa"] < a["wilson_upper"]
    assert abs(a["active_measured_pfa"] - 0.001) < 5 * np.sqrt(0.001 * 0.999 / 200000) + 2 / 200000
    assert a["correlated_pfa"] < 0.0006 and a["textured_pfa"] > 0.008
    assert values(52, "broken")["active_measured_pfa"] > 1.5 * a["active_measured_pfa"]
    d = scenarios[52]["baseline"]["diagnostics"]
    assert d["running_counts"][-1] == a["active_alarm_count"]
    assert d["running_wilson_width"][-1] < d["running_wilson_width"][0]


def test_stencils_exclude_cut_guards_and_incomplete_edges():
    module = _load(_folder(45) / "experiment.py")
    cuts, refs = module._refs(256, 12, 2)
    assert refs.shape == (228, 24)
    assert np.all(abs(refs - cuts[:, None]) > 2)
    assert refs.min() == 0 and refs.max() == 255
    constant = np.ones(256) * 7
    _, threshold, det, estimate = module._ca(constant, 12, 2, 0.001)
    np.testing.assert_allclose(estimate, 7)
    assert not np.any(det)
    np.testing.assert_allclose(threshold, 7 * 24 * (0.001 ** (-1 / 24) - 1))
    two = _load(_folder(50) / "experiment.py")
    threshold, eligible, n, estimate, mask = two._ring(np.ones((96, 64)), 6, 4)
    assert n == 196 and np.count_nonzero(mask) == 196
    np.testing.assert_allclose(estimate[eligible], 1)
    assert estimate[0, 0] < 1 and not eligible[0, 0]


def test_independent_calibration_and_zero_count_interval():
    go = _load(_folder(48) / "experiment.py")
    os = _load(_folder(49) / "experiment.py")
    for t in [4, 12, 20]:
        for variant in ["GO", "SO"]:
            for p in [0.01, 0.001, 0.0001]:
                alpha = go._calibrate(
                    lambda a, t=t, variant=variant: go._variant_pfa(a, t, variant), p
                )
                assert go._variant_pfa(alpha, t, variant) == pytest.approx(p, abs=1e-12)
    for rank in [1, 12, 18, 24]:
        alpha = os._calibrate(lambda a, rank=rank: os._os_pfa(a, 24, rank), 0.001)
        assert os._os_pfa(alpha, 24, rank) == pytest.approx(0.001, abs=1e-12)
    mc = _load(_folder(52) / "experiment.py")
    lo, hi = mc._wilson(0, 500)
    assert lo == pytest.approx(0, abs=1e-15) and 0 < hi < 0.01


def test_heatmap_coordinates_retain_targets_and_zero(scenarios):
    heat = scenarios[42]["baseline"]["plots"]["map"]["data"][0]
    for row in scenarios[42]["baseline"]["diagnostics"]["measured_targets"]:
        assert row[0] in heat["y"] and row[1] in heat["x"]
    assert 0 in heat["x"] and 0 in heat["y"]
    heat = scenarios[50]["baseline"]["plots"]["power"]["data"][0]
    for r in [27 * 30, 52 * 30, 75 * 30, 3 * 30]:
        assert r in heat["y"]
    assert 0 in heat["x"]


def test_prior_reference_prefix_is_immutable():
    raw = (COURSE / "remediation_reference_cases.py").read_bytes()
    assert (
        hashlib.sha256(raw[:90006]).hexdigest()
        == "639080c7d5ee1da82ee8753edf755d41b68631ba751622b55c074a33d84fc09d"
    )
    assert raw[90006:].startswith(b"# P41-P52 independent references.")


@pytest.mark.parametrize("number", range(41, 53))
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
