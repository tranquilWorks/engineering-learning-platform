# P51 course checkpoint

## Predict and derive

Predict how ride height shifts aero balance while speed changes all force magnitudes.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `C_Lf=0.58-2.2(h_f[m]-0.080)`
- `F_df=0.5 rho A v^2 C_Lf and F_dr=0.5 rho A v^2 C_Lr`
- `balance_f=F_df/(F_df+F_dr) and M_pitch=1.50 F_dr-1.20 F_df`

## Controlled comparison

- `speed_m_s`: 45 → 65. Hold the other controls at baseline; predict and explain the change before executing.
- `front_ride_height_mm`: 80 → 110. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

At 80 mm, front coefficient is 0.58 and rear 0.72, so front balance is 0.58/1.30, about 44.62 percent. Dynamic pressure times area scales both with v². The pitch moment is rear force*1.5-front force*1.2; balance percentage alone does not determine its sign without lever arms. A millimetre value used as metres can yield absurd coefficients even though the v² scaling remains intact.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

The affine ride-height map has no stall, ground-contact, pitch or wind dynamics and is not measured aerodynamics.

Competency links: VD-AERO-ENERGY. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
