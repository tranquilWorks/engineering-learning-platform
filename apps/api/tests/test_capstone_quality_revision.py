"""Physical and preservation checks for the twelve-lesson semantic repair."""

from __future__ import annotations

import ast
import importlib.util
import json
import subprocess
from functools import lru_cache
from pathlib import Path

import numpy as np
import pytest
import yaml

ROOT = Path(__file__).resolve().parents[3]
BASELINE = "4e8e39fb3fc05eef8b4ca5607bec4d0bc9320891"
SELECTED = {
    "controls-gnc": (66, 67, 68),
    "robotics-autonomy": (68, 69),
    "vehicle-dynamics": tuple(range(61, 68)),
}
IDENTITIES = [(course, number) for course, numbers in SELECTED.items() for number in numbers]


def folder(course, number):
    return next((ROOT / "courses" / course / "modules").glob(f"{number}-*"))


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@lru_cache
def model(course, number):
    return load(folder(course, number) / "experiment.py", f"revision_{course}_{number}")


def defaults(course, number):
    manifest = yaml.safe_load((folder(course, number) / "module.yaml").read_text())
    return {c["id"]: c["default"] for c in manifest["controls"]}


def result(course, number, **overrides):
    return model(course, number).run(defaults(course, number) | overrides)


def test_exact_twelve_payload_scope_and_preserved_source_pins():
    changed = subprocess.check_output(
        [
            "git",
            "diff",
            "--name-only",
            BASELINE,
            "b107ac198543e8dfb563c6aae4175cc87da6210d",
            "--",
            "courses",
            ".gitmodules",
        ],
        cwd=ROOT,
        text=True,
    ).splitlines()
    prefixes = [str(folder(c, n).relative_to(ROOT)) + "/" for c, n in IDENTITIES]
    references = {f"courses/{c}/expansion_reference_cases.py" for c in SELECTED}
    maps = {f"courses/{c}/expansion-map.yaml" for c in SELECTED}
    assert changed
    assert all(
        p in references | maps or any(p.startswith(prefix) for prefix in prefixes) for p in changed
    )
    assert not subprocess.check_output(
        ["git", "diff", BASELINE, "--", ".gitmodules", "courses/*-learning"], cwd=ROOT
    )


@pytest.mark.parametrize("course", SELECTED)
def test_unaffected_reference_functions_origins_and_all_five_outputs_unchanged(course, tmp_path):
    path = ROOT / "courses" / course / "expansion_reference_cases.py"
    old = subprocess.check_output(
        ["git", "show", f"{BASELINE}:{path.relative_to(ROOT)}"], cwd=ROOT, text=True
    )
    baseline_path = tmp_path / "baseline.py"
    baseline_path.write_text(old)
    baseline = load(baseline_path, "historical_reference")
    # This guard audits PR53, while the current successor has its own exact-baseline guard.
    merged_source = subprocess.check_output(
        ["git", "show", f"b107ac198543e8dfb563c6aae4175cc87da6210d:{path.relative_to(ROOT)}"],
        cwd=ROOT,
        text=True,
    )
    merged_path = tmp_path / "merged.py"
    merged_path.write_text(merged_source)
    revised = load(merged_path, "revised_reference")

    def definitions(text):
        return {
            n.name: ast.get_source_segment(text, n)
            for n in ast.parse(text).body
            if isinstance(n, ast.FunctionDef)
        }

    before, after = definitions(old), definitions(merged_source)
    mapping = yaml.safe_load((path.parent / "expansion-map.yaml").read_text())
    for row in mapping["implemented_native_modules"]:
        number = int(row["id"][1:])
        if number in SELECTED[course]:
            continue
        assert before[f"_p{number}"] == after[f"_p{number}"]
        assert baseline.origin(number) == revised.origin(number)
        design_path = (path.parent / row["folder"] / "design.yaml").relative_to(ROOT)
        design = yaml.safe_load(
            subprocess.check_output(
                ["git", "show", f"b107ac198543e8dfb563c6aae4175cc87da6210d:{design_path}"],
                cwd=ROOT,
                text=True,
            )
        )
        for parameters in design["scenarios"].values():
            np.testing.assert_array_equal(
                baseline.reference_signature(number, parameters),
                revised.reference_signature(number, parameters),
            )


