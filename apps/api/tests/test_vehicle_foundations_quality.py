"""Vehicle motion/tire/chassis revision: independent physics and immutable scope."""

import ast
import fnmatch
import importlib.util
import itertools
import json
import math
import subprocess
from pathlib import Path

import numpy as np
import pytest
import yaml

from elp_api.catalog import CourseCatalog
from elp_api.runtime import ExperimentRuntime

ROOT = Path(__file__).resolve().parents[3]
BASELINE = "607c716993be14e7b782897ab054a7f8478f5dc0"
COURSE = ROOT / "courses/vehicle-dynamics"


def load(path):
    spec = importlib.util.spec_from_file_location("vehicle_quality_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


REFERENCE = load(COURSE / "reference_cases.py")
VERIFY = load(ROOT / "scripts/verify-vehicle-foundations-quality.py")


def folder(n):
    return next((COURSE / "modules").glob(f"{n:02d}-*"))


def run(n, **changes):
    manifest = json.loads((folder(n) / "module.yaml").read_text())
    p = {c["id"]: c["default"] for c in manifest["controls"]}
    p.update(changes)
    return load(folder(n) / "experiment.py").run(p)


def physical(n, **changes):
    return run(n, **changes)["diagnostics"]["physical"]


def original(path):
    return subprocess.check_output(["git", "show", f"{BASELINE}:{path}"], cwd=ROOT)


def test_exact_scope_inventory_controls_and_historical_coverage():
    contract = yaml.safe_load((ROOT / "contracts/active-batch.yaml").read_text())
    assert contract["batch"]["id"] == "ELP-VEHICLE-FOUNDATIONS-QUALITY-12"
    assert contract["sources"]["baseline_commit"] == BASELINE
    assert (
        subprocess.check_output(
            ["git", "rev-parse", BASELINE + "^{tree}"], cwd=ROOT, text=True
        ).strip()
        == contract["sources"]["baseline_tree"]
    )
    changed = subprocess.check_output(
        ["git", "diff", "--name-only", BASELINE, "--", "courses", ".gitmodules"],
        cwd=ROOT,
        text=True,
    ).splitlines()
    allowed = [f"courses/vehicle-dynamics/modules/{n:02d}-*/**" for n in range(1, 13)] + [
        "courses/vehicle-dynamics/reference_cases.py",
        "courses/vehicle-dynamics/coverage.yaml",
    ]
    assert all(any(fnmatch.fnmatch(p, pattern) for pattern in allowed) for p in changed)
    # Compare bytes directly, including files that might otherwise be hidden by changed-path logic.
    tracked = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", BASELINE, "--", "courses"], cwd=ROOT, text=True
    ).splitlines()
    for path in tracked:
        if any(fnmatch.fnmatch(path, pattern) for pattern in allowed):
            continue
        if (ROOT / path).is_file():
            assert (ROOT / path).read_bytes() == original(path), path
    before = json.loads(original("courses/vehicle-dynamics/coverage.yaml"))
    after = json.loads((COURSE / "coverage.yaml").read_text())
    for n, (a, b) in enumerate(zip(before["items"], after["items"], strict=True), 1):
        if n <= 12:
            a.pop("target_content_digest")
            b.pop("target_content_digest")
        assert a == b
    for n in range(1, 13):
        path = folder(n) / "module.yaml"
        a, b = json.loads(original(path.relative_to(ROOT))), json.loads(path.read_text())
        assert a["id"] == b["id"] and a["number"] == b["number"]
        for old, new in zip(a["controls"], b["controls"], strict=True):
            assert {k: v for k, v in old.items() if k not in ("label", "description")} == {
                k: v for k, v in new.items() if k not in ("label", "description")
            }
        assert b["runtime"]["timeout_seconds"] == 3
    catalog = CourseCatalog([ROOT / "courses"]).summaries()
    assert len(catalog) == 6 and sum(len(c.modules) for c in catalog) == 290


