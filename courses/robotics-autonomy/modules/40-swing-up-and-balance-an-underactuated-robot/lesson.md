# Swing Up and Capture a Reaction-Wheel Pendulum



## Model, derivation, and conventions

`I_body*theta_ddot+g_moment*sin(theta)=tau_body`

`J_rotor*psi_ddot=-tau_body; E=0.5 I_body*theta_dot²+g_moment(1-cos(theta))`

`tau_swing=k(E_target-E)*theta_dot/omega_reference²`

The plant is a reaction-wheel pendulum with two rotational degrees of freedom and one internal motor. Body inertia is 0.05 kg m², wheel inertia is 0.008 kg m², and the gravitational moment coefficient is 0.3*9.81*0.35 N m. Body angle theta is zero downward and pi upward. Production integrates body angle and rate together with absolute wheel angle psi and rate. The motor applies equal and opposite body and wheel torques, making the system genuinely underactuated rather than a fully actuated pendulum with an unused extra state.

The selected torque limit clips body torque symmetrically. Wheel torque is its negative, so internal actuation does not create net external angular momentum; gravity is the external torque. Eliminating absolute wheel acceleration gives I_body*theta_ddot=tau_body-g_moment*sin(theta) and J_rotor*psi_ddot=-tau_body. An equivalent formulation uses relative wheel angle phi=psi-theta and the coupled inertia matrix [[I_body+J_rotor,J_rotor],[J_rotor,J_rotor]]. The independent reference uses that second formulation.

Body energy is 0.5*I_body*theta_dot²+g_moment*(1-cos(theta)), and the upright rest target is twice the gravitational moment coefficient. The swing torque is gain times energy error times body rate, divided by a declared reference angular speed squared of (1 rad/s)². This normalization preserves the gain slider's inverse-second unit. Multiplying by body rate gives positive body-energy injection when energy is below target and the gain sign is correct. The exact downward rest state would not start moving because rate is zero, so the initial body rate is explicitly 0.15 rad/s; the absolute wheel starts at rest.

Capture is detected by an integration event, not by a scheduled switch. The body must be within 0.2 rad of upright and have absolute rate no greater than 1.5 rad/s. After entering that region, the controller switches to gravity compensation minus two times wrapped angle error minus 0.65 times body rate, still subject to the same torque limit. The event time is computed through the solver's continuous interpolation. The twelve-second observation horizon is reported as censored if no event occurs.

The first metric is capture time or the censored horizon, the second is terminal wrapped upright angle error, and the third is maximum absolute body-energy error over the whole record. That energy maximum includes the initial low-energy condition, so successful capture does not imply a small value. The plots and diagnostics retain body motion, wheel motion, motor torque, energy and control mode. The wheel's angle and speed are neither regulated nor limited in this model. A successful body balance therefore cannot certify a viable real reaction-wheel system without wheel speed, momentum capacity and actuator evidence.

## Predict before running

Predict why reversing the energy-pumping sign prevents the default pendulum from reaching the capture region. Record the expected direction of change and an invariant before reading the computed result. State a condition under which the fault could be hidden, rather than assuming every faulty setting must look worse.

## Baseline workflow

Reset controls and disable the named fault. Use Energy-shaping gain = 1.4 1/s; Actuator torque limit = 2.2 N*m. Read the response curve, then connect it to the mechanism curve using the governing equations.

Reaction-wheel swing-up plots Angle error (rad) against Time (s). Its series are Body error, Upright. Pendulum body energy plots Body energy (J) against Time (s). Its series are Body energy, Target.

The default record is Capture time or observation horizon: 0.778142 s; Terminal upright angle error: 1.33227e-15 rad; Peak body energy error: 2.05954 J. These computed values are a worked example for these settings, not acceptance limits for every experiment. Keep parameter values and units beside the result. A near-zero residual has meaning only in relation to the stated model and numerical precision.

## Two one-variable sweeps

1. Increase energy gain at fixed motor limit. Compare actual applied torque, energy growth and capture time. Once torque saturates, requested energy injection no longer scales freely with gain.

2. Increase torque authority at fixed energy gain. Check the capture event and terminal body state, but also inspect wheel motion. An improved body result may require unmodeled wheel speed or momentum capacity.

Return to defaults between sweeps. Hold the other control fixed and record both a changing output and an expected invariant. Explain the physical or numerical path from the selected input to the observed response.

## Intentionally broken case

The fault reverses the swing-up energy term. It still applies equal and opposite motor torques and uses the same state-dependent capture condition; the default run then fails to reach capture.

Run the same parameter values with the fault enabled. Compare complete curves as well as summary metrics. Identify the actual operation that changed and calculate why it affects the measured result. A changed warning label is not numerical evidence.

## Recovery

Restore the energy-pumping sign and reset the initial state. Verify the computed capture event, subsequent balance mode and body/wheel trajectories.

Repeat a saved nominal setting and confirm that its values and curves return. Recovery must restore the governing mechanism and its evidence, not merely clear a warning.

## Alternative and limiting cases

Exactly downward at zero rate, this energy law cannot initiate motion without a perturbation. No capture within twelve seconds is censored evidence, not a proof of impossibility. Wheel speed and position are unregulated and unlimited; successful body capture is not hardware qualification.

## Independent evidence and MATLAB-style design boundary

The reference integrates the coupled mass matrix in body and relative-wheel coordinates with RK45 and an independently expressed upright-angle event. Production integrates eliminated equations in absolute-wheel coordinates with DOP853. State conversion and body-energy traces are compared.

Five retained cases cover baseline, two single-control sweeps, the named fault and recovery. Expected values come from the independent formulation; actual values come from the executable lesson. Absolute and relative comparison tolerances remain 1e-8. Full-state or geometric checks supplement these three-number signatures, which alone cannot establish correctness. MATLAB has not been executed and no MATLAB equivalence is claimed. Browser and container evidence is recorded separately. Agreement between synthetic implementations does not establish empirical model validity.

## Engineering review checklist

Reconstruct one displayed quantity from the actual state or geometric arrays. Check coordinate ordering, signs and units before comparing numbers. Explain which assumption each check constrains, and identify a defect that another check could miss. Preserve the baseline, one controlled sweep, fault and recovery as a reproducible evidence sequence. State the model boundary before making a broader engineering recommendation.

## Common mistakes

Do not infer correctness from a changing headline alone. Exactly downward at zero rate, this energy law cannot initiate motion without a perturbation.

Do not change both sliders at once and attribute the result to one cause. Separate a model assumption from a measured property, and a finite-horizon observation from a universal guarantee. Floating-point roundoff is not a physical effect; equally, an attractive plot is not a substitute for the governing calculation.

## Focused check and teach-back

What makes this plant underactuated, and why is a captured body insufficient to claim a practical balanced robot?

Answer rationale: Two rotational coordinates share one equal-and-opposite internal motor torque. Capturing the body can leave substantial wheel motion; the model lacks wheel-speed and momentum limits, so body tracking alone cannot establish actuator feasibility.

Use the embedded Course checkpoint to explain your default, sweep, fault and recovery records to a colleague. Include one calculation with units, the causal diagnosis and an explicit untested boundary. This is a self-assessment; no learner score is stored.
