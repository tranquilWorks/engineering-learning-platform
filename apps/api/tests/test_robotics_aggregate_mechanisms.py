"""Physical and independent algorithm checks for the aggregate Robotics review."""

import importlib.util
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[3]
COURSE = ROOT / "courses/robotics-autonomy"


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("count,noise", [(5, 0.005), (30, 0.08), (100, 0.5), (17, 0.137)])
@pytest.mark.parametrize("broken", [False, True])
def test_joint_slam_estimates_unknown_map_and_heading(count, noise, broken):
    model = load(next((COURSE / "modules").glob("51-*/experiment.py")))
    ref = load(COURSE / "aggregate_references.py").joint_slam(count, noise, broken)
    out = model._joint_slam(count, noise, broken)
    poses = out["poses"].copy()
    landmarks = out["landmarks"].copy()
    if broken:
        angle = ref["poses"][0, 2] - poses[0, 2]
        R = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        shift = ref["poses"][0, :2] - R @ poses[0, :2]
        poses[:, :2] = poses[:, :2] @ R.T + shift
        poses[:, 2] += angle
        landmarks = landmarks @ R.T + shift
    np.testing.assert_allclose(poses, ref["poses"], atol=3e-6, rtol=3e-6)
    np.testing.assert_allclose(landmarks, ref["landmarks"], atol=3e-6, rtol=3e-6)
    assert abs(out["cost"] - ref["cost"]) < 1e-7
    assert np.all(np.diff(out["iterations"][:, 1]) <= 1e-9)
    assert out["jacobian"].shape[1] == 3 * count + 6
    # Three SE(2) gauge directions must survive only in the unanchored graph.
    x = np.r_[out["poses"].ravel(), out["landmarks"].ravel()]
    directions = np.zeros((len(x), 3))
    for i, p in enumerate(out["poses"]):
        directions[3 * i : 3 * i + 3] = [[1, 0, -p[1]], [0, 1, p[0]], [0, 0, 1]]
    for j, landmark in enumerate(out["landmarks"]):
        directions[3 * count + 2 * j : 3 * count + 2 * j + 2] = [
            [1, 0, -landmark[1]],
            [0, 1, landmark[0]],
        ]
    norms = np.linalg.norm(out["jacobian"] @ directions, axis=0)
    assert np.all(norms < 1e-8) if broken else np.all(norms > 1.0)


def test_joint_slam_jacobian_matches_finite_perturbations():
    model = load(next((COURSE / "modules").glob("51-*/experiment.py")))
    truth, lm, odom, observations, state = model._joint_slam_problem(7, 0.08, False)
    r, J = model._joint_slam_linearize(state, 7, odom, observations, truth[0], 0.08, False)
    for i in range(len(state)):
        h = np.zeros_like(state)
        h[i] = 1e-6
        plus, _ = model._joint_slam_linearize(
            state + h, 7, odom, observations, truth[0], 0.08, False
        )
        minus, _ = model._joint_slam_linearize(
            state - h, 7, odom, observations, truth[0], 0.08, False
        )
        np.testing.assert_allclose(
            (plus - minus) / 2e-6, J[:, i].toarray().ravel(), atol=2e-7, rtol=2e-7
        )


@pytest.mark.parametrize("number", [62, 69])
@pytest.mark.parametrize(
    "noise,yaw,friction,broken",
    [
        (1.2, 0.8, 0.5, False),
        (5.0, 0.8, 0.5, False),
        (1.37, 1.73, 0.337, False),
        (1.2, 5.0, 0.5, False),
        (1.2, 0.8, 0.1, False),
        (1.2, 0.8, 0.5, True),
    ],
)
def test_executed_manipulation_independent_dynamics(number, noise, yaw, friction, broken):
    model = load(next((COURSE / "modules").glob(f"{number}-*/experiment.py")))
    reference = load(COURSE / "aggregate_references.py").manipulation(noise, yaw, friction, broken)
    actual = model._manipulation(noise, yaw, friction, broken)
    assert actual["success"] == reference["success"]
    assert actual["failure"] == reference["failure"]
    np.testing.assert_allclose(actual["events"], reference["events"], rtol=0, atol=4e-5)
    np.testing.assert_allclose(actual["history"], reference["history"], rtol=0, atol=4e-5)
    h = actual["history"]
    assert np.isfinite(h).all()
    assert actual["max_torque_nm"] <= 25
    assert np.all((h[:, 10] >= 0) & (h[:, 10] <= 10))
    if actual["success"]:
        assert list(actual["events"][:, 2]) == [1, 2, 3, 4, 5, 6, 7, 8, 10]
        assert actual["placement_error_m"] < 0.02
        assert h[-1, 11] == 0
        assert np.linalg.norm(h[-1, 6:8] - h[-1, 8:10]) > 0.1
    else:
        assert actual["terminal_stage"] == 9
        assert not np.any(h[:, 11])
        np.testing.assert_allclose(h[:, 8:10], np.tile(actual["true_object"], (len(h), 1)))


@pytest.mark.parametrize("acceleration,speed", [(1, 1), (3, 1), (2.37, 1.19), (2, 4)])
def test_kinodynamic_bounded_infeasibility_and_trace(acceleration, speed):
    model = load(next((COURSE / "modules").glob("59-*/experiment.py")))
    for broken in [False, True]:
        p = {
            "acceleration_limit_m_s2": acceleration,
            "speed_limit_m_s": speed,
            "broken_mode": broken,
        }
        out = model._model(p, broken)
        expected = load(COURSE / "expansion_reference_cases.py").reference_signature(59, p)
        np.testing.assert_allclose(out["signature"], expected, atol=1e-8)
        trace = out["plots"]["mechanism"]["data"][0]
        assert out["signature"][2] == abs(trace["y"][-1])
        if broken:
            position = out["plots"]["response"]["data"][0]["y"]
            np.testing.assert_allclose(
                np.diff(position), np.diff(trace["x"]) * (trace["y"][1:] + trace["y"][:-1]) / 2
            )


