# Follow Waypoints and Paths with Line-of-Sight Guidance

**Guiding question:** How do lookahead and speed set cross-track convergence without commanding impossible curvature?

Apply line-of-sight path guidance to a straight segment and connect lookahead to heading command and exponential cross-track decay. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{chi_c=chi_path-atan(e_y/L)}$$
$$\text{e_y_dot approximately -(V/L)e_y}$$
$$\text{kappa_c=2 sin(eta)/L}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

Positive lookahead produces bounded heading commands and exponential local cross-track convergence for forward speed. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `vehicle_speed_m_s` at `8.0 m/s` and sweep `lookahead_distance_m` from `2.0` through `15.0` to `60.0 m`.
2. Restore `lookahead_distance_m` to `15.0 m` and sweep `vehicle_speed_m_s` from `1.0` through `8.0` to `25.0 m/s`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode reverses the cross-track sign, commanding divergence from the path. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Restore the frame/sign convention, select lookahead from curvature authority, and verify waypoint switching separately. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- As cross-track error tends to zero the heading command tends to path heading.
- Increasing lookahead reduces command aggressiveness and convergence rate.

Teaching invariant: Positive lookahead produces bounded heading commands and exponential local cross-track convergence for forward speed.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `lookahead_distance_m` from sensitivity to `vehicle_speed_m_s`.
