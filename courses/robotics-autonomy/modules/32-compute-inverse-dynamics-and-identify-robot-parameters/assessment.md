# P32 course checkpoint

## Predict and derive

Separate parameter fitting from held-out torque prediction.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `tau=0.08 qddot + [0.25 qddot+4.905 cos(q), qdot] theta`
- `theta_hat=argmin ||Y theta-y||²+0.02||theta-theta_prior||²`
- `heldout_error=tau_predicted-tau_true`

## Controlled comparison

- `excitation_amplitude_rad`: 0.7 → 1.5. Hold the other controls at baseline and explain the mechanism before executing.
- `payload_guess_kg`: 1.1 → 3.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Excitation determines regressor rank; fit residual and parameter error must be checked separately on new motion.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Low residual on an unexciting trajectory does not identify unique parameters.

Competency links: ROBOT-DYNAMICS. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.


# Retained scoped evidence task

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
