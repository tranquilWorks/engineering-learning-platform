# Fit Longitudinal Force versus Slip Ratio

**Guiding question:** How do low-slip slope and saturated force identify different parts of a longitudinal tire law?

Identify stiffness and peak friction from deterministic synthetic offline slip data, then validate on held-out slip ratios. This is a competency-derived Python-first native design. It is not a source conversion, MATLAB-runtime comparison, rig test, track test, or measured-vehicle result.

## Why this lesson exists

The 24 source-bound lessons establish the surface workflow. This depth lesson requires a governing tire relation, a falsifiable invariant, a named failure, and independent evidence. State the frame, sign, unit, and synthetic-data assumptions before reading any curve.

## Model and equations

- `F_x=clip(C_kappa*kappa,-mu*F_z,mu*F_z)`
- `C_kappa_hat=argmin sum(F_x-C*kappa)^2 on unsaturated samples`
- `mu_hat=max(|F_x|)/F_z`

All angles cross a labeled degree-to-radian boundary before trigonometric use. Longitudinal force is positive forward, lateral force follows the lesson's displayed convention, normal load is positive into the contact patch, and dissipated energy is nonnegative.

## Predict before running

Low-slip samples identify longitudinal stiffness while saturated samples identify peak friction; slip ratio is dimensionless, not percent. Predict the direction of every signature change before moving a control.

## Baseline workflow

1. Run the defaults with broken mode disabled.
2. Read all signature metrics and their physical units.
3. Compare the response plot with the mechanism plot.
4. Check both limiting cases before accepting the interpretation.
5. Save the baseline so recovery can be compared exactly.

## Two one-variable sweeps

1. Hold peak friction at 1.15 and sweep true stiffness from 30000 to 140000 N.
2. Restore stiffness to 80000 N and sweep peak friction from 0.70 to 1.50.

Change only one variable per sweep. Attribute the change to one displayed equation rather than to visual resemblance.

## Intentionally broken case

Broken mode treats percent slip as a dimensionless ratio during fitting, shrinking the reported stiffness by one hundred and failing held-out prediction in the declared unit. The broken case is an invalid counterexample, not an alternate tire calibration.

## Recovery

Use dimensionless slip ratio at both fit and validation boundaries, retain low-slip and saturated samples, and recheck the held-out residual. Recovery restores the exact baseline inputs and must restore the baseline signature.

## Limiting cases and invariants

- At zero slip ratio the longitudinal force is zero.
- With no saturated samples peak friction is not independently identifiable.

Teaching invariant: Low-slip samples identify longitudinal stiffness while saturated samples identify peak friction; slip ratio is dimensionless, not percent.

## Independent evidence

Expected signatures come from `expansion_reference_cases.py`, which imports no production experiment, consumes no production result, and perturbs no production value. Baseline, two one-variable sweeps, broken behavior, and exact recovery are retained separately. Agreement covers only these equations and bounded deterministic scenarios.

## Common mistakes

- Using percent values where the equation expects a ratio.
- Estimating stiffness only from saturated samples.
- Reporting training fit without a held-out force residual.
- Treating deterministic synthetic observations as measured tire, rig, track, or vehicle evidence.
- Extending this bounded teaching model beyond its stated validity range.

## Formative checks

- Which samples carry stiffness information?
- Why does a percent-versus-ratio defect corrupt the parameter even if a plot still saturates?
- Which plotted quantity would first reveal the named broken behavior?
- What evidence would still be required before using this relation for physical setup decisions?

## Teach-back

Derive one signature quantity from the displayed equations, explain exactly which invariant the broken case violates, and distinguish the model's software evidence from a measured tire validation claim.
