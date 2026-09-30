# Time-Scale Two Joint Cubics Under Speed and Acceleration Limits



## Model, derivation, and conventions

`q_i=d_i(3s²-2s³); s=t/T`

`peak_speed=1.5 max|d_i|/T; peak_acceleration=6 max|d_i|/T²`

`T=max(1.5 max|d_i|/v_limit, sqrt(6 max|d_i|/a_limit))`

Two joints move from zero to displacements [d,-0.6d] rad using a shared normalized cubic. The displacement slider chooses d, and the other slider selects a common joint-speed bound in rad/s. Both joints have a fixed acceleration bound of 3 rad/s². The normalized coordinate s runs from zero to one. The polynomial h(s)=3s²-2s³ makes position continuous and sets velocity to zero at both endpoints. It does not set endpoint acceleration to zero.

Differentiating with actual elapsed time gives qdot=d*(6s-6s²)/T and qddot=d*(6-12s)/T² for each joint. The speed parabola peaks at s=0.5, where its coefficient is 1.5. Acceleration is linear and its greatest magnitude occurs at an endpoint, with coefficient six. These analytic extrema derive the two required durations. The selected duration is the larger of the speed-based and acceleration-based requirements, using the largest absolute displacement across joints.

The response plot shows the actual two joint velocities over zero to the applied duration, with their positive and negative speed bounds. The mechanism plot shows actual joint accelerations. Retained diagnostics also include accelerations, peak values, required duration and acceleration excess. The headline acceleration is a measured maximum absolute joint acceleration, not the declared bound. Speed violation is max(0, peak speed minus selected bound); a zero violation means that constraint is satisfied within floating-point precision, not that the trajectory uses all available speed.

At the default displacement 2 rad and speed bound 1.2 rad/s, speed requires T=2.5 s. Acceleration requires T=2 s. Applying T=2.5 s gives peak acceleration 1.92 rad/s², below its 3 rad/s² limit. A naive distance-over-speed duration would be approximately 1.667 s and would underestimate the cubic peak speed by a factor of 1.5. The second joint has a smaller displacement and therefore smaller absolute speed and acceleration under the shared timing.

This construction is minimum duration only within the fixed, synchronized cubic family and the stated independent kinematic bounds. It is not a globally time-optimal path parameterization and does not include actuator torque, gravity, obstacles or jerk constraints. Acceleration jumps when connecting this cubic to a stationary segment, so a robot requiring smooth jerk needs a different profile or transition construction. Keeping that boundary explicit prevents an easy kinematic calculation from being sold as a complete motion planner.

## Predict before running

Predict why distance divided by the speed limit is too short for a rest-to-rest cubic trajectory. Record the expected direction of change and an invariant before reading the computed result. State a condition under which the fault could be hidden, rather than assuming every faulty setting must look worse.

## Baseline workflow

Reset controls and disable the named fault. Use Joint-space path length = 2.0 rad; Joint speed limit = 1.2 rad/s. Read the response curve, then connect it to the mechanism curve using the governing equations.

Synchronized velocities plots Velocity (rad/s) against Time (s). Its series are Joint 1, Joint 2, Speed +, Speed −. Joint accelerations plots Acceleration (rad/s²) against Time (s). Its series are Joint 1, Joint 2.

The default record is Applied cubic duration: 2.5 s; Peak joint acceleration: 1.92 rad/s^2; Measured speed-limit excess: 0 rad/s. These computed values are a worked example for these settings, not acceptance limits for every experiment. Keep parameter values and units beside the result. A near-zero residual has meaning only in relation to the stated model and numerical precision.

## Two one-variable sweeps

1. Increase displacement while holding speed bound fixed. Compare the linear speed-duration requirement with the square-root acceleration-duration requirement; identify which one sets the applied time.

2. Increase speed allowance at fixed displacement. Duration eventually stops decreasing when acceleration becomes the active constraint. Confirm the plateau using computed acceleration rather than assuming the slider is ineffective.

Return to defaults between sweeps. Hold the other control fixed and record both a changing output and an expected invariant. Explain the physical or numerical path from the selected input to the observed response.

## Intentionally broken case

The fault applies a fixed one-second duration instead of the derived duration. It then differentiates the actual applied cubic, so speed and acceleration violations follow from the trajectory.

Run the same parameter values with the fault enabled. Compare complete curves as well as summary metrics. Identify the actual operation that changed and calculate why it affects the measured result. A changed warning label is not numerical evidence.

## Recovery

Restore derived timing and inspect both speed and acceleration constraints. A small speed excess alone cannot certify acceleration feasibility.

Repeat a saved nominal setting and confirm that its values and curves return. Recovery must restore the governing mechanism and its evidence, not merely clear a warning.

## Alternative and limiting cases

At zero displacement the trajectory is stationary; the interactive displacement range remains positive to keep a nonzero duration. A short move or generous limits can make one second feasible, so the named fault does not guarantee a violation at every setting. Endpoint acceleration is nonzero and torque limits are absent.

## Independent evidence and MATLAB-style design boundary

The reference constructs polynomial objects, differentiates them, and evaluates their extrema and sampled trajectories independently of the production explicit cubic formulas.

Five retained cases cover baseline, two single-control sweeps, the named fault and recovery. Expected values come from the independent formulation; actual values come from the executable lesson. Absolute and relative comparison tolerances remain 1e-8. Full-state or geometric checks supplement these three-number signatures, which alone cannot establish correctness. MATLAB has not been executed and no MATLAB equivalence is claimed. Browser and container evidence is recorded separately. Agreement between synthetic implementations does not establish empirical model validity.

## Engineering review checklist

Reconstruct one displayed quantity from the actual state or geometric arrays. Check coordinate ordering, signs and units before comparing numbers. Explain which assumption each check constrains, and identify a defect that another check could miss. Preserve the baseline, one controlled sweep, fault and recovery as a reproducible evidence sequence. State the model boundary before making a broader engineering recommendation.

## Common mistakes

Do not infer correctness from a changing headline alone. At zero displacement the trajectory is stationary; the interactive displacement range remains positive to keep a nonzero duration.

Do not change both sliders at once and attribute the result to one cause. Separate a model assumption from a measured property, and a finite-horizon observation from a universal guarantee. Floating-point roundoff is not a physical effect; equally, an attractive plot is not a substitute for the governing calculation.

## Focused check and teach-back

Why can increasing the allowed speed cease to shorten the move?

Answer rationale: The acceleration requirement then sets the shared duration. For the fixed cubic, speed scales as 1/T while acceleration scales as 1/T²; both constraints must be satisfied, and the larger required time wins.

Use the embedded Course checkpoint to explain your default, sweep, fault and recovery records to a colleague. Include one calculation with units, the causal diagnosis and an explicit untested boundary. This is a self-assessment; no learner score is stored.
