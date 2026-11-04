## P28 evidence task

How do you distinguish a real position singularity from the omitted-column fault?

Before running: Predict what a missing elbow column does to task rank and to an independently differenced forward-kinematic check.

Collect the default result, one single-control sweep, the named fault and recovery. Record controls and units beside the evidence.

Position-task singular values plots Singular value (m/rad) against Elbow angle (deg). Its series are Largest, Smallest. Kinematic derivative check plots Jacobian difference (m/rad) against Elbow angle (deg). Its series are Central-difference residual.

### Reasoning rubric

- Model: use `x=l1 cos(q1)+l2 cos(q1+q2); y=l1 sin(q1)+l2 sin(q1+q2); l1=1 m` to reconstruct a quantity from the executed mechanism.
- Evidence: Sweep elbow angle from zero to 70 and then 175 degrees at fixed link ratio. Compare the smallest singular value near straight and nearly folded configurations. The graph covers every intermediate sampled elbow angle, so its starting point is singular even when the selected endpoint is not.
- Diagnosis: Broken mode omits the elbow Jacobian column while leaving the forward kinematics unchanged. The computed Jacobian loses a joint contribution and the finite-difference residual exposes it.
- Recovery and scope: Restore the second column, reset controls and compare both derivative agreement and task singular values. A small singular value at a truly aligned configuration is expected and should not be repaired by adding an arbitrary floor. State this limit: At elbow zero the correct position map is singular. The shoulder angle rotates the task axes without changing singular values. A derivative check has truncation and floating-point error; exact symbolic zero is not required. No orientation or dynamics claim follows from this position-only calculation.

### Check your explanation

At a real aligned configuration the correct analytic Jacobian still agrees with independently differentiated kinematics. The omitted column disagrees with a nonzero elbow derivative and causes rank loss even away from geometric alignment.

A complete answer includes the calculation or geometric construction, an observed comparison with units, fault/recovery evidence and the stated limitation. This is a self-assessment; no learner score is stored.
