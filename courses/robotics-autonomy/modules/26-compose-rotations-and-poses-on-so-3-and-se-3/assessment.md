# P26 course checkpoint

## Predict and derive

Compare rigid pose composition with elementwise matrix interpolation.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `T=[R,t;0,1]; p_A=T_AB p_B`
- `T^-1=[R^T,-R^T t;0,1] only when R^T R=I`
- `R_blend(f)=(1-f)I+f Rz(theta)`

## Controlled comparison

- `rotation_angle_deg`: 35.0 → 170.0. Hold the other controls at baseline and explain the mechanism before executing.
- `translation_m`: 0.6 → 2.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Proper rotations preserve orthogonality and determinant one; translation and rotation composition generally do not commute.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A valid SE(3) matrix does not establish a correct sensor-frame convention.

Competency links: RIGID-BODY-GEOMETRY. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.


# Retained scoped evidence task

## P26 evidence task

Why can the final broken matrix pass both rotation checks while the lesson still reports a nonzero maximum defect?

Before running: Predict whether two valid rotation endpoints make every linear matrix blend between them a valid rotation.

Collect the default result, one single-control sweep, the named fault and recovery. Record controls and units beside the evidence.

Pose composition order plots World y coordinate (m) against World x coordinate (m). Its series are A after B, B after A. Rotation-group checks plots Rotation residual (1) against Composition fraction (1). Its series are Orthogonality error, Determinant error.

### Reasoning rubric

- Model: use `T=[R,t;0,1]; p_A=T_AB p_B` to reconstruct a quantity from the executed mechanism.
- Evidence: Sweep rotation angle from zero through 90 to 180 degrees at fixed translation. Inspect the entire fraction-dependent orthogonality curve in broken mode. Checking only the final matrix misses the invalid interior, because both endpoint rotations remain valid.
- Diagnosis: Broken mode linearly interpolates rotation matrices instead of constructing a rotation at each fractional angle.
- Recovery and scope: Restore angle-based rotation, reset defaults and check orthogonality, determinant and rigid-inverse point residual together. Keep the composition-order difference; making it vanish is not the recovery objective. State this limit: Zero rotation is a legitimate degenerate case in which the blend remains identity. Determinant one alone does not establish orthogonality. The x/y chart omits a spatial component, so compare retained three-dimensional vectors before inferring identical poses.

### Check your explanation

The blend equals the valid endpoint rotation at f=1. Interior blends generally leave SO(3); the metric deliberately measures the maximum over the executed interpolation, not just its last sample.

A complete answer includes the calculation or geometric construction, an observed comparison with units, fault/recovery evidence and the stated limitation. This is a self-assessment; no learner score is stored.
