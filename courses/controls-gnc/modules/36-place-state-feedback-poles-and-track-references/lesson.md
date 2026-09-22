# Place State-Feedback Poles and Track References

**Guiding question:** How do controllability, pole placement, and a reference precompensator combine in a state-feedback servo?

Place both double-integrator poles analytically, compute the DC reference precompensator, and separate eigenvalue assignment from command tracking. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{u=-Kx+Nbar*r}$$
$$\text{det(sI-(A-BK))=(s+p_1)(s+p_2)}$$
$$\text{Nbar=-1/(C(A-BK)^-1 B)}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

Controllability permits both poles to be assigned, but unit steady reference tracking requires the separately computed precompensator. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `pole_ratio` at `2.0 1` and sweep `dominant_pole_per_s` from `0.5` through `2.0` to `6.0 1/s`.
2. Restore `dominant_pole_per_s` to `2.0 1/s` and sweep `pole_ratio` from `1.1` through `2.0` to `5.0 1`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode keeps the placed poles but replaces the precompensator with one, producing a steady command scale error. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Retain the stabilizing gain and restore the DC precompensator, then verify both eigenvalues and final-value tracking. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- For the double integrator K=[p1*p2,p1+p2].
- The precompensator changes command gain without moving feedback poles.

Teaching invariant: Controllability permits both poles to be assigned, but unit steady reference tracking requires the separately computed precompensator.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `dominant_pole_per_s` from sensitivity to `pole_ratio`.
