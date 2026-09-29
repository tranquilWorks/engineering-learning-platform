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
