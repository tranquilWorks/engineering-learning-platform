# Cancel Nonlinearities with Feedback Linearization

**Guiding question:** What remains after model-based nonlinear cancellation, and how does mismatch re-enter the error dynamics?

Cancel a quadratic drift, impose first-order tracking dynamics, and expose residual drift under coefficient mismatch. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{x_dot=c*x^2+u}$$
$$\text{u=-c_hat*x^2-k(x-r)}$$
$$\text{e_dot=-k*e+(c-c_hat)x^2}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

Exact cancellation leaves the selected linear error dynamics; model mismatch appears explicitly as residual nonlinear drift. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `tracking_gain_per_s` at `2.0 1/s` and sweep `model_mismatch` from `0.0` through `0.08` to `0.5 1`.
2. Restore `model_mismatch` to `0.08 1` and sweep `tracking_gain_per_s` from `0.2` through `2.0` to `6.0 1/s`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode reverses the cancellation term, doubling rather than removing the nonlinear drift. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Restore the cancellation sign, bound parameter mismatch, and verify the residual over the stated state interval. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- At x=0 the quadratic cancellation term is zero.
- With exact model and positive k the tracking error decays exponentially.

Teaching invariant: Exact cancellation leaves the selected linear error dynamics; model mismatch appears explicitly as residual nonlinear drift.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `model_mismatch` from sensitivity to `tracking_gain_per_s`.
