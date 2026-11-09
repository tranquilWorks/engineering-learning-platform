# P37 course checkpoint

## Predict and derive

Explain why a restoring static moment slope is insufficient, then test trim, both poles and an executed transient.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `F_y=mu F_z tanh(C_alpha alpha/(mu F_z))`
- `M_z=a F_yf-b F_yr`
- `S=-partial M_z/partial beta`

## Controlled comparison

- `steer_deg`: 6 → 9. Hold the other controls at baseline; predict and explain the change before executing.
- `friction_mu`: 1.15 → 0.8. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

A static moment slice holds yaw rate at an imposed value; it does not enforce beta_dot=0. A valid trim must simultaneously satisfy total lateral force=m*v*r and zero yaw moment. At r=0.2 rad/s and v=28 m/s, required total force is 8120 N, divided 4511.11 N front and 3608.89 N rear by moment balance. Evaluate the nonlinear effective slopes and both Jacobian eigenvalues only after checking trim validity. Compare the actual three-second trajectory and force utilization with the component slice; a domain cutoff is incomplete evidence, not recovery.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Stability is local to a valid trim of a constant-speed small-body-angle model. No global recoverability, spin prediction or measured-car qualification follows.

Competency links: VD-HANDLING-NONLINEAR. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
