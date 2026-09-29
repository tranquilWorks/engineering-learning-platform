# Project Configurations and Velocities onto a Circle Constraint



## Model, derivation, and conventions

`h(q)=||q||-1 m=0; J_h=q^T/||q||`

`P=I-J_h^T(J_h J_h^T)^-1 J_h; v=P[1,0]^T m/s`

`clearance=||q-[1.5,0.5] m||-0.2 m`

The configuration q is a point in a two-dimensional Cartesian plane, measured in metres. It is constrained to a circle of radius one metre. This is a holonomic constraint because it is an equation of configuration, without a path-dependent velocity condition. The slider named joint span selects an angular interval around zero; it does not create an articulated-arm joint model. We sample 121 angles from minus half the span to plus half the span. Raw configurations lie at radius one plus the selected offset. Normal mode divides each raw vector by its norm, projecting it radially onto the unit circle. The raw and used configurations are both retained, so a control that disappears from the projected result still has a visible causal role.

The constraint Jacobian is the unit outward radial row vector. Its rank is one everywhere in this experiment because no sampled configuration is zero. Two ambient coordinates minus one independent constraint leave a one-dimensional tangent space. The requested candidate velocity is [1,0] m/s. Orthogonal projection removes its radial component. At angle zero, q=[1,0] and the requested velocity points entirely outward; the projected velocity is zero. At angle pi/2, q=[0,1] and the same requested velocity is already tangent, so it remains [1,0]. At angle pi/4, the result is [0.5,-0.5] m/s. These three hand calculations explain the radial-velocity mechanism plot without relying on a headline score.

An obstacle is a disk centred at [1.5,0.5] m with radius 0.2 m. Clearance is the Euclidean centre distance minus that radius, evaluated at each used configuration. The minimum metric is over the displayed samples only. The arc is generated from angle, not by integrating the projected velocity. Consequently the plot does not claim that the candidate velocity traces that arc or avoids the obstacle over future time.

## Predict before running

Predict which quantities remain invariant when only the radial offset changes in normal mode, and whether tangency guarantees clearance.

## Baseline workflow

Reset controls and leave the named fault disabled. Use Constraint offset = 0.08 m; Joint span = 1.2 rad. Write a prediction before executing. Read the response curve first, then explain it using the mechanism curve.

Configuration projection plots Configuration y (m) against Configuration x (m). Its series are Raw configurations, Used configurations, Unit-radius constraint. Velocity tangency plots Radial velocity (m/s) against Configuration angle (rad). Its series are Used candidate velocity, Requested radial part.

The computed default record is Maximum radius constraint residual: 2.22045e-16 m; Measured tangent dimension: 1 count; Minimum sampled obstacle clearance: 0.381143 m. These values are a reproducible worked example, not acceptance thresholds for every slider setting. Retain units and parameter values when comparing another run. A displayed residual near machine precision should be interpreted with the stated model and numerical tolerance.

## Two one-variable sweeps

1. Increase radial offset from zero to 0.2 m with span fixed. The raw arc moves outward, while normal projection returns the same unit-circle arc. Confirm nearly zero constraint residual and unchanged projected clearance; an invariant output can be correct when the preprocessing intentionally removes the changed coordinate.

2. Increase angular span with offset fixed. The samples cover more of the circle, changing radial components of the requested velocity and potentially the minimum sampled obstacle clearance. Compare the location of the smallest clearance rather than assuming wider span is always safer.

Return to defaults between sweeps. Keep the other control fixed, record the changed quantity and identify an expected invariant. A control need not change every output; explain the model path through which it acts.

## Intentionally broken case

Broken mode bypasses both radial configuration projection and velocity projection. The Jacobian and its actual rank are still computed at the used configuration; the fault does not invent an extra tangent dimension.

Run the same selected controls with the fault enabled. Compare the curve shape as well as the numerical summary. The fault is a specific executed operation; a red warning or a changed mode flag would not by itself demonstrate its consequence.

## Recovery

Disable broken mode, restore defaults and compare raw versus used configurations. Check both radius residual and radial velocity; repairing the position alone would leave the velocity condition unverified.

Repeat one previously saved nominal setting and check that its values and curves return. Recovery should restore the mechanism, not merely dismiss the warning.

## Alternative and limiting cases

At zero offset the broken configuration already lies on the circle, so its radius residual can vanish while its unprojected velocity is still wrong. The Jacobian rank remains one. First-order tangency describes an instantaneous velocity and does not establish finite-step constraint preservation or collision avoidance.

## Independent evidence and MATLAB-style design boundary

The independent signature uses the analytic polar radius and obstacle distance. Physical tests use the tangent basis [-sin(theta),cos(theta)] to reconstruct velocity, separately from the production matrix projector.

Five retained cases cover baseline, two single-control sweeps, the named fault and recovery. Expected values are generated independently; actual values come from the executable lesson. Absolute and relative tolerances remain 1e-8. Agreement checks the declared synthetic model, not empirical validity. MATLAB has not been executed and no MATLAB equivalence is claimed. Browser and container evidence are recorded separately from numerical evidence.

## Engineering review checklist

Check the declared coordinates, units and ordering before evaluating the result. Reconstruct at least one displayed value from retained state or geometric data. Identify which output changes in each sweep and which should remain invariant. Diagnose the named faulty operation, then demonstrate its recovery. Finally state the strongest claim supported by these observations and one claim that requires additional evidence.

## Common mistakes

Do not infer correctness from a changing headline alone. In this lesson, the critical limit is: At zero offset the broken configuration already lies on the circle, so its radius residual can vanish while its unprojected velocity is still wrong. The Jacobian rank remains one. First-order tangency describes an instantaneous velocity and does not establish finite-step constraint preservation or collision avoidance.

Do not compare two runs after changing both controls and attribute the difference to one cause. Do not treat a near-zero floating-point residual as symbolic identity, or a finite sample sweep as a proof for all configurations. Keep the operation that creates the evidence separate from the interpretation assigned to it.

## Focused check and teach-back

At q=[1,0] m, why does projecting [1,0] m/s produce zero, and why can zero radius error fail to diagnose the broken mode?

Answer rationale: The requested velocity is wholly normal to the constraint and has no tangent component. With zero input offset the configuration is already valid, but a nonzero outward velocity violates J_h v=0. Both configuration and velocity evidence are needed.

Use the embedded Course checkpoint to collect a default record, a sweep, a faulty record and a recovered record. Explain the evidence to a colleague using the governing relation and units, then name the untested boundary. This is a self-assessment; no learner score is stored.
