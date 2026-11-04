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
