## P36 evidence task

Why is J times secondary torque equal to zero the wrong condition for preserving task acceleration?

Before running: Predict whether a torque in the Euclidean null space of J necessarily produces zero task acceleration.

Collect a default record, one single-control sweep, the named fault and recovery. Record the parameter values, plotted quantities and units so another learner can reproduce the comparison.

Resulting task acceleration plots Acceleration (m/s²) against Torque fraction (1). Its series are Actual x, Actual y. Directional task inertia plots Inertia (kg) against Task direction (rad). Its series are Inertia.

### Reasoning rubric

- Model: reconstruct a displayed value using `Lambda=(J M^-1 J^T)^-1; Jbar=M^-1 J^T Lambda` and the actual state or geometry.
- Evidence: Increase link mass scale at fixed geometry. The operational inertia scales with mass. The same raw secondary torque has less acceleration effect as mass grows, while correct primary compensation still requests the selected task acceleration.
- Diagnosis: The fault projects secondary torque with a Euclidean velocity-null projector. It preserves the raw torque, physical inertia and primary task command, then computes the resulting acceleration.
- Recovery and scope: Restore the dynamically consistent torque projector and compare acceleration with and without the secondary torque. Check J M inverse tau_secondary directly. State this boundary: At zero secondary fraction both modes reduce to the same primary task command. This is a local zero-velocity calculation with exact gravity compensation. A moving task requires Jdot*qdot, updated geometry and an actual trajectory controller.

### Check your explanation

Torque is converted to joint acceleration through M inverse. At zero velocity the task effect is J M inverse tau_secondary, so a torque projector must cancel that quantity. The Euclidean null condition applies directly to joint velocity, not arbitrary torque.

A complete explanation contains a calculation, an observed comparison with units, the executed fault and a reproduced recovery. Name a setting that can hide the fault and a claim requiring evidence outside this model. This is a self-assessment; no learner score is stored.
