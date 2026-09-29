"""Executed navigation and geometry mechanisms, independent of display summaries."""

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
BASELINE = "8820f21d349836b63db00f1e596f5eb00b488ab9"
SELECTED = {"controls-gnc": (56, 57, 60, 61, 62, 64, 65), "robotics-autonomy": (25, 26, 27, 28, 29)}
CASES = [(course, n) for course, numbers in SELECTED.items() for n in numbers]


def load(path):
    spec = importlib.util.spec_from_file_location("navigation_quality", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def folder(course, n):
    return next((ROOT / "courses" / course / "modules").glob(f"{n}-*"))


def run(n, course="controls-gnc", **changes):
    path = folder(course, n)
    manifest = yaml.safe_load((path / "module.yaml").read_text())
    p = {c["id"]: c["default"] for c in manifest["controls"]}
    p.update(changes)
    return load(path / "experiment.py").run(p)["diagnostics"]


def test_exact_scope_and_prerequisite_inventory():
    contract = yaml.safe_load((ROOT / "contracts/active-batch.yaml").read_text())
    assert contract["batch"]["id"] == "ELP-NAV-GEOMETRY-QUALITY-12"
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
    return ExperimentRuntime(CourseCatalog([ROOT / "courses"]))


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


def test_rts_whole_trajectory_matches_joint_conditioning_and_terminal_equality():
    d = run(56)
    q = 0.08
    r = 0.4
    k = np.arange(41)
    C = 1 + q * np.minimum.outer(k, k)
    y = np.array(d["measurements"])
    posterior = C @ np.linalg.solve(C + r * np.eye(41), y)
    covariance = C - C @ np.linalg.solve(C + r * np.eye(41), C)
    np.testing.assert_allclose(d["smoothed_mean"], posterior, atol=1e-10)
    np.testing.assert_allclose(d["smoothed_variance"], np.diag(covariance), atol=1e-10)
    assert d["smoothed_mean"][-1] == d["filtered_mean"][-1]
    assert d["smoothed_variance"][-1] == d["filtered_variance"][-1]
    assert np.all(np.array(d["smoothed_variance"]) <= np.array(d["filtered_variance"]) + 1e-12)
    assert min(d["smoothed_variance"]) > 0
    broken = run(56, process_variance=0.3, broken_mode=True)
    np.testing.assert_array_equal(broken["smoothed_mean"], broken["filtered_mean"])
    assert broken["signature"] != run(56, broken_mode=True)["signature"]


def test_quaternion_group_vector_calibration_and_scaled_identity_limit():
    model = load(folder("controls-gnc", 57) / "experiment.py")
    d = run(57)
    for q, R, used, truth in zip(
        d["quaternions"], d["matrices"], d["used_vectors"], d["true_vectors"], strict=True
    ):
        np.testing.assert_allclose(model.quaternion_matrix(-np.array(q)), R, atol=1e-14)
        np.testing.assert_allclose(np.array(R).T @ R, np.eye(3), atol=1e-14)
        np.testing.assert_allclose(used, truth, atol=1e-14)
    assert np.linalg.norm(d["raw_vectors"][-1] - d["true_vectors"][-1]) > 0
    zero = run(57, yaw_angle_deg=0, sensor_misalignment_deg=0, broken_mode=True)
    assert zero["signature"][0] == pytest.approx(0.2)
    assert zero["signature"][1:] == [0.0, 0.0]


@pytest.mark.parametrize("broken", (False, True))
def test_navigation_solution_residuals_and_stationarity(broken):
    model = load(folder("controls-gnc", 60) / "experiment.py")
    d = run(60, broken_mode=broken)
    predicted = model._ranges(np.array(d["satellites"]), np.array(d["state"][:3]))[0] + (
        0 if broken else d["state"][3]
    )
    np.testing.assert_allclose(np.array(d["observations"]) - predicted, d["residual"], atol=1e-10)
    np.testing.assert_allclose(np.array(d["jacobian"]).T @ d["residual"], 0, atol=1e-8)
    assert len(d["state"]) == (3 if broken else 4)
    assert (
        run(60, geometry_dilution=12)["condition_number"]
        > run(60, geometry_dilution=1)["condition_number"]
    )


def test_error_state_injection_joseph_covariance_and_bias_drift():
    good = run(61)
    bad = run(61, broken_mode=True)
    assert bad["states"][-1, 0] - 40 == pytest.approx(8.0, abs=1e-10)
    assert abs(good["states"][-1, 0] - 40) < 0.2
    assert abs(good["states"][-1, 2] - 0.04) < 0.01
    np.testing.assert_allclose(good["covariances"], bad["covariances"], atol=1e-12)
    assert min(np.linalg.eigvalsh(good["covariances"]).ravel()) > 0
    np.testing.assert_array_equal(good["reset_error_state"], np.zeros(3))
    np.testing.assert_array_equal(good["reset_jacobian"], np.eye(3))
    unusual = run(61, gnss_interval_s=0.7)
    np.testing.assert_allclose(unusual["update_time"], np.arange(0.7, 20.0, 0.7), atol=1e-9)


def test_exclusion_recomputes_rows_state_and_fit_without_forced_zero_fault_alarm():
    d = run(62)
    broken = run(62, broken_mode=True)
    zero = run(62, fault_magnitude_m=0)
    assert d["suspect"] == 2 and d["alarm"]
    assert 2 not in d["retained_rows"] and len(d["retained_rows"]) == 7
    assert len(broken["retained_rows"]) == 8
    assert not zero["alarm"] and len(zero["retained_rows"]) == 8
    high_threshold = run(62, integrity_threshold=10)
    assert not high_threshold["alarm"] and len(high_threshold["retained_rows"]) == 8
    assert np.linalg.norm(d["state"] - d["before_state"]) > 1
    np.testing.assert_allclose(np.array(d["jacobian"]).T @ d["post_residual"], 0, atol=1e-8)
    assert d["signature"][2] < broken["signature"][2]


def test_guidance_integrates_distinct_trajectories_and_actual_events():
    d = run(64)
    bad = run(64, broken_mode=True)
    assert d["signature"][0] == pytest.approx(-bad["signature"][0])
    for _law, trajectory in d["trajectories"].items():
        states = np.array(trajectory["states"])
        t = np.array(trajectory["time"])
        np.testing.assert_allclose(
            trajectory["separation"],
            np.linalg.norm(states[:, 3:5] - states[:, :2], axis=1),
            atol=1e-12,
        )
        assert t[-1] <= 8 and len(t) == 121
        if trajectory["captured"]:
            assert trajectory["separation"][-1] == pytest.approx(1, abs=1e-9)
    assert d["trajectories"]["pn"]["time"][-1] != d["trajectories"]["pursuit"]["time"][-1]
    assert bad["signature"][1] > d["signature"][1]


def test_terminal_dynamics_box_feasibility_and_kkt():
    d = run(65)
    u = np.array(d["commands"])
    states = np.array(d["states"])
    dt = 0.1
    np.testing.assert_allclose(
        states[1:, 0], states[:-1, 0] + dt * states[:-1, 1] + dt * dt * u / 2, atol=1e-12
    )
    np.testing.assert_allclose(states[1:, 1], states[:-1, 1] + dt * u, atol=1e-12)
    assert max(abs(u)) <= 20
    assert np.linalg.norm(d["projected_gradient"], np.inf) < 1e-9
    assert run(65, acceleration_limit_m_s2=3)["terminal"][0] >= 24 - 1e-10
    assert run(65, broken_mode=True)["signature"][1] > 0


def test_constraint_projection_rank_tangency_and_zero_offset_fault():
    d = run(25, "robotics-autonomy")
    theta = np.array(d["angles"])
    tangent = np.column_stack([-np.sin(theta), np.cos(theta)])
    np.testing.assert_allclose(d["velocities"], tangent * tangent[:, 0, None], atol=1e-14)
    np.testing.assert_allclose(d["radial_velocity"], 0, atol=1e-14)
    assert set(d["constraint_ranks"]) == {1}
    zero = run(25, "robotics-autonomy", constraint_offset_m=0, broken_mode=True)
    assert zero["signature"][0] < 1e-14 and max(abs(zero["radial_velocity"])) > 0.5
    changed = run(25, "robotics-autonomy", constraint_offset_m=0.2)
    np.testing.assert_allclose(changed["configurations"], d["configurations"], atol=1e-14)


def test_rotation_blend_interior_failure_and_rigid_inverse():
    d = run(26, "robotics-autonomy")
    bad = run(26, "robotics-autonomy", rotation_angle_deg=180, broken_mode=True)
    assert max(d["rigid_inverse_point_error"]) < 1e-14
    assert bad["orthogonality"][0] < 1e-14 and bad["orthogonality"][-1] < 1e-14
    assert bad["determinants"][60] == pytest.approx(0, abs=1e-14)
    assert max(bad["rigid_inverse_point_error"]) > 0.1
    assert run(26, "robotics-autonomy", rotation_angle_deg=0, broken_mode=True)["signature"][0] == 0


def test_dual_wrench_power_and_separate_roundtrip_units():
    d = run(27, "robotics-autonomy")
    bad = run(27, "robotics-autonomy", broken_mode=True)
    np.testing.assert_allclose(d["powers"], 0.69, atol=1e-14)
    np.testing.assert_allclose(d["angular_roundtrip_rad_s"], 0, atol=1e-14)
    assert max(bad["linear_roundtrip_m_s"]) < 1e-14
    assert bad["signature"][0] > 0.01
    for A, V, W in zip(d["adjoints"], d["twists"], d["wrenches"], strict=True):
        np.testing.assert_allclose(np.array(A).T @ W, d["source_wrench"], atol=1e-14)
        assert np.dot(W, V) == pytest.approx(0.69, abs=1e-14)


def test_position_jacobian_derivatives_and_real_singularity():
    good = run(28, "robotics-autonomy")
    bad = run(28, "robotics-autonomy", broken_mode=True)
    np.testing.assert_allclose(good["jacobians"], good["finite_differences"], atol=1e-9)
    assert bad["signature"][2] > 0.7
    assert run(28, "robotics-autonomy", elbow_angle_deg=0)["signature"][0] < 1e-14
    assert good["signature"][0] > 0.1


def test_null_projector_idempotence_and_damping_residual_are_distinct():
    d = run(29, "robotics-autonomy")
    J = np.array(d["jacobian"])
    N = np.array(d["projector"])
    np.testing.assert_allclose(N @ N, N, atol=1e-14)
    np.testing.assert_allclose(J @ N, 0, atol=1e-14)
    np.testing.assert_allclose(d["task_velocity"], np.tile(J @ d["primary"], (121, 1)), atol=1e-14)
    assert d["signature"][0] > 0.001 and d["signature"][1] < 1e-14
    assert run(29, "robotics-autonomy", damping=0)["signature"][0] < 1e-14
    np.testing.assert_array_equal(
        run(29, "robotics-autonomy", null_gain_per_s=0)["joint_velocity"],
        run(29, "robotics-autonomy", null_gain_per_s=0, broken_mode=True)["joint_velocity"],
    )


@pytest.mark.parametrize(
    "course,n,changes",
    [
        ("controls-gnc", 57, {"yaw_angle_deg": 0}),
        ("robotics-autonomy", 28, {"elbow_angle_deg": 0}),
        ("robotics-autonomy", 29, {"null_gain_per_s": 0}),
    ],
)
def test_zero_span_keeps_real_point_data_visible(course, n, changes):
    path = folder(course, n)
    manifest = yaml.safe_load((path / "module.yaml").read_text())
    p = {c["id"]: c["default"] for c in manifest["controls"]}
    p.update(changes)
    result = load(path / "experiment.py").run(p)
    for plot in result["plots"].values():
        for trace in plot["data"]:
            assert np.ptp(trace["x"]) == 0
            assert "markers" in trace["mode"]
            assert np.isfinite(trace["y"]).all()
