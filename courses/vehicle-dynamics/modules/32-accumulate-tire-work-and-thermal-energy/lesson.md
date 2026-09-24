# Accumulate Tire Work and Thermal Energy

**Guiding question:** Where does contact-patch slip work go, and how can an energy ledger reveal a missing loss path?

Integrate longitudinal and lateral slip power into tire work, stored heat, rejected heat, and an energy-balance residual. This is a competency-derived Python-first native design. It is not a source conversion, MATLAB-runtime comparison, rig test, track test, or measured-vehicle result.

## Why this lesson exists

The 24 source-bound lessons establish the surface workflow. This depth lesson requires a governing tire relation, a falsifiable invariant, a named failure, and independent evidence. State the frame, sign, unit, and synthetic-data assumptions before reading any curve.

## Model and equations

- `P_slip=|F_x*v*kappa|+|F_y*v*tan(alpha)|`
- `E_work=integral(P_slip dt)`
- `E_work=Delta_E_thermal+E_loss`

All angles cross a labeled degree-to-radian boundary before trigonometric use. Longitudinal force is positive forward, lateral force follows the lesson's displayed convention, normal load is positive into the contact patch, and dissipated energy is nonnegative.

## Predict before running

Cumulative nonnegative slip work must equal stored thermal energy plus rejected heat over the same bounded interval. Predict the direction of every signature change before moving a control.

## Baseline workflow

1. Run the defaults with broken mode disabled.
2. Read all signature metrics and their physical units.
3. Compare the response plot with the mechanism plot.
4. Check both limiting cases before accepting the interpretation.
5. Save the baseline so recovery can be compared exactly.

## Two one-variable sweeps

1. Hold slip angle at 5 deg and sweep slip ratio from 0 to 0.20.
2. Restore slip ratio to 0.08 and sweep slip angle from 0 to 15 deg.

Change only one variable per sweep. Attribute the change to one displayed equation rather than to visual resemblance.

## Intentionally broken case

Broken mode omits heat rejection from the state update while the audit still evaluates the required loss path, producing a positive energy-balance residual. The broken case is an invalid counterexample, not an alternate tire calibration.

## Recovery

Restore heat rejection inside the same integration loop and verify work equals stored energy plus accumulated loss. Recovery restores the exact baseline inputs and must restore the baseline signature.

## Limiting cases and invariants

- At zero slip ratio and zero slip angle the slip power is zero.
- With zero heat-transfer coefficient all slip work remains stored as thermal energy.

Teaching invariant: Cumulative nonnegative slip work must equal stored thermal energy plus rejected heat over the same bounded interval.

## Independent evidence

Expected signatures come from `expansion_reference_cases.py`, which imports no production experiment, consumes no production result, and perturbs no production value. Baseline, two one-variable sweeps, broken behavior, and exact recovery are retained separately. Agreement covers only these equations and bounded deterministic scenarios.

## Common mistakes

- Dropping absolute value and allowing dissipative work to cancel.
- Mixing watts and kilowatts or seconds and hours.
- Computing loss for the report but omitting it from the thermal state.
- Treating deterministic synthetic observations as measured tire, rig, track, or vehicle evidence.
- Extending this bounded teaching model beyond its stated validity range.

## Formative checks

- Why is dissipated slip power nonnegative here?
- Which three cumulative energy terms must close?
- Which plotted quantity would first reveal the named broken behavior?
- What evidence would still be required before using this relation for physical setup decisions?

## Teach-back

Derive one signature quantity from the displayed equations, explain exactly which invariant the broken case violates, and distinguish the model's software evidence from a measured tire validation claim.
