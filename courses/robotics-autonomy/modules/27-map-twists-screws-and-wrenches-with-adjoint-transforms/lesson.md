# Transform Twists and Dual Wrenches with Power Invariance



## Model, derivation, and conventions

`V=[omega;v]; W=[moment;force]; power=W^T V`

`Ad_T=[[R,0],[[t]cross R,R]]; V_A=Ad_T V_B`

`W_A=Ad_T^-T W_B; pitch=omega·v/(omega·omega)`

A twist represents instantaneous rigid motion at a declared reference origin. This lesson orders its components as angular velocity followed by linear velocity. A wrench is the dual force object, ordered as moment followed by force. Angular velocity has units rad/s, linear velocity m/s, moment N m and force N. Their paired scalar is mechanical power in watts, treating radians as dimensionless in the power product. Adding angular and linear round-trip residuals into one unlabelled norm would hide their different physical dimensions, so the lesson reports linear residual in m/s and retains angular residual separately in rad/s.

The source twist is [0,0,speed,0.2,0.3,0.1]. The source wrench is [0.1,0.2,0.3,2,-1,0.5]. At the default speed 1.8 rad/s, source power is 0.3 times 1.8 plus 2 times 0.2 minus 0.3 plus 0.5 times 0.1, which equals 0.69 W. The linear velocity is specified at the source frame origin; translating the origin changes those components even when the physical motion is unchanged. At each of 121 fractions, the frame rotates about z by up to 60 degrees and translates by [lever times f,0.2 times lever times f,0] m. The motion adjoint includes the cross-product block formed from this translation.

The wrench must transform contragrediently: the inverse transpose of the motion map preserves the pairing. Expanding the formula gives force_A=R force_B and moment_A=R moment_B+t cross (R force_B). In contrast, motion uses omega_A=R omega_B and v_A=R v_B+t cross (R omega_B). These two block relationships are different because force and motion are dual quantities. Reusing the motion adjoint on a wrench mixes the wrong blocks and, interpreted physically, the wrong dimensions. That is the named fault, not an alternative convention silently switched midway through the lesson.

The screw pitch is omega dot v divided by squared angular speed. Here it equals 0.1/speed metres per radian. At speed 1.8 the pitch is approximately 0.05556 m/rad. The translated cross-product term is perpendicular to angular velocity, so it does not change this pitch. The speed slider excludes zero because this pitch expression is undefined for a pure translation.

## Predict before running

Predict which transform preserves the scalar power pairing when the frame origin is translated.

## Baseline workflow

Reset controls and leave the named fault disabled. Use Lever arm = 0.45 m; Angular speed = 1.8 rad/s. Write a prediction before executing. Read the response curve first, then explain it using the mechanism curve.

Transformed linear velocity plots Linear velocity (m/s) against Transform fraction (1). Its series are vx, vy, vz. Dual-transform power plots Power (W) against Transform fraction (1). Its series are Transformed power, Original power.

The computed default record is Maximum power discrepancy: 4.44089e-16 W; Linear round-trip residual: 2.00148e-16 m/s; Screw pitch: 0.0555556 m/rad. These values are a reproducible worked example, not acceptance thresholds for every slider setting. Retain units and parameter values when comparing another run. A displayed residual near machine precision should be interpreted with the stated model and numerical tolerance.

## Two one-variable sweeps

1. Increase lever arm while holding angular speed fixed. The transformed linear velocity and moment change, yet normal power stays at the source value. In broken mode compare the power discrepancy across the whole frame sweep rather than only its starting frame.

2. Increase angular speed while holding lever arm fixed. Recalculate source power and screw pitch. The correct power need not stay numerically equal to its previous run; it must stay invariant between frames within each run.

Return to defaults between sweeps. Keep the other control fixed, record the changed quantity and identify an expected invariant. A control need not change every output; explain the model path through which it acts.

## Intentionally broken case

Broken mode applies the motion adjoint directly to the wrench instead of its inverse transpose. It still performs the correct twist transformation and round-trip motion check.

Run the same selected controls with the fault enabled. Compare the curve shape as well as the numerical summary. The fault is a specific executed operation; a red warning or a changed mode flag would not by itself demonstrate its consequence.

## Recovery

Restore the dual wrench transformation, reset both controls and compare the two power curves. The motion round-trip residual can remain tiny in both modes, so it alone cannot diagnose the wrench fault.

Repeat one previously saved nominal setting and check that its values and curves return. Recovery should restore the mechanism, not merely dismiss the warning.

## Alternative and limiting cases

At zero transform fraction the adjoint is identity and the wrong wrench map can coincide with the correct map. Zero power discrepancy at one frame is insufficient. Pure translation has no finite pitch under this formula, and this lab deliberately keeps angular speed positive.

## Independent evidence and MATLAB-style design boundary

The reference uses complex planar rotations and explicit cross products for the separate force, moment, angular and linear components. It does not construct or invert the production adjoint matrix.

Five retained cases cover baseline, two single-control sweeps, the named fault and recovery. Expected values are generated independently; actual values come from the executable lesson. Absolute and relative tolerances remain 1e-8. Agreement checks the declared synthetic model, not empirical validity. MATLAB has not been executed and no MATLAB equivalence is claimed. Browser and container evidence are recorded separately from numerical evidence.

## Engineering review checklist

Check the declared coordinates, units and ordering before evaluating the result. Reconstruct at least one displayed value from retained state or geometric data. Identify which output changes in each sweep and which should remain invariant. Diagnose the named faulty operation, then demonstrate its recovery. Finally state the strongest claim supported by these observations and one claim that requires additional evidence.

## Common mistakes

Do not infer correctness from a changing headline alone. In this lesson, the critical limit is: At zero transform fraction the adjoint is identity and the wrong wrench map can coincide with the correct map. Zero power discrepancy at one frame is insufficient. Pure translation has no finite pitch under this formula, and this lab deliberately keeps angular speed positive.

Do not compare two runs after changing both controls and attribute the difference to one cause. Do not treat a near-zero floating-point residual as symbolic identity, or a finite sample sweep as a proof for all configurations. Keep the operation that creates the evidence separate from the interpretation assigned to it.

## Focused check and teach-back

Why can the twist round-trip check pass while power invariance fails, and what is the default source power?

Answer rationale: The twist and its inverse map can be correct while the wrench uses the wrong dual map. The default pairing is 0.54+0.4-0.3+0.05=0.69 W. Correct power invariance checks both sides of the dual relationship.

Use the embedded Course checkpoint to collect a default record, a sweep, a faulty record and a recovered record. Explain the evidence to a colleague using the governing relation and units, then name the untested boundary. This is a self-assessment; no learner score is stored.

Related primary reference: [Modern Robotics: wrenches and power invariance](https://modernrobotics.northwestern.edu/nu-gm-book-resource/3-4-wrenches/).
