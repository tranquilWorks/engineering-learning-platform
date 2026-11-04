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
