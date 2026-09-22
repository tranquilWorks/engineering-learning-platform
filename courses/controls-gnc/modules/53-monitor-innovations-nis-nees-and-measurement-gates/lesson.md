# Monitor Innovations, NIS, NEES, and Measurement Gates

**Guiding question:** How do consistency statistics distinguish expected residuals from outliers and filter overconfidence?

Normalize a deterministic innovation, compare NIS to a gate, and show why accepting a large outlier corrupts consistency. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{nu=z-H xhat}$$
$$\text{S=H P H^T+R}$$
$$\text{NIS=nu^T S^-1 nu}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

A measurement is accepted only when its NIS is inside the declared gate; NEES/NIS interpretation requires the corresponding covariance model. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `outlier_sigma` at `4.0 sigma` and sweep `nis_gate` from `1.0` through `6.63` to `15.0 1`.
2. Restore `nis_gate` to `6.63 1` and sweep `outlier_sigma` from `0.5` through `4.0` to `10.0 sigma`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode accepts the measurement regardless of a gate exceedance. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Restore innovation gating, log the rejection, and diagnose the model rather than silently shrinking covariance. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- A zero innovation has NIS zero.
- For a scalar residual measured in sigma, NIS is its squared magnitude.

Teaching invariant: A measurement is accepted only when its NIS is inside the declared gate; NEES/NIS interpretation requires the corresponding covariance model.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `nis_gate` from sensitivity to `outlier_sigma`.
