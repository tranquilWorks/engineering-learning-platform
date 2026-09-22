# Solve Finite-Horizon and Time-Varying LQR

**Guiding question:** How does backward Riccati propagation turn future terminal cost into a time-varying feedback gain?

Integrate a scalar time-varying Riccati equation backward from terminal cost and compare its gain schedule with the invalid forward construction. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{-P_dot=2A(t)P-P^2/R+Q}$$
$$\text{P(t_f)=S_f}$$
$$\text{K(t)=R^-1 B^T P(t)}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

Finite-horizon optimal feedback is obtained from the terminal boundary backward; the terminal Riccati value must equal the declared terminal weight. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `terminal_weight` at `6.0 1` and sweep `horizon_s` from `1.0` through `4.0` to `10.0 s`.
2. Restore `horizon_s` to `4.0 s` and sweep `terminal_weight` from `0.0` through `6.0` to `20.0 1`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode marches the terminal condition forward from the initial time, violating the boundary-value problem and producing the wrong initial gain. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Restore backward integration from the actual terminal boundary and verify P(tf)=Sf before interpreting the gain schedule. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- At terminal time P equals the terminal weight exactly.
- As horizon grows in a time-invariant stable case, early gains approach the infinite-horizon solution.

Teaching invariant: Finite-horizon optimal feedback is obtained from the terminal boundary backward; the terminal Riccati value must equal the declared terminal weight.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `horizon_s` from sensitivity to `terminal_weight`.
