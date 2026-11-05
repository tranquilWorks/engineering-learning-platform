# P16 course checkpoint

## Predict and derive

Derive speed scaling for aerodynamic force and power, then distribute downforce between axles.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `Rational coefficient-area scaling and complementary axle-load accounting`

## Controlled comparison

- `speed_m_s`: 40.0 → 10.0. Hold the other controls at baseline; predict and explain the change before executing.
- `wing_angle_deg`: 8.0 → 18.0. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

At fixed coefficients, force is proportional to v² and drag power to v³. Doubling speed therefore gives four times drag but eight times drag power. Front and rear downforce must sum to the total, and their lever arms determine pitch moment. More downforce can improve grip while consuming power through drag; neither an axle split nor a favorable sign creates free energy.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

The coefficient map is synthetic and excludes stall, pitch dynamics, wind and measured aerodynamic validation.

Competency links: VD-AERO-ENERGY. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.


# Retained scoped evidence task

# P16 evidence task

## Reconstruct the default operating point

Before running, calculate dynamic pressure at 40 m/s and the two coefficient-area products at 8 degrees. Carry Pa and m² through the force calculation, then multiply drag by speed to obtain power. Reproduce approximately 731.08 N drag, 646.8 N downforce and 29243.2 W drag power demand. Explain why joining these three numbers on one generic SI axis would obscure their meanings.

Calculate front aero share and divide downforce into front and rear contributions. Add the separate 53/47 static-weight distribution to obtain total axle normal loads. Verify both the aero-force sum and total normal-load sum, and explain what each check can and cannot detect.

## Two controlled sweeps

First hold 8 degrees and compare speeds 20 and 40 m/s. Predict the force and power ratios before inspecting the plots. Check fourfold aerodynamic force and eightfold drag power. Explain why total constant-mu tire capacity does not grow by a factor of four: its static-weight term does not scale with speed.

Then hold 40 m/s and compare wing settings 0, 8 and 18 degrees. Use the common force-axis secondary sweep to distinguish the linear downforce-area trend from the quadratic drag-area trend. Quantify the 8-to-18 degree tradeoff: approximately 441 N additional downforce and 15288 W additional drag power. State why those gains and costs alone do not establish an optimal setting.

## Failure and same-input recovery

At the default setting, activate the fault without moving either control. Record negative drag power, a −129.36 N rear aero contribution, and a still-positive rear total normal load of approximately 5956.764 N. Check that total downforce and aggregate capacity can still sum correctly. Identify the sign and allocation checks needed to detect the error. Disable the fault at the same inputs, verify recovery, and reset separately afterward.

## Reasoning rubric

A complete explanation keeps force and power dimensions separate, derives the speed exponents, accounts for static weight, and distinguishes aero contribution from total normal load. It detects the fault even when aggregate sums agree and names the constant-mu/empirical-coefficient limitations.

An incomplete explanation treats negative rear aero contribution as automatic wheel lift, calls a larger wing setting universally better, or scales total capacity as V². Revise those claims from the declared equations and your selected evidence. This formative task records no completion claim: no learner score is stored, and no measured aero, tire qualification or whole-course acceptance is implied.
