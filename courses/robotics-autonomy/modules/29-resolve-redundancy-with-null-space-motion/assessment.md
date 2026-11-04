# P29 course checkpoint

## Predict and derive

Separate desired task velocity from secondary null-space motion.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `qdot_primary=J^T(JJ^T+lambda²I)^-1 v_desired`
- `N=I-Jplus J; qdot_secondary=-gain N q`
- `qdot=qdot_primary+qdot_secondary; leakage=||J qdot_secondary||`

## Controlled comparison

- `damping`: 0.08 → 0.5. Hold the other controls at baseline and explain the mechanism before executing.
- `null_gain_per_s`: 0.6 → 2.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

The projector should suppress the secondary task-space contribution; damping alters the primary inverse and its residual.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Large finite integration steps can invalidate an instantaneous null-space argument.

Competency links: MANIPULATOR-KINEMATICS. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.


# Retained scoped evidence task

## P29 evidence task

Why can the total task residual be nonzero while secondary leakage is essentially zero?

Before running: Predict whether primary damping requires secondary posture motion to leak into the task when an exact null projector is used.

Collect the default result, one single-control sweep, the named fault and recovery. Record controls and units beside the evidence.

Instantaneous joint commands plots Joint velocity (rad/s) against Posture gain (1/s). Its series are Joint 1, Joint 2, Joint 3. Resulting task velocity plots Task velocity (m/s) against Posture gain (1/s). Its series are Actual x, Actual y, Desired x, Desired y.

### Reasoning rubric

- Model: use `qdot_primary=J^T(JJ^T+lambda²I)^-1 v_desired` to reconstruct a quantity from the executed mechanism.
- Evidence: Increase primary damping from zero to 0.5 while holding posture gain fixed. Compare task velocity residual and joint speed. Secondary leakage should remain near roundoff in normal mode because the exact projector is independent of primary damping.
- Diagnosis: Broken mode bypasses the null projector and adds minus gain times the full posture vector to the primary command.
- Recovery and scope: Restore the exact projector and defaults. Check actual task velocity, secondary leakage and joint velocity together; a low total joint speed alone cannot certify task preservation. State this limit: At zero gain both modes coincide because no secondary motion is requested. At zero damping the full-row-rank primary inverse tracks the desired task to roundoff. The null projector is local to one configuration; finite motion requires recomputing it. No joint limits, collision constraints or integrated posture trajectory are claimed.

### Check your explanation

The damped primary inverse trades tracking accuracy against joint speed. An exact null projector preserves that primary task velocity when posture motion is added; it does not undo the original damping residual.

A complete answer includes the calculation or geometric construction, an observed comparison with units, fault/recovery evidence and the stated limitation. This is a self-assessment; no learner score is stored.
