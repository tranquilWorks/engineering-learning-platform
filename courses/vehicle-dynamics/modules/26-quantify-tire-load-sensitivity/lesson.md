# Quantify Tire Load Sensitivity

**Guiding question:** Why can the total tire capacity fall when axle load is redistributed but its total stays fixed?

Use a sublinear peak-force law to distinguish friction coefficient from force capacity and expose load-transfer loss. This is a competency-derived Python-first native design. It is not a source conversion, MATLAB-runtime comparison, rig test, track test, or measured-vehicle result.

## Why this lesson exists

The 24 source-bound lessons establish the surface workflow. This depth lesson requires a governing tire relation, a falsifiable invariant, a named failure, and independent evidence. State the frame, sign, unit, and synthetic-data assumptions before reading any curve.

## Model and equations

- `F_peak(F_z)=mu_ref*F_ref*(F_z/F_ref)^n`
- `mu(F_z)=F_peak(F_z)/F_z`
- `Delta_F=2*F_peak(F_z)-F_peak(F_z*(1-lambda))-F_peak(F_z*(1+lambda))`

All angles cross a labeled degree-to-radian boundary before trigonometric use. Longitudinal force is positive forward, lateral force follows the lesson's displayed convention, normal load is positive into the contact patch, and dissipated energy is nonnegative.

## Predict before running

For an exponent below one, peak force grows with normal load while effective friction falls, and unequal load sharing reduces paired capacity. Predict the direction of every signature change before moving a control.

## Baseline workflow

1. Run the defaults with broken mode disabled.
2. Read all signature metrics and their physical units.
3. Compare the response plot with the mechanism plot.
4. Check both limiting cases before accepting the interpretation.
5. Save the baseline so recovery can be compared exactly.

## Two one-variable sweeps

1. Hold exponent at 0.88 and sweep normal load from 1000 to 7000 N.
2. Restore 3500 N and sweep the exponent from 0.70 to 1.00.

Change only one variable per sweep. Attribute the change to one displayed equation rather than to visual resemblance.

## Intentionally broken case

Broken mode silently forces the exponent to one, erasing load sensitivity and the paired-capacity penalty while still returning finite forces. The broken case is an invalid counterexample, not an alternate tire calibration.

## Recovery

Restore the reviewed exponent, compare equal and split pairs at identical total load, and verify the documented power-law scaling ratio. Recovery restores the exact baseline inputs and must restore the baseline signature.

## Limiting cases and invariants

- At exponent one the force law is linear and load-transfer loss is zero.
- At zero load-transfer fraction the even and split paired capacities are identical.

Teaching invariant: For an exponent below one, peak force grows with normal load while effective friction falls, and unequal load sharing reduces paired capacity.

## Independent evidence

Expected signatures come from `expansion_reference_cases.py`, which imports no production experiment, consumes no production result, and perturbs no production value. Baseline, two one-variable sweeps, broken behavior, and exact recovery are retained separately. Agreement covers only these equations and bounded deterministic scenarios.

## Common mistakes

- Treating friction coefficient and peak force as the same quantity.
- Comparing two tires without holding their total normal load fixed.
- Assuming a linear force law after observing a sublinear exponent.
- Treating deterministic synthetic observations as measured tire, rig, track, or vehicle evidence.
- Extending this bounded teaching model beyond its stated validity range.

## Formative checks

- What happens to effective friction as load rises for n below one?
- Why must the paired loss vanish at n equals one?
- Which plotted quantity would first reveal the named broken behavior?
- What evidence would still be required before using this relation for physical setup decisions?

## Teach-back

Derive one signature quantity from the displayed equations, explain exactly which invariant the broken case violates, and distinguish the model's software evidence from a measured tire validation claim.
