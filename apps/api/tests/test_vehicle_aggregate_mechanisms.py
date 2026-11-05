"""Independent physical identities and full histories for the Vehicle repairs."""

import importlib.util
from pathlib import Path

import numpy as np
import pytest
from scipy.integrate import solve_ivp
from scipy.linalg import eigh

COURSE = Path(__file__).resolve().parents[3] / "courses/vehicle-dynamics"


def load(number):
    path = next((COURSE / "modules").glob(f"{number:02d}-*")) / "experiment.py"
    spec = importlib.util.spec_from_file_location(f"vehicle_{number}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    "steer,mu,broken",
    [
        (1, 0.7, False),
        (6, 1.15, False),
        (10, 0.7, False),
        (3.37, 0.93, False),
        (10, 1.5, False),
        (6, 1.15, True),
        (10, 0.7, True),
    ],
)
def test_nonlinear_bicycle_full_history_and_jacobian(steer, mu, broken):
    module = load(37)
    p = {"steer_deg": steer, "friction_mu": mu}
    study = module._dynamic_study(p, broken)

    # Independent lateral-velocity coordinates, axle moment balance and DOP853.
    def rhs(t, state):
        lateral, yaw = state
        slips = [np.deg2rad(steer) - (lateral + 1.2 * yaw) / 28, -(lateral - 1.5 * yaw) / 28]
        limits = mu * 9.81 * np.array([1450 * 1.5 / 2.7, 1450 * 1.2 / 2.7])
        requested = np.array([70000, 75000]) * slips
        forces = requested if broken else limits * np.tanh(requested / limits)
        return [(sum(forces) - 1450 * 28 * yaw) / 1450, np.dot([1.2, -1.5], forces) / 2400]

    independent = solve_ivp(
        rhs,
        [0, study["time"][-1]],
        [0, 0],
        t_eval=study["time"],
        method="DOP853",
        rtol=1e-11,
        atol=1e-12,
    )
    states = independent.y.T / np.array([28, 1])
    np.testing.assert_allclose(study["states"], states, atol=2e-8, rtol=2e-7)
    refined = module._dynamic_study(p, broken, dt=0.0025)
    common = min(len(study["states"]), len(refined["states"][::2]))
    np.testing.assert_allclose(
        study["states"][:common], refined["states"][::2][:common], atol=2e-8, rtol=2e-7
    )
    point = np.array([-0.07, 0.21])
    epsilon = 1e-6
    _, jac, _ = module._dynamic_rhs(point, np.deg2rad(steer), mu, broken)
    numeric = np.column_stack(
        [
            (
                module._dynamic_rhs(point + epsilon * axis, np.deg2rad(steer), mu, broken)[0]
                - module._dynamic_rhs(point - epsilon * axis, np.deg2rad(steer), mu, broken)[0]
            )
            / (2 * epsilon)
            for axis in np.eye(2)
        ]
    )
    np.testing.assert_allclose(jac, numeric, rtol=2e-8, atol=2e-8)
    if study["trim_valid"]:
        np.testing.assert_allclose(rhs(0, study["trim"] * np.array([28, 1])), 0, atol=3e-7)
        assert study["decay_margin"] == pytest.approx(
            -max(
                np.linalg.eigvals(
                    module._dynamic_rhs(study["trim"], np.deg2rad(steer), mu, broken)[1]
                ).real
            )
        )
    else:
        assert study["decay_margin"] == 0
    if not broken:
        assert max(study["utilization"]) <= 1
    assert np.max(abs(study["states"][:, 0])) <= 0.35


@pytest.mark.parametrize("accel,fraction", [(0.2, 0.3), (1, 0.58), (1.5, 0.75), (0.73, 0.413)])
def test_transfer_force_moment_and_contact_boundary(accel, fraction):
    module = load(38)
    model = module._model(
        {"lateral_accel_g": accel, "front_roll_stiffness_fraction": fraction}, False
    )
    front, rear, _, closure, loss = model["signature"]
    assert front * 1.55 + rear * 1.53 == pytest.approx(1450 * accel * 9.81 * 0.52)
    weight = 1450 * 9.81 * 1.5 / 2.7
    normals = np.linalg.solve([[1, 1], [-1.55 / 2, 1.55 / 2]], [weight, front * 1.55])
    if min(normals) >= 0:
        expected = 1.25 * 3500 * (2 * (weight / 7000) ** 0.86 - sum((normals / 3500) ** 0.86))
        assert loss == pytest.approx(expected)
    assert closure < 1e-9
    assert module._capacity_loss(weight, 0) == pytest.approx(0, abs=1e-10)
    assert module._capacity_loss(weight, weight) == pytest.approx(
        module._capacity_loss(weight, weight / 2)
    )
    assert np.all(
        np.diff([module._capacity_loss(weight, t) for t in np.linspace(0, weight / 2, 50)]) >= 0
    )


