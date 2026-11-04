# P50 course checkpoint

## Predict and derive

Separate gating from robust weighting of accepted residuals.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `d_j^2=nu_j^T S_j^-1 nu_j`
- `accept j only if d_j^2<=gamma`
- `rho_Huber(r)=r^2/2 for |r|<=delta, else delta(|r|-delta/2)`

## Controlled comparison

- `gate_sigma`: 3.0 → 8.0. Hold the other controls at baseline and explain the mechanism before executing.
- `outlier_sigma`: 5.0 → 12.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Mahalanobis distance tests compatibility; a Huber influence bound limits an accepted outlier without changing its units.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Two labeled candidates do not demonstrate general combinatorial association.

Competency links: STATE-ESTIMATION, SLAM-MAPPING. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