def test_unselected_reference_definitions_and_outputs_unchanged(tmp_path):
    relative = "courses/vehicle-dynamics/reference_cases.py"
    before = original(relative).decode()
    after = (ROOT / relative).read_text()

    def definitions(text):
        return {
            n.name: ast.get_source_segment(text, n)
            for n in ast.parse(text).body
            if isinstance(n, ast.FunctionDef)
        }

    a, b = definitions(before), definitions(after)
    old_path = tmp_path / "old_reference.py"
    old_path.write_text(before)
    old = load(old_path)
    for n in range(13, 25):
        assert a[f"_p{n:02d}"] == b[f"_p{n:02d}"]
        m = json.loads((folder(n) / "module.yaml").read_text())
        p, s = [c["id"] for c in m["controls"][:2]]
        for case in json.loads((folder(n) / "verification.yaml").read_text())["scenarios"]:
            inputs = case["inputs"]
            np.testing.assert_array_equal(
                old.evaluate(f"P{n:02d}", inputs[p], inputs[s], inputs["broken_mode"]),
                REFERENCE.evaluate(f"P{n:02d}", inputs[p], inputs[s], inputs["broken_mode"]),
            )


@pytest.mark.parametrize("n", range(1, 13))
def test_retained_independent_mechanisms_dimensional_plots_and_authored_checkpoint(n):
    root = folder(n)
    m = json.loads((root / "module.yaml").read_text())
    v = json.loads((root / "verification.yaml").read_text())
    assert v["reference"]["tolerance_abs"] == v["reference"]["tolerance_rel"] == "1e-10"
    assert (
        not v["reference"]["imports_production"]
        and not v["reference"]["consumes_production_output"]
    )
    assert {"type": "markdown", "title": "Course checkpoint", "source": "assessment.md"} in m[
        "blocks"
    ]
    lesson = (root / "lesson.md").read_text()
    checkpoint = (root / "assessment.md").read_text()
    assert len(lesson.split()) >= 700 and len(checkpoint.split()) >= 300
    for phrase in (f"P{n:02d} evidence task", "Reasoning rubric", "no learner score is stored"):
        assert phrase in checkpoint
    prod = load(root / "experiment.py")
    assert [c["name"] for c in v["scenarios"]] == [
        "baseline",
        "sweep_1",
        "sweep_2",
        "broken",
        "recovery",
    ]
    for case in v["scenarios"]:
        p = case["inputs"]
        result = prod.run(p)
        assert result == prod.run(p)
        expected = REFERENCE.vehicle_foundations_reference(
            n, p[prod.PRIMARY], p[prod.SECONDARY], p["broken_mode"]
        )
        VERIFY.assert_mechanism(result["diagnostics"], expected)
        for name in ("expected-independent", "actual-production"):
            saved = json.loads((root / "evidence" / f"{name}.json").read_text())["cases"][
                case["name"]
            ]
            VERIFY.assert_mechanism(saved, expected)
        for axis, control, index in [
            ("primary", prod.PRIMARY, prod.P_INDEX),
            ("secondary", prod.SECONDARY, prod.S_INDEX),
        ]:
            sweep = result["diagnostics"][axis + "_sweep"]
            reference_values = []
            for value in sweep["x"]:
                q = dict(p)
                q[control] = value
                reference_values.append(
                    REFERENCE.evaluate(f"P{n:02d}", q[prod.PRIMARY], q[prod.SECONDARY], False)[
                        index
                    ]
                )
            np.testing.assert_allclose(sweep["y"], reference_values, atol=1e-10, rtol=1e-10)
        for plot in result["plots"].values():
            for trace in plot["data"]:
                meta = trace["meta"]
                for axis in ("x", "y"):
                    title = plot["layout"][axis + "axis"]["title"]["text"].replace("<br>", " ")
                    assert (
                        meta[axis + "_quantity"] in title and f"({meta[axis + '_unit']})" in title
                    )
                assert len(trace["x"]) == len(trace["y"])
                assert np.isfinite(trace["y"]).all()


@pytest.fixture(scope="module")
def runtime():
    return ExperimentRuntime(CourseCatalog([COURSE]))


