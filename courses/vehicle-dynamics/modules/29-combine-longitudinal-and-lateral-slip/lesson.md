# Combine Longitudinal and Lateral Slip

**Guiding question:** Why can two individually valid pure-slip forces become impossible when requested together?

Project simultaneous longitudinal and lateral tire demands onto a friction-circle constraint and inspect the remaining margin. This is a competency-derived Python-first native design. It is not a source conversion, MATLAB-runtime comparison, rig test, track test, or measured-vehicle result.

## Why this lesson exists

The 24 source-bound lessons establish the surface workflow. This depth lesson requires a governing tire relation, a falsifiable invariant, a named failure, and independent evidence. State the frame, sign, unit, and synthetic-data assumptions before reading any curve.

## Model and equations

- `F_x0=mu*F_z*tanh(C_kappa*kappa/(mu*F_z))`
- `F_y0=-mu*F_z*tanh(C_alpha*alpha/(mu*F_z))`
- `u_0=sqrt((F_x0/(mu*F_z))^2+(F_y0/(mu*F_z))^2)`
- `[F_x,F_y]=min(1,1/u_0)*[F_x0,F_y0]`

All angles cross a labeled degree-to-radian boundary before trigonometric use. Longitudinal force is positive forward, lateral force follows the lesson's displayed convention, normal load is positive into the contact patch, and dissipated energy is nonnegative.

## Predict before running

The delivered combined-force vector never exceeds unit friction utilization when both pure-slip demands share one contact patch. Predict the direction of every signature change before moving a control.

## Baseline workflow

1. Run the defaults with broken mode disabled.
2. Read all signature metrics and their physical units.
3. Compare the response plot with the mechanism plot.
4. Check both limiting cases before accepting the interpretation.
5. Save the baseline so recovery can be compared exactly.

## Two one-variable sweeps

1. Hold slip angle at 8 deg and sweep slip ratio from -0.30 to 0.30.
2. Restore slip ratio to 0.12 and sweep slip angle from -18 to 18 deg.

Change only one variable per sweep. Attribute the change to one displayed equation rather than to visual resemblance.

## Intentionally broken case

Broken mode delivers both pure-slip saturated forces independently, so the vector exceeds the one-contact-patch friction constraint. The broken case is an invalid counterexample, not an alternate tire calibration.

## Recovery

Compute the joint utilization before delivery, apply one common radial scale factor, and verify nonpositive constraint residual. Recovery restores the exact baseline inputs and must restore the baseline signature.

## Limiting cases and invariants

- With zero slip angle the combined model reduces to the pure longitudinal law.
- With zero slip ratio the combined model reduces to the pure lateral law.

Teaching invariant: The delivered combined-force vector never exceeds unit friction utilization when both pure-slip demands share one contact patch.

## Independent evidence

Expected signatures come from `expansion_reference_cases.py`, which imports no production experiment, consumes no production result, and perturbs no production value. Baseline, two one-variable sweeps, broken behavior, and exact recovery are retained separately. Agreement covers only these equations and bounded deterministic scenarios.

## Common mistakes

- Adding two pure-slip maxima without a shared constraint.
- Applying different arbitrary scale factors to longitudinal and lateral force.
- Using degrees directly inside the lateral-force hyperbolic tangent.
- Treating deterministic synthetic observations as measured tire, rig, track, or vehicle evidence.
- Extending this bounded teaching model beyond its stated validity range.

## Formative checks

- When is the common scale factor exactly one?
- Why must both force components receive the same radial scale?
- Which plotted quantity would first reveal the named broken behavior?
- What evidence would still be required before using this relation for physical setup decisions?

## Teach-back

Derive one signature quantity from the displayed equations, explain exactly which invariant the broken case violates, and distinguish the model's software evidence from a measured tire validation claim.
