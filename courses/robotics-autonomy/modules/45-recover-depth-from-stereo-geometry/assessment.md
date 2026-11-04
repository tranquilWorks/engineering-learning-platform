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


# Retained scoped evidence task

## P45 evidence task

Why can increasing baseline increase displayed depth uncertainty in this particular sweep?

Before running: Predict how depth and depth uncertainty change when baseline increases while the selected rectified disparity, rather than physical range, is held fixed.

Collect a default record, one single-control sweep, the named fault and recovery. Record the parameter values, plotted quantities and units so another learner can reproduce the comparison.

Triangulated depth plots Depth (m) against Disparity (px). Its series are Estimate, True. Pixel-noise uncertainty plots Depth sigma (m) against Disparity (px). Its series are Sigma, Selected.

### Reasoning rubric

- Model: reconstruct a displayed value using `point_hat=midpoint(closest_points_on_calibrated_rays)` and the actual state or geometry.
- Evidence: Increase baseline while holding selected rectified disparity fixed. Record the resulting change in scene depth and uncertainty, and explain why this is different from comparing two baselines viewing the same fixed-range point.
- Diagnosis: The triangulator treats the yawed right camera as parallel while preserving its actual observed pixels and the selected geometry. Reprojection is evaluated through the true camera poses.
- Recovery and scope: Restore the right-camera ray rotation, solve the closest-ray system again and verify both the reconstructed point and actual two-view residual. State this boundary: The deterministic estimate uses noiseless synthetic correspondences; its covariance is a first-order prediction under independent pixel noise, not an observed confidence interval. Positive disparity avoids the infinite-depth singularity but does not make low-disparity geometry well conditioned. Calibration uncertainty, matching errors and occlusion are excluded.

### Check your explanation

The control holds rectified disparity fixed, so increasing baseline also moves the constructed point farther away. The fixed-range precision benefit of a larger baseline answers a different experiment; the held variable must be stated.

A complete explanation contains a calculation, an observed comparison with units, the executed fault and a reproduced recovery. Name a setting that can hide the fault and a claim requiring evidence outside this model. This is a self-assessment; no learner score is stored.
