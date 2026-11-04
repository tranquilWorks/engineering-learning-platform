## P31 evidence task

Why does a positive minimum inertia eigenvalue not prove that the velocity forces are correct?

Before running: Predict whether positive inertia alone can reveal a missing Coriolis coupling.

Collect a default record, one single-control sweep, the named fault and recovery. Record the parameter values, plotted quantities and units so another learner can reproduce the comparison.

Joint inertia eigenvalues plots Inertia (kg·m²) against Elbow angle (rad). Its series are Min eig, Max eig. Joint gravity torques plots Torque (N·m) against Elbow angle (rad). Its series are Joint 1, Joint 2.

### Reasoning rubric

- Model: reconstruct a displayed value using `M(q) qddot+C(q,qdot) qdot+g(q)=tau` and the actual state or geometry.
- Evidence: Increase payload at fixed elbow angle. Compare both inertia eigenvalues and the shoulder gravity component. The normal skew defect stays near roundoff even though the underlying mass derivative and Coriolis entries grow.
- Diagnosis: The fault removes C12 while preserving the physical mass and gravity calculations. The symmetric part of Mdot-2C therefore measures an executed missing coupling.
- Recovery and scope: Restore C12 and repeat the bent-pose comparison. Check positive eigenvalues, the skew identity and the gravity vector separately. State this boundary: At elbow zero or pi the omitted sine coupling vanishes, so this fault can be locally hidden. The point-mass model excludes distributed link inertia, friction, elasticity and motor dynamics; it is an instantaneous identity check, not a trajectory experiment.

### Check your explanation

Positive inertia certifies the kinetic-energy quadratic form. A missing C entry leaves that form unchanged while breaking the skew identity at a bent moving configuration. The tests constrain different parts of the dynamics.

A complete explanation contains a calculation, an observed comparison with units, the executed fault and a reproduced recovery. Name a setting that can hide the fault and a claim requiring evidence outside this model. This is a self-assessment; no learner score is stored.
