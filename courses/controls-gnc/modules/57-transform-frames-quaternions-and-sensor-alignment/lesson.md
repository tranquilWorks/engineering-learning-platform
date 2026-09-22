# Transform Frames, Quaternions, and Sensor Alignment

**Guiding question:** How do quaternion normalization and frame order prevent silent attitude and alignment errors?

Rotate a body vector by a yaw quaternion, apply a sensor misalignment, and verify norm and DCM orthogonality invariants. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{q=[cos(psi/2),0,0,sin(psi/2)]}$$
$$\text{v_n=R_nb v_b}$$
$$\text{R^T R=I and det R=1}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

A normalized quaternion produces an orthogonal proper rotation that preserves vector norm; alignment order remains explicit. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `sensor_misalignment_deg` at `3.0 deg` and sweep `yaw_angle_deg` from `-180.0` through `35.0` to `180.0 deg`.
2. Restore `yaw_angle_deg` to `35.0 deg` and sweep `sensor_misalignment_deg` from `0.0` through `3.0` to `20.0 deg`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode treats degrees as radians and scales the quaternion, violating the norm/orthogonality checks. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Convert units, normalize the quaternion, state active/passive frame order, and recheck vector norm and determinant. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- Zero yaw produces the identity rotation.
- Any proper rotation preserves Euclidean vector length.

Teaching invariant: A normalized quaternion produces an orthogonal proper rotation that preserves vector norm; alignment order remains explicit.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `yaw_angle_deg` from sensitivity to `sensor_misalignment_deg`.
