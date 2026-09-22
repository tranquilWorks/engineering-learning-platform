# Analyze Navigation Observability and Alignment Calibration

**Guiding question:** Which maneuvers make heading and sensor bias separately observable?

Build a two-parameter alignment information matrix from changing headings and quantify rank and conditioning. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{Y=[cos psi,1] [theta,bias]^T}$$
$$\text{I=Y^T R^-1 Y}$$
$$\text{rank(I)=2 requires heading diversity}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

Heading/bias calibration requires maneuver diversity; repeated geometry cannot separate the two parameters regardless of sample count. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `measurement_noise` at `0.05 1` and sweep `maneuver_span_deg` from `0.0` through `60.0` to `180.0 deg`.
2. Restore `maneuver_span_deg` to `60.0 deg` and sweep `measurement_noise` from `0.005` through `0.05` to `0.3 1`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode removes the maneuver span, collapsing the information matrix rank. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Execute a sufficiently diverse calibration maneuver and reject a covariance result from rank-deficient geometry. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- At zero heading span determinant is zero.
- Reducing measurement noise scales information but cannot repair missing rank.

Teaching invariant: Heading/bias calibration requires maneuver diversity; repeated geometry cannot separate the two parameters regardless of sample count.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `maneuver_span_deg` from sensitivity to `measurement_noise`.
