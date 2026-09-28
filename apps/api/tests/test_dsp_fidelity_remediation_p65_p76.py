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
        for n in range(65, 77)
    }


@pytest.mark.parametrize("number", range(65, 77))
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


@pytest.mark.parametrize("number", range(65, 77))
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
    for number in range(65, 77):
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
    for number in range(65, 77):
        assert scenarios[number]["baseline"] == scenarios[number]["recovery"]
        base = _values(scenarios, number)
        assert base["model_valid"] == 1
        for name in ["sweep_1", "sweep_2", "broken"]:
            assert base != _values(scenarios, number, name)
        assert _values(scenarios, number, "broken")["model_valid"] == 0


@pytest.mark.parametrize("number", range(65, 77))
def test_source_specific_physical_invariants(number, scenarios):
    a = _values(scenarios, number)
    b = _values(scenarios, number, "broken")
    d = scenarios[number]["baseline"]["diagnostics"]
    module = _load(_folder(number) / "experiment.py")
    if number == 65:
        assert a["output_sinr"] > a["fixed_sinr"] + 10
        assert b["output_sinr"] < a["output_sinr"] - 8
        assert a["raw_solve_refused"] == 1 and a["distortionless_error"] < 1e-12
        assert a["corrected_recovery_sinr"] > b["output_sinr"] + 8
        with pytest.raises(ValueError, match="refused"):
            module._mvdr(np.ones((8, 8), complex), np.ones(8), 0)
        assert abs(a["true_response"] - 1) < 1e-12
    elif number == 66:
        assert a["angle_rmse"] < 0.25 and b["angle_rmse"] > 5
        assert a["music_contrast"] > 10 and a["bartlett_contrast"] < 0
        assert a["coherent_gap"] < 1 and a["smoothed_gap"] > 3
        assert a["smoothed_rmse"] < 0.25
        assert len(module._peaks(np.zeros(11), np.arange(11))) == 0
        assert module._angle_error(np.array([]), np.array([-3, 3])) == 80
    elif number == 67:
        assert a["manifold_error_recovered"] < a["manifold_error_before"] / 100
        assert b["manifold_error_active"] > 1 and b["active_sinr"] < a["active_sinr"] - 20
        assert a["music_rmse"] < 0.5 and a["other_direction_residual"] > 0.05
        assert np.all(np.diff(d["positions"]) > 0)
        c = np.array(d["coupling_real"]) + 1j * np.array(d["coupling_imag"])
        np.testing.assert_array_equal(c, c.T)
        assert not np.allclose(c, c.conj().T)  # reciprocal complex coupling, not Hermitian
    elif number == 68:
        assert a["active_scnr"] > a["separate_scnr"] + 10
        assert b["active_scnr"] < a["clean_scnr"] - 10 and b["target_response"] < -3
        assert a["distortionless_error"] < 1e-12
        assert b["selected_contaminated_cells"] == 51
        np.testing.assert_allclose(module._st(0, 0), np.ones(64))
        v = module._st(10, 0.2).reshape(8, 8)
        np.testing.assert_allclose(v[1] / v[0], np.exp(2j * np.pi * 0.2))
        assert d["training_rank"] == 64
    elif number == 69:
        assert abs(a["active_range"] - 45) < 0.02 and b["active_range"] == 2 * a["active_range"]
        assert abs(a["fft_beat"] - 150) < 0.02 and abs(a["phase_beat"] - 150) < 0.02
        assert a["valid_samples"] == 3176 and a["nominal_resolution"] == 7.5
        assert np.all(np.diff(d["range_sweep_beats_khz"]) > 0)
    elif number == 70:
        assert (
            a["range_bin_spacing"] == 1
            and abs(a["velocity_bin_spacing"] - 0.6087662337662338) < 1e-12
        )
        assert a["active_isolated_velocity"] > 0 and b["active_isolated_velocity"] == 0
        assert a["first_target_velocity"] < 0 and a["third_target_range"] == 23
        assert d["raw_shape"] == [512, 64] and d["range_shape"] == [257, 64]
        # Fast and slow axes must distinguish signed frequencies without truth.
        t = np.arange(128)
        m = np.arange(16)
        x = np.exp(2j * np.pi * (5 * t[:, None] / 128 - 2 * m / 16))
        _, rd, ra, va = module._process(x)
        i, j = np.unravel_index(np.argmax(abs(rd)), rd.shape)
        assert ra[i] == 20 and va[j] > 0
    elif number == 71:
        assert abs(a["stationary_bias"] + 3.08) < 0.01
        assert abs(a["active_error"]) < 0.01 and abs(b["active_error"] + 6.16) < 0.01
        assert abs(_values(scenarios, 71, "sweep_1")["stationary_bias"] - 4.62) < 0.01
        assert d["velocity_is_independent_input"] is True
    elif number == 72:
        assert abs(a["selected_range_error"]) < 0.08 and abs(a["selected_velocity_error"]) < 0.08
        assert all(min(abs(r - 30), abs(r - 65)) > 5 for r in d["ghost_ranges"])
        np.testing.assert_allclose(d["recovered_ranges"], [30, 65], atol=0.8)
        np.testing.assert_allclose(d["recovered_velocities"], [15, -10], atol=1.5)
        assert b["active_velocity"] > 100
        assert module._solve(100000, -100000) == (30, 0)
    elif number == 73:
        assert a["virtual_hpbw"] < 0.5 * a["physical_hpbw"]
        assert abs(b["angle_error"]) > 4 and abs(a["named_recovered_angle"] - 18) < 0.2
        assert abs(a["named_estimated_velocity"] - 10) < 0.05
        assert d["virtual_resolved"] == [False, True, True]
        assert len(set(d["virtual_positions"])) == 8 and d["tx_slots"] == [0] * 4 + [1] * 4
        np.testing.assert_allclose(d["motion_angles_after"], 18, atol=0.2)
    elif number == 74:
        assert a["bulk_doppler"] == pytest.approx(192)
        assert abs(a["active_dominant_doppler"] - 192) < 2.4 and b["active_dominant_doppler"] == 0
        assert a["frame_count"] == 147 and a["limb_low"] == -128 and a["limb_high"] == 512
        assert d["window_frame_counts"] == [397, 147, 47]
        assert np.all(np.diff(d["carrier_bulk_doppler"]) > 0)
        z, t, f = module._stft(np.exp(-2j * np.pi * 300 * np.arange(19200) / 4800), 512)
        assert abs(module._dominant(z, f) - 300) < 2.4
        assert t[0] == pytest.approx(255.5 / 4800)
    elif number == 75:
        assert a["range_excursion"] == pytest.approx(0.7996802557443061)
        assert a["phase_span"] == pytest.approx(26.65600852481)
        assert a["active_focus_peak"] > 0.99 and b["active_focus_peak"] < 0.15
        assert a["maximum_phase_step"] < 0.9 * np.pi
        assert np.all(np.diff(d["aperture_phase_spans"]) > 0)
        assert _values(scenarios, 75, "sweep_1")["recovered_coordinate"] == 20
        assert _values(scenarios, 75, "sweep_2")["aperture_samples"] == 101
    elif number == 76:
        assert a["active_phase_coherence"] > 0.98 and b["active_phase_coherence"] < 0.2
        assert a["maximum_range_quantization"] <= 0.625 + 1e-9
        assert d["raw_shape"] == [401, 361] and d["compressed_shape"] == [401, 600]
        assert d["pair_resolved"] == [False, False, True]
        assert np.all(np.diff(d["bandwidth_hpbw"]) < 0)
        # A zero-extended end pulse cannot circularly wrap into early outputs.
        x = np.zeros(361, complex)
        x[-1] = 1
        c = module._chirp(20)
        y = module._compress(x, c)
        np.testing.assert_allclose(y[:360], 0, atol=1e-14)
        np.testing.assert_allclose(y[360:], c[::-1].conj() / 240, atol=1e-14)


def test_active_contract_ledger_and_prior_source_prefix():
    raw = (COURSE / "remediation_reference_cases.py").read_bytes()
    assert (
        hashlib.sha256(raw[:154384]).hexdigest()
        == "3e335831c25b63a7ef02dd6a6ced2e39b42deb2a57f2597252c02ffcd0ee5bb8"
    )
    assert raw[154384:].lstrip().startswith(b"# P65-P76 independent references.")
    contract = yaml.safe_load((ROOT / "contracts/active-batch.yaml").read_text())
    assert contract["batch"]["id"] == "ELP-DSP-FIDELITY-P65-P76"
    assert contract["sources"]["baseline_commit"] == "e28b041aff3f4e66cec2190e04a5d689be23f260"
    ledger = yaml.safe_load((COURSE / "remediation-map.yaml").read_text())
    assert ledger["derived_counts"]["repaired_in_prior_batches"] == 63
    assert ledger["derived_counts"]["repaired_in_batch"] == 12
    assert ledger["derived_counts"]["pending"] == 8
    assert ledger["claim_boundary"]["numerically_verified"] == "blocked"


@pytest.mark.parametrize("number", range(65, 77))
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