@pytest.mark.parametrize(
    "front,rear,broken",
    [(42000, 38000, False), (65000, 25000, False), (31731, 51237, False), (42000, 38000, True)],
)
def test_modal_energy_and_generalized_eigenproblem(front, rear, broken):
    module = load(39)
    m = np.diag([1450, 2600, 650])
    geometry = np.array([[1, 1.2, 0.775], [1, 1.2, -0.775], [1, -1.5, 0.765], [1, -1.5, -0.765]])
    k = geometry.T @ np.diag([1.04 * front, 0.96 * front, 0.97 * rear, 1.03 * rear]) @ geometry
    values, vectors = eigh(np.diag(np.diag(k)) if broken else k, m)
    result = module._model({"front_spring_rate_n_m": front, "rear_spring_rate_n_m": rear}, broken)
    np.testing.assert_allclose(result["signature"][:3], np.sqrt(values) / (2 * np.pi), atol=1e-12)
    expected = np.diag(m)[:, None] * vectors**2
    actual = np.array([t["y"] for t in result["plots"]["mechanism"]["data"]])
    np.testing.assert_allclose(actual, expected, atol=1e-12)
    np.testing.assert_allclose(actual.sum(axis=0), 1, atol=1e-12)
    assert result["signature"][-1] > 0.01 if broken else result["signature"][-1] < 1e-12


@pytest.mark.parametrize("gain,noise", [(0.35, 0.08), (0.13, 0.033), (0.7, 0.2)])
def test_observer_covariance_complete_history_independent_sum(gain, noise):
    module = load(57)
    actual = module._covariance_history(gain, noise)
    f = np.eye(3) + 0.02 * np.array([[-1.1, -0.35, 0.2], [0.8, -1.6, 0.1], [0, 0, -0.25]])
    observer_gain = np.diag([gain, 0.75 * gain, 0.45 * gain])
    c = np.eye(3) - observer_gain
    closed = c @ f
    added = c @ np.diag([2e-5, 4e-5, 1e-5]) @ c.T + noise**2 * observer_gain @ observer_gain.T
    # Sum independent noise contributions from each previous epoch.
    powers = [np.linalg.matrix_power(closed, i) for i in range(301)]
    accumulated = np.zeros((3, 3))
    expected = []
    for power in powers:
        expected.append(power @ (0.25 * np.eye(3)) @ power.T + accumulated)
        accumulated += power @ added @ power.T
    np.testing.assert_allclose(actual, expected, atol=1e-14, rtol=1e-11)
    assert np.linalg.eigvalsh(actual).min() > 0
    larger = module._covariance_history(gain, noise * 2)
    assert np.trace(larger[-1]) > np.trace(actual[-1])


@pytest.mark.parametrize("excitation,sigma", [(0.2, 150), (0.7, 80), (0.437, 36.7)])
def test_parameter_covariance_matches_qr_and_excitation_scaling(excitation, sigma):
    module = load(59)
    signature, _, _, standard = module._analyze(excitation, sigma, False)
    i = np.arange(60)
    x = excitation * np.column_stack(
        [
            0.030 * np.sin(0.25 * i) + 0.008 * np.cos(0.53 * i),
            0.028 * np.sin(0.25 * i + 0.16) + 0.004 * np.cos(0.91 * i),
        ]
    )
    _, r = np.linalg.qr(x, mode="reduced")
    inverse = np.linalg.solve(r, np.eye(2))
    np.testing.assert_allclose(
        standard, np.sqrt(np.diag(sigma**2 * inverse @ inverse.T)), rtol=1e-12
    )
    twice = module._analyze(excitation * 2, sigma, False)
    np.testing.assert_allclose(twice[-1], standard / 2, rtol=1e-12)
    assert signature[5] in (0, 0.5, 1)


@pytest.mark.parametrize("sigma,fraction", [(80, 0.35), (25, 0.2), (137, 0.47)])
def test_prediction_band_includes_parameter_uncertainty(sigma, fraction):
    module = load(33)
    result = module._model({"observation_sigma_n": sigma, "validation_fraction": fraction}, False)
    traces = {t["name"]: t for t in result["plots"]["mechanism"]["data"]}
    upper = traces["Conditional predictive upper"]["y"]
    assert np.all(upper > 1.96)
    # The added parameter term must increase with held-out regressor magnitude.
    x = np.array(result["plots"]["response"]["data"][0]["x"])
    ratio = (upper / 1.96) ** 2 - 1
    np.testing.assert_allclose(ratio / x**2, np.full_like(x, ratio[0] / x[0] ** 2), rtol=1e-11)


