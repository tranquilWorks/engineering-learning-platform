# Measure MIMO Interaction, Zeros, and Decoupling

**Guiding question:** How do relative gain, transmission zeros, and decoupling residual reveal multivariable limitations?

Analyze a coupled two-input/two-output plant with RGA, frequency singular values, transmission zeros, and regularized static decoupling. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{Lambda=G(0) elementwise (G(0)^-T)}$$
$$\text{det G(z)=0 defines transmission zeros}$$
$$\text{D=(G(0)+epsilon I)^-1}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

RGA rows and columns sum to one for a nonsingular plant, while decoupling residual grows when coupling or regularization prevents exact inversion. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `decoupler_regularization` at `0.02 1` and sweep `cross_coupling` from `0.0` through `0.6` to `1.3 1`.
2. Restore `cross_coupling` to `0.6 1` and sweep `decoupler_regularization` from `0.0` through `0.02` to `0.3 1`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode omits the decoupler and treats diagonal loop closures as independent despite measured cross-coupling. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Compute RGA and transmission zeros first, then use a conditioned decoupler and report its off-diagonal residual rather than claiming perfect separation. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- At zero coupling the DC RGA is diagonal.
- With zero regularization and nonsingular DC gain, static inversion has zero algebraic residual.

Teaching invariant: RGA rows and columns sum to one for a nonsingular plant, while decoupling residual grows when coupling or regularization prevents exact inversion.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `cross_coupling` from sensitivity to `decoupler_regularization`.
