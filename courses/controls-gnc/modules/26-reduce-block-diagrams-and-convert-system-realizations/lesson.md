# Reduce Block Diagrams and Convert System Realizations

**Guiding question:** When are transfer, state-space, and reduced block descriptions actually equivalent?

Compare a third-order transfer function with a controllable realization and quantify the danger of canceling a merely nearby pole and zero. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{G(s)=(s+2)/((s+1)(s+2+delta)(s+4))}$$
$$\text{G(s)=C(sI-A)^-1B}$$
$$\text{G_red(s)=1/((s+1)(s+4)) only when delta=0}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

A valid realization matches the unreduced transfer function, while exact cancellation is permitted only at zero pole-zero distance. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `max_frequency_rad_s` at `20.0 rad/s` and sweep `pole_offset_per_s` from `0.0` through `0.0` to `1.0 1/s`.
2. Restore `pole_offset_per_s` to `0.0 1/s` and sweep `max_frequency_rad_s` from `5.0` through `20.0` to `50.0 rad/s`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode performs the cancellation regardless of pole offset and presents the reduced response as exact. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Retain the third state whenever the pole-zero distance is nonzero, then compare frequency responses before accepting a reduced realization. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- At zero offset the cancellation is algebraically exact.
- As offset grows, the naive reduced model develops a measurable low-frequency bias.

Teaching invariant: A valid realization matches the unreduced transfer function, while exact cancellation is permitted only at zero pole-zero distance.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `pole_offset_per_s` from sensitivity to `max_frequency_rad_s`.
