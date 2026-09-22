# Shape Sensitivity with Bode Loop Design

**Guiding question:** How does loop shape trade tracking and disturbance rejection against noise and control effort?

Compute S, T, PS, and CS for a lead-shaped type-one loop and expose the waterbed and effort penalties of excessive gain. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{S=1/(1+L)}$$
$$\text{T=L/(1+L)}$$
$$\text{PS=P*S and CS=C*S}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

S+T=1 pointwise; lowering low-frequency sensitivity necessarily changes complementary sensitivity and control effort elsewhere. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `lead_zero_rad_s` at `1.0 rad/s` and sweep `loop_gain` from `0.5` through `5.0` to `30.0 1`.
2. Restore `loop_gain` to `5.0 1` and sweep `lead_zero_rad_s` from `0.2` through `1.0` to `5.0 rad/s`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode closes the same loop with the wrong feedback sign, replacing 1+L by 1-L and producing a near-singular sensitivity peak. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Restore negative feedback and select crossover only after checking all four maps: S, T, PS, and CS. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- At low frequency the integrator drives S toward zero.
- At high frequency strictly proper L drives T toward zero and S toward one.

Teaching invariant: S+T=1 pointwise; lowering low-frequency sensitivity necessarily changes complementary sensitivity and control effort elsewhere.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `loop_gain` from sensitivity to `lead_zero_rad_s`.
