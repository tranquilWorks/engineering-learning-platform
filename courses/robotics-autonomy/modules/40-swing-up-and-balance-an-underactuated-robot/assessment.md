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


# Retained scoped evidence task

## P40 evidence task

What makes this plant underactuated, and why is a captured body insufficient to claim a practical balanced robot?

Before running: Predict why reversing the energy-pumping sign prevents the default pendulum from reaching the capture region.

Collect a default record, one single-control sweep, the named fault and recovery. Record the parameter values, plotted quantities and units so another learner can reproduce the comparison.

Reaction-wheel swing-up plots Angle error (rad) against Time (s). Its series are Body error, Upright. Pendulum body energy plots Body energy (J) against Time (s). Its series are Body energy, Target.

### Reasoning rubric

- Model: reconstruct a displayed value using `I_body*theta_ddot+g_moment*sin(theta)=tau_body` and the actual state or geometry.
- Evidence: Increase energy gain at fixed motor limit. Compare actual applied torque, energy growth and capture time. Once torque saturates, requested energy injection no longer scales freely with gain.
- Diagnosis: The fault reverses the swing-up energy term. It still applies equal and opposite motor torques and uses the same state-dependent capture condition; the default run then fails to reach capture.
- Recovery and scope: Restore the energy-pumping sign and reset the initial state. Verify the computed capture event, subsequent balance mode and body/wheel trajectories. State this boundary: Exactly downward at zero rate, this energy law cannot initiate motion without a perturbation. No capture within twelve seconds is censored evidence, not a proof of impossibility. Wheel speed and position are unregulated and unlimited; successful body capture is not hardware qualification.

### Check your explanation

Two rotational coordinates share one equal-and-opposite internal motor torque. Capturing the body can leave substantial wheel motion; the model lacks wheel-speed and momentum limits, so body tracking alone cannot establish actuator feasibility.

A complete explanation contains a calculation, an observed comparison with units, the executed fault and a reproduced recovery. Name a setting that can hide the fault and a claim requiring evidence outside this model. This is a self-assessment; no learner score is stored.
