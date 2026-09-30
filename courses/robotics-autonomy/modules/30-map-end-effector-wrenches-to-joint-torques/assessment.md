## P30 evidence task

Why can a matrix multiplication run successfully while producing the wrong joint torques?

Before running: Predict which mapping preserves virtual power throughout an elbow sweep, and whether zero force can expose the wrong mapping.

Collect a default record, one single-control sweep, the named fault and recovery. Record the parameter values, plotted quantities and units so another learner can reproduce the comparison.

Mapped joint torques plots Torque (N·m) against Elbow angle (rad). Its series are Joint 1, Joint 2. Virtual power check plots Power (W) against Elbow angle (rad). Its series are Joint, Cartesian.

### Reasoning rubric

- Model: reconstruct a displayed value using `v=J(q) qdot; tau=J(q)^T F` and the actual state or geometry.
- Evidence: Increase force magnitude while holding proximal length fixed. Torque and both power traces scale linearly. The unit-force gain stays unchanged, and normal power discrepancy remains near numerical roundoff.
- Diagnosis: The fault applies J F instead of J transpose F. Because this planar map happens to be square, the multiplication has compatible array dimensions and runs, but it violates the work duality.
- Recovery and scope: Restore the transpose, reset controls, and compare both power traces across every elbow sample. A single zero-power configuration is insufficient evidence. State this boundary: At zero force both torque maps produce zero, so the fault is unobservable through power. At zero length the ideal geometric torques vanish; the interactive length range remains positive. This is quasistatic mapping, with no inertia, friction or actuator model.

### Check your explanation

The square array dimensions do not enforce physical duality. Only J transpose maps Cartesian force into joint torque while preserving F dot (J qdot) = tau dot qdot. A zero-force trial cannot distinguish the maps.

A complete explanation contains a calculation, an observed comparison with units, the executed fault and a reproduced recovery. Name a setting that can hide the fault and a claim requiring evidence outside this model. This is a self-assessment; no learner score is stored.
