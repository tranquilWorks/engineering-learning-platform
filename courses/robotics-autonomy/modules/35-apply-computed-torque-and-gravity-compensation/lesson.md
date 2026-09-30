# Integrate Computed Torque with Gravity Error and Saturation



## Model, derivation, and conventions

`M(q) qddot+C(q,qdot) qdot+g(q)=tau_applied`

`tau_requested=(1+epsilon)[M(a_d+2w(v_d-v)+w²(q_d-q))+Cv+g]`

`tau_applied=clip(tau_requested,-20,20)`

This experiment integrates the nonlinear dynamics of a planar two-link robot, not an assigned error decay. It uses point masses 1 and 0.8 kg at link endpoints, lengths 0.7 and 0.5 m, and downward gravity 9.81 m/s². Angles are relative joint coordinates measured from the horizontal. The physical inertia, Coriolis and gravity terms follow the same explicitly declared point-mass model as the preceding dynamics lesson, with no adjustable payload in this experiment.

The desired trajectory is q_d=[0.4+0.15sin(t),0.6+0.12cos(1.3t)] rad. Its first and second derivatives are analytic. Initial position is desired position plus [0.1,-0.08] rad and initial velocity is zero, which generally differs from desired velocity. The four-second state contains both actual joint positions and rates. At every integration evaluation, the controller computes a desired acceleration plus proportional and derivative feedback, then transforms that acceleration into torque through its model.

The model-error slider multiplies the controller's entire inverse-dynamics model by 1+epsilon. This is a deliberately simple correlated mismatch, not independent uncertainty in each link parameter. The plant retains its original physical parameters. With exact model, correct gravity sign and no saturation, substitution into the plant equation gives e_ddot+2w e_dot+w²e=0. That familiar critically damped relation is a conditional derivation; the executable plant continues to use nonlinear dynamics when those assumptions are violated.

Each requested joint torque is clipped to ±20 N m before entering the plant. Applied and requested torque arrays are both retained. High bandwidth can therefore demand more torque without receiving it, and a larger requested cancellation does not imply better tracking. The main metric is the root mean square of the joint-error vector norm across the 241 observation samples. Peak torque refers to applied torque, while gravity-compensation defect is the RMS norm of modeled gravity contribution minus actual gravity. The last metric isolates that contribution, rather than claiming to summarize all model error.

Broken mode reverses only the controller's gravity term before applying mismatch scaling and saturation. Physical gravity still acts downward in the plant. With zero mismatch this changes the requested gravity contribution from g to -g, so its cancellation defect is -2g at the actual state. The state itself changes under that faulty control, so the defect must be evaluated along the resulting trajectory. A constant multiplier applied to a precomputed nominal error would miss that causal interaction.

The experiment omits friction, flexible links, sensor delay and sampled actuator electronics. It provides a deterministic software example of computed torque and its assumptions. It cannot establish robustness margins or hardware safety from a four-second bounded trace.

## Predict before running

Predict why increasing feedback bandwidth may not reduce tracking error when requested torques exceed actuator limits. Record the expected direction of change and an invariant before reading the computed result. State a condition under which the fault could be hidden, rather than assuming every faulty setting must look worse.

## Baseline workflow

Reset controls and disable the named fault. Use Dynamics-model error = 0.08 1; Tracking bandwidth = 3.0 1/s. Read the response curve, then connect it to the mechanism curve using the governing equations.

Robot tracking errors plots Joint error (rad) against Time (s). Its series are Joint 1, Joint 2. Applied computed torque plots Torque (N·m) against Time (s). Its series are Joint 1, Joint 2.

The default record is Joint tracking RMS: 0.188043 rad; Peak applied torque: 13.9558 N*m; Gravity compensation RMS defect: 1.01834 N*m. These computed values are a worked example for these settings, not acceptance limits for every experiment. Keep parameter values and units beside the result. A near-zero residual has meaning only in relation to the stated model and numerical precision.

## Two one-variable sweeps

1. Increase model mismatch at fixed bandwidth. Compare actual tracking, requested versus applied torques and gravity defect. Attribute changes to the controller model while preserving the physical plant.

2. Increase bandwidth at fixed mismatch. Inspect whether applied torque reaches ±20 N m and explain any failure of the nominal error-law prediction using the saturated plant input.

Return to defaults between sweeps. Hold the other control fixed and record both a changing output and an expected invariant. Explain the physical or numerical path from the selected input to the observed response.

## Intentionally broken case

The controller subtracts modeled gravity where it should add it. The physical plant, reference trajectory and actuator limits remain unchanged, and the resulting state is integrated.

Run the same parameter values with the fault enabled. Compare complete curves as well as summary metrics. Identify the actual operation that changed and calculate why it affects the measured result. A changed warning label is not numerical evidence.

## Recovery

Restore the gravity sign, reset the same trajectory and compare state, applied torque and compensation defect. Keep mismatch visible rather than assuming restored gravity makes the model exact.

Repeat a saved nominal setting and confirm that its values and curves return. Recovery must restore the governing mechanism and its evidence, not merely clear a warning.

## Alternative and limiting cases

At zero mismatch and without saturation, computed torque yields the derived linear error equation. At a pose with zero gravity contribution the sign fault is locally hidden; along a trajectory it can reappear. Torque clipping invalidates exact cancellation even with an otherwise correct model.

## Independent evidence and MATLAB-style design boundary

The reference computes inverse dynamics from Cartesian point accelerations and Newton-Euler force moments. It obtains inertia columns through unit accelerations and integrates with RK45, independently of the production analytic M/C/g formulation and DOP853 integration.

Five retained cases cover baseline, two single-control sweeps, the named fault and recovery. Expected values come from the independent formulation; actual values come from the executable lesson. Absolute and relative comparison tolerances remain 1e-8. Full-state or geometric checks supplement these three-number signatures, which alone cannot establish correctness. MATLAB has not been executed and no MATLAB equivalence is claimed. Browser and container evidence is recorded separately. Agreement between synthetic implementations does not establish empirical model validity.

## Engineering review checklist

Reconstruct one displayed quantity from the actual state or geometric arrays. Check coordinate ordering, signs and units before comparing numbers. Explain which assumption each check constrains, and identify a defect that another check could miss. Preserve the baseline, one controlled sweep, fault and recovery as a reproducible evidence sequence. State the model boundary before making a broader engineering recommendation.

## Common mistakes

Do not infer correctness from a changing headline alone. At zero mismatch and without saturation, computed torque yields the derived linear error equation.

Do not change both sliders at once and attribute the result to one cause. Separate a model assumption from a measured property, and a finite-horizon observation from a universal guarantee. Floating-point roundoff is not a physical effect; equally, an attractive plot is not a substitute for the governing calculation.

## Focused check and teach-back

Why can exact parameters still fail to produce the nominal critically damped tracking error?

Answer rationale: The derivation assumes the requested torque reaches the plant. Clipping changes that input and leaves an uncompensated acceleration. Compare requested and applied torque along the actual trajectory before applying the linear error equation.

Use the embedded Course checkpoint to explain your default, sweep, fault and recovery records to a colleague. Include one calculation with units, the causal diagnosis and an explicit untested boundary. This is a self-assessment; no learner score is stored.
