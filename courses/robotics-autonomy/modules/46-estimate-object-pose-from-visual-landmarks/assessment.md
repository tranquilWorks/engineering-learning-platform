# P46 course checkpoint

## Predict and derive

Recover object pose from landmarks and check projection consistency.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `pixel_i=project(R*landmark_i+t); R in SO(3), t in metres`
- `delta=argmin ||J*delta+pixel_residual||²`
- `R_next=exp([delta_rotation]x)*R; t_next=t+delta_translation`

## Controlled comparison

- `landmark_noise_px`: 1.2 → 8.0. Hold the other controls at baseline and explain the mechanism before executing.
- `visible_landmarks`: 12.0 → 40.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Pose changes both rotation and translation of each 3D point; reprojection and cheirality distinguish plausible solutions.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Known correspondences and an initialized solver do not solve unrestricted object detection.

Competency links: VISION-PERCEPTION, MANIPULATION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.


# Retained scoped evidence task

## P46 evidence task

Why can a low pixel residual coexist with a biased translation estimate?

Before running: Predict whether more visible landmarks can repair a focal-calibration error, and distinguish residual fit from actual pose accuracy.

Collect a default record, one single-control sweep, the named fault and recovery. Record the parameter values, plotted quantities and units so another learner can reproduce the comparison.

Observed and fitted pixels plots Image y (px) against Image x (px). Its series are Observed, Fitted. Pose-fit objective plots Half SSE (px²) against Iteration (count). Its series are Objective.

### Reasoning rubric

- Model: reconstruct a displayed value using `pixel_i=project(R*landmark_i+t); R in SO(3), t in metres` and the actual state or geometry.
- Evidence: Increase pixel-noise amplitude at a fixed landmark count. Compare actual translation, rotation and reprojection errors, and inspect the solver status instead of assuming every local fit has converged.
- Diagnosis: The estimator uses focal length 650 px for observations generated with 800 px. The actual selected points, pixel noise, initializer and positive-depth condition remain unchanged.
- Recovery and scope: Restore focal length 800 px, rerun from the declared initializer and compare the fitted transform, pixel residuals and local rank under the same observations. State this boundary: This solves a local six-degree-of-freedom pose from a near initializer and a synthetic noncoplanar object; it makes no global PnP uniqueness or arbitrary-initialization claim. The noise sequence is deterministic, visible points are selected by a fixed rule, and solver budget or stalling status remains meaningful even when two independent estimates agree closely.

### Check your explanation

Pose can compensate partly for incorrect focal calibration, and noisy data are fitted within the assumed model. Residual consistency is different from agreement with independent metric truth; inspect calibration, geometry and the full transform.

A complete explanation contains a calculation, an observed comparison with units, the executed fault and a reproduced recovery. Name a setting that can hide the fault and a claim requiring evidence outside this model. This is a self-assessment; no learner score is stored.
