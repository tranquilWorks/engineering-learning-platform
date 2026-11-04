# P40 course checkpoint

## Predict and derive

Explain the energy-shaping and balance-control switching condition.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `I_body*theta_ddot+g_moment*sin(theta)=tau_body`
- `J_rotor*psi_ddot=-tau_body; E=0.5 I_body*theta_dot²+g_moment(1-cos(theta))`
- `tau_swing=k(E_target-E)*theta_dot/omega_reference²`

## Controlled comparison

- `energy_gain_per_s`: 1.4 → 4.0. Hold the other controls at baseline and explain the mechanism before executing.
- `torque_limit_n_m`: 2.2 → 6.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

The unactuated link receives energy through coupled dynamics; switching depends on angle and rate, not merely elapsed time.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A successful nominal swing-up is not a global stabilizing guarantee.

Competency links: ROBOT-DYNAMICS, ACTUATION-JOINT-CONTROL. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
