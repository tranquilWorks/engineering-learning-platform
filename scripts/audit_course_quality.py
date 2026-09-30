#!/usr/bin/env python3
"""Reproducible structural inventory, explicitly not a semantic quality certificate."""

import hashlib
import json
import re
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
COURSES = ("dsp-radar", "controls-gnc", "robotics-autonomy", "vehicle-dynamics")
# Scoped numerical/physical review; this is not whole-course certification.
REPAIRED = {
    (
        "controls-gnc",
        36,
    ): "Executed full state-feedback acceleration with position and velocity terms, dimensioned gains, analytic derivatives and DC/pole checks.",
    (
        "controls-gnc",
        38,
    ): "Executed declared-cost CARE LQR and actual coupled plant/observer states; analytic CARE/spectrum and state-transition checks.",
    (
        "controls-gnc",
        42,
    ): "Measured the actual integral-state peak consistently, bounded manual/automatic actuation and explicitly censored recovery; independent piecewise-affine replay.",
    (
        "controls-gnc",
        43,
    ): "Integrated double-well dynamics and damping work; independent implicit solver plus energy, phase-field and zero-damping checks.",
    (
        "controls-gnc",
        45,
    ): "Recomputed the barrier filter at every sampled state; independent linear/geometric trajectory and full-history safety checks.",
    (
        "controls-gnc",
        46,
    ): "Constructed real gain-table knots and measured interpolation errors; independent secant evaluator plus knot, off-grid and refinement checks.",
    (
        "controls-gnc",
        47,
    ): "Integrated nonlinear cancellation residual with an explicit departure event; independent reciprocal-state trajectory/event and exact-cancellation checks.",
    (
        "controls-gnc",
        48,
    ): "Evaluated dimensionless sensitivity over the declared uncertainty and frequency grid; independent complex transfer and stability/pole checks.",
    (
        "controls-gnc",
        49,
    ): "Solved actual bounded horizon optimization and applied receding-horizon moves; independent Bellman policy plus full-plan feasibility, objective and KKT checks.",
    (
        "controls-gnc",
        50,
    ): "Generated excitation, fitted an ARX model and evaluated separate held-out free-run data; independent convolution/normal equations and rank/recovery checks.",
    (
        "controls-gnc",
        51,
    ): "Executed recursive least-squares gain, estimate and covariance updates; independent weighted batch information and zero-excitation checks.",
    (
        "controls-gnc",
        55,
    ): "Constructed and transformed actual sigma points; independently checked Gaussian moments and distinct mean/covariance weights. Scope is the transform component, not recursive UKF.",
    (
        "controls-gnc",
        66,
    ): "Executed calibration identification, feedback and scalar estimation across three stressed plants; independent normal-equation/information-form replay and plant/rank checks.",
    (
        "controls-gnc",
        67,
    ): "Executed exact planar motion, GNSS/inertial updates, waypoint guidance and freshness holds; independent complex-arc replay and timing/turn checks.",
    (
        "controls-gnc",
        68,
    ): "Executed timestamped command delivery, drop burst, old-packet rejection, plant feedback and fail-zero watchdog; independent arrival reconstruction and zero-fault checks.",
    (
        "robotics-autonomy",
        68,
    ): "Executed range observations, occupancy, graph replanning, timed hold/resume and continuous segment separation; independent breadth-first replay and geometric checks.",
    (
        "robotics-autonomy",
        69,
    ): "Executed calibrated reach, static support and timed contact control with exact spring work; independent kinematic/work replay and zero-tank checks.",
    (
        "vehicle-dynamics",
        61,
    ): "Corrected dimensional signatures and sample-mean interpretation; independent ellipse geometry plus circle, scaling and sampling checks.",
    (
        "vehicle-dynamics",
        62,
    ): "Corrected signature order and units; executed drag-shifted, power-clipped force envelope and actual demand; independent force-balance and zero-speed checks.",
    (
        "vehicle-dynamics",
        63,
    ): "Executed closed-ellipse offset geometry and local distance/speed integration with a dimensional penalty; independent quadrature and circle/corridor checks.",
    (
        "vehicle-dynamics",
        64,
    ): "Executed cyclic force reachability and an energy budget that changes speed, with brake-work temperature; independent Jacobi/piecewise-energy solution and seam/refinement checks.",
    (
        "vehicle-dynamics",
        65,
    ): "Corrected dimensions and unused-point validation in an explicitly synthetic factorial; independent contrast solution and rank/disjointness checks.",
    (
        "vehicle-dynamics",
        66,
    ): "Executed synthetic CAN/BLE provenance, timing, calibration, reconstruction, chronological fitting and fault recovery; independent raw-byte/scalar reference and split/covariance checks.",
    (
        "vehicle-dynamics",
        67,
    ): "Executed an explicitly illustrative tire/load/gear/brake/aero/track/line/lap chain and friction scenarios; independent scalar solver and load/force/refinement checks.",
}
REPAIRED[("controls-gnc", 56)] = (
    "Executed recover a trajectory with rts smoothing. An independently conditioned joint Gaussian trajectory uses C[i,j]=1+q min(i,j). Its posterior covariance is C-C(C+rI)^-1 C; prefix conditioning supplies the filtered variances. It does not import the production recursion. Embedded checkpoint; selected synthetic numerical and browser evidence. Aggregate course review remains separate."
)
REPAIRED[("controls-gnc", 57)] = (
    "Executed compose quaternions and calibrate sensor vectors. The reference constructs independent axis rotations using rotation vectors and applies R_fault=I+1.2²(R_true-I). This identity tests the scaled-quaternion defect without calling the production quaternion functions. Embedded checkpoint; selected synthetic numerical and browser evidence. Aggregate course review remains separate."
)
REPAIRED[("controls-gnc", 60)] = (
    "Executed solve position and clock from synthetic pseudoranges. The reference uses complex-step derivatives and a separate nonlinear least-squares solver on dimensionless rationalized range offsets. The production solver uses an analytic Jacobian and Gauss-Newton increments. Embedded checkpoint; selected synthetic numerical and browser evidence. Aggregate course review remains separate."
)
REPAIRED[("controls-gnc", 61)] = (
    "Executed inject and reset a one-axis navigation error state. The independent full-state filter uses the same physical model but evaluates process covariance by three-point Gaussian quadrature and uses the Schur covariance update instead of the production Joseph recurrence. Embedded checkpoint; selected synthetic numerical and browser evidence. Aggregate course review remains separate."
)
REPAIRED[("controls-gnc", 62)] = (
    "Executed detect and exclude a synthetic range fault. The reference computes leverage through an orthonormal SVD basis and uses a separate complex-step nonlinear solver before and after selecting a row. Embedded checkpoint; selected synthetic numerical and browser evidence. Aggregate course review remains separate."
)
REPAIRED[("controls-gnc", 64)] = (
    "Executed compare civilian moving-beacon guidance trajectories. The independent reference integrates range, LOS angle and both headings in relative polar coordinates with a different numerical integrator, rather than replaying the Cartesian production state. Embedded checkpoint; selected synthetic numerical and browser evidence. Aggregate course review remains separate."
)
REPAIRED[("controls-gnc", 65)] = (
    "Executed solve a bounded terminal guidance objective. The independent reference solves a two-dimensional dual terminal-residual equation with clipped controls, rather than the production twenty-variable bounded least-squares problem. Embedded checkpoint; selected synthetic numerical and browser evidence. Aggregate course review remains separate."
)
REPAIRED[("robotics-autonomy", 25)] = (
    "Executed project configurations and velocities onto a circle constraint. The independent signature uses the analytic polar radius and obstacle distance. Physical tests use the tangent basis [-sin(theta),cos(theta)] to reconstruct velocity, separately from the production matrix projector. Embedded checkpoint; selected synthetic numerical and browser evidence. Aggregate course review remains separate."
)
REPAIRED[("robotics-autonomy", 26)] = (
    "Executed compose rigid transforms and diagnose invalid rotation blends. The reference applies separate scalar x/z rotation formulas to coordinates and uses the analytic blend defect 2f(1-f)(1-cos(theta)). This independently checks the homogeneous-matrix implementation. Embedded checkpoint; selected synthetic numerical and browser evidence. Aggregate course review remains separate."
)
REPAIRED[("robotics-autonomy", 27)] = (
    "Executed transform twists and dual wrenches with power invariance. The reference uses complex planar rotations and explicit cross products for the separate force, moment, angular and linear components. It does not construct or invert the production adjoint matrix. Embedded checkpoint; selected synthetic numerical and browser evidence. Aggregate course review remains separate."
)
REPAIRED[("robotics-autonomy", 28)] = (
    "Executed build a planar position jacobian and diagnose singularities. The reference differentiates forward kinematics using complex steps and computes singular values from the two-by-two Gram matrix eigenvalues. It separately predicts the missing-column discrepancy instead of copying the production finite-difference array. Embedded checkpoint; selected synthetic numerical and browser evidence. Aggregate course review remains separate."
)
REPAIRED[("robotics-autonomy", 29)] = (
    "Executed separate damped task motion from exact null-space motion. The reference derives the Jacobian by complex-step kinematics, computes the primary command with SVD and constructs the one-dimensional null basis from the cross product of the two Jacobian rows. It does not use the production pseudoinverse projector. Embedded checkpoint; selected synthetic numerical and browser evidence. Aggregate course review remains separate."
)
REPAIRED[("robotics-autonomy", 30)] = (
    "Executed map planar end-effector force to joint torque. The reference differentiates forward kinematics using complex steps, then independently forms torque and the two scalar powers. It retains Jacobians and torque vectors for full-sweep comparisons. Embedded checkpoint with selected synthetic numerical and browser evidence. At zero force both torque maps produce zero, so the fault is unobservable through power. At zero length the ideal geometric torques vanish; the interactive length range remains positive. This is quasistatic mapping, with no inertia, friction or actuator model. Aggregate course review remains separate."
)
REPAIRED[("robotics-autonomy", 31)] = (
    "Executed construct manipulator inertia, coriolis and gravity terms. The reference builds mass from Cartesian point-mass Jacobians, obtains mass and potential derivatives by complex steps, and constructs C from Christoffel symbols. It checks M, C, Mdot and gravity separately. Embedded checkpoint with selected synthetic numerical and browser evidence. At elbow zero or pi the omitted sine coupling vanishes, so this fault can be locally hidden. The point-mass model excludes distributed link inertia, friction, elasticity and motor dynamics; it is an instantaneous identity check, not a trajectory experiment. Aggregate course review remains separate."
)
REPAIRED[("robotics-autonomy", 32)] = (
    "Executed identify payload and damping from synthetic joint torque. The reference constructs the multisine through a frequency/phase array and solves the regularized normal equations, independently of the production augmented least-squares factorization. It retains fitted parameters, regressors and held-out residuals. Embedded checkpoint with selected synthetic numerical and browser evidence. Stationary samples cannot identify viscous damping because velocity is zero. The ridge solution depends on the stated units and prior; real identification also requires sensor calibration, suitable noise assumptions and a model of unmodeled dynamics. Aggregate course review remains separate."
)
REPAIRED[("robotics-autonomy", 33)] = (
    "Executed time-scale two joint cubics under speed and acceleration limits. The reference constructs polynomial objects, differentiates them, and evaluates their extrema and sampled trajectories independently of the production explicit cubic formulas. Embedded checkpoint with selected synthetic numerical and browser evidence. At zero displacement the trajectory is stationary; the interactive displacement range remains positive to keep a nonzero duration. A short move or generous limits can make one second feasible, so the named fault does not guarantee a violation at every setting. Endpoint acceleration is nonzero and torque limits are absent. Aggregate course review remains separate."
)
REPAIRED[("robotics-autonomy", 34)] = (
    "Executed compare joint and cartesian kinematic feedback. The reference differentiates forward kinematics by complex steps, uses an explicit two-by-two inverse, and integrates a separate Cartesian-controller state with RK45. Production uses an analytic Jacobian, pseudoinverse and DOP853. Embedded checkpoint with selected synthetic numerical and browser evidence. At zero Cartesian error both mappings command zero motion, so a settled target does not distinguish them. The experiment assumes ideal velocity servos, a fixed local goal branch and no collision or torque constraints. Near singularities, rate clipping changes the nominal exponential error law. Aggregate course review remains separate."
)
REPAIRED[("robotics-autonomy", 35)] = (
    "Executed integrate computed torque with gravity error and saturation. The reference computes inverse dynamics from Cartesian point accelerations and Newton-Euler force moments. It obtains inertia columns through unit accelerations and integrates with RK45, independently of the production analytic M/C/g formulation and DOP853 integration. Embedded checkpoint with selected synthetic numerical and browser evidence. At zero mismatch and without saturation, computed torque yields the derived linear error equation. At a pose with zero gravity contribution the sign fault is locally hidden; along a trajectory it can reappear. Torque clipping invalidates exact cancellation even with an otherwise correct model. Aggregate course review remains separate."
)
REPAIRED[("robotics-autonomy", 36)] = (
    "Executed compute operational inertia and dynamically consistent torque. The reference differentiates link-centre and endpoint coordinates with complex steps, then solves a constrained block system for operational inertia and null acceleration. Its faulty comparison uses a cross-product null basis instead of the production pseudoinverse projector. Embedded checkpoint with selected synthetic numerical and browser evidence. At zero secondary fraction both modes reduce to the same primary task command. This is a local zero-velocity calculation with exact gravity compensation. A moving task requires Jdot*qdot, updated geometry and an actual trajectory controller. Aggregate course review remains separate."
)
REPAIRED[("robotics-autonomy", 37)] = (
    "Executed compare impedance and ideal admittance contact transients. The reference advances both state vectors using the exact two-by-two matrix exponential. Production integrates the differential equations with DOP853. Their complete state, energy and contact-force traces are compared. Embedded checkpoint with selected synthetic numerical and browser evidence. At zero damping the ideal system conserves energy and generally does not settle. The maintained-preload linearization and ideal position servo exclude contact loss, actuator limits and servo bandwidth. A censored 0.4 s result is not a measured settling time. Aggregate course review remains separate."
)
REPAIRED[("robotics-autonomy", 38)] = (
    "Executed regulate tangential motion and normal contact force. The reference integrates normal and tangential surface coordinates with RK45, including the unilateral force law. Production integrates Cartesian position with DOP853; the resulting positions, velocities and forces are compared after an independent basis transformation. Embedded checkpoint with selected synthetic numerical and browser evidence. At zero surface angle world vertical and the physical normal coincide, so both modes agree. At zero force goal the unilateral contact may open in faulty mode. This ideal velocity-servo example omits impacts, robot inertia, sensor delay and actuator constraints. Aggregate course review remains separate."
)
REPAIRED[("robotics-autonomy", 39)] = (
    "Executed account for delayed port work with a causal energy limiter. The reference uses cumulative candidate work and its running maximum to derive the minimal reflection correction that keeps the balance nonnegative. This global mathematical identity independently checks the production causal sample loop. Embedded checkpoint with selected synthetic numerical and browser evidence. At a zero-velocity sample the port work is zero regardless of finite force. This is a prescribed-motion, sampled-work demonstration with ideal force application. It does not establish continuous-time passivity, a closed-loop delay margin or stability of a physical haptic system. Aggregate course review remains separate."
)
REPAIRED[("robotics-autonomy", 40)] = (
    "Executed swing up and capture a reaction-wheel pendulum. The reference integrates the coupled mass matrix in body and relative-wheel coordinates with RK45 and an independently expressed upright-angle event. Production integrates eliminated equations in absolute-wheel coordinates with DOP853. State conversion and body-energy traces are compared. Embedded checkpoint with selected synthetic numerical and browser evidence. Exactly downward at zero rate, this energy law cannot initiate motion without a perturbation. No capture within twelve seconds is censored evidence, not a proof of impossibility. Wheel speed and position are unregulated and unlimited; successful body capture is not hardware qualification. Aggregate course review remains separate."
)
REPAIRED[("robotics-autonomy", 41)] = (
    "Executed transform and project points through a pinhole camera. The reference computes rotated camera components explicitly and derives projection and sensitivity from ray ratios, independently of the production matrix transform. It compares the entire camera cloud, accepted mask and projected pixels. Embedded checkpoint with selected synthetic numerical and browser evidence. At an empty accepted set, zero-valued projection summaries are unavailable sentinels, not visible on-axis points. A far cloud may hide the faulty visibility count while retaining wrong pixels. The model excludes lens distortion, occlusion, image bounds, calibration uncertainty and camera noise. Aggregate course review remains separate."
)
KNOWN = {}

