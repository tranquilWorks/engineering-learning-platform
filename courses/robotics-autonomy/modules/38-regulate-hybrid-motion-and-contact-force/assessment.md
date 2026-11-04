# P38 course checkpoint

## Predict and derive

Separate tangential motion control from normal contact-force control.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `n=[-sin(theta),cos(theta)]; t=[cos(theta),sin(theta)]`
- `P_force=n n^T; P_motion=I-P_force`
- `F=600 max(n^T x,0); xdot=P_motion(v_t+5(x_goal-x))+n*0.012(F_goal-F)`

## Controlled comparison

- `force_setpoint_n`: 12.0 → 40.0. Hold the other controls at baseline and explain the mechanism before executing.
- `surface_angle_deg`: 25.0 → 80.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Projection must respect the surface frame, and unilateral contact prevents tensile wall force when separation occurs.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A fixed planar surface omits changing contact normals and frictional slip.

Competency links: PHYSICAL-INTERACTION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.


# Retained scoped evidence task

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
