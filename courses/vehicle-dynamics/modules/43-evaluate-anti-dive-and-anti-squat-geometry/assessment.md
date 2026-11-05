# P43 course checkpoint

## Predict and derive

Show that anti geometry changes the path carrying pitch transfer rather than the total transfer itself.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `anti_dive=eta_b tan(theta) L/h`
- `anti_squat=eta_d tan(theta) L/h`
- `Delta F_z=Delta F_geometry+Delta F_spring`

## Controlled comparison

- `sideview_angle_deg`: 5 → 7. Hold the other controls at baseline; predict and explain the change before executing.
- `cg_height_m`: 0.52 → 0.65. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Total longitudinal transfer is m*a*h/L. The declared anti-dive fraction is 0.70*tan(angle)*L/h, while anti-squat omits the 0.70 brake-distribution factor. Geometric and spring-supported contributions must sum to total transfer even when a fraction exceeds one and the spring contribution changes sign. At 5 degrees, use tan(5*pi/180), not tan(5). Explain why changing height affects both the total demand and the anti percentage.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

These side-view force-line approximations omit suspension motion, force migration and transient pitch; anti percentage is not a braking-capacity gain.

Competency links: VD-RIDE-SUSPENSION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
