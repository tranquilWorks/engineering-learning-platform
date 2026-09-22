# Propagate Strapdown Inertial Navigation and IMU Error

**Guiding question:** How does a constant accelerometer bias grow into velocity and position error during strapdown propagation?

Integrate a declared body-axis bias, compare analytic error growth, and show the effect of a bias correction. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{delta_v=b_a t}$$
$$\text{delta_r=.5 b_a t^2}$$
$$\text{f_n=R_nb(f_b-b_hat)+g_n}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

Under constant uncorrected bias, velocity error grows linearly and position error quadratically with coast time. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `coast_duration_s` at `30.0 s` and sweep `accelerometer_bias_m_s2` from `0.0` through `0.03` to `0.2 m/s^2`.
2. Restore `accelerometer_bias_m_s2` to `0.03 m/s^2` and sweep `coast_duration_s` from `1.0` through `30.0` to `120.0 s`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode doubles the applied bias and disables the bias correction. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Estimate and subtract bias, reapply gravity/frame conventions, and compare propagation to the analytic limiting case. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- At zero duration both errors are zero.
- Doubling coast time quadruples constant-bias position error.

Teaching invariant: Under constant uncorrected bias, velocity error grows linearly and position error quadratically with coast time.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `accelerometer_bias_m_s2` from sensitivity to `coast_duration_s`.
