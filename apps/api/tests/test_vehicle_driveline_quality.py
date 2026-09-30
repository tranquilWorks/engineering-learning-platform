"""Independent physical and preservation checks for Vehicle P13–P16."""

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
BASELINE = "1a0041bd24de1168c03ff2bf2a656a6061cac0e3"
COURSE = ROOT / "courses/vehicle-dynamics"


def load(path):
    spec = importlib.util.spec_from_file_location("driveline_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


REFERENCE = load(COURSE / "reference_cases.py")
VERIFY = load(ROOT / "scripts/verify-vehicle-driveline-quality.py")


def folder(n):
    return next((COURSE / "modules").glob(f"{n:02d}-*"))


def original(path):
    return subprocess.check_output(["git", "show", f"{BASELINE}:{path}"], cwd=ROOT)


def run(n, **changes):
    manifest = json.loads((folder(n) / "module.yaml").read_text())
    inputs = {c["id"]: c["default"] for c in manifest["controls"]}
    inputs.update(changes)
    return load(folder(n) / "experiment.py").run(inputs)


def physical(n, **changes):
    return run(n, **changes)["diagnostics"]["physical"]


def test_exact_scope_controls_source_pins_and_historical_coverage():
    contract = yaml.safe_load((ROOT / "contracts/active-batch.yaml").read_text())
    assert contract["batch"]["id"] == "ELP-VEHICLE-DRIVELINE-QUALITY-04"
    assert contract["sources"]["baseline_commit"] == BASELINE
    assert (
        subprocess.check_output(
            ["git", "rev-parse", BASELINE + "^{tree}"], cwd=ROOT, text=True
        ).strip()
        == contract["sources"]["baseline_tree"]
    )
    allowed = [f"courses/vehicle-dynamics/modules/{n}-*/**" for n in range(13, 17)] + [
        "courses/vehicle-dynamics/reference_cases.py",
        "courses/vehicle-dynamics/coverage.yaml",
    ]
    changed = subprocess.check_output(
        ["git", "diff", "--name-only", BASELINE, "--", "courses", ".gitmodules"],
        cwd=ROOT,
        text=True,
    ).splitlines()
    assert all(any(fnmatch.fnmatch(p, rule) for rule in allowed) for p in changed)
    tracked = subprocess.check_output(
        [
            "git",
            "ls-tree",
            "-r",
            "--format=%(objectmode) %(path)",
            BASELINE,
            "--",
            "courses",
            ".gitmodules",
        ],
        cwd=ROOT,
        text=True,
    ).splitlines()
    for row in tracked:
        mode, path = row.split(" ", 1)
        if mode == "160000" or any(fnmatch.fnmatch(path, rule) for rule in allowed):
            continue
        assert (ROOT / path).is_file(), path
        assert (ROOT / path).read_bytes() == original(path), path
    before = json.loads(original("courses/vehicle-dynamics/coverage.yaml"))
    after = json.loads((COURSE / "coverage.yaml").read_text())
    for n, (a, b) in enumerate(zip(before["items"], after["items"], strict=True), 1):
        if 13 <= n <= 16:
            a.pop("target_content_digest")
            b.pop("target_content_digest")
        assert a == b
    for n in range(13, 17):
        path = folder(n) / "module.yaml"
        old, new = json.loads(original(path.relative_to(ROOT))), json.loads(path.read_text())
        assert (old["id"], old["number"]) == (new["id"], new["number"])
        assert new["runtime"] == old["runtime"] and new["runtime"]["timeout_seconds"] == 3
        for i, (a, b) in enumerate(zip(old["controls"], new["controls"], strict=True)):
            a = {k: v for k, v in a.items() if k not in ("label", "description")}
            b = {k: v for k, v in b.items() if k not in ("label", "description")}
            if n == 14 and i < 2:
                assert a["step"] == 0.05 and b["step"] == 0.001
                a["step"] = 0.001
            assert a == b
    catalog = CourseCatalog([ROOT / "courses"]).summaries()
    assert len(catalog) == 6 and sum(len(c.modules) for c in catalog) == 290


def test_all_unselected_reference_definitions_and_outputs_preserved(tmp_path):
    path = "courses/vehicle-dynamics/reference_cases.py"
    before, after = original(path).decode(), (ROOT / path).read_text()

    def definitions(source):
        return {
            node.name: ast.get_source_segment(source, node)
            for node in ast.parse(source).body
            if isinstance(node, ast.FunctionDef)
        }

    old_defs, new_defs = definitions(before), definitions(after)
    for name in old_defs.keys() - {f"_p{n}" for n in range(13, 17)}:
        assert old_defs[name] == new_defs[name], name
    previous = tmp_path / "previous_reference.py"
    previous.write_text(before)
    old = load(previous)
    for n in list(range(1, 13)) + list(range(17, 25)):
        manifest = json.loads((folder(n) / "module.yaml").read_text())
        p, s = [c["id"] for c in manifest["controls"][:2]]
        for case in json.loads((folder(n) / "verification.yaml").read_text())["scenarios"]:
            inputs = case["inputs"]
            np.testing.assert_array_equal(
                old.evaluate(f"P{n:02d}", inputs[p], inputs[s], inputs["broken_mode"]),
                REFERENCE.evaluate(f"P{n:02d}", inputs[p], inputs[s], inputs["broken_mode"]),
            )


@pytest.mark.parametrize("n", range(13, 17))
def test_retained_full_mechanisms_dimensions_sweeps_and_checkpoint(n):
    root = folder(n)
    manifest = json.loads((root / "module.yaml").read_text())
    verification = json.loads((root / "verification.yaml").read_text())
    prod = load(root / "experiment.py")
    assert (
        verification["reference"]["tolerance_abs"]
        == verification["reference"]["tolerance_rel"]
        == "1e-10"
    )
    assert (
        not verification["reference"]["imports_production"]
        and not verification["reference"]["consumes_production_output"]
    )
    assert {
        "type": "markdown",
        "title": "Course checkpoint",
        "source": "assessment.md",
    } in manifest["blocks"]
    assert len((root / "lesson.md").read_text().split()) >= 700
    checkpoint = (root / "assessment.md").read_text()
    assert len(checkpoint.split()) >= 300
    for phrase in (f"P{n} evidence task", "Reasoning rubric", "no learner score is stored"):
        assert phrase in checkpoint
    assert [c["name"] for c in verification["scenarios"]] == [
        "baseline",
        "sweep_1",
        "sweep_2",
        "broken",
        "recovery",
    ]
    for case in verification["scenarios"]:
        inputs = case["inputs"]
        result = prod.run(inputs)
        assert result == prod.run(inputs)
        expected = REFERENCE.vehicle_driveline_reference(
            n, inputs[prod.PRIMARY], inputs[prod.SECONDARY], inputs["broken_mode"]
        )
        assert set(result["diagnostics"]["physical"]) == set(expected["physical"])
        VERIFY.assert_mechanism(result["diagnostics"], expected)
        for name in ("expected-independent", "actual-production"):
            saved = json.loads((root / "evidence" / f"{name}.json").read_text())["cases"][
                case["name"]
            ]
            VERIFY.assert_mechanism(saved, expected)
        for axis, control, specification in [
            ("primary", prod.PRIMARY, prod.P_SWEEP),
            ("secondary", prod.SECONDARY, prod.S_SWEEP),
        ]:
            sweep = result["diagnostics"][axis + "_sweep"]
            states = []
            for value in sweep["x"]:
                q = dict(inputs)
                q[control] = value
                state = REFERENCE._vehicle_driveline_reference_state(
                    n, q[prod.PRIMARY], q[prod.SECONDARY], False
                )
                if n == 14:
                    assert state["decision_available"]
                states.append(state)
            for values, (_, field) in zip(sweep["series"], specification[0], strict=True):
                np.testing.assert_allclose(
                    values, [s[field] for s in states], atol=1e-10, rtol=1e-10
                )
        assert set(result["plots"]) == {
            "response",
            "primary_sweep",
            "secondary_sweep",
            "broken_recovery",
        }
        for plot in result["plots"].values():
            for trace in plot["data"]:
                for axis in ("x", "y"):
                    title = plot["layout"][axis + "axis"]["title"]["text"].replace("<br>", " ")
                    assert trace["meta"][axis + "_quantity"] in title
                    assert f"({trace['meta'][axis + '_unit']})" in title
                assert len(trace["x"]) == len(trace["y"]) > 1
                assert np.isfinite(trace["x"]).all() and np.isfinite(trace["y"]).all()


@pytest.fixture(scope="module")
def runtime():
    return ExperimentRuntime(CourseCatalog([COURSE]))


@pytest.mark.parametrize("n", range(13, 17))
def test_all_32_runtime_control_corners(n, runtime):
    manifest = json.loads((folder(n) / "module.yaml").read_text())
    controls = manifest["controls"][:2]
    for a, b, fault in itertools.product(
        *[(c["minimum"], c["maximum"]) for c in controls], (False, True)
    ):
        inputs = {controls[0]["id"]: a, controls[1]["id"]: b, "broken_mode": fault}
        result = runtime.run("vehicle-dynamics", folder(n).name, inputs)
        assert result.diagnostics["broken_active"] == fault
        VERIFY.assert_mechanism(
            result.diagnostics, REFERENCE.vehicle_driveline_reference(n, a, b, fault)
        )


@pytest.mark.parametrize("torque,gear", [(80, 0.8), (250, 3), (320, 4.2)])
def test_p13_delivered_power_curtailment_and_executed_loss_fault(torque, gear):
    good = physical(13, engine_torque_n_m=torque, gear_ratio=gear)
    bad = physical(13, engine_torque_n_m=torque, gear_ratio=gear, broken_mode=True)
    for state in (good, bad):
        assert state["applied_wheel_force_n"] <= 1320 * 9.81
        assert state["curtailed_request_w"] >= 0
        assert state["delivered_engine_torque_nm"] <= torque
        assert state["requested_engine_power_w"] == pytest.approx(
            state["delivered_engine_power_w"] + state["curtailed_request_w"]
        )
        assert state["wheel_power_w"] == pytest.approx(state["applied_wheel_force_n"] * 20)
    assert abs(good["power_residual_w"]) <= 1e-10
    assert bad["power_residual_w"] == pytest.approx(0.1 * bad["delivered_engine_power_w"])
    assert bad["invalid"] == 1
    if (torque, gear) == (320, 4.2):
        assert good["applied_wheel_force_n"] == bad["applied_wheel_force_n"]
        assert good["curtailed_request_w"] == pytest.approx(62106.6666666667)


@pytest.mark.parametrize(
    "current,nxt,kind",
    [
        (2.188, 1.541, "redline"),
        (2.09, 2.08, "crossover"),
        (2.188, 2.187, "crossover"),
        (2.09, 2.09 - 1e-9, "crossover"),
        (2, 2, "unavailable"),
        (1.4, 2.4, "unavailable"),
    ],
)
def test_p14_crossovers_redline_and_invalid_order(current, nxt, kind):
    result = run(14, current_gear_ratio=current, next_gear_ratio=nxt)
    state = result["diagnostics"]["physical"]
    expected = REFERENCE.vehicle_driveline_reference(14, current, nxt)
    VERIFY.assert_mechanism(result["diagnostics"], expected)
    if kind == "unavailable":
        assert not state["decision_available"] and state["invalid"]
        for metric in result["metrics"]:
            if metric["label"] in (
                "Decision engine speed",
                "Decision road speed",
                "Current-gear force",
                "Next-gear force",
                "Post-shift engine speed",
            ):
                assert metric["value"] == "Unavailable"
    else:
        assert state["decision_available"] and state["post_shift_rpm"] < state["shift_rpm"]
        if kind == "crossover":
            assert state["crossover"] and 2500 < state["shift_rpm"] < 7400
            assert abs(state["force_gap_n"]) < 1e-10
        else:
            assert state["redline_limited"] and state["shift_rpm"] == 7400
            assert state["force_gap_n"] == pytest.approx(-975.945908421696)


def test_p14_lookup_fault_preserves_kinematics_but_not_full_curve():
    good = run(14, current_gear_ratio=2.09, next_gear_ratio=2.08)["diagnostics"]
    bad = run(14, current_gear_ratio=2.09, next_gear_ratio=2.08, broken_mode=True)["diagnostics"]
    assert good["physical"]["crossover"] and bad["physical"]["redline_limited"]
    assert good["response"]["post_shift_rpm"] == bad["response"]["post_shift_rpm"]
    assert bad["physical"]["maximum_lookup_force_error_n"] > 0
    # At 7400 + 2600 RPM, the symmetric torque map happens to agree at one point.
    prod = load(folder(14) / "experiment.py")
    q = 2600 / 7400
    current = 3.0
    nxt = current * q
    np.testing.assert_allclose(
        prod._forces(current, nxt, 7400, False),
        prod._forces(current, nxt, 7400, True),
        atol=1e-10,
        rtol=1e-10,
    )
    assert (
        physical(14, current_gear_ratio=current, next_gear_ratio=nxt, broken_mode=True)[
            "maximum_lookup_force_error_n"
        ]
        > 100
    )


@pytest.mark.parametrize("speed,brake_request", [(5, 1000), (30, 10000), (30, 18000), (55, 18000)])
def test_p15_work_heat_trajectory_and_load_moments(speed, brake_request):
    result = run(15, initial_speed_m_s=speed, requested_brake_force_n=brake_request)
    good = result["diagnostics"]["physical"]
    response = result["diagnostics"]["response"]
    bad = physical(
        15, initial_speed_m_s=speed, requested_brake_force_n=brake_request, broken_mode=True
    )
    energy = 0.5 * 1320 * speed**2
    force = min(brake_request, 1.05 * 1320 * 9.81)
    assert good["stopping_work_j"] == pytest.approx(energy)
    assert abs(good["work_residual_fraction"]) < 1e-10
    assert abs(good["heat_residual_fraction"]) < 1e-10
    assert bad["heat_residual_fraction"] == pytest.approx(0.15)
    assert good["stopping_distance_m"] == bad["stopping_distance_m"]
    assert bad["rotor_delta_t_c"] > good["rotor_delta_t_c"]
    assert good["rear_load_n"] > 0 and good["front_load_n"] + good["rear_load_n"] == pytest.approx(
        1320 * 9.81
    )
    assert (good["front_load_n"] - 0.53 * 1320 * 9.81) * 2.57 == pytest.approx(force * 0.5)
    np.testing.assert_allclose(
        np.array(response["stopping_work_j"]) + response["remaining_kinetic_energy_j"],
        energy,
        atol=1e-10,
        rtol=1e-10,
    )
    np.testing.assert_allclose(
        response["braking_power_w"], force * np.array(response["series"][0]), atol=1e-10, rtol=1e-10
    )
    acceleration = np.diff(response["series"][0]) / np.diff(response["x"])
    np.testing.assert_allclose(acceleration, -force / 1320, atol=1e-10, rtol=1e-10)


def test_p15_force_cap_and_speed_scaling_are_distinct():
    below = physical(15, requested_brake_force_n=13500)
    above = physical(15, requested_brake_force_n=14000)
    maximum = physical(15, requested_brake_force_n=18000)
    assert (
        below["stopping_distance_m"]
        > above["stopping_distance_m"]
        == maximum["stopping_distance_m"]
    )
    slow = physical(15, initial_speed_m_s=20)
    fast = physical(15, initial_speed_m_s=40)
    for key in ("stopping_distance_m", "kinetic_energy_j", "rotor_delta_t_c"):
        assert fast[key] == pytest.approx(4 * slow[key])
    assert fast["stop_time_s"] == pytest.approx(2 * slow["stop_time_s"])


@pytest.mark.parametrize("angle", [0, 8, 18])
def test_p16_speed_powers_allocation_and_actual_fault(angle):
    slow = physical(16, speed_m_s=20, wing_angle_deg=angle)
    fast = physical(16, speed_m_s=40, wing_angle_deg=angle)
    bad = physical(16, speed_m_s=40, wing_angle_deg=angle, broken_mode=True)
    for key in ("dynamic_pressure_pa", "drag_n", "downforce_n", "front_aero_n", "rear_aero_n"):
        assert fast[key] == pytest.approx(4 * slow[key])
    assert fast["drag_power_w"] == pytest.approx(8 * slow["drag_power_w"])
    assert fast["tire_capacity_n"] - 1320 * 9.81 == pytest.approx(
        4 * (slow["tire_capacity_n"] - 1320 * 9.81)
    )
    for state in (fast, bad):
        assert state["front_aero_n"] + state["rear_aero_n"] == pytest.approx(state["downforce_n"])
        assert state["front_normal_n"] + state["rear_normal_n"] == pytest.approx(
            state["tire_capacity_n"]
        )
    assert bad["rear_aero_n"] < 0 < bad["rear_normal_n"]
    assert bad["drag_power_w"] < 0 and bad["invalid"] == 1
    assert bad["tire_capacity_n"] == fast["tire_capacity_n"]


def test_p16_wing_tradeoff_and_default_units():
    low = physical(16, wing_angle_deg=8)
    high = physical(16, wing_angle_deg=18)
    assert high["downforce_n"] - low["downforce_n"] == pytest.approx(441)
    assert high["drag_power_w"] - low["drag_power_w"] == pytest.approx(15288)
    for n in range(13, 17):
        assert math.isfinite(sum(run(n)["diagnostics"]["signature"]))
