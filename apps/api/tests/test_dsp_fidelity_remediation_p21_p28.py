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
        for n in range(21, 29)
    }


@pytest.mark.parametrize("number", range(21, 29))
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


@pytest.mark.parametrize("number", range(21, 29))
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
            assert 0 < len(trace["x"]) == len(trace["y"]) <= 512
    manifest = yaml.safe_load((_folder(number) / "module.yaml").read_text())
    wired = {block["plot"] for block in manifest["blocks"] if block["type"] == "plot"}
    assert wired == set(result["plots"])


def test_independent_reference_provenance_and_no_production_imports(references):
    text = (COURSE / "remediation_reference_cases.py").read_text()
    assert "experiment.py" not in text
    assert "importlib" not in text and "elp_api" not in text
    for number in range(21, 29):
        provenance = json.loads((_folder(number) / "evidence/provenance.json").read_text())
        assert provenance["reference"]["independent"] is True
        assert provenance["reference"]["imports_production"] is False
        # P29-P40 adds references without altering this historically attested prefix.
        prior_bytes = (COURSE / "remediation_reference_cases.py").read_bytes()[:67205]
        assert provenance["reference"]["sha256"] == hashlib.sha256(prior_bytes).hexdigest()
        assert provenance["production"]["sha256"] == _sha(_folder(number) / "experiment.py")
        assert provenance["scenarios"] == references.SCENARIOS[f"P{number}"]


def test_failure_recovery_and_source_limiting_cases(scenarios):
    def sig(n, name="baseline"):
        return scenarios[n][name]["diagnostics"]["signature"]

    for n in range(21, 29):
        assert scenarios[n]["baseline"] == scenarios[n]["recovery"]
        assert sig(n) != sig(n, "broken")
        assert sig(n) != sig(n, "sweep_1")
        assert sig(n) != sig(n, "sweep_2")
    assert sig(21)[3:5] == pytest.approx([0.3, 0.3], abs=0.001)
    assert sig(21, "broken")[5] < 0
    assert sig(21, "broken")[6] > 0.2 and sig(21, "broken")[7] < 0.01
    assert sig(22)[1:3] == [1000, 1000]
    assert sig(22, "broken")[4] > 0.15
    assert sig(22)[6] == 10200 and sig(22)[7] < 55 and sig(22)[8] >= 500
    assert sig(23)[2:4] == pytest.approx([1, 1])
    assert sig(23)[4] / sig(23)[5] == pytest.approx(np.sqrt(2))
    assert sig(23, "broken")[7] > 0.45 and sig(23, "broken")[8] == 0
    assert sig(24)[0] == pytest.approx(1) and sig(24)[1] == 64
    assert sig(24)[5] < 2 and sig(24)[4] < sig(24)[3]
    assert sig(24, "broken")[4] > 3 * sig(24)[4]
    assert sig(24, "broken")[6] > 0.3
    assert sig(25)[1] < sig(25)[0] and sig(25)[2] < sig(25)[0]
    assert sig(25, "broken")[9] == pytest.approx(-60)
    assert sig(25)[11] < sig(25)[10] and sig(25)[13] < sig(25)[12]
    assert sig(25)[14] > 0  # regularization reports, rather than hides, residual distortion
    assert min(sig(26)[0], sig(26)[2]) > 20
    assert sig(26)[1] == pytest.approx(1, abs=0.05)
    assert sig(26)[3] == pytest.approx(1, abs=0.05)
    assert sig(26)[5] < 0.08 and sig(26)[6] < 3001
    assert sig(26, "sweep_2")[2] < 1
    assert 1 <= sig(26, "broken")[7] < 6001 and sig(26, "broken")[8] == 0
    assert sig(27)[3] < sig(27)[5] < sig(27)[4]
    assert sig(27, "sweep_1")[4] - sig(27, "sweep_1")[3] > sig(27)[4] - sig(27)[3]
    assert sig(27, "broken")[2] == 0 and sig(27, "broken")[6:8] == [1, 0]
    assert sig(27, "broken")[4] < sig(27)[5]
    assert sig(28)[:2] == pytest.approx(sig(28)[2:4], abs=0.025)
    assert sig(28)[5] / sig(28)[6] == pytest.approx(1, abs=0.08)
    assert abs(sig(28)[4]) / np.sqrt(sig(28)[6]) < 0.05
    assert sig(28, "broken")[4] > sig(28)[4] + 0.1
    assert sig(28)[7] == pytest.approx(sig(28)[8], abs=0.04)
    assert sig(28, "broken")[10] < 12000 and sig(28, "broken")[11] == 0


def test_pulse_singularities_and_fm_sweep_limits():
    pulse_module = _load(_folder(24) / "experiment.py")
    for alpha in [0.1, 0.25, 0.5, 1.0]:
        for span in [2, 4, 6, 8]:
            pulse = pulse_module._rrc(alpha, span)
            assert np.all(np.isfinite(pulse))
            assert np.sum(pulse**2) == pytest.approx(1, abs=1e-12)
            assert pulse == pytest.approx(pulse[::-1], abs=1e-12)
    fm = _load(_folder(22) / "experiment.py")
    assert [fm._fm(d, 100)[7] for d in [50, 200, 400, 800]] == [200, 600, 1000, 1800]
    assert [fm._fm(400, f)[7] for f in [50, 100, 200, 400]] == [900, 1000, 1200, 1600]


@pytest.mark.parametrize("number", range(21, 29))
def test_controls_reject_out_of_contract_values(number, runtime):
    manifest = yaml.safe_load((_folder(number) / "module.yaml").read_text())
    control = manifest["controls"][0]["id"]
    with pytest.raises(RuntimeContractError):
        runtime.run("dsp-radar", _folder(number).name, {control: -99999})


def test_roc_monotonicity_and_population_recovery(scenarios):
    result = scenarios[28]["baseline"]
    for trace in result["plots"]["roc"]["data"]:
        assert trace["x"][0] == trace["y"][0] == 1
        assert trace["x"][-1] == trace["y"][-1] == 0
        assert np.all(np.diff(trace["x"]) <= 0) and np.all(np.diff(trace["y"]) <= 0)
    for trace in result["plots"]["variance_sweep"]["data"]:
        assert np.all(np.diff(trace["y"]) < 0)
    assert (
        scenarios[28]["broken"]["diagnostics"]["signature"][9]
        == result["diagnostics"]["signature"][4]
    )
