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
        for n in range(29, 41)
    }


@pytest.mark.parametrize("number", range(29, 41))
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


@pytest.mark.parametrize("number", range(29, 41))
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
    for number in range(29, 41):
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

    for n in range(29, 41):
        assert scenarios[n]["baseline"] == scenarios[n]["recovery"]
        base = values(n)
        assert base != values(n, "broken")
        assert base != values(n, "sweep_1")
        assert base != values(n, "sweep_2")
        assert base["model_valid"] == 1 and values(n, "broken")["model_valid"] == 0
    assert values(29)["active_decade_slope"] == -40
    assert values(29, "broken")["active_decade_slope"] == -20
    assert values(29, "sweep_2")["threshold_range"] / values(29)[
        "threshold_range"
    ] == pytest.approx(4**0.25)
    assert values(30, "broken")["active_reported_range"] == 2 * values(30)["refined_range"]
    assert values(30)["close_pair_peaks"] == 1 and values(30)["wide_pair_peaks"] == 2
    assert abs(values(30)["refined_error"]) < abs(
        values(30)["integer_range"] - values(30)["true_range"]
    )
    assert values(31)["physical_peak_count"] == 1 and values(31)["wideband_peak_count"] == 2
    assert (
        values(31)["high_snr_rmse"]
        < 1
        < values(31)["measured_response_width"]
        < values(31)["low_snr_rmse"]
    )
    assert values(31, "broken")["active_claimed_count"] == 2
    assert values(31)["false_display_separation"] < 0.2
    assert values(32, "broken")["active_width"] > 5 * values(32)["correct_width"]
    assert values(32, "broken")["active_peak_loss"] < -6
    assert abs(values(32)["measured_bt_gain"] - values(32)["predicted_bt_gain"]) < 3
    assert values(32, "sweep_1")["correct_width"] < values(32)["correct_width"]
    assert values(33)["active_pslr"] < values(33)["rectangular_pslr"] - 10
    assert values(33)["active_width"] > values(33)["rectangular_width"]
    assert values(33)["active_snr_loss"] < -1
    assert (
        values(33)["active_visibility_margin"]
        > 0
        > values(33, "broken")["active_visibility_margin"]
    )
    assert values(33)["weak_local_peak"] == 1 and values(33, "broken")["weak_local_peak"] == 0
    assert values(34, "broken")["active_extreme_delay"] == 1
    assert values(34)["zero_filled_extreme"] == pytest.approx(1 / 130)
    assert abs(values(34)["positive_ridge_delay"] - values(34)["predicted_ridge_delay"]) <= 0.1
    assert values(34)["lfm_delay_width"] < values(34)["rectangular_delay_width"] / 10
    assert values(35)["ambiguity_order"] == 2
    assert 0 <= values(35)["apparent_range"] < values(35)["unambiguous_range"]
    assert values(35, "broken")["active_reported_range"] == 18
    assert abs(values(36)["active_phase_doppler"] - values(36)["true_doppler"]) < 10
    assert (
        values(36, "broken")["active_fft_doppler"]
        == values(36, "broken")["active_phase_doppler"]
        == 0
    )
    assert values(36, "sweep_1")["active_phase_doppler"] < 0
    assert values(37)["middle_range_bin"] == 120
    assert values(37)["range_axis_span"] < values(37)["prf_unambiguous_range"]
    assert values(37)["neglected_migration"] < 0.1
    assert (
        values(37, "broken")["active_middle_doppler"]
        == values(37, "broken")["active_fft_peak"]
        == 0
    )
    assert (
        values(38)["active_clutter_residual"] == 0 < values(38, "broken")["active_clutter_residual"]
    )
    assert values(38)["two_noise_power_gain"] == pytest.approx(2, rel=0.05)
    assert values(38)["three_noise_power_gain"] == pytest.approx(6, rel=0.05)
    assert values(38)["slow_target_three_gain"] == pytest.approx(
        values(38)["slow_target_two_gain"] ** 2
    )
    assert (
        values(38)["active_output_columns"] == 63
        and values(38, "broken")["active_output_rows"] == 127
    )
    assert values(39)["primary_normalized_gain"] < 1e-12
    assert values(39)["active_fused_gain"] > 0.3 > values(39, "broken")["active_fused_gain"]
    assert values(39)["stationary_fused_gain"] == 0
    assert values(40)["coherent_detectability"] / values(40)[
        "noncoherent_detectability"
    ] == pytest.approx(np.sqrt(32))
    assert values(40, "broken")["active_signal_power_fraction"] < 1e-20
    assert values(40, "broken")["recovered_signal_power_fraction"] == pytest.approx(1)
    assert values(40, "broken")["noncoherent_signal_energy_fraction"] == pytest.approx(1)


@pytest.mark.parametrize("number", range(29, 41))
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


def test_zero_extension_and_non_circular_ambiguity():
    ranging = _load(_folder(30) / "experiment.py")
    pulse = np.ones(20)
    echo = ranging._echo(pulse, 100, 70.25)
    assert np.count_nonzero(echo[:70]) == 0
    assert echo[70] == 0.75 and echo[90] == 0.25
    assert not np.any(ranging._echo(pulse, 100, 110))
    ambiguity = _load(_folder(34) / "experiment.py")
    result = ambiguity._ambiguity(np.ones(13), [0])
    np.testing.assert_allclose(result[0], np.r_[np.arange(1, 14), np.arange(12, 0, -1)] / 13)


def test_pulse_energy_gain_and_noise_normalizations(scenarios):
    gaussian = _load(_folder(31) / "experiment.py")
    for bandwidth in [2e6, 4e6, 8e6]:
        pulse = gaussian._gaussian_case(bandwidth, 22)[0]
        assert sum(pulse**2) == pytest.approx(1, abs=1e-12)
        np.testing.assert_allclose(pulse, pulse[::-1], atol=1e-12)
    chirp = _load(_folder(32) / "experiment.py")
    np.testing.assert_allclose(abs(chirp._lfm(8e6, 10e-6)), 1, atol=1e-12)
    jitter = scenarios[40]["baseline"]["plots"]["jitter"]["data"]
    assert jitter[0]["y"][0] == 1 and np.all(np.diff(jitter[0]["y"]) < 0)
    assert jitter[1]["y"] == [1] * len(jitter[1]["x"])


def test_prior_reference_prefix_is_immutable():
    expected = "fffe190b7c067e8ed3ae692a699f3b055f1055ada36674ecfbf9f56b9ae189a8"
    raw = (COURSE / "remediation_reference_cases.py").read_bytes()
    assert hashlib.sha256(raw[:67205]).hexdigest() == expected
    assert raw[67205:].startswith(b"\n# P29-P40 independent references.")


def test_heatmap_thinning_preserves_zero_and_target_peaks(scenarios):
    for name in ["rectangular_surface", "lfm_surface", "code_surface"]:
        trace = scenarios[34]["baseline"]["plots"][name]["data"][0]
        assert 0 in trace["x"] and 0 in trace["y"]
        assert trace["z"][trace["y"].index(0)][trace["x"].index(0)] == pytest.approx(0, abs=1e-12)
    ranges = scenarios[37]["baseline"]["plots"]["matrix"]["data"][0]["y"]
    for index in [60, 120, 160]:
        assert index * 299792458 / 40000000 == pytest.approx(
            min(ranges, key=lambda r: abs(r - index * 299792458 / 40000000)), abs=1e-10
        )
