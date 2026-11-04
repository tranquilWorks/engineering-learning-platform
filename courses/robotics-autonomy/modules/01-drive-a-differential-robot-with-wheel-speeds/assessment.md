# P01 course checkpoint

## Predict and derive

Predict straight motion, a left arc and pure spin from wheel speeds.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `v=r(omega_R+omega_L)/2`
- `Omega=r(omega_R-omega_L)/b`

## Controlled comparison

- Vary only `left_wheel_rad_s` through [-6, 6, 12]; predict Average and difference create spin, arc, and reversed curvature.
- Vary only `track_width_m` through [0.2, 0.35, 0.7]; predict A wider track reduces yaw rate for the same wheel-speed difference.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

The mean rim speed sets translation while the difference divided by track width sets yaw; world displacement must rotate with heading.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

No lateral slip or wheel-radius calibration error is estimated.

Competency links: MOBILE-KINEMATICS. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
