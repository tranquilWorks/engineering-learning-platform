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


# Retained scoped evidence task

## P48 evidence task

Why can an ICP run converge with a small residual and still have a wrong transform?

Before running: Predict whether a falling nearest-neighbour residual establishes correct registration when initialization is poor or correspondences include clutter.

Collect a default record, one single-control sweep, the named fault and recovery. Record the parameter values, plotted quantities and units so another learner can reproduce the comparison.

Registered point clouds plots World y (m) against World x (m). Its series are Target, Moved. ICP objective plots Mean cost (m²) against Update (count). Its series are Objective.

### Reasoning rubric

- Model: reconstruct a displayed value using `nearest_i=argmin_j ||R*source_i+t-target_j||` and the actual state or geometry.
- Evidence: Increase initial translation offset with outlier fraction fixed. Compare convergence status, objective descent and truth-based transform error; look for a finite wrong local fit or the maximum iteration budget.
- Diagnosis: The estimator disables the 0.5 m correspondence gate and includes every source point in each nearest-neighbour rigid fit.
- Recovery and scope: Restore the gate, restart from the same initial transform and compare the final rigid transform, accepted correspondence set and executed iteration history. State this boundary: The problem is planar SE(2), uses a fixed local initializer family and can reach a wrong local alignment or its iteration budget. Zero clutter can hide the rejection fault. A decreasing nearest-neighbour objective or tiny final increment does not establish the correct physical correspondence or a global optimum.

### Check your explanation

Nearest-neighbour assignments and rigid fitting optimize a local objective. A wrong correspondence pattern can be self-consistent and produce tiny updates; independent geometry, initialization limits and truth-based evaluation are separate checks.

A complete explanation contains a calculation, an observed comparison with units, the executed fault and a reproduced recovery. Name a setting that can hide the fault and a claim requiring evidence outside this model. This is a self-assessment; no learner score is stored.
