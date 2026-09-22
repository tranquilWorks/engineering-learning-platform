# Augment an Integral Servo and Limit Commands

**Guiding question:** How does integral augmentation reject constant load without ignoring actuator limits?

Simulate an integral servo under constant disturbance, measure saturation, and distinguish zero steady bias from feasible command authority. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{z_dot=r-y}$$
$$\text{u=clip(k_p(r-y)+k_i z,u_min,u_max)}$$
$$\text{x_dot=-x+u+d}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

When command authority exceeds the constant load, integral state drives steady error toward zero; saturation duration still records feasibility cost. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `command_limit_m_s2` at `2.0 m/s^2` and sweep `integral_gain_per_s` from `0.1` through `1.2` to `4.0 1/s`.
2. Restore `integral_gain_per_s` to `1.2 1/s` and sweep `command_limit_m_s2` from `0.4` through `2.0` to `5.0 m/s^2`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode disconnects the integral state while retaining the load, leaving the proportional servo with a visible steady bias. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Reconnect integral augmentation, verify the command limit exceeds the load, and wait for the error and integrator derivative to settle. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- With zero integral gain the load produces proportional steady error.
- If the command limit is below the load, no controller can remove the bias.

Teaching invariant: When command authority exceeds the constant load, integral state drives steady error toward zero; saturation duration still records feasibility cost.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `integral_gain_per_s` from sensitivity to `command_limit_m_s2`.
