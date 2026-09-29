# Compose Rigid Transforms and Diagnose Invalid Rotation Blends



## Model, derivation, and conventions

`T=[R,t;0,1]; p_A=T_AB p_B`

`T^-1=[R^T,-R^T t;0,1] only when R^T R=I`

`R_blend(f)=(1-f)I+f Rz(theta)`

A homogeneous transform maps a column of point coordinates between declared frames. Its top-left block is a dimensionless rotation matrix, its translation is in metres, and its bottom row is [0,0,0,1]. The point uses homogeneous coordinate one, so translation acts on it. A free direction would use coordinate zero and should not receive that translation. This distinction explains why frame transformations must be applied to actual geometric objects, rather than checked only by a determinant display.

The moving transform A uses a z rotation and a translation along y. At fraction f it rotates by f times the selected angle and translates by [0,f times distance,0]. The fixed transform B rotates 30 degrees about x and translates by [0,0.25,0.1] m. The source point is [0.3,0.2,0.4] m. The experiment evaluates ABp and BAp separately at 121 fractions. The chart displays their x/y projection, while retained diagnostics contain all three spatial coordinates. Under column-vector conventions AB applies B first, then A. The two paths generally differ because rigid transforms do not commute. Their final separation is an expected order effect, not a numerical accuracy error.

For a simple worked example, take a point [1,0,0] m, a 90-degree z rotation and translation [0,1,0] m. Rotating first and then translating gives [0,2,0] m. Translating first gives [1,1,0], and then rotating gives [-1,1,0] m. Each operation is valid, yet the results differ. This example isolates the order issue before interpreting the more complete fixed-x-rotation setup.

The fault replaces the rotation path by a linear blend of endpoint matrices while retaining the same translation path. At a 180-degree endpoint rotation and f=0.5, the x/y block collapses to zero. Its determinant is zero and its orthogonality defect is large even though f=0 and f=1 are valid rotations. A true matrix inverse, where one exists, is not the same as the rigid inverse formula when orthogonality fails. The experiment deliberately applies the rigid formula and measures the resulting point round-trip residual.

## Predict before running

Predict whether two valid rotation endpoints make every linear matrix blend between them a valid rotation.

## Baseline workflow

Reset controls and leave the named fault disabled. Use Rotation angle = 35.0 deg; Translation magnitude = 0.6 m. Write a prediction before executing. Read the response curve first, then explain it using the mechanism curve.

Pose composition order plots World y coordinate (m) against World x coordinate (m). Its series are A after B, B after A. Rotation-group checks plots Rotation residual (1) against Composition fraction (1). Its series are Orthogonality error, Determinant error.

The computed default record is Maximum rotation orthogonality error: 2.25194e-16 1; Maximum determinant error: 2.22045e-16 1; Final composition-order point difference: 0.3801 m. These values are a reproducible worked example, not acceptance thresholds for every slider setting. Retain units and parameter values when comparing another run. A displayed residual near machine precision should be interpreted with the stated model and numerical tolerance.

## Two one-variable sweeps

1. Sweep rotation angle from zero through 90 to 180 degrees at fixed translation. Inspect the entire fraction-dependent orthogonality curve in broken mode. Checking only the final matrix misses the invalid interior, because both endpoint rotations remain valid.

2. Sweep translation distance with rotation fixed. Rotation-group residuals should be unchanged because translation does not determine whether R belongs to SO(3). The composition-order point separation can change because the fixed x rotation acts on the y translation.

Return to defaults between sweeps. Keep the other control fixed, record the changed quantity and identify an expected invariant. A control need not change every output; explain the model path through which it acts.

## Intentionally broken case

Broken mode linearly interpolates rotation matrices instead of constructing a rotation at each fractional angle.

Run the same selected controls with the fault enabled. Compare the curve shape as well as the numerical summary. The fault is a specific executed operation; a red warning or a changed mode flag would not by itself demonstrate its consequence.

## Recovery

Restore angle-based rotation, reset defaults and check orthogonality, determinant and rigid-inverse point residual together. Keep the composition-order difference; making it vanish is not the recovery objective.

Repeat one previously saved nominal setting and check that its values and curves return. Recovery should restore the mechanism, not merely dismiss the warning.

## Alternative and limiting cases

Zero rotation is a legitimate degenerate case in which the blend remains identity. Determinant one alone does not establish orthogonality. The x/y chart omits a spatial component, so compare retained three-dimensional vectors before inferring identical poses.

## Independent evidence and MATLAB-style design boundary

The reference applies separate scalar x/z rotation formulas to coordinates and uses the analytic blend defect 2f(1-f)(1-cos(theta)). This independently checks the homogeneous-matrix implementation.

Five retained cases cover baseline, two single-control sweeps, the named fault and recovery. Expected values are generated independently; actual values come from the executable lesson. Absolute and relative tolerances remain 1e-8. Agreement checks the declared synthetic model, not empirical validity. MATLAB has not been executed and no MATLAB equivalence is claimed. Browser and container evidence are recorded separately from numerical evidence.

## Engineering review checklist

Check the declared coordinates, units and ordering before evaluating the result. Reconstruct at least one displayed value from retained state or geometric data. Identify which output changes in each sweep and which should remain invariant. Diagnose the named faulty operation, then demonstrate its recovery. Finally state the strongest claim supported by these observations and one claim that requires additional evidence.

## Common mistakes

Do not infer correctness from a changing headline alone. In this lesson, the critical limit is: Zero rotation is a legitimate degenerate case in which the blend remains identity. Determinant one alone does not establish orthogonality. The x/y chart omits a spatial component, so compare retained three-dimensional vectors before inferring identical poses.

Do not compare two runs after changing both controls and attribute the difference to one cause. Do not treat a near-zero floating-point residual as symbolic identity, or a finite sample sweep as a proof for all configurations. Keep the operation that creates the evidence separate from the interpretation assigned to it.

## Focused check and teach-back

Why can the final broken matrix pass both rotation checks while the lesson still reports a nonzero maximum defect?

Answer rationale: The blend equals the valid endpoint rotation at f=1. Interior blends generally leave SO(3); the metric deliberately measures the maximum over the executed interpolation, not just its last sample.

Use the embedded Course checkpoint to collect a default record, a sweep, a faulty record and a recovered record. Explain the evidence to a colleague using the governing relation and units, then name the untested boundary. This is a self-assessment; no learner score is stored.