@pytest.mark.parametrize("n", range(1, 13))
def test_all_96_runtime_control_corners(n, runtime):
    root = folder(n)
    m = json.loads((root / "module.yaml").read_text())
    controls = m["controls"][:2]
    for a, b, fault in itertools.product(
        *[(c["minimum"], c["maximum"]) for c in controls], (False, True)
    ):
        p = {controls[0]["id"]: a, controls[1]["id"]: b, "broken_mode": fault}
        result = runtime.run("vehicle-dynamics", root.name, p)
        assert result.diagnostics["broken_active"] == fault
        VERIFY.assert_mechanism(
            result.diagnostics, REFERENCE.vehicle_foundations_reference(n, a, b, fault)
        )


def test_p01_path_kinematics_zero_sign_speed_and_grip():
    for steer in (-20, 0, 5, 20):
        for speed in (1, 15, 30, 45):
            for fault in (False, True):
                d = run(1, steering_deg=steer, speed_mps=speed, broken_mode=fault)["diagnostics"]
                k, r, ay = d["signature"][:3]
                assert r == pytest.approx(speed * k, abs=1e-10, rel=1e-10)
                assert ay == pytest.approx(speed * r, abs=1e-10, rel=1e-10)
                x, y = np.array(d["response"]["x"]), np.array(d["response"]["series"][0])
                # A dimensionless circle identity remains well-conditioned near zero curvature.
                np.testing.assert_allclose(
                    (k * x) ** 2 + (1 - k * y) ** 2, 1, atol=1e-10, rtol=1e-10
                )
                assert d["physical"]["grip_feasible"] == (abs(ay) <= 9.81)
                if steer == 0:
                    np.testing.assert_allclose(y, 0, atol=1e-10, rtol=1e-10)
                    np.testing.assert_allclose(
                        x, speed * np.array(d["response"]["time_s"]), atol=1e-10, rtol=1e-10
                    )
    assert physical(1, steering_deg=20, speed_mps=45, broken_mode=True)["grip_feasible"] is False


def test_p02_force_accounting_fault_and_inactive_capacity():
    for speed in (0, 20, 55):
        a = physical(2, tractive_force_n=9000, speed_mps=speed)
        s = a["signature"]
        assert s[0] < s[4] and not a["traction_limited"]
        assert 1320 * s[3] == pytest.approx(s[0] - s[1] - s[2], abs=1e-10, rel=1e-10)
        fault = physical(2, speed_mps=speed, broken_mode=True)
        assert fault["force_balance_residual_n"] == pytest.approx(
            fault["signature"][1] + fault["signature"][2], abs=1e-10, rel=1e-10
        )
    assert physical(2, tractive_force_n=0, speed_mps=0)["signature"][3] < 0


def test_p03_weight_and_pitch_are_independent_checks():
    for accel in (-9, 0, 9):
        for height in (0.25, 0.85):
            d = physical(3, acceleration_mps2=accel, cg_height_m=height)
            f, r = d["signature"][:2]
            assert f + r == pytest.approx(1320 * 9.81, abs=1e-10, rel=1e-10)
            assert (0.53 * 1320 * 9.81 - f) * 2.57 == pytest.approx(
                1320 * accel * height, abs=1e-10, rel=1e-10
            )
            faulty = physical(3, acceleration_mps2=accel, cg_height_m=height, broken_mode=True)
            assert faulty["weight_balance_residual_n"] == pytest.approx(0, abs=1e-10)
            assert abs(faulty["pitch_balance_residual_nm"]) == pytest.approx(
                abs(1320 * accel * height), abs=1e-10, rel=1e-10
            )


@pytest.mark.parametrize("x,y", [(0, 0), (1000, 1000), (3780, 0), (2800, 3500), (-6500, 6500)])
def test_p04_radial_projection_direction_and_capacity(x, y):
    d = physical(4, longitudinal_force_n=x, lateral_force_n=y)
    fx, fy = d["signature"][:2]
    assert math.hypot(fx, fy) == pytest.approx(min(math.hypot(x, y), 3780), abs=1e-10, rel=1e-10)
    assert d["direction_cross_residual"] == pytest.approx(0, abs=1e-10)
    assert fx * x + fy * y >= 0
    f = physical(4, longitudinal_force_n=x, lateral_force_n=y, broken_mode=True)
    assert f["signature"][:2] == [x, y]


