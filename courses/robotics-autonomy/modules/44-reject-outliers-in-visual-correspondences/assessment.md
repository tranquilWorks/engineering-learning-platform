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


# Retained scoped evidence task

## P44 evidence task

Why is a large consensus insufficient to prove that the recovered image motion is correct?

Before running: Predict why a low average residual over selected correspondences is insufficient without checking support and known synthetic model error.

Collect a default record, one single-control sweep, the named fault and recovery. Record the parameter values, plotted quantities and units so another learner can reproduce the comparison.

Match residuals plots Residual (px) against Match index (1). Its series are Residual, Limit. Observed displacements plots Vertical (px) against Horizontal (px). Its series are Matches, Fitted.

### Reasoning rubric

- Model: reconstruct a displayed value using `displacement_i=target_i-source_i; residual_i=||displacement_i-t_hat||` and the actual state or geometry.
- Evidence: Increase outlier fraction at a fixed threshold. Track support, actual translation error and false acceptance together; explain why a spread-out wrong-match distribution can remain rejectable even at high contamination.
- Diagnosis: The estimator replaces exhaustive consensus and inlier refitting with least squares over every observed displacement. The selected threshold remains active for evaluation.
- Recovery and scope: Restore consensus on the same data, then reconstruct the translation from the actual accepted displacements and inspect residuals on both genuine and wrong matches. State this boundary: The fitted motion is a two-dimensional translation and the search is exhaustive, not random RANSAC or general epipolar estimation. Zero outliers can hide the selection fault. Coherent wrong clusters, model mismatch and threshold choice can defeat consensus; the synthetic contamination fraction alone does not define a guarantee.

### Check your explanation

A wrong but coherent group can be larger than the genuine group, and an overly broad threshold can count incompatible displacements as support. Inspect the model family, residuals and independent truth or validation, not just the accepted fraction.

A complete explanation contains a calculation, an observed comparison with units, the executed fault and a reproduced recovery. Name a setting that can hide the fault and a claim requiring evidence outside this model. This is a self-assessment; no learner score is stored.