# Additional findings from the wider direct model review; separate repair scopes.
for _number in range(1, 17):
    KNOWN[("vehicle-dynamics", _number)] = (
        "The main response chart joins signature quantities with different physical units on one generic SI axis; sweeps also lack a named response/unit. Replace these with physically meaningful curves or separately labeled quantities and specific limiting-case checks."
    )
KNOWN[("robotics-autonomy", 42)] = (
    "Calibration errors are formulas of view count and distortion; no synthetic calibration views are fitted or independently reprojected."
)
KNOWN[("robotics-autonomy", 43)] = (
    "Feature repeatability, descriptor distance and count are formulas of threshold and rotation; no image features or descriptors are computed."
)
KNOWN[("robotics-autonomy", 44)] = (
    "Inlier and false-acceptance metrics are formulas of outlier fraction and threshold; no correspondence consensus model is fitted."
)
KNOWN[("robotics-autonomy", 45)] = (
    "Stereo depth and uncertainty formulas execute, but the round-trip residual is fixed rather than computed from reprojection."
)
KNOWN[("robotics-autonomy", 46)] = (
    "Pose and reprojection errors are formulas of noise and landmark count; no landmark pose solve is executed."
)
KNOWN[("robotics-autonomy", 47)] = (
    "Occupancy and entropy metrics are formulas of beam count and probability rather than ray updates on an occupancy grid."
)
KNOWN[("robotics-autonomy", 48)] = (
    "ICP residual, transform error and iteration count are algebraic surrogates; no point correspondence or registration iteration is executed."
)
KNOWN[("robotics-autonomy", 52)] = (
    "Appearance and geometry gates execute, but map deformation is a fixed-factor residual formula rather than a recomputed graph solution."
)


