# Schedule Gains Across Operating Points

**Guiding question:** When does interpolation across operating points improve control, and what does a schedule fail to guarantee?

Schedule inverse plant gain across a nonlinear operating coordinate and quantify interpolation and closed-loop bandwidth error. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{g(rho)=1+.5*rho^2}$$
$$\text{K(rho)=2/g(rho)}$$
$$\text{lambda_cl=-g(rho)K(rho)}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

At tabulated points the inverse-gain schedule restores the target bandwidth; interpolation error must be measured between points. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `grid_spacing` at `0.25 1` and sweep `operating_point` from `0.0` through `0.5` to `1.0 1`.
2. Restore `operating_point` to `0.5 1` and sweep `grid_spacing` from `0.05` through `0.25` to `0.5 1`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode freezes the sea-level gain while evaluating the highest-gain operating point. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Restore interpolation, test the grid midpoints, and keep stability claims within the scheduled envelope. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- At rho=0 the schedule equals the nominal gain.
- As grid spacing tends to zero interpolation approaches the exact inverse schedule.

Teaching invariant: At tabulated points the inverse-gain schedule restores the target bandwidth; interpolation error must be measured between points.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `operating_point` from sensitivity to `grid_spacing`.
