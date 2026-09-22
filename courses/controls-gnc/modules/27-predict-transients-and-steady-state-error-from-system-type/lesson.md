# Predict Transients and Steady-State Error from System Type

**Guiding question:** How do poles set transient specifications while loop type sets steady tracking error?

Measure overshoot and settling from a second-order servo, then connect its integrator and velocity constant to ramp error. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{T(s)=omega_n^2/(s^2+2*zeta*omega_n*s+omega_n^2)}$$
$$\text{M_p=exp(-pi*zeta/sqrt(1-zeta^2))}$$
$$\text{e_ramp=1/K_v=2*zeta/omega_n}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

For stable positive damping, increasing damping reduces overshoot while the type-one loop keeps zero step error and finite ramp error. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `natural_frequency_rad_s` at `3.0 rad/s` and sweep `damping_ratio` from `0.15` through `0.55` to `1.2 1`.
2. Restore `damping_ratio` to `0.55 1` and sweep `natural_frequency_rad_s` from `0.5` through `3.0` to `8.0 rad/s`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode reverses damping, moving the conjugate poles into the right half-plane so transient specifications no longer describe a settling response. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Restore positive damping, verify both poles are left-half-plane, and report steady error for the correct input class rather than from a finite snapshot. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- At zeta approaching one the underdamped overshoot tends to zero.
- Increasing natural frequency at fixed damping shortens settling and ramp error.

Teaching invariant: For stable positive damping, increasing damping reduces overshoot while the type-one loop keeps zero step error and finite ramp error.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `damping_ratio` from sensitivity to `natural_frequency_rad_s`.
