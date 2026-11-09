# P42 course checkpoint

## Predict and derive

Separate geometric travel effects from force-induced compliance and carry units through wheel-rate conversion.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `gamma=gamma_0+g_gamma z+c_gamma F_y`
- `toe=toe_0+g_toe z+c_toe F_y`
- `k_wheel=k_spring MR(z)^2`

## Controlled comparison

- `bump_travel_mm`: 25 → 50. Hold the other controls at baseline; predict and explain the change before executing.
- `lateral_force_n`: 3000 → 4500. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

At 25 mm and 3000 N, camber is -1-0.035*25-0.00004*3000=-1.995 deg. Toe is 0.10+0.004*25+0.00006*3000=0.38 deg. Motion ratio is 0.86, so wheel rate is 45000*0.86²=33282 N/m. The coefficients multiplying travel are per millimetre; dividing travel by 1000 without changing them corrupts geometry while leaving compliance unchanged. Use the two sweeps to separate those causes.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

These local affine kinematics/compliance maps are synthetic and do not solve a linkage or validate structural deflection.

Competency links: VD-RIDE-SUSPENSION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
