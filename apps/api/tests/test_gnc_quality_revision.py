"""Physical regressions for twelve Controls repairs, independent of headline metrics."""

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
COURSE = ROOT / "courses/controls-gnc"
BASELINE = "00983cab0599b1ce3a613a2cc8ef42eb7b45f0b4"
SELECTED = (36, 38, 42, 43, 45, 46, 47, 48, 49, 50, 51, 55)


def load(path):
    spec = importlib.util.spec_from_file_location("quality_model", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def folder(n):
    return next((COURSE / "modules").glob(f"{n}-*"))


def manifest(n):
    return yaml.safe_load((folder(n) / "module.yaml").read_text())


def run(n, **changes):
    p = {c["id"]: c["default"] for c in manifest(n)["controls"]}
    p.update(changes)
    return load(folder(n) / "experiment.py").run(p)


def detail(n, **changes):
    return run(n, **changes)["diagnostics"]


def test_exact_baseline_contract_payloads_and_prerequisite_graph():
    contract = yaml.safe_load((ROOT / "contracts/active-batch.yaml").read_text())
    assert contract["batch"]["id"] == "ELP-GNC-SEMANTIC-QUALITY-12"
    assert contract["sources"]["baseline_commit"] == BASELINE
    changed = subprocess.check_output(
        ["git", "diff", "--name-only", BASELINE, "--", "courses", ".gitmodules"],
        cwd=ROOT,
        text=True,
    ).splitlines()
    allowed = [f"courses/controls-gnc/modules/{n}-*/**" for n in SELECTED] + [
        "courses/controls-gnc/expansion_reference_cases.py",
        "courses/controls-gnc/expansion-map.yaml",
        "courses/controls-gnc/competency-map.yaml",
    ]
    assert all(any(fnmatch.fnmatch(p, a) for a in allowed) for p in changed)
    path = "courses/controls-gnc/competency-map.yaml"
    old = yaml.safe_load(
        subprocess.check_output(["git", "show", f"{BASELINE}:{path}"], cwd=ROOT, text=True)
    )
    new = yaml.safe_load((ROOT / path).read_text())
    assert [(r["id"], r["depends_on"], r["competency_ids"]) for r in old["modules"]] == [
        (r["id"], r["depends_on"], r["competency_ids"]) for r in new["modules"]
    ]
    assert new["count_derivation"] == old["count_derivation"]
    assert new["batch_plan"] == old["batch_plan"]


def test_unselected_reference_definitions_origins_and_outputs_are_exact(tmp_path):
    path = COURSE / "expansion_reference_cases.py"
    old = subprocess.check_output(
        ["git", "show", f"{BASELINE}:{path.relative_to(ROOT)}"], cwd=ROOT, text=True
    )
    historical = tmp_path / "old.py"
    historical.write_text(old)
    before = load(historical)
    after = load(path)

    def definitions(source):
        return {
            n.name: ast.get_source_segment(source, n)
            for n in ast.parse(source).body
            if isinstance(n, ast.FunctionDef)
        }

    original, current = definitions(old), definitions(path.read_text())
    for n in range(25, 69):
        if n in SELECTED:
            continue
        assert original[f"_p{n}"] == current[f"_p{n}"]
        assert before.origin(n) == after.origin(n)
        for p in yaml.safe_load((folder(n) / "design.yaml").read_text())["scenarios"].values():
            np.testing.assert_array_equal(
                before.reference_signature(n, p), after.reference_signature(n, p)
            )


@pytest.mark.parametrize("n", SELECTED)
def test_independent_five_cases_and_portable_checkpoint(n):
    design = yaml.safe_load((folder(n) / "design.yaml").read_text())
    reference = load(COURSE / "expansion_reference_cases.py")
    assert design["tolerance"] == {"absolute": 1e-8, "relative": 1e-8}
    assert any(
        b.get("source") == "assessment.md" and b.get("title") == "Course checkpoint"
        for b in manifest(n)["blocks"]
    )
    checkpoint = (folder(n) / "assessment.md").read_text()
    assert (
        f"P{n} evidence task" in checkpoint
        and "Reasoning rubric" in checkpoint
        and "no learner score is stored" in checkpoint
    )
    for scenario, p in design["scenarios"].items():
        expected = reference.reference_signature(n, p)
        actual = load(folder(n) / "experiment.py").run(p)["diagnostics"]["signature"]
        np.testing.assert_allclose(actual, expected, atol=1e-8, rtol=1e-8)
        for name, values in [("expected-independent", expected), ("actual-production", actual)]:
            saved = json.loads((folder(n) / f"evidence/{name}.json").read_text())
            np.testing.assert_allclose(
                saved["cases"][scenario]["signature"], values, atol=1e-8, rtol=1e-8
            )


@pytest.fixture(scope="module")
def runtime():
    return ExperimentRuntime(CourseCatalog([ROOT / "courses"]))


@pytest.mark.parametrize("n", SELECTED)
def test_all_control_corners_use_real_runtime_and_finite_outputs(n, runtime):
    module = manifest(n)
    sliders = module["controls"][:2]
    for a, b, fault in itertools.product(
        *[[c["minimum"], c["maximum"]] for c in sliders], [False, True]
    ):
        result = runtime.run(
            "controls-gnc",
            module["id"],
            {sliders[0]["id"]: a, sliders[1]["id"]: b, "broken_mode": fault},
        )
        assert all(np.isfinite(m.value) for m in result.metrics)
        for plot in result.plots.values():
            for trace in plot.data:
                assert np.isfinite(trace["x"]).all() and np.isfinite(trace["y"]).all()


@pytest.mark.parametrize("fault", [False, True])
def test_state_feedback_full_command_matches_analytic_velocity_and_acceleration(fault):
    d = detail(36, broken_mode=fault)
    t = d["time"]
    kp, kd = d["gains"]
    scale = d["feedforward"] / kp
    # Differentiated two-exponential step response, independent of matrix propagation.
    velocity = scale * 4 * (np.exp(-2 * t) - np.exp(-4 * t))
    acceleration = scale * 4 * (-2 * np.exp(-2 * t) + 4 * np.exp(-4 * t))
    np.testing.assert_allclose(d["velocity"], velocity, atol=1e-12)
    np.testing.assert_allclose(d["acceleration"], acceleration, atol=1e-12)
    assert max(abs(d["feedforward"] - kp * d["position"] - d["acceleration"])) > 0.1
    np.testing.assert_allclose(
        d["acceleration"], d["feedforward"] - kp * d["position"] - kd * d["velocity"], atol=1e-12
    )


def test_lqr_is_cost_derived_and_augmented_states_obey_the_transition():
    from scipy.linalg import expm

    d = detail(38)
    P = d["P"]
    A = np.array([[0.0, 1.0], [0.0, 0.0]])
    B = np.array([[0.0], [1.0]])
    np.testing.assert_allclose(d["K"], [[2.25, np.sqrt(3) * 1.5]], atol=1e-12)
    np.testing.assert_allclose(A.T @ P + P @ A - P @ B @ B.T @ P + d["Q"], 0, atol=1e-11)
    np.testing.assert_allclose(
        d["augmented_state"][1:],
        d["augmented_state"][:-1] @ expm(d["augmented_matrix"] * np.diff(d["time"])[0]).T,
        atol=1e-12,
    )
    # Independently integrate physical plant and observer coordinates, rather than
    # trusting the returned augmented matrix or only its block-triangular spectrum.
    from scipy.integrate import solve_ivp

    gain = np.array([2.25, np.sqrt(3) * 1.5])
    injection = np.array([13.5, 40.5])

    def plant_and_observer(_time, state):
        x, velocity, estimated_x, estimated_velocity = state
        command = -gain @ np.array([estimated_x, estimated_velocity])
        innovation = x - estimated_x
        return [
            velocity,
            command,
            estimated_velocity + injection[0] * innovation,
            command + injection[1] * innovation,
        ]

    independent = solve_ivp(
        plant_and_observer,
        [0.0, d["time"][-1]],
        [1.0, 0.0, 0.9, 0.0],
        t_eval=d["time"],
        method="DOP853",
        rtol=1e-12,
        atol=1e-13,
    )
    assert independent.success
    physical = independent.y.T
    np.testing.assert_allclose(d["augmented_state"][:, :2], physical[:, :2], atol=1e-11)
    np.testing.assert_allclose(
        d["augmented_state"][:, 2:], physical[:, :2] - physical[:, 2:], atol=1e-11
    )
    fast = detail(38, observer_speed_ratio=8.0)
    np.testing.assert_array_equal(d["K"], fast["K"])
    assert d["signature"][0] == fast["signature"][0]
    assert detail(38, broken_mode=True)["signature"][1] > 0


@pytest.mark.parametrize("fault", [False, True])
def test_actual_integrator_peak_actuator_bounds_switch_and_censoring(fault):
    d = detail(42, broken_mode=fault, actuator_limit=0.4)
    assert max(abs(d["applied"])) <= 0.4
    assert d["signature"][2] == max(abs(d["integral"]))
    np.testing.assert_allclose(
        np.diff(d["state"]), 0.01 * (-d["state"][:-1] + d["applied"][:-1]), atol=1e-15
    )
    idx = np.r_[np.arange(300, 1200)]
    kaw = 0 if fault else 4
    np.testing.assert_allclose(
        np.diff(d["integral"])[idx],
        0.01
        * (
            1.2 * (d["reference"][idx] - d["state"][idx])
            + kaw * (d["applied"][idx] - d["requested"][idx])
        ),
        atol=1e-14,
    )
    if not fault:
        assert abs(d["signature"][0]) < 1e-14
    if not d["recovery_observed"]:
        assert d["signature"][1] == 5 and abs(d["state"][-1] - 0.2) > 0.04


@pytest.mark.parametrize("fault", [False, True])
def test_double_well_energy_balance_and_true_vector_field(fault):
    d = detail(43, broken_mode=fault)
    x = d["position"]
    v = d["velocity"]
    t = d["time"]
    np.testing.assert_allclose(d["energy"], v * v / 2 - x * x / 2 + x**4 / 4, atol=1e-12)
    np.testing.assert_allclose(
        d["energy"] - d["energy"][0], d["damping_work"], atol=2e-9, rtol=1e-10
    )
    # Centered differences independently check the plotted phase trajectory.
    np.testing.assert_allclose(np.gradient(x, t)[2:-2], v[2:-2], atol=0.006, rtol=0.002)
    np.testing.assert_allclose(
        np.gradient(v, t)[2:-2], (x - x**3 - d["damping"] * v)[2:-2], atol=0.015, rtol=0.004
    )
    assert (
        np.all(np.diff(d["energy"]) >= -1e-10) if fault else np.all(np.diff(d["energy"]) <= 1e-10)
    )
    zero = detail(43, damping_per_s=0.0)
    np.testing.assert_allclose(zero["energy"], 0.8, atol=1e-10)


def test_barrier_reevaluates_and_preserves_every_sample():
    d = detail(45)
    h = d["clearance"]
    u = d["command"]
    np.testing.assert_allclose(np.diff(h), 0.01 * u[:-1], atol=1e-15)
    np.testing.assert_allclose(u, np.maximum(-1.5, -2 * h), atol=1e-15)
    assert min(h) >= 0 and min(d["barrier_residual"]) >= 0 and u[-1] != u[0]
    assert detail(45, broken_mode=True)["signature"][1] < 0
    initial = detail(45, barrier_gain_per_s=8.0, nominal_closing_speed=0.1)
    assert initial["command"][0] == -0.1
    slow_fault = detail(45, barrier_gain_per_s=8.0, nominal_closing_speed=0.1, broken_mode=True)
    # An inactive filter is not an observed safety failure inside this finite window.
    np.testing.assert_allclose(initial["clearance"], slow_fault["clearance"], atol=1e-14)
    assert min(slow_fault["clearance"]) > 0


def test_gain_table_knots_off_grid_and_refinement():
    d = detail(46)
    grid = d["grid"]
    gain = d["interpolated_gain"]
    for node, table in zip(d["knots"], d["table"], strict=True):
        assert gain[np.argmin(abs(grid - node))] == table
    assert d["signature"][1] == 0 and d["signature"][2] > 0
    assert detail(46, operating_point=0.6)["signature"][1] > 0
    assert detail(46, grid_spacing=0.05)["signature"][2] < d["signature"][2]
    assert detail(46, broken_mode=True)["signature"][2] > d["signature"][2]


def test_nonlinear_cancel_exact_limit_and_declared_escape_event():
    exact = detail(47, model_mismatch=0.0)
    np.testing.assert_allclose(exact["state"], np.exp(-2 * exact["time"]), atol=1e-11)
    d = detail(47, model_mismatch=0.5, tracking_gain_per_s=0.2)
    assert d["escape_observed"] and d["time"][-1] < 4
    assert d["state"][-1] == pytest.approx(10, abs=1e-10)
    analytic = 1 / (2.5 - 1.5 * np.exp(0.2 * d["time"]))
    np.testing.assert_allclose(d["state"], analytic, atol=2e-9, rtol=1e-10)
    np.testing.assert_allclose(d["input"], -0.5 * d["state"] ** 2 - 0.2 * d["state"], atol=1e-12)


def test_sensitivity_uses_dimensionless_transfer_and_actual_uncertainty():
    d = detail(48)
    delta = d["uncertainty"]
    w = d["frequency"]
    assert delta[0] == -0.3 and delta[-1] == 0.3
    actual = abs((1 + delta[:, None] + 1j * w) / (2.5 + delta[:, None] + 1j * w))
    np.testing.assert_allclose(d["sensitivity"], actual, atol=1e-14)
    assert not detail(48, broken_mode=True)["family_stable"]
    collapsed = detail(48, uncertainty_radius=0.0)
    np.testing.assert_allclose(
        collapsed["sensitivity"], np.tile(collapsed["sensitivity"][0], (81, 1)), atol=0
    )


@pytest.mark.parametrize("horizon,limit", [(2, 0.1), (6, 0.8), (20, 2.0)])
def test_mpc_whole_plan_recurrence_objective_kkt_and_receding_execution(horizon, limit):
    model = load(folder(49) / "experiment.py")
    u, x, cost, residual = model.solve_plan(1.5, horizon, limit)
    np.testing.assert_allclose(x, 1.5 + np.cumsum(u), atol=1e-13)
    assert max(abs(u)) <= limit and residual < 1e-9
    assert cost == pytest.approx(sum(x * x) + 0.1 * sum(u * u))
    # Coordinate perturbations are feasible negative tests of the optimized objective.
    for j in range(horizon):
        for sign in [-1, 1]:
            perturbed = u.copy()
            perturbed[j] = np.clip(perturbed[j] + sign * 0.001, -limit, limit)
            xx = 1.5 + np.cumsum(perturbed)
            assert sum(xx * xx) + 0.1 * sum(perturbed * perturbed) >= cost - 1e-12
    d = detail(49, prediction_horizon=horizon, input_limit=limit)
    np.testing.assert_allclose(np.diff(d["state"]), d["input"], atol=1e-14)
    assert max(d["kkt_residuals"]) < 1e-9
    assert detail(49, broken_mode=True)["signature"][1] > 0


def test_identification_recovers_noise_free_coefficients_and_uses_heldout_free_run():
    model = load(folder(50) / "experiment.py")
    u, train, _ = model.identification_data(1.0, 2.0, noise=0.0)
    theta = np.linalg.lstsq(np.column_stack([train[:-1], u[:300]]), train[1:], rcond=None)[0]
    np.testing.assert_allclose(theta, [0.82, 0.18], atol=1e-13)
    d = detail(50)
    a, b = d["theta"]
    np.testing.assert_allclose(
        d["prediction"][1:], a * d["prediction"][:-1] + b * d["input"][300:], atol=1e-14
    )
    assert d["training_indices"][1] < d["validation_indices"][0] and d["rank"] == 2
    broken = detail(50, broken_mode=True)
    assert broken["rank"] == 1 and broken["theta"][1] == 0 and broken["signature"][2] > 0.5
    assert not np.array_equal(d["input"], detail(50, frequency_spread_hz=3.0)["input"])


def test_rls_matches_batch_information_at_each_sample_and_zero_excitation():
    d = detail(51, forgetting_factor=1.0)
    phi = d["regressor"]
    y = d["measurement"]
    information = 0.1 + np.cumsum(phi * phi)
    estimate = np.cumsum(phi * y) / information
    np.testing.assert_allclose(d["estimate"][1:], estimate, atol=1e-13)
    np.testing.assert_allclose(d["covariance"][1:], 1 / information, atol=1e-13)
    model = load(folder(51) / "experiment.py")
    _, _, theta, P, gain = model.rls_history(0.98, 0.0)
    assert np.all(theta == 0) and np.all(gain == 0) and np.all(np.diff(P) > 0)
    _, _, theta, _, _ = model.rls_history(1.0, 1.0, noise=0.0)
    assert abs(theta[-1] - 1) < 0.002


@pytest.mark.parametrize("alpha", [0.2, 0.7, 1.0, 2.0])
def test_sigma_points_reconstruct_moments_and_negative_weights_are_valid(alpha):
    d = detail(55, sigma_spread=alpha)
    points = d["points"]
    wm = d["mean_weights"]
    wc = d["covariance_weights"]
    assert sum(wm) == pytest.approx(1)
    assert wm @ points == pytest.approx(0, abs=1e-14)
    assert wm @ (points**2) == pytest.approx(0.64)
    assert d["mean"] == pytest.approx(0.64) and d["variance"] == pytest.approx(0.8192)
    assert sum(wc) == pytest.approx(4 - alpha * alpha)
    if alpha < 1:
        assert min(wm) < 0
    fault = detail(55, sigma_spread=alpha, broken_mode=True)
    assert fault["mean"] == pytest.approx(0.64)
    assert fault["variance"] == pytest.approx((alpha * alpha - 1) * 0.8**4, abs=1e-12)
    zero = detail(55, state_standard_deviation=0.0, sigma_spread=alpha)
    assert zero["mean"] == zero["variance"] == 0