def test_shift_interruption_pays_road_resistance():
    module = load(47)
    _, time, speed, gears = module._simulate(4.1, 0.25, False)
    differences = np.diff(speed)
    assert np.any(differences < 0)
    indices = np.flatnonzero(differences < 0)
    expected = -(180 + 0.38 * speed[indices] ** 2) / 1450 * np.diff(time)[indices]
    np.testing.assert_allclose(differences[indices], expected, atol=1e-12, rtol=1e-10)
    assert gears[0] >= 1


@pytest.mark.parametrize(
    "number,key",
    [
        (26, "response"),
        (34, "response"),
        (35, "response"),
        (37, "state_history"),
        (52, "mechanism"),
        (53, "response"),
    ],
)
def test_repaired_axes_have_one_unit_per_axis(number, key):
    module = load(number)
    result = module.run({})
    plot = result["plots"][key]
    units = {}
    for trace in plot["data"]:
        units.setdefault(trace.get("yaxis", "y"), set()).add(trace["meta"]["y_unit"])
    assert all(len(v) == 1 for v in units.values())
    assert "yaxis2" in plot["layout"]


@pytest.mark.parametrize("fraction,severity", [(0.2, 0.5), (0.3, 1), (0.4, 2), (0.273, 1.417)])
def test_telemetry_capstone_full_raw_to_trajectory_and_qr_fit(fraction, severity):
    import json

    records = [
        json.loads(line)
        for line in (COURSE / "fixtures/gr86-can-replay-v1.jsonl").read_text().splitlines()
    ]
    wheels = []
    yaws = []
    for record in records:
        data = bytes.fromhex(record["data_hex"])
        t = record["source_time_us"] * 1e-6
        if record["can_id"] == "0x139":
            counts = [256 * data[i] + data[i + 1] for i in (0, 2, 4, 6)]
            wheels.append((t, sum(counts) / (4 * 128 * 3.6)))
        if record["can_id"] == "0x2D2":
            yaws.append((t, (256 * data[0] + data[1] - 32768) * np.pi / 18000))
    wheels = np.array(wheels)
    yaws = np.array(yaws)
    time, speed = wheels.T
    rate = np.interp(time, yaws[:, 0], yaws[:, 1])
    positions = np.zeros((len(time), 2))
    heading = 0.0
    for i, dt in enumerate(np.diff(time)):
        positions[i + 1] = positions[i] + speed[i] * dt * np.array(
            [np.cos(heading), np.sin(heading)]
        )
        heading += rate[i] * dt
    result = load(66)._telemetry(fraction, severity, False)
    np.testing.assert_allclose(result["speed"], speed, atol=1e-11)
    np.testing.assert_allclose(result["yaw_rad_s"], rate, atol=1e-11)
    np.testing.assert_allclose(
        np.c_[result["position"].real, result["position"].imag], positions, atol=1e-10
    )
    stop = int(np.floor((1 - fraction) * len(time)))
    accel = np.r_[0, np.diff(speed) / np.diff(time)]
    x = np.c_[accel, speed**2]
    observed = 1450 * accel + 0.45 * speed**2 + 2 * np.sin(0.9 * np.arange(len(time)))
    q, r = np.linalg.qr(x[1:stop], mode="reduced")
    estimate = np.linalg.solve(r, q.T @ observed[1:stop])
    np.testing.assert_allclose(result["parameters"], estimate, atol=2e-9)
    np.testing.assert_allclose(result["predicted_force"], x @ estimate, atol=2e-8)
    inverse = np.linalg.solve(r, np.eye(2))
    residual = observed[1:stop] - x[1:stop] @ estimate
    covariance = (residual @ residual / (stop - 3)) * (inverse @ inverse.T)
    np.testing.assert_allclose(result["covariance"], covariance, rtol=1e-8, atol=1e-12)
    assert result["split"] == stop
    assert all(v["passed"] for v in result["requirements"].values())


