# Build a Planar Position Jacobian and Diagnose Singularities



## Model, derivation, and conventions

`x=l1 cos(q1)+l2 cos(q1+q2); y=l1 sin(q1)+l2 sin(q1+q2); l1=1 m`

`J=partial(x,y)/partial(q1,q2); task_velocity=J joint_velocity`

`manipulability=sigma_max sigma_min=|det J|`

This is a two-link planar arm with proximal length one metre and distal length equal to the selected ratio times one metre. The shoulder is fixed at 0.4 rad for the configuration sweep, while the elbow ranges from zero to the selected angle in 121 samples. The task contains only end-effector x and y position. Therefore the computed Jacobian is a two-by-two position Jacobian with units m/rad. It is not a six-row spatial-twist Jacobian and does not assess all orientation capabilities. Narrowing that claim is essential: a position singularity and rank loss of a full twist map are different questions.

Each column is the derivative of the same forward kinematics that defines the arm endpoint. The shoulder moves both links, so its column contains proximal and distal contributions. The elbow moves only the distal link, so its column contains the distal contribution. Multiplying by joint velocities in rad/s gives task velocity in m/s. The analytic Jacobian is checked against central differences of the endpoint, perturbing one joint at a time by 1e-5 rad. A small residual checks agreement between two calculations; it is not proof of a complete robot model or a claim that finite differences are exact.

For a hand example, choose shoulder zero, elbow 90 degrees and equal one-metre links. Then J=[[-1,-1],[1,0]] m/rad, with determinant one in m²/rad². A shoulder-only velocity [1,0] rad/s produces [-1,1] m/s, while elbow-only [0,1] produces [-1,0] m/s. The two columns are independent. At elbow zero both links align, the two columns become parallel and first-order radial position motion is unavailable. This geometric explanation should accompany the smallest singular value approaching zero.

The singular values quantify local velocity amplification under the stated coordinates and units. Their product is planar position manipulability, an area scaling in m²/rad². It is not dimensionless and is not a global reachability score. A long distal link can change both singular values even at the same elbow angle. Near a straight or folded arm, finite perturbations and numerical roundoff require care: the lesson reports finite singular values and derivative residuals without manufacturing a finite condition number by silently clipping infinity.

## Predict before running

Predict what a missing elbow column does to task rank and to an independently differenced forward-kinematic check.

## Baseline workflow

Reset controls and leave the named fault disabled. Use Elbow angle = 70.0 deg; Distal/proximal link ratio = 0.8 1. Write a prediction before executing. Read the response curve first, then explain it using the mechanism curve.

Position-task singular values plots Singular value (m/rad) against Elbow angle (deg). Its series are Largest, Smallest. Kinematic derivative check plots Jacobian difference (m/rad) against Elbow angle (deg). Its series are Central-difference residual.

The computed default record is Minimum position singular value: 0.465256 m/rad; Position manipulability: 0.751754 m^2/rad^2; Jacobian difference norm: 3.17367e-11 m/rad. These values are a reproducible worked example, not acceptance thresholds for every slider setting. Retain units and parameter values when comparing another run. A displayed residual near machine precision should be interpreted with the stated model and numerical tolerance.

## Two one-variable sweeps

1. Sweep elbow angle from zero to 70 and then 175 degrees at fixed link ratio. Compare the smallest singular value near straight and nearly folded configurations. The graph covers every intermediate sampled elbow angle, so its starting point is singular even when the selected endpoint is not.

2. Sweep link ratio from 0.2 to 1.5 with elbow fixed. Predict how the elbow column length changes, then compare singular values and manipulability. Keep the one-metre proximal length explicit when interpreting units.

Return to defaults between sweeps. Keep the other control fixed, record the changed quantity and identify an expected invariant. A control need not change every output; explain the model path through which it acts.

## Intentionally broken case

Broken mode omits the elbow Jacobian column while leaving the forward kinematics unchanged. The computed Jacobian loses a joint contribution and the finite-difference residual exposes it.

Run the same selected controls with the fault enabled. Compare the curve shape as well as the numerical summary. The fault is a specific executed operation; a red warning or a changed mode flag would not by itself demonstrate its consequence.

## Recovery

Restore the second column, reset controls and compare both derivative agreement and task singular values. A small singular value at a truly aligned configuration is expected and should not be repaired by adding an arbitrary floor.

Repeat one previously saved nominal setting and check that its values and curves return. Recovery should restore the mechanism, not merely dismiss the warning.

## Alternative and limiting cases

At elbow zero the correct position map is singular. The shoulder angle rotates the task axes without changing singular values. A derivative check has truncation and floating-point error; exact symbolic zero is not required. No orientation or dynamics claim follows from this position-only calculation.

## Independent evidence and MATLAB-style design boundary

The reference differentiates forward kinematics using complex steps and computes singular values from the two-by-two Gram matrix eigenvalues. It separately predicts the missing-column discrepancy instead of copying the production finite-difference array.

Five retained cases cover baseline, two single-control sweeps, the named fault and recovery. Expected values are generated independently; actual values come from the executable lesson. Absolute and relative tolerances remain 1e-8. Agreement checks the declared synthetic model, not empirical validity. MATLAB has not been executed and no MATLAB equivalence is claimed. Browser and container evidence are recorded separately from numerical evidence.

## Engineering review checklist

Check the declared coordinates, units and ordering before evaluating the result. Reconstruct at least one displayed value from retained state or geometric data. Identify which output changes in each sweep and which should remain invariant. Diagnose the named faulty operation, then demonstrate its recovery. Finally state the strongest claim supported by these observations and one claim that requires additional evidence.

## Common mistakes

Do not infer correctness from a changing headline alone. In this lesson, the critical limit is: At elbow zero the correct position map is singular. The shoulder angle rotates the task axes without changing singular values. A derivative check has truncation and floating-point error; exact symbolic zero is not required. No orientation or dynamics claim follows from this position-only calculation.

Do not compare two runs after changing both controls and attribute the difference to one cause. Do not treat a near-zero floating-point residual as symbolic identity, or a finite sample sweep as a proof for all configurations. Keep the operation that creates the evidence separate from the interpretation assigned to it.

## Focused check and teach-back

How do you distinguish a real position singularity from the omitted-column fault?

Answer rationale: At a real aligned configuration the correct analytic Jacobian still agrees with independently differentiated kinematics. The omitted column disagrees with a nonzero elbow derivative and causes rank loss even away from geometric alignment.

Use the embedded Course checkpoint to collect a default record, a sweep, a faulty record and a recovered record. Explain the evidence to a colleague using the governing relation and units, then name the untested boundary. This is a self-assessment; no learner score is stored.
