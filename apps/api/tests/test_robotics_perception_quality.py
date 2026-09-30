"""Executed Robotics perception and mapping, with independent geometry and state checks."""

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
BASELINE = "f04472f16fc1da00e817d385eaef0a63f3c71b48"
HISTORICAL_HEAD = "607c716993be14e7b782897ab054a7f8478f5dc0"
SELECTED = {"robotics-autonomy": (42, 43, 44, 45, 46, 47, 48, 52)}
CASES = [(course, n) for course, numbers in SELECTED.items() for n in numbers]


def load(path):
    spec = importlib.util.spec_from_file_location("navigation_quality", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def folder(course, n):
    return next((ROOT / "courses" / course / "modules").glob(f"{n}-*"))


def run(n, course="robotics-autonomy", **changes):
    path = folder(course, n)
    manifest = yaml.safe_load((path / "module.yaml").read_text())
    p = {c["id"]: c["default"] for c in manifest["controls"]}
    p.update(changes)
    return load(path / "experiment.py").run(p)["diagnostics"]


def test_exact_scope_and_prerequisite_inventory():
    contract = yaml.safe_load(
        subprocess.check_output(
            ["git", "show", f"{HISTORICAL_HEAD}:contracts/active-batch.yaml"], cwd=ROOT, text=True
        )
    )
    assert contract["batch"]["id"] == "ELP-ROBOTICS-PERCEPTION-QUALITY-08"
    assert contract["sources"]["baseline_commit"] == BASELINE
    assert (
        subprocess.check_output(
            ["git", "rev-parse", BASELINE + "^{tree}"], cwd=ROOT, text=True
        ).strip()
        == contract["sources"]["baseline_tree"]
    )
    paths = subprocess.check_output(
        ["git", "diff", "--name-only", BASELINE, HISTORICAL_HEAD, "--", "courses", ".gitmodules"],
        cwd=ROOT,
        text=True,
    ).splitlines()
    allowed = [f"courses/{c}/modules/{n}-*/**" for c, n in CASES] + [
        f"courses/{c}/{name}"
        for c in SELECTED
        for name in (
            "expansion_reference_cases.py",
            "expansion-map.yaml",
            "competency-map.yaml",
        )
    ]
    allowed += [
        "courses/robotics-autonomy/modules/31-*/" + name
        for name in ("experiment.py", "lesson.md", "module.yaml")
    ]
    allowed += [
        f"courses/robotics-autonomy/modules/{n}-*/module.yaml" for n in (32, 34, 36, 37, 40, 41)
    ]
    assert all(any(fnmatch.fnmatch(p, a) for a in allowed) for p in paths)
    for course in SELECTED:
        path = f"courses/{course}/competency-map.yaml"
        before = yaml.safe_load(
            subprocess.check_output(["git", "show", f"{BASELINE}:{path}"], cwd=ROOT, text=True)
        )
        after = yaml.safe_load(
            subprocess.check_output(
                ["git", "show", f"{HISTORICAL_HEAD}:{path}"], cwd=ROOT, text=True
            )
        )
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
    reviewed = tmp_path / "reviewed_reference.py"
    current_text = subprocess.check_output(
        ["git", "show", f"{HISTORICAL_HEAD}:{path.relative_to(ROOT)}"], cwd=ROOT, text=True
    )
    reviewed.write_text(current_text)
    before, after = load(historical), load(reviewed)

    def definitions(source):
        return {
            n.name: ast.get_source_segment(source, n)
            for n in ast.parse(source).body
            if isinstance(n, ast.FunctionDef)
        }

    old, new = definitions(original), definitions(current_text)
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
        for name, value in [
            ("expected-independent", expected),
            ("actual-production", actual),
        ]:
            saved = json.loads((path / f"evidence/{name}.json").read_text())
            np.testing.assert_allclose(
                saved["cases"][scenario]["signature"], value, atol=1e-8, rtol=1e-8
            )


@pytest.fixture(scope="module")
def runtime():
    return ExperimentRuntime(CourseCatalog([ROOT / "courses/robotics-autonomy"]))


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
        ref = load(ROOT / "courses" / course / "expansion_reference_cases.py")
        assert_independent(n, result.diagnostics, ref.robotics_perception_reference(n, p))
        for plot in result.model_dump(mode="json")["plots"].values():
            for trace in plot["data"]:
                for coordinate in ("x", "y", "z"):
                    if coordinate in trace:
                        assert np.isfinite(trace[coordinate]).all()


def details(n, broken=False, **changes):
    path = folder("robotics-autonomy", n)
    p = {
        c["id"]: c["default"]
        for c in yaml.safe_load((path / "module.yaml").read_text())["controls"]
    }
    p.update(broken_mode=broken, **changes)
    production = load(path / "experiment.py").run(p)["diagnostics"]
    reference = load(
        ROOT / "courses/robotics-autonomy/expansion_reference_cases.py"
    ).robotics_perception_reference(n, p)
    return production, reference


FIELDS = {
    42: (
        "training_camera_points",
        "observed_pixels",
        "design_matrix",
        "coefficients",
        "heldout_camera_points",
        "heldout_true_pixels",
        "heldout_predicted_pixels",
        "heldout_residuals",
        "outer_mask",
    ),
    43: (
        "base_image",
        "rotated_image",
        "base_response",
        "rotated_response",
        "base_features",
        "rotated_features",
        "base_descriptors",
        "rotated_descriptors",
        "base_orientations",
        "rotated_orientations",
        "geometric_pairs",
        "descriptor_distances",
    ),
    44: (
        "source_pixels",
        "target_pixels",
        "displacements",
        "true_outliers",
        "translation",
        "residuals",
        "accepted",
    ),
    45: (
        "estimated_point",
        "true_point",
        "observed_pixels",
        "reprojected_pixels",
        "pixel_jacobian",
        "point_covariance",
        "depth_sweep",
        "uncertainty_sweep",
    ),
    46: (
        "landmarks",
        "observed_pixels",
        "true_rotation",
        "true_translation",
        "rotation",
        "translation",
        "camera_points",
        "predicted_pixels",
        "residuals",
    ),
    47: (
        "truth",
        "cell_centres",
        "angles",
        "ray_paths",
        "log_odds",
        "probabilities",
        "hit_mask",
        "traversed_free_mask",
    ),
    48: (
        "source_points",
        "target_points",
        "clean_source",
        "true_rotation",
        "true_translation",
        "source_outliers",
        "rotation",
        "translation",
        "moved_points",
        "nearest_indices",
        "distances",
        "accepted",
        "history",
        "transform_history",
        "accepted_history",
        "solver_status",
    ),
    52: (
        "true_nodes",
        "odometry",
        "baseline_nodes",
        "optimized_nodes",
        "closure_measurement",
        "innovation",
        "factor_inserted",
        "robust_weight",
        "odometry_residuals",
        "closure_residual",
        "node_displacements",
        "gradient",
    ),
}


def assert_independent(n, actual, expected):
    for key in ("signature", *FIELDS[n]):
        if key == "solver_status":
            assert actual[key] == expected[key]
        elif key == "ray_paths":
            assert len(actual[key]) == len(expected[key])
            for a, b in zip(actual[key], expected[key], strict=True):
                np.testing.assert_allclose(a, b, atol=1e-8, rtol=1e-8)
        else:
            np.testing.assert_allclose(
                actual[key], expected[key], atol=1e-8, rtol=1e-8, err_msg=f"P{n} {key}"
            )


@pytest.mark.parametrize("n", SELECTED["robotics-autonomy"])
@pytest.mark.parametrize("broken", (False, True))
def test_full_geometry_arrays_match_separate_formulations(n, broken):
    actual, expected = details(n, broken)
    assert_independent(n, actual, expected)


def test_calibration_fits_observations_and_holds_out_different_poses():
    d = run(42)
    A = np.asarray(d["design_matrix"])
    pixels = np.asarray(d["observed_pixels"]).ravel()
    beta = np.asarray(d["coefficients"])
    assert d["rank"] == 4 and d["training_point_count"] == 216
    np.testing.assert_allclose(A.T @ (A @ beta - pixels), 0, atol=1e-8, rtol=1e-8)
    residual = np.asarray(d["heldout_predicted_pixels"]) - d["heldout_true_pixels"]
    np.testing.assert_allclose(d["heldout_residuals"], residual, atol=1e-8, rtol=1e-8)
    assert len(residual) == 48 and sum(d["outer_mask"]) == 12
    assert d["signature"][0] < run(42, broken_mode=True)["signature"][0]


def test_calibration_zero_distortion_is_not_a_forced_fault_penalty():
    normal = run(42, radial_k1=0)
    restricted = run(42, radial_k1=0, broken_mode=True)
    assert normal["signature"][0] < 0.1 and restricted["signature"][0] < 0.1
    assert restricted["coefficients"][1] == 0 and restricted["rank"] == 3


def test_descriptor_fault_preserves_detector_and_zero_rotation_hides_it():
    normal = run(43)
    bad = run(43, broken_mode=True)
    for key in (
        "base_image",
        "rotated_image",
        "base_response",
        "rotated_response",
        "base_features",
        "rotated_features",
        "geometric_pairs",
    ):
        np.testing.assert_array_equal(normal[key], bad[key])
    assert (
        normal["signature"][0] == bad["signature"][0]
        and normal["signature"][2] == bad["signature"][2]
    )
    assert normal["signature"][1] < bad["signature"][1]
    for mode in (False, True):
        d = run(43, image_rotation_deg=0, broken_mode=mode)
        assert d["matching_available"] and abs(d["signature"][1]) < 1e-8


def test_pixel_patch_descriptors_are_normalized_actual_samples():
    d = run(43)
    for key in ("base_descriptors", "rotated_descriptors"):
        values = np.asarray(d[key])
        assert values.shape[1] == 81
        np.testing.assert_allclose(values.mean(axis=1), 0, atol=1e-8, rtol=1e-8)
        np.testing.assert_allclose(np.linalg.norm(values, axis=1), 1, atol=1e-8, rtol=1e-8)
    assert np.shape(d["base_image"]) == (96, 96)
    assert (
        run(43, detector_threshold=0.8)["signature"][2]
        < run(43, detector_threshold=0.01)["signature"][2]
    )


def test_consensus_refits_its_actual_mask_without_truth_labels():
    d = run(44)
    delta = np.asarray(d["displacements"])
    accepted = np.asarray(d["accepted"], bool)
    np.testing.assert_allclose(d["translation"], delta[accepted].mean(axis=0), atol=1e-8, rtol=1e-8)
    np.testing.assert_array_equal(accepted, np.linalg.norm(delta - d["translation"], axis=1) <= 2.0)
    outliers = np.asarray(d["true_outliers"], bool)
    np.testing.assert_allclose(
        d["signature"][2],
        sum(accepted & outliers) / sum(outliers),
        atol=1e-8,
        rtol=1e-8,
    )
    bad = run(44, broken_mode=True)
    np.testing.assert_allclose(
        bad["translation"],
        np.asarray(bad["displacements"]).mean(axis=0),
        atol=1e-8,
        rtol=1e-8,
    )
    assert d["signature"][1] < bad["signature"][1]


def test_consensus_no_outlier_limit_has_an_explicit_rate_convention():
    a = run(44, outlier_fraction=0)
    b = run(44, outlier_fraction=0, broken_mode=True)
    assert a["signature"][2] == b["signature"][2] == 0
    np.testing.assert_allclose(a["translation"], b["translation"], atol=1e-8, rtol=1e-8)


def test_stereo_reprojects_actual_rays_and_covariance_is_positive():
    d = run(45)
    bad = run(45, broken_mode=True)
    np.testing.assert_allclose(d["estimated_point"], d["true_point"], atol=1e-8, rtol=1e-8)
    np.testing.assert_allclose(d["reprojected_pixels"], d["observed_pixels"], atol=1e-8, rtol=1e-8)
    covariance = np.asarray(d["point_covariance"])
    J = np.asarray(d["pixel_jacobian"])
    np.testing.assert_allclose(
        covariance, d["pixel_noise_std"] ** 2 * J @ J.T, atol=1e-8, rtol=1e-8
    )
    assert np.linalg.eigvalsh(covariance).min() > -1e-12 and d["positive_depth"]
    assert bad["signature"][2] > 1 and abs(bad["signature"][0] - d["signature"][0]) > 1
    # A biased model can report smaller conditional uncertainty; it excludes calibration bias.
    assert bad["signature"][1] < d["signature"][1]


def test_fixed_disparity_baseline_sweep_changes_scene_range():
    a = run(45, baseline_m=0.18)
    b = run(45, baseline_m=0.36)
    np.testing.assert_allclose(
        b["true_point"], 2 * np.asarray(a["true_point"]), atol=1e-8, rtol=1e-8
    )
    np.testing.assert_allclose(
        b["estimated_point"], 2 * np.asarray(a["estimated_point"]), atol=1e-8, rtol=1e-8
    )
    np.testing.assert_allclose(
        b["point_covariance"],
        4 * np.asarray(a["point_covariance"]),
        atol=1e-8,
        rtol=1e-8,
    )


def test_pose_stays_rigid_and_zero_noise_recovers_the_local_branch():
    d = run(46, landmark_noise_px=0)
    R = np.asarray(d["rotation"])
    np.testing.assert_allclose(R.T @ R, np.eye(3), atol=1e-8, rtol=1e-8)
    np.testing.assert_allclose(np.linalg.det(R), 1, atol=1e-8, rtol=1e-8)
    np.testing.assert_allclose(d["signature"], 0, atol=1e-8, rtol=1e-8)
    assert d["jacobian_rank"] == 6 and d["minimum_camera_depth"] > 0.2
    assert run(46, landmark_noise_px=0, broken_mode=True)["signature"][0] > 0.5


def test_pose_analytic_jacobian_matches_independent_complex_perturbations():
    from scipy.linalg import expm

    d = run(46)
    R = np.asarray(d["rotation"])
    t = np.asarray(d["translation"])
    landmarks = np.asarray(d["landmarks"])
    expected = []
    for axis in np.eye(6):
        x, y, z = axis[:3]
        skew = np.array([[0.0, -z, y], [z, 0.0, -x], [-y, x, 0.0]])
        rotated = expm(1e-20j * skew) @ R
        camera = landmarks @ rotated.T + t + 1e-20j * axis[3:]
        pixels = d["used_focal_length"] * camera[:, :2] / camera[:, 2, None] + [
            320,
            240,
        ]
        expected.append(np.imag(pixels.ravel()) / 1e-20)
    J = np.asarray(d["jacobian"])
    np.testing.assert_allclose(J, np.column_stack(expected), atol=1e-8, rtol=1e-8)
    residual = np.asarray(d["residuals"]).ravel()
    np.testing.assert_allclose(
        (J.T @ residual) / np.linalg.norm(J, axis=0), 0, atol=1e-8, rtol=1e-8
    )
    assert d["solver_status"] in {
        "small_increment",
        "stalled_search",
        "maximum_iterations",
    }


def test_range_updates_preserve_unknown_prior_and_omit_only_free_evidence():
    normal = run(47)
    bad = run(47, broken_mode=True)
    hits = np.asarray(normal["hit_mask"], bool)
    free = np.asarray(normal["traversed_free_mask"], bool)
    prob = np.asarray(normal["probabilities"])
    np.testing.assert_array_equal(hits, bad["hit_mask"])
    np.testing.assert_allclose(
        prob[hits], np.asarray(bad["probabilities"])[hits], atol=1e-8, rtol=1e-8
    )
    np.testing.assert_array_equal(np.asarray(normal["log_odds"])[~hits & ~free], 0)
    np.testing.assert_array_equal(np.asarray(bad["log_odds"])[free], 0)
    assert np.all(prob[free] < 0.5) and normal["signature"][1] < bad["signature"][1]
    assert bad["signature"][2] == 1 and normal["signature"][2] < 1
    truth = np.asarray(normal["truth"], bool)
    np.testing.assert_allclose(
        normal["signature"][2], np.mean(prob[~truth] >= 0.45), atol=1e-8, rtol=1e-8
    )


def test_ray_corner_ties_and_first_hits_are_geometric():
    model = load(folder("robotics-autonomy", 47) / "experiment.py")
    for angle in (0.0, np.pi / 4, np.pi / 2, np.pi, 3 * np.pi / 4):
        path = model.dda(angle)
        assert path[0][:2] == (15, 15)
        assert not any(cell[2] for cell in path[:-1])
        if not path[-1][2]:
            row, col, _hit, entry = path[-1]
            direction = np.array([np.cos(angle), np.sin(angle)])
            exits = [
                (0.1 * (index - 15) + np.sign(component) * 0.05) / component
                for index, component in zip((col, row), direction, strict=True)
                if abs(component) > 1e-14
            ]
            assert entry <= 1.4 and min(exits) >= 1.4 - 1e-12
        assert np.all(np.diff([cell[3] for cell in path]) > 0)
    path = model.dda(np.pi / 4)
    assert all(row == col for row, col, hit, entry in path)


def test_icp_uses_rigid_composition_and_a_descending_actual_objective():
    for broken in (False, True):
        d = run(48, broken_mode=broken)
        R = np.asarray(d["rotation"])
        history = np.asarray(d["history"])
        np.testing.assert_allclose(R.T @ R, np.eye(2), atol=1e-8, rtol=1e-8)
        np.testing.assert_allclose(np.linalg.det(R), 1, atol=1e-8, rtol=1e-8)
        assert np.max(np.diff(history[:, 0]), initial=0) < 1e-10
        assert d["signature"][2] == len(history) == len(d["transform_history"])
        prior_R = np.eye(2)
        prior_t = np.array([0.25, 0.0])
        for matrix, record in zip(d["transform_history"], history, strict=True):
            matrix = np.asarray(matrix)
            now_R, now_t = matrix[:, :2], matrix[:, 2]
            incremental_R = now_R @ prior_R.T
            incremental_t = now_t - incremental_R @ prior_t
            np.testing.assert_allclose(
                np.linalg.norm(incremental_t), record[1], atol=1e-8, rtol=1e-8
            )
            np.testing.assert_allclose(
                abs(np.arctan2(incremental_R[1, 0], incremental_R[0, 0])),
                record[2],
                atol=1e-8,
                rtol=1e-8,
            )
            prior_R, prior_t = now_R, now_t


def test_icp_difficult_initialization_retains_finite_local_failure_status():
    d = run(48, initial_offset_m=1.5, outlier_fraction=0.7)
    assert d["solver_status"] == "maximum_iterations" and d["signature"][2] == 30
    assert d["signature"][1] > 0.1
    assert np.isfinite(d["signature"]).all()


def test_loop_graph_anchor_stationarity_and_actual_robust_weight():
    for broken in (False, True):
        d = run(52, broken_mode=broken)
        nodes = np.asarray(d["optimized_nodes"])
        baseline = np.asarray(d["baseline_nodes"])
        np.testing.assert_array_equal(nodes[0], [0.0, 0.0])
        np.testing.assert_allclose(d["gradient"], 0, atol=1e-8, rtol=1e-8)
        np.testing.assert_allclose(
            d["odometry_residuals"],
            np.diff(nodes, axis=0) - d["odometry"],
            atol=1e-8,
            rtol=1e-8,
        )
        np.testing.assert_allclose(
            d["signature"][2],
            np.linalg.norm(nodes - baseline, axis=1).max(),
            atol=1e-8,
            rtol=1e-8,
        )
        weight = 1.0 if broken else min(1.0, 0.05 / np.linalg.norm(d["closure_residual"]))
        np.testing.assert_allclose(d["signature"][0], 0.78 * weight, atol=1e-8, rtol=1e-8)
    assert run(52)["signature"][2] < run(52, broken_mode=True)["signature"][2]


def test_loop_rejection_zero_innovation_and_bad_geometry_preserve_controls():
    for changes in (
        {"descriptor_score": 0.5},
        {"geometric_residual_m": 2.0},
        {"geometric_residual_m": 0.0},
    ):
        d = run(52, **changes)
        np.testing.assert_allclose(d["optimized_nodes"], d["baseline_nodes"], atol=1e-8, rtol=1e-8)
        assert abs(d["signature"][2]) < 1e-8
    rejected = run(52, geometric_residual_m=2)
    fault = run(52, geometric_residual_m=2, broken_mode=True)
    np.testing.assert_array_equal(rejected["closure_measurement"], fault["closure_measurement"])
    assert not rejected["factor_inserted"] and fault["factor_inserted"]
    assert fault["signature"][2] > 0.5


def test_prior_inertia_polish_changes_only_the_declared_wording():
    path = folder("robotics-autonomy", 31)
    old = (
        "The reported skew defect is the norm of the symmetric part of Mdot−2C, "
        "with inertia-rate units."
    )
    new = (
        "The reported skew defect is ||S+Sᵀ|| with S=Mdot−2C, "
        "twice the conventional symmetric-part norm, with inertia-rate units."
    )
    original = subprocess.check_output(
        ["git", "show", f"{BASELINE}:{(path / 'experiment.py').relative_to(ROOT)}"],
        cwd=ROOT,
        text=True,
    )
    expected = original.replace(old, new)
    assert ast.dump(ast.parse(expected)) == ast.dump(
        ast.parse((path / "experiment.py").read_text())
    )
    manifest = yaml.safe_load(
        subprocess.check_output(
            ["git", "show", f"{BASELINE}:{(path / 'module.yaml').relative_to(ROOT)}"],
            cwd=ROOT,
            text=True,
        )
    )
    manifest["summary"] = manifest["summary"].replace(old, new)
    assert manifest == yaml.safe_load((path / "module.yaml").read_text())
    assert "twice the conventional symmetric-part norm" in (path / "lesson.md").read_text()


def test_prior_static_overview_polish_preserves_every_other_manifest_field():
    for n in (32, 34, 36, 37, 40, 41):
        path = folder("robotics-autonomy", n) / "module.yaml"
        before = yaml.safe_load(
            subprocess.check_output(
                ["git", "show", f"{BASELINE}:{path.relative_to(ROOT)}"],
                cwd=ROOT,
                text=True,
            )
        )
        after = yaml.safe_load(path.read_text())
        assert before.pop("summary") != after.pop("summary")
        assert before == after