@pytest.mark.parametrize("setup,friction", [(0.02, 0.9), (0.15, 1.1), (0.0837, 0.973)])
def test_digital_twin_every_segment_independent_force_energy_and_gear_ledger(setup, friction):
    result = load(67)._lap(setup, friction)
    v = np.asarray(result["speed_m_s"])
    ds = np.asarray(result["segment_lengths_m"])
    k = np.asarray(result["curvature_per_m"])
    force = np.asarray(result["force_n"])
    loads = np.asarray(result["physical_loads_n"])
    drag = 0.5 * 1.225 * 0.72 * (1 + setup) * v**2
    rolling = 0.012 * 1450 * 9.81
    required = 1450 * np.diff(np.r_[v**2, v[0] ** 2]) / (2 * ds) + drag + rolling
    np.testing.assert_allclose(force, required, atol=2e-9)
    # Telescoping cyclic kinetic energy: net wheel work equals total road loss.
    assert sum(force * ds) == pytest.approx(sum((drag + rolling) * ds), abs=1e-6)
    assert result["temperature_c"] == pytest.approx(20 + sum(np.maximum(-force * ds, 0)) / 16000)
    down = 1.53125 * (1 + 2 * setup) * v**2
    np.testing.assert_allclose(loads.sum(axis=1), 1450 * 9.81 + down, atol=1e-9)
    # Half-track times left/right difference must reconstruct roll demand.
    np.testing.assert_allclose(
        (loads[:, 0] - loads[:, 1] + loads[:, 2] - loads[:, 3]) * 1.52 / 2,
        1450 * v**2 * k * 0.5,
        atol=1e-9,
    )
    normal = 1450 * 9.81 / 4
    mu = 1.15 * (1 + 0.3 * setup) * friction
    capacity = mu * normal * np.sum((loads / normal) ** 0.9, axis=1)
    np.testing.assert_allclose(
        result["grip_utilization"], np.hypot(force, 1450 * v**2 * k) / capacity, atol=1e-12
    )
    assert max(result["grip_utilization"]) <= 1 + 1e-8
    assert loads.min() >= 200 - 1e-7
    for speed, selected, demand in zip(v, result["gears"], force, strict=True):
        candidates = []
        for ratio in [3.63, 2.19, 1.54, 1.21, 1, 0.77]:
            rpm = speed * ratio * 4.1 * 60 / (0.31 * 2 * np.pi)
            torque = np.interp(
                rpm, [2000, 3000, 4000, 5000, 6000, 7000, 7400], [170, 205, 225, 230, 225, 200, 180]
            )
            candidates.append(torque * ratio * 4.1 * 0.9 / 0.31 if 2000 <= rpm <= 7400 else 0)
        assert selected == np.argmax(candidates) + 1
        assert demand <= max(candidates) + 1e-6
    assert result["lap_s"] == pytest.approx(sum(ds / v), abs=1e-11)
    assert result["lap_s"] == min(result["candidate_times_s"])


@pytest.mark.parametrize(
    "front,rear,kind",
    [(65000, 80000, "understeer"), (100000, 80000, "neutral"), (100000, 40000, "oversteer")],
)
def test_characteristic_speed_applicability_is_explicit(front, rear, kind):
    result = load(36).run({"front_cornering_n_rad": front, "rear_cornering_n_rad": rear})
    metrics = {m["id"]: m["value"] for m in result["metrics"]}
    assert bool(metrics["characteristic_available"]) == (kind == "understeer")
    assert bool(metrics["critical_available"]) == (kind == "oversteer")
    if kind != "understeer":
        assert len(result["plots"]["mechanism"]["data"][0]["x"]) == 0
    gradient = (1450 * 9.81 / 2.7) * (1.5 / front - 1.2 / rear)
    if kind == "oversteer":
        assert metrics["critical_speed"] == pytest.approx(np.sqrt(-9.81 * 2.7 / gradient))


@pytest.mark.parametrize("number", [26, 33, 34, 35, 36, 37, 38, 39, 45, 47, 52, 53, 54, 55, 57, 59])
def test_repaired_native_corners_and_off_grid_are_finite_and_recover(number):
    from itertools import product

    module = load(number)
    names = list(module.RANGES)
    cases = [
        dict(zip(names, values, strict=True))
        for values in product(*(module.RANGES[k] for k in names))
    ]
    cases.append({k: lo + 0.371 * (hi - lo) for k, (lo, hi) in module.RANGES.items()})
    for case in cases:
        healthy = module.run(case)
        fault = module.run({**case, "broken_mode": True})
        recovery = module.run(case)
        np.testing.assert_array_equal(
            healthy["diagnostics"]["signature"], recovery["diagnostics"]["signature"]
        )
        for result in [healthy, fault]:
            assert np.isfinite(result["diagnostics"]["signature"]).all()
            for plot in result["plots"].values():
                for trace in plot["data"]:
                    assert np.isfinite(trace["x"]).all() and np.isfinite(trace["y"]).all()
