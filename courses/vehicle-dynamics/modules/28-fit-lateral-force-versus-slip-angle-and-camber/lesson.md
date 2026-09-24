# Fit Lateral Force versus Slip Angle and Camber

**Guiding question:** How can a two-input experiment distinguish slip-angle force from camber thrust?

Separate cornering and camber stiffness in a bounded lateral-force fit with an explicit SAE-style sign convention. This is a competency-derived Python-first native design. It is not a source conversion, MATLAB-runtime comparison, rig test, track test, or measured-vehicle result.

## Why this lesson exists

The 24 source-bound lessons establish the surface workflow. This depth lesson requires a governing tire relation, a falsifiable invariant, a named failure, and independent evidence. State the frame, sign, unit, and synthetic-data assumptions before reading any curve.

## Model and equations

- `F_y=clip(-(C_alpha*alpha+C_gamma*gamma),-mu*F_z,mu*F_z)`
- `[C_alpha_hat,C_gamma_hat]=argmin ||F_y+X*C||_2`
- `alpha_rad=pi*alpha_deg/180`

All angles cross a labeled degree-to-radian boundary before trigonometric use. Longitudinal force is positive forward, lateral force follows the lesson's displayed convention, normal load is positive into the contact patch, and dissipated energy is nonnegative.

## Predict before running

With independently varied slip angle and camber, the unsaturated design matrix separates cornering stiffness from camber stiffness in radians. Predict the direction of every signature change before moving a control.

## Baseline workflow

1. Run the defaults with broken mode disabled.
2. Read all signature metrics and their physical units.
3. Compare the response plot with the mechanism plot.
4. Check both limiting cases before accepting the interpretation.
5. Save the baseline so recovery can be compared exactly.

## Two one-variable sweeps

1. Hold camber stiffness at 9000 N/rad and sweep cornering stiffness.
2. Restore cornering stiffness to 70000 N/rad and sweep camber stiffness from 0 to 20000 N/rad.

Change only one variable per sweep. Attribute the change to one displayed equation rather than to visual resemblance.

## Intentionally broken case

Broken mode fits degree-valued angles as though they were radians, producing deceptively small stiffness estimates and a large radian-domain validation residual. The broken case is an invalid counterexample, not an alternate tire calibration.

## Recovery

Convert measured degrees to radians before constructing the regression matrix, retain independent alpha and camber excitation, and re-run held-out validation. Recovery restores the exact baseline inputs and must restore the baseline signature.

## Limiting cases and invariants

- At zero slip angle and zero camber the lateral force is zero.
- At zero camber stiffness only the slip-angle column contributes force.

Teaching invariant: With independently varied slip angle and camber, the unsaturated design matrix separates cornering stiffness from camber stiffness in radians.

## Independent evidence

Expected signatures come from `expansion_reference_cases.py`, which imports no production experiment, consumes no production result, and perturbs no production value. Baseline, two one-variable sweeps, broken behavior, and exact recovery are retained separately. Agreement covers only these equations and bounded deterministic scenarios.

## Common mistakes

- Mixing degrees and radians inside the design matrix.
- Changing slip angle and camber together so their effects are confounded.
- Extrapolating a linear fit beyond the clipped force boundary.
- Treating deterministic synthetic observations as measured tire, rig, track, or vehicle evidence.
- Extending this bounded teaching model beyond its stated validity range.

## Formative checks

- Why must alpha and camber vary independently?
- What unit should both fitted stiffness coefficients carry?
- Which plotted quantity would first reveal the named broken behavior?
- What evidence would still be required before using this relation for physical setup decisions?

## Teach-back

Derive one signature quantity from the displayed equations, explain exactly which invariant the broken case violates, and distinguish the model's software evidence from a measured tire validation claim.