@pytest.mark.parametrize("n", [5, 6])
def test_tire_odd_symmetry_initial_slope_sign_capacity_and_benign_zero(n):
    key = "slip_ratio" if n == 5 else "slip_angle_deg"
    sign = 1 if n == 5 else -1
    stiffness = 85000 if n == 5 else 78000
    for load_value in (1000, 3600, 6000):
        for value in (1e-8, 0.01, 0.08):
            plus = physical(n, **{key: value, "normal_load_n": load_value})["signature"]
            minus = physical(n, **{key: -value, "normal_load_n": load_value})["signature"]
            assert plus[1] == pytest.approx(-minus[1], abs=1e-10, rel=1e-10)
            assert 0 < sign * plus[1] <= 1.05 * load_value
        tiny = physical(n, **{key: 1e-8, "normal_load_n": load_value})["signature"]
        assert tiny[1] / tiny[0] == pytest.approx(sign * stiffness, rel=1e-10, abs=1e-10)
        zero = physical(n, **{key: 0, "normal_load_n": load_value})
        bad = physical(n, **{key: 0, "normal_load_n": load_value, "broken_mode": True})
        assert zero["signature"] == bad["signature"]
    assert physical(n, broken_mode=True)["signature"][-1] == 1


def test_p07_original_regression_balance_and_separate_validity(tmp_path):
    path = folder(7) / "experiment.py"
    old_path = tmp_path / "old.py"
    old_path.write_bytes(original(path.relative_to(ROOT)))
    p = {"steering_deg": 3, "speed_mps": 18, "broken_mode": False}
    old = load(old_path).run(p)["diagnostics"]["signature"]
    beta, yaw = old[:2]
    front = 90000 * (math.radians(3) - beta - 1.15 * yaw / 18)
    rear = 100000 * (-beta + 1.42 * yaw / 18)
    assert abs(front + rear - 1320 * 18 * yaw) > 59000
    assert abs(1.15 * front - 1.42 * rear) > 17000
    for steer, speed in itertools.product((-8, 0, 3, 8), (3, 18, 40)):
        d = physical(7, steering_deg=steer, speed_mps=speed)
        assert d["front_force_n"] + d["rear_force_n"] == pytest.approx(
            1320 * speed * d["signature"][1], abs=1e-10, rel=1e-10
        )
        assert 1.15 * d["front_force_n"] - 1.42 * d["rear_force_n"] == pytest.approx(0, abs=1e-10)
    d = physical(7, broken_mode=True)
    assert d["force_balance_residual_n"] == pytest.approx(
        front + rear - 1320 * 18 * yaw, abs=1e-10, rel=1e-10
    )
    # High excitation can close the equations while failing their linearization assumption.
    assert not physical(7, steering_deg=8, speed_mps=40)["small_angle_valid"]


def test_p08_neutral_critical_boundary_and_honest_plot_branches():
    neutral = dict(
        front_cornering_stiffness_n_rad=90000, rear_cornering_stiffness_n_rad=90000 * 1.15 / 1.42
    )
    for fault in (False, True):
        d = run(8, **neutral, broken_mode=fault)
        VERIFY.assert_mechanism(
            d["diagnostics"],
            REFERENCE.vehicle_foundations_reference(
                8, 90000, neutral["rear_cornering_stiffness_n_rad"], fault
            ),
        )
        assert not d["diagnostics"]["physical"]["critical_speed_available"]
        assert (
            next(m["value"] for m in d["metrics"] if m["label"] == "Critical speed")
            == "Unavailable"
        )
    result = run(8, front_cornering_stiffness_n_rad=140000, rear_cornering_stiffness_n_rad=45000)
    s = result["diagnostics"]["signature"]
    assert s[0] < 0 and s[2] > 0
    assert 2.57 + s[0] * s[2] ** 2 == pytest.approx(0, abs=1e-10)
    for trace in result["plots"]["response"]["data"]:
        stable = trace["meta"]["steady_branch_stable"]
        assert all((v < s[2]) == stable for v in trace["x"])
        if not stable:
            assert trace["line"]["dash"] == "dash" and "unstable" in trace["name"]
    assert not physical(8)["critical_speed_available"]


