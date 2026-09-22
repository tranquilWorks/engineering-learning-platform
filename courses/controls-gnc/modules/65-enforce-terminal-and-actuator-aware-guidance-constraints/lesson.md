# Enforce Terminal and Actuator-Aware Guidance Constraints

**Guiding question:** How do terminal requirements change when the actuator cannot deliver the unconstrained guidance command?

Compare required terminal acceleration with actuator authority and propagate the residual terminal miss under saturation. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{a_req=2 e/t_go^2+2 v_e/t_go}$$
$$\text{a_cmd=clip(a_req,a_max)}$$
$$\text{terminal cost=w_f e(tf)^2}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

The applied command never exceeds actuator authority; an infeasible terminal requirement must appear as residual error, not a hidden command. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `terminal_weight` at `8.0 1` and sweep `acceleration_limit_m_s2` from `3.0` through `20.0` to `50.0 m/s^2`.
2. Restore `acceleration_limit_m_s2` to `20.0 m/s^2` and sweep `terminal_weight` from `1.0` through `8.0` to `20.0 1`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode applies the unconstrained terminal command and reports zero miss despite violating actuator authority. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Restore saturation, propagate the constrained plant, and renegotiate terminal requirements when authority is insufficient. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- If required acceleration is within the limit, clipping is inactive.
- As time-to-go shrinks a fixed terminal error demands increasing acceleration.

Teaching invariant: The applied command never exceeds actuator authority; an infeasible terminal requirement must appear as residual error, not a hidden command.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `acceleration_limit_m_s2` from sensitivity to `terminal_weight`.
