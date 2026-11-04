# P52 course checkpoint

## Predict and derive

Explain why a plausible false loop can deform an entire map.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `objective=0.5*sum(||position_j-position_i-odometry_ij||²/sigma_odom²)+score*Huber(||closure_residual||/sigma_closure)`
- `Huber_weight=min(1,delta/||closure_residual||)`
- `position_0=[0,0]; appearance>=0.70 and innovation<=0.30 m admit a normal loop`

## Controlled comparison

- `descriptor_score`: 0.78 → 1.0. Hold the other controls at baseline and explain the mechanism before executing.
- `geometric_residual_m`: 0.12 → 2.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

A robust loss limits the loop's influence while odometry and the anchor resist deformation; inspect distributed map error.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Robust optimization does not make arbitrary false correspondences harmless.

Competency links: SLAM-MAPPING. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.


# Retained scoped evidence task

## P52 evidence task

Why are geometric rejection and a robust loss complementary rather than interchangeable?

Before running: Predict whether a high appearance score is enough to justify moving a map, and distinguish rejecting a loop from reducing the influence of an accepted loop.

Collect a default record, one single-control sweep, the named fault and recovery. Record the parameter values, plotted quantities and units so another learner can reproduce the comparison.

Anchored position graph plots World y (m) against World x (m). Its series are Baseline, Updated. Loop-induced displacement plots Displacement (m) against Node index (1). Its series are Shift.

### Reasoning rubric

- Model: reconstruct a displayed value using `objective=0.5*sum(||position_j-position_i-odometry_ij||²/sigma_odom²)+score*Huber(||closure_residual||/sigma_closure)` and the actual state or geometry.
- Evidence: Increase appearance score while holding innovation fixed, including values on both sides of 0.70. Separate the discrete insertion decision from the continuous influence of an accepted factor.
- Diagnosis: The system keeps the appearance gate but skips geometric rejection and replaces robust closure influence with a quadratic loss. Both selected controls and all odometry factors remain intact.
- Recovery and scope: Restore geometric gating and Huber influence, solve again from the same odometry graph and confirm the anchor, residuals and node displacements. State this boundary: This is an anchored two-dimensional translation graph with an externally supplied appearance score, not full rotational SLAM or image-based loop recognition. Rejected factors and zero innovation leave the baseline unchanged. A robust loss limits damage but does not prove that an accepted factor identifies the correct physical place.

### Check your explanation

A gate decides whether a factor enters the graph at all; a robust loss controls how an inserted factor influences the fitted states. Neither alone proves place identity, and a high appearance score cannot replace geometric consistency.

A complete explanation contains a calculation, an observed comparison with units, the executed fault and a reproduced recovery. Name a setting that can hide the fault and a claim requiring evidence outside this model. This is a self-assessment; no learner score is stored.
