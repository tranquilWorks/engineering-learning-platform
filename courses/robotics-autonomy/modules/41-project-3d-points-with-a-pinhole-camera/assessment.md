# P41 course checkpoint

## Predict and derive

Predict pixel motion from depth and camera pose.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `p_camera=R^T(p_world-camera_origin)`
- `u=f X/Z; v=f Y/Z, accepted only when Z>0.05 m`
- `depth_sensitivity=f sqrt(X²+Y²)/Z²`

## Controlled comparison

- `focal_length_px`: 520.0 → 1200.0. Hold the other controls at baseline and explain the mechanism before executing.
- `point_depth_m`: 3.0 → 12.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Perspective division follows the camera frame; points behind or too near the image plane require explicit handling.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A pinhole model excludes lens distortion and rolling shutter.

Competency links: VISION-PERCEPTION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.


# Retained scoped evidence task

## P41 evidence task

Why can the faulty projection report zero invalid accepted rays and still be wrong?

Before running: Predict why a positive world height is insufficient to decide whether a point lies in front of a rotated camera.

Collect a default record, one single-control sweep, the named fault and recovery. Record the parameter values, plotted quantities and units so another learner can reproduce the comparison.

Projection over depth plots Image x (px) against World depth (m). Its series are Projection. Camera-frame depths plots Camera depth (m) against World x (m). Its series are Depth, Near plane.

### Reasoning rubric

- Model: reconstruct a displayed value using `p_camera=R^T(p_world-camera_origin)` and the actual state or geometry.
- Evidence: Increase focal length at fixed world-cloud depth. Accepted point count stays unchanged, while pixel radius and depth sensitivity scale linearly. Explain why focal length does not decide front-versus-behind geometry.
- Diagnosis: The fault omits camera translation and rotation, using world coordinates for projection and acceptance. Invalid accepted rays are counted against the correctly transformed physical geometry.
- Recovery and scope: Restore the world-to-camera transform and compare accepted rays, pixel locations and reprojection residual. A zero invalid-ray count alone does not certify a calibrated projection. State this boundary: At an empty accepted set, zero-valued projection summaries are unavailable sentinels, not visible on-axis points. A far cloud may hide the faulty visibility count while retaining wrong pixels. The model excludes lens distortion, occlusion, image bounds, calibration uncertainty and camera noise.

### Check your explanation

All points may genuinely lie in front of the camera while the omitted translation and rotation still change their ray directions and pixels. Visibility is only one condition; coordinate transformation and reprojection agreement must also be checked.

A complete explanation contains a calculation, an observed comparison with units, the executed fault and a reproduced recovery. Name a setting that can hide the fault and a claim requiring evidence outside this model. This is a self-assessment; no learner score is stored.
