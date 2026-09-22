# Certify Decay with Lyapunov Functions and Regions of Attraction

**Guiding question:** How does a Lyapunov sublevel set become a defensible local region-of-attraction certificate?

Evaluate V=x²/2 for xdot=-x+mu*x³, find where Vdot is negative, and reject a sublevel that crosses the unstable boundary. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{V=x^2/2}$$
$$\text{V_dot=-x^2+mu*x^4}$$
$$\text{|x|<1/sqrt(mu)}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

A claimed sublevel is certified only when V is positive and Vdot is strictly negative everywhere except the origin. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `cubic_coefficient` at `0.8 1` and sweep `sublevel_radius` from `0.1` through `0.7` to `1.4 1`.
2. Restore `sublevel_radius` to `0.7 1` and sweep `cubic_coefficient` from `0.2` through `0.8` to `1.5 1`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode selects a sublevel outside the analytical decay region, making boundary Vdot positive. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Shrink the sublevel below 1/sqrt(mu) and report it as a sufficient local certificate, not the exact global basin. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- At the origin V and Vdot are zero.
- At |x|=1/sqrt(mu), Vdot reaches zero and strict decay is lost.

Teaching invariant: A claimed sublevel is certified only when V is positive and Vdot is strictly negative everywhere except the origin.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `sublevel_radius` from sensitivity to `cubic_coefficient`.
