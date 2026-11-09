# P28 course checkpoint

## Predict and derive

Show why slip-angle and camber excitation must be distinguishable to estimate two stiffnesses.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `F_y=clip(-(C_alpha*alpha+C_gamma*gamma),-mu*F_z,mu*F_z)`
- `[C_alpha_hat,C_gamma_hat]=argmin ||F_y+X*C||_2`
- `alpha_rad=pi*alpha_deg/180`

## Controlled comparison

- `cornering_stiffness_n_rad`: 70000 → 120000. Hold the other controls at baseline; predict and explain the change before executing.
- `camber_stiffness_n_rad`: 9000 → 18000. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

The design matrix has columns alpha and gamma, both in radians, and force is C_alpha*alpha+C_gamma*gamma. If gamma is proportional to alpha, the columns lose rank and only a combination of stiffnesses is identifiable. One degree is pi/180 rad, so a 70000 N/rad coefficient predicts about 1221.73 N per degree in the uncapped linear region. Check held-out predictions and units for both coefficients.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

This linear superposition omits saturation, combined slip and temperature; low residual alone does not certify a tire.

Competency links: VD-TIRE-LAT. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
