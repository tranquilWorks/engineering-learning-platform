## P57 evidence task

At zero yaw and zero misalignment, does zero matrix residual prove that the fault is absent?

Before running: Predict whether a quaternion norm fault can escape a matrix check at zero total rotation.

Collect the default result, one single-control sweep, the named fault and recovery. Record controls and units beside the evidence.

World sensor vector plots World y component (1) against World x component (1). Its series are Reported compensated vector, Correct world vector, Alignment omitted. Rotation residuals plots Residual norm (1) against Yaw sweep (deg). Its series are Quaternion norm error, Orthogonality residual, Compensated vector error.

### Reasoning rubric

- Model: use `q=[w,x,y,z]; q_world_sensor=q_world_body ⊗ q_body_sensor` to reconstruct a quantity from the executed mechanism.
- Evidence: Sweep yaw through negative, zero and positive angles with alignment fixed. Compare the world-vector path and the sign of the x/y components; residuals should stay near roundoff in normal mode.
- Diagnosis: Broken mode multiplies the composed quaternion by 1.2 and feeds it to a formula that assumes unit norm, without normalization.
- Recovery and scope: Disable broken mode, restore defaults, and check norm, orthogonality and actual vector error together. State this limit: q and -q encode the same rotation. At identity the unit-quaternion matrix formula can return identity even for [1.2,0,0,0], so a matrix-only test can miss invalid quaternion norm. This is a static calibration/rotation exercise, not an attitude filter.

### Check your explanation

No. The scalar quaternion can have norm 1.2 while its vector part is zero; the assumed-unit matrix formula still yields identity. Inspect the quaternion norm and declare the formula precondition.

A complete answer includes the calculation or geometric construction, an observed comparison with units, fault/recovery evidence and the stated limitation. This is a self-assessment; no learner score is stored.
