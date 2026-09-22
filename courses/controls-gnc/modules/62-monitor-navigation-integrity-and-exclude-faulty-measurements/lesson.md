# Monitor Navigation Integrity and Exclude Faulty Measurements

**Guiding question:** How do residual testing, protection levels, and fault exclusion bound a navigation solution?

Normalize a pseudorange fault, compare it with an integrity threshold, and measure residual reduction after exclusion. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{T=||S^-1/2 r||}$$
$$\text{alarm if T>T_gate}$$
$$\text{HPL=K_H sigma_H}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

A declared fault above threshold raises an alarm and the excluded solution must be recomputed before reporting a reduced residual. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `integrity_threshold` at `5.0 sigma` and sweep `fault_magnitude_m` from `0.0` through `18.0` to `60.0 m`.
2. Restore `fault_magnitude_m` to `18.0 m` and sweep `integrity_threshold` from `2.0` through `5.0` to `10.0 sigma`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode suppresses the alarm and retains the faulty measurement. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Restore residual monitoring, exclude the identified fault, recompute the solution, and keep protection-level assumptions explicit. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- With zero fault the normalized test statistic is zero.
- Exclusion cannot be credited unless a new solution and residual are calculated.

Teaching invariant: A declared fault above threshold raises an alarm and the excluded solution must be recomputed before reporting a reduced residual.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `fault_magnitude_m` from sensitivity to `integrity_threshold`.
