"""Preserve the original trajectory solver while skipping already-feasible scans."""

import importlib.util
import json
import subprocess
import time
from pathlib import Path

import numpy as np
import pytest
import yaml

ROOT = Path(__file__).resolve().parents[3]
RELATIVE = Path(
    "courses/robotics-autonomy/modules/58-optimize-a-trajectory-through-obstacle-constraints"
)
BASELINE = "b107ac198543e8dfb563c6aae4175cc87da6210d"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def models(tmp_path_factory):
    old = tmp_path_factory.mktemp("r58-original") / "experiment.py"
    old.write_bytes(
        subprocess.check_output(["git", "show", f"{BASELINE}:{RELATIVE}/experiment.py"], cwd=ROOT)
    )
    return load(old, "r58_original"), load(ROOT / RELATIVE / "experiment.py", "r58_current")


CASES = [
    (name, params)
    for name, params in yaml.safe_load((ROOT / RELATIVE / "design.yaml").read_text())[
        "scenarios"
    ].items()
]
CASES += [
    (
        f"corner-{clearance}-{weight}-{broken}",
        {"required_clearance_m": clearance, "smoothness_weight": weight, "broken_mode": broken},
    )
    for clearance in (0.05, 1.0)
    for weight in (2.0, 50.0)
    for broken in (False, True)
]


def same(first, second):
    if isinstance(first, dict):
        assert first.keys() == second.keys()
        for key in first:
            same(first[key], second[key])
    elif isinstance(first, (list, tuple)):
        assert len(first) == len(second)
        for a, b in zip(first, second, strict=True):
            same(a, b)
    elif isinstance(first, np.ndarray):
        np.testing.assert_array_equal(first, second)
    else:
        assert first == second


@pytest.mark.parametrize("name,parameters", CASES, ids=[name for name, _ in CASES])
def test_complete_output_matches_original_solver_exactly(models, name, parameters):
    original, current = models
    started = time.perf_counter()
    before = original.run(parameters)
    before_seconds = time.perf_counter() - started
    started = time.perf_counter()
    after = current.run(parameters)
    after_seconds = time.perf_counter() - started
    same(before, after)
    print(
        "R58_TIMING "
        + json.dumps(
            {
                "scenario": name,
                "parameters": parameters,
                "before_seconds": before_seconds,
                "after_seconds": after_seconds,
                "whole_output_exact": True,
            }
        )
    )
    assert len(after["plots"]["mechanism"]["data"][0]["y"]) == 1201
    assert after["plots"]["response"]["data"][0]["x"][[0, -1]].tolist() == [0.0, 10.0]
    if name in ("baseline", "sweep_1", "sweep_2", "broken", "recovery"):
        retained = json.loads((ROOT / RELATIVE / "evidence/expected-independent.json").read_text())
        np.testing.assert_allclose(
            after["diagnostics"]["signature"],
            retained["cases"][name]["signature"],
            atol=1e-8,
            rtol=1e-8,
        )


def test_near_contact_infeasible_and_degenerate_projection_preserves_order(models):
    original, current = models
    safety = 1.45
    rng = np.random.default_rng(58)
    paths = [
        np.array([[0.0, safety + offset], [5.0, safety + offset], [10.0, safety + offset]])
        for offset in (-2e-8, -1e-9, -1e-10, 0.0, 1e-10, 1e-8, 2e-8)
    ]
    paths += [np.array([[0.0, 0.0], [5.0, 0.0], [5.0, 0.0], [10.0, 0.0]])]
    for _ in range(64):
        points = np.column_stack((np.linspace(0, 10, 31), rng.uniform(-2.5, 2.5, 31)))
        points[[0, -1], 1] = 0.0
        paths.append(points)
    for points in paths:
        before = points.copy()
        expected = original._restore_segment_feasibility(points, safety)
        actual = current._restore_segment_feasibility(points, safety)
        np.testing.assert_array_equal(actual, expected)
        np.testing.assert_array_equal(points, before)
        np.testing.assert_array_equal(actual[[0, -1]], before[[0, -1]])
    manifest = yaml.safe_load((ROOT / RELATIVE / "module.yaml").read_text())
    assert manifest["runtime"]["timeout_seconds"] == 3
