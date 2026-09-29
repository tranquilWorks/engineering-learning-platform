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
