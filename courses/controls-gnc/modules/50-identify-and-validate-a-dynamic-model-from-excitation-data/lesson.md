# Identify and Validate a Dynamic Model from Excitation Data

**Guiding question:** How do excitation richness and held-out residuals determine whether an identified model is usable?

Relate an input information matrix to parameter uncertainty and validation residual without testing on the fit data. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{theta_hat=(Phi^T Phi)^-1 Phi^T y}$$
$$\text{cov(theta_hat) proportional (Phi^T Phi)^-1}$$
$$\text{validate on held-out input}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

Persistent excitation improves information conditioning, while held-out residual—not training fit—bounds the model claim. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `frequency_spread_hz` at `2.0 Hz` and sweep `excitation_amplitude` from `0.1` through `1.0` to `3.0 1`.
2. Restore `excitation_amplitude` to `1.0 1` and sweep `frequency_spread_hz` from `0.1` through `2.0` to `5.0 Hz`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode collapses excitation amplitude and frequency spread, making the regression nearly singular while still reporting a training fit. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Restore broadband excitation within safety limits and retain a separate validation segment. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- Zero excitation provides no parameter information.
- Increasing independent excitation directions reduces covariance conditioning.

Teaching invariant: Persistent excitation improves information conditioning, while held-out residual—not training fit—bounds the model claim.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `excitation_amplitude` from sensitivity to `frequency_spread_hz`.
