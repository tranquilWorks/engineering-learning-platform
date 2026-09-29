# Compose Quaternions and Calibrate Sensor Vectors



## Model and equations

`q=[w,x,y,z]; q_world_sensor=q_world_body ⊗ q_body_sensor`

`q_normalized=q/||q||; R(q)^T R(q)=I for unit q`

`v_world=R(q_world_sensor)v_sensor`

Use scalar-first Hamilton quaternions and active column-vector rotations. Sensor-to-body alignment rotates about body x; body-to-world yaw rotates about world z. Composition applies alignment first and yaw second. The known body vector is [0.4,0.7,0.2], a dimensionless calibration direction. Its sensor coordinates are obtained by the inverse alignment. Each of 121 yaw samples constructs both quaternions, multiplies them, normalizes the product, converts it to a matrix and transforms the sensor vector. At yaw 90 degrees and zero misalignment the correct vector is [-0.7,0.4,0.2]. Ignoring nonzero alignment changes the vector even when the yaw rotation is otherwise valid. Thus a small orthogonality residual cannot certify sensor calibration. The displayed uncalibrated comparison measures a different failure from the active norm fault.

## Predict before running

Predict whether a quaternion norm fault can escape a matrix check at zero total rotation.

## Baseline workflow

Reset controls and leave the named fault disabled. Use Yaw angle = 35.0 deg; Sensor misalignment = 3.0 deg. Write a prediction before executing. Read the response curve first, then explain it using the mechanism curve.

World sensor vector plots World y component (1) against World x component (1). Its series are Reported compensated vector, Correct world vector, Alignment omitted. Rotation residuals plots Residual norm (1) against Yaw sweep (deg). Its series are Quaternion norm error, Orthogonality residual, Compensated vector error.

The computed default record is Final quaternion norm error: 0 1; Final rotation orthogonality error: 2.81889e-16 1; Final compensated vector error: 1.14439e-16 1; Error without sensor alignment: 0.0381142 1. These values are a reproducible worked example, not acceptance thresholds for every slider setting. Retain units and parameter values when comparing another run. A displayed residual near machine precision should be interpreted with the stated model and numerical tolerance.

## Two one-variable sweeps

1. Sweep yaw through negative, zero and positive angles with alignment fixed. Compare the world-vector path and the sign of the x/y components; residuals should stay near roundoff in normal mode.

2. Sweep misalignment from zero to 20 degrees with yaw fixed. The correctly compensated vector remains consistent while the uncalibrated comparison changes. This useful invariance is evidence that calibration is being applied.

Return to defaults between sweeps. Keep the other control fixed, record the changed quantity and identify an expected invariant. A control need not change every output; explain the model path through which it acts.

## Intentionally broken case

Broken mode multiplies the composed quaternion by 1.2 and feeds it to a formula that assumes unit norm, without normalization.

Run the same selected controls with the fault enabled. Compare the curve shape as well as the numerical summary. The fault is a specific executed operation; a red warning or a changed mode flag would not by itself demonstrate its consequence.

## Recovery

Disable broken mode, restore defaults, and check norm, orthogonality and actual vector error together.

Repeat one previously saved nominal setting and check that its values and curves return. Recovery should restore the mechanism, not merely dismiss the warning.

## Limiting cases and invariants

q and -q encode the same rotation. At identity the unit-quaternion matrix formula can return identity even for [1.2,0,0,0], so a matrix-only test can miss invalid quaternion norm. This is a static calibration/rotation exercise, not an attitude filter.

## Independent evidence

The reference constructs independent axis rotations using rotation vectors and applies R_fault=I+1.2²(R_true-I). This identity tests the scaled-quaternion defect without calling the production quaternion functions.

Five retained cases cover baseline, two single-control sweeps, the named fault and recovery. Expected values are generated independently; actual values come from the executable lesson. Absolute and relative tolerances remain 1e-8. Agreement checks the declared synthetic model, not empirical validity. MATLAB has not been executed and no MATLAB equivalence is claimed. Browser and container evidence are recorded separately from numerical evidence.

## Engineering review checklist

Check the declared coordinates, units and ordering before evaluating the result. Reconstruct at least one displayed value from retained state or geometric data. Identify which output changes in each sweep and which should remain invariant. Diagnose the named faulty operation, then demonstrate its recovery. Finally state the strongest claim supported by these observations and one claim that requires additional evidence.

## Common mistakes

Do not infer correctness from a changing headline alone. In this lesson, the critical limit is: q and -q encode the same rotation. At identity the unit-quaternion matrix formula can return identity even for [1.2,0,0,0], so a matrix-only test can miss invalid quaternion norm. This is a static calibration/rotation exercise, not an attitude filter.

Do not compare two runs after changing both controls and attribute the difference to one cause. Do not treat a near-zero floating-point residual as symbolic identity, or a finite sample sweep as a proof for all configurations. Keep the operation that creates the evidence separate from the interpretation assigned to it.

## Teach-back

At zero yaw and zero misalignment, does zero matrix residual prove that the fault is absent?

Answer rationale: No. The scalar quaternion can have norm 1.2 while its vector part is zero; the assumed-unit matrix formula still yields identity. Inspect the quaternion norm and declare the formula precondition.

Use the embedded Course checkpoint to collect a default record, a sweep, a faulty record and a recovered record. Explain the evidence to a colleague using the governing relation and units, then name the untested boundary. This is a self-assessment; no learner score is stored.
