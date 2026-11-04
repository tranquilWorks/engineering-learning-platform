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
