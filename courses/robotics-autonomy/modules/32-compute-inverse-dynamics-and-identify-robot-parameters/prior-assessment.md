## P32 evidence task

How can a rank-deficient experiment return a finite condition number and a unique fit?

Before running: Predict which parameter becomes unobservable when training measurements use a stationary joint.

Collect a default record, one single-control sweep, the named fault and recovery. Record the parameter values, plotted quantities and units so another learner can reproduce the comparison.

Training and test motion plots Joint angle (rad) against Time (s). Its series are Training, Held-out. Held-out torque prediction plots Torque (N·m) against Time (s). Its series are Predicted, Truth.

### Reasoning rubric

- Model: reconstruct a displayed value using `tau=0.08 qddot + [0.25 qddot+4.905 cos(q), qdot] theta` and the actual state or geometry.
- Evidence: Change the payload prior while holding excitation fixed. Compare fitted payload and held-out torque error. Strong data should reduce prior influence, but the ridge term means the result is not generally independent of the guess.
- Diagnosis: The fault replaces the training multisine with a stationary joint. Its damping regressor vanishes; the held-out experiment remains dynamic and unchanged.
- Recovery and scope: Restore the multisine and compare raw rank, fitted damping and held-out torque error. Do not repair the result by changing the held-out truth or labeling a finite regularized condition as full identifiability. State this boundary: Stationary samples cannot identify viscous damping because velocity is zero. The ridge solution depends on the stated units and prior; real identification also requires sensor calibration, suitable noise assumptions and a model of unmodeled dynamics.

### Check your explanation

The reported condition belongs to the regularized augmented system. Its prior supplies a numerical constraint on damping, but stationary training supplies no damping information. A dynamic held-out residual exposes that distinction.

A complete explanation contains a calculation, an observed comparison with units, the executed fault and a reproduced recovery. Name a setting that can hide the fault and a claim requiring evidence outside this model. This is a self-assessment; no learner score is stored.