@pytest.mark.parametrize("width,error", [(0.18, 10), (0.27, 10), (0.36, 0), (0.237, 7.3)])
def test_task_planner_exhaustion_is_explicit_failure(width, error):
    model = load(next((COURSE / "modules").glob("64-*/experiment.py")))
    p = {"corridor_width_m": width, "geometry_error_cm": error, "broken_mode": False}
    out = model._model(p, False)
    np.testing.assert_allclose(
        out["signature"], load(COURSE / "expansion_reference_cases.py").reference_signature(64, p)
    )
    if width - 0.01 * error < 0.16:
        assert out["signature"][0] == 0
    assert out["signature"][1] <= 2


@pytest.mark.parametrize("dropout,drift", [(120, 50), (240, 250), (173, 137), (20, 0), (400, -250)])
@pytest.mark.parametrize("broken", [False, True])
def test_replay_measures_recovery_events(dropout, drift, broken):
    model = load(next((COURSE / "modules").glob("67-*/experiment.py")))
    p = {"dropout_duration_ms": dropout, "clock_drift_ppm": drift, "broken_mode": broken}
    out = model.run(p)
    np.testing.assert_allclose(
        out["diagnostics"]["signature"],
        load(COURSE / "expansion_reference_cases.py").reference_signature(67, p),
        atol=1e-8,
    )
    d = out["diagnostics"]
    events = d["timing_events"]
    assert abs(d["calibration_scale"] - (1 + drift * 1e-6)) < 1e-12
    if d["recovery_observed"]:
        started = next(t for t, name in events if name == "watchdog entered hold")
        ended = next(t for t, name in events if name == "valid checkpoint reset and resumed")
        assert abs(d["signature"][2] - 1000 * (ended - started)) < 1e-9
        assert ended >= started
    if broken:
        assert not d["recovery_observed"]


@pytest.mark.parametrize(
    "dropout,speed,broken",
    [(0, 0.1, False), (10, 0.3, False), (40, 0.3, False), (17.3, 0.437, False), (10, 0.3, True)],
)
def test_mobile_stage_flow_and_independent_filter(dropout, speed, broken):
    model = load(next((COURSE / "modules").glob("68-*/experiment.py")))
    out = model._tracked_mission(dropout, speed, broken)
    h = out["history"]
    cov = out["covariances"]
    # Independent information-form updates from the synthetic measurement model.
    mean = np.zeros(4)
    P = 0.04 * np.eye(4)
    updates = {round(r[0], 8): r for r in out["updates"]}
    for k, row in enumerate(h):
        if round(row[0], 8) in updates:
            measurement = row[1:3] + 0.015 * np.array([np.sin(0.7 * k), np.cos(0.9 * k)])
            information = np.linalg.inv(P)
            rhs = information @ mean
            information[:2, :2] += np.eye(2) / 0.0025
            rhs[:2] += measurement / 0.0025
            P = np.linalg.inv(information)
            mean = P @ rhs
        np.testing.assert_allclose(row[5:9], mean, atol=2e-11)
        np.testing.assert_allclose(cov[k], P, atol=2e-11)
        assert np.linalg.eigvalsh(P).min() > 0
        acceleration = row[11:13]
        assert np.max(abs(acceleration)) <= 1
        mean[:2] += 0.1 * mean[2:] + 0.005 * acceleration
        mean[2:] += 0.1 * acceleration
        F = np.eye(4)
        F[:2, 2:] = 0.1 * np.eye(2)
        P = F @ P @ F.T + 1e-5 * np.eye(4)
        if k + 1 < len(h):
            np.testing.assert_allclose(
                h[k + 1, 1:3], row[1:3] + 0.1 * row[3:5] + 0.005 * acceleration, atol=1e-12
            )
            np.testing.assert_allclose(h[k + 1, 3:5], row[3:5] + 0.1 * acceleration, atol=1e-12)
    assert out["goal_reached"]
    if broken:
        assert out["minimum_clearance_m"] < 0.02
        assert not h[:, 9].any()
    else:
        assert out["minimum_clearance_m"] > 0.6
        assert h[:, 9].max() > np.log(0.7 / 0.3)
        assert not any(np.all(cell == [4, 0]) for cell in out["route"])
        if dropout:
            holds = h[h[:, 13] == 1]
            assert len(holds)
            assert np.linalg.norm(holds[-1, 3:5]) < np.linalg.norm(holds[0, 3:5])
    # Independent dense-time bound against exact polynomial minimum.
    sampled = []
    for row in h:
        tau = np.linspace(0, 0.1, 101)
        points = row[1:3] + tau[:, None] * row[3:5] + 0.5 * tau[:, None] ** 2 * row[11:13]
        moving = np.column_stack((np.full(len(tau), 6), -2 + speed * (row[0] + tau)))
        sampled.extend(
            [
                np.linalg.norm(points - [4, 0], axis=1).min(),
                np.linalg.norm(points - moving, axis=1).min(),
            ]
        )
    assert 0 <= min(sampled) - out["minimum_clearance_m"] < 1e-3
