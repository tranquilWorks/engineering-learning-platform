# P44 course checkpoint

## Predict and derive

Reject outliers before refitting a geometric correspondence model.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `displacement_i=target_i-source_i; residual_i=||displacement_i-t_hat||`
- `consensus(t)={i: residual_i<=threshold}; t_refit=mean(displacement_consensus)`
- `false_acceptance=accepted_true_outliers/true_outlier_count`

## Controlled comparison

- `outlier_fraction`: 0.35 → 0.85. Hold the other controls at baseline and explain the mechanism before executing.
- `ransac_threshold_px`: 2.0 → 8.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Consensus counts compatible observations; a refit must use the selected inliers rather than all original matches.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A high inlier fraction can still support the wrong geometric model.

Competency links: VISION-PERCEPTION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
