"""Executed Robotics dynamics and interaction, with independent trajectory checks."""

import ast
import fnmatch
import importlib.util
import itertools
import json
import subprocess
from pathlib import Path

import numpy as np
import pytest
import yaml

from elp_api.catalog import CourseCatalog
from elp_api.runtime import ExperimentRuntime

ROOT = Path(__file__).resolve().parents[3]
BASELINE = "e8d94c521a086a93a3b595c035867c19866bbdbd"
SELECTED = {"robotics-autonomy": tuple(range(30, 42))}
CASES = [(course, n) for course, numbers in SELECTED.items() for n in numbers]


def load(path):
    spec = importlib.util.spec_from_file_location("navigation_quality", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def folder(course, n):
    return next((ROOT / "courses" / course / "modules").glob(f"{n}-*"))


def run(n, course="robotics-autonomy", **changes):
    path = folder(course, n)
    manifest = yaml.safe_load((path / "module.yaml").read_text())
    p = {c["id"]: c["default"] for c in manifest["controls"]}
    p.update(changes)
    return load(path / "experiment.py").run(p)["diagnostics"]


def test_exact_scope_and_prerequisite_inventory():
    contract = yaml.safe_load((ROOT / "contracts/active-batch.yaml").read_text())
    assert contract["batch"]["id"] == "ELP-ROBOTICS-DYNAMICS-QUALITY-12"
    assert contract["sources"]["baseline_commit"] == BASELINE
    assert (
        subprocess.check_output(
            ["git", "rev-parse", BASELINE + "^{tree}"], cwd=ROOT, text=True
        ).strip()
        == contract["sources"]["baseline_tree"]
    )
    paths = subprocess.check_output(
        ["git", "diff", "--name-only", BASELINE, "--", "courses", ".gitmodules"],
        cwd=ROOT,
        text=True,
    ).splitlines()
    allowed = [f"courses/{c}/modules/{n}-*/**" for c, n in CASES] + [
        f"courses/{c}/{name}"
        for c in SELECTED
        for name in ("expansion_reference_cases.py", "expansion-map.yaml", "competency-map.yaml")
    ]
    assert all(any(fnmatch.fnmatch(p, a) for a in allowed) for p in paths)
    for course in SELECTED:
        path = f"courses/{course}/competency-map.yaml"
        before = yaml.safe_load(
            subprocess.check_output(["git", "show", f"{BASELINE}:{path}"], cwd=ROOT, text=True)
        )
        after = yaml.safe_load((ROOT / path).read_text())
        assert [(m["id"], m["depends_on"], m["competency_ids"]) for m in before["modules"]] == [
            (m["id"], m["depends_on"], m["competency_ids"]) for m in after["modules"]
        ]
        assert before["count_derivation"] == after["count_derivation"]
        assert before["batch_plan"] == after["batch_plan"]


@pytest.mark.parametrize("course", SELECTED)
def test_unselected_reference_definitions_origins_and_five_outputs(course, tmp_path):
    path = ROOT / "courses" / course / "expansion_reference_cases.py"
    original = subprocess.check_output(
        ["git", "show", f"{BASELINE}:{path.relative_to(ROOT)}"], cwd=ROOT, text=True
    )
    historical = tmp_path / "reference.py"
    historical.write_text(original)
    before, after = load(historical), load(path)

    def definitions(source):
        return {
            n.name: ast.get_source_segment(source, n)
            for n in ast.parse(source).body
            if isinstance(n, ast.FunctionDef)
        }

    old, new = definitions(original), definitions(path.read_text())
    for n in range(25, 69 if course == "controls-gnc" else 70):
        if n in SELECTED[course]:
            continue
        assert old[f"_p{n}"] == new[f"_p{n}"]
        assert before.origin(n) == after.origin(n)
        design = yaml.safe_load((folder(course, n) / "design.yaml").read_text())
        for p in design["scenarios"].values():
            np.testing.assert_array_equal(
                before.reference_signature(n, p), after.reference_signature(n, p)
            )


@pytest.mark.parametrize("course,n", CASES)
def test_five_independent_cases_retained_and_embedded(course, n):
    path = folder(course, n)
    design = yaml.safe_load((path / "design.yaml").read_text())
    manifest = yaml.safe_load((path / "module.yaml").read_text())
    assert design["tolerance"] == {"absolute": 1e-8, "relative": 1e-8}
    assert manifest["runtime"]["timeout_seconds"] == 3
    assert any(
        b.get("source") == "assessment.md" and b.get("title") == "Course checkpoint"
        for b in manifest["blocks"]
    )
    assessment = (path / "assessment.md").read_text()
    assert (
        f"P{n} evidence task" in assessment
        and "Reasoning rubric" in assessment
        and "no learner score is stored" in assessment
    )
    ref = load(ROOT / "courses" / course / "expansion_reference_cases.py")
    model = load(path / "experiment.py")
    for scenario, p in design["scenarios"].items():
        expected = ref.reference_signature(n, p)
        actual = model.run(p)["diagnostics"]["signature"]
        np.testing.assert_allclose(actual, expected, atol=1e-8, rtol=1e-8)
        for name, value in [("expected-independent", expected), ("actual-production", actual)]:
            saved = json.loads((path / f"evidence/{name}.json").read_text())
            np.testing.assert_allclose(
                saved["cases"][scenario]["signature"], value, atol=1e-8, rtol=1e-8
            )


@pytest.fixture(scope="module")
def runtime():
    return ExperimentRuntime(CourseCatalog([ROOT / "courses/robotics-autonomy"]))


@pytest.mark.parametrize("course,n", CASES)
def test_all_eight_control_corners_through_unchanged_runtime(course, n, runtime):
    path = folder(course, n)
    manifest = yaml.safe_load((path / "module.yaml").read_text())
    controls = manifest["controls"][:2]
    for a, b, fault in itertools.product(
        *[(c["minimum"], c["maximum"]) for c in controls], (False, True)
    ):
        p = {controls[0]["id"]: a, controls[1]["id"]: b, "broken_mode": fault}
        result = runtime.run(course, path.name, p)
        assert np.isfinite(result.diagnostics["signature"]).all()
        assert result.diagnostics["broken_active"] == fault
        for plot in result.model_dump(mode="json")["plots"].values():
            for trace in plot["data"]:
                assert np.isfinite(trace["x"]).all() and np.isfinite(trace["y"]).all()


def details(n, broken=False, **changes):
    path = folder("robotics-autonomy", n)
    p = {
        c["id"]: c["default"]
        for c in yaml.safe_load((path / "module.yaml").read_text())["controls"]
    }
    p.update(broken_mode=broken, **changes)
    production = load(path / "experiment.py").run(p)["diagnostics"]
    reference = load(
        ROOT / "courses/robotics-autonomy/expansion_reference_cases.py"
    ).robotics_dynamics_reference(n, p)
    return production, reference


TRACE_FIELDS = {
    30: ["jacobians", "torques", "powers"],
    31: ["M", "C", "Mdot", "gravity"],
    32: ["fitted_parameters", "heldout_residual", "regressor"],
    33: ["position", "velocity", "acceleration"],
    35: ["state", "applied_torque", "tracking_error", "gravity_compensation_defect"],
    36: ["J", "M", "Lambda", "secondary_torque", "actual_acceleration"],
    37: ["state", "energy", "contact_force"],
    38: ["position", "velocity", "normal_force"],
    39: ["energy"],
    40: ["state_body_and_absolute_rotor", "body_energy"],
    41: ["camera_points", "accepted", "pixels", "depth_sensitivity"],
}


@pytest.mark.parametrize("n", range(30, 42))
@pytest.mark.parametrize("broken", (False, True))
def test_full_mechanism_arrays_match_independent_formulations(n, broken):
    d, r = details(n, broken)
    if n == 34:
        np.testing.assert_allclose(d["states"][:, 2:], r["task_states"], atol=1e-8, rtol=1e-8)
        np.testing.assert_allclose(
            d["applied_velocity"][:, 2:], r["task_velocity"], atol=1e-8, rtol=1e-8
        )
    else:
        for key in TRACE_FIELDS[n]:
            np.testing.assert_allclose(d[key], r[key], atol=1e-8, rtol=1e-8, err_msg=key)


def test_virtual_power_and_zero_force_blind_spot():
    d = run(30)
    J = np.asarray(d["jacobians"])
    tau = np.asarray(d["torques"])
    v = np.asarray(d["joint_velocity"])
    force = np.asarray(d["force"])
    np.testing.assert_allclose(tau, np.einsum("nji,j->ni", J, force), atol=1e-12)
    np.testing.assert_allclose(tau @ v, np.einsum("nij,j->ni", J, v) @ force, atol=1e-12)
    assert run(30, broken_mode=True)["signature"][1] > 0.1
    np.testing.assert_allclose(run(30, force_n=0, broken_mode=True)["signature"][:2], 0, atol=1e-12)


def test_mass_positive_and_energy_skew_identity_are_independent_checks():
    good, bad = run(31), run(31, broken_mode=True)
    for d in (good, bad):
        M = np.asarray(d["M"])
        np.testing.assert_allclose(M, M.T, atol=1e-12)
        assert np.linalg.eigvalsh(M).min() > 0
        assert np.asarray(d["inertia_eigenvalues"]).min() > 0
    S = good["Mdot"] - 2 * good["C"]
    np.testing.assert_allclose(S + S.T, 0, atol=1e-12)
    assert bad["signature"][1] > 1e-3
    assert run(31, broken_mode=True, elbow_angle_deg=0)["signature"][1] < 1e-12


def test_identification_stationarity_rank_and_heldout_replay():
    for broken in (False, True):
        d = run(32, broken_mode=broken)
        Y = d["regressor"]
        theta = d["fitted_parameters"]
        target = d["training_torque"] - 0.08 * d["training_acceleration"]
        np.testing.assert_allclose(
            Y.T @ (Y @ theta - target) + d["ridge"] * (theta - d["prior"]), 0, atol=1e-10
        )
        np.testing.assert_allclose(
            d["heldout_predicted_torque"] - d["heldout_true_torque"],
            d["heldout_residual"],
            atol=1e-12,
        )
        assert d["rank"] == (1 if broken else 2)
        if broken:
            np.testing.assert_array_equal(Y[:, 1], 0)
            assert theta[1] == pytest.approx(d["prior"][1])
    assert run(32)["signature"][0] < run(32, broken_mode=True)["signature"][0]


def test_cubic_endpoints_and_both_constraints_use_applied_time():
    good, bad = run(33), run(33, broken_mode=True)
    for d in (good, bad):
        np.testing.assert_allclose(d["position"][0], 0, atol=1e-12)
        np.testing.assert_allclose(d["position"][-1], d["displacement"], atol=1e-12)
        np.testing.assert_allclose(d["velocity"][[0, -1]], 0, atol=1e-12)
        T = d["time"][-1]
        peak = max(abs(d["displacement"]))
        assert max(abs(d["velocity"]).ravel()) == pytest.approx(1.5 * peak / T)
        assert max(abs(d["acceleration"]).ravel()) == pytest.approx(6 * peak / T**2)
    assert good["signature"][2] < 1e-12 and good["acceleration_excess"] < 1e-12
    assert bad["signature"][2] > 0 and bad["acceleration_excess"] > 0


def test_joint_servo_exponential_and_task_rate_units():
    d = run(34)
    t = d["time"]
    initial = np.array([0.18, -0.12])
    np.testing.assert_allclose(
        d["states"][:, :2] - d["goal_q"], np.exp(-3 * t[:, None]) * initial, atol=1e-9
    )
    assert max(abs(d["applied_velocity"]).ravel()) <= d["speed_limit"]
    assert d["actual_condition"] == pytest.approx(np.linalg.cond(d["goal_J"]))
    assert d["actual_condition"] != 4
    assert run(34, broken_mode=True)["signature"][1] > d["signature"][1]


def test_computed_torque_applied_input_satisfies_actual_plant():
    model = load(folder("robotics-autonomy", 35) / "experiment.py")
    for broken in (False, True):
        d = run(35, broken_mode=broken)
        np.testing.assert_array_equal(d["applied_torque"], np.clip(d["requested_torque"], -20, 20))
        for state, derivative, tau in zip(
            d["state"], d["state_derivative"], d["applied_torque"], strict=True
        ):
            M, C, g = model.dynamics(state[:2], state[2:])
            np.testing.assert_allclose(M @ derivative[2:] + C @ state[2:] + g, tau, atol=1e-10)
    exact = run(35, model_error_fraction=0)
    np.testing.assert_allclose(exact["gravity_compensation_defect"], 0, atol=1e-12)
    assert run(35, tracking_bandwidth_per_s=20)["signature"][1] <= 20


def test_operational_torque_projection_is_dynamical_not_euclidean():
    good, bad = run(36), run(36, broken_mode=True)
    for d in (good, bad):
        J, M = d["J"], d["M"]
        assert np.linalg.eigvalsh(M).min() > 0
        np.testing.assert_allclose(J @ np.linalg.solve(M, J.T) @ d["Lambda"], np.eye(2), atol=1e-10)
        np.testing.assert_allclose(
            J @ np.linalg.solve(M, d["primary_torque"] + d["secondary_torque"]),
            d["actual_acceleration"],
            atol=1e-12,
        )
    np.testing.assert_allclose(
        good["J"] @ np.linalg.solve(good["M"], good["torque_projector"]), 0, atol=1e-10
    )
    np.testing.assert_allclose(bad["J"] @ bad["torque_projector"], 0, atol=1e-10)
    assert bad["signature"][1] > 1e-3


def test_contact_energy_sign_and_censored_observation():
    good, bad = run(37), run(37, broken_mode=True)
    for d in (good, bad):
        y = d["state"]
        E = (
            0.5 * d["mass"] * y[:, [1, 3]] ** 2
            + 0.5 * (d["virtual_stiffness"] + d["environment_stiffness"]) * y[:, [0, 2]] ** 2
        )
        np.testing.assert_allclose(d["energy"], E, atol=1e-12)
        np.testing.assert_allclose(
            d["energy_derivative"], -d["effective_damping"] * y[:, [1, 3]] ** 2, atol=1e-12
        )
    assert np.diff(good["energy"], axis=0).max() < 1e-10
    assert np.diff(bad["energy"], axis=0).min() > -1e-10
    assert bad["settling_censored"] and bad["signature"][1] == 0.4


def test_hybrid_projectors_remain_orthogonal_in_wrong_frame_and_contact_can_open():
    for broken in (False, True):
        d = run(38, broken_mode=broken)
        Pf, Pt = d["force_projector"], d["motion_projector"]
        np.testing.assert_allclose(Pf @ Pt, 0, atol=1e-12)
        np.testing.assert_allclose(Pf @ Pf, Pf, atol=1e-12)
        np.testing.assert_allclose(
            d["normal_force"], 600 * np.maximum(d["position"] @ d["normal"], 0), atol=1e-10
        )
    assert run(38, broken_mode=True)["signature"][2] > 0
    np.testing.assert_allclose(
        run(38, surface_angle_deg=0)["signature"],
        run(38, surface_angle_deg=0, broken_mode=True)["signature"],
        atol=1e-12,
    )
    d, r = details(38, True, force_setpoint_n=0, surface_angle_deg=70)
    np.testing.assert_allclose(d["position"], r["position"], atol=1e-9)
    assert min(d["position"] @ d["normal"]) < 0


def test_sampled_port_work_conservation_and_causal_reflection():
    for broken in (False, True):
        d = run(39, broken_mode=broken)
        np.testing.assert_allclose(
            d["work"], d["applied_force"] * d["velocity"] * d["dt"], atol=1e-14
        )
        np.testing.assert_allclose(np.diff(d["energy"]), -d["work"], atol=1e-14)
        assert len(d["energy"]) == len(d["work"]) + 1
        assert max(abs(d["applied_force"])) <= d["force_limit"] + 1e-12
    good, bad = run(39), run(39, broken_mode=True)
    assert min(good["energy"]) >= -1e-12 and min(bad["energy"]) < -0.1
    assert good["signature"][2] > 0 and bad["signature"][2] == 0


def test_reaction_wheel_capture_event_internal_torque_and_energy():
    good, bad = run(40), run(40, broken_mode=True)
    for d in (good, bad):
        state = d["state_body_and_absolute_rotor"]
        np.testing.assert_array_equal(d["body_torque"], -d["rotor_torque"])
        np.testing.assert_allclose(d["relative_rotor_angle"], state[:, 2] - state[:, 0], atol=1e-12)
        np.testing.assert_allclose(
            d["body_energy"],
            0.5 * d["body_inertia"] * state[:, 1] ** 2
            + d["gravity_coefficient"] * (1 - np.cos(state[:, 0])),
            atol=1e-12,
        )
        assert max(abs(d["body_torque"])) <= d["torque_limit"]
    assert good["captured"] and not good["capture_censored"]
    event = good["capture_state"]
    assert (
        abs(np.arctan2(-np.sin(event[0]), -np.cos(event[0]))) <= 0.2 + 1e-10
        and abs(event[1]) <= 1.5 + 1e-10
    )
    assert bad["capture_censored"] and not bad["balance_active"].any() and bad["signature"][0] == 12
    assert abs(good["state_body_and_absolute_rotor"][-1, 3]) > 1


def test_camera_visibility_is_measured_in_transformed_coordinates():
    good, bad = run(41), run(41, broken_mode=True)
    for d in (good, bad):
        np.testing.assert_allclose(
            d["camera_points"],
            (d["world_points"] - d["camera_origin"]) @ d["camera_rotation"],
            atol=1e-12,
        )
        np.testing.assert_array_equal(d["physically_valid"], d["camera_points"][:, 2] > 0.05)
        assert d["invalid_accepted_count"] == sum(d["accepted"] & ~d["physically_valid"])
    assert good["invalid_accepted_count"] == 0 and bad["invalid_accepted_count"] > 0
    empty = run(41, point_depth_m=0.2)
    assert not empty["projection_available"] and empty["signature"][:2] == [0.0, 0.0]
    far = run(41, point_depth_m=10, broken_mode=True)
    assert far["invalid_accepted_count"] == 0 and max(far["reconstruction_error"]) > 0.1
