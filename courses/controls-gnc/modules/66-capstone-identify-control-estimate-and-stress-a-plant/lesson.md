# Capstone: Identify, Control, Estimate, and Stress a Plant

**Guiding question:** Can one evidence chain carry an identified model through controller, estimator, and uncertainty stress tests?

Reuse identification information, loop design, and covariance consistency to produce a requirements-traced software-only capstone verdict. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{identify theta from excitation}$$
$$\text{design K(theta_hat) and estimator covariance}$$
$$\text{stress delta in declared uncertainty set}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

The capstone passes only when identification conditioning, tracking error, estimator consistency, and actuator authority all pass their named requirements. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Requirements trace

- `ID-1`: the excitation-information condition proxy must be at least `2.0`; a stale model fails this requirement even if a downstream curve looks smooth.
- `CTRL-1`: worst normalized tracking error across the declared uncertainty family must remain below `0.35`.
- `ACT-1`: the control-effort proxy must not exceed the normalized authority limit `3.0`.
- `EST-1`: maximum NEES must remain below the declared consistency ceiling `6.0`.

The `requirements_passed` metric is the logical conjunction of these four booleans. No averaging or compensating trade is allowed, and the diagnostic payload retains every requirement value, operator, threshold, and verdict.

## Two one-variable sweeps

1. Hold `measurement_noise` at `0.1 1` and sweep `plant_uncertainty` from `0.0` through `0.2` to `0.8 1`.
2. Restore `plant_uncertainty` to `0.2 1` and sweep `measurement_noise` from `0.01` through `0.1` to `0.5 1`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode reuses a stale nominal model and underreports estimator covariance under the same uncertainty/noise stress. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Re-identify, redesign, and rerun the exact stress family; do not waive a failed upstream requirement. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- At zero uncertainty/noise the nominal chain reaches its numerical floor.
- A pass flag is the conjunction of traced requirements, not an average score.

Teaching invariant: The capstone passes only when identification conditioning, tracking error, estimator consistency, and actuator authority all pass their named requirements.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `plant_uncertainty` from sensitivity to `measurement_noise`.
