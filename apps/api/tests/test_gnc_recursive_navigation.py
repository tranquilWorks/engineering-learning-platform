"""Recursive filters and 3D strapdown/fusion: independent histories and invariants."""

import ast
import importlib.util
from pathlib import Path

import numpy as np
import pytest
from scipy.spatial.transform import Rotation

ROOT = Path(__file__).resolve().parents[3]
COURSE = ROOT / "courses/controls-gnc"


def load(path):
    spec = importlib.util.spec_from_file_location("checked", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def production(n):
    return load(next((COURSE / "modules").glob(f"{n}-*/experiment.py")))


REF = load(COURSE / "recursive_navigation_references.py")


@pytest.mark.parametrize("method", ["EKF", "UKF"])
@pytest.mark.parametrize(
    "sigma,initial,alpha,broken",
    [
        (0.5, 1.0, 1.0, False),
        (0.05, 0.0, 0.2, False),
        (2.0, 3.0, 2.0, False),
        (0.733, 1.231, 0.47, False),
        (0.8, 1.0, 0.7, True),
    ],
)
def test_recursive_complete_histories(method, sigma, initial, alpha, broken):
    actual = production(54 if method == "EKF" else 55)._recursive_filter(
        sigma, initial, alpha, method, broken
    )
    expected = REF.recursive(sigma, initial, alpha, method, broken)
    np.testing.assert_allclose(actual, expected, rtol=2e-10, atol=2e-10)
    assert actual.shape == (80, 13)
    assert np.all(actual[:, 4] > 0) and np.all(actual[:, 10] > 0)
    assert np.all(actual[:, 10] <= actual[:, 4] + 1e-12)
    np.testing.assert_allclose(actual[:, 6], actual[:, 2] - actual[:, 5])
    np.testing.assert_allclose(actual[:, 9], actual[:, 3] + actual[:, 8] * actual[:, 6])
    if broken:
        np.testing.assert_array_equal(actual[:, 8], 0)
    else:
        # An overconfident wrong prior legitimately has a large initial transient.
        # Require recovery, not uniformly good RMSE across incompatible priors.
        assert np.sqrt(np.mean((actual[-20:, 9] - actual[-20:, 1]) ** 2)) < 0.05
        if initial == 0 and sigma == 0.05:
            assert np.sqrt(np.mean((actual[:10, 9] - actual[:10, 1]) ** 2)) > 0.3


NAV_CASES = [
    dict(mode="coast"),
    dict(mode="coast", duration=120.0, bias=0.2),
    dict(mode="coast", duration=1.0, bias=0.0),
    dict(mode="coast", duration=17.3, bias=0.073),
    dict(mode="coast", broken=True),
    dict(mode="fusion"),
    dict(mode="fusion", interval=0.2, walk=0.001),
    dict(mode="fusion", interval=10.0, walk=0.08),
    dict(mode="fusion", interval=1.7, walk=0.023),
    dict(mode="fusion", broken=True),
    dict(mode="survey", dropout=4.0),
    dict(mode="survey", dropout=0.0, turn_limit=3.0),
    dict(mode="survey", dropout=20.0, turn_limit=30.0),
    dict(mode="survey", dropout=7.3, turn_limit=11.7),
    dict(mode="survey", dropout=4.0, broken=True),
]


@pytest.mark.parametrize("parameters", NAV_CASES)
def test_navigation_full_history_and_covariance(parameters):
    actual, covariance, events = production(61)._navigation_sequence(**parameters)
    expected, reference_covariance = REF.navigation(**parameters)
    # Quaternion double-cover is a representation equivalence, not an error allowance.
    for a, b in zip(actual, expected, strict=True):
        if a[13:17] @ b[13:17] < 0:
            b[13:17] *= -1
    # 120 s unaided covariance can reach 1e8 in mixed units; relative tolerance
    # is explicit. Near-zero attitude angles use an absolute angular budget.
    np.testing.assert_allclose(actual, expected, rtol=2e-7, atol=2e-7)
    np.testing.assert_allclose(covariance, reference_covariance, rtol=2e-7, atol=2e-7)
    np.testing.assert_allclose(np.linalg.norm(actual[:, 13:17], axis=1), 1, atol=1e-12)
    np.testing.assert_allclose(covariance, covariance.transpose(0, 2, 1), atol=1e-7)
    assert np.linalg.eigvalsh(covariance).min() > 0
    assert all(np.linalg.norm(e["delta"]) > 0 for e in events)
    if parameters["mode"] == "fusion" and not parameters.get("broken"):
        assert actual[-1, 17] < actual[-1, 18]


def test_stationary_tilted_platform_gravity_and_90_degree_body_force():
    m = production(59)
    rotation = Rotation.from_euler("xyz", [0.3, -0.2, 0.8])
    q = rotation.as_quat(scalar_first=True)
    state = (np.zeros(3), np.zeros(3), q, np.zeros(3), np.zeros(3))
    force = rotation.inv().apply([0, 0, 9.80665])
    for _ in range(100):
        state = m._mechanize(state, np.zeros(3), force, 0.1)
    np.testing.assert_allclose(state[0], 0, atol=1e-11)
    np.testing.assert_allclose(state[1], 0, atol=1e-11)
    q = Rotation.from_euler("z", np.pi / 2).as_quat(scalar_first=True)
    out = m._mechanize(
        (np.zeros(3), np.zeros(3), q, np.zeros(3), np.zeros(3)),
        np.zeros(3),
        np.array([1, 0, 9.80665]),
        2.0,
    )
    np.testing.assert_allclose(out[0], [0, 2, 0], atol=1e-12)
    np.testing.assert_allclose(out[1], [0, 2, 0], atol=1e-12)


def test_error_transition_matches_perturbed_mechanization_to_order_dt_squared():
    m = production(61)
    r = Rotation.from_euler("xyz", [0.2, -0.1, 0.4])
    q = r.as_quat(scalar_first=True)
    state = (
        np.array([1.0, 2.0, 3.0]),
        np.array([0.2, 0.3, 0.4]),
        q,
        np.array([0.01, 0.02, 0.03]),
        np.array([0.001, 0.002, 0.003]),
    )
    omega = np.array([0.1, 0.2, -0.1])
    force = np.array([0.2, -0.3, 9.7])

    def error(output, nominal):
        return np.r_[
            output[0] - nominal[0],
            output[1] - nominal[1],
            (
                Rotation.from_quat(nominal[2], scalar_first=True).inv()
                * Rotation.from_quat(output[2], scalar_first=True)
            ).as_rotvec(),
            output[3] - nominal[3],
            output[4] - nominal[4],
        ]

    errors = []
    for dt in [0.01, 0.005]:
        nominal = m._mechanize(state, omega, force, dt)
        columns = []
        for delta in np.eye(15) * 1e-6:
            perturbed = (
                state[0] + delta[:3],
                state[1] + delta[3:6],
                m._quat_product(q, m._quat_increment(delta[6:9])),
                state[3] + delta[9:12],
                state[4] + delta[12:15],
            )
            columns.append(error(m._mechanize(perturbed, omega, force, dt), nominal) / 1e-6)
        numeric = np.column_stack(columns)
        approximation = m._nav_transition(q, omega - state[4], force - state[3], dt)
        errors.append(np.max(abs(numeric - approximation)))
    assert errors[0] < 2e-4 and errors[1] < 0.3 * errors[0]


def test_gnss_clock_geometry_and_joint_update_cross_coupling():
    m = production(61)
    for p in [np.zeros(3), np.array([23.0, -12.0, 7.0])]:
        fix, ranges = m._gnss_fix(p, 2.3)
        np.testing.assert_allclose(fix, REF.gnss(p, 2.3), atol=1e-8)
        assert np.linalg.norm(fix[:3] - p) < 0.2 and abs(fix[3] - 75) < 0.2
    _, _, events = m._navigation_sequence()
    last = events[-1]
    assert np.linalg.norm(last["delta"][6:9]) > 1e-9
    assert np.linalg.norm(last["delta"][9:12]) > 1e-9
    assert np.linalg.norm(last["delta"][12:15]) > 1e-9
    # Reset is an attitude-coordinate transform, not identity for a finite correction.
    assert not np.allclose(last["prior_covariance"], last["posterior_covariance"])


def test_fault_recovery_and_outage_do_not_claim_a_finished_mission():
    m = production(67)
    good = m.run({"gnss_dropout_s": 4.0, "turn_rate_limit_deg_s": 12.0, "broken_mode": False})
    bad = m.run({"gnss_dropout_s": 4.0, "turn_rate_limit_deg_s": 12.0, "broken_mode": True})
    repeat = m.run({"gnss_dropout_s": 4.0, "turn_rate_limit_deg_s": 12.0, "broken_mode": False})
    np.testing.assert_array_equal(
        good["diagnostics"]["navigation_history"], repeat["diagnostics"]["navigation_history"]
    )
    assert all(v["passed"] for v in good["diagnostics"]["integrated_requirements"].values())
    assert not all(v["passed"] for v in bad["diagnostics"]["integrated_requirements"].values())
    h = good["diagnostics"]["navigation_history"]
    assert not np.any((h[:, 0] >= 5) & (h[:, 0] < 9) & (h[:, 22] > 0))
    assert np.any((h[:, 0] >= 9) & (h[:, 22] > 0))
    assert np.any(h[:, 24] > 0)
    assert "SURVEY-COMPLETE" not in good["diagnostics"]["integrated_requirements"]


def test_embedded_kernels_identical_and_oracle_has_no_production_imports():
    names = [
        "_skew",
        "_quat_product",
        "_quat_increment",
        "_rotation",
        "_mechanize",
        "_nav_transition",
        "_gnss_fix",
        "_nav_update",
        "_navigation_sequence",
    ]

    def definitions(n):
        tree = ast.parse(next((COURSE / "modules").glob(f"{n}-*/experiment.py")).read_text())
        return {
            f.name: ast.dump(f)
            for f in tree.body
            if isinstance(f, ast.FunctionDef) and f.name in names
        }

    assert definitions(59) == definitions(61) == definitions(67)
    text = (COURSE / "recursive_navigation_references.py").read_text()
    assert "importlib" not in text and "experiment.py" not in text
    assert "expected-independent.json" not in text


def test_integrated_evidence_is_visible_and_fits_existing_inline_contract():
    import json

    import yaml

    from elp_api.serialization import jsonable

    for number in (54, 55, 59, 61, 67):
        folder = next((COURSE / "modules").glob(f"{number}-*"))
        manifest = yaml.safe_load((folder / "module.yaml").read_text())
        parameters = {control["id"]: control["default"] for control in manifest["controls"]}
        if number == 61:
            parameters["gnss_interval_s"] = 0.2  # largest update-event payload
        result = production(number).run(parameters)
        assert len(json.dumps(jsonable(result), separators=(",", ":")).encode()) < 8 * 1024 * 1024
        visible = {b.get("table") for b in manifest["blocks"] if b["type"] == "table"}
        assert "integration_evidence" in visible
        assert len(result["tables"]["integration_evidence"]["rows"]) >= 7
        assert any(b.get("source") == "integration.md" for b in manifest["blocks"])
        if number in (61, 67):
            assert "last_correction" in visible
            assert len(result["tables"]["last_correction"]["rows"]) == 5


def test_recursive_kernel_copies_cannot_drift():
    names = {"_recursive_filter", "_append_recursive"}
    snapshots = []
    for number in (54, 55):
        path = next((COURSE / "modules").glob(f"{number}-*/experiment.py"))
        snapshots.append(
            {
                node.name: ast.dump(node)
                for node in ast.parse(path.read_text()).body
                if isinstance(node, ast.FunctionDef) and node.name in names
            }
        )
    assert set(snapshots[0]) == names
    assert snapshots[0] == snapshots[1]
