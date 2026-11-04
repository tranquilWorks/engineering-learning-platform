# P35 course checkpoint

## Predict and derive

Explain the effect of payload mismatch on computed-torque compensation.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `M(q) qddot+C(q,qdot) qdot+g(q)=tau_applied`
- `tau_requested=(1+epsilon)[M(a_d+2w(v_d-v)+w²(q_d-q))+Cv+g]`
- `tau_applied=clip(tau_requested,-20,20)`

## Controlled comparison

- `model_error_fraction`: 0.08 → 0.6. Hold the other controls at baseline and explain the mechanism before executing.
- `tracking_bandwidth_per_s`: 3.0 → 8.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Model cancellation uses inertia, coupling and gravity; feedback corrects residual error only within available effort.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Nominal cancellation is not robust to arbitrary model mismatch.

Competency links: ROBOT-DYNAMICS, ACTUATION-JOINT-CONTROL. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.


# Retained scoped evidence task

## P35 evidence task

Why can exact parameters still fail to produce the nominal critically damped tracking error?

Before running: Predict why increasing feedback bandwidth may not reduce tracking error when requested torques exceed actuator limits.

Collect a default record, one single-control sweep, the named fault and recovery. Record the parameter values, plotted quantities and units so another learner can reproduce the comparison.

Robot tracking errors plots Joint error (rad) against Time (s). Its series are Joint 1, Joint 2. Applied computed torque plots Torque (N·m) against Time (s). Its series are Joint 1, Joint 2.

### Reasoning rubric

- Model: reconstruct a displayed value using `M(q) qddot+C(q,qdot) qdot+g(q)=tau_applied` and the actual state or geometry.
- Evidence: Increase model mismatch at fixed bandwidth. Compare actual tracking, requested versus applied torques and gravity defect. Attribute changes to the controller model while preserving the physical plant.
- Diagnosis: The controller subtracts modeled gravity where it should add it. The physical plant, reference trajectory and actuator limits remain unchanged, and the resulting state is integrated.
- Recovery and scope: Restore the gravity sign, reset the same trajectory and compare state, applied torque and compensation defect. Keep mismatch visible rather than assuming restored gravity makes the model exact. State this boundary: At zero mismatch and without saturation, computed torque yields the derived linear error equation. At a pose with zero gravity contribution the sign fault is locally hidden; along a trajectory it can reappear. Torque clipping invalidates exact cancellation even with an otherwise correct model.

### Check your explanation

The derivation assumes the requested torque reaches the plant. Clipping changes that input and leaves an uncompensated acceleration. Compare requested and applied torque along the actual trajectory before applying the linear error equation.

A complete explanation contains a calculation, an observed comparison with units, the executed fault and a reproduced recovery. Name a setting that can hide the fault and a claim requiring evidence outside this model. This is a self-assessment; no learner score is stored.