@pytest.mark.parametrize("course,number", IDENTITIES)
def test_signature_dimensions_scenarios_and_visible_verdicts(course, number):
    root = folder(course, number)
    design = yaml.safe_load((root / "design.yaml").read_text())
    manifest = yaml.safe_load((root / "module.yaml").read_text())
    assert design["scenarios"]["baseline"] == defaults(course, number)
    response = result(course, number)
    assert [m["unit"] for m in response["metrics"]] == [s["unit"] for s in design["signature"]]
    if "requirements" in response["diagnostics"]:
        assert any(b.get("table") == "requirements" for b in manifest["blocks"])
        rows = response["tables"]["requirements"]["rows"]
        assert len(rows) == len(response["diagnostics"]["requirements"])
        for key, r in response["diagnostics"]["requirements"].items():
            predicate = (
                r["value"] <= r["threshold"] + 1e-10
                if r["operator"] == "<="
                else r["value"] >= r["threshold"] - 1e-10
            )
            assert r["passed"] == predicate
            assert next(row for row in rows if row["Requirement"] == key)["Verdict"] == (
                "pass" if predicate else "fail"
            )
    for filename in ("expected-independent.json", "actual-production.json"):
        evidence = json.loads((root / "evidence" / filename).read_text())
        assert evidence["signature_fields"] == design["signature"]
        for name, parameters in design["scenarios"].items():
            assert evidence["cases"][name]["parameters"] == parameters


def test_identification_feedback_estimator_execute_the_plant_recurrence():
    healthy = result("controls-gnc", 66)["diagnostics"]
    broken = result("controls-gnc", 66, broken_mode=True)["diagnostics"]
    assert healthy["calibration_rank"] == 2 and broken["calibration_rank"] == 1
    np.testing.assert_allclose(
        healthy["identified_coefficients"], [np.exp(-0.02), 1 - np.exp(-0.02)], atol=1e-12
    )
    history = np.asarray(healthy["state_estimate_covariance_command_nees"])
    for i, stress in enumerate((-0.2, 0.0, 0.2)):
        decay = np.exp(-(1 + stress) * 0.02)
        gain = (1 - stress / 2) / (1 + stress) * (1 - decay)
        previous = np.r_[0.0, history[i, :-1, 0]]
        np.testing.assert_allclose(
            history[i, :, 0], decay * previous + gain * history[i, :, 3], atol=1e-12
        )
    np.testing.assert_allclose(
        history[:, :, 4], (history[:, :, 0] - history[:, :, 1]) ** 2 / history[:, :, 2]
    )
    assert np.max(abs(history[:, :, 3])) <= 3
    rank, _, zero_stress = model("controls-gnc", 66)._simulate(0.0, 0.1, False)
    assert rank == 2
    np.testing.assert_array_equal(zero_stress[0], zero_stress[2])
    changed = result("controls-gnc", 66, broken_mode=True, measurement_noise=0.5)["diagnostics"]
    assert changed["signature"] != broken["signature"]  # faults do not overwrite controls


def test_survey_uses_exact_arcs_fixes_hold_and_applied_turns():
    module = model("controls-gnc", 67)
    np.testing.assert_allclose(
        module._arc(np.array([1.0, 2.0, 0.0]), 2.0, 0.0, 0.05), [1.1, 2.0, 0.0]
    )
    history = np.asarray(result("controls-gnc", 67)["diagnostics"]["survey"])
    assert np.any(history[:, 10] == 1)
    assert np.all(history[history[:, 6] > 3, 7] == 0)
    assert max(abs(history[:, 8])) <= 12 + 1e-10
    assert np.any(history[history[:, 6] == 0, 7] > 0)
    for k in range(1, len(history)):
        expected = module._arc(history[k - 1, :3], history[k, 7], np.deg2rad(history[k, 8]), 0.05)
        np.testing.assert_allclose(history[k, :3], expected, atol=1e-12)
    assert not np.any(module._survey(0, 12, False)[:, 10])


def test_loop_source_time_and_no_fault_limit():
    module = model("controls-gnc", 68)
    h, events, drops = module._loop(12, 0.05, False)
    assert drops == 25
    accepted = events[events[:, 3] == 1, 0]
    assert np.all(np.diff(accepted) > 0)
    assert np.any(events[:, 3] == 0)  # late old-source arrival really happened
    assert np.all(h[h[:, 5] > 0, 2] == 0)
    np.testing.assert_allclose(
        h[:, 0], np.exp(-0.02) * np.r_[0.0, h[:-1, 0]] + (1 - np.exp(-0.02)) * h[:, 2], atol=1e-12
    )
    clean, clean_events, drops = module._loop(0, 0, False)
    assert drops == 0 and len(clean_events) == 500
    assert np.all(clean[:, 3:6] == 0)
    assert module._model({"one_way_latency_ms": 0, "packet_drop_fraction": 0}, False)[
        "signature"
    ] == [0.0, 0.0, 1.0]
    fault, _, _ = module._loop(12, 0.05, True)
    assert np.count_nonzero((fault[:, 5] > 0) & (abs(fault[:, 2]) > 0)) > 0


