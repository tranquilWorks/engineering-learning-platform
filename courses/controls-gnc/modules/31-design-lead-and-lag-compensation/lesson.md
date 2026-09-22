# Design Lead and Lag Compensation

**Guiding question:** How do lead and lag networks change phase, crossover, and low-frequency authority?

Place a lead network around a target frequency, add lag for low-frequency gain, and verify phase and magnitude contributions separately. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{C_lead=(1+s/z_l)/(1+s/p_l), p_l>z_l}$$
$$\text{phi_max=sin^-1((1-alpha)/(1+alpha))}$$
$$\text{C_lag=(1+s/z_g)/(1+s/p_g), p_g<z_g}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

A correctly ordered lead pole and zero add positive phase, while lag raises low-frequency gain relative to high frequency. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `lag_beta` at `5.0 1` and sweep `lead_alpha` from `0.05` through `0.2` to `0.8 1`.
2. Restore `lead_alpha` to `0.2 1` and sweep `lag_beta` from `1.2` through `5.0` to `12.0 1`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode swaps the lead pole and zero, turning the intended phase lead into phase lag. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Restore p_lead greater than z_lead, confirm positive phase at the target frequency, then add lag below crossover. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- As alpha tends to one, lead phase tends to zero.
- At zero frequency the chosen lag network has gain beta.

Teaching invariant: A correctly ordered lead pole and zero add positive phase, while lag raises low-frequency gain relative to high frequency.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `lead_alpha` from sensitivity to `lag_beta`.
