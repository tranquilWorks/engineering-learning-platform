# Solve a GNSS Pseudorange Navigation Fix

**Guiding question:** How do receiver clock bias and satellite geometry jointly determine a pseudorange solution?

Relate range noise and geometry dilution to position/clock error and reject a near-collinear geometry. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{rho_i=||r-r_i||+c dt+epsilon_i}$$
$$\text{delta_x=(H^T H)^-1 H^T delta_rho}$$
$$\text{sigma_pos=GDOP*sigma_rho}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

A valid fix estimates position and clock bias together; geometry dilution scales range noise into state uncertainty. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `geometry_dilution` at `2.2 1` and sweep `pseudorange_noise_m` from `0.1` through `2.0` to `10.0 m`.
2. Restore `pseudorange_noise_m` to `2.0 m` and sweep `geometry_dilution` from `1.0` through `2.2` to `12.0 1`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode uses near-collinear geometry with dilution 25, making the normal equations practically singular. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Restore four-or-more diverse lines of sight, solve clock and position jointly, and inspect post-fit residuals. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- With zero range noise the linearized error bound tends to zero.
- Worse geometry increases position error without changing receiver measurement noise.

Teaching invariant: A valid fix estimates position and clock bias together; geometry dilution scales range noise into state uncertainty.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `pseudorange_noise_m` from sensitivity to `geometry_dilution`.
