# P27 course checkpoint

## Predict and derive

Preserve mechanical power while changing twist and wrench frames.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `V=[omega;v]; W=[moment;force]; power=W^T V`
- `Ad_T=[[R,0],[[t]cross R,R]]; V_A=Ad_T V_B`
- `W_A=Ad_T^-T W_B; pitch=omega·v/(omega·omega)`

## Controlled comparison

- `lever_arm_m`: 0.45 → 1.5. Hold the other controls at baseline and explain the mechanism before executing.
- `angular_speed_rad_s`: 1.8 → 6.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Angular and linear velocity transform together with the lever-arm term; the dual wrench map preserves their scalar power product.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Omitting translation can remain hidden when force or angular velocity is zero.

Competency links: RIGID-BODY-GEOMETRY. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.


# Retained scoped evidence task

## P27 evidence task

Why can the twist round-trip check pass while power invariance fails, and what is the default source power?

Before running: Predict which transform preserves the scalar power pairing when the frame origin is translated.

Collect the default result, one single-control sweep, the named fault and recovery. Record controls and units beside the evidence.

Transformed linear velocity plots Linear velocity (m/s) against Transform fraction (1). Its series are vx, vy, vz. Dual-transform power plots Power (W) against Transform fraction (1). Its series are Transformed power, Original power.

### Reasoning rubric

- Model: use `V=[omega;v]; W=[moment;force]; power=W^T V` to reconstruct a quantity from the executed mechanism.
- Evidence: Increase lever arm while holding angular speed fixed. The transformed linear velocity and moment change, yet normal power stays at the source value. In broken mode compare the power discrepancy across the whole frame sweep rather than only its starting frame.
- Diagnosis: Broken mode applies the motion adjoint directly to the wrench instead of its inverse transpose. It still performs the correct twist transformation and round-trip motion check.
- Recovery and scope: Restore the dual wrench transformation, reset both controls and compare the two power curves. The motion round-trip residual can remain tiny in both modes, so it alone cannot diagnose the wrench fault. State this limit: At zero transform fraction the adjoint is identity and the wrong wrench map can coincide with the correct map. Zero power discrepancy at one frame is insufficient. Pure translation has no finite pitch under this formula, and this lab deliberately keeps angular speed positive.

### Check your explanation

The twist and its inverse map can be correct while the wrench uses the wrong dual map. The default pairing is 0.54+0.4-0.3+0.05=0.69 W. Correct power invariance checks both sides of the dual relationship.

A complete answer includes the calculation or geometric construction, an observed comparison with units, fault/recovery evidence and the stated limitation. This is a self-assessment; no learner score is stored.