def audit():
    rows = []
    registry_path = ROOT / "courses/dsp-radar/assessment-map.json"
    checkpoints = (
        {r["module_id"]: r for r in json.loads(registry_path.read_text())["lessons"]}
        if registry_path.exists()
        else {}
    )
    for course in COURSES:
        for path in sorted(
            (ROOT / "courses" / course / "modules").glob("*/module.yaml")
        ):
            folder = path.parent
            module = yaml.safe_load(path.read_text())
            lesson = (folder / "lesson.md").read_text()
            controls = module.get("controls", [])
            blocks = module.get("blocks", [])
            records = [
                p
                for p in folder.rglob("*")
                if p.is_file()
                and p.suffix in {".yaml", ".json", ".md", ".py"}
                and "__pycache__" not in p.parts
            ]
            digest = hashlib.sha256()
            for p in sorted(records):
                digest.update(
                    str(p.relative_to(folder)).encode() + b"\0" + p.read_bytes()
                )
            number = module["number"]
            issue = KNOWN.get((course, number))
            evidence = sorted(
                str(p.relative_to(ROOT))
                for p in records
                if p.suffix == ".json"
                or p.name
                in (
                    "conversion.yaml",
                    "design.yaml",
                    "verification.yaml",
                    "requirements-trace.yaml",
                )
            )
            headings = [
                line.lstrip("# ")
                for line in lesson.splitlines()
                if line.startswith("#")
            ]
            findings = {
                "concept": {
                    "state": "present"
                    if len(lesson.split()) >= 200
                    else "review_required",
                    "word_count": len(lesson.split()),
                    "headings": headings,
                },
                "equations": {
                    "state": "candidate_text_present"
                    if re.search(r"=|\\\[|\$\$", lesson)
                    else "review_required",
                    "rendered_math_expected": bool(
                        re.search(r"\\\[|\\\(|\$\$", lesson)
                    ),
                },
                "prediction": {
                    "state": "present"
                    if any(b["type"] == "prediction" and b.get("text") for b in blocks)
                    else "review_required"
                },
                "controls": {
                    "state": "present" if controls else "review_required",
                    "labels": [c["label"] for c in controls],
                    "units": {c["id"]: c.get("unit") for c in controls},
                },
                "plots": {
                    "state": "declared"
                    if any(b["type"] in ("plot", "plot_grid") for b in blocks)
                    else "review_required"
                },
                "interpretation": {
                    "state": "declared"
                    if any(b["type"] == "callout" for b in blocks)
                    else "review_required"
                },
                "focused_checks": {
                    "state": "candidate_text_present"
                    if re.search(
                        r"check|question|exercise|assessment", lesson, re.IGNORECASE
                    )
                    else "review_required"
                },
                "failure_recovery": {
                    "state": "candidate_text_present"
                    if re.search(r"fail|broken", lesson, re.IGNORECASE)
                    and re.search(r"recover|restor|repair", lesson, re.IGNORECASE)
                    else "review_required"
                },
                "independent_evidence": {
                    "state": "retained_artifacts_require_semantic_review"
                    if evidence
                    else "review_required",
                    "paths": evidence,
                },
                "competency_alignment": {
                    "state": "map_present_requires_semantic_review"
                    if (ROOT / "courses" / course / "competency-map.yaml").exists()
                    else "aggregate_map_pending"
                },
            }
            rows.append(
                {
                    "course": course,
                    "module": module["id"],
                    "number": number,
                    "title": module["title"],
                    "path": str(folder.relative_to(ROOT)),
                    "payload_sha256": digest.hexdigest(),
                    "checks": findings,
                    "semantic_review": "blocked"
                    if issue
                    else (
                        "scoped_model_reviewed"
                        if (course, number) in REPAIRED
                        else "not_recertified_by_structural_audit"
                    ),
                    "scoped_review": REPAIRED.get((course, number)),
                    "assessment_review": {
                        "checkpoint": checkpoints[module["id"]]["id"],
                        "competency": checkpoints[module["id"]]["competency_id"],
                        "cumulative": checkpoints[module["id"]]["domain_id"],
                        "case_count": len(checkpoints[module["id"]]["retained_cases"]),
                        "scope_limit": checkpoints[module["id"]]["claim_limit"],
                        "learner_result": "not_recorded",
                    }
                    if course == "dsp-radar" and module["id"] in checkpoints
                    else None,
                    "known_issue": issue,
                    "manual_learner_validation": "not_run",
                }
            )
    sources = []
    native_sources = {c + "-learning" for c in COURSES}
    for line in subprocess.check_output(
        ["git", "ls-tree", "HEAD:courses"], cwd=ROOT, text=True
    ).splitlines():
        mode, _kind, tail = line.split(maxsplit=2)
        if mode != "160000":
            continue
        sha, name = tail.split("\t")
        sources.append(
            {
                "repository": name,
                "pinned_commit": sha,
                "delivery": "native_revised_course"
                if name in native_sources
                else "source_only",
            }
        )
    return {
        "schema_version": 1,
        "validation_level": "structural_inventory_and_named_semantic_findings",
        "claim_boundary": "Presence checks do not certify derivations, physical fidelity, independent references, curriculum completeness or learning effectiveness.",
        "engineering_lesson_count": len(rows),
        "source_repositories": sources,
        "lessons": rows,
    }


if __name__ == "__main__":
    value = audit()
    target = ROOT / "docs/course-quality/lesson-audit.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, indent=2) + "\n")
    # Baked into the browser so discovered limitations travel with their lesson.
    projection = [
        {
            "course": r["course"],
            "module": r["module"],
            "known_issue": r["known_issue"],
            "scoped_review": r["scoped_review"],
            "assessment_review": r["assessment_review"],
            "evidence_count": len(r["checks"]["independent_evidence"]["paths"]),
        }
        for r in value["lessons"]
    ]
    (ROOT / "apps/web/src/lesson-quality.json").write_text(
        json.dumps(projection, indent=2) + "\n"
    )
    print(
        f"Audited {len(value['lessons'])} lessons; {sum(bool(r['known_issue']) for r in value['lessons'])} confirmed semantic issue(s); no blanket quality certification."
    )
