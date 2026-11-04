# P07 course checkpoint

## Predict and derive

Compute endpoint velocity and acceleration for the displayed trajectory.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `s(tau)=10tau^3-15tau^4+6tau^5`
- `x=Ds, dx/dt=(D/T)s', d2x/dt2=(D/T^2)s''`

## Controlled comparison

- Vary only `distance_m` through [0.5, 2, 4]; predict All dimensional outputs scale with distance.
- Vary only `duration_s` through [1.5, 4, 8]; predict Velocity scales as 1/T and acceleration as 1/T^2.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Differentiate the interpolation polynomial and check endpoints, extrema and physical units; sample spacing alone does not guarantee smooth motion.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A smooth reference can exceed actuator acceleration or torque limits.

Competency links: GLOBAL-MOTION-PLANNING. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
