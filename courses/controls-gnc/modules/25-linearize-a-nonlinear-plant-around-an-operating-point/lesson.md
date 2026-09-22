# Linearize a Nonlinear Plant Around an Operating Point

**Guiding question:** How do equilibrium residual and local Taylor error make or break a linear model?

Balance a nonlinear pendulum, derive its Jacobian, and measure the neighborhood where the local model is credible. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{tau_g=m*g*l*sin(theta)}$$
$$\text{delta_x_dot=A*delta_x+B*delta_tau}$$
$$\text{A21=-(g/l)*cos(theta_0)}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

The balanced operating point has zero residual, and Taylor error decreases quadratically as the perturbation radius shrinks. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `perturbation_rad` at `0.2 rad` and sweep `operating_angle_rad` from `-1.0` through `0.45` to `1.0 rad`.
2. Restore `operating_angle_rad` to `0.45 rad` and sweep `perturbation_rad` from `0.02` through `0.2` to `0.8 rad`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode omits the equilibrium torque, so the supposedly linearized origin accelerates before any perturbation is applied. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Restore the balancing torque, recompute the Jacobian at the same angle, and shrink the perturbation until the nonlinear and tangent torques agree. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- At zero perturbation the nonlinear and tangent torques coincide.
- At theta_0=0 the small-angle stiffness is g/l.

Teaching invariant: The balanced operating point has zero residual, and Taylor error decreases quadratically as the perturbation radius shrinks.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `operating_angle_rad` from sensitivity to `perturbation_rad`.
