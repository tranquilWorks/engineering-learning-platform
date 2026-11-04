# P45 course checkpoint

## Predict and derive

Predict depth uncertainty as disparity approaches zero.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `point_hat=midpoint(closest_points_on_calibrated_rays)`
- `depth_truth=f*baseline/disparity; f=520 px`
- `Sigma_point=J_pixels*Sigma_pixels*J_pixels^T; sigma_Z=sqrt(Sigma_point[2,2])`

## Controlled comparison

- `baseline_m`: 0.18 → 0.8. Hold the other controls at baseline and explain the mechanism before executing.
- `disparity_px`: 28.0 → 140.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Triangulation couples baseline, focal scale and disparity; far-range depth becomes sensitive even when pixel residuals stay small.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A finite depth estimate does not prove positive depth in both cameras.

Competency links: VISION-PERCEPTION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
