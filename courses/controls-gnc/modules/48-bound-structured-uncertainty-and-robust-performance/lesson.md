# Bound Structured Uncertainty and Robust Performance

**Guiding question:** How can a declared real-parameter family support a narrow robust-stability statement without becoming a certification claim?

Sweep a first-order pole uncertainty, calculate the worst closed-loop margin and sensitivity proxy, and expose a destabilizing gain choice. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{p(delta)=-(1+delta)}$$
$$\text{lambda_cl=p(delta)-K}$$
$$\text{margin=min_delta -Re(lambda_cl)}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

A robust statement is valid only for every member of the explicitly swept uncertainty family and the stated performance metric. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `feedback_gain` at `1.5 1` and sweep `uncertainty_radius` from `0.0` through `0.3` to `0.9 1`.
2. Restore `uncertainty_radius` to `0.3 1` and sweep `feedback_gain` from `0.1` through `1.5` to `4.0 1`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode applies the feedback with the wrong sign, allowing the least-stable family member to cross right half-plane. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Restore the sign, recompute the worst member, and report the finite family and margin rather than general robust certification. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- At zero uncertainty the family collapses to the nominal plant.
- Worst margin occurs at an interval endpoint for this affine scalar family.

Teaching invariant: A robust statement is valid only for every member of the explicitly swept uncertainty family and the stated performance metric.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `uncertainty_radius` from sensitivity to `feedback_gain`.
