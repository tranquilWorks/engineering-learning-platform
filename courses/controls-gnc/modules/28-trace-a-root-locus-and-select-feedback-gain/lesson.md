# Trace a Root Locus and Select Feedback Gain

**Guiding question:** How can the root locus turn a gain choice into a pole-location and damping decision?

Trace every closed-loop branch for a three-pole plant with a movable zero and select gain from stability and damping evidence. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{1+K(s+z)/(s(s+2)(s+5))=0}$$
$$\text{sum(angles)=odd*pi}$$
$$\text{sigma_a=(sum poles-sum zeros)/(n-m)}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

All three branches start at open-loop poles, one terminates at the finite zero, and the remaining two follow the asymptotes from the centroid. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `zero_location_per_s` at `1.0 1/s` and sweep `loop_gain` from `0.1` through `4.0` to `60.0 1`.
2. Restore `loop_gain` to `4.0 1` and sweep `zero_location_per_s` from `0.2` through `1.0` to `4.0 1/s`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode applies the gain with the wrong feedback sign, moving one characteristic root into the right half-plane. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Move the gain marker back into the left-half-plane segment and verify dominant damping before accepting the time-domain design. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- As K tends to zero, roots approach 0, -2, and -5 per second.
- As K grows, one branch approaches the finite zero and two approach the asymptotes.

Teaching invariant: All three branches start at open-loop poles, one terminates at the finite zero, and the remaining two follow the asymptotes from the centroid.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `loop_gain` from sensitivity to `zero_location_per_s`.
