# Quantify Quantization and Sampling Jitter

**Guiding question:** How do amplitude quantization and clock jitter create different error signatures in sampled feedback data?

Sample a deterministic sinusoid on a jittered clock, quantize it, and separate level error from timing-induced phase error. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{Delta=V_FS/2^N}$$
$$\text{e_j approximately x_dot*delta_t}$$
$$\text{SNR=20 log10(rms(x)/rms(e))}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

Quantization error follows converter step size, while jitter error scales with signal slope and timing displacement. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `jitter_fraction` at `0.03 sample` and sweep `converter_bits` from `3.0` through `10.0` to `16.0 bit`.
2. Restore `converter_bits` to `10.0 bit` and sweep `jitter_fraction` from `0.0` through `0.03` to `0.45 sample`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode forces three bits and 0.45-sample deterministic jitter, making both staircase and phase displacement visible. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Restore adequate resolution and clock stability, then budget quantization and jitter as separate mechanisms before combining them. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- With zero jitter, timing error is zero at every sample.
- Each added ideal bit halves quantization step size.

Teaching invariant: Quantization error follows converter step size, while jitter error scales with signal slope and timing displacement.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `converter_bits` from sensitivity to `jitter_fraction`.
