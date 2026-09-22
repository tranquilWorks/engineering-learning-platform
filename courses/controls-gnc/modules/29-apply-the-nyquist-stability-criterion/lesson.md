# Apply the Nyquist Stability Criterion

**Guiding question:** How do open-loop right-half-plane poles and encirclements determine closed-loop stability?

Close a Nyquist contour for an unstable open-loop plant, count the winding of -1, and reconcile it with closed-loop poles. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{L(s)=K(s+1)/((s-p)(s+2)(s+3))}$$
$$\text{N=Z-P}$$
$$\text{Delta arg(1+L)=2*pi*N}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

The winding count of 1+L equals closed-loop right-half-plane poles minus open-loop right-half-plane poles under the stated contour convention. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `unstable_pole_per_s` at `0.5 1/s` and sweep `loop_gain` from `0.2` through `6.0` to `20.0 1`.
2. Restore `loop_gain` to `6.0 1` and sweep `unstable_pole_per_s` from `0.1` through `0.5` to `1.5 1/s`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode reduces gain below the stabilizing range while ignoring the plant's one open-loop right-half-plane pole. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Count P before inspecting the curve, choose gain whose encirclement satisfies N=Z-P, and confirm Z from the characteristic polynomial. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- At very high frequency the strictly proper loop approaches the origin.
- A marginal crossing through -1 invalidates a casual integer winding count and needs a detour.

Teaching invariant: The winding count of 1+L equals closed-loop right-half-plane poles minus open-loop right-half-plane poles under the stated contour convention.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `loop_gain` from sensitivity to `unstable_pole_per_s`.
