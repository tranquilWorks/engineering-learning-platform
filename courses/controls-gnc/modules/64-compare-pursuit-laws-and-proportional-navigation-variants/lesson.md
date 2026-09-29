# Compare Civilian Moving-Beacon Guidance Trajectories



## Model and equations

`Rdot=r·vrel/||r||; lambda_dot=cross(r,vrel)/||r||²`

`a_PN=N max(-Rdot,0) lambda_dot; heading_dot=a/3`

`a_pursuit=v_p k_heading wrap(lambda-heading); v_p=3 m/s; k_heading=1.5/s`

`a_augmented=a_PN+(N/2) v_beacon omega_beacon cos(heading_beacon-heading); v_beacon=1 m/s`

A civilian point-mass follower starts at (0,0) with heading zero and speed 3 m/s. A moving beacon starts at (12,4) m with heading 0.6 rad and speed 1 m/s. The selected beacon turn rate is constant. Each guidance law integrates its own Cartesian trajectory, using the same starting conditions. The PN acceleration is normal to follower velocity and uses positive closing speed. Heading pursuit turns in proportion to wrapped heading error. The augmented comparison adds a declared projection of known beacon lateral acceleration; it is an educational feed-forward variant, not an optimality claim. Integration ends at one-metre separation or eight seconds. Each result retains 121 samples over its actual observation duration. A sampled closest separation of one metre often means that the capture event stopped integration, not that all laws have identical continuous trajectories. Initial range is sqrt(160), approximately 12.65 m.

## Predict before running

Predict how reversing the measured line-of-sight rate changes the initial PN command and the integrated path.

## Baseline workflow

Reset controls and leave the named fault disabled. Use PN navigation constant = 3.5 1; Beacon turn rate = 4.0 deg/s. Write a prediction before executing. Read the response curve first, then explain it using the mechanism curve.

Moving-beacon separation plots Separation (m) against Time (s). Its series are pursuit, pn, augmented. Executed lateral commands plots Acceleration (m/s²) against Time (s). Its series are pursuit, pn, augmented.

The computed default record is Initial PN command: 0.637911 m/s^2; Sampled closest PN separation: 1 m; PN observation duration: 5.79445 s; Peak sampled PN acceleration: 0.637911 m/s^2. These values are a reproducible worked example, not acceptance thresholds for every slider setting. Retain units and parameter values when comparing another run. A displayed residual near machine precision should be interpreted with the stated model and numerical tolerance.

## Two one-variable sweeps

1. Increase navigation constant from 1 to 6 while holding beacon turn fixed. Compare command demand, actual capture duration and separation history. Do not infer universal performance from one sampled minimum.

2. Increase beacon turn rate from zero to 15 degrees per second at fixed navigation constant. Compare pursuit, PN and the feed-forward variant over their own observation windows.

Return to defaults between sweeps. Keep the other control fixed, record the changed quantity and identify an expected invariant. A control need not change every output; explain the model path through which it acts.

## Intentionally broken case

Broken mode reverses the LOS-rate sign in PN and augmented PN while preserving both controls and the pursuit comparison.

Run the same selected controls with the fault enabled. Compare the curve shape as well as the numerical summary. The fault is a specific executed operation; a red warning or a changed mode flag would not by itself demonstrate its consequence.

## Recovery

Restore the rate sign and defaults. Confirm the initial command reverses back and inspect the resulting trajectory duration and separation curve.

Repeat one previously saved nominal setting and check that its values and curves return. Recovery should restore the mechanism, not merely dismiss the warning.

## Limiting cases and invariants

Capture is a one-metre event, not zero-distance contact. Closest approach is sampled. No actuator saturation, collision planning, sensor noise or universal capture guarantee is included. A comparison ending early has a shorter observation window.

## Independent evidence

The independent reference integrates range, LOS angle and both headings in relative polar coordinates with a different numerical integrator, rather than replaying the Cartesian production state.

Five retained cases cover baseline, two single-control sweeps, the named fault and recovery. Expected values are generated independently; actual values come from the executable lesson. Absolute and relative tolerances remain 1e-8. Agreement checks the declared synthetic model, not empirical validity. MATLAB has not been executed and no MATLAB equivalence is claimed. Browser and container evidence are recorded separately from numerical evidence.

## Engineering review checklist

Check the declared coordinates, units and ordering before evaluating the result. Reconstruct at least one displayed value from retained state or geometric data. Identify which output changes in each sweep and which should remain invariant. Diagnose the named faulty operation, then demonstrate its recovery. Finally state the strongest claim supported by these observations and one claim that requires additional evidence.

## Common mistakes

Do not infer correctness from a changing headline alone. In this lesson, the critical limit is: Capture is a one-metre event, not zero-distance contact. Closest approach is sampled. No actuator saturation, collision planning, sensor noise or universal capture guarantee is included. A comparison ending early has a shorter observation window.

Do not compare two runs after changing both controls and attribute the difference to one cause. Do not treat a near-zero floating-point residual as symbolic identity, or a finite sample sweep as a proof for all configurations. Keep the operation that creates the evidence separate from the interpretation assigned to it.

## Teach-back

Why can two laws have the same one-metre minimum yet different guidance performance?

Answer rationale: Both may reach the declared capture event, which terminates their integrations at the same radius. Capture time, command demand and trajectory history still differ; the threshold is not a fabricated miss metric.

Use the embedded Course checkpoint to collect a default record, a sweep, a faulty record and a recovered record. Explain the evidence to a colleague using the governing relation and units, then name the untested boundary. This is a self-assessment; no learner score is stored.
