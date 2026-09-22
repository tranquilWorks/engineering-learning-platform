# Estimate Nonlinear State with an Extended Kalman Filter

**Guiding question:** When is a first-order measurement linearization informative enough for an EKF update?

Update a scalar state through z=x², track the Jacobian and posterior covariance, and expose the unobservable zero-Jacobian initialization. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{h(x)=x^2}$$
$$\text{H=2*xhat}$$
$$\text{K=P H/(H^2 P+R)}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

An EKF update uses the local Jacobian; at xhat=0 the quadratic measurement has zero first-order sensitivity despite nonzero global information. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `linearization_state` at `1.0 1` and sweep `prior_standard_deviation` from `0.05` through `0.5` to `2.0 1`.
2. Restore `prior_standard_deviation` to `0.5 1` and sweep `linearization_state` from `0.0` through `1.0` to `3.0 1`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode freezes the Jacobian at zero, so the filter ignores the nonlinear measurement. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Move to an observable linearization or use an estimator that represents the nonlinear transform, then recheck innovation consistency. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- At xhat=0 the first-order Jacobian is zero.
- As prior variance tends to zero, the measurement gain tends to zero.

Teaching invariant: An EKF update uses the local Jacobian; at xhat=0 the quadratic measurement has zero first-order sensitivity despite nonzero global information.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `prior_standard_deviation` from sensitivity to `linearization_state`.
