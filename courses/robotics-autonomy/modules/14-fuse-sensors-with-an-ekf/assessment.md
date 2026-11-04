# P14 course checkpoint

## Predict and derive

Trace a wheel/absolute-position observation through EKF prediction and correction.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `x_minus=f(x,u), P_minus=F P F^T+Q`
- `K=P_minus H^T(H P_minus H^T+R)^-1`

## Controlled comparison

- Vary only `gps_noise_m` through [0.05, 0.25, 1.0]; predict Noisier GPS has less correction authority.
- Vary only `gps_interval_s` through [0.1, 0.5, 2.0]; predict Longer prediction spans produce larger uncertainty peaks.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

The motion Jacobian propagates pose covariance; an innovation changes state through its gain and must also update covariance.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Small error in one deterministic trajectory is not statistical consistency.

Competency links: STATE-ESTIMATION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
