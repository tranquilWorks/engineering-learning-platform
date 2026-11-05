# P32 course checkpoint

## Predict and derive

Derive dissipated slip power and close accumulated work against stored heat plus cooling.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `P_slip=|F_x*v*kappa|+|F_y*v*tan(alpha)|`
- `E_work=integral(P_slip dt)`
- `E_work=Delta_E_thermal+E_loss`

## Controlled comparison

- `slip_ratio`: 0.08 → 0.18. Hold the other controls at baseline; predict and explain the change before executing.
- `slip_angle_deg`: 5 → 14. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Longitudinal slip work rate is the magnitude of Fx*v*kappa; lateral slip work rate uses Fy*v*tan(alpha). Each is newtons times metres per second, hence watts. Integrate those rates over time and compare with C*(T-T0) plus rejected heat. Removing cooling from the temperature update while continuing to report it in the ledger double-counts energy removal. A nonnegative power trace alone cannot prove thermal closure.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Constant forces and lumped heat capacity exclude changing grip, wear and spatial temperature fields.

Competency links: VD-TIRE-LONG, VD-TIRE-LAT, VD-AERO-ENERGY. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
