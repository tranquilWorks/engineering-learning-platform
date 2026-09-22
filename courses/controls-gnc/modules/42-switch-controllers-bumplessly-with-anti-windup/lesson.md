# Switch Controllers Bumplessly with Anti-Windup

**Guiding question:** How can a controller switch modes without a command jump and recover cleanly from saturation?

Switch a saturated PI loop from manual to automatic, track the actuator for bumpless initialization, and compare back-calculation recovery with windup. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{u_sat=clip(k_p e+z)}$$
$$\text{z_dot=k_i e+k_aw(u_sat-u_raw)}$$
$$\text{z_switch=u_manual-k_p e}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

Tracking initialization makes the auto command equal the manual command at the switch, and positive back-calculation bounds windup during saturation. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `actuator_limit` at `1.2 1` and sweep `antiwindup_gain_per_s` from `0.0` through `4.0` to `12.0 1/s`.
2. Restore `antiwindup_gain_per_s` to `4.0 1/s` and sweep `actuator_limit` from `0.4` through `1.2` to `3.0 1`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode disables tracking initialization and back-calculation, producing a mode-switch bump and a long saturated recovery. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Initialize the integral state from the actual manual actuator command and restore back-calculation before enabling automatic control. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- With exact tracking initialization the ideal switch bump is zero.
- Without saturation, the anti-windup correction term is zero.

Teaching invariant: Tracking initialization makes the auto command equal the manual command at the switch, and positive back-calculation bounds windup during saturation.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `antiwindup_gain_per_s` from sensitivity to `actuator_limit`.
