# P36 course checkpoint

## Predict and derive

Compute operational-space inertia and diagnose singular directions.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `Lambda=(J M^-1 J^T)^-1; Jbar=M^-1 J^T Lambda`
- `N_tau=I-J^T Jbar^T; tau_secondary=N_tau tau_raw`
- `xddot=J M^-1(tau_primary+tau_secondary)`

## Controlled comparison

- `task_inertia_kg`: 2.0 → 8.0. Hold the other controls at baseline and explain the mechanism before executing.
- `jacobian_condition`: 5.0 → 30.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

The task inertia depends on both the Jacobian and joint inertia; null directions require explicit treatment rather than an unstable inverse.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

The bounded example is not whole-body contact planning.

Competency links: ROBOT-DYNAMICS, ACTUATION-JOINT-CONTROL. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
