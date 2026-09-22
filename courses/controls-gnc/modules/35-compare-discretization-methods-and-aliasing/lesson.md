# Compare Discretization Methods and Aliasing

**Guiding question:** Which continuous-time behaviors survive ZOH, Tustin, and Euler discretization at a chosen sample rate?

Map a stable pole three ways, expose explicit-Euler instability, and distinguish discrete pole error from input-frequency aliasing. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{z_ZOH=exp(a*T_s)}$$
$$\text{z_Tustin=(1+a*T_s/2)/(1-a*T_s/2)}$$
$$\text{f_alias=wrap(f,[-f_s/2,f_s/2])}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

ZOH maps the autonomous pole exactly, Tustin preserves stability, and any sampled sinusoid is indistinguishable from its Nyquist-folded alias. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `input_frequency_hz` at `3.0 Hz` and sweep `sample_period_s` from `0.01` through `0.08` to `0.6 s`.
2. Restore `sample_period_s` to `0.08 s` and sweep `input_frequency_hz` from `0.2` through `3.0` to `15.0 Hz`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode forces a 0.6-second Euler step for a -3 per-second pole, making the discrete Euler pole cross outside the unit circle. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Reduce the sample period or use a stability-preserving mapping, then place the antialias boundary before sampling. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- All consistent mappings approach 1+a*T_s as T_s tends to zero.
- A tone below Nyquist retains its original sampled frequency.

Teaching invariant: ZOH maps the autonomous pole exactly, Tustin preserves stability, and any sampled sinusoid is indistinguishable from its Nyquist-folded alias.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `sample_period_s` from sensitivity to `input_frequency_hz`.
