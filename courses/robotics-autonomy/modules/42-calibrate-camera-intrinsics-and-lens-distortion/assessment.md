# P42 course checkpoint

## Predict and derive

Compare calibration fit error with held-out reprojection error.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `u=f x+f k1 x(x²+y²)+cx; v=f y+f k1 y(x²+y²)+cy`
- `beta=[f,f*k1,cx,cy]; beta_hat=argmin ||A beta-pixels||²`
- `heldout_RMS=sqrt(mean(||predicted_pixel-true_pixel||²))`

## Controlled comparison

- `radial_k1`: -0.18 → 0.3. Hold the other controls at baseline and explain the mechanism before executing.
- `calibration_views`: 18.0 → 60.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Intrinsics and distortion must explain multiple board views; pose diversity matters more than repeating one view.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Synthetic board calibration does not validate a physical camera.

Competency links: SENSOR-MODELING-CALIBRATION, VISION-PERCEPTION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.


# Retained scoped evidence task

## P42 evidence task

Why can a low training error and an apparently sensible focal length still fail to establish a calibrated camera?

Before running: Predict whether adding more board views can eliminate held-out bias when the fitted model omits real radial distortion.

Collect a default record, one single-control sweep, the named fault and recovery. Record the parameter values, plotted quantities and units so another learner can reproduce the comparison.

Held-out residuals plots Residual (px) against Point index (1). Its series are Residual. Fitted radial model plots Radial factor (1) against Radius (1). Its series are True, Fitted.

### Reasoning rubric

- Model: reconstruct a displayed value using `u=f x+f k1 x(x²+y²)+cx; v=f y+f k1 y(x²+y²)+cy` and the actual state or geometry.
- Evidence: Change k1 while holding the number of views fixed. Compare held-out and outer-region errors in both modes, and include k1=0 to expose the case where removing distortion is physically appropriate.
- Diagnosis: The fit omits the radial-distortion column while the observations retain the selected lens distortion. No control value or measured residual is overwritten.
- Recovery and scope: Restore the full four-coefficient fit using the same observations. Confirm the held-out and outer-region residuals and reconstruct k1 from the fitted coefficient product. State this boundary: Known board poses and coordinates are exact; this does not perform joint pose/intrinsic calibration, feature extraction or real lens calibration. At zero radial distortion the omitted-column fault may be hidden. Deterministic noise, finite pose coverage, and conditioning limit generalization; more views do not guarantee monotonically smaller error.

### Check your explanation

An omitted radial term can be absorbed partly into focal length and principal point over the training geometry. Held-out rays, especially away from the optical centre, reveal the wrong spatial dependence; rank and coverage must also be checked.

A complete explanation contains a calculation, an observed comparison with units, the executed fault and a reproduced recovery. Name a setting that can hide the fault and a claim requiring evidence outside this model. This is a self-assessment; no learner score is stored.
