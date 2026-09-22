# Propagate State Modes and Diagnose Numerical Conditioning

**Guiding question:** How do modal geometry and conditioning affect a state-transition calculation?

Propagate a two-mode state exactly, separate modal decay from eigenvector conditioning, and detect when a numerically fragile realization hides the physics. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{x(t)=V exp(Lambda t) V^-1 x(0)}$$
$$\text{Phi(t)=exp(A t)}$$
$$\text{kappa(V)=sigma_max(V)/sigma_min(V)}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

Modal decay rates remain the eigenvalues, while nearly parallel eigenvectors amplify reconstruction sensitivity without moving those eigenvalues. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Two one-variable sweeps

1. Hold `eigenvector_angle_deg` at `25.0 deg` and sweep `slow_mode_per_s` from `0.2` through `0.8` to `2.0 1/s`.
2. Restore `slow_mode_per_s` to `0.8 1/s` and sweep `eigenvector_angle_deg` from `2.0` through `25.0` to `80.0 deg`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode collapses the eigenvector angle toward one-half degree, creating an ill-conditioned realization whose modal coefficients become enormous. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Restore a separated eigenbasis or use a numerically balanced realization, then verify state propagation against the direct matrix reconstruction. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- At zero time the state transition is the identity.
- For an orthogonal modal basis the two-norm condition number is one.

Teaching invariant: Modal decay rates remain the eigenvalues, while nearly parallel eigenvectors amplify reconstruction sensitivity without moving those eigenvalues.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `slow_mode_per_s` from sensitivity to `eigenvector_angle_deg`.
