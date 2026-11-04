# P33 course checkpoint

## Predict and derive

Find the trajectory duration required by both speed and acceleration limits.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `q_i=d_i(3s²-2s³); s=t/T`
- `peak_speed=1.5 max|d_i|/T; peak_acceleration=6 max|d_i|/T²`
- `T=max(1.5 max|d_i|/v_limit, sqrt(6 max|d_i|/a_limit))`

## Controlled comparison

- `path_distance_rad`: 2.0 → 6.0. Hold the other controls at baseline and explain the mechanism before executing.
- `speed_limit_rad_s`: 1.2 → 4.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Time scaling changes first derivatives inversely with duration and second derivatives inversely with duration squared.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A sample-only extrema check may miss between-sample limit violations.

Competency links: ROBOT-DYNAMICS, GLOBAL-MOTION-PLANNING. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
