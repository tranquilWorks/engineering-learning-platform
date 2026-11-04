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
