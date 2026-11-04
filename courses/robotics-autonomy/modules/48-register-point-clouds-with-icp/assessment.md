# P48 course checkpoint

## Predict and derive

Separate nearest-neighbor association from rigid-transform fitting.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `nearest_i=argmin_j ||R*source_i+t-target_j||`
- `delta_R,delta_t=argmin sum_accepted ||delta_R*moved_i+delta_t-target_nearest_i||²`
- `R_next=delta_R*R; t_next=delta_R*t+delta_t`

## Controlled comparison

- `initial_offset_m`: 0.25 → 1.5. Hold the other controls at baseline and explain the mechanism before executing.
- `outlier_fraction`: 0.12 → 0.7. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

ICP alternates correspondences and pose updates; residual reduction depends on initialization and overlap.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A small local residual does not prove global registration correctness.

Competency links: RANGE-PERCEPTION, SLAM-MAPPING. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
