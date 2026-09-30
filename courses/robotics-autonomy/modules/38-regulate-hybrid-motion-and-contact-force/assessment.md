## P38 evidence task

How can the projector algebra pass while hybrid motion and force regulation is still wrong?

Before running: Predict whether two perfectly orthogonal projectors can still be wrong for a tilted contact surface.

Collect a default record, one single-control sweep, the named fault and recovery. Record the parameter values, plotted quantities and units so another learner can reproduce the comparison.

Normal force feedback plots Normal force (N) against Time (s). Its series are Actual, Setpoint. Tangential motion plots Velocity (m/s) against Time (s). Its series are Actual, Desired.

### Reasoning rubric

- Model: reconstruct a displayed value using `n=[-sin(theta),cos(theta)]; t=[cos(theta),sin(theta)]` and the actual state or geometry.
- Evidence: Increase force goal at fixed surface angle. Compare terminal force and transient tangential speed. Correct projection preserves tangential tracking while normal displacement changes to support the new force.
- Diagnosis: The fault retains complementary orthogonal projectors but builds them from world vertical instead of the actual surface normal. Physical force is still measured along the real normal.
- Recovery and scope: Restore surface-aligned projectors and reset position. Check physical force and tangential velocity, then verify that the matrix alignment defect returns to roundoff. State this boundary: At zero surface angle world vertical and the physical normal coincide, so both modes agree. At zero force goal the unilateral contact may open in faulty mode. This ideal velocity-servo example omits impacts, robot inertia, sensor delay and actuator constraints.

### Check your explanation

Orthogonality describes the relation between the two chosen subspaces, not their alignment with the environment. World-axis projectors are internally orthogonal but mix real normal and tangential directions on a tilted surface.

A complete explanation contains a calculation, an observed comparison with units, the executed fault and a reproduced recovery. Name a setting that can hide the fault and a claim requiring evidence outside this model. This is a self-assessment; no learner score is stored.