def test_p09_virtual_work_and_frequency_scaling():
    a = physical(9, motion_ratio=0.6)["signature"]
    b = physical(9, motion_ratio=0.9)["signature"]
    assert b[0] / a[0] == pytest.approx(2.25, abs=1e-10, rel=1e-10)
    assert b[1] / a[1] == pytest.approx(1.5, abs=1e-10, rel=1e-10)
    assert b[0] * b[2] == pytest.approx(2943, abs=1e-10, rel=1e-10)
    assert (
        physical(9, motion_ratio=1)["signature"]
        == physical(9, motion_ratio=1, broken_mode=True)["signature"]
    )


@pytest.mark.parametrize("damping", [400, 3200, 2 * math.sqrt(300 * 35000), 8000])
@pytest.mark.parametrize("fault", [False, True])
def test_p10_full_state_transition_ode_energy_and_regimes(damping, fault):
    r = run(10, damping_n_s_m=damping, spring_rate_n_m=35000, broken_mode=fault)
    d = r["diagnostics"]
    VERIFY.assert_mechanism(d, REFERENCE.vehicle_foundations_reference(10, damping, 35000, fault))
    response = d["response"]
    x = np.array(response["series"][0])
    v = np.array(response["velocity_m_s"])
    acceleration = np.array(response["acceleration_m_s2"])
    c = -damping if fault else damping
    np.testing.assert_allclose(
        300 * acceleration + c * v + 35000 * (x - 0.01), 0, atol=1e-10, rtol=1e-10
    )
    assert x[0] == pytest.approx(0, abs=1e-10) and v[0] == pytest.approx(0, abs=1e-10)
    e = np.array(response["energy_j"])
    power = np.array(response["energy_rate_w"])
    np.testing.assert_allclose(
        e, 0.5 * 300 * v * v + 0.5 * 35000 * (x - 0.01) ** 2, atol=1e-10, rtol=1e-10
    )
    np.testing.assert_allclose(power, -c * v * v, atol=1e-10, rtol=1e-10)
    assert np.all(np.diff(e) >= -1e-10) if fault else np.all(np.diff(e) <= 1e-10)
    time = next(m["value"] for m in r["metrics"] if m["id"] == "physical_2")
    assert (time == "Unavailable") == fault
    assert (
        response["x"]
        == run(10, damping_n_s_m=damping, broken_mode=not fault)["diagnostics"]["response"]["x"]
    )


def test_p11_moment_transfer_and_opposite_share_trends():
    d = physical(11)
    s = d["signature"]
    assert (s[1] + s[2]) * 1.53 == pytest.approx(4620, abs=1e-10, rel=1e-10)
    front = physical(11, front_roll_stiffness_n_m_rad=40000)["signature"]
    rear = physical(11, rear_roll_stiffness_n_m_rad=40000)["signature"]
    assert front[0] < s[0] and rear[0] < s[0]
    assert front[3] > s[3] > rear[3]
    assert physical(11, broken_mode=True)["signature"][4] == pytest.approx(
        26000 * 4620 / 32000, abs=1e-10, rel=1e-10
    )


def test_p12_angle_units_parity_zero_and_power():
    a = physical(12, camber_deg=-2, toe_deg=0.1)["signature"]
    b = physical(12, camber_deg=2, toe_deg=-0.1)["signature"]
    assert a[2] == -b[2] and a[3:5] == b[3:5]
    assert a[4] == pytest.approx(20 * a[3], abs=1e-10, rel=1e-10)
    bad = physical(12, broken_mode=True)["signature"]
    assert bad[2] / a[2] == pytest.approx(180 / math.pi, abs=1e-10, rel=1e-10)
    assert (
        physical(12, camber_deg=0, toe_deg=0)["signature"]
        == physical(12, camber_deg=0, toe_deg=0, broken_mode=True)["signature"]
    )