def test_mobile_robot_perceives_then_replans_and_replays_real_events():
    module = model("robotics-autonomy", 68)
    r = module._mission(10, 0.3, False)
    assert r == module._mission(10, 0.3, False)
    assert r["collisions"] == r["source_order_errors"] == r["stale_moves"] == 0
    assert r["recovered_sources"] and r["goal_distance_m"] == 0
    seen = [row for row in r["observations"] if row[2] and row[3]]
    assert seen and min(row[0] for row in seen) > 0
    assert any(row[0] == 3 and row[1] == 35 and row[3] == 0 for row in r["observations"])
    for row in r["segments"]:
        time, x, y, nx, ny, _, separation, _ = row
        tau = np.linspace(0, 1, 201)
        sampled = np.hypot(x + (nx - x) * tau - 6, y + (ny - y) * tau + 2 - 0.3 * (time + tau))
        assert separation <= min(sampled) + 1e-12
        assert min(sampled) - separation < 0.002
        assert separation >= 0.85 - 1e-10
    bad = module._mission(10, 0.3, True)
    assert bad["collisions"] > 0 and bad["source_order_errors"] > 0 and bad["stale_moves"] > 0


def test_contact_accounts_for_first_spring_work_and_actual_timing_fault():
    module = model("robotics-autonomy", 69)
    zero = np.asarray(module._contact(False, initial_tank=0.0))
    assert np.all(zero[:, 1] == 0) and np.all(zero[:, 2] == 0)
    h = np.asarray(module._contact(False))
    energies = h[:, 1] ** 2 / (2 * 600)
    debit = np.maximum(np.diff(np.r_[0.0, energies]), 0)
    np.testing.assert_allclose(h[:, 2], 0.18 - np.cumsum(debit), atol=1e-12)
    assert np.any(h[:, 5] > 0.04)
    assert np.all(h[h[:, 5] > 0.04 + 1e-12, 3] == 0)
    assert h[-1, 4] >= 96 and abs(h[-1, 1] - 10) < 3
    assert np.min(module._contact(True), axis=0)[2] < 0
    low_friction = result("robotics-autonomy", 69, contact_friction_coefficient=0.1)["diagnostics"]
    assert not low_friction["requirements"]["R69-GRASP"]["passed"]


def test_track_circle_scaling_and_sampling_limits():
    module = model("vehicle-dynamics", 61)
    circle = module._calc(60, 181, False, aspect_ratio=1.0)[0]
    assert circle[0] == pytest.approx(2 * 180 * 60 * np.sin(np.pi / 180), abs=1e-10)
    assert circle[1] == pytest.approx(1 / 60)
    a = module._calc(60, 181, False)[0]
    b = module._calc(40, 181, False)[0]
    assert a[0] / b[0] == pytest.approx(1.5)
    assert a[1] / b[1] == pytest.approx(2 / 3)
    assert module._calc(60, 301, False)[0][-1] < a[-1]


def test_force_envelope_demand_and_power_are_the_same_physical_quantities():
    module = model("vehicle-dynamics", 62)
    zero = module._state(0, 1.2, False)
    np.testing.assert_allclose(zero[:3], [1.2 * 9.81] * 3)
    assert zero[3:] == [0.0, 0.0, 0.0]
    for broken in (False, True):
        r = result("vehicle-dynamics", 62, broken_mode=broken)
        d = r["diagnostics"]
        fx, fy = d["demand_force_n"]
        assert d["signature"][-1] == pytest.approx(
            max(0, np.hypot(fx, fy) / d["tire_capacity_n"] - 1)
        )
        point = r["plots"]["mechanism"]["data"][-1]
        assert point["x"][0] == pytest.approx((fx - d["signature"][4]) / 1450)
        assert (d["power_excess_w"] > 0) == broken


def test_offset_line_uses_local_time_and_circle_geometry():
    module = model("vehicle-dynamics", 63)
    ds, k = module._geometry(256, 100, 100)
    lengths, curve, speed, time = module._line(3, ds, k)
    assert sum(lengths) == pytest.approx(2 * np.pi * 97)
    np.testing.assert_allclose(curve, 1 / 97)
    assert time == pytest.approx(2 * np.pi * np.sqrt(97 / 11.5))
    ds, k = module._geometry()
    lengths, _, speeds, time = module._line(2.4, ds, k)
    assert time == pytest.approx(sum(lengths / speeds))
    assert abs(time - sum(lengths) / np.mean(speeds)) > 0.5
    assert module._calc(0, 0.02, False)[0][0] == 0
    assert module._calc(3, 0.06, False)[0][0] < module._calc(3, 0.02, False)[0][0]


