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
