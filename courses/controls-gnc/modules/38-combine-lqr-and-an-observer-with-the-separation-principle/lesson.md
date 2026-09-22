# Combine LQR and an Observer with the Separation Principle

**Guiding question:** Why can regulator and observer poles be designed separately, and when does the combined loop still fail?

Combine a stabilizing double-integrator feedback law with a full-order observer and verify the block-triangular separation spectrum. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{u=-K x_hat}$$
$$\text{x_hat_dot=A x_hat+B u+L(y-C x_hat)}$$
$$\text{eig(A_aug)=eig(A-BK) union eig(A-LC)}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

For the nominal linear model the combined estimator-controller eigenvalues are exactly the union of regulator and observer eigenvalues. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `observer_speed_ratio` at `3.0 1` and sweep `regulator_bandwidth_per_s` from `0.4` through `1.5` to `4.0 1/s`.
2. Restore `regulator_bandwidth_per_s` to `1.5 1/s` and sweep `observer_speed_ratio` from `1.2` through `3.0` to `8.0 1`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode reverses observer injection, placing an estimation-error pole in the right half-plane despite a stable regulator. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Restore the innovation sign, keep the observer faster but not arbitrarily ill-conditioned, and check the full augmented spectrum. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- With zero initial estimation error, nominal state feedback and observer feedback coincide.
- Separation guarantees nominal eigenvalues, not robustness to unmodeled dynamics or saturation.

Teaching invariant: For the nominal linear model the combined estimator-controller eigenvalues are exactly the union of regulator and observer eigenvalues.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `regulator_bandwidth_per_s` from sensitivity to `observer_speed_ratio`.
