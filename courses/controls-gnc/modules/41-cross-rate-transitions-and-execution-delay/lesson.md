# Cross Rate Transitions and Execution Delay

**Guiding question:** How do zero-order hold age and execution delay accumulate in a multirate control path?

Move a command from a slow task to a fast plant, measure data age and phase lag, and expose incoherent read/write timing. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{u_fast[k]=u_slow[floor(k/M)]}$$
$$\text{delay phase=-omega*tau}$$
$$\text{age=t_read-t_sample}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

A coherent rate transition never uses future data; maximum age is bounded by one slow period plus execution delay. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `execution_delay_ms` at `12.0 ms` and sweep `rate_ratio` from `2.0` through `5.0` to `20.0 1`.
2. Restore `rate_ratio` to `5.0 1` and sweep `execution_delay_ms` from `0.0` through `12.0` to `80.0 ms`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode combines the maximum rate ratio and delay with a one-frame stale read, exceeding the declared coherent age bound. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Use an explicit hold/buffer handoff, timestamp every sample, and include execution delay in the phase-margin budget. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- At rate ratio one, hold error vanishes before execution delay.
- At zero delay, phase lag from execution is zero but hold age remains.

Teaching invariant: A coherent rate transition never uses future data; maximum age is bounded by one slow period plus execution delay.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `rate_ratio` from sensitivity to `execution_delay_ms`.
