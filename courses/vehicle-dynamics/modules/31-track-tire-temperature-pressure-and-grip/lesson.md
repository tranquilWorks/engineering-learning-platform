# Track Tire Temperature, Pressure, and Grip

**Guiding question:** How do heat input, cooling, absolute pressure, and the grip window interact over a run?

Integrate a bounded thermal state, convert absolute temperature to pressure, and evaluate a temperature-pressure grip envelope. This is a competency-derived Python-first native design. It is not a source conversion, MATLAB-runtime comparison, rig test, track test, or measured-vehicle result.

## Why this lesson exists

The 24 source-bound lessons establish the surface workflow. This depth lesson requires a governing tire relation, a falsifiable invariant, a named failure, and independent evidence. State the frame, sign, unit, and synthetic-data assumptions before reading any curve.

## Model and equations

- `C_th*dT/dt=Q_in-h*(T-T_amb)`
- `p/p_0=T_K/T_0K`
- `mu=mu_peak*exp(-((T-T_opt)/w_T)^2)*(1-k_p*(p-p_opt)^2)`

All angles cross a labeled degree-to-radian boundary before trigonometric use. Longitudinal force is positive forward, lateral force follows the lesson's displayed convention, normal load is positive into the contact patch, and dissipated energy is nonnegative.

## Predict before running

Gas pressure scales with absolute Kelvin temperature, while stored thermal energy plus rejected heat equals supplied heat. Predict the direction of every signature change before moving a control.

## Baseline workflow

1. Run the defaults with broken mode disabled.
2. Read all signature metrics and their physical units.
3. Compare the response plot with the mechanism plot.
4. Check both limiting cases before accepting the interpretation.
5. Save the baseline so recovery can be compared exactly.

## Two one-variable sweeps

1. Hold ambient at 25 degC and sweep heat input from 0 to 2500 W.
2. Restore heat input to 900 W and sweep ambient from -10 to 45 degC.

Change only one variable per sweep. Attribute the change to one displayed equation rather than to visual resemblance.

## Intentionally broken case

Broken mode forms a pressure ratio from Celsius temperatures, creating a large physical-law residual even though the returned pressure remains finite. The broken case is an invalid counterexample, not an alternate tire calibration.

## Recovery

Convert both initial and current gas temperatures to Kelvin at the pressure boundary, then close the integrated thermal-energy balance. Recovery restores the exact baseline inputs and must restore the baseline signature.

## Limiting cases and invariants

- With zero heat input the tire remains at ambient temperature.
- At thermal steady state heat input equals convective loss.

Teaching invariant: Gas pressure scales with absolute Kelvin temperature, while stored thermal energy plus rejected heat equals supplied heat.

## Independent evidence

Expected signatures come from `expansion_reference_cases.py`, which imports no production experiment, consumes no production result, and perturbs no production value. Baseline, two one-variable sweeps, broken behavior, and exact recovery are retained separately. Agreement covers only these equations and bounded deterministic scenarios.

## Common mistakes

- Using Celsius in an absolute gas-law ratio.
- Interpreting the hottest tire as the highest-grip tire.
- Ignoring heat rejection when checking stored energy.
- Treating deterministic synthetic observations as measured tire, rig, track, or vehicle evidence.
- Extending this bounded teaching model beyond its stated validity range.

## Formative checks

- Why must pressure use Kelvin?
- At steady state, which two power terms are equal?
- Which plotted quantity would first reveal the named broken behavior?
- What evidence would still be required before using this relation for physical setup decisions?

## Teach-back

Derive one signature quantity from the displayed equations, explain exactly which invariant the broken case violates, and distinguish the model's software evidence from a measured tire validation claim.
