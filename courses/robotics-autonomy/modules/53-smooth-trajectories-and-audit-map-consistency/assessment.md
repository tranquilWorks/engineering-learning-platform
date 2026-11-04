# P53 course checkpoint

## Predict and derive

Distinguish a backward smoother from a causal filter with smaller error bars.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `C_k=P_k^f F^T(P_{k+1}^-)^-1 and x_k^s=x_k^f+C_k(x_{k+1}^s-x_{k+1}^-)`
- `P_k^s=P_k^f+C_k(P_{k+1}^s-P_{k+1}^-)C_k^T`
- `NEES=e^T P^-1 e and held-out fixes audit covariance and map consistency`

## Controlled comparison

- `process_noise`: 0.06 → 0.5. Hold the other controls at baseline and explain the mechanism before executing.
- `measurement_noise`: 0.15 → 1.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Future measurements affect past states through the smoothing gain; held-out observations audit errors separately from fitting.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

One deterministic trajectory cannot establish probabilistic covariance coverage.

Competency links: STATE-ESTIMATION, SLAM-MAPPING. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
