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
KNOWN = {}

# Additional findings from the wider direct model review; separate repair scopes.
for _number in range(1, 17):
    KNOWN[("vehicle-dynamics", _number)] = (
        "The main response chart joins signature quantities with different physical units on one generic SI axis; sweeps also lack a named response/unit. Replace these with physically meaningful curves or separately labeled quantities and specific limiting-case checks."
    )
KNOWN[("controls-gnc", 36)] = (
    "The displayed state-feedback control omits the velocity feedback term; recompute control from both propagated states and reconcile its units."
)
KNOWN[("controls-gnc", 38)] = (
    "The separation-principle model places poles directly but the lesson calls the design LQR; distinguish pole placement from a cost-derived optimal gain."
)
KNOWN[("controls-gnc", 42)] = (
    "The peak integral-state metric uses peak command in nominal mode and final integral state in broken mode; it does not measure the named quantity consistently."
)
KNOWN[("controls-gnc", 43)] = (
    "The declared nonlinear double-well phase portrait is replaced by an exponential sinusoid and unrelated energy formulas; the stated dynamics are not integrated."
)
KNOWN[("controls-gnc", 45)] = (
    "The barrier plot extrapolates one fixed command without reevaluating the state-dependent barrier; it can cross the safety boundary while presented as a filtered trajectory."
)
KNOWN[("controls-gnc", 46)] = (
    "The interpolation error is assigned from grid spacing instead of measuring interpolation of a sampled gain schedule."
)
KNOWN[("controls-gnc", 47)] = (
    "The quadratic feedback-linearization model is replaced by a linear exponential and an algebraic terminal-error formula; the nonlinear closed loop is not executed."
)
KNOWN[("controls-gnc", 48)] = (
    "The uncertainty plot does not sweep the declared uncertainty interval, and the inverse decay-rate metric is labeled dimensionless sensitivity without a defined transfer response."
)
KNOWN[("controls-gnc", 49)] = (
    "The MPC lesson clips a fixed move and divides a residual by horizon; it does not minimize the stated horizon cost or execute receding-horizon control."
)
KNOWN[("controls-gnc", 50)] = (
    "Identification conditioning, parameter error and held-out residual are algebraic functions of excitation settings; no dynamic model is fitted or validated."
)
KNOWN[("controls-gnc", 51)] = (
    "The online-identification lesson does not execute its recursive least-squares update; error and covariance metrics are parameter formulas."
)
KNOWN[("controls-gnc", 55)] = (
    "Unscented-transform errors and weights are assigned directly; sigma points and their weighted transformed moments are not computed."
)
KNOWN[("controls-gnc", 56)] = (
    "The claimed RTS smoother multiplies filtered covariance by a fixed 0.65 instead of executing a forward filter and backward smoother."
)
KNOWN[("controls-gnc", 57)] = (
    "Quaternion norm and rotation orthogonality errors are fixed constants; no quaternion-to-matrix transformation is evaluated."
)
KNOWN[("controls-gnc", 60)] = (
    "GNSS position and clock errors are algebraic dilution formulas; the claimed pseudorange position/clock solve is not executed."
)
KNOWN[("controls-gnc", 61)] = (
    "GNSS/INS uncertainty is reduced by a fixed 0.35 factor rather than an error-state covariance update and state reset."
)
KNOWN[("controls-gnc", 62)] = (
    "The post-exclusion residual is multiplied by a fixed 0.15 without excluding a measurement and recomputing the navigation solution."
)
KNOWN[("controls-gnc", 64)] = (
    "The guidance comparison reports an explicitly named miss proxy, but the trajectories and variants are not integrated; its scope and cumulative interpretation need revision."
)
KNOWN[("controls-gnc", 65)] = (
    "Terminal error is assigned from an acceleration shortfall; the terminal dynamics are not propagated and the displayed violation is not measured from applied commands."
)
KNOWN[("robotics-autonomy", 25)] = (
    "Constraint residual and tangent dimension are assigned without constructing the constraint Jacobian or projecting a configuration velocity."
)
KNOWN[("robotics-autonomy", 26)] = (
    "Orthogonality, determinant and composition errors are algebraic surrogates without constructing and composing rigid transforms."
)
KNOWN[("robotics-autonomy", 27)] = (
    "Power-invariance and adjoint round-trip errors are assigned without transforming an actual twist/wrench pair."
)
KNOWN[("robotics-autonomy", 28)] = (
    "Singular values and finite-difference errors are assigned from elbow-angle formulas without constructing the Jacobian or differencing kinematics."
)
KNOWN[("robotics-autonomy", 29)] = (
    "Task error and null-space leakage are parameter formulas without executing a Jacobian pseudoinverse and null-space projection."
)
KNOWN[("robotics-autonomy", 30)] = (
    "The virtual-power error is assigned from force times lever arm, which has torque units; no joint/Cartesian velocity power comparison is executed."
)
KNOWN[("robotics-autonomy", 31)] = (
    "Inertia eigenvalue and skew-identity error are assigned without constructing inertia and Coriolis matrices."
)
KNOWN[("robotics-autonomy", 32)] = (
    "Payload error, regressor conditioning and inverse-dynamics residual are formulas of the guess and excitation rather than an identified model and held-out torque calculation."
)
KNOWN[("robotics-autonomy", 33)] = (
    "The cubic trajectory duration omits its 1.5 peak-velocity factor, while the nominal limit-violation metric is forced to zero and plotted acceleration omits time scaling."
)
KNOWN[("robotics-autonomy", 34)] = (
    "Joint/task tracking and torque metrics use condition-number formulas rather than executing the stated kinematics and feedback loops."
)
KNOWN[("robotics-autonomy", 35)] = (
    "Computed-torque tracking and gravity residuals are algebraic surrogates rather than an integrated robot model with model-based compensation."
)
KNOWN[("robotics-autonomy", 36)] = (
    "Operational-space inertia and residuals are assigned without forming the joint inertia, Jacobian or operational-space dynamics."
)
KNOWN[("robotics-autonomy", 37)] = (
    "Contact responses and settling metrics use exponential surrogates instead of the declared impedance/admittance differential equations."
)
KNOWN[("robotics-autonomy", 38)] = (
    "Hybrid motion/force residuals and projector error are assigned without constructing the surface-frame projectors or executing feedback."
)
KNOWN[("robotics-autonomy", 39)] = (
    "Passivity energy and recovery are formulas of delay and force limit; no delayed work/energy trace is executed."
)
KNOWN[("robotics-autonomy", 40)] = (
    "Swing-up time and balance error are algebraic surrogates; no underactuated dynamics, energy controller or balancing transition is executed."
)
KNOWN[("robotics-autonomy", 41)] = (
    "Pinhole projection executes, but the near-plane violation metric is a fixed mode flag rather than a test of projected point depth."
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
