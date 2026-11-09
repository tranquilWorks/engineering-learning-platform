# P44 course checkpoint

## Predict and derive

Calculate wheel force and road speed at one engine operating point, then identify the active traction constraint.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `T_e=220-6e-6(n_e-4500)^2`
- `F_engine=T_e i_g i_0 eta/r_t`
- `F_delivered=min(F_engine,mu F_z_driven)`

## Controlled comparison

- `engine_rpm`: 5000 → 6200. Hold the other controls at baseline; predict and explain the change before executing.
- `gear_ratio`: 3.2 → 2.2. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

At 5000 rpm the declared torque map gives 218.5 N m. With gear 3.2, final drive 4.1, efficiency 0.92 and radius 0.31 m, available wheel force is about 8507.69 N. Driven-tire capacity is 1.15*1450*9.81*0.45, about 7361.18 N, so delivered force is capped. Raising gearing can increase available force without increasing delivered force in this regime. Check utilization and rpm-to-speed conversion together.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

The fixed driven-axle load omits longitudinal transfer and differential effects. It is not a complete launch simulation.

Competency links: VD-POWERTRAIN. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
