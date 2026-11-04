# P11 course checkpoint

## Predict and derive

Separate a range-sensor blind zone from random-looking measurement variation.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `r=d/cos(theta)`
- `z=clip(r+n,0,r_max)`

## Controlled comparison

- Vary only `beam_angle_deg` through [0, 30, 60]; predict Slant range follows the secant curve.
- Vary only `noise_std_m` through [0, 0.02, 0.2]; predict Residual RMS grows while geometric bias remains identifiable.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Compare true distance, bias, saturation and invalid-return rules before summarizing residuals; an invalid return is not a physical zero range.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Synthetic perturbations do not identify a real sensor noise distribution.

Competency links: SENSOR-MODELING-CALIBRATION, RANGE-PERCEPTION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
