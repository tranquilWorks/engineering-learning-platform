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


# Retained scoped evidence task

## P33 evidence task

Why can increasing the allowed speed cease to shorten the move?

Before running: Predict why distance divided by the speed limit is too short for a rest-to-rest cubic trajectory.

Collect a default record, one single-control sweep, the named fault and recovery. Record the parameter values, plotted quantities and units so another learner can reproduce the comparison.

Synchronized velocities plots Velocity (rad/s) against Time (s). Its series are Joint 1, Joint 2, Speed +, Speed −. Joint accelerations plots Acceleration (rad/s²) against Time (s). Its series are Joint 1, Joint 2.

### Reasoning rubric

- Model: reconstruct a displayed value using `q_i=d_i(3s²-2s³); s=t/T` and the actual state or geometry.
- Evidence: Increase displacement while holding speed bound fixed. Compare the linear speed-duration requirement with the square-root acceleration-duration requirement; identify which one sets the applied time.
- Diagnosis: The fault applies a fixed one-second duration instead of the derived duration. It then differentiates the actual applied cubic, so speed and acceleration violations follow from the trajectory.
- Recovery and scope: Restore derived timing and inspect both speed and acceleration constraints. A small speed excess alone cannot certify acceleration feasibility. State this boundary: At zero displacement the trajectory is stationary; the interactive displacement range remains positive to keep a nonzero duration. A short move or generous limits can make one second feasible, so the named fault does not guarantee a violation at every setting. Endpoint acceleration is nonzero and torque limits are absent.

### Check your explanation

The acceleration requirement then sets the shared duration. For the fixed cubic, speed scales as 1/T while acceleration scales as 1/T²; both constraints must be satisfied, and the larger required time wins.

A complete explanation contains a calculation, an observed comparison with units, the executed fault and a reproduced recovery. Name a setting that can hide the fault and a claim requiring evidence outside this model. This is a self-assessment; no learner score is stored.