def test_lap_budget_changes_motion_and_preserves_energy_force_and_seam():
    module = model("vehicle-dynamics", 64)
    high = module._solve(1.15, 3, False)
    low = module._solve(1.15, 0.8, False)
    assert high["signature"][0] < low["signature"][0]
    for run in (high, low):
        w = run["speed"] ** 2
        wheel_work = (
            0.5 * 1450 * (np.roll(w, -1) - w) + (0.441 * w + 0.012 * 1450 * 9.81) * run["ds"]
        )
        np.testing.assert_allclose(run["wheel_work_j"], wheel_work)
        assert sum(np.maximum(wheel_work, 0)) / 1e6 == pytest.approx(run["signature"][3])
        assert max(run["utilization"]) <= 1 + 1e-10
        assert run["signature"][-1] < 1e-5
        assert abs(run["segment_force_n"][-1]) <= 0.5 * 1.15 * 1450 * 9.81 + 1e-6
    zero = module._solve(1.15, 0, False)
    assert not zero["budget_feasible"] and zero["signature"][0] == 0
    assert module._solve(1.15, 3, True)["signature"][-1] > 1000
    refined = module._solve(1.15, 3, False, count=256)
    assert abs(refined["signature"][0] - high["signature"][0]) / high["signature"][0] < 0.02


def test_factorial_validation_points_are_unused_and_detect_aliasing():
    healthy = result("vehicle-dynamics", 65)["diagnostics"]
    broken = result("vehicle-dynamics", 65, broken_mode=True)["diagnostics"]
    corners = {(-1, -1), (-1, 1), (1, -1), (1, 1)}
    assert not corners & {tuple(p) for p in healthy["held_out_points"]}
    assert healthy["signature"][5] == 4 and broken["signature"][5] == 2
    assert healthy["signature"][-1] < 1e-10 < broken["signature"][-1]
    assert broken["signature"][-1] == pytest.approx(1.256483187313)


def test_telemetry_chain_provenance_split_covariance_and_recovery():
    r = result("vehicle-dynamics", 66)["diagnostics"]
    bad = result("vehicle-dynamics", 66, broken_mode=True)["diagnostics"]
    assert r["record_count"] == 309 and r["samples"] == 101
    assert r["training_stop"] == r["held_out_start"] < r["samples"]
    assert r["synthetic_force_channel"] is True
    np.testing.assert_allclose(r["mass_drag_estimate"], [1450, 0.45], atol=0.05)
    covariance = np.asarray(r["parameter_covariance"])
    np.testing.assert_allclose(covariance, covariance.T)
    assert min(np.linalg.eigvalsh(covariance)) >= 0
    assert bad["requirements"]["TV-02"]["value"] > 0.02
    assert bad["requirements"]["TV-03"]["value"] == pytest.approx(0.5)
    assert bad["requirements"]["TV-08"]["value"] == 2
    assert all(item["passed"] for item in r["requirements"].values())
    # Exact deterministic recovery, independently rerunning the complete chain.
    assert result("vehicle-dynamics", 66)["diagnostics"] == r


def test_integrated_vehicle_load_work_gear_uncertainty_and_real_failure():
    module = model("vehicle-dynamics", 67)
    d = result("vehicle-dynamics", 67)["diagnostics"]
    bad = result("vehicle-dynamics", 67, broken_mode=True)["diagnostics"]
    current = d["current"]
    speed = np.asarray(current["speed_m_s"])
    loads = np.asarray(current["physical_loads_n"])
    down = 1.53125 * (1 + 2 * 0.08) * speed**2
    np.testing.assert_allclose(loads.sum(axis=1), 1450 * 9.81 + down, atol=1e-9)
    assert min(current["gears"]) >= 1 and max(current["gears"]) <= 6
    assert max(current["grip_utilization"]) <= 1.000001
    assert d["signature"][3] == pytest.approx(abs(np.diff(d["friction_lap_endpoints_s"])[0]))
    assert bad["requirements"]["DT-06"]["value"] > 0.1
    assert not bad["requirements"]["DT-06"]["passed"]
    assert bad["requirements"]["DT-11"]["passed"]  # clean replay never validates current fault
    assert bad["signature"][0] < 11
    assert module._model(0, 0, False)["signature"][3:5] == [0.0, 0.0]
    refined = module._lap(0.08, count=192)
    assert abs(refined["lap_s"] - current["lap_s"]) / current["lap_s"] < 0.03


@pytest.mark.parametrize("course,number", IDENTITIES)
def test_all_control_corners_have_finite_computed_results(course, number):
    manifest = yaml.safe_load((folder(course, number) / "module.yaml").read_text())
    first, second, _ = manifest["controls"]
    for a in (first["minimum"], first["default"], first["maximum"]):
        for b in (second["minimum"], second["default"], second["maximum"]):
            for broken in (False, True):
                r = result(
                    course, number, **{first["id"]: a, second["id"]: b, "broken_mode": broken}
                )
                assert np.all(np.isfinite(r["diagnostics"]["signature"]))
                if "requirements" in r["diagnostics"]:
                    assert all(
                        np.isfinite(v["value"]) for v in r["diagnostics"]["requirements"].values()
                    )
