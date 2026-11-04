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
