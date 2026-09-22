# Compare Pursuit Laws and Proportional-Navigation Variants

**Guiding question:** When does proportional navigation outperform pure pursuit, and how do sign and target maneuver alter miss distance?

Compare PN navigation constant and target-turn demand using closing-speed and LOS-rate conventions. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{a_n=N V_c lambda_dot}$$
$$\text{V_c=-R_dot>0 for closing}$$
$$\text{augmented PN adds target acceleration estimate}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

For a closing engagement with correct LOS-rate sign, N greater than two reduces the nonmaneuvering miss proxy while increasing acceleration demand. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `target_turn_rate_deg_s` at `4.0 deg/s` and sweep `navigation_constant` from `1.0` through `3.5` to `6.0 1`.
2. Restore `navigation_constant` to `3.5 1` and sweep `target_turn_rate_deg_s` from `0.0` through `4.0` to `15.0 deg/s`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode reverses closing-speed sign, steering away from the intercept geometry. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Restore the frame and closing convention, apply actuator limits, and compare pursuit laws under the same target maneuver. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- At zero LOS rate classical PN commands zero lateral acceleration.
- Target maneuver increases required acceleration and residual miss when not estimated.

Teaching invariant: For a closing engagement with correct LOS-rate sign, N greater than two reduces the nonmaneuvering miss proxy while increasing acceleration demand.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `navigation_constant` from sensitivity to `target_turn_rate_deg_s`.
